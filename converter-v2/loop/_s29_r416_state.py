#!/usr/bin/env python3
"""r416 finalise — LOOP_STATE.md: the Round 7 PICK section moves to the archive (+ the what-shipped record), the Position updates,
the Round-log line is appended. Run under WSL."""
import os, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
a = idx("## Session 29 — Round 7 PICK (engine r416)"); b = idx("## Round log")
pick = lines[a:b]
shipped = ("- **What shipped (r416, build 260619.87, 20 Sept ≈21:05):** `activity_wrapper.standalone_title_heading.embedded_free_text {enabled, env EMBTITLE_OFF, max_words 8, "
           "min_chars 3, require_capital, strip_trailing_stop, exclude_alias_words [interactive], remainder_allow [individual, independent, group], widget_directives "
           "[INTERACTIVE, ELEMENT], strip_leading_id}` — `ContentConverter.#embeddedOpenerTitle` at BOTH opener sites (the plain path → `it._embeddedTitle` → "
           "`ActivitiesBuilder.activityOpen` emits the `<h3>` and renders the whole black tail as content; the bundle-owned path → the first `_ownerTitle` lead item), "
           "the new `TagNormaliser.HasInstructionCue`. The first probe's 49 pages taught the rule five guards the census had not seen: the `[interactive activity] type and "
           "check` alias, the Word run split (`L` + `ooking…` joined; `Click` + ` on the link…` prepended to the tail — never dropped), the lowercase aside, the trailing "
           "stop, the broken bracket / leading id. Probe OFF = disk 2555 / 2555; ON 44 pages / 37 modules; scored 41 paired pages 22 up / 12 down / 7 same, +33.1pp-sum "
           "(the dips ≤ 0.7 = the scorer's alignment artefact on gold-titled sites — MXDB202 4B matches its gold byte-for-byte; MXFL104 the A1 minority). THE FULL "
           "REGENERATION of all 494 (`_s29_r416_fullship_par.sh`, 39 batches rc 0, 6 min): 0 stale; the manifest diff = the probe's 44 pages / 37 modules EXACTLY — NO "
           "residue from the seven scoped ships r409–r415; `run_all_gates.sh` + `_gatecheck.py`: every row HELD-or-IMPROVED — skeleton 53.9110 → 53.9284 % (+0.0174pp; "
           "33 movers 22 up / 11 down, 0 outside the set; the pairing ladder re-resolved on ENGI101_1_0 −10.4 (gold 1.0 → 2.0) and MXDI101 (+17.6 net) — named), "
           "≥50 1415 / ≥75 238 / ≥90 20 EXACT, RAW 37.996 → 38.000; cs 14168 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44, tags 9557 — "
           "all EXACT; every verifier ✓; 16 selftests GREEN (46 / 0); feature index GREEN; ledger FULL recorded (scoped counter 0); miner 181 → 181; checksums engine 5 "
           "changed / gates 0. Plateau: +0.0174pp with no other protected gate moved — the window opens at 1 of 3.")
lines[a:b] = ["## Session 29 — Round 7 (engine r416) — THE ACTIVITY TITLE TYPED INSIDE THE RED SPAN + the FULL-regeneration backstop — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 29 — Round 7 PICK (engine r416) + what shipped'; the one-line summary is the s29-r7 Round-log line below.", ""]
p = idx("- LAST SHIPPED: **r415**")
lines[p] = ("- LAST SHIPPED: **r416** (build 260619.87, 20 Sept ≈21:05, session 29 Round 7 — THE ACTIVITY TITLE TYPED INSIDE THE RED SPAN: `[Activity 2A] Concrete poems` all "
            "red — the span's free text, which the r66 rule and the owner lead never read, is the box's `<h3>` (the gold's box opens with it on 40 / 48 = 0.83); "
            "`standalone_title_heading.embedded_free_text`, env `EMBTITLE_OFF`; probe OFF = disk 2555 / 2555, ON 44 pages / 37 modules (22 up / 12 down, +33.1pp-sum); "
            "**THE FULL REGENERATION of all 494 — the ledger's backstop after seven scoped ships (0 stale; the manifest diff = the probe's 44 pages exactly, no residue "
            "from r409–r415; the scoped counter reset to 0)**; **skeleton 53.911 → 53.928 % (+0.0174pp), ≥50 1415, ≥75 238, ≥90 20, RAW 38.000 % @ 2349 pairs**; cs "
            "14168 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44 — all EXACT; every verifier EXACT; 16 selftests GREEN; the miner 181 → 181); "
            "before it **r415** (build 260619.86, 20 Sept ≈20:10, session 29 Round 6 — the owned heading-led bundle with no table, `NOTABLEOWNED_OFF`, 24 up / 2 down, "
            "+0.0246pp, ≥50 +3), **r414** (build 260619.85, the nested activity box, `NESTBOX_OFF`, +0.0696pp, ≥50 +4, ≥75 +2), **r413** (build 260619.84, the owned half "
            "of the r412 class, `HEADTABLEOWNED_OFF`, +0.0080pp), **r412** (build 260619.83, the heading-then-table owner form, `HEADTABLE_OFF`, +0.0139pp), **r411** (build "
            "260619.82, the tile menu ROW+COL shell, `TILEMENUROW_OFF`, +0.0058pp) and **r410** (build 260619.81, the WJFUN tile-page dialect, `TILEPAGE_OFF`, 53.680 → "
            "53.789 %, ≥50 +8). **Corpus = r416** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r416; `outputs/_s29_r416_sk_final.json` the skeleton state; "
            "ceiling 90.9 % → 53.928 = **59.3 % of achievable**).")
