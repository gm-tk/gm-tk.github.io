#!/usr/bin/env python3
"""ROUND 496 finalise (session 46 Round 7 — the XDLS choice board's stray-marker scrap release, CDSCRAPREL_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 496," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.58";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 495 BASELINE"; a11 = "| `HINTFACEMARK_OFF` | 495 |"; a14 = "- **Build:** `260620.58` (round 495"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 496 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈13:05, session 46 Round 5", "- LAST SHIPPED: **r495**",
          "- Before it: **r494**", "- Before them: **r493 → r467**", "- Plateau window (§4): **0 of 3** — r495", "- Standing facts: AppVersion **260620.58**",
          "## Round log", "**Next session starts with:**", "- **(s46-r6) the XDLS choice board's five declined pages"):
    find(p)
entry = """## 2026-09-25 (round 496, build 260620.59) — THE XDLS CHOICE BOARD'S STRAY MARKER: r307 / r418's tile prepass releases what a writer's stray `[click drop image]` marker captured instead of declining the page's whole choice board (XDLS906 5.0: 48.9 → 73.4 %)

### 1. WHAT CHANGED

**The find** (session 46 Rounds 6–7 — the clickDrop refusal trace `_s46_r6_cdwhy.sh`, then the tile prepass trace `_s46_trace_cc.cjs`): the Learning-Support choice board (`[Click Drop Activity N with embedded image] Label [image … icon from LS global edits]`, XDLS902–906) is built by the r307 / r418 tile prepass on 30 of 35 lesson pages; it declines the whole row on five, each for a different reason — XDLS906 5.0: after `[Activity] **5B**` the writer typed a STRAY numberless, nameless `[click drop image]`, which opens a scrap that captures the activity's own `[H4] Where my ancestors came from` + `[body]` lines, so the prepass met "any other member = content" and gave up; XDLS906 3.0: the writer typed `[Activity] **3E**` BEFORE its `[Click Drop Activity 5] Judge` button (the button's scrap captures the activity's heading + body); XDLS903 1.0: a nameless numbered marker; XDLS904 5.0 / XDLS905 4.0: five free activity anchors for six tiles.

**The fix** (`ContentConverter.#cdTilePrepass`, data `interactive_builders.clickDrop.tile_grid.scrap_release`, env `CDSCRAPREL_OFF`): (a) a scrap whose marker is a stray (numberless, nameless — the r307 comment's own "writer's stray duplicate") RELEASES its otherwise-refused members back to the page — they render where the writer put them, inside the activity — instead of declining the row; (b) an inline marker of a `release_inline_tags` type (`info trigger`) on the SAME paragraph as a heading the prepass already releases is released with it (it fires on no page today — XDLS906 3.0 declines later on the writer's swapped order; kept as the heading release's own completion). Only a member that would have declined the row is released, so every row that built before is byte-identical.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **XDLS906_5_0 only** (+ its `_interactives.txt`): the page now carries the six choice tiles and six paired `clickDropContent` panels like its sibling pages. Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS**.

### 3. PROTECTED GATES

- Skeleton **55.4051 % → 55.4150 % @ 2491 (+0.0098pp)**, RAW 39.375 → 39.386 %; **≥50 1587 → 1588 (+1)**, ≥75 277, ≥90 26; **1 mover: XDLS906_5_0 48.9 → 73.4 (+24.4)**; body ANY 236 → 235; cs 16745 / 198 / 888 / 24, clean 2591 / 2633, leak 52 / 42 EXACT; tags 9557 / 9557; every verifier RESULT ✓; selftests 50 green / 0 fail; the miner 194 CANDIDATE.
- Plateau (§4): +0.0098pp (< 0.02) but ≥50 +1 — a protected bucket moved: neither counts nor resets; **0 of 3**.

**Recorded, not built:** the other three declined choice-board pages — XDLS906 3.0 (the swapped `[Activity]`-before-button order), XDLS903 1.0 (a nameless numbered marker), XDLS904 5.0 / XDLS905 4.0 (a sixth activity anchor consumed elsewhere).

**Ledger:** scoped #6 since the r490 FULL · data `interactive_builders.clickDrop.tile_grid.scrap_release` · env `CDSCRAPREL_OFF` · code `ContentConverter.#cdTilePrepass` · tools `_s46_r6_cdwhy.sh`, `_s46_trace_cc.cjs`, `_r496_finalise.py` · session 46 Round 7.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 496 (260620.59): THE XDLS CHOICE BOARD'S STRAY MARKER (session 46 Round 7) — the r307 tile prepass releases what a "
                "stray numberless [click drop image] marker captured. Env CDSCRAPREL_OFF.\n" + '\tstatic AppVersion = "260620.59";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 496 BASELINE (the XDLS choice board's stray marker, "
                "`CDSCRAPREL_OFF`; SCOPED, scoped #6 since the r490 FULL; scoped_ship PASS): SCAFFOLD mean 55.4150% / >=50% 1588 / >=75% 277 / >=90% "
                "26 / RAW 39.386% @ 2491 pairs — +0.0098pp (1 mover, XDLS906_5_0 +24.4), >=50 +1; body ANY 235; cs / clean / leak EXACT.** Previous: "
                "**ROUND 495 BASELINE")
