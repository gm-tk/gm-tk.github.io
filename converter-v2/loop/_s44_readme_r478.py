#!/usr/bin/env python3
"""Session 44 Round 1 — rewrite the loop README's r478 row (BUILT, TOGGLED OFF -> SHIPPED). WSL."""
import io, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "pageforge-site", "converter-v2", "loop", "README.md")
s = io.open(P, encoding="utf-8", newline="").read(); L = s.split("\n")
idx = [i for i, l in enumerate(L) if l.startswith("| `_r478_{regen,postship}.sh`")]; assert len(idx) == 1
L[idx[0]] = ("| `_r478_{regen,postship,commit_named}.sh` / `_r478_finalise.py` / `_r478_{scoped_ship,sk_full,skdelta,sk_off,skdelta_off,off_regen_a,"
             "off_regen_b,off_diff,spotcheck_plan,fastloop_named,gates,gatecheck,gatecheck_csbc,selftests,index,postship_run}.log` / "
             "`_r478_probe_{OFF,ON,SAVE}*.log` / `_r478_{ON_pages,ON_modules,regen_codes,changed_before_off,row}.txt` / `_affected_r478.txt` / "
             "`_s43_r10_{linkdet,parents}.py` / `_s43_r10_inlinelinks*.log` / `_s43_stop.py` / `_s44_condense1.py` / `_s44_readme_r478.py` | "
             "`CONVERTER_V2/outputs/` | **Round 478 (session 43 Round 10, FINISHED session 44 Round 1, 2026-09-25) — KB c75 FOR THE ACTIVITY'S LEAD "
             "PROSE (`LEADLINKS_OFF`) — SHIPPED (260620.42, scoped #4, committed NAMED −0.0027pp)** — the link census re-run on r477, the OFF / ON "
             "probe (13 modules / 21 pages, identical in both sessions), the parent census, the regeneration + spot-check, the scoped ship (mean "
             "only), the named commit, the post-ship suite, the finalise; the s43 stop's flag-off regeneration and the s44 start condense. |")
io.open(P, "w", encoding="utf-8", newline="").write("\n".join(L)); print("README row r478 rewritten")
