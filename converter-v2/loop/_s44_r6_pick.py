#!/usr/bin/env python3
"""Session 44 Round 6 — write the PICK (engine r482) + raise the in-flight marker in LOOP_STATE.md (§3 step 1). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r482-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈01:35, session 44 Round 4")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 482 IN FLIGHT — NOT PROVEN** (session 44 Round 6, 25 Sept ≈02:00): THE BILINGUAL LESSON TITLE KEEPS ITS h2 — the r137 "
         "`[H2] Lesson N / Hei Mahi N` title (`section_grouping.lesson_heading.title_level` 2) is demoted to h3 by the page's re-level pass; "
         "pinned through the r371 writer-digit marker. Files: `app/js/BilingualBuilder.js` (`bilingualLessonTitleHtml`), `data/Emit_Templates.json` "
         "`section_grouping.lesson_heading.pin_title` {enabled, env `LESSONPIN_OFF`}. Affected: TRR108 / TRR115 / TRR203 / TRR301 / TRR304 (14 pages).")
p = [i for i, l in enumerate(L) if l.startswith("## Session 44 — Round 4 PICK (engine r481)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 44 — Round 6 PICK (engine r482) — THE BILINGUAL LESSON TITLE KEEPS ITS h2 (IN FLIGHT)",
 "- **Lane:** the Bilingual low-module scan (`_s44_famdiff.py` over TRR304 / TRR301 / TRR115 / TRR107 / TRR203 / PMT101 — PMT101's one-table "
 "template dominates, one module, below floor) surfaced `body SUBSTITUTED h2 → h3 «Hei Mahi N»`. **Measured:** the gold ships the bilingual "
 "lesson title (`Hei Mahi N` / `Lesson N` + its English pair) at **h2 on 22 / 22** (16 pages / 7 modules); Claude at **h3 on 30 / 30** (14 "
 "pages / 5 modules: TRR108 2, TRR115 3, TRR203 3, TRR301 3, TRR304 3).",
 "- **Mechanism:** `BilingualBuilder.bilingualLessonTitleHtml` FORCES `section_grouping.lesson_heading.title_level` (2) on the title (r137 — "
 "\"so the site-wide re-levelling pass can never push this title below the human's h2\"), but `ContentConverter.#relevelHeadings` (the "
 "rank normalisation, base h3) still treats it as the page's shallowest free heading and maps it to h3.",
 "- **Authority:** KB 07D's MTK lesson skeleton (`<h2 reo>{MAORI_LESSON_HEADING}</h2>`) — §1b rank 1 — and the gold 22 / 22; the existing data "
 "rule's own intent (r137). A §1d family dialect (the Bilingual `[H2] Lesson N` opener only; 14 pages, under the floor). Predicts a small "
 "skeleton move (two heading lines per page).",
 "- **Fix:** the title's tags carry the transient r371 `data-wd` marker at `title_level`; the re-level pass pins a marked heading to its digit "
 "(and still counts it in the rank pool, so the page's other headings keep their levels) and strips the marker. Data "
 "`section_grouping.lesson_heading.pin_title` {enabled, env `LESSONPIN_OFF`}.",
 "",
]
io.open(S, "w", encoding="utf-8", newline="\n").write("\n".join(L)); print("ok", os.path.getsize(S))
