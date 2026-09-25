#!/usr/bin/env python3
"""ROUND 500 finalise (session 46 Round 12 — the back-to-back split trigger, TRIGHOST_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 500," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.62";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 499 BASELINE"; a11 = "| `HOVERPUNCT_OFF` | 499 |"; a14 = "- **Build:** `260620.62` (round 499"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 500 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈15:40, session 46 Round 11", "- LAST SHIPPED: **r499**",
          "- Before it: **r498**", "- Before them: **r497 → r467**", "- Plateau window (§4): **0 of 3** — r499", "- Standing facts: AppVersion **260620.62**",
          "## Round log", "**Next session starts with:**", "- **(s46-r9) the hover definitions after r498"):
    find(p)
entry = """## 2026-09-25 (round 500, build 260620.63) — THE BACK-TO-BACK SPLIT TRIGGER: a split-bracket hover trigger that follows another one anchors on the sentence, not on the closer the first one emptied (12 pages / 12 modules; the broken sentences rejoined; CEDO105_3_0 70.2 → 76.6 %)

### 1. WHAT CHANGED

**The find** (session 46 Round 12 — r499's residue: the 16 drops with an EMPTY host, `_s46_items.cjs BLL243`): the split-bracket trigger form — `…such as who [HInfo trigger: ] asks about a character ] , what [HInfo trigger: ] asks about a thing or idea ] , where …` (red opener, the definition black, a red `]` closer whose black tail continues the sentence) — anchored on `items[i-1]`. For the SECOND trigger of a run that item is the `]` closer the first trigger had just emptied, so its sentinel began a bare line: the definition was DROPPED (16 of r499's 120 drops; the gold builds 14 — BLL243 `what` / `where` / `when`, BLL252 `stanzas` / `rhythm`, ENFUN03 / ENGI103 `verbs`, ENFUN04 `antonyms`, CEDO105 `codes`, OSAI401 `legal` …) and the sentence broke into separate paragraphs (`<p> , where</p>`, `<p> , or when</p>`, an empty `<p></p>`).

**The fix** (`InteractiveScanner` inline-trigger split-bracket branch, data `elements.info_trigger_inline.closer_host_skip_empty`, env `TRIGHOST_OFF`): when `items[i-1]` is an emptied item, the nearest preceding item of the SAME paragraph that still carries text hosts the sentinel — the rule the self-closed branch and the hover weave already follow.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **12 pages / 12 modules** (BLL243 BLL245 BLL252 BLL275 BLLR203 CEDO105 ENFUN03 ENFUN04 ENGC301 ENGI103 OSAI401 TEFUN05), each diffed: every one rejoins a sentence the writer typed as one paragraph and builds its tooltips (`who, what, where, or when` on BLL243 1.1; `lines and stanzas, … a rhythm` on BLL252; `subjects and verbs to make some sentences` on ENFUN03 / ENGI103). Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS** (no dip).
- Companion (`_s46_r9_itdrop.py`): drops **120 → 103** — every empty-host case gone; the rest are 78 writer notes (by design), 14 on a term named elsewhere, 2 after a stray `[`.

### 3. PROTECTED GATES

- Skeleton **55.4504 % → 55.4588 % @ 2491 (+0.0084pp)**, RAW 39.420 → 39.425 %; ≥50 1592; **≥75 276 → 277 (+1)**; ≥90 26; **10 movers, all up** (pp-sum +21.0), 0 outside the affected set: **CEDO105_3_0 70.2 → 76.6** (the ≥75 crossing), BLL252_2_0 +3.4, ENGI103_2_0 +3.2, OSAI401_4_0 +3.0, BLL243_1_1 +1.9, BLLR203_5_0 +1.1, ENFUN04 / BLL245 +0.6, ENFUN03 / TEFUN05 +0.4; **cs exact 16745 → 16746 (+1)**; EXTRA 198, missing 888, body ANY 232, clean 2591 / 2633, leak 52 / 42 EXACT; tags 9557; every verifier RESULT ✓; selftests 50 / 0; the miner 195 CANDIDATE.
- Plateau (§4): +0.0084pp (< 0.02) but ≥75 +1 / cs exact +1 (protected gates moved) — neither; **0 of 3**.

