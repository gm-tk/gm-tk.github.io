#!/usr/bin/env python3
"""Session 27 Round 8 SHIPPED (engine r403) — LOOP_STATE.md: the Position block (LAST SHIPPED r403, gates, ledger scoped #7, miner 169),
the plateau window RESET (>=50 +1), Standing facts AppVersion 260619.74, the Round-8 PICK section moved to the archive as the what-shipped
record, the Round-log line. LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r8 (engine r403)" in s:
    print("already applied"); sys.exit(0)
# 1. Position: LAST SHIPPED
i = s.index("- LAST SHIPPED: **r402**"); j = s.index("\n", i) + 1
new = ("- LAST SHIPPED: **r403** (build 260619.74, 19 Sept ≈15:05, session 27 Round 8 — an `[embed]` of an external web page is the KB's externalButton, never a bare iframe; "
       "r402 the `[interactive: video]` line is the box's first lead element; r401 no synthetic activity box around a widget that captured nothing; r400 the un-numbered activity "
       "opener takes the next positional letter; r399 the wānanga / talanoa box is the KB's cultural alert; r398 the videoSection `icon` registry re-mined + the widget-embedded "
       "video; r397 a table header cell is plain; r396 the captioned carousel video slide is `item video` (the FULL backstop); r395–r387 session 26; r386 / r382 instrument "
       "corrections; r385–r377 session 24) — SCOPED regeneration of 53 modules (**the ledger at scoped #7 since the r396 FULL — THE NEXT SHIP IS THE FULL BACKSTOP**). "
       "**Corpus = r403** (2109 pages / 416 modules). Gates at r403 (`gate_baseline.json`): skeleton **53.998 %** / ≥50 **1175** / ≥75 **200** / ≥90 **18** @ 1956 pairs; RAW "
       "38.006 %; compare_structure exact **11798** (EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget "
       "verifier at its recorded baseline. Ceiling 91.9 % → 58.7 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈15:00 on the r403 corpus (`_diff_miner_s27_r403.log`: 1956 "
       "pairs / **CANDIDATE 169**; `_s27_r403_queue_delta.log`; the pre-r403 queue kept at `_diff_queue_pre_r403.md`): one row gone (`activity EXTRA div.col-12 › div.TKmodal`, "
       "20 pages / 17 modules — an alignment shadow), one new at the floor (`body SUBSTITUTED div.col-12.col-md-8: div.alert → div.activity.clickDropContent.dropbox[number=*]`, "
       "20 pages / 4 modules — the XDLS tile-panel alignment, an artefact to measure before taking); every other disposition stands.\n")
s = s[:i] + new + s[j:]
# 2. Plateau window
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, "- Plateau window (§4): **0 of 3** — r403 +0.0091pp but ≥50 1174 → 1175 moved a protected bucket, which RESETS the window (the r346 precedent); "
                   "r401 +0.0095 / r402 gate-neutral had counted 1 and 2.\n", 1)
# 3. Standing facts
s = s.replace("- Standing facts: AppVersion 260619.73 (session 27 in progress);", "- Standing facts: AppVersion 260619.74 (session 27 in progress);", 1)
# 4. the Round-8 PICK section -> archive as the what-shipped record
h = "## Session 27 — Round 8 PICK (engine r403, in progress; 19 Sept ≈14:55 NZST): an `[embed]` of an external web page is the KB's externalButton, never a bare iframe"
i = s.index(h); j = s.index("\n## ", i + 1)
sec = s[i:j].rstrip("\n") + "\n"
shipped = sec.replace(h, "## Session 27 — Round 8 PICK (engine r403) + what shipped — an `[embed]` of an external web page is the KB's externalButton, never a bare iframe (19 Sept ≈14:40 → 15:05 NZST)", 1)
shipped += ("- **What shipped (r403, build 260619.74):** the probe OFF 2109 / 2109; ON 66 pages / 53 modules (every site the 3-line wrapper → the 1-line anchored button); scored on "
            "the ON pages 18 up / 2 down / 44 same (+17.7); the 53 regenerated (6 batches, all rc 0; `fresh --affected` 0 truly stale; probe ON == disk 344 / 344); skeleton "
            "53.989 → 53.998 % (+0.0091pp; 20 movers 18 up / 2 down, 0 outside the affected set — XDLS903_7_0 −8.7 the scorer's alignment artefact on a page whose gold ships this "
            "very site as `a > div.externalButton`, MXDI202_8_0 −0.7), **≥50 1174 → 1175** (TEFUN08_0_0), ≥75 200, ≥90 18, RAW 38.000 → 38.006 %; compare_structure 11798 / 172 / 626, "
            "body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — EXACT; every verifier RESULT identical to r402; 15 selftests + the feature-index selftest GREEN; "
            "**ledger scoped #7 since the r396 FULL — the next ship must be the FULL regeneration backstop**; miner 169 → 169 (one alignment-shadow row gone, one alignment row "
            "new at the floor); checksums engine 3 changed / gates 0.\n"
            "- **Also this round, a 30-minute loss to the memory-note trap:** a `python3 - <<EOF` typed natively under Git Bash hung on the Windows Store stub and had to be killed — "
            "every python invocation goes through `wsl.exe -e bash -lc`, never a native heredoc.\n")
a = rd(AR)
if "Round 8 PICK (engine r403) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n" + shipped
    wr(AR, a); print("archive: r403 record appended", len(a.encode("utf-8")))
s = s[:i] + s[j + 1:]
# 5. the Round-log line
line = ("- s27-r8 (engine r403) · AN `[embed]` OF AN EXTERNAL WEB PAGE IS THE KB'S externalButton, NEVER A BARE IFRAME (the label census's Claude-only `div.ratio.ratio-16x9` — gold 0 / "
        "Claude 133; on the paired pages the gold iframes none of the 129 sites, drops 91 and links 38 — 24 buttons, 14 anchors; the `[embed]` route now emits the r338 external-destination "
        "form for a non-internal host; `elements.embeds.external_button`, env `EMBEDBTN_OFF`; KB 05D + constraint 75; measured and declined first: the r6 merge-box class, gold own-box "
        "0.62 / merged 0.08) · SCOPED regen 53 modules / 66 pages (the probe proving the other 363 byte-identical; scoped ship #7 since the r396 FULL — the FULL backstop is due next) · "
        "skeleton 53.989 → 53.998 (+0.0091pp; 20 movers 18 up / 2 down, named), ≥50 1174 → 1175; every other gate EXACT · 15:05 · plateau RESET (≥50 moved)\n")
anchor = "- s27-r7 (engine r402)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
wr(LS, s); print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes")
