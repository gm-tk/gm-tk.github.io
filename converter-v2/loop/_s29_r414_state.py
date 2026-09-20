#!/usr/bin/env python3
"""r414 finalise — LOOP_STATE.md: the Round 5 PICK section moves to the archive (+ the what-shipped record), the Position updates,
the Round-log line is appended. Run under WSL."""
import os, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
a = idx("## Session 29 — Round 5 PICK (engine r414)"); b = idx("## Round log")
pick = lines[a:b]
shipped = ("- **What shipped (r414, build 260619.85, 20 Sept ≈18:30):** `activity_wrapper.standalone_widget_box.inside_open_activity {enabled, env NESTBOX_OFF, "
           "close_outer_subjects: []}` — at the bundle site, when the r217 / r266 synthetic owner is about to open and the stack top is an activity, the synthetic box is "
           "SUPPRESSED and the widget renders inside the open box (no positional letter spent); a subject in `close_outer_subjects` (none) takes the close-first form. "
           "The PICK's planned per-subject mix was superseded by the gate's own scorer on the probe's 84 paired ON pages (`_s29_r414_variants.sh`): suppress everywhere "
           "81 up / 3 down (+163.5pp-sum, every subject group net up) vs close-the-outer everywhere 28 / 24 (+27.7) vs the mix 50 / 10 (+115.4). Probe OFF = disk "
           "2555 / 2555; ON 94 pages / 65 modules; nested boxes 108 → 0; SCOPED regeneration of the 65 + the 12-module sample (7 batches rc 0; `scoped_ship.sh` PASS — "
           "0 stale, containment 65 ⊆ 65, spot-check 12 / 12, every gate held-or-improved); skeleton 53.8168 → 53.8864 % (+0.0696pp; 84 movers 81 up / 3 down — "
           "BLL162_1_0 −1.1, HIS1004_8_0 −0.5, XDLS909_4_0 −0.1; 0 outside the set), ≥50 1408 → 1412, ≥75 236 → 238, ≥90 20, RAW 37.970 → 37.997; compare_structure / "
           "body_compare / defect / every verifier EXACT; 16 selftests GREEN; feature index GREEN; ledger scoped #6 since the 19 Sept FULL (2 of headroom); miner 182 → 181 "
           "(the `activity EXTRA div.col-12` row gone); checksums engine 3 changed / gates 0. Recorded: the module-menu empty shell (725 — class C content on 445 pages; "
           "FRFUN / ConnectED no-menu-element = a family `menu_type` row), the 38 writer-owned empty boxes, the 14 HPFUN omitted-prompt rows.")
lines[a:b] = ["## Session 29 — Round 5 (engine r414) — THE NESTED ACTIVITY BOX: the synthetic widget box suppressed inside an open activity box — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 29 — Round 5 PICK (engine r414) + what shipped'; the one-line summary is the s29-r5 Round-log line below.", ""]
p = idx("- LAST SHIPPED: **r413**")
lines[p] = ("- LAST SHIPPED: **r414** (build 260619.85, 20 Sept ≈18:30, session 29 Round 5 — THE NESTED ACTIVITY BOX: the r217 / r266 synthetic widget box never opens "
            "inside an open activity box, the widget belongs to the open box; `standalone_widget_box.inside_open_activity`, env `NESTBOX_OFF`; 108 nested boxes on 94 pages / "
            "65 modules → 0, the gold nests on 3 pages; the two un-nesting forms scored on the gate's own `match()` — suppress 81 up / 3 down vs close-the-outer 28 / 24; "
            "probe OFF = disk 2555 / 2555, ON 94 pages / 65 modules; SCOPED regeneration of the 65 — scoped ship #6 since the 19 Sept FULL (2 of headroom); "
            "**skeleton 53.817 → 53.886 % (+0.0696pp), ≥50 1408 → 1412, ≥75 236 → 238, ≥90 20, RAW 37.997 % @ 2349 pairs**; every other gate EXACT; 16 selftests GREEN; "
            "the miner 182 → 181); before it **r413** (build 260619.84, 20 Sept ≈17:35, session 29 Round 4 — the owned half of the r412 class, `HEADTABLEOWNED_OFF`, "
            "8 up / 0 down, +0.0080pp), **r412** (build 260619.83, the heading-then-table owner form, `HEADTABLE_OFF`, +0.0139pp, ≥50 +2), **r411** (build 260619.82, "
            "the tile menu ROW+COL shell, `TILEMENUROW_OFF`, +0.0058pp) and **r410** (build 260619.81, the WJFUN tile-page dialect, `TILEPAGE_OFF`, skeleton "
            "53.680 → 53.789 %, ≥50 +8). **Corpus = r414** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r414; `outputs/_s29_r414_sk_final.json` the "
            "skeleton state; ceiling 90.9 % → 53.886 = **59.3 % of achievable**).")
q = idx("- Plateau window (§4): **1 of 3**")
lines[q] = "- Plateau window (§4): **0 of 3** — r414 RESET it (+0.0696pp, ≥50 +4, ≥75 +2). Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.84")
lines[r] = lines[r].replace("AppVersion 260619.84 (r413, session 29 Round 4, 20 Sept); before it 260619.83 (r412)", "AppVersion 260619.85 (r414, session 29 Round 5, 20 Sept); before it 260619.84 (r413) / 260619.83 (r412)")
assert "260619.85" in lines[r]
t = idx("- s29-r4 (engine r413")
lines.insert(t + 1, "- s29-r5 (engine r414, build 260619.85, 20 Sept ≈17:40 → 18:30) · THE NESTED ACTIVITY BOX — a synthetic widget box (the r217 standalone box / the r266 level-pages box, decided after the `isNewActivity` guard) opened INSIDE a writer's still-open activity frame on 94 pages / 65 modules (108 boxes; the gold nests on 3 pages); found through the empty-shell census (`_s29_r5_emptyrows.py`: 818 shells, 725 the module menu's, the body's 154 decomposed — the nested box's close is the shell's mechanism) and measured by `_s29_r5_nestbox.py` (the gold keeps the widget inside the outer box 19 / separate 18 / no box 6 / 54 absent); the two un-nesting forms scored on the gate's own `match()` (`_s29_r414_variants.sh`): SUPPRESS the synthetic box everywhere 81 up / 3 down (+163.5) vs close-the-outer 28 / 24 (+27.7) — the widget belongs to the open box; `standalone_widget_box.inside_open_activity {enabled, env NESTBOX_OFF, close_outer_subjects: []}` · SHIPPED · probe OFF = disk 2555 / 2555, ON 94 pages / 65 modules · SCOPED regen of the 65 (scoped #6 since the 19 Sept FULL; 0 stale; spot-check 12 / 12) · skeleton 53.817 → 53.886 (+0.0696pp), ≥50 +4, ≥75 +2; all else EXACT · miner 182 → 181 · plateau RESET (0 of 3) · recorded: the module-menu empty shell (class C content 445 pages; FRFUN / ConnectED no-menu-element = a family `menu_type` row), the 38 writer-owned empty boxes, the 14 HPFUN omitted-prompt rows, the unclassified-path later-heading rows (gold 0.57 — the r362 guard stands), `iframe.embed-responsive-item` (KB-over-gold)")
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with io.open(ARCH, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n## Session 29 — Round 5 PICK (engine r414) + what shipped — THE NESTED ACTIVITY BOX (20 Sept ≈17:40 → 18:30 NZST)\n\n" + "\n".join(pick).rstrip("\n") + "\n" + shipped + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
