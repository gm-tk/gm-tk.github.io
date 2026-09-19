#!/usr/bin/env python3
"""Session 27 Round 11 SHIPPED (engine r406, scoped #1 since the r405 full) — LOOP_STATE.md: the Position block (LAST SHIPPED r406, gates, ledger scoped #1,
miner 169), the plateau window RESET (0 of 3), Standing facts AppVersion 260619.77, the Round-11 PICK section moved to the archive as the what-shipped record,
the Round-log line. LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r11 (engine r406)" in s:
    print("already applied"); sys.exit(0)
# 1. Position: LAST SHIPPED
i = s.index("- LAST SHIPPED: **r405**"); j = s.index("\n", i) + 1
new = ("- LAST SHIPPED: **r406** (build 260619.77, 19 Sept ≈16:10, session 27 Round 11 — the bracket-less red `Activity 4A` line is the `[Activity 4A]` opener; r405 the journal "
       "section is an activity box (the previous FULL); r404 DECLINED-INERT (the alert-top side column's class by subject); r403 an `[embed]` of an external web page is the KB's "
       "externalButton; r402 the `[interactive: video]` line is the box's first lead element; r401 no synthetic activity box around a widget that captured nothing; r400 the "
       "un-numbered activity opener takes the next positional letter; r399 the wānanga / talanoa box; r398 the videoSection `icon` registry; r397 a table header cell is plain; "
       "r396 the captioned carousel video slide; r395–r387 session 26; r386 / r382 instrument corrections; r385–r377 session 24) — **SCOPED regeneration of the 7 affected modules "
       "(scoped ship #1 since the r405 full; the probe proving the other 409 byte-identical; 0 truly stale; probe ON == disk 39 / 39)**. **Corpus = r406** (2109 pages / 416 "
       "modules). Gates at r406 (`gate_baseline.json`): skeleton **54.025 %** / ≥50 **1176** / ≥75 **200** / ≥90 **18** @ 1956 pairs; RAW 38.012 %; compare_structure exact "
       "**11795** (the text-matched pool 13814 → 13813; EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget "
       "verifier at its recorded baseline. Ceiling 91.9 % → 58.8 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈16:08 on the r406 corpus (`_diff_miner_s27_r406.log`: 1956 "
       "pairs / **CANDIDATE 169**; `_s27_r406_queue_delta.log`; the pre-r406 queue kept at `_diff_queue_pre_r406.md`): nothing gone, nothing new; every disposition stands.\n")
s = s[:i] + new + s[j:]
# 2. Plateau window
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, "- Plateau window (§4): **0 of 3 — RESET by r406** (+0.0244pp AND ≥50 1175 → 1176; the r346 precedent: a ≥50 bucket move is another protected gate moving). "
                   "r404 declined-inert and r405 +0.0032pp had stood at 2 of 3.\n", 1)
# 3. Standing facts
s = s.replace("- Standing facts: AppVersion 260619.76 (session 27 in progress);", "- Standing facts: AppVersion 260619.77 (session 27 in progress);", 1)
# 4. the Round-11 PICK section -> archive
h = "## Session 27 — Round 11 PICK (engine r406, in progress; 19 Sept ≈15:50 NZST): the bracket-less red `Activity 4A` line is the `[Activity 4A]` opener"
i = s.index(h); j = s.index("\n## ", i + 1)
sec = s[i:j].rstrip("\n") + "\n"
shipped = sec.replace(h, "## Session 27 — Round 11 PICK (engine r406) + what shipped — the bracket-less red `Activity 4A` line is the `[Activity 4A]` opener (19 Sept ≈15:50 → 16:10 NZST)", 1)
shipped += ("- **What shipped (r406, build 260619.77):** the first ON probe changed 0 pages — `_s27_r11_itemdump.cjs` proved the red span DID arrive as a no-primary noise tag "
            "item, and the data block turned out to sit one level too deep (`id_heading_opener.bare_red_opener` vs the engine's `opener_rule.bare_red_opener`; relocated by "
            "`_s27_r11_movedata.py`); then the probe OFF 2109 / 2109, ON **15 pages / 7 modules** (ANZH101 1, ENGI102 2, ENGJ402 2, ENGS302 3, PES1001 5, SSFUN06 1, TWHA902 1; "
            "TWHK902's one site is a table cell — not an item); scored on the ON pages **9 up / 3 down / 3 same, pp-sum +47.8** (PES1001_2_0 +22.6, ENGS302_2_0 +9.0; the dips "
            "named: ENGS302_6_0 −4.0 the scorer's alignment on a page whose gold boxes 6C too, PES1001_10_0 −3.6 the gold's colon-split `Vocabulary review` title, PES1001_1_0 "
            "−1.9 the gold's own un-boxed 1B); SCOPED regeneration of the 7 (2 batches rc 0; `_content_manifest.py fresh` 0 truly stale; probe ON == disk 39 / 39); skeleton "
            "54.001 → 54.025 % (+0.0244pp; 12 movers 9 up / 3 down, 0 outside the affected set), **≥50 1175 → 1176** (PES1001_2_0), ≥75 200, ≥90 18, RAW 38.008 → 38.012 %; "
            "compare_structure exact 11795 (the pool −1, the r344 class) / 172 / 626; body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — EXACT; every verifier "
            "RESULT identical to r405; 15 selftests + the feature-index selftest GREEN; ledger scoped #1 since the r405 full; miner 169 → 169; checksums engine 3 changed / "
            "gates 0. **Plateau window RESET (0 of 3).**\n"
            "- **Recorded:** the re-parsed opener + `[H4]` + red instruction + `[Body]` + table takes the r362 MEMBER form (the h4 ends the walk → an empty box with the `no "
            "content captured` flag + the h3 / p / table free after it) where the gold's `activity interactive 4A` holds h3 + p + the built dragAndDrop (ENGI102 lesson 8, +0.8 "
            "only) — the owner form scoped to a lead whose red instruction names a drag-and-drop is the measured follow-up (r362 found the owner form worse for the type-and-check "
            "table); the instruction sentence naming the widget TYPE as prose (`Drag and drop self-marking comprehension questions…`) is a type-from-instruction class of its own "
            "(the r301 no-curve-fitting rule).\n")
a = rd(AR)
if "Round 11 PICK (engine r406) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n" + shipped
    wr(AR, a); print("archive: r406 record appended", len(a.encode("utf-8")))
s = s[:i] + s[j + 1:]
# 5. the Round-log line
line = ("- s27-r11 (engine r406) · THE BRACKET-LESS RED `Activity 4A` LINE IS THE `[Activity 4A]` OPENER (a tag-less, primary-less red span whose entire folded text is the word + id "
        "is re-parsed in place as the typed opener — 36 sites / 14 modules on the parsed WTs, the gold's box count exceeding Claude's on every tracked one; "
        "`InteractiveScanner.#bareRedOpeners`, `opener_rule.bare_red_opener`, env `BAREACT_OFF`; the data block first inserted one level too deep, found by the item dump) · "
        "15 pages / 7 modules · SCOPED regeneration of the 7 (scoped #1 since the r405 full; 0 stale; probe == disk 39 / 39) · skeleton 54.001 → 54.025 (+0.0244pp; 9 up / 3 "
        "down, named), ≥50 1175 → 1176, ≥75 200 / ≥90 18 EXACT; compare_structure exact −1 = the pool −1; every other gate EXACT · 16:10 · plateau RESET 0 of 3\n")
anchor = "- s27-r10 (engine r405"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
wr(LS, s); print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes")
