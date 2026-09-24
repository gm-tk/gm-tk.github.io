#!/usr/bin/env python3
"""Session 45 Round 11 — record the PICK pass (no engine change) in LOOP_STATE.md. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-s45-r11.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 45 Round 11 (25 Sept 08:35 → 08:50 real clock) — a PICK pass, no engine change.** (1) **Round 7's 'absent' group** (246 lesson "
         "pages with an empty Claude menu whose gold menu text is nowhere on Claude's page): beyond the ≈ 126 r436-declined repeated overview "
         "menus, the rest carry DEVELOPER-authored lesson intentions — MXFU202 lesson 2's 'to solve true or false number sentences… / to "
         "notice patterns' is not in the WT (the writer gave only the module-level list) — class C. (2) **WT tables that open with a "
         "learning-intentions lead** (`_s45_r11_litable.py`): 80 — EXPFUN's scenario activity tables 60 body / body (gold and Claude agree), "
         "12 absent / body, TEDC401 / 402's `[Overview]` one-cell LI / SC table 6 (the gold's menu) — the TEDC form is two modules, under the "
         "floor. (3) **The MTK drop-down-menu template's tab set** (TRR203 / TRR301 / PMT101): the gold ships the bilingual Overview / Strand / "
         "Dispositions / … tab set, Claude a generic Overview | Information pair — the second `[Content for DROP DOWN MENU]` table's header "
         "names THREE tabs at once ('Strands | Dispositions … | Key Objectives' / 'Ngā Whenu | Ngā Toi Mokopuna | Ngā Whāinga Matua'), which "
         "the r212 composer does not split — three overviews, skeleton-blind (the tabs collapse), a family dialect for its own round. (4) The "
         "r488 follow-up — `_verify_carousel.cjs`'s 8 video ids on BLL116 / BLL144 / BLL155 come from the WT's hyperlinks (not its visible "
         "text) and BLL155's six are all on the gold's own page; BLL116's four are in no gold page (the developer's swap, class C).")
k = find("## Round log")
L.insert(k + 1, "- s45-r11 (no engine change, 25 Sept 08:35 → 08:50) · a PICK pass: Round 7's absent lesson LIs are developer-authored (class C); WT LI "
         "tables are EXPFUN activity content (body on both sides) + TEDC's 6-page `[Overview]` table; the MTK drop-down template's three-tab "
         "header (TRR203 / TRR301 / PMT101) recorded as a dialect; the carousel video ids class C · plateau 0 of 3 (neither).")
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(L)); os.replace(S + ".tmp", S)
print("ok", os.path.getsize(S))
