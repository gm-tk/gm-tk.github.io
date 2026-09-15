#!/usr/bin/env python3
"""ROUND 332 — finalise: changelog, AppVersion (260619.02 → 260619.03), CLAUDE.md §9/§11/§14, gate_baseline.json,
LOOP_STATE.md (what shipped + position + round log), KB status D-row. Idempotent."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
SK_B, SK_A, RAW_B, RAW_A = "50.558", "50.827", "34.881", "35.066"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 332, build 260619.03) — THE EMPTY FOOTER: A NO-EVIDENCE REGISTRY VALUE FALLS BACK TO THE KB'S PAGE-POSITION FORM, and the BLL1 footer class (KB 01B "Footer and Acknowledgements" + 06 §3; the autonomous loop, session 5, Round 3; **SCOPED regeneration of the 130 affected modules; skeleton +0.269pp / ≥50% +10 / ≥75% +4, every other gate EXACT; scoped ship #6 since the round-326 full**)

### 1. WHAT CHANGED, IN ONE LINE

**141 Claude pages shipped a `<div id="footer">` with NO links at all — the Style-Anchor registry carries the miner's no-evidence marker (an em dash) as the `footer_links.final` value on ~60 groups (and `lesson` on OSSC), and `SkeletonBuilder.#buildFooter` treated any present value as a pattern. A registry footer value with no `value_map` entry now falls back to the KB's form for the page position — overview `next + home`, middle `prev + next + home`, final `prev + home` (01B); `home` only under `fundamentals-nav` (06 §3.3); the CED inquiry shell's forced links outrank it. And the BLL1 series' stale registry delta `footer_class: footer-nav` is removed, so BLL1 inherits the subject rule `footer-nav inquiry-nav` that its gold ships on 128 of 150 pages. 239 pages / 130 modules changed.**

### 2. THE EVIDENCE (docx → human → Claude)

- **BLL112** — gold `-03` (the last page): `<ul class="footer-nav inquiry-nav">` with `prev-lesson + next-lesson + home-nav`; gold `-01`/`-02` the same class → Claude before: `_2_0` an empty `<div id="footer"></div>`, `_0_0`/`_1_0` plain `footer-nav`; after: `inquiry-nav` on all three, `prev + home` on the last.
- **OSSC401 lessons 1–3** — gold `prev + next + home` → Claude before: empty (registry `lesson: —`); after: `prev + next + home`.
- **HIS1001 lesson 10** — gold `prev + home` → Claude before: empty (registry `final: —`); after: `prev + home`.
- **The KB:** 01B — "Footer nav differs by page position: Overview `next-lesson + home-nav` only; Middle pages all three; Final page `prev-lesson + home-nav` only"; 06 §3.3 — `footer-nav fundamentals-nav` "typically home-nav only"; 06 §3.4 — the inquiry shell "with prev + next + home".

### 3. THE MEASUREMENT (all paired pages; the r331 skeleton-gap instrument surfaced the footer lines — `a.home-nav` missing on 280 gold pages, `ul.footer-nav.inquiry-nav` on 164)

- Footer composition gold == Claude on 904 Standard pages; the mismatches decompose into **(A) the empty footer — 141 Claude pages / ~125 modules** (BLL1 49, TRR1 10, AGH1 9, OSSC 9, HIS1 8, PNR 5, CEDT 5, MXFL 5, CEDR 3, SSOG 3 …; 120 the module's last page, the rest OSSC401/501's lessons), where the gold is never empty (`prev+next+home` 82 / `prev+home` 29 / no footer at all 12 / `next+home` 2); **(B) the BLL1 class — 98 Claude pages plain `footer-nav`**, the gold `footer-nav inquiry-nav` on 41 of 48 BLL1 modules (0.85; BLL121 / 172 / 174–177 plain, BLL171 mixed) — the same as BLL2 (123 : 25) and the subject rule; and editorial residue (link ORDER `home+prev+next`, `active` items, a doubled `prev`), not chased.
- Gold by footer class (every gold page): `footer-nav` all-three 1493 / `next+home` 164 / `prev+home` 134 / `home` 20; `inquiry-nav` 199 / 86 / 40 / 4; `fundamentals-nav` **home 63 : all-three 12 = 0.84**.
- The registry's no-evidence `final` marker sits on ~60 groups (BLL, ENGS, HPE, MX*, Science, SocSci, CED*, ECE, EXP*, XDLS/XMES, NCEA1, OS*, TMoA, TWHA …) — `outputs/_r332_probe_on.log` names every page the fallback reaches.

### 4. THE FIX — Part A, one data block `footer.kb_position_defaults` `{{ enabled, env: "FOOTERPOS_OFF", overview, lesson, final, by_footer_class }}`; Part B, a registry correction

- `SkeletonBuilder.#buildFooter`: when the registry's `footer_links` value has no `value_map` entry, the KB's value for the page position applies — the sub-type map first (`by_footer_class`, keyed on a token of the resolved footer class: `fundamentals-nav` → `home`), else `overview` / `lesson` / `final`; a caller-forced link set (`forceLinks`, the r102/r108 CED inquiry shell) outranks both; a registry value that IS in the map is never touched, so every module carrying real evidence is byte-identical. The warn note becomes an info note naming the fallback. **Env `FOOTERPOS_OFF`** reverts byte-for-byte (the empty footer returns).
- Part B — `Style_Anchor_Registry.json` `1-10 Blended Literacy / bases / BLL / levels / BLL1 / delta`: `footer_class` removed (a dated correction note left in its place); the level now inherits `footer-nav inquiry-nav`. No engine change; the reversal is git (the r263 / r285 registry-correction precedent).

### 5. THE PROOF AND THE GATES

- The in-memory probe over ALL 416 modules (`_r332_probe.cjs`, four shards): ON names **239 pages / 130 modules**, every differing line one of: 141 empty footers gaining `<ul>` + links (141 `home-nav`, 118 `prev-lesson`, 31 `next-lesson`; 171 `inquiry-nav` / 67 `footer-nav` / 1 `fundamentals-nav` uls) and 98 BLL1 `<ul class="footer-nav">` → `inquiry-nav` — nothing else; OFF (`FOOTERPOS_OFF=1`) leaves exactly Part B's 98 BLL1 lines. Scoped regeneration in the planner's 12 batches (`_r332_batches_run.sh`); `_content_manifest.py fresh --affected` → **0 truly stale**; `diff` = exactly the 239 pages, 0 added/removed; ON in memory = disk 2102/2102 afterwards.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.269pp) IMPROVED / ≥50% 1034 → 1044 / ≥75% 196 → 200 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%.** 207 pages moved — **185 up / 22 down**, pp-sum +526.22 (BLL1 128 pages +254.7; OSSC +55.3, TRR1 +39.2, AGH1 +30.4, CEDT +23.5, PNR +22.8, HIS1 +20.3 …; TRR107_3_0 +10.78, OSSC501_2_0 +10.27). The 22 dips NAMED: 16 on the BLL1 plain-footer minority (BLL121 / 172 / 174 / 175 / 176 / 177 / 145 — the series' 0.15, −0.6 to −1.8 each) = the series-consensus cost; SSOG101_7_0 −3.5 / MXFL401_7_0 −3.4 / XDLS502_4_0 / TRR102_5_0 / CEDK102_0_0 = final pages whose gold keeps `next` — the KB's `prev+home` override (LOOP §1b).
- Every other gate EXACT (`_fastloop_diff.py` PASS; full suite `_r332_gates.log` line-for-line identical to r331 outside the skeleton block): cs exact 11360 / EXTRA 186 / missing 591 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · mtkQuiz 17 shells defect 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN**.
- **Ceiling:** SCAFFOLD {SK_A}% = **55.5% of achievable** (55.49).

### 6. NAMED, NOT CHASED

- The registry's no-evidence marker on other fields (`module_code`, `h1_count`, `menu_type` — the r238 unknown-literal class) — the r263 "registry re-mine round" stays the durable fix; the CED Inquiry overview pages the shell does not force (12, now `next+home` where the gold ships all three); the gold's editorial link orders.

**Ledger:** scoped ship #6 since the r326 full · data `footer.kb_position_defaults` + the `Style_Anchor_Registry` BLL1 delta correction · env `FOOTERPOS_OFF` (Part A) · tools `outputs/_r332_probe.cjs`, `_r332_finalise.py` (the measurement is the inline footer census recorded in `LOOP_STATE.md`) · state `outputs/_r332_sk_final.json` (FRESH) · logs `_r332_gates.log`, `_r332_sk_full.log`, `_r332_fastloop.log`, `_r332_fastloop_commit.log`, `_r332_selftests.log`, `_r332_probe_on_0*.log`, `_r332_probe_on.log`, `_r332_probe_off.log`, `_r332_probe_on2_0*.log`, `_r332_regen.log`, `_r332_fresh.log`, `_r332_affected.txt`, `_r332_batches_run.sh`.

"""
if "round 332, build 260619.03" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.02";\n'
NEW = ('\t// ROUND 332 (2026-09-15, build 260619.03): the empty footer — a registry footer_links value with no\n'
       '\t// value_map entry (the style-anchor miner\'s no-evidence marker) falls back to the KB\'s page-position\n'
       '\t// form (01B: overview next+home / lesson prev+next+home / final prev+home; fundamentals-nav home) —\n'
       '\t// 141 pages had no links; and the stale BLL1 registry footer_class delta removed (inquiry-nav, gold\n'
       '\t// 0.85). 239 pages / 130 modules, scoped. Env FOOTERPOS_OFF; data footer.kb_position_defaults.\n'
       '\t// Skeleton +0.269pp, >=50% +10, >=75% +4.\n'
       '\tstatic AppVersion = "260619.03";\n')
