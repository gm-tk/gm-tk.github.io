#!/usr/bin/env python3
"""Session 44 Round 3 — write the PICK (engine r480) + raise the in-flight marker in LOOP_STATE.md (§3 step 1). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r480-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈00:40, session 44 Round 2")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 480 IN FLIGHT — NOT PROVEN** (session 44 Round 3, 25 Sept ≈01:00): THE MTK ACTIVITY IS ONE BOX — the `Activity NX: ║ "
         "Ngohe NX:` intro table + its `[Activity: Embedded]` table (+ spec tables) render as ONE `div.activity.interactive`, the marker table's "
         "own data rows as ONE hand-off (KB 07B 'Activity Structure'; a §1d TRR family dialect). Files: `app/js/ContentConverter.js` (the reoMode "
         "dispatch), `app/js/BilingualBuilder.js` (`isActLabelTable`, `bilingualActivity`), `data/Emit_Templates.json` "
         "`elements.dual_language.act_label_box` {enabled, env `ACTLABELBOX_OFF`, families}. Affected: TRR116 / TRR106 (+ any TRR marker table "
         "with data rows).")
p = [i for i, l in enumerate(L) if l.startswith("## Session 44 — Round 2 PICK (engine r479)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 44 — Round 3 PICK (engine r480) — THE MTK ACTIVITY IS ONE BOX (a §1d TRR family dialect; IN FLIGHT)",
 "- **Lane (00:45 → 01:00):** the TRR1 lesson-page lane continued (the loss ledger's lowest large family). Sub-classes sized first and "
 "NOT taken: (b) the identical reo = eng pair (`_s44_r3_bilpairs.py`): the gold ships the text ONCE on 111 pairs and TWICE on 132 — no "
 "consensus, DECLINED; (c) the audio-word line `p.center-text.sassoonI-text` — 98 in 4 modules, 84 of them TRR111 — one module's dialect, "
 "below floor. The coverage dashboard refreshed on r479 (`_s44_dashboard_run.sh`: 44.7 % of 7,290 widgets build; dragAndDrop 110 / 1033). "
 "Miner rows re-checked and already dispositioned: #4 title `h1>span` (the gold's Te Reo titles in no WT — class C, r198 / r358); the "
 "footer rows #422–#445 (KB 01B: overview next + home, final prev + home — Claude KB-correct); body `div.row` EXTRA / MISSING (the s25 "
 "row-break decline — the r51 rules hold at gold consensus).",
 "- **The class (TRIANGULATED TRR116_4_0 / TRR116_1_0 / TRR106_2_0):** TRR116 / TRR106 write each activity as TWO tables — a bilingual "
 "intro `English ║ Te Reo Māori` / `Activity 4E: ║ Ngohe 4E:` / `[H2] title` / `[Body] …` and the red `[Activity: Embedded] <type>` table "
 "(instructions + the widget's data, often a NESTED table). The gold boxes them TOGETHER — the title inside `div.activity` on 47 / 50 "
 "(`_s44_r2_actlabel.py`); Claude renders the intro as free `row > col-md-8` prose and the embedded table as its own box, whose data rows "
 "`bilingualActivity` unfolds into loose paragraphs reading only the first TWO columns (`_s44_r3_actprobe.cjs`: 45 boxes / 4 modules, "
 "TRR116 35 — 399 elements; `_s44_r3_embrows.cjs`: 3- to 6-column data rows inside the marker table — the third+ cells are LOST). TRR116's "
 "nine lesson pages score 18–35 %.",
 "- **Authority:** KB 07B §7 'Activity Structure' (`| Activity 1A: | Ngohe 1A: |` + `[H2]` + `[Body]` → `div.activity number=` holding the "
 "reo / eng title + prose; `interactive` when it holds a widget) — §1b rank 1, the gold agrees 47 / 50. Under the 20-page floor (≈ 12 "
 "pages / 2 modules): shipped only under §1d exception 1 — a FAMILY dialect (data `families: [\"TRR\"]`), matching the family's own gold "
 "on every page, OFF byte-identical, every other gate held. Predicts a skeleton move on TRR116 / TRR106; plateau: a KB-rule round.",
 "- **Fix (planned):** (A) the reoMode dispatch, BEFORE `bilingualTable`: a bilingual table whose first content row is an `Activity NX: ║ "
 "Ngohe NX:` label pair (bold / red stripped) gathers itself + a following `[Activity: Embedded]` marker table + its spec tables (the "
 "existing gather's stops) and renders through `bilingualActivity` (label rows skipped, the number captured through the bold). (B) in "
 "`bilingualActivity`, a MARKER table's rows after its leading marker / heading / body rows are the widget's DATA → ONE `cv2-interactive "
 "bilingual-unbuilt` hand-off (the whole grid, every column kept) instead of paragraphs. Data `elements.dual_language.act_label_box`; env "
 "`ACTLABELBOX_OFF` = the r479 bytes.",
 "",
]
io.open(S, "w", encoding="utf-8", newline="\n").write("\n".join(L)); print("ok", os.path.getsize(S))
