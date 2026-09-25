#!/usr/bin/env python3
"""ROUND 499 finalise (session 46 Round 11 — the hover definition after the full stop, HOVERPUNCT_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 499," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.61";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 498 BASELINE"; a11 = "| `HOVERTAILHEAD_OFF` | 498 |"; a14 = "- **FULL backstop** at `260620.61`"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 499 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈14:55, session 46 Round 10", "- LAST SHIPPED: **r498**",
          "- Before it: **r497**", "- Before them: **r496 → r467**", "- Plateau window (§4): **0 of 3** — r498", "- Standing facts: AppVersion **260620.61**",
          "## Round log", "**Next session starts with:**", "- **(s46-r9) the hover definitions after r498"):
    find(p)
entry = """## 2026-09-25 (round 499, build 260620.62) — THE HOVER DEFINITION AFTER THE FULL STOP: a woven hover definition whose marker the writer typed after the sentence's punctuation is anchored instead of dropped (153 → 120 drops; 25 pages / 23 modules; ARFUN05 40.0 → 57.8 %)

### 1. WHAT CHANGED

**The find** (session 46 Rounds 9 / 11 — `TRACE_ITDROP=1` over the corpus, `_s46_r9_itdrop.py`): `ListsAndRuns.inlineMarkup` wraps the word right before a woven hover sentinel; a writer who typed the marker AFTER the sentence's punctuation (`…the addition of organic matter. [hover definition: …]`, `…wellbeing holistically. [Hover: Looking at the whole picture…]`, `Ka rawe tō mahi! [hover: Excellent work!] You have now completed…`) left no such word, and the definition was DROPPED — 153 corpus-wide (145 unique, 74 modules), the gold building 49 of them; 90 of the rest are writer notes riding the same path (`on ‘Fibre’` ×8 HES1002, `colour 3`, `over Māori boy`, `(`, `Blue text:`).

