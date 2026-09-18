#!/usr/bin/env python3
"""Session 26 Round 2 (r388) — LOOP_STATE.md: archive the Round 2 PICK (+ what shipped) to LOOP_STATE_ARCHIVE.md, add the
Round-log line, update the Position block. LF preserved; idempotent. Run from anywhere (python3 on either side)."""
import io, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)

s = rd(LS)
if "s26-r2 (engine r388)" in s:
    print("already applied"); sys.exit(0)

# 1. archive the PICK section
h = "## Session 26 — Round 2 PICK (engine r388)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r388, build 260619.59, 19 Sept ≈01:05 NZST):** data `callouts.flow_after_tags.rules` (rule 1 = r387 verbatim; rule 2 = "
           "`{tags: [alert, important], templates: [Standard], exclude_class_match: \\btop\\b, env: ALERTFLOW_OFF}`) + `ContentConverter.#flowsAfter(tag, run, boxOpen)` "
           "(the rules walk, the box's own open tag at both after-box breakRow sites, the per-rule env) — `_s26_r388_splice.py` + `_s26_r388_ruleenv.py`. Probe OFF "
           "(`WHFLOW_OFF`) = the r386 bytes + exactly the 63 r387 pages (the family env reverts both rules); ON 323 pages / 138 modules; scored before the regen: 298 "
           "paired 244 up / 54 down, pp-sum +117.3 (the dips = the 0.26 gold-BREAK minority, named). FULL regeneration of all 416 (the ledger's backstop, 36 batches "
           "rc 0 in 5 min; 0 stale; manifest diff = the probe's 323 pages / 138 modules, 0 added / removed — NO residue from r378–r387; probe ON == disk 1027 / 1027). "
           "Skeleton 53.395 → 53.455 (+0.060pp = the prediction), ≥50 1152 → 1155, ≥75 189 → 192, ≥90 15, RAW 37.688 → 37.719, 1956 pairs / 0 skipped / 0 movers "
           "outside the affected set; compare_structure 11643 / 172 / 625, body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — all EXACT; every "
           "verifier RESULT line identical to r387; 15 selftests + the skeleton selftest GREEN; fast-loop / manifest / feature index refreshed; ledger FULL (counter "
           "0); the miner re-mined 178 CANDIDATE rows (179 → 178, 0 new — the `activity › row > col-12 › WIDGET` row under the floor); checksums refreshed (engine "
           "3 changed); finalise = changelog entry `_s26_r388_entry.md`, AppVersion 260619.59, CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.\n")
a = rd(AR)
if "## Session 26 — Round 2 PICK (engine r388) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 26 — Round 2 PICK (engine r388) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈01:05 NZST, session 26)\n" + pick + shipped
    wr(AR, a)
stub = ("## Session 26 — Round 2 (engine r388) SHIPPED — its PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md ('Session 26 — Round 2 PICK (engine r388) + "
        "what shipped'); the one-line summary is in the Round log below.\n")
s = s[:i] + stub + s[j:]

# 2. the Round-log line (≤ 500 chars)
line = ("- s26-r2 (engine r388) · THE PLAIN / SOLID ALERT DOES NOT CLOSE ITS COLUMN EITHER — prose after `div.alert` / `div.alert.solid` flows on in the same "
        "col-md-8 (paired census `_s26_rowpair.py`: gold flows 0.74 / 0.74, every Standard group ≥ 0.64; `top` excluded); data `flow_after_tags.rules`, "
        "env `ALERTFLOW_OFF` · SHIPPED 19 Sept 01:05 · ON 323 pp / 138 mods (244 up / 54 down, +117.3); FULL regen (ledger 0, no residue) · skeleton "
        "53.395→53.455 (+0.060), ≥50 +3, ≥75 +3; all else EXACT · build 260619.59\n")
assert len(line) <= 505, len(line)
anchor = "- s26-r1 (engine r387)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]

# 3. Position
old = s[s.index("- LAST SHIPPED: **r387**"):]
old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r388** (build 260619.59, 19 Sept ≈01:05, session 26 Round 2 — the plain / solid alert does not close its column either; r387 the whakataukī; "
       "r386 the skeleton label's class-token order; r385 the panel's first own heading is h2; r384 declined inert; r383 the long first row is a data row; r382 the "
       "reader's shared `body_source`; r381 the reverse trio; r380 / r379 the mode-opener boxes; r378 the post-table body; r377 the `[Hn] Activity <id>` heading "
       "opener) — **FULL regeneration of all 416 (the ledger's backstop: scoped counter 0, 8 of headroom; the manifest diff was exactly the probe's 323 pages — the "
       "seven scoped ships r378–r387 left NO residue)**. **Corpus = r388** (2109 pages / 416 modules). Gates at r388 (`gate_baseline.json`): skeleton **53.455 %** / "
       "≥50 **1155** / ≥75 **192** / ≥90 **15** @ 1956 pairs; RAW 37.719 %; compare_structure exact 11643 (EXTRA 172 / MISSING 625 / row-wrap 23); body_compare "
       "218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.2 % of achievable. `DIFF_QUEUE.md` "
       "re-mined 19 Sept ≈00:57 on the r388 corpus (`_diff_miner_s26_r388.log`: 1956 pairs / 8154 classes / **CANDIDATE 178** — 179 → 178, 0 new, the "
       "`activity › row > col-12 › WIDGET` SUBSTITUTED row fell under the 20-page floor; `_s26_r388_queue_delta.log`; the pre-r388 queue kept at "
       "`_diff_queue_pre_r388.md`); every disposition stands.\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **0 of 3** (r388 +0.060pp, ≥50 +3, ≥75 +3 — not a plateau round; r387 +0.043pp / ≥75 +4; r385 +0.015pp but ≥50 +1 moved; r383 "
       "+0.031pp / ≥75 +1; r382 / r386 instrument re-baselines, r384 declined inert — not plateau rounds).\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.58;", "- Standing facts: AppVersion 260619.59;", 1)
s = s.replace("`DIFF_QUEUE.md` 18 Sept 19:07 on the r385 corpus, 179 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈00:57 on the r388 corpus, 178 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s), "bytes; archive:", len(a), "bytes")
