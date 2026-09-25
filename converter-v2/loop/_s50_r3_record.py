#!/usr/bin/env python3
"""Session 50 Round 3 record (WSL): r512 DECLINED on measurement + the PICK pass. Clears the r512 in-flight marker (archived
verbatim), adds the ride-along patch, a Declined-classes entry, the follow-up bullet and the Round-log line."""
import io, os, subprocess, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
T = subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()
s = io.open(S, encoding="utf-8", newline="").read()
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s50-r3.bak"))
L = s.split("\n")
fl = [i for i, l in enumerate(L) if l.startswith("- **ROUND 512 IN FLIGHT — NOT PROVEN**")]
assert len(fl) == 1, fl
marker = L[fl[0]]
del L[fl[0]]
nr = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (26 Sept 2026")]
assert len(nr) == 1, nr
old = "Checked at r511 (MXDB302 only): none rides."
assert L[nr[0]].count(old) == 1
L[nr[0]] = L[nr[0]].replace(old, old + " **+ `_r512_declined.patch`** (the `[Activity: Embedded] <widget>` bracket, r510's class — "
    "10 modules: AGH1007, ANZH104, TRR102 / 109 / 110 / 111 / 112 / 113 / 116 / 301; it rides only with a round that first keeps a "
    f"bilingual TRR table-dialect widget INSIDE its numbered activity box — s50-r3, {T}).")
dc = [i for i, l in enumerate(L) if l.startswith("## Declined classes")]
assert len(dc) == 1
L.insert(dc[0] + 1, (
    f"- **Session 50 Round 3 (26 Sept ≈01:22 → {T}) — a PICK pass, then engine r512 BUILT, PROBED and DECLINED on measurement.** "
    "(1) **r512 — the `[Activity: Embedded] Drag and Drop` bracket names its widget too** (r510's class, KB c14; data "
    "`embedded_bracket_pattern`, env `IQEMBED_OFF`): probe OFF 0 / ON **10 modules**; scoped_ship FAILED — skeleton −0.03pp, ≥50 −5, "
    "cs exact −82 (31 movers: 15 up / 16 down, −79.8pp-sum). The losses are the bilingual TRR table-cell dialect: once the span's "
    "widget is recognised the widget is built OUTSIDE its numbered activity box (the reo row number, not a writer id) and the box "
    "keeps only its title (TRR116_3_0 58.8 → 33.3, five TRR116 pages fall below 50 %), while TRR112 / 113 / 110 pages rise; outside "
    "TRR only AGH1007 / ANZH104 change — under the floor. Backed out (`git apply -R`), saved as the ride-along patch "
    "`outputs/_r512_declined.patch`; the 10 modules regenerated → `_content_manifest.py diff` 0 pages; the failed run's ledger record "
    "removed (`_s50_r512_ledger_fix.py`, scoped_since 7 → 6). **Re-open only with the TRR table-dialect ownership fixed first.** "
    "(2) **reorder** (the dashboard's largest no-builder type, 115 bundles / 67 modules; `_s50_wdump.cjs` → `_s50_reorder_dump.log`): "
    "the writer STATES the correct order on only 20 bundles, across four renderers (sentence / image lists ≈ 15, two-column matches ≈ 5) — "
    "every shape under the 20-site floor; the other 95 give no order to trust (never invent). Recorded. (3) **The unclassified activity "
    "table** (`_s50_r3_unclasstable.py`, 511 paired pages whose unclassified box holds a table): the gold renders it as a plain table on "
    "61 = 12 % (absent 223, built widgets 135+) — boxing it is right; DECLINED. (4) **Flip-card text defects** (`_verify_flipcard.cjs` over "
    "every module: 2,409 card texts, exact 1,399, unmatched 387) — diffuse (rewritten wording, media labels, ≈ 13 face labels, stray "
    "designer notes); recorded. (5) The loss ledger (45.86pp; wrapper-empty 6.94 / chrome 5.17 / alignment 5.13) — its form rows are the "
    "recorded KB overrides (`videoSection.icon`, `iframe.embed-responsive-item`). (6) The placement census (SAME 40.4 % / MOVED 22.2 %) — "
    "its CANDIDATE rows are the declined class-C lanes."))
fu = [i for i, l in enumerate(L) if l.startswith("## Follow-up candidates surfaced by Round 1")]
assert len(fu) == 1
L.insert(fu[0] + 1, (
    "- **(s50) recorded, each below the floor or blocked on a prior fix:** the D15-19 dropDown yellow residue (`_s50_r511_ddyellow.cjs`: 27 "
    "yellow-marked bundles — 4 built; the TABLE forms ≈ 12 (ENFUN03 / 08, ENGC201, ENGI303, ENGI401, ENGR302 3C, ENGS202, FRFUN07 / 08, "
    "MXFU202, OSAH501, OSAI501 — each a different layout), numbered / lettered option LINES 3 (ENFUN02, ENGR302 5B, ENGS301), a "
    "highlighted word with no options 3 (HES1002 ×2, CEDR401 — never invented)); the ANNOUNCED yet unbuilt SCCH301 #27 / SCES201 ×2; "
    "reorder by shape (stated-order lists ≈ 15, two-column matches ≈ 5, word-level with a `[correct]` sentence ≈ 6, jumbled with no "
    "order ≈ 90); `[Activity: Embedded] <widget>` (r512 — needs the TRR table-dialect ownership fix); the remaining generic-bracket spans "
    "(`_s49_r11_unknownquiz.cjs`: 358 unresolved red brackets / 143 modules — the D2L `[add button] quiz` and dev notes by design, "
    "`[flip]` face labels inside flip tables 9 + 5 + 3 + 2)."))
rl = [i for i, l in enumerate(L) if l.startswith("## Round log")]
assert len(rl) == 1
L.insert(rl[0] + 1, (f"- s50-r3 (engine r512, 26 Sept ≈01:22 → {T}) · a PICK pass (reorder, the unclassified table, flip-card text, "
    "the ledger, the census, the recognition census) then `[Activity: Embedded] <widget>` (r510's class) · DECLINED on measurement "
    "(TRR table-dialect ownership: skeleton −0.03pp, cs exact −82), backed out, patch parked, corpus restored (0 pages differ) · "
    "plateau 0 of 3 (neither)."))
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Session 50 — r512 PICK (the in-flight marker, verbatim) — DECLINED\n\n" + marker + "\n")
out = "\n".join(L)
tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(out); os.replace(tmp, S)
print("LOOP_STATE", len(s.encode()), "->", os.path.getsize(S))
