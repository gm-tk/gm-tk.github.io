#!/usr/bin/env python3
"""ROUND 460 finalise — BUILD_CHANGELOG.md (prepend), Config.js AppVersion, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json,
KB_AMALGAMATION_STATUS.md row 67, LOOP_STATE.md (marker cleared, Position, round log, PICK → archive). Line edits only; .bak kept.
Run under WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)

# ---------- BUILD_CHANGELOG.md ----------
P = os.path.join(CV, "BUILD_CHANGELOG.md"); s = rd(P)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert s.startswith(head)
entry = """## 2026-09-24 (round 460, build 260620.30) — KNOWLEDGE AND PRACTICES ARE THEIR OWN OVERVIEW TABS (KB constraint 67 / CL-0040): in a tabbed overview menu the writer's Knowledge and Practices sections now each get their own nav tab, in the KB's canonical order Overview → Knowledge → Practices → Information → Standards, and the Information tab those moves leave empty is removed — the loop's session 41 Round 8 (the loss-ledger / content re-read lane → the KB queue); THE LEDGER'S FULL-SHIP BACKSTOP

### 1. WHAT CHANGED

**The find** (`outputs/_s41_r8_lost.py` → 3.0 % of the Writers-Template text the human carries is on no Claude page; the WJFUN / science / language rows led to the module menu; `outputs/_s41_r8_kppane.py`): 36 tabbed-archetype overviews whose Knowledge / Practices sections sat inside Claude's Overview pane (or its Information pane), while the gold moves them out — 21 into their own nav tabs, 10 into Information. KB constraint 67 (CL-0040, Universal; KB 10 §2 "whenever the overview menu IS tabbed its tab composition follows the canonical set") makes them their own tabs; the r263 mechanism (`menu.extra_tabs.curriculum_tabs`) only fired for a registry row naming the section (`SCCH|7-8`).

