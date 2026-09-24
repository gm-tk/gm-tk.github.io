#!/usr/bin/env python3
"""Session 44 Round 9 — write the PICK (engine r484) + raise the in-flight marker in LOOP_STATE.md (§3 step 1). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r484-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈02:45, session 44 Round 8")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 484 IN FLIGHT — NOT PROVEN** (session 44 Round 9, 25 Sept ≈02:50): KB c38 FOR THE QUIZ TYPES — r483's "
         "`skeleton.template_autocheck.widgets` gains multiChoiceQuiz / dropQuiz / typing / radioQuiz / wordSelect (the class only: Claude's quiz "
         "builders emit no Undo / Check row in either form; the typing quiz keeps its buttons per KB 03D). File: `data/Emit_Templates.json` only "
         "(the r483 code path); env `TPLAUTOCHECK_OFF` + a sub-toggle `TPLAUTOQUIZ_OFF`.")
p = [i for i, l in enumerate(L) if l.startswith("## Session 44 — Round 8 PICK (engine r483)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 44 — Round 9 PICK (engine r484) — KB c38 FOR THE QUIZ TYPES (IN FLIGHT)",
 "- **The class:** r483's remainder (`_s44_r8_autocheck.py`): on 1-3 / 4-6 pages Claude builds 7 multiChoiceQuiz (1 with autoCheck), 5 "
 "dropQuiz (3), 1 typing (1) — 8 widgets without it. KB 03A lists MCQ / multiChoiceQuiz / Dropdown Quiz / Radio Quiz / Word Select / typing "
 "as autoCheck-capable; the builders' own autoCheck form (the writer's wording, r287 / r449) is the root class alone — no button row is "
 "emitted in either form (BLL273_2_0 / BLL251_2_0 vs their plain siblings), and the typing quiz keeps its buttons (KB 03D).",
 "- **Authority:** c38 / 03A (rank 1). Under the floor alone — rides along with r483's rule and mechanism (§2), proven the same way. "
 "Skeleton-blind; judged on the dropDown / typing verifiers; plateau: neither.",
 "",
]
io.open(S, "w", encoding="utf-8", newline="\n").write("\n".join(L)); print("ok", os.path.getsize(S))
