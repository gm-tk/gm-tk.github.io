"""SESSION 40 ROUND 10 — the LOOP_STATE.md finalise edits for the measurement-tool round (written with the Write tool; run under WSL
from FINAL_MODULE_DATA). Each prefix must match exactly once or nothing is written."""
import io, sys

S = "LOOP_STATE.md"
src = io.open(S, encoding="utf-8", newline="").read()
lines = src.split("\n")


def find(prefix):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        sys.exit(f"prefix {prefix[:60]!r} matched {len(hits)} lines")
    return hits[0]


i = find("- **ROUND 10 IN FLIGHT — NOT PROVEN**")
lines[i] = ("- **No round in flight** (24 Sept 2026 04:55, session 40 Round 10 SHIPPED a measurement-tool change — no engine change; the "
            "corpus on disk IS the r452 state, LAST SHIPPED r452, LAST FULL r444, ledger scoped #7 — 1 of headroom: **the next engine ship "
            "should be the FULL backstop**). The Round-10 marker was raised at 04:47 real time (its '05:20' was a clock slip).")

i = find("- Plateau window (§4): **2 of 3** — r452")
lines[i] = lines[i].replace("- Plateau window (§4): **2 of 3** — r452",
                            "- Plateau window (§4): **2 of 3** — s40-r10 a measurement-tool round (neither counts nor resets); r452", 1)

i = find("- s40-r9 ")
lines.insert(i, "- s40-r10 (no engine change — a MEASUREMENT-TOOL round, 24 Sept 04:40 → 04:55) · THE COVERAGE DASHBOARD GAINS THE D13-4 "
                "QUIZ ROWS (the r449 follow-up): `_measure_r271_variations.cjs` `WANT` + the 7 answer-key types, env `CENSUS_QUIZ_OFF`; "
                "proof OFF 5732 = ON minus quiz, record for record; headline coverage RE-BASED 50.8 % → 44.9 % (7286 widgets) · SHIPPED "
                "(tool) · gates untouched. PICK pass first: TEDC avatar leak 8 in-bubble (below floor); image-description captions measured "
                "(follow-up).")

i = find("- **(r449) The coverage dashboard has no quiz-engine rows.**")
lines[i] = ("- ~~**(r449) The coverage dashboard has no quiz-engine rows.**~~ → **SHIPPED s40-r10** (the census counts the 7 D13-4 types; "
            "`CENSUS_QUIZ_OFF=1` = the old census; headline 50.8 % → 44.9 % is a RE-BASE). Read now: multiChoiceQuiz 12 / 413 built, "
            "typing 8 / 270, dropDown 341 / 598, reorder 0 / 104, radioQuiz 0 / 89, selectionBox 0 / 80.")
lines.insert(i, "- **(s40-r10) The writer's `[Image] <description>` line ships as a visible `<p>`.** `outputs/_s40_r10_imgdesc.py` / "
                "`_imgdesc2.py`: 177 such paragraphs; the gold ships the words on 46, lacks them on 131. By shape: a description followed "
                "by an iStock title / URL (the stock descriptor) — gold lacks 90 / has 18 (TEDC402's 'avatar Tina' = 42 of the 90; without "
                "it 48 / 18 = 0.73 over ≈ 14 modules); an instruction cue ('please recreate', 'creative services, please source …') — lacks "
                "20 / has 3 (→ a Writers Note); plain — lacks 21 / has 25 (a tie: captions). **The mechanism is NOT the r240 own-text "
                "pair** (`_s40_r10_imgown.cjs`: 1 site) — find where TEDC's 'avatar Tina' (black before the red 'from:' seam, the iStock "
                "title after it) reaches `MediaBuilder.image`'s caption before sizing a fix; TEDC402 also leaks it INSIDE 8 built bubbles "
                "(`_s40_r10_bubbledesc.py`, D13-9 part 1).")

out = "\n".join(lines)
io.open(S + ".new", "w", encoding="utf-8", newline="").write(out)
print("state", len(src.encode()), "->", len(out.encode()))