**The fix** (`MenuBuilder` promotion + `SkeletonBuilder` shell order; data `Emit_Templates.menu.extra_tabs.curriculum_tabs.kb_canonical` {labels, heading_pattern, drop_empty_tab2, exclude_subjects}; env **`KPTABS_OFF`**, byte-identical OFF): a heading whose folded text IS the section heading (`^(year N |level N )?(knowledge|practices?):?$` — never "Learning intentions – Cultural knowledge") opens a canonical Knowledge / Practices tab titled by canon (`<h4><span>Knowledge</span></h4>`, never the writer's "Knowledge:"); the tab LEADS (it renders before the Information slot); an Information tab the promotions emptied is dropped (the KB omission rule). Excluded: subject **BLL** (CL-0040 leaves the open BLL263 D2 overview tab-split question untouched) and **WJFUN** (the r410 tile dialect — its K / P headings never reach the menu walk; a follow-up).

### 2. PROOF

- In-memory A/B (`outputs/_r460_probe_run.sh`): OFF 3217 / 3217 identical; ON 28 pages / 19 modules (BLLR201-203, ENGC204 / 206 / 403, ENGS405, ENO2060, FRNO901 / 902, GENO901, HPRE203 / 301, SCBI301, SCES201, SCPH301, SSCI104, SSCI205 ×10 pages — its lesson pages carry the module menu, SSEA203).
- **The skeleton SCAFFOLD is blind to this BY DESIGN**: the module menu's `div.tabs` collapses to one WIDGET line, so the pre-score reads +0.0 on every page. The menu-only evidence (`outputs/_r460_rawmenu.py`, the `#module-menu-content` subtree's skeleton vs gold): **20 up / 7 down, menu pp-sum +262.8; RAW skeleton pp-sum +77.8** (BLLR202 / 203 63 → 96, SCPH301 53 → 93, SCBI301 63 → 89, ENGC204 59 → 89, HPRE203 56 → 88, GENO901 32 → 64; SSCI205's Information-pane gold still rises 72 → 86). The first ON probe put the tabs AFTER Information (ENGC403 menu-only −9): repaired in-round with the `lead` order.
- NAMED KB overrides (the gold keeps K / P in tab 1 or drops them; KB rank 1 outranks it, LOOP §1b): SSCI104 (menu-only 71 → 40), ENGS405 (79 → 56), SSEA203 (58 → 47), ENO2060 (49 → 38); FRNO902 27 ← 32 is the repeat-collapse artefact (its two new panes share one shape and collapse to "2× repeated"); BLLR201 / ENGC206 −0.3 / −0.9.
- **THE FULL REGENERATION** (`outputs/_r460_fullship_par.sh`, 42 batches, 4 workers, every rc 0): stale 0; `_content_manifest.py fresh --affected` the 19 → **0 truly stale; the 523 unaffected byte-identical to the manifest**. Ledger `record-full --round 460`: scoped-since reset to 0.

### 3. PROTECTED GATES

- Skeleton **54.9376 % @ 2524 → 54.9376 % @ 2524 (+0.0000pp — EXACT, 0 movers)**; ≥50 1581, ≥75 275, ≥90 25; **RAW 38.934 → 38.967 (+0.033pp)**.
- compare_structure 16719 / 208 / 896 / 24 EXACT; body_compare 61 / 5 / 176 / 239 EXACT; clean 2621 / 2667 EXACT; leak 75 / 46 EXACT; tags 9557; selftests 50 PASS; index GREEN; the miner 197 CANDIDATE @ 2524.
- `_verify_menulabels.cjs` over the 19: ENO2060 title-above-label 4 on its LESSON pages — pre-existing (identical under `KPTABS_OFF`; only ENO2060_0_0 changed), recorded as its per-module baseline (the r359 precedent); every other module 0.
- Plateau (§4): the PICK predicted a small skeleton move before the WIDGET collapse was found; it delivered +0.0000pp → counted as NOT moving (conservative): **1 of 3**.

"""
assert "(round 460," not in s[:3000]
wr(P, head + entry + s[len(head):])
print("changelog ok")

# ---------- Config.js ----------
P = os.path.join(CV, "app", "js", "Config.js"); s = rd(P)
old = '\tstatic AppVersion = "260620.29";'
assert s.count(old) == 1
s = s.replace(old, "\t// ROUND 460 (260620.30): KNOWLEDGE AND PRACTICES ARE THEIR OWN OVERVIEW TABS (session 41 Round 8; KB constraint 67 / CL-0040). In a TABBED overview menu the Knowledge / Practices sections now take their own canonical nav tabs (Overview -> Knowledge -> Practices -> Information -> Standards), titled by canon, and an Information tab the promotions emptied is dropped (the KB omission rule) — r263 did this only for the SCCH|7-8 registry row. Emit_Templates menu.extra_tabs.curriculum_tabs.kb_canonical, env KPTABS_OFF; BLL (the open BLL263 D2 question) and WJFUN (the r410 tile dialect) excluded. 19 modules / 28 pages; THE FULL BACKSTOP (523 unaffected byte-identical); skeleton EXACT (the menu tabs are one WIDGET line), RAW +0.033pp, menu-only 20 up / 7 down.\n" + '\tstatic AppVersion = "260620.30";', 1)
wr(P, s); print("config ok")

# ---------- OPERATING_GUIDE.md ----------
P = os.path.join(CV, "OPERATING_GUIDE.md"); s = rd(P)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 459 BASELINE"
assert s.count(a9) == 1
s = s.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 460 BASELINE (Knowledge / Practices are their own overview tabs — KB c67, `KPTABS_OFF`; THE FULL BACKSTOP, ledger reset to 0): SCAFFOLD mean 54.9376% / >=50% 1581 / >=75% 275 / >=90% 25 / RAW 38.967% @ 2524 pairs — +0.0000pp (the menu tabs are one WIDGET line), RAW +0.033pp; cs 16719 / 208 / 896 / 24, body 61 / 5 / 176 / 239, clean 2621 / 2667, leak 75 / 46 — all EXACT.** Previous: **ROUND 459 BASELINE", 1)
a11 = "| `INTROFORM_OFF` | 459 |"
assert s.count(a11) == 1
s = s.replace(a11, "| `KPTABS_OFF` | 460 | **KNOWLEDGE AND PRACTICES ARE THEIR OWN OVERVIEW TABS** (session 41 Round 8; KB constraint 67 / CL-0040). Reverts `menu.extra_tabs.curriculum_tabs.kb_canonical`: the Knowledge / Practices sections of a tabbed overview return to the Overview (or Information) pane unless a registry row names them (r263's SCCH|7-8), and the emptied-Information drop and the `lead` tab order go with them; byte-identical to r459. 19 modules / 28 pages; skeleton EXACT (the menu tabs are one WIDGET), RAW +0.033pp. |\n" + a11, 1)
a14 = "- **Build:** `260620.29` (round 459"
assert s.count(a14) == 1
s = s.replace(a14, "- **Build:** `260620.30` (round 460 — **KNOWLEDGE AND PRACTICES ARE THEIR OWN OVERVIEW TABS** (KB c67): the canonical tab set in every tabbed overview, BLL / WJFUN excluded; `KPTABS_OFF`; **THE FULL BACKSTOP** — ledger reset to 0; 19 modules / 28 pages; skeleton 54.9376 % EXACT, RAW 38.967 %).\n" + a14, 1)
wr(P, s); print("OG ok")

# ---------- gate_baseline.json ----------
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json")
shutil.copyfile(P, P + ".pre-r460.bak")
L = rd(P).split("\n")
def setv(key, old, new):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            L[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            L.insert(i, line); return
    raise SystemExit(f"anchor not found {key}")
setv("build", '"260620.29"', '"260620.30"'); setv("round", "459", "460")
insert_before("_note_r459", '    "_note_r460": "Round 460 (session 41 Round 8, 2026-09-24; KB constraint 67 / CL-0040) — KNOWLEDGE AND PRACTICES ARE THEIR OWN OVERVIEW TABS (KPTABS_OFF) — THE FULL BACKSTOP (42 batches, 523 unaffected modules byte-identical, ledger reset to 0). 19 modules / 28 pages changed, all in the module menu, which the skeleton SCAFFOLD collapses to one WIDGET line: SCAFFOLD EXACT, RAW 38.934 -> 38.967; cs / body / defect / leak EXACT; menu-only 20 up / 7 down (outputs/_r460_rawmenu.log).",')
setv("raw_mean_pct", "38.93", "38.97")
insert_before("_note_r459_state", '    "_note_r460_state": "r460 (the K / P overview tabs, FULL): SCAFFOLD 54.9376 @ 2524 EXACT (0 movers), RAW 38.934 -> 38.967; ≥50 1581 / ≥75 275 / ≥90 25.",')
for i, l in enumerate(L):
    if l.strip() == '"TWHA904": 1':
        L[i] = l + ","; L.insert(i + 1, l.replace('"TWHA904": 1', '"ENO2060": 4')); break
else: raise SystemExit("TWHA904 per_module not found")
out = "\n".join(L); json.loads(out); wr(P, out)
# the menulabels note sits inside the menulabels block: insert after its "_note_r359" (the SECOND one — the menulabels block)
L = rd(P).split("\n"); idx = [i for i, l in enumerate(L) if l.strip().startswith('"_note_r359": "Round 359: the verifier over the whole changed Inquiry family')]
assert len(idx) == 1
L[idx[0]] = L[idx[0]].rstrip()
if not L[idx[0]].endswith(","): L[idx[0]] += ","
L.insert(idx[0] + 1, '    "_note_r460": "Round 460: the verifier over the 19 changed modules — ENO2060 carries 4 PRE-EXISTING title-above-label defects on its LESSON pages (identical under KPTABS_OFF; r460 changed only ENO2060_0_0). Recorded as its per-module baseline; ✗ only above 4."')
out = "\n".join(L); json.loads(out); wr(P, out)
print("gate_baseline ok")

# ---------- KB_AMALGAMATION_STATUS.md ----------
P = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); s = rd(P)
old = "**LIVE** for the tab set + headings (`tooltip=\"Overview\"` 493 pages"
assert s.count(old) == 1
s = s.replace(old, "**LIVE** for the tab set + headings — **the Knowledge / Practices tabs CAPTURED universally in r460** (`curriculum_tabs.kb_canonical`, KPTABS_OFF; before it only SCCH|7-8; BLL (the open D2 question) and WJFUN excluded) (`tooltip=\"Overview\"` 493 pages", 1)
wr(P, s); print("KB status ok")
