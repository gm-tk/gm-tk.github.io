#!/usr/bin/env python3
"""Session 26 Round 3 (r389) — write the PICK section into LOOP_STATE.md (before the code, per §3). Idempotent; LF preserved."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md")
s = io.open(LS, encoding="utf-8", newline="").read()
if "## Session 26 — Round 3 PICK (engine r389)" in s:
    print("already"); sys.exit(0)
PICK = """## Session 26 — Round 3 PICK (engine r389): the BUILT FLIPCARD GROUP closes its column — the prose after `div.flipCardsContainer.row` opens a new row
- **The instrument:** the r388 paired row-break census, direction B (Claude FLOWS after block X; does the gold break?) cut by the FULL signature of the `div` kind (`outputs/_s26_r389_divpair.py` → `.out`): **after a built flipCard group the gold BREAKS 23 / flows 5 = 0.82 (26 pages / 20 modules; the text after it always a `p`)** — Standard: English 3 / 0, ConnectED 6 / 0, Online Safety 8 / 2 = 0.80, Leaving to Learn 3 / 2 = 0.60 (n = 5, at the floor); Inquiry 2 / 1 (under the floor). The other `div` kinds are singletons (ratio / TKmodal / shapeHover). The WIDGET kind (every OTHER built widget, collapsed by the reader) is a tie at 0.55 — the flipCard group is the one built widget whose after-rule the gold breaks.
- **The gold's own form (`_s26_r389_flipgold.py` → `.out`, every top-level gold flipCardsContainer, 187 / 146 pages / 83 modules Standard):** position in its column `only` 82 / `last` 58 / `middle` 45 / `first` 2 → LAST-or-only 0.75 (the after-break); FIRST-or-only 0.45 = a TIE → the break BEFORE the group is NOT taken (Claude keeps the preceding prose in the same column; ConnectED 21 / 28 `only` is the one family that isolates it, NCEA1 5 / 7 — recorded). Column class col-md-8 118 / col-md-12 58 → Claude's col-md-8 stays. Per subject after-share (only + last): English 0.87, Mathematics 0.93, ConnectED 0.82, OS 0.82, NCEA1 0.71, ANZH 0.33 (n = 6), **Leaving to Learn 0.32 (19 / 28 `middle`)** — LtL's paired 0.60 on 5 boundaries disagrees with its gold-side 0.32 → the probe's per-subject score decides LtL.
- **KB-first check:** 03A / 05D give the flipCard build (`row.flipCardsContainer > col > flipCard`); nothing on the section row after the group → §1b level 3 / 4. Structure-only → derivable.
- **Fix (DATA OVER CODE):** `body_region.row_breaks.after_built_widgets {enabled, env: FLIPBREAK_OFF, rules: [{class_match: \\\\bflipCardsContainer\\\\b, templates: [Standard], exclude_subjects: []}]}`; at the INLINE widget site (`emit(this.#interactivePlaceholder(...))` — a top-level widget, `!stack.length`) the built html's open tag is tested against the rule and `breakRow()` follows the group. The r51 `flow_blocks` rule is otherwise untouched (the WIDGET kind is a tie); the bundle-owned site (inside an activity box) never breaks. Regeneration: SCOPED (the probe's ON list) = scoped ship #1 since the r388 full.
- **Not taken:** the break BEFORE the group (0.45, a tie); the col-md-12 width (0.31); the other built widgets (WIDGET 0.55).

"""
anchor = "## Round log\n"
i = s.index(anchor)
s = s[:i] + PICK + s[i:]
io.open(LS, "w", encoding="utf-8", newline="").write(s)
print("PICK written", len(s))
