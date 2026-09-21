#!/usr/bin/env python3
"""r421 finalise — LOOP_STATE.md: the Round 3 PICK-pass section and the Round 4 PICK section move to the archive (+ the what-shipped
record), the Position updates, the Round-log line is appended. Run under WSL."""
import os, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
# Round 3 PICK pass → archive
a3 = idx("## Session 30 — Round 3 PICK pass"); a4 = idx("## Session 30 — Round 4 PICK (engine r421)"); b = idx("## Round log")
pick3 = lines[a3:a4]; pick4 = lines[a4:b]
shipped = ("- **What shipped (r421, build 260619.92, 21 Sept ≈19:55):** `Input_Doc_Rules.module_code_detection.registry_token {enabled, env CODEREG_OFF, "
           "separators, min_length}` + `ModuleResolver.DetectModuleCode` step 1b — when the filename regex names nothing, each filename's leading token that is a "
           "key of `ModuleStructureIndex.module_meta` is a candidate ahead of the front-matter regex. Probe OFF (`CODEREG_OFF`) = disk 2555 / 2555; ON exactly the 4 "
           "modules (CHWHA / GEWHA / ANZHFUN05 / PWYWHA1), each output renamed to its code, nothing else changed. Scored against the gold before regenerating: CHWHA "
           "41.0 → 43.9 (its registry row + the r419 CJK wrap now firing), GEWHA 25.9 → 25.8, ANZHFUN05 11.0 → 9.1 (its row gives `body.fundamentals`, no menu and "
           "the fundamentals footer — the gold's own — but the Novice / Emergent two-tile page is unbuilt, difflib re-aligns lower), PWYWHA1 15.2 → 13.8 — net "
           "−0.6pp-sum, NAMED and accepted (`_fastloop_diff.py --commit --accept-named`, `_s30_r421_fastloop_named.log`). SCOPED regeneration of the 4 + 12 "
           "spot-checks (0 stale; 12 / 12; containment 4 ⊆ 4; the ledger scoped #5 since the r416 FULL — 3 of headroom). `run_all_gates.sh`: skeleton 54.2067 → "
           "54.2065 % (−0.0002pp; 0 movers on the unchanged pages, 4 renamed), ≥50 1441 / ≥75 238 / ≥90 20 / RAW 38.229 EXACT; cs 14170 / 186 / 683 / 23, body 54 / 5 "
           "/ 190 / 247, clean 2504 / 2548, leak 73 / 44, tags 9557 — all EXACT; every verifier ✓; 17 selftests GREEN; feature index GREEN; miner 182 → 182; "
           "checksums refreshed. Follow-ups recorded from F23: the FRFUN multi-file Novice / Emergent renderer (28 pages / 3 modules — a build), the JPFUN "
           "`[Novice Content starts here]` marker alias for the r265 level pages (2 modules), the MXFUN dual-build pairing (needs-Chris).")
lines[a3:b] = [
    "## Session 30 — Round 3 PICK pass (no engine change; 21 Sept ≈17:40 → 19:05) — nine instruments on the r420 corpus, nothing at the floor → LOOP_STATE_ARCHIVE.md 'Session 30 — Round 3 PICK pass (archived at the r421 finalise)'; the one-line summary is the s30-r3 Round-log line below.",
    "",
    "## Session 30 — Round 4 (engine r421) — THE REGISTRY-KNOWN MODULE CODE (CHWHA / GEWHA / ANZHFUN05 / PWYWHA1 resolve through the structure index) — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 30 — Round 4 PICK (engine r421) + what shipped'; the one-line summary is the s30-r4 Round-log line below.",
    ""]
p = idx("- LAST SHIPPED: **r420**")
old = lines[p]
head = "- LAST SHIPPED: **r420** (build 260619.91, 21 Sept ≈17:45, session 30 Round 2 — "
assert old.startswith(head)
rest = old[len(head):]
r420_short = ("**r420** (build 260619.91, 21 Sept ≈17:45, session 30 Round 2 — the letter-grid bingo: the BLL `[Self check]` letter table builds the KB 03E bingo, "
              "D10-3's selfCheck kickoff shape 1, `BINGO_OFF`, the NEW gate `_verify_bingo.cjs` 52 grids / defect 0, −0.0005pp named)")
