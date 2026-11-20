"""Consolidation (BENCH-02 action 1): cross-page grouping, style roll-up, safe handling of model output."""
import json
from types import SimpleNamespace

from sqlalchemy import create_engine, inspect, text

from src.portal import db as dbm, processing
from src.tmpcheck import consolidate as cons


def F(page, issue, ev, sev="Minor", **kw):
    return {"page": page, "issue": issue, "evidence": ev, "severity": sev, **kw}


ITEMS = [
    ("ai", F(10, "TMP says 6 months but TGSs say 4 weeks", "Duration of Work 6 months", "Major", **{"pass": "B"})),
    ("ai", F(59, "TGS duration 4 weeks conflicts with TMP 6 months", "Duration: 4 weeks", "Moderate", **{"pass": "D"})),
    ("ai", F(9, "Unit spacing inconsistent", "60km/h", **{"pass": "A"})),
    ("ai", F(21, "Volume unit spacing inconsistent", "6599vpd", **{"pass": "A"})),
    ("ai", F(19, "'activites' is misspelt", "activites", **{"pass": "A"})),
]


def test_cross_page_group_and_style_rollup():
    out = processing.consolidate(ITEMS, lambda fs: [([0, 1], "issue"), ([2], "style_variant"),
                                                    ([3], "style_variant"), ([4], "issue")])
    assert len(out) == 3
    src, dur = out[0]
    assert dur["severity"] == "Major" and dur["page"] == 10 and dur["related_pages"] == [59]
    assert src == "AI B, AI D"
    typo = out[1][1]
    assert typo["issue"].startswith("'activites'")
    roll = out[2][1]
    assert roll["issue"].startswith("Style inconsistencies") and "(2 items)" in roll["issue"]
    assert "p9:" in roll["evidence"] and "p21:" in roll["evidence"]


def test_single_style_point_not_rolled_up():
    out = processing.consolidate(ITEMS[2:3] + ITEMS[4:], lambda fs: [([0], "style_variant"), ([1], "issue")])
    assert len(out) == 2 and not any(f["issue"].startswith("Style inconsistencies") for _, f in out)


def test_normalise_handles_bad_model_output():
    g = cons.Grouping(groups=[cons.Group(ids=[0, 1, 1, 9], kind="issue"), cons.Group(ids=[1, 2], kind="issue")])
    assert cons.normalise(g, 4) == [([0, 1], "issue"), ([2], "issue"), ([3], "issue")]


def test_group_findings_with_fake_client():
    reply = json.dumps({"groups": [{"ids": [0, 1], "kind": "issue"}, {"ids": [2, 3], "kind": "style_variant"},
                                   {"ids": [4], "kind": "issue"}]})
    msg = SimpleNamespace(content=[SimpleNamespace(type="text", text=reply)],
                          usage=SimpleNamespace(input_tokens=10000, output_tokens=1000,
                                                cache_read_input_tokens=0, cache_creation_input_tokens=0))

    class Stream:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def get_final_message(self): return msg
    calls = {}

    class Msgs:
        def stream(self, **kw):
            calls.update(kw)
            return Stream()
    client = SimpleNamespace(beta=SimpleNamespace(messages=Msgs()))
    groups, usd = cons.group_findings([f for _, f in ITEMS], client=client)
    assert groups == [([0, 1], "issue"), ([2, 3], "style_variant"), ([4], "issue")]
    assert usd == 0.06 and "Duration of Work" in calls["messages"][0]["content"]


def test_sqlite_migration_adds_new_column(tmp_path):
    eng = create_engine(f"sqlite:///{tmp_path}/old.db")
    with eng.begin() as c:
        c.execute(text("CREATE TABLE finding (id INTEGER PRIMARY KEY, check_id INTEGER, severity VARCHAR(16), "
                       "page INTEGER, section VARCHAR(200), evidence TEXT)"))
        c.execute(text("INSERT INTO finding (check_id, severity, page, section, evidence) VALUES (1,'Minor',2,'s','e')"))
    dbm.init_db(eng)
    cols = {c["name"] for c in inspect(eng).get_columns("finding")}
    assert {"pages", "source", "disposition"} <= cols
    with eng.begin() as c:
        assert c.execute(text("SELECT count(*) FROM finding")).scalar() == 1
