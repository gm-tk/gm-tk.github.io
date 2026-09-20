#!/usr/bin/env python3
"""r410 finalise — LOOP_STATE.md: resolve the HANDOVER block (moved verbatim to the archive), update Position, append the Round-log line."""
import os
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = ROOT + "LOOP_STATE.md", ROOT + "LOOP_STATE_ARCHIVE.md"
lines = open(STATE, encoding="utf-8").read().split("\n")

def idx(prefix):
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            return i
    raise SystemExit("not found: " + prefix)

# 1. the HANDOVER block (heading + its one body line) -> archive verbatim; replaced by a one-line resolution
h = idx("## >>> HANDOVER 2026-09-20 ≈13:35 NZST")
assert lines[h + 1].startswith("**What is done and committed:**")
handover = lines[h:h + 2]
lines[h:h + 2] = [
    "## HANDOVER of 2026-09-20 ≈13:35 (session 28, round 410 in flight) — RESOLVED 2026-09-20 ≈15:05 NZST by session 29 Round 1: **r410 SHIPPED** (build 260619.81). The verbatim block is in LOOP_STATE_ARCHIVE.md 'HANDOVER 2026-09-20 session 28 — round 410 in flight (verbatim, archived at the session 29 r410 finalise)'. Task 4 (PMT101 opener; XOTP recognition round 1) is still NOT started — a queue item, not a block.",
]

# 2. Position: LAST SHIPPED / plateau / standing facts
p = idx("- LAST SHIPPED: **r408**")
lines[p] = ("- LAST SHIPPED: **r410** (build 260619.81, 20 Sept ≈15:05, session 29 Round 1 — THE WJFUN TILE-PAGE DIALECT, built in session 28 Task 3 and finished by the loop: "
            "`body_region.fundamentals_panels.tile_pages`, env `TILEPAGE_OFF`; the probe OFF = disk 2555 / 2555, ON exactly the 21 WJFUN overviews (21 up / 0 down, +257.1pp-sum); "
            "SCOPED regeneration of the 23 WJFUN + JPFUN modules — scoped ship #2 since the 19 Sept FULL (6 of headroom); **skeleton 53.680 → 53.789 % (+0.1095pp), ≥50 1398 → 1406, ≥75 236, ≥90 20, RAW 37.884 → 37.925 % @ 2349 pairs**; "
            "compare_structure exact 14091 → 14175 / EXTRA 186 / MISSING 690 / row-wrap 23; body 54 / 6 / 190 / 248 EXACT; clean 2504 / 2548, leak 73 / 44 EXACT; every verifier EXACT; 16 selftests GREEN; the WJFUN family 37.6 → 49.9 %; "
            "the miner re-mined on the r410 corpus: 183 → 184 CANDIDATE rows — the three `phases-nav` rows and two body `h2` rows GONE, six surfaced beneath (`DIFF_QUEUE.md` 20 Sept 14:59)); before it **r408** (build 260619.79, 20 Sept ≈11:30, session 28 pre-loop Task 1 — the mined registries rebuilt over the 552-module corpus: "
            "module_meta 454 → 552, 24 new Style-Anchor bases (WJFUN + JPFUN single-file), `Subject_Prefix_Map.json` PROPOSED, FRFUN held back; scoped regen of 103; skeleton 53.134 → 53.680 %; WJFUN 10.4 → 37.6 %) and **r407** (build 260619.78, 19 Sept, session 27 Round 12 — the last pre-intake engine round; the r398–r407 one-liners are in the Round log). "
            "**Corpus = r410** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r410; `outputs/_s29_r410_sk_final.json` the skeleton state).")
q = idx("- Plateau window (§4): **0 of 3** — r406")
lines[q] = "- Plateau window (§4): **0 of 3** — RESET by r410 (+0.1095pp, ≥50 +8). Read every delta on the post-intake 2,349-pair population (§1e); pre-19-Sept deltas are not comparable."
r = idx("- Standing facts: AppVersion 260619.79")
lines[r] = lines[r].replace("- Standing facts: AppVersion 260619.79 (r408, session 28 pre-loop Task 1, 20 Sept); before it 260619.78 (session 27 STOPPED 19 Sept ≈16:40 on the budget);",
                            "- Standing facts: AppVersion 260619.81 (r410, session 29 Round 1, 20 Sept); before it 260619.80 (r409) / 260619.79 (r408, session 28 pre-loop) / 260619.78 (session 27 STOPPED 19 Sept ≈16:40 on the budget);")
assert "260619.81" in lines[r]

# 3. the Round-log line, after the s28-t1 line (and any s28 lines after it)
t = idx("- s28-t1 (data r408")
j = t
while j + 1 < len(lines) and lines[j + 1].startswith("- s28-"):
    j += 1
lines.insert(j + 1, "- s29-r1 (engine r410, build 260619.81, 20 Sept ≈14:40 → 15:05) · THE WJFUN TILE-PAGE DIALECT (built + proven in session 28 Task 3, finished by the loop: `tile_pages`, env `TILEPAGE_OFF`; ContentConverter.#tilePagesPrepass → the r265 level-pages machinery, #tilePageMarker, MenuBuilder.#levelTabs, panelTitleLevelPostpass level_dialect_code_prefixes) · SHIPPED · probe OFF = disk 2555 / 2555, ON exactly the 21 WJFUN overviews (21 up / 0 down, +257.1) · SCOPED regen of the 23 WJFUN + JPFUN (scoped #2 since the 19 Sept FULL; 0 stale; probe == disk 21 / 21; spot-check 12 / 12 identical) · skeleton 53.680 → 53.789 (+0.1095pp), ≥50 1398 → 1406, ≥75 236 / ≥90 20 EXACT; cs exact +84; all else EXACT · WJFUN 37.6 → 49.9 % · miner 183 → 184 (phases-nav rows gone) · plateau RESET 0 of 3")

open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with open(ARCH, "a", encoding="utf-8") as f:
    f.write("\n## HANDOVER 2026-09-20 session 28 — round 410 in flight (verbatim, archived at the session 29 r410 finalise)\n\n" + "\n".join(handover) + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
