#!/usr/bin/env python3
"""Session 45 Round 2 — write the PICK (engine r487) + the in-flight marker in LOOP_STATE.md (§3 step 1, BEFORE any code). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r487-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈06:05, session 45 Round 1")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 487 IN FLIGHT — NOT PROVEN** (session 45 Round 2, 25 Sept ≈06:40): THE UNQUOTED NAMED HOVER ANCHOR — "
         "`[rollover definition for TERM: DEF]` / `[hover on TERM: DEF]` / `[roll over definition TERM: DEF]` weaves onto TERM in the nearest "
         "3 text items (first occurrence for a standalone definition line, last for an inline marker) instead of being appended after the "
         "host's last word and dropped. Files: `app/js/InteractiveScanner.js` (`#weaveHoverDefinition`), `data/Emit_Templates.json` "
         "`elements.hover_definition_inline.named_anchor` {enabled, env `HOVERNAMED_OFF`}. Affected: ≈ 14 modules (HIS / ARFUN / CEDO / DAN).")
p = [i for i, l in enumerate(L) if l.startswith("## Session 45 — Round 1 PICK (engine r486)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 45 — Round 2 PICK (engine r487) — THE UNQUOTED NAMED HOVER ANCHOR (IN FLIGHT)",
 "- **Lane:** the HIS1 family view again (`_s45_r1_his1.log`: `span.infoTrigger` MISSING 57 lines / 21 pages / 7 modules). Traced on "
 "HIS1005 (`_probe_infotrigger.cjs`): the writer's standalone `[Rollover definition for supreme: Ultimate or final.]` line resolves to "
 "the `info trigger` INTERACTIVE tag; `InteractiveScanner.#weaveHoverDefinition` recovers the definition, but honours only a QUOTED "
 "named anchor (r222c), so the sentinel is appended after the host paragraph's last word — which ends in a full stop — and "
 "`inlineMarkup` finds no word and DROPS the definition silently (writer content lost; the gold wraps `supreme`).",
 "- **Measured (`_s45_r2_hover.py`, every hover / rollover marker in every scored WT, by shape; the def matched whitespace-free "
 "against every `info=` attribute):** NAMED-FOR (`for / on / of TERM:`) 104 markers / 14 modules — gold builds & Claude drops **47**, "
 "both 41, neither 14; NAMED-BARE (`definition TERM:`) 17 / 4 — gold-only **8**; per module: HIS1005 23, HIS1002 12, HIS1006 5, "
 "HIS1008 4, ARFUN05 3, ARFUN01 2, ARFUN03 2, CEDO202 2, HIS1001 / 1006 / 1007 1. The TERM sits in the marker's own paragraph 44, the "
 "previous line 53, two / three lines back 11, not in 3 lines 13. (COLON-inline — no term — gold-only 94 over 20+ modules, 2–8 each: "
 "a separate class, recorded.)",
 "- **Authority:** the writer's tag (KB 01D: hover-over → `infoTrigger`) + the r222c named-anchor rule it generalises; the gold builds "
 "55 of the 76 named sites whose definition it carries anywhere. Writer content currently lost. Predicts a small skeleton move up "
 "(`span.infoTrigger` lines on ≈ 25 HIS / ARFUN pages); counts toward the plateau window if < 0.02pp.",
]
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(L)); os.replace(S + ".tmp", S)
print("ok", os.path.getsize(S))
