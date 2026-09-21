#!/usr/bin/env python3
"""r421 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-21 (round 421, build 260619.92) — THE REGISTRY-KNOWN MODULE CODE: a filename's leading token that the structure index knows is the module code (the WHA / ANZHFUN recognition gap; the autonomous loop's session 30 Round 4; SCOPED regeneration of the 4 modules, the probe proving the other 490 byte-identical)

### 1. WHAT CHANGED

**The defect.** `ModuleResolver.DetectModuleCode` reads the module code with ONE regex — `\\b([A-Z]{2,6}\\d{2,4}(?:RR)?)\\b` — over the upload filenames and then the first 40 front-matter paragraphs. Four intake modules fall outside it: **CHWHA / GEWHA** (no digits), **ANZHFUN05** (seven letters), **PWYWHA1** (one digit — and its front matter mentions `PWY1000`, so it converted AS PWY1000). Their builds shipped as `MODULE_0_0.html` / `PWY1000_0_0.html` with no `run.moduleCode`, so the round-408 registry rows mined for exactly these codes (`Module_Structure_Index.module_meta` holds all four) were never reached — global defaults instead: ANZHFUN05 without its `body.fundamentals` / fundamentals footer nav (11.0 %), PWYWHA1 as PWY1000 (15.2 %), CHWHA's Chinese runs bare under r419 (its `han_needs_module_language` saw no code), and the acks / interactives-manifest / hand-off file names wrong on all four. Found through the DIFF MINER's chrome fact F23 (`nav:phases` MISSING, 11 modules — decomposed: FRFUN06–08 the multi-file Novice / Emergent renderer, 28 pages / 3 modules, the s28 follow-up; JPFUN01 / 02 the `[Novice Content starts here]` marker dialect the r265 level-page machinery does not read; MXFUN01–03 the dual-build gold pairing, needs-Chris; ANZHFUN05 this defect; ARFUN04 / SSFUN07 singletons) and the r420 CHWHA note.

**The fix (a recognition defect — the PMT101-style item; DATA OVER CODE).** `Input_Doc_Rules.module_code_detection.registry_token {enabled, env CODEREG_OFF, separators, min_length}`: between the filename regex and the front-matter regex, each filename's LEADING token (split on space / underscore / dot / dash, upper-cased) that is a key of `ModuleStructureIndex.module_meta` is a candidate ("filename — a registry-known code"), so a code the regex cannot shape still resolves when the corpus registry knows it. Only when the regex found nothing in the filenames — every module the regex already names keeps its path byte-for-byte; the front-matter regex stays the last resort (PWYWHA1's `PWY1000` mention now surfaces as the standing multiple-candidates warning and loses to the filename).

### 2. PROOF

- `_s30_r421_probe_run.sh` (the r410 harness over all 494 Claude-dir modules): **OFF (`CODEREG_OFF`) = the disk on every page, 2555 / 2555**; **ON = exactly the 4 modules** — each one output RENAMED (`MODULE_0_0.html` → `CHWHA_0_0.html` / `GEWHA_0_0.html` / `ANZHFUN05_0_0.html`, `PWY1000_0_0.html` → `PWYWHA1_0_0.html`), nothing else changed anywhere.
- The four pages against their gold on the gate's own `match()` before regenerating: CHWHA 41.0 → 43.9 (+2.9 — its registry row + the r419 CJK wrap now firing), GEWHA 25.9 → 25.8, ANZHFUN05 11.0 → 9.1, PWYWHA1 15.2 → 13.8 — net −0.6pp-sum. ANZHFUN05 decomposed: the registry row gives it `body.container-fluid.fundamentals`, no module menu and the `ul.footer-nav.fundamentals-nav` footer — all three the gold's own — but the gold's page is the two-tile Novice / Emergent split (`div.phases` + `div.introduction` + `phaseContainer` + `fundamentalsPanel`) that the r265 level-page machinery cannot read from this WT's markers, and difflib re-aligns the rest lower; PWYWHA1's row drops the module menu the gold also lacks and relevels two h4 → h3. A recognition fix is right by construction (§1b level 2 / 3 — the module's own registry row over global defaults); the movement is NAMED and accepted through the r289 override (`_fastloop_diff.py --commit --accept-named "skeleton SCAFFOLD mean"`, `_s30_r421_fastloop_named.log`).
- SCOPED regeneration (`_s30_r421_regen.sh`: the 4 + a fresh 12-module spot-check sample): `_content_manifest.py fresh` **0 truly stale**; `_scoped_spotcheck.py verify` **12 / 12 byte-identical**; `scoped_ship.sh` containment **4 ⊆ 4**; the ledger at scoped #5 since the r416 FULL.
- `run_all_gates.sh` (`_s30_r421_gates.log`): skeleton state `_s30_r421_sk_final.json` **54.2067 → 54.2065 % (−0.0002pp)**, RAW 38.229 EXACT, ≥50 1441 / ≥75 238 / ≥90 20 EXACT; 0 movers on the unchanged pages, 4 pages renamed (4 new-only / 4 gone); compare_structure 14170 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44, tags 9557 — all EXACT; every verifier ✓ (bingo 52 grids / defect 0); 17 selftests GREEN (49 / 0); feature index GREEN; DIFF MINER 182 → 182 CANDIDATE rows.

### 3. PROTECTED GATES (all HELD — `_s30_r421_gates.log`, `_s30_r421_scoped_ship.log`, `_s30_r421_fastloop_named.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.2067 → 54.2065 % (−0.0002pp — NAMED: the four re-paired pages, the registry row's chrome right, the level-page dialect unbuilt)**; ≥50 **1441**, ≥75 **238**, ≥90 **20**, RAW **38.229 %** EXACT; 2349 pairs, skipped 0.
- **compare_structure** 14170 / 186 / 683 / 23 EXACT; **body_compare** 54 / 5 / 190 / 247 EXACT; **defect** clean 2504 / 2548, leak 73 / 44 EXACT; tags 9557 / 9557; every verifier EXACT.
- Plateau (§4): a recognition round (the pairing set itself changed on 4 pages); the window stays at 0 of 3 with r420 / r419 behind it.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-21 (round 420")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.91";'; assert s.count(old) == 1
note = ("\t// ROUND 421 (260619.92): THE REGISTRY-KNOWN MODULE CODE — ModuleResolver.DetectModuleCode's one regex (2-6 letters + 2-4 digits) could not name "
        "CHWHA / GEWHA (no digits), ANZHFUN05 (seven letters) or PWYWHA1 (one digit; converted AS the front-matter's PWY1000), so those four shipped as "
        "MODULE_0_0.html / PWY1000_0_0.html and never reached their r408 registry rows. A filename's leading token that Module_Structure_Index.module_meta "
        "knows is now a candidate between the filename regex and the front-matter regex (Input_Doc_Rules.module_code_detection.registry_token, env "
        "CODEREG_OFF). The loop's session 30 Round 4: OFF = disk 2555 / 2555, ON exactly the 4 (each output renamed); SCOPED regeneration of the 4 (scoped "
        "#5 since the r416 FULL); skeleton 54.2067 -> 54.2065 % (-0.0002pp named — CHWHA +2.9, ANZHFUN05 -1.9 on its now-correct fundamentals chrome), "
        "every other gate EXACT.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.92";'))

p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 420 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 421 BASELINE (the registry-known module code — CHWHA / GEWHA / ANZHFUN05 / PWYWHA1 "
        "resolve through the structure index, `module_code_detection.registry_token`, env `CODEREG_OFF`; 4 modules / 4 pages renamed; SCOPED regeneration of "
        "the 4, the probe proving the other 490 byte-identical; scoped ship #5 since the r416 FULL): SCAFFOLD mean 54.2065% / >=50% 1441 / >=75% 238 / >=90% "
        "20 / RAW 38.229% @ 2349 pairs, pairs skipped 0 — the mean −0.0002pp is the four re-paired pages (CHWHA +2.9, GEWHA −0.1, ANZHFUN05 −1.9, PWYWHA1 −1.5 "
        "— the registry chrome right, the Novice / Emergent level-page dialect unbuilt), NAMED and accepted; every bucket and every other gate EXACT.** "
        "Previous — ROUND 420 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `BINGO_OFF` | 420 | **THE LETTER-GRID BINGO"; assert s.count(old11) == 1
row11 = ("| `CODEREG_OFF` | 421 | **THE REGISTRY-KNOWN MODULE CODE — a filename's leading token that the structure index knows is the module code** (the "
         "autonomous loop's session 30 Round 4; a recognition defect, the PMT101-style item). `ModuleResolver.DetectModuleCode` reads the code with one regex "
         "(`[A-Z]{2,6}\\d{2,4}(RR)?`) over the filenames, then the front matter; CHWHA / GEWHA (no digits), ANZHFUN05 (seven letters) and PWYWHA1 (one digit — "
         "converted AS the front-matter's `PWY1000`) fell outside it, shipped as `MODULE_0_0.html` / `PWY1000_0_0.html`, and never reached their r408 registry "
         "rows (global defaults; CHWHA's Chinese bare under r419). `Input_Doc_Rules.module_code_detection.registry_token {enabled, env, separators, "
         "min_length}`: when the filename regex finds nothing, each filename's LEADING token (split on space / underscore / dot / dash, upper-cased) that is a "
         "key of `ModuleStructureIndex.module_meta` is a candidate, ahead of the front-matter regex; every module the regex already names keeps its path. "
         "OFF = the r420 output (2555 / 2555). ON = exactly the 4 modules, each output renamed to its code (CHWHA 41.0 → 43.9, the others' registry chrome "
         "right with difflib dips named). Follow-ups recorded from F23: the FRFUN multi-file Novice / Emergent renderer (28 pages / 3 modules), the JPFUN "
         "`[Novice Content starts here]` marker alias for the r265 level pages (2 modules), the MXFUN dual-build pairing (needs-Chris). |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.91` (round 420 — **the letter-grid bingo"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.92` (round 421 — **the registry-known module code: a filename's leading token that the structure index knows is the module "
       "code** — CHWHA / GEWHA / ANZHFUN05 / PWYWHA1 fell outside the detection regex, shipped as `MODULE_0_0.html` / `PWY1000_0_0.html` and never reached "
       "their r408 registry rows (`Input_Doc_Rules.module_code_detection.registry_token`, env `CODEREG_OFF`; `ModuleResolver.DetectModuleCode` step 1b); the "
       "autonomous loop's session 30 Round 4; the probe OFF = disk 2555 / 2555, ON exactly the 4 (each output renamed); **SCOPED regeneration of the 4 "
       "(scoped ship #5 since the r416 FULL)**; **ROUND 421 BASELINE: SCAFFOLD mean 54.2065% / >=50% 1441 / >=75% 238 / >=90% 20 / RAW 38.229% @ 2349 pairs** "
       "(−0.0002pp named — CHWHA +2.9, ANZHFUN05 −1.9 on its now-correct fundamentals chrome); every other gate EXACT; every verifier EXACT; 17 selftests GREEN; "
       "the miner 182 → 182). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.91"', '"260619.92"'); setv("round", 420, 421)
a = '    "_note_r420": "Round 420 (session 30 Round 2)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r421": "Round 421 (session 30 Round 4): the registry-known module code — CHWHA / GEWHA / ANZHFUN05 / PWYWHA1 resolve through Module_Structure_Index.module_meta (Input_Doc_Rules.module_code_detection.registry_token, env CODEREG_OFF); their outputs renamed, their r408 registry rows reached. SCOPED regeneration of the 4 (scoped #5 since the r416 FULL); the probe proving the other 490 byte-identical. The scaffold mean 54.2067 -> 54.2065 (-0.0002pp) is the four re-paired pages, NAMED and accepted through _fastloop_diff.py --accept-named.",\n' + a)
a2 = '    "_note_r419b": "Round 420: SCAFFOLD 54.2072'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r420b": "Round 421: SCAFFOLD 54.2067 -> 54.2065 (-0.0002pp NAMED — 4 pages re-paired under their real codes: CHWHA 41.0 -> 43.9, GEWHA 25.9 -> 25.8, ANZHFUN05 11.0 -> 9.1, PWYWHA1 15.2 -> 13.8; 0 movers elsewhere), 1441 / 238 / 20, RAW 38.229 EXACT; 2349 pairs.",\n' + a2)
b2 = '    "_note_r420": "Round 420: 14170 / 186 / 683 / 23 EXACT.",'; assert s.count(b2) == 1
s = s.replace(b2, '    "_note_r421": "Round 421: 14170 / 186 / 683 / 23 EXACT.",\n' + b2)
b3 = '    "_note_r420": "Round 420: over-capture 54 / runaway 5 / EMPTY 190 / ANY 247 EXACT.",'; assert s.count(b3) == 1
s = s.replace(b3, '    "_note_r421": "Round 421: over-capture 54 / runaway 5 / EMPTY 190 / ANY 247 EXACT.",\n' + b3)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r421 finalise: changelog + Config.js 260619.92 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
