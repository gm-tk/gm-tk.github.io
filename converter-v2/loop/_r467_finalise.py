#!/usr/bin/env python3
"""ROUND 467 finalise (session 42 Round 4 — KB c67 / 01B the canonical Standards tab, STDTAB_OFF) — BUILD_CHANGELOG.md (prepend),
Config.js AppVersion 260620.33 -> 260620.34, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json, KB_AMALGAMATION_STATUS.md (row 67
note), LOOP_STATE.md (marker cleared, Position, plateau, round log, follow-ups; the marker → archive). Line edits only; .bak kept;
nothing written until every anchor is found. Run under WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 467," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.33";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 466 BASELINE"; a11 = "| `COURSECODE_OFF` | 466 |"; a14 = "- **Build:** `260620.33` (round 466"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK); k67 = "**the Knowledge / Practices tabs CAPTURED universally in r460**"; assert sk.count(k67) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 467 IN FLIGHT — NOT PROVEN**", "- **Before r467: no round in flight**", "- LAST SHIPPED: **r466**",
          "- Plateau window (§4): **2 of 3** — r466", "- Standing facts: AppVersion 260620.33", "## Round log",
          "**Next session starts with:**", "- **(s42-r3) THE PLACEMENT CENSUS"):
    find(p)
DOWN = "ENGJ202 / ENGJ301 / ENGJ402 / ENGR301 / ENGR302, MXDB301 / MXDI201 / MXDI301 / MXEO102 / MXEX301 / MXFL104 / MXFL203 / MXFL401 / MXFU302, OSOH201"
entry = f"""## 2026-09-24 (round 467, build 260620.34) — THE STANDARDS TAB (KB constraint 67 / 01B): a tabbed overview's writer section "Aromatawai | Assessment for Learning" is now its own canonical **Standards** tab even where the mined tab registry has no row for the module's subject — where it used to be folded into the Information tab — the loop's session 42 Round 4 (the placement census, §1g, P1)

### 1. WHAT CHANGED

