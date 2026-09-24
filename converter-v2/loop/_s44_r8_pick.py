#!/usr/bin/env python3
"""Session 44 Round 8 — write the PICK (engine r483) + raise the in-flight marker in LOOP_STATE.md (§3 step 1). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r483-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈02:10, session 44 Round 6")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 483 IN FLIGHT — NOT PROVEN** (session 44 Round 8, 25 Sept ≈02:40): KB c38 — AUTOCHECK ON THE 1-3 / 4-6 / ECH TEMPLATES "
         "(the drag-and-drop: `autoCheck` + only the Reset button, KB 03B). Files: `app/js/SkeletonBuilder.js` (a page post-pass keyed on the "
         "resolved `<html template>`), `data/Emit_Templates.json` `skeleton.template_autocheck` {enabled, env `TPLAUTOCHECK_OFF`}, the gate tool "
         "`reference/tests/_verify_dragdrop.cjs` (accept KB 03B's autoCheck form). Affected: the 1-3 / 4-6 pages with a built dragAndDrop (≈ 38 modules).")
p = [i for i, l in enumerate(L) if l.startswith("## Session 44 — Round 6 PICK (engine r482)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 44 — Round 8 PICK (engine r483) — KB c38: AUTOCHECK ON THE 1-3 / 4-6 / ECH TEMPLATES (IN FLIGHT)",
 "- **Lane:** the KB queue — the UNVERIFIED rows re-read (c7, c15, c27, c38, c66). **c38** (`autoCheck` auto-applied on the ECH / 1-3 / 4-6 "
 "templates; KB 03A 'autoCheck Auto-Application': \"`autoCheck` MUST be applied automatically to every interactive that supports it\", the "
 "Undo / Check buttons dropped exactly as each component's 'With autoCheck' example shows; the typing quiz keeps its buttons) measured "
 "(`_s44_r8_autocheck.py`, by the page's `<html template>`): Claude builds 51 dragAndDrops on 1-3 / 4-6 pages (38 modules; standard 24, "
 "images 13, column 14 — no free-form area layout) and **0** carries `autoCheck`; also 7 multiChoiceQuiz (1), 5 dropQuiz (3), 1 typing (1). "
 "The gold on 1-3: dragAndDrop 348 / 793, multiChoiceQuiz 237 / 310, dropQuiz 42 / 65, radioQuiz 46 / 59 — far above its 7-8 / 9-10 / NCEA "
 "rates (the rule shows), not universal (pre-rule builds).",
 "- **Authority:** a numbered constraint (c38, 00D) + KB 03A / 03B — §1b rank 1; the gold share not consulted (§2). Scope this round: the "
 "dragAndDrop (KB 03B's exact form — `class=\"dragAndDrop autoCheck …\"`, the button row reduced to Reset); the quiz types (12 widgets) "
 "recorded for a later round. Skeleton-blind by design (a widget-root class + its button row, both inside the collapsed WIDGET line; "
 "compare_structure excludes widget subtrees) — judged on the dragAndDrop verifier, taught KB 03B's autoCheck form; plateau: neither.",
 "- **Fix:** `SkeletonBuilder.BuildPage` — once the page's template attribute is resolved, a post-pass over the body: every `dragAndDrop` root "
 "without `autoCheck` (and not `layout=\"area\"`) gains the class and loses its own `undo` / `checkAnswer` buttons. Data "
 "`skeleton.template_autocheck` {templates [1-3, 4-6, ech], widgets.dragAndDrop}; env `TPLAUTOCHECK_OFF` = the r482 bytes.",
 "",
]
io.open(S, "w", encoding="utf-8", newline="\n").write("\n".join(L)); print("ok", os.path.getsize(S))
