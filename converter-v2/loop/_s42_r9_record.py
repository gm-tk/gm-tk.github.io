#!/usr/bin/env python3
"""Session 42 Round 9 — a PICK pass, no engine change: the loss ledger's two largest families (BLL2 / BLL1 scoped miners), the refreshed
coverage dashboard and the widget decline census. LOOP_STATE.md: a Declined-classes entry + the round-log line. .bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
shutil.copyfile(S, S + ".pre-s42-r9.bak")
k = find("## Declined classes")
L.insert(k + 1, "- **Session 42 Round 9 (24 Sept 16:28 → ≈16:55) — a PICK pass, no engine change: the loss ledger's two largest families + the "
         "widget-build lane's census.** BLL2xx (148 pages / 54 modules, `_s42_r9_miner_bll2.md`): the footer ORDER (gold home → prev → next "
         "on BLL210-type pages vs Claude prev → next → home) is KB 01B's own example order — Claude KB-correct; the menu's `div.row` wrapper "
         "around the tabs (row #6, 12 modules — the gold omits it) is KB c67 / 01B's canonical shell — Claude KB-correct; the activity-region "
         "EXTRA rows are the s37-declined box boundary. BLL1 (150 pages, `_s42_r9_miner_bll1.md`): the menu rows are the D10-9 label "
         "override and the s36-r5 `section_content_is_list` decline (no line-level discriminator). The coverage dashboard refreshed on "
         "r470 (`outputs/_s42_dashboard_run.sh`: 44.8 % of 7,290 writer-tagged widgets build) and the decline records grouped by the "
         "builder's reason (`_s42_r9_declines.py` → `.log`): the big buckets are member-less bundles (the writer's tag with no content — "
         "not derivable) and many one-off shapes, EXCEPT dragAndDrop's two-column tables (`width < min_columns 3`: 209 bundles / 182 "
         "pages / 139 modules; 6×2 40, 5×2 30, 4×2 29) → Round 10 (the D10-3 build lane).")
k = find("## Round log")
L.insert(k + 1, "- s42-r9 (no engine change, 24 Sept 16:28 → ≈16:55) · a PICK pass: BLL2 / BLL1 scoped miners (footer order + menu row "
         "wrapper = KB-correct; the rest dispositioned), the dashboard refreshed (coverage 44.8 %), the widget decline census → the "
         "two-column dragAndDrop tables (182 pages / 139 modules) queued as Round 10 · plateau 2 of 3 (neither).")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