so = so.replace(a11, "| `CDSCRAPREL_OFF` | 496 | **THE XDLS CHOICE BOARD'S STRAY MARKER** (session 46 Round 7). Reverts "
                "`interactive_builders.clickDrop.tile_grid.scrap_release`: a tile scrap opened by a stray numberless `[click drop image]` marker "
                "declines the page's whole choice board again (XDLS906 5.0); byte-identical to r495. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.59` (round 496 — **the XDLS choice board's stray marker**; `CDSCRAPREL_OFF`; scoped #6 since the r490 "
                "FULL; 1 page; skeleton 55.4150 % @ 2491, +0.0098pp, ≥50 +1).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r496.bak")
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
setv("build", '"260620.58"', '"260620.59"'); setv("round", "495", "496")
insert_before("_note_r495", '    "_note_r496": "Round 496 (session 46 Round 7, 2026-09-25) — THE XDLS CHOICE BOARD\'S STRAY MARKER (CDSCRAPREL_OFF): XDLS906_5_0 '
              '48.9 -> 73.4; SCAFFOLD 55.4051 -> 55.4150 @ 2491 (+0.0098pp); RAW 39.375 -> 39.386; >=50 1587 -> 1588; body ANY 236 -> 235; cs / '
              'clean / leak EXACT; scoped #6; scoped_ship PASS.",')
setv("pages_ge_50", "1587", "1588"); setv("raw_mean_pct", "39.38", "39.39")
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r496-finalise.bak")
i = find("- **ROUND 496 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈13:30, session 46 Round 7 — r496 (the XDLS choice board's stray marker) SHIPPED and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r496** (260620.59); **LAST FULL = r490 (the s45 Round 10 backstop)**; ledger "
        "**scoped #6** (2 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, "
        "10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈13:05, session 46 Round 5"); prior = L[k]; del L[k]
k = find("- Before it: **r494**"); r494 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r495**"); L[k] = L[k].replace("- LAST SHIPPED: **r495**", "- Before it: **r495**", 1)
L.insert(k, "- LAST SHIPPED: **r496** (build 260620.59, 25 Sept ≈13:30, session 46 Round 7 — THE XDLS CHOICE BOARD'S STRAY MARKER, "
         "`CDSCRAPREL_OFF`; SCOPED, **scoped #6 since the r490 FULL backstop**, scoped_ship PASS; **XDLS906_5_0 48.9 → 73.4**; **skeleton 55.4051 "
         "→ 55.4150 % @ 2491 (+0.0098pp)**, **≥50 1588 (+1)**, ≥75 277, ≥90 26, RAW 39.386 %; body ANY 235; cs / clean / leak EXACT; "
         "`gate_baseline.json` at r496; the miner 194 CANDIDATE).")
k = find("- Before them: **r493 → r467**")
L[k] = L[k].replace("- Before them: **r493 → r467** (260620.56 → 260620.34 — the BLL closing section,",
                    "- Before them: **r494 → r467** (260620.57 → 260620.34 — the carousel slide-table tail, the BLL closing section,", 1)
assert "r494 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r495")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r495", "- Plateau window (§4): **0 of 3** — r496 +0.0098pp but ≥50 +1 (neither); r495", 1)
k = find("- Standing facts: AppVersion **260620.58**")
L[k] = L[k].replace("AppVersion **260620.58** (r495 KB c5 the literal-tag leak — session 46 Round 5, 25 Sept); before it 260620.57",
                    "AppVersion **260620.59** (r496 the XDLS choice board's stray marker — session 46 Round 7, 25 Sept); before it 260620.58 (r495 KB "
                    "c5 the literal-tag leak — session 46 Round 5); before it 260620.57", 1)
assert "260620.59" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s46-r7 (engine r496, build 260620.59, 25 Sept ≈13:15 → 13:30) · THE XDLS CHOICE BOARD'S STRAY MARKER (finishing r307 / r418 on "
         "its declined pages: a stray `[click drop image]` scrap's captured lines released instead of declining the row) · SHIPPED scoped #6, "
         "scoped_ship PASS · XDLS906_5_0 **48.9 → 73.4** · skeleton +0.0098pp, ≥50 +1 · plateau 0 of 3 (neither).")
k = find("- **(s46-r6) the XDLS choice board's five declined pages")
L[k] = L[k].replace("- **(s46-r6) the XDLS choice board's five declined pages (r307 / r418 build the other 30):**",
                    "- **(s46-r6 / r7) the XDLS choice board's declined pages — XDLS906_5_0 FIXED by r496 (48.9 → 73.4); four left:**", 1)
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r494 + the r495 no-round line (verbatim, s46 r496)\n\n" + r494 + "\n" + prior + "\n"
    "\n## Session 46 — Round 7 (engine r496) — the XDLS choice board's stray marker\n\n" + marker + "\n"
    "- **What shipped (r496, 260620.59):** `interactive_builders.clickDrop.tile_grid.scrap_release` (env `CDSCRAPREL_OFF`). Probe OFF 0; ON "
    "XDLS906_5_0; scoped_ship PASS; +0.0098pp (XDLS906_5_0 +24.4), ≥50 +1.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