tail_ix = rest.find("; before it **r419**")
assert tail_ix > 0
tail = rest[tail_ix + len("; before it "):]
lines[p] = ("- LAST SHIPPED: **r421** (build 260619.92, 21 Sept ≈19:55, session 30 Round 4 — THE REGISTRY-KNOWN MODULE CODE: a filename's leading token that "
            "`Module_Structure_Index.module_meta` knows is the module code (CHWHA / GEWHA / ANZHFUN05 / PWYWHA1 fell outside the detection regex and shipped as "
            "`MODULE_0_0.html` / `PWY1000_0_0.html`, never reaching their r408 registry rows; `module_code_detection.registry_token`, env `CODEREG_OFF`); probe OFF = "
            "disk 2555 / 2555, ON exactly the 4 (each output renamed); SCOPED regeneration of the 4 (scoped ship #5 since the r416 FULL); **skeleton 54.2067 → "
            "54.2065 % (−0.0002pp — the four re-paired pages, NAMED), ≥50 1441, ≥75 238, ≥90 20, RAW 38.229 % @ 2349 pairs**; cs 14170 / 186 / 683 / 23, body 54 / 5 "
            "/ 190 / 247, clean 2504 / 2548, leak 73 / 44 — all EXACT; every verifier EXACT; 17 selftests GREEN; the miner 182 → 182); before it " + r420_short + ", " + tail)
lines[p] = lines[p].replace("**Corpus = r420** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r420; `outputs/_s30_r420_sk_final.json` the skeleton state; ceiling 90.9 % → 54.207 = **59.6 % of achievable**)",
                            "**Corpus = r421** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r421; `outputs/_s30_r421_sk_final.json` the skeleton state; ceiling 90.9 % → 54.207 = **59.6 % of achievable**)")
assert "Corpus = r421" in lines[p]
q = idx("- Plateau window (§4): **0 of 3**")
lines[q] = "- Plateau window (§4): **0 of 3** — r421 a recognition round (4 pages re-paired; −0.0002pp named), r420 a build round (selfCheck still-a-box 215 → 163), r419 +0.0212pp (≥50 +2). Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.91")
lines[r] = lines[r].replace("AppVersion 260619.91 (r420, session 30 Round 2, 21 Sept); before it 260619.90 (r419)", "AppVersion 260619.92 (r421, session 30 Round 4, 21 Sept); before it 260619.91 (r420) / 260619.90 (r419)")
assert "260619.92" in lines[r]
t = idx("- s30-r3 (no engine change")
lines.insert(t, "- s30-r4 (engine r421, build 260619.92, 21 Sept ≈19:20 → 19:55) · THE REGISTRY-KNOWN MODULE CODE — `DetectModuleCode`'s one regex (2–6 letters + 2–4 digits) could not name CHWHA / GEWHA (no digits), ANZHFUN05 (seven letters) or PWYWHA1 (one digit; converted AS the front-matter's PWY1000): shipped as `MODULE_0_0.html` / `PWY1000_0_0.html`, their r408 registry rows never reached (found through the miner's F23 `nav:phases` decomposition + the r420 CHWHA note); a filename's leading token that `module_meta` knows is now a candidate between the filename regex and the front-matter regex (`Input_Doc_Rules.module_code_detection.registry_token`, env `CODEREG_OFF`) · SHIPPED · probe OFF = disk 2555 / 2555, ON exactly the 4 (each output renamed; CHWHA 41.0 → 43.9, GEWHA −0.1, ANZHFUN05 −1.9 / PWYWHA1 −1.5 on their now-correct registry chrome — the Novice / Emergent page unbuilt; NAMED) · SCOPED regen of the 4 + 12 spot-checks (0 stale; 12 / 12; containment 4 ⊆ 4; scoped #5 since the r416 FULL) · skeleton 54.2067 → 54.2065 (−0.0002pp named), buckets / RAW EXACT; all else EXACT; every verifier ✓; 17 selftests GREEN; miner 182 → 182 · F23 decomposed: FRFUN multi-file renderer (28 pages / 3 modules, a build), JPFUN `[Novice Content starts here]` alias (2 modules), MXFUN dual-build pairing (needs-Chris) · plateau 0 of 3 · build 260619.92")
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with io.open(ARCH, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n## Session 30 — Round 3 PICK pass (archived at the r421 finalise) — nine instruments on the r420 corpus, nothing at the floor (21 Sept ≈17:40 → 19:05 NZST)\n\n" + "\n".join(pick3).rstrip("\n") + "\n")
    f.write("\n## Session 30 — Round 4 PICK (engine r421) + what shipped — THE REGISTRY-KNOWN MODULE CODE (21 Sept ≈19:20 → 19:55 NZST)\n\n" + "\n".join(pick4).rstrip("\n") + "\n" + shipped + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
