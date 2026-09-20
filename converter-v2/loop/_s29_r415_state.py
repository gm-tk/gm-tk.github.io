#!/usr/bin/env python3
"""r415 finalise — LOOP_STATE.md: the Round 6 PICK section moves to the archive (+ the what-shipped record), the Position updates,
the Round-log line is appended. Run under WSL."""
import os, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
a = idx("## Session 29 — Round 6 PICK (engine r415)"); b = idx("## Round log")
pick = lines[a:b]
shipped = ("- **What shipped (r415, build 260619.86, 20 Sept ≈20:10):** `opener_rule.heading_table_owner.owned_bundles.no_table {enabled, env NOTABLEOWNED_OFF}` — in "
           "`InteractiveScanner.#headingTableOwner` the table look-ahead no longer returns on a non-table item; when it finds no table, an OWNED bundle (a real owner, or "
           "`bundle.activityId != null` — the r92 embedded form `[Activity 1A] [Dropdown Quiz…]`, which the first probe missed: 22 pages → 35 once the gate widened) takes "
           "the heading as its first lead item and the member walk RESUMES right after it (`#swallowMembers` from the heading's successor; the r366 lead_free rule frees the "
           "first paragraph). Probe OFF = disk 2555 / 2555; ON 35 pages / 22 modules; scored with the gate's own `match()` 34 paired pages 24 up / 2 down / 8 same, "
           "+57.7pp-sum (MiW 8 / 0, NCEA1 4 / 0, Science 3 / 0, Maths 1 / 0, Technology 6 / 0 + 7 same, EXPlore 1 / 0, ENFUN 1 / 2 −1.5; without WJFUN 16 / 2, +36.6). "
           "SCOPED regeneration of the 22 + the 12-module sample (4 batches rc 0; content-hash 0 truly stale; containment 22 ⊆ 22; spot-check 12 / 12); `scoped_ship.sh` "
           "FAILED on `compare_structure exact chain` −6 alone (14174 → 14168) — decomposed per module (`_s29_r415_cs_decomp.log`: the matched pool −13 — ENFUN01 −2, "
           "ENFUN03 −6, ENFUN04 −1, SCES201 −1, TEFUN02 −1, WJFUN210 −1, WJFUN306 −1 — all inside the affected set; EXTRA 186 EXACT; MISSING 690 → 683 IMPROVED = the "
           "r57 / r147 / r412 relocation class) → `_fastloop_diff.py $UNION --commit --accept-named 'compare_structure exact chain'` (MOVED, ACCEPTED AS NAMED) + the "
           "manifest snapshot; skeleton 53.8864 → 53.9110 % (+0.0246pp; 26 movers 24 up / 2 down — ENFUN03_0_0 −1.8, ENFUN01_0_0 −0.2; 0 outside the set), ≥50 "
           "1412 → 1415, ≥75 238, ≥90 20, RAW 37.997 → 37.996 (the captured section moving inside the collapsed widget — the net-positive class); body_compare runaway "
           "6 → 5 / ANY 248 → 247; defect / tags / every verifier EXACT; 16 selftests GREEN (46 PASS / GREEN, 0 FAIL); feature index GREEN; ledger scoped #7 since the "
           "19 Sept FULL (1 of headroom — THE NEXT SHIP MUST BE THE FULL `ship.sh` BACKSTOP); miner 181 → 181; checksums engine 4 changed / gates 0.")
lines[a:b] = ["## Session 29 — Round 6 (engine r415) — THE OWNED HEADING-LED BUNDLE WITH NO TABLE: the empty writer-owned box takes its section — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 29 — Round 6 PICK (engine r415) + what shipped'; the one-line summary is the s29-r6 Round-log line below.", ""]
p = idx("- LAST SHIPPED: **r414**")
lines[p] = ("- LAST SHIPPED: **r415** (build 260619.86, 20 Sept ≈20:10, session 29 Round 6 — THE OWNED HEADING-LED BUNDLE WITH NO TABLE: a writer-owned (or r92 embedded-id) "
            "typed-widget box whose walk ended on the writer's `[H3]`, the quiz written as paragraphs after it, takes the heading as its lead and resumes the member walk "
            "right after it — the r412 / r413 rule completed for the no-table dialect; `heading_table_owner.owned_bundles.no_table`, env `NOTABLEOWNED_OFF`; Claude 96 empty "
            "writer-owned boxes, the gold's same-numbered box holding the section on 60 = 0.63; probe OFF = disk 2555 / 2555, ON 35 pages / 22 modules (24 up / 2 down, "
            "+57.7pp-sum); SCOPED regeneration of the 22 — **scoped ship #7 since the 19 Sept FULL (1 of headroom — the NEXT ship is the FULL `ship.sh` backstop)**; "
            "**skeleton 53.886 → 53.911 % (+0.0246pp), ≥50 1412 → 1415, ≥75 238, ≥90 20, RAW 37.996 % @ 2349 pairs**; cs exact 14174 → 14168 = the matched pool −13, "
            "the relocation class accepted by name (`_fastloop_diff.py --accept-named`), MISSING 690 → 683; body runaway 6 → 5; every other gate EXACT; 16 selftests GREEN; "
            "the miner 181 → 181); before it **r414** (build 260619.85, 20 Sept ≈18:30, session 29 Round 5 — the nested activity box, `NESTBOX_OFF`, 81 up / 3 down, "
            "+0.0696pp, ≥50 +4, ≥75 +2), **r413** (build 260619.84, the owned half of the r412 class, `HEADTABLEOWNED_OFF`, +0.0080pp), **r412** (build 260619.83, the "
            "heading-then-table owner form, `HEADTABLE_OFF`, +0.0139pp), **r411** (build 260619.82, the tile menu ROW+COL shell, `TILEMENUROW_OFF`, +0.0058pp) and "
            "**r410** (build 260619.81, the WJFUN tile-page dialect, `TILEPAGE_OFF`, 53.680 → 53.789 %, ≥50 +8). **Corpus = r415** (2555 pages / 494 dirs / 2349 pairs; "
            "`gate_baseline.json` at r415; `outputs/_s29_r415_sk_final.json` the skeleton state; ceiling 90.9 % → 53.911 = **59.3 % of achievable**).")