**The fix** (`ListsAndRuns.inlineMarkup`, data `elements.info_trigger_punct_anchor`, env `HOVERPUNCT_OFF`), before the drop, in order: (1) the line's FIRST SENTENCE (≤ 8 words, ending `.?!`) right before the marker is the anchor, punctuation INSIDE — the gold's own form (`<span …>setting.</span>` ARFUN05, `<span …>Ka rawe tō mahi!</span> You have…` BLL272–276, `WIE HEIßT DU? WIE HEIßEN SIE?` GENO901); (2) a bold / italic run right before the punctuation (`<b>korero purakau</b>.` ENGI302, `<b>verb</b>.` FRNO902); (3) a quoted phrase (`“push factors”` ANZH301 / 302, `“ich komme aus…”`); (4) the last word before 1–2 punctuation marks, only for a CAPITALISED definition of 2+ words (measured on the 32 candidates: the last word was the gold's term for 17 of 22 capitalised definitions but 4 of 10 lower-case ones, which mostly gloss a term named earlier — HIS1006 `the belief that certain groups…` = stereotype). A definition matching `note_pattern` (a leading `on / over / for / with`, a trailing colon, `colour N`, `with image`, `CS`, a `term – def`, a file name) or holding no letter is still dropped.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **25 pages / 23 modules** (ANZH301 ANZH302 ARFUN04 ARFUN05 BLL272 BLL273 BLL275 BLL276 CEDW501 DAN1003 DAN1006 ENFUN05 ENGI302 ENGI405 ENGS401 FRNO902 GENO901 HIS1003 HIS1004 HIS1005 MXEO301 SSOG301 WJFUN304), every change a new `infoTrigger` span (31), read one by one. Regeneration + 12-module spot-check clean. The first cut (the last word only) failed the scoped ship on `compare_structure` exact −7 (ARFUN05 / BLL272–276 / ENGS401: the gold wraps the whole short sentence, punctuation inside) — the first-sentence rule (1) fixed it; the second attempt's commas / colons over-reach (SSFUN07 `Question 3: If a product is defective,`, TEFUN01 a def of `1`) — rule (1) takes `.?!` only and a def needs a letter.
- Companion (`_s46_r9_itdrop.py` / `_s45_r2_hover.py`): drops **153 → 120**; gold-matched definitions **+10** (COLON-inline 304 → 310, TRIGGER 32 → 34, NAMED-FOR 79 → 81); definitions the gold does not carry +8 (DAN1006 ×4 — see below — ANZH302 ×2, MXEO301, HIS1005).

### 3. PROTECTED GATES

- Skeleton **55.4469 % → 55.4504 % @ 2491 (+0.0035pp)**, RAW 39.419 → 39.420 %; **≥50 1591 → 1592 (+1)**; **≥75 277 → 276 (−1, ACCEPTED AS NAMED)**; ≥90 26; 19 movers (10 up / 9 down, pp-sum +8.8), 0 outside the affected set: **ARFUN05_0_0 40.0 → 57.8** (the six drama-element list tooltips now all built), ENGS401_5_0 +2.5, ENGI302_2_0 +1.0, BLL272 / 273 / 275 / 276 +0.6–0.9, CEDW501_2_0 +0.7, HIS1005_1_0 +0.7, FRNO902_5_0 +0.5. **NAMED down:** **DAN1006_2_0 84.4 → 72.2 (the ≥75 crossing)** — the writer asked for four hovers on its dance-technique list (`Lower centre of gravity. [hover: Bending legs…]`) and the gold writes them inline as `Lower centre of gravity: bending legs…`; HIS1005_6_1 −2.7 / HIS1004_1_0 −1.0 / MXEO301_1_0 −0.7 / HIS1003_7_0 −0.5 — tooltips on a word the gold does not wrap (HIS1005 `opinion` / `document`, HIS1004 the whole `29. Subject to law.`); ENFUN05 / WJFUN304 / SSOG301 / ARFUN04 ≤ −0.1. cs 16745 / 198 / 888, body ANY 232, clean 2591 / 2633, leak 52 / 42 EXACT; tags 9557; every verifier RESULT ✓; selftests 50 / 0; the miner 195 CANDIDATE.
- Plateau (§4): +0.0035pp (< 0.02) but ≥50 +1 / ≥75 −1 (protected buckets moved) — neither; **0 of 3**.

**Recorded, not built:** the 120 drops left — 78 writer notes (kept on the drop path by design), 14 empty hosts the gold builds (BLL243 `what` / `where` / `when`, ENFUN03 / ENGI103 `verbs`, BLL252 `stanzas` / `rhythm` — the anchor is a separate run before the marker), 14 punctuated the gold builds on a term named elsewhere (ANZH205's `Sovereignty` / `Possession` / `government` / `chieftainship` one-word translations, DAN1003 `source acknowledgment`, HIS1002 `Moruroa and Fangataufa`); four new tooltips sit on a less apt last word (DAN1003 `expected`, ENFUN05 `Hill`, HIS1005 `opinion`, WJFUN304's `Kupe` definition on `tradition,`… — the last is the Round-9 `[Hinfo trigger] Kupe [` in-marker anchor, not built here: it stays dropped because its def is on the comma rule's lower-case path? — no: `A legendary…` is capitalised; it is recorded for the named-anchor path).

**Ledger:** scoped #3 since the r498 FULL (the two failed scoped_ship attempts counted) · data `elements.info_trigger_punct_anchor` · env `HOVERPUNCT_OFF` · code `ListsAndRuns.inlineMarkup` · tools `_s46_r9_itdrop.py`, `_s46_r11_split.py`, `_r499_finalise.py` · session 46 Round 11.

"""
entry = entry.replace(" (DAN1003 `expected`, ENFUN05 `Hill`, HIS1005 `opinion`, WJFUN304's `Kupe` definition on `tradition,`… — the last is the Round-9 `[Hinfo trigger] Kupe [` in-marker anchor, not built here: it stays dropped because its def is on the comma rule's lower-case path? — no: `A legendary…` is capitalised; it is recorded for the named-anchor path).",
                      " (DAN1003 `expected` for `source acknowledgment`, ENFUN05 `Hill`, HIS1005 `opinion`, WJFUN304 `tradition,` carrying the definition of `Kupe` — the writer's in-marker anchor `[Hinfo trigger] Kupe [`, a named-anchor case for a later round).")
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 499 (260620.62): THE HOVER DEFINITION AFTER THE FULL STOP (session 46 Round 11) — a woven hover def whose marker "
                "follows the sentence's punctuation is anchored (first sentence / bold / quoted / last word) instead of dropped. Env HOVERPUNCT_OFF.\n"
                + '\tstatic AppVersion = "260620.62";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 499 BASELINE (the hover definition after the full stop, "
                "`HOVERPUNCT_OFF`; SCOPED, scoped #3 since the r498 FULL; ≥75 −1 ACCEPTED AS NAMED): SCAFFOLD mean 55.4504% / >=50% 1592 / >=75% 276 / "
                ">=90% 26 / RAW 39.420% @ 2491 pairs — +0.0035pp (19 movers, 10 up / 9 down NAMED; ARFUN05_0_0 +17.8, DAN1006_2_0 −12.2 the ≥75 "
                "crossing — the gold inlines the four list definitions); cs / body / clean / leak EXACT.** Previous: **ROUND 498 BASELINE")
so = so.replace(a11, "| `HOVERPUNCT_OFF` | 499 | **THE HOVER DEFINITION AFTER THE FULL STOP** (session 46 Round 11). Reverts "
                "`elements.info_trigger_punct_anchor`: a woven hover definition whose marker follows the sentence's punctuation is dropped again "
                "(153 corpus-wide instead of 120); byte-identical to r498. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.62` (round 499 — **the hover definition after the full stop**; `HOVERPUNCT_OFF`; scoped #3 since the r498 "
                "FULL; 25 pages; skeleton 55.4504 % @ 2491, +0.0035pp, ≥50 +1, ≥75 −1 NAMED).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r499.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    hits = [i for i, l in enumerate(G) if l.strip().rstrip(",") == f'"{key}": {old}']
    assert len(hits) == 1, (key, hits); G[hits[0]] = G[hits[0]].replace(f'"{key}": {old}', f'"{key}": {new}')
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.61"', '"260620.62"'); setv("round", "498", "499")
setv("pages_ge_50", "1591", "1592"); setv("pages_ge_75", "277", "276")
insert_before("_note_r498", '    "_note_r499": "Round 499 (session 46 Round 11, 2026-09-25) — THE HOVER DEFINITION AFTER THE FULL STOP (HOVERPUNCT_OFF): 25 pages / '
              '23 modules, 31 tooltips (drops 153 -> 120, gold-matched +10); SCAFFOLD 55.4469 -> 55.4504 @ 2491 (+0.0035pp); >=50 1591 -> 1592; '
              '>=75 277 -> 276 ACCEPTED AS NAMED (DAN1006_2_0 84.4 -> 72.2: the gold writes the four list definitions inline); cs / body / clean / '
              'leak EXACT; scoped #3.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r499-finalise.bak")
i = find("- **ROUND 499 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈15:40, session 46 Round 11 — r499 (the hover definition after the full stop) SHIPPED and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r499** (260620.62); **LAST FULL = r498 (the session-46 Round 10 backstop)**; "
        "ledger **scoped #3** (5 of headroom; the two failed r499 scoped_ship attempts were counted). Ride-along patches "
        "`outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the lesson "
        "menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈14:55, session 46 Round 10"); prior = L[k]; del L[k]
k = find("- Before it: **r497**"); r497 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r498**"); L[k] = L[k].replace("- LAST SHIPPED: **r498**", "- Before it: **r498**", 1)
L.insert(k, "- LAST SHIPPED: **r499** (build 260620.62, 25 Sept ≈15:40, session 46 Round 11 — THE HOVER DEFINITION AFTER THE FULL STOP, "
         "`HOVERPUNCT_OFF`; SCOPED, **scoped #3 since the r498 FULL backstop**; ≥75 −1 ACCEPTED AS NAMED (DAN1006_2_0 84.4 → 72.2 — the gold "
         "writes the four list definitions inline); 31 tooltips on 25 pages, drops 153 → 120, gold-matched +10; **ARFUN05_0_0 40.0 → 57.8**; "
         "**skeleton 55.4469 → 55.4504 % @ 2491 (+0.0035pp)**, **≥50 1592 (+1)**, ≥75 276, ≥90 26, RAW 39.420 %; cs / body / clean / leak "
         "EXACT; `gate_baseline.json` at r499; the miner 195 CANDIDATE).")
k = find("- Before them: **r496 → r467**")
L[k] = L[k].replace("- Before them: **r496 → r467** (260620.59 → 260620.34 — the XDLS choice board's stray marker,",
                    "- Before them: **r497 → r467** (260620.60 → 260620.34 — the XDLS choice board's last declined pages, the stray marker,", 1)
assert "r497 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r498")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r498", "- Plateau window (§4): **0 of 3** — r499 +0.0035pp but ≥50 +1 / ≥75 −1 (neither); r498", 1)
k = find("- Standing facts: AppVersion **260620.61**")
L[k] = L[k].replace("AppVersion **260620.61** (r498 the hover definition's red first letter — session 46 Round 9, 25 Sept); before it 260620.60",
                    "AppVersion **260620.62** (r499 the hover definition after the full stop — session 46 Round 11, 25 Sept); before it 260620.61 (r498 "
                    "the hover definition's red first letter — session 46 Round 9); before it 260620.60", 1)
assert "260620.62" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s46-r11 (engine r499, build 260620.62, 25 Sept ≈14:55 → 15:40) · THE HOVER DEFINITION AFTER THE FULL STOP (the s46-r9 drop "
         "lane: a def whose marker follows the sentence's punctuation anchored on the first sentence / bold run / quoted phrase / last word, "
         "writer notes still dropped) · SHIPPED scoped #3, ≥75 −1 NAMED (DAN1006_2_0) after two scoped_ship FAILs (cs exact −7 → the "
         "first-sentence rule; comma over-reach → `.?!` only) · 31 tooltips, drops 153 → 120, ARFUN05_0_0 **40.0 → 57.8** · skeleton +0.0035pp, "
         "≥50 +1 · plateau 0 of 3 (neither).")
k = find("- **(s46-r9) the hover definitions after r498")
L[k] = L[k].replace("(a) **153 hover definitions (145 unique, 74 modules) are still DROPPED**",
                    "(a) **153 → 120 after r499 (the punctuation anchor, s46-r11)**; left: 78 writer notes (by design), 14 empty hosts the gold builds "
                    "(BLL243 / BLL252 / ENFUN03 / ENGI103 — the anchor is a separate run), 14 on a term named elsewhere (ANZH205's one-word "
                    "translations, DAN1003 `source acknowledgment`, HIS1002 `Moruroa and Fangataufa`) — was: 153 hover definitions (145 unique, "
                    "74 modules) DROPPED", 1)
assert "153 → 120" in L[k]
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r497 + the Round-10 no-round line (verbatim, s46 r499)\n\n" + r497 + "\n" + prior + "\n"
    "\n## Session 46 — Round 11 (engine r499) — the hover definition after the full stop\n\n" + marker + "\n"
    "- **What shipped (r499, 260620.62):** `elements.info_trigger_punct_anchor` (env `HOVERPUNCT_OFF`). Probe OFF 0; ON 25 pages / 23 modules; "
    "scoped_ship FAIL ×2 then PASS with ≥75 −1 ACCEPTED AS NAMED (DAN1006_2_0); +0.0035pp, ≥50 +1.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
