"""Check queue (Owner 2026-11-25): one check at a time, later uploads wait in upload order."""
import threading
import time

from src.portal import processing


def test_one_at_a_time_in_upload_order(monkeypatch):
    monkeypatch.setattr(processing, "max_concurrent", lambda: 1)
    running, peak, order = [0], [0], []
    lock = threading.Lock()

    def fake(cid):
        with lock:
            running[0] += 1; peak[0] = max(peak[0], running[0]); order.append(cid)
        time.sleep(0.05)
        with lock:
            running[0] -= 1

    monkeypatch.setattr(processing, "_run_check", fake)
    with processing._queue_cond:                       # reserve places as uploads arrive
        processing._queue_waiting.update([3, 1, 2])
    threads = [threading.Thread(target=processing.run_check, args=(i,)) for i in (3, 1, 2)]
    for t in threads:
        t.start()
    time.sleep(0.01)
    assert processing.queue_position(3) in (2, 3, None)
    for t in threads:
        t.join(5)
    assert peak[0] == 1 and order == [1, 2, 3]
    assert processing.queue_position(1) is None and processing._queue_running == 0


def test_failure_releases_slot(monkeypatch):
    monkeypatch.setattr(processing, "max_concurrent", lambda: 1)
    monkeypatch.setattr(processing, "_run_check", lambda cid: (_ for _ in ()).throw(RuntimeError("boom")))
    try:
        processing.run_check(99)
    except RuntimeError:
        pass
    assert processing._queue_running == 0


def test_upload_reserves_credits_for_queued_checks(tmp_path, monkeypatch):
    import pytest
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from src.portal import db as dbm
    eng = create_engine("sqlite://"); dbm.Base.metadata.create_all(eng)
    s = sessionmaker(bind=eng)(); org = dbm.Organisation(name="O"); s.add(org); s.commit()
    from tests.portal.test_portal import buy
    buy(s, org.id, 1, dbm.utcnow())          # 1 credit, already reserved by queued check A
    s.add(dbm.Check(org_id=org.id, doc_ref="A", filename="a.pdf", status=dbm.CheckStatus.uploaded)); s.commit()
    pdf = open("test-library/samples/SAMPLE-TMP-01.pdf", "rb").read()
    monkeypatch.setattr(processing, "UPLOAD_DIR", tmp_path, raising=False)
    with pytest.raises(processing.UploadError, match="reserved"):
        processing.create_check(s, org.id, "b.pdf", pdf)


def test_confidence_labels():
    a = {"page": 3, "evidence": "Signs will be installed", "issue": "x", "severity": "Minor", "pass": "A", "run": 1}
    b = dict(a, run=2)
    c = {"page": 9, "evidence": "Other text entirely here", "issue": "y", "severity": "Minor", "pass": "B", "run": 1}
    merged = processing.dedupe([("ai", a), ("ai", b), ("ai", c)])
    labels = sorted(processing.confidence(s, f, 2) for s, f in merged)
    assert labels == ["Both runs", "One run"]
    assert processing.confidence("deterministic", {"page": 1}, 2) == "Rule check"
    assert processing.confidence("ai", c, 1) is None