q = idx("- Plateau window (§4): **0 of 3**")
lines[q] = "- Plateau window (§4): **0 of 3** — r414 RESET it (+0.0696pp); r415 +0.0246pp (above the 0.02 threshold, ≥50 +3). Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.85")
lines[r] = lines[r].replace("AppVersion 260619.85 (r414, session 29 Round 5, 20 Sept); before it 260619.84 (r413)", "AppVersion 260619.86 (r415, session 29 Round 6, 20 Sept); before it 260619.85 (r414) / 260619.84 (r413)")
assert "260619.86" in lines[r]
t = idx("- s29-r5 (engine r414")
lines.insert(t + 1, "- s29-r6 (engine r415, build 260619.86, 20 Sept ≈18:45 → 20:10) · THE OWNED HEADING-LED BUNDLE WITH NO TABLE — a writer-owned (real `[Activity N]` opener) or r92 embedded-id (`[Activity 1A] [Dropdown Quiz – Auto Check]`) typed-widget invocation whose member walk ended at once on the writer's `[H3]`, the quiz written as PARAGRAPHS after it (WJFUN307 / 210 / 211, ENGJ403, ENFUN03, ENGS404, TEFUN05, SCES201, HIS1002, MXFU302): r413 took the heading + prose only when a TABLE followed, so the box shipped EMPTY (the `no content captured` flag) and the section free after it; found through the empty-box census (`_s29_r6_emptybox.py`: Claude 96 EMPTY writer-owned boxes on 73 pages / 47 modules — the gold's same-numbered box holds text 39 / media 21 = 0.63) + the r4 owned-walk census's no-table rows; the gold check over all 125 heading-led no-table bundles a TIE (0.46, split by family — the UNOWNED half 0.41 stays free), the OWNED half decided by the gate's own scorer (24 up / 2 down / 8 same, +57.7pp-sum; without WJFUN 16 / 2 +36.6 — holds outside the intake family) · `heading_table_owner.owned_bundles.no_table {enabled, env NOTABLEOWNED_OFF}` — the table look-ahead finding none, an owned bundle takes the heading as its first lead item and the walk resumes right after it · SHIPPED · probe OFF = disk 2555 / 2555, ON 35 pages / 22 modules · SCOPED regen of the 22 (scoped #7 since the 19 Sept FULL — THE NEXT SHIP IS THE FULL BACKSTOP; 0 truly stale; spot-check 12 / 12) · scoped_ship FAILED on cs exact −6 alone → decomposed (pool −13, all inside the set — the relocation class) → accepted by name · skeleton 53.886 → 53.911 (+0.0246pp), ≥50 +3, ≥75 238, ≥90 20; cs MISSING 690 → 683, body runaway 6 → 5; all else EXACT · miner 181 → 181 · plateau 0 of 3 · recorded: the unowned no-table shape (0.41), DIFF_QUEUE #3677 (the gold's `col-12 col-md-8` single column ≥ 0.78 — an alignment artefact), #587 / #606 (the `interactive` flag tracks the widget the box holds; 446 gold-interactive / Claude-plain boxes hold NO widget = a capture class), the after-widget row break (0.63 vs 0.57 — a tie), the footer rows #441–443 (page-count artefacts), the 133 commented-out gold menus, CHI1003 / 1004 / 1005's `Merge item N` lessons (the r300 zero class)")
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with io.open(ARCH, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n## Session 29 — Round 6 PICK (engine r415) + what shipped — THE OWNED HEADING-LED BUNDLE WITH NO TABLE (20 Sept ≈18:45 → 20:10 NZST)\n\n" + "\n".join(pick).rstrip("\n") + "\n" + shipped + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
