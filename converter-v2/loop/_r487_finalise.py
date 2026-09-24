#!/usr/bin/env python3
"""ROUND 487 finalise (session 45 Round 2 — the unquoted named hover anchor, HOVERNAMED_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 487," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.50";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 486 BASELINE"; a11 = "| `QUOTEFORM_OFF` | 486 |"; a14 = "- **Build:** `260620.50` (round 486"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 487 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈06:05, session 45 Round 1", "- LAST SHIPPED: **r486**",
          "- Before it: **r485**", "- Before them: **r484 → r467**", "- Plateau window (§4): **0 of 3** — r486", "- Standing facts: AppVersion **260620.50**",
          "## Round log", "**Next session starts with:**", "## Session 45 — Round 2 PICK (engine r487)", "- **(s45-r1) the quote family after r486"):
    find(p)
entry = """## 2026-09-25 (round 487, build 260620.51) — THE UNQUOTED NAMED HOVER ANCHOR: `[Rollover definition for TERM: DEF]` / `[Hover on TERM: DEF]` / `[roll over definition TERM: DEF]` weaves onto TERM instead of being dropped

### 1. WHAT CHANGED

**The find** (session 45 Round 2 — the HIS1 family view, `span.infoTrigger` MISSING 57 lines / 21 pages / 7 modules, traced on HIS1005 with `_probe_infotrigger.cjs`): the writer's standalone `[Rollover definition for supreme: Ultimate or final.]` line (typed after the paragraph that contains "supreme") resolves to the `info trigger` tag; `InteractiveScanner.#weaveHoverDefinition` recovers the definition, but honours only a QUOTED named anchor (r222c — `[hover info ‘pitch’: …]`), so the sentinel was appended after the host paragraph's LAST word — which ends in a full stop — and `inlineMarkup` found no word and **silently dropped the definition** (writer content lost; the gold wraps "supreme"). Inline markers whose named word was not the last one before them were anchored on the wrong word (ARFUN02 "elements" for "components", DAN1004 "state" for "surging").

**Measured** (`_s45_r2_hover.py` — every hover / rollover marker in every scored WT, by shape, the def matched whitespace-free against every `info=` attribute): the `for / on / of TERM:` form 104 markers / 14 modules — the gold builds 47 that Claude dropped, both 41, neither 14; the `definition TERM:` form 17 / 4 — gold-only 8. HIS1005 23, HIS1002 12, HIS1006 5, HIS1008 4, ARFUN05 3, ARFUN01 / 03 2, CEDO202 2, HIS1001 / 1007 1.

**The fix:** the named TERM (data `patterns[]` group 1, a leading the / a / an stripped) is searched — whole word, case-insensitive, never inside an earlier woven definition, never a word that already carries one — in the nearest 3 text items when the marker stands on its own line (a different source paragraph; the sentinel lands after its FIRST occurrence — the gold's HIS1005 "supreme"), and ONLY in its own paragraph when the marker is inline (after its LAST occurrence — the word just before it; ARFUN05's writer typo `setting. [hover on time: …]` keeps the historical placement on "setting" instead of reaching back into the "time" bullet); after any closing `**` / `*` so a bold anchor wraps whole. A standalone definition line's own trailing text stays its own paragraph. A quoted or lifted anchor keeps its path; no TERM / no match → the unchanged historical append. Data `Emit_Templates.elements.hover_definition_inline.named_anchor`; env **`HOVERNAMED_OFF`**, byte-identical OFF.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **30 pages / 12 modules** (ANZH401 ARFUN01 ARFUN02 ARFUN03 CEDO202 DAN1004 HIS1001 HIS1002 HIS1005 HIS1006 HIS1007 HIS1008): **infoTrigger spans +70** (HIS1005 5 → 33, HIS1002 1 → 13, HIS1006 0 → 9, HIS1008 0 → 4, HIS1001 1 → 3, HIS1007 3 → 5, CEDO202 11 → 13, ARFUN01 / 03 +1); four modules re-anchor a span onto the writer-named word (ARFUN02 components, DAN1004 surging, ANZH401 pūrakau without its full stop). No new literal marker text on any page. Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS**.

### 3. PROTECTED GATES

