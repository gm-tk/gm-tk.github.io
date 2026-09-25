#!/usr/bin/env python3
"""ROUND 498 finalise (session 46 Round 9 — the hover definition's red first letter, HOVERTAILHEAD_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 498," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.60";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 497 BASELINE"; a11 = "| `CDSCRAPREL2_OFF` | 497 |"; a14 = "- **Build:** `260620.60` (round 497"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 498 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈14:05, session 46 Round 8", "- LAST SHIPPED: **r497**",
          "- Before it: **r496**", "- Before them: **r495 → r467**", "- Plateau window (§4): **0 of 3** — r497", "- Standing facts: AppVersion **260620.60**",
          "## Round log", "**Next session starts with:**", "- **(s46-r6 → r8) the XDLS choice board's declined pages"):
    find(p)
entry = """## 2026-09-25 (round 498, build 260620.61) — THE HOVER DEFINITION'S RED FIRST LETTER: a colon hover marker whose red run carries the definition's first letter(s) keeps them, and a `]` typed black ends the definition (15 → 6 cut tooltips; 16 pages / 16 modules)

### 1. WHAT CHANGED

**The find** (session 46 Round 9 — the hover lane's s45-r2 (a) residue traced: `_s46_r9_colon.py` → `_s46_r9_infohead.py`, `_s46_items.cjs`): Word often leaves the definition's FIRST LETTER in the red marker run — `[roll over definition: T` red, `o move to or find a place.` black (SSFUN03), `[hover definition: S` + `pecific measurable details.` (TEFUN05), `[roll-over definition: for` + `the rights of urban Māori…` (ANZH301 / 302). The unclosed marker takes r222c's def_black_tail path, which read only the black tail, so **15 tooltips in 9 modules shipped with their first letter(s) cut** (`o move to…`, `hings the stakeholders want`, `n computing, a bus is…`, `ollaboration, support, belonging`). The same path took a `]` the writer typed BLACK as part of the definition, so the rest of the paragraph shipped inside the tooltip (GEO1006 `…a river follows.] is often narrow…`, HIS1003, SSFUN01, XDLS502, XDLS901) and AGH1008's `sires [hover: fathers] and dams [hover: mothers]` built one tooltip holding both.

**The fix** (`InteractiveScanner.#weaveHoverDefinition` A4, data `elements.hover_definition_inline.split_bracket.def_black_tail_head`, env `HOVERTAILHEAD_OFF`): (a) the text after the unclosed marker's colon heads the definition, joined as the source joins it — a space when the black tail opens with one or the red run ENDS with one (the run's own space shows as two before the extractor's one-space pad: `for␣␣` + `the rights…`, but `T␣` + `o move…`); (b) a black `]` ends the definition there and the rest is the sentence again.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **16 pages / 16 modules** (AGH1008 ANZH301 ANZH302 ARFUN03 DAN1004 ENGS404 GEO1006 HIS1003 SSFUN01 SSFUN03 SSOG301 TEDC402 TEFUN05 XDLS502 XDLS901 XGF9002), each diffed by hand: every change is a restored definition head (`To move…`, `Specific…`, `Things…`, `In computing…`, `Collaboration…`, `The outcome…`, `for the rights…`) or a definition cut at its black `]` with the sentence restored after the anchor (GEO1006, HIS1003 `lionise`, SSFUN01, XDLS502, XDLS901); AGH1008 now builds BOTH tooltips (`sires` = fathers, `dams` = mothers). Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS**.
- Companion (the gate is blind to `info=`): `_s46_r9_infohead.py` first-letter cuts **15 → 6** (the six left are other shapes); `_s45_r2_hover.py` gold-matched definitions **COLON-inline 297 → 304, QUOTED 18 → 19 (+8)**; Claude tooltips 1070 → 1071.

### 3. PROTECTED GATES

- Skeleton **55.4469 % @ 2491 — 0 movers** (a skeleton-blind text-fidelity round), ≥50 1591, ≥75 277, ≥90 26, RAW 39.419 %; body ANY 232; cs 16745 / 198 / 888, clean 2591 / 2633, leak 52 / 42 EXACT; tags 9557 / 9557; every verifier RESULT ✓; selftests 50 green / 0 fail; the miner 195 CANDIDATE.
- Plateau (§4): a skeleton-blind writer-content round (the r495 precedent) — neither; **0 of 3**.

**Recorded, not built (the PICK pass):** `TRACE_ITDROP` over the corpus — **153 hover definitions (145 unique, 74 modules) are still DROPPED by `ListsAndRuns.inlineMarkup`** because no clean word sits right before the sentinel: 84 after a full stop, 14 `?`, 6 `!`, 6 a closing quote, 16 an empty host (`_s46_r9_itdrop.py`); the gold builds 49 of them (anchors: the last word before the punctuation — `holistically`, `colony`, `atmospheres` — a quoted phrase `“push factors”`, a whole short exclamation `Ka rawe tō mahi!`), but 90 are writer notes (`on ‘Fibre’`, `colour 3`, `over Māori boy`, `(`) — a punctuation-anchor rule needs a note filter first. The six first-letter cuts left (GEO1006 `ctions`, MXFL301 `maginary`, OSBY101, OSSM301, TEFUN05, XDLS909) are other marker shapes.

**Ledger:** scoped #8 since the r490 FULL — **the FULL backstop is DUE** · data `elements.hover_definition_inline.split_bracket.def_black_tail_head` · env `HOVERTAILHEAD_OFF` · code `InteractiveScanner.#weaveHoverDefinition` (A4) · tools `_s46_r9_colon.py`, `_s46_r9_infohead.py`, `_s46_r9_itdrop.py` (+ the `TRACE_ITDROP` stderr hook in `ListsAndRuns.inlineMarkup`), `_s46_items.cjs`, `_r498_finalise.py` · session 46 Round 9.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 498 (260620.61): THE HOVER DEFINITION'S RED FIRST LETTER (session 46 Round 9) — a colon hover marker whose red run "
                "carries the def's first letter(s) keeps them; a black ']' ends the def. Env HOVERTAILHEAD_OFF.\n" + '\tstatic AppVersion = "260620.61";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 498 BASELINE (the hover definition's red first letter, "
                "`HOVERTAILHEAD_OFF`; SCOPED, scoped #8 since the r490 FULL — the FULL backstop DUE; scoped_ship PASS): SCAFFOLD mean 55.4469% / >=50% "
                "1591 / >=75% 277 / >=90% 26 / RAW 39.419% @ 2491 pairs — 0 movers (skeleton-blind: 16 pages' tooltips; first-letter cuts 15 -> 6, "
                "gold-matched defs +8); body ANY 232; cs / clean / leak EXACT.** Previous: **ROUND 497 BASELINE")