**The find** (the placement census `outputs/_placement_census.py`, P1; `outputs/_s42_r4_navtabs.py`): 27 modules whose gold overview carries a Standards tab (opening with the writer's "Assessment for Learning" heading) where Claude folded that section into Information — ART1002 / 1003, CBI1004 / 1005 / 1008 / 1009, COM1002 / 1006, DAN1003 / 1004 / 1006, DTC1004 / 1005, EXBP901, GEO1004–1006, GER1002, HIS1001, MUS1004, PWY1002 / 1007–1009 (gold Overview > Standards, no Information), SPA1004, XTAS101 / 103; 49 modules already matched. The mechanism: the assessment section is promoted only through `menu.extra_tabs.registry` (mined 10 July from the gold, keyed subject|phase — 26 groups), which predates the September-intake NCEA families. KB constraint 67 (CL-0040, Universal) + 01B "THE FIVE CANONICAL PANELS": the tabbed overview is Overview → Knowledge → Practices → Information → **Standards/Assessment**; "for the last tab, use **Standards** … the internal heading is **Assessment for Learning** either way"; all headings `<h5>`, no te reo; the omission rule. The skeleton is blind to it (the menu is one WIDGET line).

**The fix** (`MenuBuilder` extra-tab walk, beside r460's Knowledge / Practices; data `Emit_Templates.menu.extra_tabs.curriculum_tabs.kb_canonical.standards` {{enabled, env, label "Standards", drop_empty_tab2, exclude_subjects []}}; env **`STDTAB_OFF`**, byte-identical OFF; independent of `KPTABS_OFF`): a tab-2-routed heading that resolves to the `assessment` section opens the canonical Standards tab when the registry names no label for it (a registry row still decides its own label — MXEX|9-10 / SSOG|7-8 / XMES|4-6 keep "Assessment"); the pane keeps the English-reduced `<h5>Assessment for Learning</h5>`; an Information tab the promotion empties is dropped (c67's omission rule — PWY1002 / 1008 now read Overview > Standards, the gold's own tab set).

### 2. PROOF

- In-memory A/B over all 545 modules (`outputs/_s42_probe_run.sh r467`): **OFF 3217 / 3217 identical; ON 42 overview pages / 42 modules.** 19 of the 27 gold-Standards modules (the other 8 — ART1002 / 1003, EXBP901, HIS1001, PWY1007 / 1009, XTAS101 / 103 — carry the assessment text in Claude's BODY, not its menu: a menu/body-boundary sub-class, recorded), CHI1003 / 1004 / 1005 / JPN1004 (excluded from scoring, D14-21), and 19 modules whose gold keeps the section in Information.
- Menu-only compare (`outputs/_s42_rawmenu.py r467`, the r460 instrument): **24 up / 16 down, menu pp-sum +88.8; RAW pp-sum +65.6** — SPA1004 43.7 → 59.2, GER1002 39.4 → 50.8, MUS1006 70.4 → 84.2, COM1002 43.8 → 53.7, COM1005 54.0 → 62.0, DTC1005 68.0 → 73.8, DAN1006 70.2 → 75.2. **NAMED KB overrides (the gold keeps "Assessment for Learning" as an Information `<h5>`; CL-0040 of 16 July postdates them; KB rank 1 outranks the gold, LOOP §1b):** {DOWN} (menu-only −2.1 to −12.2; ENGJ301 70.6 → 58.4 and MXFL401 72.3 → 62.7 the largest); DAN1004 −0.1 (RAW +5.7). The placement census after the ship: `menu:Standards → menu:Information` 21 modules → **0** corpus-wide; SAME +39 / MOVED −50 blocks.
- Scoped regeneration of the 42 + the 12-module spot-check (`_r467_regen.sh`): 0 truly stale (42 affected, 500 untouched byte-identical), spot-check 12 / 12, the disk = the probe's ON files 361 / 361. `scoped_ship.sh --toggle STDTAB_OFF --round 467`: **PASS**, scoped **#3** since the r460 FULL.

### 3. PROTECTED GATES

- Skeleton **55.2654 % @ 2487 EXACT** (0 movers — skeleton-blind by design, the §1g lane); ≥50 1575 / ≥75 276 / ≥90 25; **RAW 39.200 → 39.216 %**.
- compare_structure 16709 / 208 / 896 / 24, body_compare 61 / 5 / 175 / 238, clean 2584 / 2629, leak 74 / 45 — all EXACT; tags 9557; every verifier ✓; selftests 50 PASS / 0 FAIL; feature index GREEN; the miner 197 CANDIDATE @ 2487.
- Plateau (§4): a skeleton-blind placement round (§1g item 1) — neither counts nor resets: **2 of 3** stands.

**Ledger:** scoped #3 since the r460 FULL · data `Emit_Templates.menu.extra_tabs.curriculum_tabs.kb_canonical.standards` · env `STDTAB_OFF` · code `MenuBuilder` (the extra-tab walk + the dropTab2 branch) · tools `outputs/_s42_r4_navtabs.py`, `_s42_rawmenu.py`, `_r467_{{regen,postship}}.sh`, `_r467_finalise.py`, `_r467_{{rawmenu,scoped_ship,gates,sk_full,skdelta,selftests,index}}.log`, `_pc_r467.{{md,json}}`, `_affected_r467.txt` · AppVersion 260620.34.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 467 (260620.34): THE STANDARDS TAB (session 42 Round 4; KB constraint 67 / 01B). A tabbed overview's 'Aromatawai | Assessment for Learning' section is its own canonical Standards tab even where menu.extra_tabs.registry has no row for the module's subject|phase; an Information tab the promotion empties is dropped. Emit_Templates menu.extra_tabs.curriculum_tabs.kb_canonical.standards, env STDTAB_OFF; 42 modules; skeleton exact (menu = WIDGET), menu-only 24 up / 16 down (the ENG / MX golds named KB overrides), RAW +0.017pp.\n" + '\tstatic AppVersion = "260620.34";', 1)
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 467 BASELINE (the canonical Standards tab — KB c67 / 01B, `STDTAB_OFF`; SCOPED, scoped #3 since the r460 FULL): SCAFFOLD mean 55.2654% / >=50% 1575 / >=75% 276 / >=90% 25 / RAW 39.216% @ 2487 pairs — skeleton EXACT (the menu is one WIDGET line), RAW +0.017pp; menu-only 24 up / 16 down (ENG / MX golds NAMED KB overrides); cs 16709 / 208 / 896 / 24, body 61 / 5 / 175 / 238, clean 2584 / 2629, leak 74 / 45 — all EXACT.** Previous: **ROUND 466 BASELINE", 1)
so = so.replace(a11, "| `STDTAB_OFF` | 467 | **THE CANONICAL STANDARDS TAB** (session 42 Round 4; KB constraint 67 / 01B). Reverts `menu.extra_tabs.curriculum_tabs.kb_canonical.standards`: a tabbed overview's assessment section is promoted to its own tab only through a registry row again (it folds into Information otherwise); byte-identical to r466. 42 modules; skeleton exact; menu-only 24 up / 16 down. |\n" + a11, 1)
so = so.replace(a14, "- **Build:** `260620.34` (round 467 — **THE CANONICAL STANDARDS TAB** (KB c67 / 01B): a tabbed overview's \"Assessment for Learning\" section is its own Standards tab without a registry row; `STDTAB_OFF`; scoped #3 since the r460 FULL; 42 modules; skeleton exact, RAW 39.216 %).\n" + a14, 1)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r467.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            G[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.33"', '"260620.34"'); setv("round", "466", "467")
insert_before("_note_r466", '    "_note_r467": "Round 467 (session 42 Round 4, 2026-09-24; KB constraint 67 / 01B) — THE CANONICAL STANDARDS TAB (STDTAB_OFF): 42 modules; SCAFFOLD 55.2654 EXACT (menu = WIDGET), RAW 39.200 -> 39.216; menu-only 24 up / 16 down (ENGJ / ENGR / MX golds NAMED KB overrides); every other gate EXACT; scoped #3 since the r460 FULL.",')
setv("raw_mean_pct", "39.2", "39.22")
insert_before("_note_r466_state", '    "_note_r467_state": "r467 (the Standards tab): SCAFFOLD 55.2654 @ 2487 EXACT, RAW 39.200 -> 39.216; 0 movers.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
sk = sk.replace(k67, k67 + " **and the Standards/Assessment tab CAPTURED universally in r467** (`curriculum_tabs.kb_canonical.standards`, STDTAB_OFF — the tab-2 \"Assessment for Learning\" section without a registry row; 42 modules; the ENGJ / ENGR / MX golds that keep it in Information are NAMED overrides)", 1)
wr(PK, sk); print("KB ok")
shutil.copyfile(S, S + ".pre-r467-finalise.bak")
i = find("- **ROUND 467 IN FLIGHT — NOT PROVEN**"); marker = L[i].replace("24 Sept ≈15:25 real clock", "24 Sept 15:05 real clock")
L[i] = ("- **No round in flight** (24 Sept 2026 ≈15:25, session 42 Round 4 — r467 (the Standards tab, KB c67) SHIPPED and committed; "
        "the in-flight marker is cleared). LAST SHIPPED **r467** (260620.34); **LAST FULL = r460**; ledger **scoped #3** since it (5 of "
        "headroom). Next: the §3 PICK pass — the miner's rows, the placement census (re-run it: `outputs/_placement_census.py`) and the "
        "follow-ups.")
k = find("- **Before r467: no round in flight**"); prior = L[k]; del L[k]
k = find("- LAST SHIPPED: **r466**"); L[k] = L[k].replace("- LAST SHIPPED: **r466**", "- Before it: **r466**", 1)
L.insert(k, "- LAST SHIPPED: **r467** (build 260620.34, 24 Sept ≈15:22, session 42 Round 4 — KB c67 / 01B: THE CANONICAL STANDARDS TAB, "
         "`STDTAB_OFF`; 42 modules; SCOPED, **scoped #3 since the r460 FULL**, scoped_ship PASS; **skeleton 55.2654 % @ 2487 EXACT** "
         "(the menu is one WIDGET line), RAW 39.200 → 39.216 %; menu-only 24 up / 16 down (the ENGJ / ENGR / MX golds NAMED KB "
         "overrides); cs / body / clean / leak EXACT; `gate_baseline.json` at r467; the miner 197 CANDIDATE).")
k = find("- Plateau window (§4): **2 of 3** — r466")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r466", "- Plateau window (§4): **2 of 3** — r467 a skeleton-blind placement "
                    "round (§1g: judged on the menu-only compare; neither counts nor resets); r466", 1)
k = find("- Standing facts: AppVersion 260620.33")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.33 (r466", "- Standing facts: AppVersion 260620.34 (r467 the canonical Standards "
                    "tab, KB c67 — session 42 Round 4, 24 Sept); before it 260620.33 (r466", 1)
k = find("- **(s42-r3) THE PLACEMENT CENSUS")
L[k] = L[k].replace("(P1) the Standards / Assessment tab — 27 modules, KB c67 → **Round 4**;", "(P1) the Standards / Assessment tab — "
                    "27 modules, KB c67 → **SHIPPED r467** (19 of the 27 + 23 more; the remaining 8 — ART1002 / 1003, EXBP901, HIS1001, "
                    "PWY1007 / 1009, XTAS101 / 103 — carry the assessment text in Claude's BODY, not the menu: a menu/body-boundary "
                    "sub-class, P1b, 8 modules — below the chrome floor alone);", 1)
assert "SHIPPED r467" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s42-r4 (engine r467, build 260620.34, 24 Sept 15:05 → ≈15:25) · KB c67 / 01B: THE CANONICAL STANDARDS TAB (a tabbed "
         "overview's \"Assessment for Learning\" section is its own Standards tab without a registry row; an emptied Information tab "
         "dropped) · SHIPPED scoped #3 · 42 modules · skeleton EXACT (menu = WIDGET), RAW +0.017pp; menu-only 24 up / 16 down "
         "(ENG / MX golds named KB overrides) · the census's Standards→Information 21 → 0 · plateau 2 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r467** (260620.34, "
        "the Standards tab); LAST FULL = **r460**; ledger scoped #3; plateau **2 of 3**; 2,487 pairs. Next: the §3 PICK pass with the "
        "placement census (`outputs/_placement_census.py`; finds P1b–P8 in Follow-up candidates). Needs Chris #17–#19, #22.")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Session 42 — Round 4 PICK (engine r467) + what shipped\n\n" + marker + "\n" + prior + "\n"
    "- **What shipped (r467, 260620.34):** `MenuBuilder`'s extra-tab walk promotes the tab-2 `assessment` section to the canonical "
    "Standards tab when the registry names no label (data `curriculum_tabs.kb_canonical.standards`, env `STDTAB_OFF`), and drops an "
    "Information tab the promotion empties. Probe OFF 3217 identical / ON 42 pages / 42 modules; menu-only 24 up / 16 down (+88.8); "
    "scoped_ship PASS. Evidence `outputs/_r467_rawmenu.log`, `_s42_r4_navtabs.log`, `_pc_r467.md`.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
