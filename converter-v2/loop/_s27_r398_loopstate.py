#!/usr/bin/env python3
"""Session 27 Round 1 (r398) — LOOP_STATE.md: archive the Round 1 PICK (+ what shipped), the Round-log line, the Position block.
LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r1 (engine r398)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 27 — Round 1 PICK (engine r398)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r398, build 260619.69, 19 Sept ≈09:55 NZST):** data `video.icon_rule` — 18 series added to `icon_series` (n ≥ 2 / share ≥ 0.85, "
           "each ≥ 8 gold videos, 14 at 1.00), the NEW `plain_series` carve-out (31 series at n ≥ 2 / share ≤ 0.40, consulted before the subject|template fallback), "
           "NEW `widget_embedded {enabled, env_off VIDEOICONWIDGET_OFF}`; engine `MediaBuilder.#videoIconGroup` (the one group decision) + `videoIconPostpass` "
           "(the last step of ContentConverter's final-body chain — every `videoSection` in an icon-group module gains the token, idempotent); Config 260619.69. "
           "`NCEA1|Standard` (0.81, n = 41) was ADDED, scored with the gate's own match() on the probe's ON pages and REMOVED — its only reachable series AGH10 "
           "(0.76, a per-module coin-flip) scored −23.2 pp-sum because its icon modules' videos are un-built widgets while its plain modules' are free-body. "
           "Probe OFF (the committed registry via `--pre` + VIDEOICONWIDGET_OFF) 2109 / 2109; ON 198 pages / 74 modules, every diff the `icon` token alone "
           "(704 tokens); scored before the regen: 84 up / 4 down / 107 gate-invisible (widget slides), pp-sum +124.4. SCOPED regeneration of the 74 (7 batches "
           "rc 0; `fresh --affected` 0 truly stale; probe ON == disk 378 / 378). Skeleton 53.695 → 53.759 (+0.064pp), ≥50 1163 → 1166 (MXDI102_0_0 the named "
           "down-crosser), ≥75 195 / ≥90 18 EXACT, RAW 37.782 → 37.846, 1956 pairs / 0 skipped / 88 movers 84 up / 4 down / 0 outside (ENGC301_2_0 +6.5, "
           "MXDB302_7_0 +4.9; MXDI102 ×4 the MXDI10 series' plain minority −5.6 … −1.1); compare_structure 11723 / 172 / 626, body_compare 42 / 4 / 173 / 218, "
           "clean 2079 / 2102, leak 26 / 23 — all EXACT; every verifier RESULT identical to r397; 15 selftests + the index selftest GREEN; fast-loop / manifest / "
           "feature index refreshed; ledger scoped #2 since the r396 full; the miner re-mined 172 CANDIDATE rows (#630 the iframe class under the new parent label "
           "= the standing KB-correct decline; #411 a same-label `li` substitution on untouched pages = a miner text artefact; three rows gone by alignment); "
           "checksums refreshed; finalise = changelog entry `_s27_r398_entry.md`, AppVersion 260619.69, CLAUDE.md §9 / §11 / §14, gate_baseline.json, "
           "loop/README.md. Plateau window RESET (r398 +0.064pp, ≥50 +3).\n")
a = rd(AR)
if "## Session 27 — Round 1 PICK (engine r398) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 27 — Round 1 PICK (engine r398) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈09:55 NZST, session 27)\n" + pick + shipped
    wr(AR, a)
s = s[:i] + s[j + 1:]
old = s[s.index("## Sessions 23 / 24 / 26 — every shipped round (engine r370–r376, r377–r386, r387–r397)"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, old.replace("## Sessions 23 / 24 / 26 — every shipped round (engine r370–r376, r377–r386, r387–r397)", "## Sessions 23 / 24 / 26 / 27 — every shipped round (engine r370–r376, r377–r386, r387–r397, r398–)", 1), 1)
line = ("- s27-r1 (engine r398) · THE videoSection `icon` REGISTRY RE-MINED + THE WIDGET-EMBEDDED VIDEO FOLLOWS IT (18 series at n ≥ 2 / 0.85 + the `plain_series` "
        "carve-out; `MediaBuilder.videoIconPostpass` at the end of the final-body chain, env `VIDEOICONWIDGET_OFF`; the gold 0.95 on the registry modules' widget "
        "videos; found by the position-free label census `_s27_r1_labelcensus.py`; NCEA1|Standard added, scored on the gate, removed −23.2) · SHIPPED 19 Sept · "
        "ON 198 pp / 74 mods (84 up / 4 down, +124.4); SCOPED (#2 since r396) · skeleton 53.695→53.759 (+0.064), ≥50 +3; all else EXACT · plateau RESET · build 260619.69\n")
assert len(line) <= 700, len(line)
anchor = "- s26-r12 (no engine change)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- LAST SHIPPED: **r397**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r398** (build 260619.69, 19 Sept ≈09:55, session 27 Round 1 — the videoSection `icon` registry re-mined + the widget-embedded video "
       "follows it; r397 a table header cell is plain; r396 the captioned carousel video slide is `item video` (the FULL backstop); r395 the flip-card column "
       "width; r394 the clickDrop buttons in the column; r393 the glyph-only line; r392 adjacent lists; r391 the LtL panel column; r390 the supervisor closer; "
       "r389 the flipCard group closes its column; r388 the plain / solid alert (the previous FULL); r387 the whakataukī; r386 / r382 instrument corrections; "
       "r385–r377 session 24) — SCOPED regeneration of 74 modules (the ledger at scoped #2 since the r396 FULL, 6 of headroom). **Corpus = r398** (2109 pages / "
       "416 modules). Gates at r398 (`gate_baseline.json`): skeleton **53.759 %** / ≥50 **1166** / ≥75 **195** / ≥90 **18** @ 1956 pairs; RAW 37.846 %; "
       "compare_structure exact **11723** (EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every "
       "widget verifier at its recorded baseline. Ceiling 91.9 % → 58.5 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈09:55 on the r398 corpus "
       "(`_diff_miner_s27_r398.log`: 1956 pairs / **CANDIDATE 172**; `_s27_r398_queue_delta.log`; the pre-r398 queue kept at `_diff_queue_pre_r398.md`): "
       "#630 (the bare `iframe` under the icon videoSection = the standing KB-correct iframe decline) and #411 (a same-label `li` substitution, a miner text "
       "artefact) dispositioned; every other disposition stands.\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **0 of 3** — RESET by r398 (+0.064pp, ≥50 +3). Before it: r397 +0.012pp / r396 +0.000pp counted 2 of 3.\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.68 (session 26 stopped ≈06:15 on the 12-round budget);", "- Standing facts: AppVersion 260619.69 (session 27 in progress);", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈05:50 on the r397 corpus, 173 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈09:55 on the r398 corpus, 172 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes; archive:", len(a.encode("utf-8")), "bytes")