**Recorded, not built:** BLL245's `<b>ho</b> the events happen to.` and TEFUN05's `ow you expect…` / `ow it actually works…` — first letters split off in other marker shapes than r498's (a bold `W`, a red `H` inside the split-bracket opener): the r498 residue list.

**Ledger:** scoped #4 since the r498 FULL · data `elements.info_trigger_inline.closer_host_skip_empty` · env `TRIGHOST_OFF` · code `InteractiveScanner` (the split-bracket inline trigger) · tools `_s46_items.cjs`, `_s46_r9_itdrop.py`, `_r500_finalise.py` · session 46 Round 12.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 500 (260620.63): THE BACK-TO-BACK SPLIT TRIGGER (session 46 Round 12) — a split-bracket hover trigger after another "
                "one anchors on the sentence, not the emptied closer. Env TRIGHOST_OFF.\n" + '\tstatic AppVersion = "260620.63";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 500 BASELINE (the back-to-back split trigger, "
                "`TRIGHOST_OFF`; SCOPED, scoped #4 since the r498 FULL; scoped_ship PASS): SCAFFOLD mean 55.4588% / >=50% 1592 / >=75% 277 / >=90% "
                "26 / RAW 39.425% @ 2491 pairs — +0.0084pp (10 movers, all up; CEDO105_3_0 +6.4), >=75 +1; cs exact 16746 (+1); body / clean / "
                "leak EXACT.** Previous: **ROUND 499 BASELINE")