so = so.replace(a11, "| `HOVERTAILHEAD_OFF` | 498 | **THE HOVER DEFINITION'S RED FIRST LETTER** (session 46 Round 9). Reverts "
                "`elements.hover_definition_inline.split_bracket.def_black_tail_head`: an unclosed colon hover marker whose red run carries the "
                "definition's first letter(s) loses them again (`o move to…`), and a black `]` no longer ends the definition; byte-identical to r497. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.61` (round 498 — **the hover definition's red first letter**; `HOVERTAILHEAD_OFF`; scoped #8 since the r490 "
                "FULL — the FULL backstop DUE; 16 pages; skeleton 55.4469 % @ 2491, 0 movers).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r498.bak")
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
setv("build", '"260620.60"', '"260620.61"'); setv("round", "497", "498")
insert_before("_note_r497", '    "_note_r498": "Round 498 (session 46 Round 9, 2026-09-25) — THE HOVER DEFINITION\'S RED FIRST LETTER (HOVERTAILHEAD_OFF): 16 pages / '
              '16 modules, tooltips only (first-letter cuts 15 -> 6, gold-matched defs +8); SCAFFOLD 55.4469 @ 2491, 0 movers; every gate EXACT; '
              'scoped #8 (the FULL backstop due); scoped_ship PASS.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r498-finalise.bak")
i = find("- **ROUND 498 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈14:35, session 46 Round 9 — r498 (the hover definition's red first letter) SHIPPED and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r498** (260620.61); **LAST FULL = r490 (the s45 Round 10 backstop)**; ledger "
        "**scoped #8 — THE FULL BACKSTOP IS DUE (take it next)**. Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / "
        "`_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈14:05, session 46 Round 8"); prior = L[k]; del L[k]
k = find("- Before it: **r496**"); r496 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r497**"); L[k] = L[k].replace("- LAST SHIPPED: **r497**", "- Before it: **r497**", 1)
L.insert(k, "- LAST SHIPPED: **r498** (build 260620.61, 25 Sept ≈14:35, session 46 Round 9 — THE HOVER DEFINITION'S RED FIRST LETTER, "
         "`HOVERTAILHEAD_OFF`; SCOPED, **scoped #8 since the r490 FULL backstop — the FULL is DUE**, scoped_ship PASS; 16 pages' tooltips "
         "(first-letter cuts 15 → 6, gold-matched definitions +8); **skeleton 55.4469 % @ 2491, 0 movers**, ≥50 1591, ≥75 277, ≥90 26, RAW "
         "39.419 %; body ANY 232; cs / clean / leak EXACT; `gate_baseline.json` at r498; the miner 195 CANDIDATE).")
k = find("- Before them: **r495 → r467**")
L[k] = L[k].replace("- Before them: **r495 → r467** (260620.58 → 260620.34 — the literal-tag leak,",
                    "- Before them: **r496 → r467** (260620.59 → 260620.34 — the XDLS choice board's stray marker, the literal-tag leak,", 1)
assert "r496 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r497")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r497", "- Plateau window (§4): **0 of 3** — r498 a skeleton-blind writer-content round (neither); r497", 1)
k = find("- Standing facts: AppVersion **260620.60**")
L[k] = L[k].replace("AppVersion **260620.60** (r497 the XDLS choice board's last declined pages — session 46 Round 8, 25 Sept); before it 260620.59",
                    "AppVersion **260620.61** (r498 the hover definition's red first letter — session 46 Round 9, 25 Sept); before it 260620.60 (r497 "
                    "the XDLS choice board's last declined pages — session 46 Round 8); before it 260620.59", 1)
