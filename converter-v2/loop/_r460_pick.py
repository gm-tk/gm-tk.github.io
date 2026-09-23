#!/usr/bin/env python3
"""r460 PICK write: raise the in-flight marker + insert the Round 8 PICK section into LOOP_STATE.md (line edits only)."""
import io
P = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/LOOP_STATE.md"
s = io.open(P, encoding="utf-8", newline="").read()
old = s[s.index("- **No round in flight** (24 Sept 2026 ≈11:00, session 41 Round 7"):]
old = old[:old.index("\n") + 1]
new = ("- **ROUND 8 (engine r460) IN FLIGHT — NOT PROVEN** (24 Sept 2026 ≈11:30, session 41): KB c67 (CL-0040) THE KNOWLEDGE / "
       "PRACTICES SECTIONS ARE THEIR OWN OVERVIEW NAV TABS (tabbed archetype; + the KB omission rule drops the emptied Information "
       "tab). Files: `app/js/MenuBuilder.js`, `data/Emit_Templates.json` (`menu.extra_tabs.curriculum_tabs.kb_canonical`), "
       "`app/js/Config.js`. Data flag `kb_canonical.enabled`; env **`KPTABS_OFF`**. LAST SHIPPED **r459** (260620.29); LAST FULL = "
       "the r452 state; ledger scoped #6.\n")
s = s.replace(old, new, 1)
anchor = "## Session 41 — Round 2 (engine r454, build 260620.25)"
pick = ("## Session 41 — Round 8 PICK (engine r460) — KB c67: KNOWLEDGE / PRACTICES ARE THEIR OWN OVERVIEW TABS\n"
        "- **Lane:** the loss ledger / content re-read (`outputs/_s41_r8_lost.py`: 3.0 % of WT∩gold 6-word shingles are on no Claude "
        "page) → the module-menu chrome region. **Authority §1b rank 1:** KB constraint 67 / CL-0040 (Universal) — the tabbed `-00` "
        "menu is the canonical set Overview → Knowledge → Practices → Information → Standards, content-driven omission rule; KB 10 §2: "
        "whenever the overview menu IS tabbed its composition follows c67. The r263 mechanism (`curriculum_tabs`) fires only for the "
        "`SCCH|7-8` registry row. Numbered constraint → no share test; the override list measured instead.\n"
        "- **Measured** (`outputs/_s41_r8_kppane.py` / `_s41_r8_kppop.py`): 36 tabbed-archetype modules whose K / P sections reach "
        "Claude's Overview pane. Gold: OWN TABS 21 (BLL 10 + BLLR 3, ENGC 3, GENO901, FRNO902, HPRE203, SCBI301 / SCES201 / SCPH301), "
        "Information pane 10 (BLL 7, HPRE301, SSCI104 / 205; ENGJ403 / ENGS404 already Info on Claude), tab 1 5 (ENGS405, FRNO901, "
        "SSEA203, WJFUN109 / 110). **Scope:** every tabbed-archetype overview EXCEPT subject `BLL` (CL-0040 leaves the BLL263 D2 "
        "overview tab-split question untouched) and `WJFUN` (the r410 tile dialect; 4 golds own-tab but Claude never routes the "
        "headings — a follow-up). Heading anchored `^(year N )?(knowledge|practices?):?$` (GENO901's 'Learning intentions – Cultural "
        "knowledge' must not promote). **Expected:** ≈12 modules up (BLLR201-203, ENGC204 / 206 / 403, GENO901, FRNO902, HPRE203, "
        "SCBI301, SCES201, SCPH301); named KB overrides ≈ HPRE301, SSCI104, SSCI205, SSEA203, FRNO901, ENGJ403, ENGS404/405, "
        "TEDC401 / 402, ENO2060. Predicts a small skeleton move (overview pages only).\n\n")
s = s.replace(anchor, pick + anchor, 1)
io.open(P + ".tmp", "w", encoding="utf-8", newline="").write(s)
import os; assert os.path.getsize(P + ".tmp") > 90000; os.replace(P + ".tmp", P)
print("ok", len(s))