so = so.replace(a11, "| `TRIGHOST_OFF` | 500 | **THE BACK-TO-BACK SPLIT TRIGGER** (session 46 Round 12). Reverts "
                "`elements.info_trigger_inline.closer_host_skip_empty`: a split-bracket hover trigger that follows another one anchors on the "
                "emptied `]` closer again — its definition dropped, the sentence broken into paragraphs (BLL243 `<p> , where</p>`); "
                "byte-identical to r499. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.63` (round 500 — **the back-to-back split trigger**; `TRIGHOST_OFF`; scoped #4 since the r498 FULL; "
                "12 pages; skeleton 55.4588 % @ 2491, +0.0084pp, ≥75 +1, cs exact +1).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r500.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    hits = [i for i, l in enumerate(G) if l.strip().rstrip(",") == f'"{key}": {old}']
    assert len(hits) == 1, (key, hits); G[hits[0]] = G[hits[0]].replace(f'"{key}": {old}', f'"{key}": {new}')
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.62"', '"260620.63"'); setv("round", "499", "500")
setv("pages_ge_75", "276", "277"); setv("mean_scaffold_pct", "55.45", "55.46"); setv("exact_chain", "16745", "16746")
insert_before("_note_r499", '    "_note_r500": "Round 500 (session 46 Round 12, 2026-09-25) — THE BACK-TO-BACK SPLIT TRIGGER (TRIGHOST_OFF): 12 pages / 12 modules '
              '(sentences rejoined, tooltips built; drops 120 -> 103); SCAFFOLD 55.4504 -> 55.4588 @ 2491 (+0.0084pp), 10 movers all up; >=75 276 -> '
              '277; cs exact 16745 -> 16746; body / clean / leak EXACT; scoped #4; scoped_ship PASS.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r500-finalise.bak")
i = find("- **ROUND 500 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈15:55, session 46 Round 12 — r500 (the back-to-back split trigger) SHIPPED and committed; "
        "the in-flight marker is cleared). LAST SHIPPED **r500** (260620.63); **LAST FULL = r498 (the session-46 Round 10 backstop)**; ledger "
        "**scoped #4** (4 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` "
        "(buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈15:40, session 46 Round 11"); prior = L[k]; del L[k]
k = find("- Before it: **r498**"); r498 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r499**"); L[k] = L[k].replace("- LAST SHIPPED: **r499**", "- Before it: **r499**", 1)
L.insert(k, "- LAST SHIPPED: **r500** (build 260620.63, 25 Sept ≈15:55, session 46 Round 12 — THE BACK-TO-BACK SPLIT TRIGGER, `TRIGHOST_OFF`; "
         "SCOPED, **scoped #4 since the r498 FULL backstop**, scoped_ship PASS; 12 pages, the broken sentences rejoined and their tooltips "
         "built, drops 120 → 103; **CEDO105_3_0 70.2 → 76.6**; **skeleton 55.4504 → 55.4588 % @ 2491 (+0.0084pp)**, ≥50 1592, **≥75 277 (+1)**, "
         "≥90 26, RAW 39.425 %; **cs exact 16746 (+1)**; body / clean / leak EXACT; `gate_baseline.json` at r500; the miner 195 CANDIDATE).")
k = find("- Before them: **r497 → r467**")
L[k] = L[k].replace("- Before them: **r497 → r467** (260620.60 → 260620.34 — the XDLS choice board's last declined pages,",
                    "- Before them: **r498 → r467** (260620.61 → 260620.34 — the hover definition's red first letter, the XDLS choice board's last declined pages,", 1)
assert "r498 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r499")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r499", "- Plateau window (§4): **0 of 3** — r500 +0.0084pp but ≥75 +1 / cs exact +1 (neither); r499", 1)
k = find("- Standing facts: AppVersion **260620.62**")
L[k] = L[k].replace("AppVersion **260620.62** (r499 the hover definition after the full stop — session 46 Round 11, 25 Sept); before it 260620.61",
                    "AppVersion **260620.63** (r500 the back-to-back split trigger — session 46 Round 12, 25 Sept); before it 260620.62 (r499 the hover "
                    "definition after the full stop — session 46 Round 11); before it 260620.61", 1)
assert "260620.63" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s46-r12 (engine r500, build 260620.63, 25 Sept ≈15:37 → 15:55) · THE BACK-TO-BACK SPLIT TRIGGER (r499's empty-host drops: the "
         "second split-bracket trigger anchored on the closer the first one emptied — definition dropped, sentence broken into paragraphs) · "
         "SHIPPED scoped #4, scoped_ship PASS · 12 pages, drops 120 → 103 · skeleton +0.0084pp, 10 up / 0 down, ≥75 +1, cs exact +1 · plateau "
         "0 of 3 (neither).")
k = find("- **(s46-r9) the hover definitions after r498")
L[k] = L[k].replace("(a) **153 → 120 after r499 (the punctuation anchor, s46-r11)**; left: 78 writer notes (by design), 14 empty hosts the gold builds "
                    "(BLL243 / BLL252 / ENFUN03 / ENGI103 — the anchor is a separate run),",
                    "(a) **153 → 120 after r499 (the punctuation anchor, s46-r11) → 103 after r500 (the back-to-back split trigger, s46-r12 — every "
                    "empty host gone)**; left: 78 writer notes (by design), 2 after a stray `[`,", 1)
assert "→ 103 after r500" in L[k]
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r498 + the r499 no-round line (verbatim, s46 r500)\n\n" + r498 + "\n" + prior + "\n"
    "\n## Session 46 — Round 12 (engine r500) — the back-to-back split trigger\n\n" + marker + "\n"
    "- **What shipped (r500, 260620.63):** `elements.info_trigger_inline.closer_host_skip_empty` (env `TRIGHOST_OFF`). Probe OFF 0; ON 12 "
    "pages / 12 modules; scoped_ship PASS; +0.0084pp, 10 up / 0 down, ≥75 +1, cs exact +1.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
