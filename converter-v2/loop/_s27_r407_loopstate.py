#!/usr/bin/env python3
"""Session 27 Round 12 SHIPPED (engine r407, scoped #2 since the r405 full) AND THE SESSION STOP (§4 budget: 12 rounds) — LOOP_STATE.md:
the Position block (LAST SHIPPED r407), the plateau window, Standing facts AppVersion 260619.78, the Round-12 PICK section moved to the archive
as the what-shipped record, the Round-log line, the session-26 STOPPED entry moved to the archive, the session-27 STOPPED entry (≤ 1,500 chars)
in its place, and the "Next session starts with:" line rewritten. LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r12 (engine r407)" in s:
    print("already applied"); sys.exit(0)
# 1. Position: LAST SHIPPED
i = s.index("- LAST SHIPPED: **r406**"); j = s.index("\n", i) + 1
new = ("- LAST SHIPPED: **r407** (build 260619.78, 19 Sept ≈16:35, session 27 Round 12 — the heading-led numbered opener takes the owner form too; r406 the bracket-less red "
       "`Activity 4A` opener; r405 the journal section is an activity box (the FULL backstop); r404 DECLINED-INERT; r403 the `[embed]` externalButton; r402 the `[interactive: video]` "
       "lead element; r401 no synthetic box around an empty capture; r400 the un-numbered opener's positional letter; r399 the wānanga box; r398 the videoSection `icon` registry; "
       "r397 a table header cell is plain; r396 the captioned carousel video slide; r395–r387 session 26; r386 / r382 instrument corrections; r385–r377 session 24) — **SCOPED "
       "regeneration of the 24 affected modules (scoped ship #2 since the r405 full; the probe proving the other 392 byte-identical; 0 truly stale; probe ON == disk 197 / 197)**. "
       "**Corpus = r407** (2109 pages / 416 modules). Gates at r407 (`gate_baseline.json`): skeleton **54.084 %** / ≥50 **1181** / ≥75 **202** / ≥90 **18** @ 1956 pairs; RAW "
       "38.022 %; compare_structure exact **11779** (the text-matched pool 13813 → 13794; EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 216 / 42 / 5 / 170 (runaway +1 "
       "ENGI202_2_0 named; EMPTY −3, ANY −2); clean 2079 / 2102, leak 26 / 23; every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.8 % of achievable. "
       "`DIFF_QUEUE.md` re-mined 19 Sept ≈16:32 on the r407 corpus (`_diff_miner_s27_r407.log`: 1956 pairs / **CANDIDATE 168**; `_s27_r407_queue_delta.log`; the pre-r407 queue "
       "kept at `_diff_queue_pre_r407.md`): one row gone (`activity MISSING div.col-12 › h3` — this round's class under the floor), nothing new; every disposition stands.\n")
s = s[:i] + new + s[j:]
# 2. Plateau window
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, "- Plateau window (§4): **0 of 3** — r406 (+0.0244pp, ≥50 +1) and r407 (+0.0583pp, ≥50 +5, ≥75 +2) both moved a protected bucket. The session stopped on the "
                   "§4 BUDGET (12 rounds), not the plateau.\n", 1)
# 3. Standing facts
s = s.replace("- Standing facts: AppVersion 260619.77 (session 27 in progress);", "- Standing facts: AppVersion 260619.78 (session 27 STOPPED 19 Sept ≈16:40 on the budget);", 1)
# 4. the Round-12 PICK section -> archive
h = "## Session 27 — Round 12 PICK (engine r407, in progress; 19 Sept ≈16:25 NZST; the budget's last round): the heading-led numbered opener takes the OWNER form — no empty box before its own section"
i = s.index(h); j = s.index("\n## ", i + 1)
sec = s[i:j].rstrip("\n") + "\n"
shipped = sec.replace(h, "## Session 27 — Round 12 PICK (engine r407) + what shipped — the heading-led numbered opener takes the owner form too (19 Sept ≈16:15 → 16:40 NZST; the budget's last round)", 1)
shipped += ("- **What shipped (r407, build 260619.78):** `heading_led_owner.empty_walk_owner {enabled, env HEADLEDOWNER_OFF}` — `member_form_tags` ignored, every heading-led "
            "numbered opener takes the r362 owner form. The probe OFF 2109 / 2109, ON **56 pages / 24 modules**; scored on the ON pages **32 up / 6 down / 16 same, pp-sum +114.0** "
            "(ENGI102_8_0 +16.5, HIS1008_6_0 +10.1, MXFL203_2_0 +9.8, ENGI102_10_0 +9.6; the dips named: MXFUN01_6_2 −11.5 and MXFUN01_5_0 −5.9 the r362-named type-and-check tables "
            "now inside the hand-off box, AGH1008_3_0 −4.6 the gold has no box #2C, TEDC401_1_0 −1.6, MXEO401_3_0 −1.4, XTAS102_1_0 −0.9); SCOPED regeneration of the 24 (4 batches rc "
            "0; `_content_manifest.py fresh` 0 truly stale; probe ON == disk 197 / 197); skeleton 54.025 → 54.084 % (+0.0583pp; 38 movers 32 up / 6 down, 0 outside the affected "
            "set), **≥50 1176 → 1181, ≥75 200 → 202**, ≥90 18, RAW 38.012 → 38.022 %; compare_structure exact 11779 (the pool −19, the r344 class) / 172 / 626; body_compare 42 / 5 "
            "(runaway +1 = ENGI202_2_0, the 2A owner walk absorbing table + list + bubble — named) / 170 / 216 (EMPTY −3, ANY −2 IMPROVED); clean 2079 / 2102, leak 26 / 23 EXACT; every "
            "verifier RESULT identical to r406; 15 selftests + the feature-index selftest GREEN; ledger scoped #2 since the r405 full; miner 169 → 168 (the `activity MISSING "
            "div.col-12 › h3` row under the floor); checksums engine 4 changed / gates 0.\n"
            "- **Recorded:** the typed-widget empty boxes (`[Activity 2A drag and drop]` + a heading, 20 of the 75 — the normal widget path's walk ended by the heading; the gold's box "
            "holds h3 + the built widget: AGH1005 2A, TEDC402 2D / 6A / 6B / 7A, TEFUN02 / 05 / 06, HES1005 7C, HIS1002 1A) — the same owner form at the normal path's opener site is "
            "the next candidate; MXFUN01's type-and-check tables (the r362 dips) want the typing builder, not a boundary rule.\n")
a = rd(AR)
if "Round 12 PICK (engine r407) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n" + shipped
    wr(AR, a); print("archive: r407 record appended", len(a.encode("utf-8")))
s = s[:i] + s[j + 1:]
# 5. the Round-log line
line = ("- s27-r12 (engine r407) · THE HEADING-LED NUMBERED OPENER TAKES THE OWNER FORM TOO (the r362 / r363 member form kept for an h2–h5-led lead was an EMPTY box with the section "
        "free after it; the gold's same-numbered box holds h3 + widget / prose / table on 61 of 75 = 0.81 — `_s27_r12_emptyowner.py`; `unclassified_activity_lead.heading_led_owner."
        "empty_walk_owner`, env `HEADLEDOWNER_OFF`) · 56 pages / 24 modules · SCOPED regeneration of the 24 (scoped #2 since the r405 full; 0 stale; probe == disk 197 / 197) · "
        "skeleton 54.025 → 54.084 (+0.0583pp; 32 up / 6 down — the r362-named MXFUN01 dips named), ≥50 1176 → 1181, ≥75 200 → 202, ≥90 18; compare_structure exact −16 = the pool "
        "−19; body_compare runaway +1 (named) / EMPTY −3 / ANY −2; every other gate EXACT · miner 169 → 168 · 16:35 · plateau 0 of 3 · THE BUDGET'S LAST ROUND\n")
anchor = "- s27-r11 (engine r406"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
# 6. the session-26 STOPPED entry -> archive; the session-27 STOPPED entry in its place
h26 = "## >>> STOPPED 2026-09-19 ≈06:15 NZST (session 26)"
i = s.index(h26); j = s.index("\n", i) + 1
old26 = s[i:j]
a = rd(AR)
if "STOPPED 2026-09-19 ≈06:15 NZST (session 26)" not in a:
    a = a.rstrip("\n") + "\n\n## STOPPED entry, session 26 (moved from LOOP_STATE.md at the session-27 stop)\n\n" + old26
    wr(AR, a); print("archive: s26 STOPPED moved", len(a.encode("utf-8")))
stop27 = ("## >>> STOPPED 2026-09-19 ≈16:40 NZST (session 27) on §4 BUDGET — 12 rounds done (the §7 default; 8 h of the 10). NINE SHIPPED: r398 the videoSection `icon` "
          "registry re-mined + widget-embedded videos · r399 the wānanga / talanoa box is the KB's cultural alert (+0.103pp, cs exact +75) · r400 the un-numbered opener takes the "
          "next positional letter (+0.118pp, ≥50 +4 / ≥75 +3) · r401 no synthetic box around an empty capture · r402 the `[interactive: video]` lead element (gate-neutral) · "
          "r403 the `[embed]` of an external page is the externalButton (≥50 +1) · r405 the journal section is an activity box (FULL backstop: all 416, 0 stale, no residue) · "
          "r406 the bracket-less red `Activity 4A` opener (+0.0244pp, ≥50 +1) · r407 the heading-led opener takes the owner form (+0.0583pp, ≥50 +5 / ≥75 +2); r404 DECLINED-INERT "
          "(the side column's class by subject); Rounds 3 / 4 PICK passes (14 classes measured, none taken). Skeleton **53.695 → 54.084 %** (+0.389pp; 58.8 % of the "
          "91.9 % ceiling), ≥50 1163 → 1181, ≥75 195 → 202, ≥90 18; compare_structure exact 11723 → 11779; every other gate EXACT or better; every verifier RESULT identical; "
          "15 + 1 selftests GREEN every round. The miner re-mined after every ship: 173 → 168 CANDIDATE rows, all dispositioned. Plateau window 0 of 3 (reset by r406 / r407). "
          "Build 260619.78; ledger scoped #2 since the r405 FULL. NEEDS CHRIS: the five items of the session-26 STOPPED entry stand (archive: 'STOPPED entry, session 26'). "
          "Tree clean at the stop commit. <<<\n")
assert len(stop27) <= 1500, len(stop27)
s = s[:i] + stop27 + s[j:]
# 7. Next session starts with
i = s.index("**Next session starts with:**"); j = s.index("\n", i)
nxt = ("**Next session starts with:** the standing `/loop-start`; health check (locks, `verify_after_transfer.sh` PASS, `wc -c`); `git status` in pageforge-site: a CLEAN tree "
       "at the session-27 stop commit (r407 beneath it); the miner's queue (≈16:32, the r407 corpus) is current — 168 CANDIDATE rows, all dispositioned; this session's productive "
       "instrument was the PAIRED ACTIVITY-BOX CENSUS against the gold's same-numbered box (`_s27_r6_emptybox.py`, `_s27_r11_bareact.out`, `_s27_r12_emptyowner.py`) — the next "
       "candidates from it: the typed-widget empty boxes (20 — the normal widget path's opener + a heading, the owner form at that site) and the 14 gold-absent boxes; score "
       "every candidate with `_skeleton_compare.match()` on the probe's ON pages BEFORE regenerating; the ledger is at scoped #2 since the r405 FULL (a FULL backstop by the 8th); "
       "`python3` only ever under `wsl.exe -e bash -lc` (the native stub hangs); the five needs-Chris items are in the session-26 STOPPED entry (archive).")
s = s[:i] + nxt + s[j:]
wr(LS, s); print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes")
