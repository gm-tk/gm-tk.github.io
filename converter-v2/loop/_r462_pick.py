#!/usr/bin/env python3
"""r462 PICK write: raise the in-flight marker + insert the Round 10 PICK section into LOOP_STATE.md (line edits only)."""
import io, os
P = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/LOOP_STATE.md"
s = io.open(P, encoding="utf-8", newline="").read()
old = s[s.index("- **No round in flight** (24 Sept 2026 ≈12:25, session 41 Round 9"):]
old = old[:old.index("\n") + 1]
new = ("- **ROUND 10 (engine r462) IN FLIGHT — NOT PROVEN** (24 Sept 2026 ≈13:10, session 41): THE AUDIO-IMAGE UNIT IN PLACE — "
       "the r461 follow-up: `dual_language.media_in_place` re-scoped to the audio-image units only (`units_only`), every other "
       "bilingual media embed keeps its end-of-row place. Files: `app/js/BilingualBuilder.js`, `data/Emit_Templates.json`, "
       "`app/js/Config.js`. Data flag `media_in_place.enabled` + `units_only`; env **`REOMEDIAPOS_OFF`**. LAST SHIPPED **r461** "
       "(260620.31); LAST FULL = r460; ledger scoped #1; plateau 2 of 3.\n")
s = s.replace(old, new, 1)
anchor = "## Session 41 — Round 9 (engine r461, build 260620.31)"
pick = ("## Session 41 — Round 10 PICK (engine r462) — THE AUDIO-IMAGE UNIT IN PLACE (the r461 follow-up)\n"
        "- **Lane:** the r461 residue. Of r461's 15 dips, 6 (TRR112_1 / 4, TRR113_3 / 4.0, TRR103_3, TRR116_1) lose because the "
        "unit sits after its cell's paragraphs; the gold puts it where the writer typed it. The full in-place interleave measured "
        "27 up / 37 down (images / video in TRR116 / TRR203 / TRR108 do NOT follow the writer's cell order in the gold) — so the "
        "re-scope moves ONLY the audio-image units. **Authority:** the gold (TRR111 / 112 / 113 place every unit in reading order) "
        "+ KB 01E (the unit is the writer's authored element at its place). **Other lanes looked at this round (recorded):** the "
        "activity box's missing title (`outputs/_s41_r10_boxtitle2.py`: 9,700 gold h3-titled boxes, 5,552 OK; ABSENT 1,956 / OUT-H "
        "1,153 / RAW 669 — heterogeneous: FRNO's `[Reorder [autocheck]] **1A Title**` nested-bracket widget tag 82 boxes on 16 pages, "
        "below floor; PWY's title inside a widget table cell; the OUT-H split `_s41_r10_outh.py` 726 'a box later' mostly page-title "
        "prefix noise, 379 'no box' = the s37-declined box-boundary class). **Prediction:** small (+10–30 pp-sum); if under the "
        "0.02pp line the plateau window fires (3 of 3).\n\n")
s = s.replace(anchor, pick + anchor, 1)
io.open(P + ".tmp", "w", encoding="utf-8", newline="").write(s)
assert os.path.getsize(P + ".tmp") > 85000; os.replace(P + ".tmp", P)
print("ok", len(s))
