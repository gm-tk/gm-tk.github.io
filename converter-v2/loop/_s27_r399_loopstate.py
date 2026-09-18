#!/usr/bin/env python3
"""Session 27 Round 2 (r399) — LOOP_STATE.md: archive the Round 2 PICK (+ what shipped), the Round-log line, the Position block,
the IN PROGRESS line removed, the Round-2 declines recorded. LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r2 (engine r399)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 27 — Round 2 PICK (engine r399)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r399, build 260619.70, 19 Sept ≈10:45 NZST):** data `callouts.by_tag.wananga.kb_form {enabled, env WANANGA_OFF, open '<div class=\"alert cultural\" "
           "layout=\"combined\">', close, wrap_content}` + `callouts.by_tag.wananga.table_cell_content {enabled, env}` + the `Tag_Lexicon._meta.tag_promote` rule carousel → wananga "
           "on the `[Banner - Wānanga…` spelling (`clear_remainder` — the promoted tag's leftover '/ box' had surfaced as a spurious Writers Note, caught on the probe; "
           "`[Rolling Banner - …]` excluded); engine `ContentConverter.#calloutOpen` (the kb_form def swap; STRICT mode: an empty gather + a next one-row one-cell table → the cell "
           "through `TablesAndGrids.renderCellParts`, the table `_consumed`) + the new `#calloutTableCell` helper consulted first by `#calloutWrapsStructured`; Config 260619.70. "
           "Probe OFF (`WANANGA_OFF=1`) 2109 / 2109 byte-identical; ON 47 pages / 6 modules (CEDK501 7, CEDO501 7, CEDO502 8, CEDR501 6, CEDT501 13, CEDW501 6), 0 outside — the "
           "rotateBanner family untouched. Scored on the gate's own match() before regenerating: 39 up / 5 down / 3 same, pp-sum +200.8; the dips named — CEDT501_7_0 −4.4 (the gold's "
           "flow-after minority, 15 / 74), CEDT501_2_0 −1.9 (the gold's box-inside-the-activity minority, 2 / 74 — the CONTAINER_OPEN auto-close class), CEDT501_5_0 −1.4, "
           "CEDW501_2_1 −0.5, CEDT501_6_0 −0.3. SCOPED regeneration of the 6 (rc 0; `fresh --affected` 0 truly stale; probe ON == disk 79 / 79). Skeleton 53.759 → 53.862 (+0.103pp), "
           "≥50 1166 → 1170, ≥75 195 → 197, ≥90 18, RAW 37.846 → 37.918, 1956 pairs / 0 skipped / 44 movers 39 up / 5 down / 0 outside; compare_structure exact 11723 → 11798 (+75), "
           "EXTRA 172 / MISSING 626 EXACT; body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 EXACT; every verifier RESULT identical to r398; 15 selftests + the index "
           "selftest GREEN; fast-loop / manifest / feature index refreshed; ledger scoped #3 since the r396 full; the miner re-mined 173 CANDIDATE rows (one new at the floor: #3698 "
           "`body EXTRA div.col-12.col-md-6 › p` 20 pages / 13 modules — English 6 / OS 5 / CED 2, a Claude paragraph in a col-md-6 the gold has no line for, crossed the floor by the two "
           "CED pages this round re-aligned; measure before taking); checksums refreshed (engine 5 changed, gates 0); finalise = changelog entry `_s27_r399_entry.md`, AppVersion 260619.70, "
           "CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md. Plateau window RESET (r399 +0.103pp, ≥50 +4, ≥75 +2).\n")
a = rd(AR)
if "## Session 27 — Round 2 PICK (engine r399) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 27 — Round 2 PICK (engine r399) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈10:45 NZST, session 27)\n" + pick + shipped
    wr(AR, a)
s = s[:i] + s[j + 1:]
# the Round-log line
line = ("- s27-r2 (engine r399) · THE WĀNANGA / TALANOA BOX IS THE KB'S CULTURAL ALERT (`[Wānanga/Talanoa box]` + a one-cell table → `div.alert.cultural[layout=combined] > row > col-12 > p…`, "
        "KB 05B + 14A §14.4; `callouts.by_tag.wananga.kb_form` + `table_cell_content`, the `tag_promote` carousel→wananga rule for CEDT501's `[Banner - …]`, env `WANANGA_OFF`; found by the "
        "paired callout-class census `_s27_r2_alertclass.py`) · SHIPPED 19 Sept · ON 47 pp / 6 mods (39 up / 5 down, +200.8); SCOPED (#3 since r396) · skeleton 53.759→53.862 (+0.103), "
        "≥50 +4, ≥75 +2; cs exact +75; all else EXACT · plateau RESET · build 260619.70\n")
assert len(line) <= 800, len(line)
anchor = "- s27-r1 (engine r398)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
# Position
old = s[s.index("- LAST SHIPPED: **r398**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r399** (build 260619.70, 19 Sept ≈10:45, session 27 Round 2 — the wānanga / talanoa box is the KB's cultural alert; r398 the videoSection `icon` registry "
       "re-mined + the widget-embedded video; r397 a table header cell is plain; r396 the captioned carousel video slide is `item video` (the FULL backstop); r395 the flip-card column "
       "width; r394 the clickDrop buttons in the column; r393 the glyph-only line; r392 adjacent lists; r391 the LtL panel column; r390 the supervisor closer; r389 the flipCard group "
       "closes its column; r388 the plain / solid alert (the previous FULL); r387 the whakataukī; r386 / r382 instrument corrections; r385–r377 session 24) — SCOPED regeneration of "
       "6 modules (the ledger at scoped #3 since the r396 FULL, 5 of headroom). **Corpus = r399** (2109 pages / 416 modules). Gates at r399 (`gate_baseline.json`): skeleton "
       "**53.862 %** / ≥50 **1170** / ≥75 **197** / ≥90 **18** @ 1956 pairs; RAW 37.918 %; compare_structure exact **11798** (EXTRA 172 / MISSING 626 / row-wrap 23); body_compare "
       "218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.6 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept "
       "≈10:45 on the r399 corpus (`_diff_miner_s27_r399.log`: 1956 pairs / **CANDIDATE 173**; `_s27_r399_queue_delta.log`; the pre-r399 queue kept at `_diff_queue_pre_r399.md`): "
       "one new row #3698 (`body EXTRA div.col-12.col-md-6 › p`, 20 pages / 13 modules at the floor — an alignment residue crossing the floor by this round's two CED pages; measure "
       "before taking); every other disposition stands.\n")
s = s.replace(old, new, 1)
old = s[s.index("- IN PROGRESS (session 27 Round 2"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, "", 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **0 of 3** — RESET by r399 (+0.103pp, ≥50 +4, ≥75 +2; r398 +0.064pp before it).\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.69 (session 27 in progress);", "- Standing facts: AppVersion 260619.70 (session 27 in progress);", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈09:55 on the r398 corpus, 172 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈10:45 on the r399 corpus, 173 candidates, all dispositioned)", 1)
# the Round-2 PICK-pass declines → Declined classes (one entry)
dh = "## Declined classes\n"
di = s.index(dh) + len(dh)
di = s.index("\n", di) + 1   # after the condense note line
decl = ("- **Session 27 Round 2 PICK pass (19 Sept ≈10:00, the classes measured before the wānanga box was taken; each probe in `CONVERTER_V2/outputs/`):** (1) the gold's `<br>` "
        "(gold 2169 skeleton lines / Claude 3; `_s27_r2_brcensus.py`): 3913 br records on 701 gold pages; paired to Claude: absent 1480 / SPLIT-P 872 / reworded 359 / ONE-P 264 — the "
        "writer-side soft-break form is split 0.40 / br 0.26 / spaced 0.33 overall (the r357 decline stands) but PER PREFIX ENGJ br 0.97 (n = 62), HIS br 0.65 (n = 20), EXPFUN "
        "space-joined 0.99 (n = 187), everyone else split — each family under the 20-page floor alone; a per-prefix soft-break-form registry (≈ 25 pages, est. +0.03pp) is a FOLLOW-UP "
        "candidate, not taken. (2) `div.col-12.col-md-12` (gold 1865 columns / 774 pages; `_s27_r2_col12.py`): DIFFUSE — no content kind ≥ 0.60 at the floor (activity.interactive 0.12, "
        "h3 0.02, dragAndDrop 0.49 vs col-12 0.42, whakatauki 0.42; only tiny built-widget wrappers dropQuiz 0.68 n = 38 / rotateBanner 0.80 n = 25 / radioQuiz 0.75 n = 16) → the r334 "
        "widened-wrapper decline stands. (3) the un-numbered `div.activity` (Claude 533 / gold 6; miner #605; `_s27_r2_acttail.py` / `_acttail2.py`): the derivable sub-class — a bare "
        "`[Activity]` opener whose tail carries `Activity 4B: Title` / `4B: Title` — is 19 sites / 8 modules / 13 gold pages (gold numbered + h3 = remainder 11, a different h3 6, no "
        "box 2; Claude numberless 8) → BELOW FLOOR; the rest is gold-invented numbering (AGH1005 / AGH1008 `[Activity: Embedded]`, no id or title — the standing needs-Chris provenance "
        "item). (4) the paired callout-class census (`_s27_r2_alertclass.py`) beyond the wānanga box: Claude `alert solid` where the gold is plain `alert` — ConnectED 19 / 23 = 0.83, "
        "English 8 / 13 = 0.62 (78 boxes / 63 pages / 39 modules overall; NCEA1 0.40 and Maths 0.36 ties); Claude `alert solid` where the gold is `alertActivity` — Inquiry / BLL 19 / 24 "
        "= 0.79; Claude `alert` where the gold is `alertActivity` (46 pp / 29 mods) or `alert top` (33 pp / 23 mods): the writer-tag decomposition of these `[important]` / `[alert]` "
        "class swaps is the NEXT candidate (a `solid` → plain registry by subject group, ≥ 20 pages in ConnectED alone).\n")
if "Session 27 Round 2 PICK pass" not in s:
    s = s[:di] + decl + s[di:]
wr(LS, s)
print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes; archive:", len(a.encode("utf-8")), "bytes")