if '"260619.03"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 331 BASELINE (a bilingual section box's headings render at the KB's activity level — KB 07B; scoped)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 332 BASELINE (the empty footer → the KB's page-position form + the BLL1 footer class; scoped 130 modules): SCAFFOLD mean {SK_A}% / >=50% 1044 / >=75% 200 / >=90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r332_sk_final.json`, FRESH). r332 +0.269 (207 moved, 185 up; the 22 dips NAMED = the BLL1 plain-footer minority modules (the series' 0.15) + final pages whose gold keeps `next` under the KB's `prev+home` override). Older r331 text: **ROUND 331 BASELINE (a bilingual section box's headings render at the KB's activity level — KB 07B; scoped)")
if "ROUND 332 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `FOOTERPOS_OFF` | 332 | **THE EMPTY FOOTER — a no-evidence registry value falls back to the KB's page-position form** (KB 01B \"Footer and Acknowledgements\" + 06 §3; the autonomous loop's session-5 Round 3; **SCOPED regeneration of the 130 affected modules; scoped ship #6 since the r326 full**). Reverts byte-for-byte (the 141 empty footers return). ON (default), `footer.kb_position_defaults`: in `SkeletonBuilder.#buildFooter` a registry `footer_links` value with no `value_map` entry (the Style-Anchor miner's em-dash no-evidence marker, ~60 groups' `final`, OSSC's `lesson`) takes the KB's value for the page position — `by_footer_class` first (`fundamentals-nav` → `home`; gold 0.84), else overview `next+home` / lesson `prev+next+home` / final `prev+home`; a caller-forced link set (the CED inquiry shell) outranks both; a registry value in the map is never touched. RIDES ALONG (data only, no toggle — the r263 / r285 registry-correction precedent): the BLL1 delta's stale `footer_class: footer-nav` removed → `footer-nav inquiry-nav` (gold 128/150 = 0.85, the same as BLL2 and the subject rule). MEASURED: 141 Claude empty footers where the gold is never empty (`prev+next+home` 82 / `prev+home` 29 / none 12 / `next+home` 2); 98 BLL1 plain-footer pages. 239 pages / 130 modules changed. Skeleton +0.269pp (≥50% +10, ≥75% +4; 185 up / 22 down, dips named); every other gate EXACT; 13 selftests GREEN. |\n")
if "| `FOOTERPOS_OFF` | 332 |" not in m:
    A = "| `REOBOXH_OFF` | 331 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.03` (round 332 — **the empty footer → the KB's page-position form + the BLL1 footer class** (KB 01B / 06 §3; the autonomous loop's session-5 Round 3; **SCOPED regeneration of 130 modules; scoped ship #6 since the r326 full**). **ROUND 332 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% 1044 / ≥75% 200 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r332_sk_final.json`, FRESH) = **55.5% of achievable** (ceiling 91.6%). Every other gate EXACT: cs exact **11360** / EXTRA **186** / missing **591** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **239 pages / 130 modules changed, 0 added/removed**; toggle `FOOTERPOS_OFF`; data `footer.kb_position_defaults` + the `Style_Anchor_Registry` BLL1 delta. Empty footers 141 → 0. **Plateau window: r330 +0.040 · r331 +0.022 · r332 +0.269.**)\n")
