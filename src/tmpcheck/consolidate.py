"""Issue consolidation (BENCH-02 action 1).

After all checks run, one short text-only Claude call groups findings that describe the same
underlying problem (same conflict reported on several pages, same leftover found by two passes)
and marks pure style/format consistency points so they can be rolled into one style-sheet finding.

The model only returns groupings of finding ids. It never edits a finding's text, page or evidence,
so evidence validation is unaffected. If the call fails, findings are returned ungrouped.
"""
from typing import List, Literal

from pydantic import BaseModel

MODEL = "claude-opus-5-5"
EFFORT = "medium"
MAX_TOKENS = 16000

INSTRUCTIONS = """Below is a list of findings from an automated check of one Traffic Management Plan.
Several checks ran independently, so the same underlying problem is often reported more than once:
on different pages (e.g. a date conflict raised at page 10 and again at each TGS), or in different words.

Return groups of finding ids:
- Put findings in the same group only when fixing one would fix the others (same conflict, same
  leftover block, same missing item, same wrong statement). Different typos are different problems,
  even if they are the same kind of error; keep them separate.
- kind = "style_variant" only for pure presentation-consistency points: unit spacing, capitalisation,
  hyphenation or dash style, number/time/date formats, abbreviation or term variants (e.g. car park /
  carpark). Spelling mistakes, wrong words, grammar errors, missing punctuation and all factual,
  consistency or completeness issues are kind = "issue".
- Every id must appear in exactly one group. A finding with no duplicate is a group of one.

Findings (id | page | severity | issue | evidence):
"""


class Group(BaseModel):
    ids: List[int]
    kind: Literal["issue", "style_variant"]


class Grouping(BaseModel):
    groups: List[Group]


def _line(i: int, f: dict) -> str:
    ev = " ".join(str(f.get("evidence", "")).split())[:140]
    issue = " ".join(str(f.get("issue", "")).split())[:220]
    return f"{i} | p{f.get('page')} | {f.get('severity')} | {issue} | {ev}"


def normalise(grouping: Grouping, n: int) -> list[tuple[list[int], str]]:
    """Make the model's answer safe: drop unknown ids, keep each id once, add missing ids as singletons."""
    seen: set[int] = set()
    out: list[tuple[list[int], str]] = []
    for g in grouping.groups:
        ids = [i for i in dict.fromkeys(g.ids) if 0 <= i < n and i not in seen]
        if ids:
            seen.update(ids)
            out.append((ids, g.kind))
    out += [([i], "issue") for i in range(n) if i not in seen]
    return out


def group_findings(findings: list[dict], client=None) -> tuple[list[tuple[list[int], str]], float]:
    """Return ([(indices, kind)], usd). Indices refer to positions in `findings`."""
    n = len(findings)
    if n < 2:
        return [([i], "issue") for i in range(n)], 0.0
    if client is None:
        import anthropic
        client = anthropic.Anthropic()
    text = INSTRUCTIONS + "\n".join(_line(i, f) for i, f in enumerate(findings))
    from .llm_checks import BETAS
    # Same request shape as the checking passes (proven on the Owner's PC, OWNER-FT-02)
    with client.beta.messages.stream(model=MODEL, max_tokens=MAX_TOKENS, output_config={"effort": EFFORT},
                                     output_format=Grouping, betas=BETAS, fallbacks="default",
                                     messages=[{"role": "user", "content": text}]) as stream:
        msg = stream.get_final_message()
    body = next(b.text for b in msg.content if b.type == "text")
    grouping = Grouping.model_validate_json(body)
    from .llm_checks import cost
    return normalise(grouping, n), round(cost(msg.usage), 4)
