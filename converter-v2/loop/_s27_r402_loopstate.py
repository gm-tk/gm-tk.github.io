#!/usr/bin/env python3
"""Session 27 Round 7 SHIPPED (engine r402) — LOOP_STATE.md: the Position block (LAST SHIPPED r402, gates, ledger scoped #6, miner 169),
the plateau window 2 of 3, Standing facts AppVersion 260619.73, the Round-7 PICK section moved to the archive as the what-shipped record,
the Round-log line. LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r7 (engine r402)" in s:
    print("already applied"); sys.exit(0)
# 1. Position: LAST SHIPPED
i = s.index("- LAST SHIPPED: **r401**"); j = s.index("\n", i) + 1
new = ("- LAST SHIPPED: **r402** (build 260619.73, 19 Sept ≈14:05, session 27 Round 7 — the `[interactive: video]` line before a widget is the box's first lead element, not its "
       "swallowed opener; r401 no synthetic activity box around a widget that captured nothing; r400 the un-numbered activity opener takes the next positional letter; r399 the "
       "wānanga / talanoa box is the KB's cultural alert; r398 the videoSection `icon` registry re-mined + the widget-embedded video; r397 a table header cell is plain; r396 the "
       "captioned carousel video slide is `item video` (the FULL backstop); r395 the flip-card column width; r394 the clickDrop buttons in the column; r393 the glyph-only line; r392 "
       "adjacent lists; r391 the LtL panel column; r390 the supervisor closer; r389 the flipCard group closes its column; r388 the plain / solid alert (the previous FULL); r387 the "
       "whakataukī; r386 / r382 instrument corrections; r385–r377 session 24) — SCOPED regeneration of 3 modules (the ledger at scoped #6 since the r396 FULL, 2 of headroom — the "
       "FULL backstop is due at 8). **Corpus = r402** (2109 pages / 416 modules). Gates at r402 (`gate_baseline.json`): skeleton **53.989 %** / ≥50 **1174** / ≥75 **200** / ≥90 "
       "**18** @ 1956 pairs; RAW 38.000 %; compare_structure exact **11798** (EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / "
       "23; every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.7 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈14:03 on the r402 corpus "
       "(`_diff_miner_s27_r402.log`: 1956 pairs / **CANDIDATE 169**; `_s27_r402_queue_delta.log`; the pre-r402 queue kept at `_diff_queue_pre_r402.md`): nothing gone, nothing "
       "new; every disposition stands.\n")
s = s[:i] + new + s[j:]
# 2. Plateau window
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, "- Plateau window (§4): **2 of 3** — r401 +0.0095pp, r402 gate-neutral (0 movers), no other protected gate moving in either (r400 +0.118pp had RESET it). "
                   "A third round under 0.02pp with nothing else moving STOPS the session.\n", 1)
# 3. Standing facts
s = s.replace("- Standing facts: AppVersion 260619.72 (session 27 in progress);", "- Standing facts: AppVersion 260619.73 (session 27 in progress);", 1)
# 4. the Round-7 PICK section -> archive as the what-shipped record
h = "## Session 27 — Round 7 PICK (in progress; 19 Sept ≈13:45 NZST): the `[interactive: X]` bracket's `activity` alias must not make the preceding media line a widget's OWNER"
i = s.index(h); j = s.index("\n## ", i + 1)
sec = s[i:j].rstrip("\n") + "\n"
shipped = sec.replace(h, "## Session 27 — Round 7 PICK (engine r402) + what shipped — the `[interactive: video]` line before a widget is the box's first lead element, not its swallowed opener (19 Sept ≈13:45 → 14:05 NZST)", 1)
shipped += ("- **What was measured (`_s27_r7_ownerscan.cjs`, the live scanner over all 416):** 128 owner spans whose primary is not `activity` (37 modules / 80 pages) — 108 carry the "
            "word `activity` itself (`[Activity 2A] [H3] Title` 78, `[Individual activity] [H3]`, `[Activity 5A: Video Review]` …) and are owners by right; **20 carry the `interactive` "
            "alias**: 14 `[interactive: video]` (AGH1004 / AGH1005 / AGH1006), `[interactive: Video – …]` TWHA902 / TWHK901 (video, `how = embedded`), and the embedded image / list "
            "instruction forms (AGH1009 ×2, ENFUN03, XTAS102).\n"
            "- **Variant (a) — the aliased span is NOT an owner (the widget standalone): DECLINED on the gate's own scorer** — 18 changed paired pages, 4 up / 14 down, −31.0 pp-sum: "
            "the gold BOXES the group the `[interactive: X]` line leads (AGH1005 7A = `<h3>` + the built carousel = the owner form to the line), so the owner reading is structurally "
            "right; only the video line's silent loss was the defect.\n"
            "- **Variant (b) — the span stays the owner but is the box's first LEAD element (a synthetic bare opener takes its place; the r364 lead_media path renders it): SHIPPED "
            "scoped** — unscoped 14 same / 4 down (the embedded image / list forms: AGH1009_8_0 −7.0 whose span's `3` had been the box id, ENFUN03 / XTAS102 / AGH1009_6_0 ≤ −0.2); "
            "with `element_tags` (video / audio / image) + `exclude_primary_hows` (embedded) the population is the 14 AGH `[interactive: video]` sites: probe OFF 2109 / 2109, ON 12 "
            "pages / 3 modules, every change a `cv2-note` (the video's `no URL` flag now surfaces inside the box, r203-coalesced with the widget's own flag where both print); scored "
            "12 same; the 3 regenerated (1 batch rc 0; `fresh --affected` 0 truly stale; probe ON == disk 26 / 26); skeleton 53.989 / 1174 / 200 / 18 / RAW 38.000 page-for-page "
            "(0 movers); every other gate EXACT; every verifier RESULT identical to r401; 15 selftests + the feature-index selftest GREEN; ledger scoped #6 since the r396 FULL (2 of "
            "headroom); miner 169 → 169; checksums engine 3 changed / gates 0. A small gate-neutral ship under the 20-page floor on the r320 precedent — built, proven, right (the r43 "
            "rule: a documented request is never silently stripped).\n"
            "- **Recorded:** the `how = embedded` video forms (TWHA902 / TWHK901) render NOTHING through the lead media path (a MediaBuilder question — an embedded-head video with no "
            "URL should print its flag); the AGH videos' URLs are Media-List items (the r292 class) — the gold's `videoSection` needs that resolution, not the scanner.\n")
a = rd(AR)
if "Round 7 PICK (engine r402) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n" + shipped
    wr(AR, a); print("archive: r402 record appended", len(a.encode("utf-8")))
s = s[:i] + s[j + 1:]
# 5. the Round-log line
line = ("- s27-r7 (engine r402) · THE `[interactive: video]` LINE BEFORE A WIDGET IS THE BOX'S FIRST LEAD ELEMENT, NOT ITS SWALLOWED OPENER (the scanner's owner lookback keeps the "
        "aliased span as the owner — the gold boxes the group it leads; the standalone form scored 4 up / 14 down and was DECLINED — but renders it through the r364 lead_media path "
        "behind a synthetic bare opener, so the writer's video request surfaces as its flag instead of vanishing; `BoundaryBank._meta.opener_rule.owner_alias_exclude`, env "
        "`OWNERALIAS_OFF`; found by the owner-span census `_s27_r7_ownerscan.cjs`: 128 non-activity-primary owners, 20 aliased) · SCOPED regen 3 AGH modules / 12 pages (gate-neutral, "
        "every change a `cv2-note`; scoped ship #6 since the r396 FULL) · skeleton 53.989 / 1174 / 200 / 18 page-for-page, every gate EXACT · 14:05 · plateau 2 of 3\n")
anchor = "- s27-r6 (engine r401)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
wr(LS, s); print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes")
