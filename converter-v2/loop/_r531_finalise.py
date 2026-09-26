#!/usr/bin/env python3
"""ROUND 531 finalise (session 52 Round 5 — the bracket fragment in a button label). WSL. argv: MEAN RAW."""
import sys
import _s52_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 531, build 260620.90) — THE BRACKET FRAGMENT IN A BUTTON LABEL: a writer's bracket fragment no longer reaches a button's label (`Add button] Download journal` → `Download journal`, `Upload to dropbox  [trigger engagement]` → `Upload to dropbox`, `go to quiz]` → `go to quiz`); KB constraint 5; 26 modules / 27 pages, text-only — every gate held by design

### 1. WHAT CHANGED

**The class** (found on ANZH301 while measuring the placement census's ORDER lane — `_s52_r5_jtail.py`, the journal button ends the activity box? a page-level TIE, 40 : 40, declined): 35 `div.button` labels on ≈ 26 pages carried a writer's bracket fragment — a split tag's tail (`Add button] Download journal`, `Button] [Download Journal`, `insert button] Download file [`), a writer note (`Upload to dropbox  [trigger engagement]`, `Lesson 5: Beyond the Basics [Not applicable]`), an unclosed note (`Download journal button] [Media item 31 -`), an orphan bracket (`Go back to [`, `go to quiz]`, `Access activities here]`). The download-button path stripped only the outer brackets of the tag text (`[Add button] Download journal.` → `Add button] Download journal`). The gold labels are clean (`Download journal`, `Go to quiz`, `Video Mode`, `Upload to dropbox`). KB constraint 5 (level 1).

**The fix** (`ContentConverter.#buttonLabelBrackets`, at the common button emit just before `#buttonLabelTrim`; data `buttons.label_bracket_clean` {{keep_pattern, note_pattern, button_words_pattern}}, env **`BTNBRACKET_OFF`**): complete bracket notes go (a short caps token like a video title's `[HD]` stays); the text after a split tag's `…]` wins when it has letters, else the text before it without the button words (`(Audio Button]` → `Audio`, `Button title: Dative forms]` → `Dative forms`); an unclosed trailing note goes; any other stray bracket goes; nothing left = the label unchanged. MXFU202's `Dropbox [` now reaches r328's canonical `Go to dropbox`. Not reached (other builders, recorded): WJFUN306's click-drop `] Video Mode`, DAN1003's external `journal]`.

### 2. PROOF

- In-memory probe over all 545 modules: `BTNBRACKET_OFF=1` → 6,432 / 6,432 pages identical; ON → **27 pages / 26 modules**, every changed line a button label (each before → after read in `_r531_ON_pages`); 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 531 --commit` PASS: 0 stale, containment 26 ⊆ 26, the 12-module spot-check byte-identical.
- Skeleton-blind by design (the gate is text-immune): the skeleton gate's own `match()` moved 0 pages.

### 3. PROTECTED GATES

Skeleton **{MEAN} % @ 2486 (±0.0000pp)**, ≥50 1632 / ≥75 301 / ≥90 28 held; RAW {RAW} %; compare_structure exact 17005 / EXTRA 198 / missing 661 held; body_compare ANY 234 held; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r531_gates.log`); `--gate-baseline-check` PASS. Plateau: **1 of 3** unchanged (a text-only round, skeleton-blind by design: neither).

**Ledger:** scoped #4 since the s51-r12 FULL (r526) · data `buttons.label_bracket_clean` · env `BTNBRACKET_OFF` · code `ContentConverter.#buttonLabelBrackets` · session 52 Round 5.
"""
F.finalise(
    N=531, old_build="260620.89", new_build="260620.90", entry=entry,
    config_comment="THE BRACKET FRAGMENT IN A BUTTON LABEL (session 52 Round 5; KB constraint 5; text-only). Env BTNBRACKET_OFF.",
    og9=None,
    og11="| `BTNBRACKET_OFF` | 531 | **THE BRACKET FRAGMENT IN A BUTTON LABEL** (session 52 Round 5). Reverts `buttons.label_bracket_clean`: a writer's "
         "bracket fragment stays in the button label (`Add button] Download journal`) — the r530 output exactly. |",
    og14=f"- **Build:** `260620.90` (round 531 — **the bracket fragment in a button label**; `BTNBRACKET_OFF`; scoped #4 since the s51-r12 FULL; "
         f"26 modules, text-only; skeleton {MEAN} % held, RAW {RAW} %).",
    gb_note=f"Round 531 (session 52 Round 5, 2026-09-26) — THE BRACKET FRAGMENT IN A BUTTON LABEL (BTNBRACKET_OFF): 26 modules / 27 pages, "
            f"text-only; every gate held by design (skeleton {MEAN}); scoped #4.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 52 Round 5 — r531 (the bracket fragment in a button label) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r531** (260620.90); **LAST FULL = r526 (the session-51 Round 12 "
             "backstop)**; ledger **scoped #4** (4 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / "
             "9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, "
             "XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: "
             "Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect ownership fix) / `_r524_declined.patch` "
             "(the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list after its title). Checked at "
             "r531: none rides — r469b is the button lane but only HIS1002 of its 9 modules lies in r531's 26.",
    last_shipped=f"- LAST SHIPPED: **r531** (build 260620.90, 26 Sept {T}, session 52 Round 5 — THE BRACKET FRAGMENT IN A BUTTON LABEL, "
                 "`BTNBRACKET_OFF`; SCOPED, **scoped #4 since the s51-r12 FULL**; 26 modules / 27 pages, text-only; every gate held by "
                 f"design, skeleton {MEAN} %).",
    before_them_add="r529 the summary heading's alert box",
    plateau="- Plateau window (§4): **1 of 3** — r531 a text-only round, skeleton-blind by design (neither); ",
    standing="- Standing facts: AppVersion **260620.90** (r531 the bracket fragment in a button label — session 52 Round 5, 26 Sept); before it "
             "260620.89 (",
    roundlog=f"- s52-r5 (engine r531, build 260620.90, 26 Sept 17:02 → {T}) · a PICK pass (the placement census ORDER lane: the journal "
             "button ends the activity box? `_s52_r5_jtail.py` — a 40 : 40 page TIE, DECLINED) then THE BRACKET FRAGMENT IN A BUTTON LABEL "
             "(KB c5; 35 labels, `Add button] Download journal` → `Download journal`) · SHIPPED scoped #4 · 26 modules / 27 pages · text-only, "
             "every gate held by design · plateau 1 of 3 (neither).",
    archive_extra="- **What shipped (r531, 260620.90):** `ContentConverter.#buttonLabelBrackets`; data `buttons.label_bracket_clean`. Probe OFF "
                  "6,432 / 6,432 identical; ON 27 pages / 26 modules, every changed line a button label; every gate held.",
)