assert "260620.61" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s46-r9 (engine r498, build 260620.61, 25 Sept ≈14:05 → 14:35) · a PICK pass on the hover lane (s45-r2 (a) traced: the COLON-"
         "inline defs Claude misses sit in hand-off boxes 30, are DROPPED 33, or cut) + the placement census (SAME 39.7 → 40.1 %) → THE HOVER "
         "DEFINITION'S RED FIRST LETTER (the def's red first letter(s) kept; a black `]` ends the def) · SHIPPED scoped #8, scoped_ship PASS · 16 "
         "pages' tooltips, first-letter cuts 15 → 6, gold-matched +8 · skeleton 0 movers · plateau 0 of 3 (neither).")
k = find("- **(s46-r6 → r8) the XDLS choice board's declined pages")
L.insert(k, "- **(s46-r9) the hover definitions after r498, each measured:** (a) **153 hover definitions (145 unique, 74 modules) are still DROPPED** "
         "by `ListsAndRuns.inlineMarkup` — no clean word right before the sentinel (`_s46_r9_itdrop.py`, from a `TRACE_ITDROP=1` probe): 84 after a "
         "full stop, 14 `?`, 6 `!`, 6 a closing quote, 16 an empty host; the gold builds 49 (the last word before the punctuation, a quoted phrase "
         "`“push factors”`, a whole short exclamation `Ka rawe tō mahi!`) but 90 are writer notes (`on ‘Fibre’` ×8 HES1002, `colour 3`, `over Māori "
         "boy`, `(`) — a punctuation-anchor rule needs a note filter first (the weave's `hover_weave_hygiene` is the place); (b) 30 COLON-inline "
         "defs sit inside un-built hand-off boxes (the widget builds own them); (c) six first-letter cuts of other shapes (GEO1006 `ctions`, "
         "MXFL301 `maginary`, OSBY101, OSSM301, TEFUN05, XDLS909). **The placement census (s46-r9, `_pc_r497.md`):** SAME 39.7 → 40.1 %, MOVED "
         "22.8 → 22.4 %; its CANDIDATE rows are the known lanes — `body:alert → body:free` 1279 blocks (the r469 alert patch), `accordion → free` "
         "1127, `tabs → free` 658 (TEFUN), `dropDown → ABSENT-inWT` 617, `flipCard → ABSENT-inWT` 546, `wordHighlighter → free` 438 (WJFUN).")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r496 + the r497 no-round line (verbatim, s46 r498)\n\n" + r496 + "\n" + prior + "\n"
    "\n## Session 46 — Round 9 (engine r498) — the hover definition's red first letter\n\n" + marker + "\n"
    "- **What shipped (r498, 260620.61):** `elements.hover_definition_inline.split_bracket.def_black_tail_head` (env `HOVERTAILHEAD_OFF`). Probe "
    "OFF 0; ON 16 pages / 16 modules; scoped_ship PASS; skeleton 0 movers; first-letter cuts 15 → 6, gold-matched defs +8.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
