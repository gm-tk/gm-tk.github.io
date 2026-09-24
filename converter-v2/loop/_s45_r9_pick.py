#!/usr/bin/env python3
"""Session 45 Round 9 — write the PICK (engine r490) + the in-flight marker in LOOP_STATE.md (§3 step 1, BEFORE any code). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r490-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈07:25, session 45 Round 5")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 490 IN FLIGHT — NOT PROVEN** (session 45 Round 9, 25 Sept ≈09:15): THE LESSON OVERVIEW'S WALT ALERT IS MENU CONTENT — "
         "an alert / important box inside a lesson's `[Lesson Overview]` block whose text opens with a learning-intentions lead ('In this "
         "lesson you are…') joins the lesson menu as its plain sentence (the r147 section-stop otherwise ends the menu at any alert). Files: "
         "`app/js/ContentConverter.js` (the section-stop `buildSet` + the menu routing), `data/Emit_Templates.json` "
         "`menu.lesson_menu_section_stop.walt_alert` {enabled, env `LOWALTALERT_OFF`}. Affected: HIS1003 / HIS1004 (≈ 20 lesson pages) + any "
         "other module with the shape.")
p = [i for i, l in enumerate(L) if l.startswith("## Session 45 — Round 5 PICK (engine r488)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 45 — Round 9 PICK (engine r490) — THE LESSON OVERVIEW'S WALT ALERT IS MENU CONTENT (IN FLIGHT)",
 "- **Lane:** the §1g placement lane, continued from Round 7 (Claude's empty lesson menu vs the gold's — 66 pages / 23 modules with the "
 "gold's menu text in Claude's body). One writer form is a clean, KB-backed rule: `[Lesson Overview] <lesson title>` → `[Alert box] In "
 "this lesson you are reviewing your understanding of the UNDHR…` → `[Lesson content]` (HIS1003 / HIS1004). Gold HIS1004_1.0: "
 "`#module-menu-content > row > col-md-8 > <p>In this lesson you are reviewing…</p>`; Claude: an empty menu and the sentence in a "
 "`div.alert` at the top of `#body` — the r147 section-stop ends the menu at ANY alert (right for CED's `[alert.top]` printable-resources "
 "boxes, which the gold keeps in the body — CEDO501).",
 "- **Measured (`_s45_r9_loalert.py` — every alert-family tag inside a `[Lesson Overview] … [Lesson content]` block of every scored WT, by "
 "its text and the gold's placement):** an alert whose text opens with a WALT lead → the gold's **MENU 20 of 21** (HIS1003 / HIS1004 `[alert "
 "box]` 20; the one exception MXFL203's `coloured box` → body); EVERY other alert in such a block (CED `alert.top` 28 absent / 4 body, "
 "plain `alert` 24 body / 12 absent, `alert box` 14 body / 6 absent, RHS / solid / top …) → body or absent, **never the menu** — the "
 "discriminator is the text, and r147's CED rule is untouched.",
 "- **Authority:** level 1 — KB 01B / 01E (the lesson page's menu IS that lesson's own `[Lesson Overview]` block; `[Lesson content]` marks "
 "where the body starts) — and the gold 20 / 21. 20 pages (the body floor exactly). Predicts a skeleton move up on ≈ 20 HIS lesson pages "
 "(the alert's wrapper lines leave the body; the menu gains the gold's p).",
]
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(L)); os.replace(S + ".tmp", S)
print("ok", os.path.getsize(S))