- Skeleton **55.3485 % → 55.3576 % @ 2491 (+0.0091pp)**, RAW 39.234 → 39.243 %; **≥50 1582 → 1584 (+2: HIS1005_1_0 46.6 → 51.5, HIS1005_4_0 48.3 → 50.2)**, ≥75 277, ≥90 26; 25 movers, **17 up / 8 down NAMED**, each with its position-free companion (`_r487_companion.py`): ARFUN01_0_0 −1.0 (overlap +1), HIS1001_10_0 −1.0 (+1), HIS1006_11_0 −1.0 (+3 — it gains the gold's own three hovers), HIS1005_5_0 −0.6 (+2), HIS1002_2_0 −0.5 (+1), HIS1001_8_0 −0.2 (+1), HIS1002_5_0 −0.1 (+4); HIS1005_0_0 −0.8 (overlap ±0): the gold's overview omits the writer's three tagged rollovers — a writer-tagged element, the gold's omission a NAMED override (c14: the writer's tag decides the component).
- compare_structure exact **16701 → 16702**, EXTRA 198 / missing 878 / row-wrap 24 EXACT; body 238 / clean 2587 / 2633 / leak 75 / 46 EXACT; tags 9557 / 9557; every verifier RESULT line ✓; selftests 50 green / 0 fail; the miner 195 CANDIDATE.
- Plateau (§4): +0.0091pp (< 0.02) but ≥50 +2 — a protected bucket moved: neither counts nor resets; **0 of 3**.

**Recorded, not built:** the COLON-inline hover markers with no named term (`[Hover definition: DEF]` after the word) — the gold builds 94 that Claude does not, spread over 20+ modules at 2–8 each (AGH1007 8, SSFUN03 / CEDR203 6, AGH1002 / AGH1009 / SCES201 5 …) — a separate class for its own measure.

**Ledger:** scoped #5 since the r482 FULL · data `elements.hover_definition_inline.named_anchor` · env `HOVERNAMED_OFF` · code `InteractiveScanner.#weaveHoverDefinition` · tools `_s45_r2_{hover,pick}.py`, `_r487_companion.py`, `_s45_{regen,postship}.sh`, `_r487_finalise.py` · session 45 Round 2.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 487 (260620.51): THE UNQUOTED NAMED HOVER ANCHOR (session 45 Round 2) — [rollover definition for TERM: DEF] weaves onto "
                "TERM (InteractiveScanner.#weaveHoverDefinition) instead of being dropped. Env HOVERNAMED_OFF.\n" + '\tstatic AppVersion = "260620.51";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 487 BASELINE (the unquoted named hover anchor, `HOVERNAMED_OFF`; "
                "SCOPED, scoped #5 since the r482 FULL; scoped_ship PASS): SCAFFOLD mean 55.3576% / >=50% 1584 / >=75% 277 / >=90% 26 / RAW 39.243% @ "
                "2491 pairs — +0.0091pp (17 up / 8 down NAMED), >=50 +2; cs exact 16702; body / clean / leak EXACT.** Previous: **ROUND 486 BASELINE")
so = so.replace(a11, "| `HOVERNAMED_OFF` | 487 | **THE UNQUOTED NAMED HOVER ANCHOR** (session 45 Round 2). Reverts "
                "`elements.hover_definition_inline.named_anchor`: `[rollover definition for TERM: DEF]` / `[hover on TERM: DEF]` / `[roll over definition "
                "TERM: DEF]` go back to the historical append after the host's last word (dropped when the host ends a sentence) — 12 modules / 30 "
                "pages; byte-identical to r486. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.51` (round 487 — **the unquoted named hover anchor**; `HOVERNAMED_OFF`; scoped #5 since the r482 FULL; 12 "
                "modules, +70 infoTrigger spans; skeleton 55.3576 % @ 2491, +0.0091pp, ≥50 +2).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r487.bak")
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
setv("build", '"260620.50"', '"260620.51"'); setv("round", "486", "487")
insert_before("_note_r486", '    "_note_r487": "Round 487 (session 45 Round 2, 2026-09-25) — THE UNQUOTED NAMED HOVER ANCHOR (HOVERNAMED_OFF): 12 modules / 30 pages, '
              '+70 infoTrigger spans; SCAFFOLD 55.3485 -> 55.3576 @ 2491 (+0.0091pp, 17 up / 8 down NAMED); RAW 39.234 -> 39.243; >=50 1582 -> 1584; '
              'cs exact 16701 -> 16702; body / clean / leak EXACT; scoped #5 since the r482 FULL; scoped_ship PASS.",')
setv("mean_scaffold_pct", "55.35", "55.36"); setv("pages_ge_50", "1582", "1584"); setv("raw_mean_pct", "39.23", "39.24")
setv("exact_chain", "16701", "16702")
insert_before("_note_r486_state", '    "_note_r487_state": "r487 (the unquoted named hover anchor): SCAFFOLD 55.3576 @ 2491, RAW 39.243; 25 movers (17 up / 8 down NAMED).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r487-finalise.bak")
i = find("- **ROUND 487 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈06:35, session 45 Round 2 — r487 (the unquoted named hover anchor) SHIPPED and committed; the "
        "in-flight marker is cleared). LAST SHIPPED **r487** (260620.51); **LAST FULL = r482 (the s44 backstop)**; ledger **scoped #5** (3 of "
        "headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈06:05, session 45 Round 1"); prior = L[k]; del L[k]
k = find("- Before it: **r485**"); r485 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r486**"); L[k] = L[k].replace("- LAST SHIPPED: **r486**", "- Before it: **r486**", 1)
L.insert(k, "- LAST SHIPPED: **r487** (build 260620.51, 25 Sept ≈06:35, session 45 Round 2 — THE UNQUOTED NAMED HOVER ANCHOR, `HOVERNAMED_OFF`; "
         "SCOPED, **scoped #5 since the r482 FULL backstop**, scoped_ship PASS; **skeleton 55.3485 → 55.3576 % @ 2491 (+0.0091pp, 17 up / 8 down "
         "NAMED)**, **≥50 1584 (+2)**, ≥75 277, ≥90 26, RAW 39.243 %; cs exact 16702 (+1); body / clean / leak EXACT; +70 infoTrigger spans; "
         "`gate_baseline.json` at r487; the miner 195 CANDIDATE).")
k = find("- Before them: **r484 → r467**")
L[k] = L[k].replace("- Before them: **r484 → r467** (260620.48 → 260620.34 — KB c38 for the quiz types,",
                    "- Before them: **r485 → r467** (260620.49 → 260620.34 — the title-bar language split, KB c38 for the quiz types,", 1)
k = find("- Plateau window (§4): **0 of 3** — r486")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r486", "- Plateau window (§4): **0 of 3** — r487 +0.0091pp but ≥50 +2 (a protected "
                    "bucket moved: neither); r486", 1)
k = find("- Standing facts: AppVersion **260620.50**")
L[k] = L[k].replace("AppVersion **260620.50** (r486 KB 01F the quote form — session 45 Round 1, 25 Sept); before it 260620.49",
                    "AppVersion **260620.51** (r487 the unquoted named hover anchor — session 45 Round 2, 25 Sept); before it 260620.50 (r486 KB 01F "
                    "the quote form — session 45 Round 1); before it 260620.49", 1)
assert "260620.51" in L[k]
k = find("- **(s45-r1) the quote family after r486")
L.insert(k, "- **(s45-r2) the hover markers after r487, each measured (`_s45_r2_hover.py`):** (a) **COLON-inline with no named term** "
         "(`[Hover definition: DEF]` right after the word) — the gold builds 94 that Claude does not, over 20+ modules at 2–8 each (AGH1007 8, "
         "SSFUN03 / CEDR203 6, AGH1002 / AGH1009 / SCES201 5, CEDT501 4, ARFUN04 / XDLS901 / AGH1004 / GEO1006 / TEDC402 / XGF9001 3) — trace a "
         "few (table cells? split runs? a bold anchor two words back?) before sizing a round; (b) the `trigger` form: gold-only 18 (ANZH205 4); "
         "(c) OTHER shapes 506 markers / 110 modules where neither side matched a def (XDLS 149, GENO 42, TEFUN 40 — `[Hover definition]` "
         "with the def elsewhere) — census by shape first; (d) HIS1005_0_0's three overview rollovers the gold omits (NAMED).")
k = find("## Round log")
L.insert(k + 1, "- s45-r2 (engine r487, build 260620.51, 25 Sept 06:10 → ≈06:35) · THE UNQUOTED NAMED HOVER ANCHOR (the HIS1 lane: "
         "`[Rollover definition for TERM: DEF]` lines were appended after a sentence-final word and DROPPED — writer content lost; now woven "
         "onto TERM, first occurrence for a standalone line, last for inline) · SHIPPED scoped #5, scoped_ship PASS · 12 modules / 30 pages, +70 "
         "infoTrigger spans · skeleton +0.0091pp (17 up / 8 down NAMED), ≥50 +2 · plateau 0 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r487** (260620.51, "
        "the unquoted named hover anchor); LAST FULL = **r482** (the s44 backstop); ledger scoped #5; plateau **0 of 3**; 2,491 pairs; census 552 / "
        "545 / 2,679. Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs "
        "Chris #17–#19, #22.")
k = find("## Session 45 — Round 2 PICK (engine r487)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 45 — Round 2 PICK (engine r487) — THE UNQUOTED NAMED HOVER ANCHOR — SHIPPED; the PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md 'Session 45 — Round 2 PICK (engine r487) + what shipped'; the one-line summary is the s45-r2 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r485 (verbatim, s45 r487)\n\n" + r485 + "\n"
    "\n## Session 45 — Round 2 PICK (engine r487) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r487, 260620.51):** `elements.hover_definition_inline.named_anchor` (env `HOVERNAMED_OFF`; two patterns — `for / on / of "
    "TERM:` and `definition TERM:`; lookback 3 for a standalone line, own paragraph only when inline; first / last occurrence; never inside or "
    "onto an existing definition) — `InteractiveScanner.#weaveHoverDefinition`. Probe OFF 0 changed; ON 30 pages / 12 modules, +70 spans; "
    "scoped_ship PASS; +0.0091pp, 17 up / 8 down NAMED, ≥50 +2.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
