#!/usr/bin/env python3
"""Session 27 Round 6 SHIPPED (engine r401) — LOOP_STATE.md: the Position block (LAST SHIPPED r401, gates, ledger scoped #5, miner re-mined 169),
the plateau window 1 of 3, Standing facts AppVersion 260619.72, the Round-6 PICK section moved to the archive as the what-shipped record,
the Round-log line. LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r6 (engine r401)" in s:
    print("already applied"); sys.exit(0)
# 1. Position: LAST SHIPPED
i = s.index("- LAST SHIPPED: **r400**"); j = s.index("\n", i) + 1
new = ("- LAST SHIPPED: **r401** (build 260619.72, 19 Sept ≈13:40, session 27 Round 6 — no synthetic activity box around a widget that captured nothing; "
       "r400 the un-numbered activity opener takes the next positional letter; r399 the wānanga / talanoa box is the KB's cultural alert; r398 the videoSection `icon` registry "
       "re-mined + the widget-embedded video; r397 a table header cell is plain; r396 the captioned carousel video slide is `item video` (the FULL backstop); r395 the flip-card "
       "column width; r394 the clickDrop buttons in the column; r393 the glyph-only line; r392 adjacent lists; r391 the LtL panel column; r390 the supervisor closer; r389 the "
       "flipCard group closes its column; r388 the plain / solid alert (the previous FULL); r387 the whakataukī; r386 / r382 instrument corrections; r385–r377 session 24) — SCOPED "
       "regeneration of 22 modules (the ledger at scoped #5 since the r396 FULL, 3 of headroom — the FULL backstop is due at 8). **Corpus = r401** (2109 pages / 416 modules). "
       "Gates at r401 (`gate_baseline.json`): skeleton **53.989 %** / ≥50 **1174** / ≥75 **200** / ≥90 **18** @ 1956 pairs; RAW 38.000 %; compare_structure exact **11798** "
       "(EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget verifier at its recorded baseline. Ceiling 91.9 % → "
       "58.7 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈13:37 on the r401 corpus (`_diff_miner_s27_r401.log`: 1956 pairs / **CANDIDATE 169**; `_s27_r401_queue_delta.log`; "
       "the pre-r401 queue kept at `_diff_queue_pre_r401.md`): nothing gone, nothing new (the empty synthetic box's `row > col-12` chain was never a text-matched class); every "
       "disposition stands.\n")
s = s[:i] + new + s[j:]
# 2. Plateau window
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, "- Plateau window (§4): **1 of 3** — r401 +0.0095pp with no other protected gate moving (r400 +0.118pp had RESET it).\n", 1)
# 3. Standing facts
s = s.replace("- Standing facts: AppVersion 260619.71 (session 27 in progress);", "- Standing facts: AppVersion 260619.72 (session 27 in progress);", 1)
# 4. the Round-6 PICK section -> archive as the what-shipped record
h = "## Session 27 — Round 6 PICK (engine r401, in progress; 19 Sept ≈13:25 NZST): no synthetic activity box around a widget that captured nothing"
i = s.index(h); j = s.index("\n## ", i + 1)
sec = s[i:j].rstrip("\n") + "\n"
shipped = sec.replace(h, "## Session 27 — Round 6 PICK (engine r401) + what shipped — no synthetic activity box around a widget that captured nothing (19 Sept ≈13:25 → 13:40 NZST)", 1)
shipped += ("- **What shipped (r401, build 260619.72):** the probe OFF 2109 / 2109; ON 27 pages / 22 modules (NOT the census's 74 pages — the other note-only boxes are the writer's "
            "OWN openers owning an empty bundle, whose box the gold ships with the widget built; the census re-run on the ON pages reads 98 → 78 note-only boxes, "
            "`_s27_r401_emptybox_on.py`); scored on the ON pages 22 up / 4 down / 1 same (+18.5); the 22 regenerated (4 batches, all rc 0; `fresh --affected` 0 truly stale; probe "
            "ON == disk 145 / 145); skeleton 53.979 → 53.989 % (+0.0095pp; 26 movers 22 up / 4 down, 0 outside the affected set — the 4 dips named: XLP05_5_0 −1.0, AGH1004_6_0 −0.9, "
            "AGH1006_2_0 −0.7, TEDC401_4_0 −0.6, pages whose gold ships a numbered box with the widget BUILT where Claude's empty box had matched its line by coincidence — the capture "
            "class), ≥50 1174, ≥75 200, ≥90 18 EXACT, RAW 37.995 → 38.000 %; compare_structure 11798 / 172 / 626, body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — "
            "EXACT; every verifier RESULT identical to r400; 15 selftests + the feature-index selftest GREEN; ledger scoped #5 since the r396 FULL (3 of headroom); miner 169 → 169 "
            "CANDIDATE (nothing gone, nothing new); checksums engine 4 changed / gates 0.\n"
            "- **Recorded (the next PICK's first candidate):** the `[interactive: video]` / `[interactive: X]` bracket resolves the tags `[\"X\", \"activity\"]` "
            "(`_s27_r5_parse1.cjs`), and `InteractiveScanner`'s owner lookback (`prev.parse.tags.some(t => t.tag === \"activity\")`) takes any span carrying an `activity` tag as the "
            "following widget's OWNER — AGH1005 lesson 2: the `[interactive: video]` line becomes the drag-and-drop's activity owner, its video never renders (the gold's `videoSection` "
            "is missing from Claude's page) and the 2A box opens empty. A primary-tag (or bare `[Activity …]`) fence on the lookback; measure the `[interactive: media]`-before-widget "
            "population first.\n")
a = rd(AR)
if "Round 6 PICK (engine r401) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n" + shipped
    wr(AR, a); print("archive: r401 record appended", len(a.encode("utf-8")))
s = s[:i] + s[j + 1:]
# 5. the Round-log line
line = ("- s27-r6 (engine r401) · NO SYNTHETIC ACTIVITY BOX AROUND A WIDGET THAT CAPTURED NOTHING (the r217 standalone box consults the placeholder's own content test — "
        "`ContentConverter.#bundleHasContent`, factored verbatim out of `#interactivePlaceholder` — and a content-less bundle renders its `no content captured` flag alone in the "
        "section flow, no box, no letter; `activity_wrapper.standalone_widget_box.skip_empty`, env `SABOXEMPTY_OFF`; found by the post-r400 activity-box census "
        "`_s27_r6_emptybox.py`: 98 note-only boxes on the paired pages, the gold 4 in 2385) · SCOPED regen 22 modules (the probe proving the other 394 byte-identical; scoped ship #5 "
        "since the r396 FULL) · skeleton 53.979 → 53.989 (+0.0095pp; 26 movers 22 up / 4 down, named), buckets 1174 / 200 / 18 EXACT; every other gate EXACT · 13:40 · plateau 1 of 3 · "
        "recorded: the `[interactive: X]` bracket's `activity` tag makes the scanner's owner lookback swallow the preceding media line (AGH1005 2A) — the next candidate\n")
anchor = "- s27-r5 (engine r400)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
wr(LS, s); print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes")
