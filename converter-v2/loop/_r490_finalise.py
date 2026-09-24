#!/usr/bin/env python3
"""ROUND 490 finalise (session 45 Round 9 — the lesson overview's WALT alert is menu content, LOWALTALERT_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 490," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.52";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 488 BASELINE"; a11 = "| `CARSTORY_OFF` | 488 |"; a14 = "- **Build:** `260620.52` (round 488"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
kD = "| — | c92 language fonts (7 pages), c85 three-part title (5 modules)"; assert sk.count(kD) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 490 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈07:25, session 45 Round 5", "- LAST SHIPPED: **r488**",
          "- Before it: **r487**", "- Before them: **r486 → r467**", "- Plateau window (§4): **0 of 3** — r488", "- Standing facts: AppVersion **260620.52**",
          "## Round log", "**Next session starts with:**", "## Session 45 — Round 9 PICK (engine r490)"):
    find(p)
entry = """## 2026-09-25 (round 490, build 260620.53) — THE LESSON OVERVIEW'S WALT ALERT IS MENU CONTENT: an alert inside a lesson's `[Lesson Overview]` block whose text opens with a learning-intentions lead joins the lesson menu as its plain sentence

### 1. WHAT CHANGED

**The find** (session 45 Rounds 7 + 9 — the §1g placement lane: lesson pages whose Claude menu is EMPTY while the gold's has text — 312 pages / 72 modules, 66 / 23 with the gold's menu text sitting in Claude's BODY, six writer forms). One form is a clean, KB-backed rule: HIS1003 / HIS1004 write `[Lesson Overview] <lesson title>` → `[Alert box] In this lesson you are reviewing your understanding of the UNDHR and responsibilities of individuals and groups within societies.` → `[Lesson content]`. The gold (HIS1004_1.0): `#module-menu-content > row > col-md-8 > <p>In this lesson you are reviewing…</p>`; Claude: an EMPTY menu and the sentence in a `div.alert` at the top of `#body`, because the r147 section-stop ends the lesson menu at ANY alert — right for the CED family's `[alert.top]` printable-resources boxes, which the gold keeps in the body (CEDO501).

**Measured** (`_s45_r9_loalert.py` — every alert-family tag inside a `[Lesson Overview] … [Lesson content]` block of every scored WT, by its text and the gold's placement): an alert whose text opens with a WALT lead → the gold's **menu 20 of 21** (the exception MXFL203's `coloured box` → body, named); EVERY other alert in such a block → body or absent, never the menu (CED `alert.top` 28 absent / 4 body; `alert` 24 body / 12 absent; `alert box` 14 / 6; RHS / solid / top …). The discriminator is the TEXT; r147's CED rule is untouched. The unifying "move any WALT lead into the menu" rule is NOT supported (Round 7: body 70 / menu 46 / absent 73) — only this form is.

**The fix:** in the lesson-menu SECTION-STOP (`ContentConverter`, r147), an alert / important box in section A (the LO intro run) whose own text matches `lead_pattern` ("in this lesson you", "we are learning", "you will", "this lesson") is menu-safe and joins the menu as a plain black-text item — its sentence as the gold's `<p>`, no alert wrapper. Every other alert still ends the section. Data `Emit_Templates.menu.lesson_menu_section_stop.walt_alert` {enabled, env, alert_tags, lead_pattern}; env **`LOWALTALERT_OFF`**, byte-identical OFF. Authority: KB 01B / 01E (the lesson page's menu IS that lesson's own `[Lesson Overview]` block; `[Lesson content]` marks where the body starts) + the gold 20 / 21.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **20 pages / 2 modules** (HIS1003, HIS1004) — every lesson page's menu now carries the gold's sentence (HIS1004_1_0 byte-for-byte the gold's menu). Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS**.

### 3. PROTECTED GATES

- Skeleton **55.3605 % → 55.3705 % @ 2491 (+0.0100pp)**, RAW 39.280 → 39.285 %; **≥50 1584 → 1585 (+1)**, ≥75 277, ≥90 26; 20 movers, **15 up / 5 down NAMED** (`_r490_companion.py`): HIS1003_7_0 23.7 → 18.9 (position-free overlap +2 — the gold's menu carries exactly this sentence; alignment); HIS1003_3_0 −2.2, HIS1003_9_0 −0.8 (the gold overview's content pair), HIS1004_2_0 −0.3, HIS1004_10_0 −0.1 — overlap equal while Claude's UNMATCHED lines fall by 3–5 (the removed alert wrapper), i.e. position-free precision rises; up HIS1003_8 +4.6, _2 +3.6, _6 +3.4, _10 +2.9, HIS1004_1 +2.6 …
- compare_structure exact 16702 / EXTRA 198 / missing 878 / row-wrap 24 EXACT; body 238 / clean 2587 / 2633 / leak 75 / 46 EXACT; tags 9557 / 9557; every verifier RESULT line ✓; selftests 50 green / 0 fail; the miner 194 CANDIDATE.
- Plateau (§4): +0.0100pp (< 0.02) but ≥50 +1 — a protected bucket moved: neither counts nor resets; **0 of 3**.

**Recorded, not built** (Round 7): the other five in-body forms — TEDC's `[Lesson content]` → `[Overview]` → a one-cell LI / SC table (6 pages), COM's `[A fancy looking box]` (12), CBI's `[Alert solid] Blue box` + `[H4] We are learning about:` (6), XGF9006's `[Insert accordion]` LI block (7), MXEX101's `[Lesson Overview]` → `[H2] Understand` (4) — each its own module family, under the floor.

**Ledger:** scoped #7 since the r482 FULL · data `menu.lesson_menu_section_stop.walt_alert` · env `LOWALTALERT_OFF` · code `ContentConverter` section-stop `buildSet` + the menu routing · tools `_s45_r7_{emptymenu,wtform,waltbody}.py`, `_s45_r9_{loalert,pick}.py`, `_r490_companion.py`, `_s45_{regen,postship}.sh`, `_r490_finalise.py` · session 45 Round 9. (r489 was consumed by Round 6's declined accordion prototype — the ride-along patch `_r489_accbullet_declined.patch`.)

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 490 (260620.53): THE LESSON OVERVIEW'S WALT ALERT IS MENU CONTENT (session 45 Round 9) — an alert in a [Lesson "
                "Overview] block whose text opens with a learning-intentions lead joins the lesson menu as its sentence (the r147 section-stop). "
                "Env LOWALTALERT_OFF.\n" + '\tstatic AppVersion = "260620.53";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 490 BASELINE (the lesson overview's WALT alert is menu content, "
                "`LOWALTALERT_OFF`; SCOPED, scoped #7 since the r482 FULL; scoped_ship PASS): SCAFFOLD mean 55.3705% / >=50% 1585 / >=75% 277 / "
                ">=90% 26 / RAW 39.285% @ 2491 pairs — +0.0100pp (15 up / 5 down NAMED), >=50 +1; cs / body / clean / leak EXACT.** Previous: "
                "**ROUND 488 BASELINE")
so = so.replace(a11, "| `LOWALTALERT_OFF` | 490 | **THE LESSON OVERVIEW'S WALT ALERT IS MENU CONTENT** (session 45 Round 9). Reverts "
                "`menu.lesson_menu_section_stop.walt_alert`: an alert inside a `[Lesson Overview]` block ends the lesson menu again (r147) and its "
                "learning-intentions sentence ships as an alert at the top of the body — HIS1003 / HIS1004, 20 pages; byte-identical to r488. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.53` (round 490 — **the lesson overview's WALT alert is menu content**; `LOWALTALERT_OFF`; scoped #7 since "
                "the r482 FULL; 2 modules / 20 pages; skeleton 55.3705 % @ 2491, +0.0100pp, ≥50 +1).\n" + a14)
wr(PO, so); print("OG ok")
KL = sk.split("\n"); iD = [i for i, l in enumerate(KL) if l.startswith(kD)][0]
KL.insert(iD, "| ~~—~~ | 01B / 01E — the lesson page's menu is that lesson's own `[Lesson Overview]` block (`[Lesson content]` marks the body): an "
          "alert INSIDE the block whose text is the lesson's learning-intentions sentence is menu content | **SHIPPED round 490 (2026-09-25, "
          "session 45 Round 9)** — `menu.lesson_menu_section_stop.walt_alert`, `LOWALTALERT_OFF`; HIS1003 / HIS1004, 20 pages (the gold 20 / 21; "
          "every other LO-block alert stays in the body — r147) | skeleton-visible (+0.0100pp, ≥50 +1) | the alert's own text (a WALT lead) | "
          "the other in-body LI forms (TEDC / COM / CBI / XGF9006 / MXEX101) each under the floor |")
wr(PK, "\n".join(KL)); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r490.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            G[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.52"', '"260620.53"'); setv("round", "488", "490")
insert_before("_note_r488", '    "_note_r490": "Round 490 (session 45 Round 9, 2026-09-25) — THE LESSON OVERVIEW\'S WALT ALERT IS MENU CONTENT (LOWALTALERT_OFF): '
              'HIS1003 / HIS1004, 20 pages; SCAFFOLD 55.3605 -> 55.3705 @ 2491 (+0.0100pp, 15 up / 5 down NAMED); RAW 39.280 -> 39.285; >=50 1584 '
              '-> 1585; cs / body / clean / leak EXACT; scoped #7 since the r482 FULL; scoped_ship PASS. (r489 = the declined accordion prototype, '
              'no ship.)",')
setv("mean_scaffold_pct", "55.36", "55.37"); setv("pages_ge_50", "1584", "1585")
insert_before("_note_r488_state", '    "_note_r490_state": "r490 (the LO WALT alert): SCAFFOLD 55.3705 @ 2491, RAW 39.285; 20 movers (15 up / 5 down NAMED).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r490-finalise.bak")
i = find("- **ROUND 490 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈08:05, session 45 Round 9 — r490 (the lesson overview's WALT alert is menu content) SHIPPED "
        "and committed; the in-flight marker is cleared). LAST SHIPPED **r490** (260620.53); **LAST FULL = r482 (the s44 backstop)**; ledger "
        "**scoped #7** (1 of headroom — the FULL backstop is due at the next scoped ship). Ride-along patches `outputs/_r489_accbullet_declined.patch` "
        "(the accordion bulleted bold lead, 9 pages / +8 accordions), `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` "
        "(buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈07:25, session 45 Round 5"); prior = L[k]; del L[k]
k = find("- Before it: **r487**"); r487 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r488**"); L[k] = L[k].replace("- LAST SHIPPED: **r488**", "- Before it: **r488**", 1)
L.insert(k, "- LAST SHIPPED: **r490** (build 260620.53, 25 Sept ≈08:05, session 45 Round 9 — THE LESSON OVERVIEW'S WALT ALERT IS MENU CONTENT, "
         "`LOWALTALERT_OFF`; SCOPED, **scoped #7 since the r482 FULL backstop**, scoped_ship PASS; **skeleton 55.3605 → 55.3705 % @ 2491 "
         "(+0.0100pp, 15 up / 5 down NAMED)**, **≥50 1585 (+1)**, ≥75 277, ≥90 26, RAW 39.285 %; cs / body / clean / leak EXACT; "
         "`gate_baseline.json` at r490; the miner 194 CANDIDATE).")
k = find("- Before them: **r486 → r467**")
L[k] = L[k].replace("- Before them: **r486 → r467** (260620.50 → 260620.34 — KB 01F the quote form,",
                    "- Before them: **r487 → r467** (260620.51 → 260620.34 — the unquoted named hover anchor, KB 01F the quote form,", 1)
k = find("- Plateau window (§4): **0 of 3** — r488")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r488", "- Plateau window (§4): **0 of 3** — r490 +0.0100pp but ≥50 +1 (a protected "
                    "bucket moved: neither); r488", 1)
k = find("- Standing facts: AppVersion **260620.52**")
L[k] = L[k].replace("AppVersion **260620.52** (r488 the story-reference carousel shell — session 45 Round 5, 25 Sept); before it 260620.51",
                    "AppVersion **260620.53** (r490 the lesson overview's WALT alert — session 45 Round 9, 25 Sept); before it 260620.52 (r488 the "
                    "story-reference carousel shell — session 45 Round 5); before it 260620.51", 1)
assert "260620.53" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s45-r9 (engine r490, build 260620.53, 25 Sept ≈07:40 → 08:05 real clock) · THE LESSON OVERVIEW'S WALT ALERT IS MENU CONTENT (the "
         "§1g lane from Round 7: an alert inside a `[Lesson Overview]` block whose text opens with a learning-intentions lead → the gold's menu "
         "20 / 21, every other LO-block alert body / absent; KB 01B) · SHIPPED scoped #7, scoped_ship PASS · HIS1003 / HIS1004, 20 pages · "
         "skeleton +0.0100pp (15 up / 5 down NAMED), ≥50 +1 · plateau 0 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r490** (260620.53, "
        "the LO WALT alert); LAST FULL = **r482** (the s44 backstop); ledger scoped #7 (the FULL backstop due at the next scoped ship); plateau "
        "**0 of 3**; 2,491 pairs; census 552 / 545 / 2,679. Ride-along patches `_r489_accbullet_declined.patch` / `_r469_declined.patch` / "
        "`_r469b_declined.patch` / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("## Session 45 — Round 9 PICK (engine r490)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 45 — Round 9 PICK (engine r490) — THE LESSON OVERVIEW'S WALT ALERT IS MENU CONTENT — SHIPPED; the PICK + what-shipped "
         "record is in LOOP_STATE_ARCHIVE.md 'Session 45 — Round 9 PICK (engine r490) + what shipped'; the one-line summary is the s45-r9 "
         "Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r487 (verbatim, s45 r490)\n\n" + r487 + "\n"
    "\n## Session 45 — Round 9 PICK (engine r490) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r490, 260620.53):** `menu.lesson_menu_section_stop.walt_alert` (env `LOWALTALERT_OFF`) — the section-stop's section A "
    "takes an LO-block alert whose text opens with a WALT lead as a menu item (its plain sentence). Probe OFF 0 changed; ON 20 pages / 2 "
    "modules; scoped_ship PASS; +0.0100pp, 15 up / 5 down NAMED, ≥50 +1.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