if "- **Build:** `260619.03` (round 332" not in m:
    A = "- **Build:** `260619.02` (round 331 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.03"; d["_meta"]["round"] = 332; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": 1044, "pages_ge_75": 200})
d["_meta"]["_round332_note"] = f"Round 332 (the empty footer → the KB's page-position form + the BLL1 footer class; scoped 130-module regeneration, scoped ship #6 since the r326 full). Skeleton {SK_B}->{SK_A} (+0.269pp; 207 moved, 185 up; >=50 1034->1044, >=75 196->200; dips named = the BLL1 plain-footer minority + final pages under the KB's prev+home override); every other gate EXACT."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
anchor = "| — | c92 language fonts (7 pages)"
row = ("| ~~—~~ | 01B \"Footer and Acknowledgements\" — the footer nav by page position (overview `next+home`, middle all three, final `prev+home`; 06 §3.3 `fundamentals-nav` home only) | **SHIPPED round 332** (141 empty Claude footers → the KB form; + the BLL1 registry `footer_class` correction, 98 pages; 239 pages / 130 modules, scoped) | skeleton-visible (the footer's `ul > li > a` lines; +0.269pp, ≥50 +10, ≥75 +4) | — | the registry's no-evidence marker (an em dash) had been read as a pattern; a registry value that IS a pattern is untouched; where the gold's final page keeps `next` the KB form is a NAMED override |\n")
if "01B \"Footer and Acknowledgements\"" not in k:
    assert k.count(anchor) == 1; k = k.replace(anchor, row + anchor, 1); wr(KB, k); print("KB status D-row")

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 5 · Round 3 (engine r332) — what shipped (the empty footer → the KB's page-position form; the BLL1 footer class)
- **Fix:** Part A — `footer.kb_position_defaults` {{enabled, env FOOTERPOS_OFF, overview next+home, lesson prev+next+home, final prev+home,
  by_footer_class {{fundamentals-nav: home}}}} in `SkeletonBuilder.#buildFooter`: a registry `footer_links` value with no `value_map` entry (the
  miner's em-dash no-evidence marker) takes the KB's page-position form; forceLinks (the CED inquiry shell) outranks it; a mapped registry
  value is untouched. Part B — the BLL1 registry delta's stale `footer_class: footer-nav` removed (→ `footer-nav inquiry-nav`, gold 0.85).
- **Regeneration:** scoped — the in-memory probe over ALL 416 modules (4 shards) named 239 pages / 130 modules; every diff line = 141 empty
  footers gaining links (141 home, 118 prev, 31 next) + 98 BLL1 class swaps, nothing else; OFF = exactly the 98 BLL1 lines; the planner's 12
  batches, all rc 0; 0 truly stale; manifest diff = exactly the 239; ON = disk 2102/2102.
- **Gates:** skeleton {SK_B} → {SK_A} (+0.269pp; 207 moved, 185 up / 22 down — dips NAMED: 16 on the BLL1 plain-footer minority modules
  BLL121/172/174–177/145 (the series' 0.15), SSOG101_7_0 −3.5 / MXFL401_7_0 −3.4 / XDLS502_4_0 / TRR102_5_0 / CEDK102_0_0 = final pages whose gold
  keeps `next` under the KB's `prev+home`); ≥50 1034 → 1044; ≥75 196 → 200; every other gate line-for-line EXACT with r331; 13 selftests GREEN.
  **55.5% of achievable.**
- **Verifier:** Claude empty footers 141 → 0; BLL1 plain-footer pages 98 → 0. **Plateau window: r330 +0.040 · r331 +0.022 · r332 +0.269.**

""")
ANCHOR = "## Session 5 · Round 3 PICK (engine r332)"
if "## Session 5 · Round 3 (engine r332) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Session 5 Round 2 (engine r331 — a bilingual section box's headings render at the KB's activity level h3, KB 07B): SHIPPED 2026-09-15 ≈17:10 (session 5). AppVersion 260619.02, CLAUDE.md §9/§11/§14, scoped ship #5 since the r326 full. Skeleton +0.022pp."
NEW_P = OLD_P + nl + "- Session 5 Round 3 (engine r332 — the empty footer → the KB's page-position form, KB 01B; + the BLL1 registry footer class): SHIPPED 2026-09-15 ≈17:40 (session 5). AppVersion 260619.03, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #6 since the r326 full. Skeleton +0.269pp, ≥50 +10, ≥75 +4."
if "- Session 5 Round 3 (engine r332" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s5-r2 (engine r331) · a bilingual section box's headings render"
i = s.find(OLD_R); assert i > 0; j = s.find(nl, i) + len(nl)
NEW_R = f"- s5-r3 (engine r332) · the empty footer → the KB's page-position form (KB 01B: a no-evidence registry footer value falls back to overview next+home / lesson all three / final prev+home; fundamentals-nav home) + the BLL1 registry footer class (inquiry-nav, gold 0.85) · SHIPPED 2026-09-15 · scoped regeneration, 239 pages / 130 modules · scaffold {SK_B}→{SK_A} (+0.269; 185 up / 22 down, dips named), ≥50 +10, ≥75 +4, every other gate EXACT · empty footers 141→0 · 55.5% of achievable · commit (see git log)" + nl
if "- s5-r3 (engine r332)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
old_h = "· r331 (Bilingual in-box heading level, scoped, +0.022pp) · SHIPPED ≈17:10.**"
new_h = "· r331 (Bilingual in-box heading level, scoped, +0.022pp; commit 612da6d) · r332 (the empty footers, scoped 130 modules, +0.269pp) · SHIPPED ≈17:40.**"
if old_h in s: s = s.replace(old_h, new_h, 1); print("header")
wr(LS, s); print("LOOP_STATE.md written")
