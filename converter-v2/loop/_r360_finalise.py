#!/usr/bin/env python3
"""ROUND 360 (loop session 19 Round 4 — the footer link set follows the KB's sub-type forms) — finalise: changelog,
AppVersion (260619.30 → 260619.31), CLAUDE.md §9 / §11 (a note under TMPLDELTA_OFF) / §14, gate_baseline.json, loop/README.md.
Idempotent; LF via wr()."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-17 (round 360, build 260619.31) — THE FOOTER LINK SET FOLLOWS THE KB'S SUB-TYPE FORMS: a Fundamentals single-page module ships `home-nav` ONLY (06 §3.3 — ARFUN / ENFUN / MXFUN / TEFUN lose the phantom `next-lesson`), an Inquiry overview ships `prev-lesson + next-lesson + home-nav` (06 §3.4 — the BLL Inquiry parents, CEDK / CEDO / CEDR / CEDW, EXPlore gain `prev-lesson`) — eleven `Style_Anchor_Registry.json` corrections (four base rules, two level deltas, two no-evidence objects replaced, three `template_deltas.Inquiry` blocks + the BLL1 / BLL2 ones) and NO engine change; the autonomous loop's session-19 Round 4, the DIFF MINER's footer facts F26 / F35 / F36; **FULL regeneration of all 416 (36 batches, all rc 0), 52 modules / 52 pages changed; skeleton SCAFFOLD 52.072 → 52.076 % (+0.004pp; 49 movers, 40 up, the 9 dips named — every one an ORDER or a no-gold-footer page), every other gate EXACT; ledger FULL (counter 0); the first round of the plateau window**

### 1. WHAT CHANGED, IN ONE LINE

**Twenty-four single-page Fundamentals modules carried a `next-lesson` link with nothing next (the defaults tier's `next+home`; MXFUN's own value was a no-evidence object the resolver overlays because only `n/a` is on the unknown-literal list), and twenty-five Inquiry overviews lacked the `prev-lesson` link their gold and the KB carry (the BLL parents inherit their 80 Standard siblings' `next+home`; the CED / EXPlore bases resolve `—` → the r332 position default) — the registry now says what each family's gold says, through the tiers that already exist.**

### 2. THE EVIDENCE (docx → human → Claude)

- **ARFUN01** (one page) — gold `<ul class=" fundamentals-nav footer-nav"><li><a href="" class="home-nav" target="_parent"></a></li></ul>`; Claude before `<li><a href="" id="next-lesson" target="_self"></a></li><li><a href="" class="home-nav" target="_parent"></a></li>`; after: `home-nav` alone. ENFUN 8 / 8, TEFUN 7 / 8, MXFUN 3 / 3 the same (CHFUN already `home` 5 / 5).
- **BLL110** (an Inquiry parent, one page) — gold `<ul class="footer-nav inquiry-nav">` prev, next, home; Claude before next, home (the BLL1 level's `next+home` — right for BLL111 … BLL177, gold 0.99); after prev, next, home. **CEDW101** — gold prev, next, home on a plain `footer-nav`; Claude before next, home; after prev, next, home. **EXPFUN02** — gold prev, next, home (`inquiry-nav`); Claude before next, home (a `—` value → the KB's overview default); after prev, next, home.

### 3. THE MEASUREMENT (before coding — `outputs/_measure_r360_footer.py` → `_r360_footer.{json,log}`: the r357 instrument on the registry's pattern fields `footer_links` {overview, lesson, final} + `footer_class`, each side's page POSITION from its own page list)

- **44 link-set CLASS groups / 158 modules.** Derivable and KB-backed: **(A)** Fundamentals single-page overview = `home` — ARFUN 5 / 5, ENFUN 8 / 8, MXFUN 3 / 3, TEFUN 7 / 8 (06 §3.3 'typically home-nav only (no prev / next)'); **(B)** Inquiry overview = `prev + next + home` — BLL parents 10 / 11, CEDK 2 / 3, CEDO 2 / 2, CEDR204, CEDW 2 / 2, EXPFUN 4 / 5 + EXPFUN07 (06 §3.4 'footer-nav inquiry-nav with prev + next + home').
- **Recorded, not chased (§1b — the KB outranks the gold):** the gold's PREV link on ~50 Standard overviews (ART / ENGI / ENGR / ENGS / MXEO / MXFL / MXFU / PES / SSOG …) — 01B: overview = next + home; the gold's NEXT link on its content-final page (ANZH / HIS / MXFL / MXFU / OSAI / PES / XDLS / XTAS / PNR …) — the gold's real final page is its acks page, Claude's acks sit on the overview (01B; the r332 named override); the CED golds' `home, prev, next` and HPFUN's `home, prev, next` ORDER (01B / 07C: prev, next, home); TEFUN's plain `footer-nav` 5 / 8 vs the KB's `fundamentals-nav`; the BLL Standard children's plain `footer-nav` on 11 of 80 (their gold's 0.86 is `inquiry-nav`); the CEDT golds with NO footer element (2 modules); SSFUN a 3 : 3 tie; MXFUN's `inquiry-nav` via the inquiry-layout override (3 modules, below floor).
- **§1b authority:** KB level 1 (06 §3.3 / §3.4) + the families' own gold ≥ 0.80.

### 4. THE MECHANISM (DATA ONLY — `outputs/_r360_splice.py` + the three-tier patch; the r336 / r357 registry-correction precedent)

`ARFUN` / `ENFUN` / `TEFUN` base_rules `footer_links = {overview: home, lesson: prev+next+home, final: prev+home}`; `MXFUN` base_rules (the no-evidence object) and the `MXFUN0` level delta the same; `CEDK` base_rules and the `CEDK1` level delta (its no-evidence object) `{prev+next+home, prev+next+home, prev+home}`; `EXPFUN` base_rules (its no-evidence object) the same; `BLL1.template_deltas.Inquiry` (the r357 block) and a new `BLL2.template_deltas.Inquiry` `footer_links = {prev+next+home, prev+next+home, prev+home}` — the 80 Standard children untouched; `CEDO` / `CEDR` / `CEDW` bases gain `template_deltas.Inquiry.footer_links` the same — CEDO105 / 301 / 501 / 502, CEDR501, CEDW501 (Standard) untouched. The KB's order prev, next, home (`footer.value_map`). Env: the template-delta half under `TMPLDELTA_OFF` (r357); the base / level corrections have no toggle — the resolved-rules dump is the A/B.

### 5. THE PROOF

- **The resolved-rules dump of all 416 before / after (`_r359_resolved.json` → `_r360_resolved_after.json`):** `footer_links` changed on exactly 52 modules (the 49 class modules + CEDK101 / EXPFUN06 whose golds have no footer + the CEDR revision briefs), no other field anywhere; `TMPLDELTA_OFF=1` (`_r360_resolved_off.json`) reverts the 19 template-delta modules.
- **The in-memory probe (`_r360_probe.cjs`, all 416):** 52 changed pages — one `<li>` per page, exactly the `next-lesson` line removed (24) or the `prev-lesson` line added (28).
- **FULL regeneration** (`_r360_fullship_par.sh`, 36 batches, all rc 0, 5 m 01 s): `_stalecheck.sh` 0 stale; `_content_manifest.py changed` = the 52 exactly.
- **Gates (`_r360_gates.log`, every RESULT ✓, 0 ✗, pairs skipped 0):** **skeleton SCAFFOLD 52.0723 → 52.0761 % (+0.004pp; 49 movers — 40 up, pp-sum +7.4), ≥50 1096 / ≥75 161 / ≥90 14 EXACT, RAW 36.763 → 36.766 %**; the 9 dips NAMED — BLL240_0_0 60.16 → 59.20 (the one BLL parent whose gold overview is `next + home`), CEDK101_0_0 51.57 → 50.87 (no gold footer), EXPFUN07 / CEDO102 / CEDK102 / BLL120–150 (−0.33 … −0.01: the gold's `home, prev, next` ORDER on the CED pages and difflib's re-alignment of a two-line change on long pages). compare_structure exact 11617 / EXTRA 175 / missing 617 EXACT; body_compare 182 EXACT; structural defect clean 98.9 % (26 occ / 23 pages) EXACT; tags 9557 / 9557; every widget verifier ✓, entry parity PASS. **Plateau window (§4): 1 of 3** — the skeleton moved < 0.02pp and no other protected gate moved.

**Ledger:** FULL regeneration of all 416, `_ship_ledger.py record-full --round 360` (counter 0) · selftests 16 GREEN, fast-loop baseline, content manifest, feature index refreshed (`_r360_postship.sh`) · `DIFF_QUEUE.md` re-mined on the r360 corpus · KB delta: none (06 §3.3 / §3.4 state both forms).

"""
if "round 360, build 260619.31" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r360 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.31"' not in s:
    old = '\tstatic AppVersion = "260619.30";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 360 (260619.31): the footer link set follows the KB\'s sub-type forms — a Fundamentals single-page module home-nav only, an Inquiry overview prev + next + home (eleven Style_Anchor_Registry corrections, no engine change); the diff miner\'s footer facts.\n\tstatic AppVersion = "260619.31";')
    wr(P, s); print("Config.js: 260619.31")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 360 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 359 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 360 BASELINE (the footer link set follows the KB's sub-type forms — registry corrections, no engine change; FULL regeneration of all 416, ledger 0): SCAFFOLD mean 52.076% / >=50% 1096 / >=75% 161 / >=90% 14 / RAW 36.766% @ 1955 pairs, pairs skipped 0 — hold-or-improve; the nine r360 dips named (BLL240_0_0, CEDK101_0_0 and seven order / re-alignment dips under 0.35pp).** Previous — ROUND 359 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `TMPLDELTA_OFF` | 357 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| *(no new toggle)* | 360 | **THE FOOTER LINK SET FOLLOWS THE KB'S SUB-TYPE FORMS — data only.** Eleven `Style_Anchor_Registry.json` `footer_links` corrections: ARFUN / ENFUN / TEFUN / MXFUN (+ the MXFUN0 delta) `{home, prev+next+home, prev+home}` (06 §3.3, a single-page module has nothing next); CEDK (+ the CEDK1 delta) and EXPFUN `{prev+next+home, prev+next+home, prev+home}` (06 §3.4); `template_deltas.Inquiry.footer_links` on BLL1 / BLL2 / CEDO / CEDR / CEDW (the Standard members keep next + home). The template-delta half reverts under `TMPLDELTA_OFF`; the base / level corrections have no toggle — the resolved-rules dump `outputs/_r360_resolved*.json` is the A/B (the r336 precedent). |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.30` (round 359"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.31` (round 360 — **the footer link set follows the KB's sub-type forms** (a Fundamentals single-page module `home-nav` only — 06 §3.3; an Inquiry overview prev + next + home — 06 §3.4; eleven `Style_Anchor_Registry.json` corrections through the base / level / `template_deltas` tiers, no engine change); the autonomous loop's session-19 Round 4, the DIFF MINER's footer facts; FULL regeneration of all 416, 52 modules / 52 pages changed; skeleton 52.072 → 52.076 % (+0.004pp, nine dips named), every other gate EXACT; ledger FULL, counter 0; the plateau window 1 of 3).\n"
             + OLD14)
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r360" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 52.076
    d["skeleton"]["raw_mean_pct"] = 36.766
    d["skeleton"]["_note_r360"] = "Round 360: the footer link sets (registry corrections) — SCAFFOLD 52.0723 → 52.0761 (+0.004pp; 49 movers, 40 up; dips NAMED: BLL240_0_0 the one BLL parent whose gold overview is next + home, CEDK101_0_0 no gold footer, seven order / re-alignment dips ≤ 0.33pp), ≥50 1096 / ≥75 161 / ≥90 14 EXACT, RAW 36.763 → 36.766. Hold-or-improve from here."
    d["_meta"]["build"] = "260619.31"; d["_meta"]["round"] = 360
    d["_meta"]["_note_r360"] = "Round 360: the footer link sets — skeleton +0.004pp (named dips), every other gate EXACT; FULL regeneration of all 416, 52 modules / 52 pages; ledger FULL (counter 0); plateau window 1 of 3."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r360")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r360_finalise.py" not in s:
    A = "| `_measure_r359_inqmenu.py`"
    assert s.count(A) == 1, "README anchor"
    ROWS = ("| `_measure_r360_footer.py` / `_r360_footer.{json,log}` / `_r360_splice.py` / `_r360_resolved_after.json` / `_r360_resolved_off.json` / `_r360_probe.cjs` / `_r360_probe_run.sh` / `_r360_probe_{off,on}_0*.log` / `_r360_fullship_par.sh` / `_r360_fullship_run.sh` / `_r360_fullship_regen.log` / `_r360_changed_modules.txt` / `_r360_gates.log` / `_r360_sk_full.log` / `_r360_sk_final.json` / `_r360_postship.sh` / `_r360_selftests.log` / `_r360_fastloop_snapshot.log` / `_r360_manifest_snapshot.log` / `_r360_ledger.log` / `_r360_index.log` / `_r360_finalise.py` | `CONVERTER_V2/outputs/` | Session 19 Round 4 (engine r360 — the diff miner's footer facts: the footer link set follows the KB's sub-type forms — eleven registry corrections, no engine change) — the footer probe (the r357 instrument on `footer_links` / `footer_class`, positions from each side's own page list), the anchored splice + the three-tier patch, the resolved-rules dumps before / after / toggle-OFF, the in-memory probe, the full regeneration, the gate suite, the fresh skeleton score, the post-ship housekeeping, the finalise |\n")
    s = s.replace(A, ROWS + A, 1)
    wr(P, s); print("README: r360 rows")
print("finalise done")