q = idx("- Plateau window (§4): **0 of 3**")
lines[q] = "- Plateau window (§4): **1 of 3** — r416 +0.0174pp with no other protected gate moved (the ENGI101 / MXDI101 pairing re-resolutions inside it); r414 +0.0696 / r415 +0.0246 before it. Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.86")
lines[r] = lines[r].replace("AppVersion 260619.86 (r415, session 29 Round 6, 20 Sept); before it 260619.85 (r414)", "AppVersion 260619.87 (r416, session 29 Round 7, 20 Sept); before it 260619.86 (r415) / 260619.85 (r414)")
assert "260619.87" in lines[r]
t = idx("- s29-r6 (engine r415")
lines.insert(t + 1, "- s29-r7 (engine r416, build 260619.87, 20 Sept ≈19:15 → 21:05) · THE ACTIVITY TITLE TYPED INSIDE THE RED SPAN — `[Activity 2A] Concrete poems` all red: the words after the bracket are the span's FREE text, which the r66 standalone title rule and the owner-lead `addLead` (both `blackAfter` readers) never saw, so the title was DROPPED silently (CEDW201 2A–4D, AGH1002 2A, CEDK101 3A, XLP01 4A–4D, the TWHA `Ka pai!` boxes ×11, MXFL202 ×4); found through DIFF_QUEUE #585 decomposed (`_s29_r7_boxtitle.py`: 7582 gold box titles — MATCH 3275, the rest the r369 numbering class / the gold's invented titles / the Bilingual table dialect / the red-embedded rows) and measured by `_s29_r7_redtitle.py` + `_s29_r7_titlerule.cjs` (216 red-embedded opener spans; the rule selects 48 sites / 30 modules, the gold's h3 on 40 = 0.83, every family ≥ 0.67) · `standalone_title_heading.embedded_free_text {enabled, env EMBTITLE_OFF, …}` — `ContentConverter.#embeddedOpenerTitle` at both opener sites (alias not `interactive`, remainder empty / a mode word, no instruction cue, not parenthesised / digit-led / colon-ended, ≤ 8 words, capitalised, not an INTERACTIVE / ELEMENT lexicon tag; a lowercase black tail continues the red words — joined or prepended, never dropped) · SHIPPED · probe OFF = disk 2555 / 2555, ON 44 pages / 37 modules (22 up / 12 down, +33.1pp-sum) · THE FULL REGENERATION of all 494 (39 batches rc 0; 0 stale; the manifest diff = the probe's 44 pages exactly — no residue from r409–r415; the ledger's backstop, counter 0) · skeleton 53.911 → 53.928 (+0.0174pp; 33 movers 22 up / 11 down, 0 outside the set; the ENGI101 −10.4 / MXDI101 +17.6 pairing re-resolutions named), buckets EXACT, RAW 38.000; every other gate EXACT · miner 181 → 181 · plateau 1 of 3 · recorded: the empty-box residue (64; the AGH journal-instruction openers 12 / 3 modules under the floor, the HPFUN numberless boxes 6), the activity-number mismatch (631 / 3540 — the r369 class; WJFUN108 / 105 the gold's reordered tiles; TRR letter-vs-decimal the r330 override), #585's Bilingual table-cell rows (1129)")
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with io.open(ARCH, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n## Session 29 — Round 7 PICK (engine r416) + what shipped — THE ACTIVITY TITLE TYPED INSIDE THE RED SPAN + the FULL-regeneration backstop (20 Sept ≈19:15 → 21:05 NZST)\n\n" + "\n".join(pick).rstrip("\n") + "\n" + shipped + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
