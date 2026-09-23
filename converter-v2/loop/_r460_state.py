#!/usr/bin/env python3
"""ROUND 460 finalise, LOOP_STATE part — clear the in-flight marker, Position rows, plateau, standing facts, round log, the
Next-session line; MOVE the Round 8 PICK section to LOOP_STATE_ARCHIVE.md (pointer left). .pre-r460-finalise.bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-r460-finalise.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
i = find("- **ROUND 8 (engine r460) IN FLIGHT — NOT PROVEN**")
marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈11:50, session 41 Round 8 — r460 SHIPPED and committed; the in-flight marker is "
        "cleared). LAST SHIPPED **r460** (260620.30); **LAST FULL = r460** (the ledger's backstop); ledger **scoped #0** since it "
        "(8 of headroom).")
k = find("- LAST SHIPPED: **r459**")
L[k] = ("- Before it: **r459** (260620.29, the module introduction stays on the overview, +0.0085pp — pre-existing +0.0264pp, "
        "≥75 +5; 17 modules, pages 2691 → 2675) — gate row in BUILD_CHANGELOG.md round 459.")
L.insert(k, "- LAST SHIPPED: **r460** (build 260620.30, 24 Sept ≈11:45, session 41 Round 8 — KNOWLEDGE / PRACTICES ARE THEIR OWN "
         "OVERVIEW TABS, KB c67 / CL-0040, `KPTABS_OFF`; 19 modules / 28 pages, all in the module menu; **THE FULL BACKSTOP** — 42 "
         "batches, 523 unaffected byte-identical, ledger reset to 0; **skeleton 54.9376 % @ 2524 EXACT** (the menu `tabs` are one "
         "WIDGET line), ≥50 1581, ≥75 275, ≥90 25, **RAW 38.934 → 38.967 %**; cs 16719 / 208 / 896 / 24, body 61 / 5 / 176 / 239, "
         "clean 2621 / 2667, leak 75 / 46 — all EXACT; menu-only 20 up / 7 down (4 NAMED KB overrides); `gate_baseline.json` at "
         "r460 (menulabels ENO2060 4 pre-existing); the miner 197 CANDIDATE @ 2524).")
k = find("- Plateau window (§4): **0 of 3** — r459")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r459", "- Plateau window (§4): **1 of 3** — r460 predicted a small "
                    "skeleton move (made before the menu's WIDGET collapse was found) and delivered +0.0000pp: counted as NOT moving "
                    "(conservative); r459", 1)
k = find("- Standing facts: AppVersion 260620.29")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.29 (r459", "- Standing facts: AppVersion 260620.30 (r460 the K / P "
                    "overview tabs, KB c67, the FULL backstop — session 41 Round 8, 24 Sept); before it 260620.29 (r459", 1)
# move the PICK section to the archive
p0 = find("## Session 41 — Round 8 PICK (engine r460)")
p1 = p0 + 1
while p1 < len(L) and not L[p1].startswith("## "): p1 += 1
pick = L[p0:p1]
L[p0:p1] = ["## Session 41 — Round 8 (engine r460, build 260620.30) — KB c67: KNOWLEDGE / PRACTICES ARE THEIR OWN OVERVIEW TABS "
            "(THE FULL BACKSTOP) — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 41 — Round 8 PICK "
            "(engine r460) + what shipped'; the one-line summary is the s41-r8 Round-log line below.", ""]
k = find("## Round log")
L.insert(k + 1, "- s41-r8 (engine r460, build 260620.30, 24 Sept ≈11:05 → ≈11:50) · KB c67: KNOWLEDGE / PRACTICES ARE THEIR OWN "
         "OVERVIEW TABS (canonical order, emptied Information dropped; BLL / WJFUN excluded) · SHIPPED as THE FULL BACKSTOP (ledger "
         "→ 0) · 19 modules / 28 pages · skeleton 54.9376 EXACT (menu = WIDGET), RAW +0.033pp, menu-only 20 up / 7 down (SSCI104 / "
         "ENGS405 / SSEA203 / ENO2060 NAMED KB overrides) · every gate EXACT · follow-ups: WJFUN K / P headings; Overview Var 1 / 2.")
k = find("**Next session starts with:**")
L[k] = L[k].replace("LAST SHIPPED **r459** (260620.29); LAST FULL = the **r452 state**; ledger scoped #6; plateau **0 of 3**.",
                    "LAST SHIPPED **r460** (260620.30); LAST FULL = **r460**; ledger scoped #0; plateau **1 of 3**.", 1)
assert "LAST SHIPPED **r460**" in L[k], L[k][:300]
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Session 41 — Round 8 PICK (engine r460) + what shipped\n\n" + "\n".join(pick).rstrip() + "\n" + marker + "\n"
    "- **What shipped (r460, 260620.30):** `MenuBuilder` promotes a heading whose fold IS Knowledge / Practice(s) (optional "
    "`Year N` / `Level N` lead, optional colon) to a canonical nav tab titled by canon, marked `lead` so `SkeletonBuilder` renders "
    "it before the Information slot; `drop_empty_tab2` removes an Information tab the promotions emptied (KB omission rule). Data "
    "`menu.extra_tabs.curriculum_tabs.kb_canonical`; env `KPTABS_OFF`; excluded BLL + WJFUN. In-round repair: the first ON probe "
    "appended the tabs after Information (ENGC403 −9 menu-only) → the `lead` order. Shipped as the FULL backstop "
    "(`_r460_fullship_par.sh`, 523 unaffected byte-identical; `_r460_postship.sh` every gate EXACT, selftests 50, miner 197). "
    "Evidence `outputs/_r460_rawmenu.log`. Follow-ups: (1) WJFUN112 / 113 / 115 / 116 — gold K / P tabs, Claude drops the "
    "headings (the r410 tile dialect's `module_pane_heading_pattern`); (2) the Overview pane after a promotion ships one "
    "`col-md-6` / `col-md-12` column — KB c67 Var 1 (two `col-md-6` paddingR / paddingL) vs Var 2 (`col-md-8`) is not "
    "derivable from list length alone (FRNO902 Var 1, SCBI301 Var 2 at 5 + 5 items); both skeleton-invisible (menu = WIDGET).\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", len(s.encode("utf-8")), "->", os.path.getsize(S))
