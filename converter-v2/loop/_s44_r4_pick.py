#!/usr/bin/env python3
"""Session 44 Round 4 — write the PICK (engine r481) + raise the in-flight marker in LOOP_STATE.md (§3 step 1). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r481-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈01:20, session 44 Round 3")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 481 IN FLIGHT — NOT PROVEN** (session 44 Round 4, 25 Sept ≈01:35): THE MTK ACTIVITY'S DATA ROWS ARE ONE HAND-OFF — "
         "`elements.dual_language.act_label_box.data_rows_handoff` false → true (the code shipped inert in r480: `BilingualBuilder.bilingualActivity` / "
         "`#markerDataFrom`); env `ACTLABELBOX_OFF` covers it (a sub-toggle `ACTDATA_OFF` added). Affected: the r480 set (TRR116 / TRR106 / TRR103).")
p = [i for i, l in enumerate(L) if l.startswith("## Session 44 — Round 3 PICK (engine r480)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 44 — Round 4 PICK (engine r481) — THE MTK ACTIVITY'S DATA ROWS ARE ONE HAND-OFF (IN FLIGHT)",
 "- **The class:** inside an r480 box the `[Activity: Embedded]` table's rows after its marker / `[H#]` / `[Body]` rows are the widget's DATA "
 "(`_s44_r3_embrows.cjs`: the nested sentence ║ word ║ picture ║ audio grids, word lists, `Note to CS` lines — 3- to 6-column rows); "
 "`bilingualActivity` unfolds each as loose `p reo` / `p eng` from the FIRST TWO cells only, so every third+ cell (the picture, the audio "
 "item) is LOST, and the gold's one WIDGET line meets a run of Claude paragraphs. One `cv2-interactive bilingual-unbuilt` hand-off (every "
 "column kept, `TablesAndGrids.contentTable`) is the loop's standard for un-built widget data (r451). Pre-scored +41.7 pp-sum on TRR116 on "
 "top of r480 (`_r480_prescore4.log` vs `_r480_prescore_Aonly.log`).",
 "- **Authority:** the hand-off is the D10-3 / r451 house form for an un-built widget's data (the builder's job, not the page's prose); KB 07B's "
 "activity holds the widget (`interactive`). A §1d family-dialect round (the r480 scope); the plateau: predicts a skeleton move.",
 "- **Watch:** compare_structure excludes a hand-off's contents on the Claude side — the r480 −80 was the boxing's pool shrink; this round's "
 "own cs effect is to be read off the scoped ship (any drop split by element before naming).",
 "",
]
io.open(S, "w", encoding="utf-8", newline="\n").write("\n".join(L)); print("ok", os.path.getsize(S))
