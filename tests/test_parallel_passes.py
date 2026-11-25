"""Parallel AI passes (Owner 2026-11-25): first pass alone (cache warm-up), the rest concurrently."""
import threading
import time
from pathlib import Path
from types import SimpleNamespace

from src.tmpcheck import llm_checks

SAMPLE = Path(__file__).resolve().parents[1] / "test-library" / "samples" / "SAMPLE-TMP-01.pdf"


def test_first_alone_then_parallel(monkeypatch):
    log, active, peak, lock = [], [0], [0], threading.Lock()

    def fake_call(client, req, code):
        with lock:
            active[0] += 1; peak[0] = max(peak[0], active[0]); log.append(code)
        time.sleep(0.2)
        with lock:
            active[0] -= 1
        u = SimpleNamespace(input_tokens=10, output_tokens=10, cache_read_input_tokens=0, cache_creation_input_tokens=0)
        msg = SimpleNamespace(stop_reason="end_turn", usage=u,
                              content=[SimpleNamespace(type="text", text='{"findings": []}')])
        return msg, 0.2

    monkeypatch.setattr(llm_checks, "_call", fake_call)
    monkeypatch.setattr(llm_checks, "_client", lambda dry_run=False: object())
    t0 = time.time()
    outs = llm_checks.run_many(SAMPLE, ["A", "B", "C", "D"], runs=2, parallel=8)
    elapsed = time.time() - t0
    assert len(outs) == 2 and set(outs[1]["passes"]) == {"A", "B", "C", "D"}
    assert log[0] == "A" and peak[0] == 7          # warm-up alone, then the other 7 together
    assert elapsed < 0.8                           # sequential would be 1.6 s
