#!/usr/bin/env python3
"""Session 26 Round 4 (r390) — LOOP_STATE.md: archive the Round 4 PICK (+ what shipped), the Round-log line, the Position block.
LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s26-r4 (engine r390)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 26 — Round 4 PICK (engine r390)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r390, build 260619.61, 19 Sept ≈02:05 NZST):** data `callouts.by_tag.\"supervisor note\".explicit_close_span {enabled, env "
           "SUPSPAN_OFF, stop_at_activity}` + `#explicitCloseAhead(bodyItems, i, tag, opts)` (opts.promotedClosers = a tag_promote source's closer counts, "
           "opts.stopAtActivity) + the own_row branch's SPAN path (stack mode `span-own`, `ownSpanClose`: emit() opens no content row meanwhile and pushes the "
           "close directly; autoClose treats it as a writer's span) — `_s26_r390_splice.py` + `_s26_r390_splice2.py`. THE PROBE'S OFF LEG CAUGHT A LEAK: the "
           "first cut added the promoted closers for every caller and EXIP901_2_0 / SCFUN01_0_0 moved under SUPSPAN_OFF (`end alert` began closing a "
           "`side alert` span, `end shape n` an `interactive` one) → re-gated to the own-row call; OFF 2109 / 2109. ON 21 pages / 3 modules (XDLS904 / 905 / "
           "906 — XDLS502 / 901's `[end supervisor note]` is typed in black, no tag); scored before the regen: 21 up / 0 down, pp-sum +92.5 (XDLS905_7_0 "
           "+19.7). SCOPED regeneration of the 3 (1 batch rc 0; `fresh --affected` 0 truly stale; manifest diff = 21 pages / 3 modules; probe ON == disk 24 / "
           "24). Skeleton 53.470 → 53.518 (+0.047pp = the prediction), ≥50 1157 / ≥75 191 / ≥90 15 EXACT, RAW 37.725 → 37.756, 1956 pairs / 0 skipped / 0 "
           "movers outside; **compare_structure exact 11643 → 11700 (+57 IMPROVED)**, EXTRA 172 / MISSING 625, body_compare 42 / 4 / 173 / 218, clean 2079 / "
           "2102, leak 26 / 23 — all EXACT; every verifier RESULT identical to r389; 15 selftests + the skeleton selftest GREEN; fast-loop / manifest / feature "
           "index refreshed; ledger scoped #2 since the r388 full; the miner re-mined 178 CANDIDATE rows (177 → 178: the new #3735 `body EXTRA div.col-12 › "
           "ul` = the panel text column's class, gold `col-12 col-md-12` in Leaving to Learn 35 / 46 = 0.76 (`_s26_r391_panelcol.out`) — the Round 5 "
           "candidate); checksums refreshed (engine 3 changed); finalise = changelog entry `_s26_r390_entry.md`, AppVersion 260619.61, CLAUDE.md §9 / §11 / "
           "§14, gate_baseline.json (skeleton + compare_structure exact_chain 11700), loop/README.md.\n")
a = rd(AR)
if "## Session 26 — Round 4 PICK (engine r390) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 26 — Round 4 PICK (engine r390) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈02:05 NZST, session 26)\n" + pick + shipped
    wr(AR, a)
stub = ("## Session 26 — Round 4 (engine r390) SHIPPED — its PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md ('Session 26 — Round 4 PICK (engine r390) + "
        "what shipped'); the one-line summary is in the Round log below.\n")
s = s[:i] + stub + s[j:]
line = ("- s26-r4 (engine r390) · THE SUPERVISOR NOTE'S EXPLICIT CLOSER MAKES THE PANEL A SPAN — `[Supervisor Button] … [End Supervisor button]` holds "
        "everything between (LtL paired 22 / 0; XDLS904 / 905 / 906, 21 pairs; other families agree with the strict panel); data `explicit_close_span`, "
        "env `SUPSPAN_OFF` (the OFF leg caught a closer leak → re-gated) · SHIPPED 19 Sept · ON 21 pp / 3 mods (21 up / 0 down, +92.5); SCOPED "
        "(#2 since r388) · skeleton 53.470→53.518 (+0.047), buckets EXACT; cs exact +57 · build 260619.61\n")
assert len(line) <= 520, len(line)
anchor = "- s26-r3 (engine r389)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- LAST SHIPPED: **r389**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r390** (build 260619.61, 19 Sept ≈02:05, session 26 Round 4 — the supervisor note's explicit closer makes the panel a span; r389 the "
       "built flipCard group closes its column; r388 the plain / solid alert (the FULL backstop); r387 the whakataukī; r386 the skeleton label's class-token "
       "order; r385 the panel's first own heading is h2; r384 declined inert; r383 the long first row is a data row; r382 the reader's shared `body_source`; "
       "r381 the reverse trio; r380 / r379 the mode-opener boxes; r378 the post-table body; r377 the `[Hn] Activity <id>` heading opener) — SCOPED regeneration "
       "of the 3 XDLS90x modules (the ledger at scoped #2 since the r388 FULL, 6 of headroom). **Corpus = r390** (2109 pages / 416 modules). Gates at r390 "
       "(`gate_baseline.json`): skeleton **53.518 %** / ≥50 **1157** / ≥75 **191** / ≥90 **15** @ 1956 pairs; RAW 37.756 %; compare_structure exact **11700** "
       "(EXTRA 172 / MISSING 625 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget verifier at its recorded "
       "baseline. Ceiling 91.9 % → 58.3 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈02:00 on the r390 corpus (`_diff_miner_s26_r390.log`: 1956 pairs / "
       "8141 classes / **CANDIDATE 178** — 177 → 178, ONE new: #3735 `body EXTRA div.col-12 › ul` (32 pages / 14 modules, LtL 26) = the supervisor panel's "
       "text-column CLASS, gold `col-12 col-md-12` in Leaving to Learn 35 / 46 = 0.76 (`_s26_r391_panelcol.out`) — DISPOSITION: the Round 5 PICK; "
       "`_s26_r390_queue_delta.log`; the pre-r390 queue kept at `_diff_queue_pre_r390.md`); every other disposition stands.\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **0 of 3** (r390 +0.047pp / cs exact +57; r389 +0.016pp with ≥50 +2 / ≥75 −1 — not a plateau round under §4's two conditions; "
       "r388 +0.060pp; r387 +0.043pp).\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.60;", "- Standing facts: AppVersion 260619.61;", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈01:27 on the r389 corpus, 177 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈02:00 on the r390 corpus, 178 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s), "bytes; archive:", len(a), "bytes")
