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
