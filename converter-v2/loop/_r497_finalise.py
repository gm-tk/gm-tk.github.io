#!/usr/bin/env python3
"""ROUND 497 finalise (session 46 Round 8 — the XDLS choice board's last declined pages, CDSCRAPREL2_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 497," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.59";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 496 BASELINE"; a11 = "| `CDSCRAPREL_OFF` | 496 |"; a14 = "- **Build:** `260620.59` (round 496"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 497 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈13:30, session 46 Round 7", "- LAST SHIPPED: **r496**",
          "- Before it: **r495**", "- Before them: **r494 → r467**", "- Plateau window (§4): **0 of 3** — r496", "- Standing facts: AppVersion **260620.59**",
          "## Round log", "**Next session starts with:**", "- **(s46-r6 / r7) the XDLS choice board's declined pages"):
    find(p)
entry = """## 2026-09-25 (round 497, build 260620.60) — THE XDLS CHOICE BOARD'S LAST DECLINED PAGES: r496's scrap release reaches the writer's `[Click Drop Activity N with embedded image]` scrap, and an activity anchor its OWN widget consumed counts as a panel (XDLS904 5.0 40.1 → 73.0, XDLS905 4.0 44.4 → 68.5, XDLS906 3.0 48.2 → 70.6 %)

### 1. WHAT CHANGED

**The find** (session 46 Round 8 — `_s46_scanend.cjs XDLS906 3.0 "*"` / `XDLS904 5.0 "*"`): after r496 four Learning-Support choice-board pages still declined the whole tile row. XDLS906 3.0: the writer typed `[Activity] **3E**` BEFORE its `[Click Drop Activity 5 with embedded image] Judge` button, so the button's scrap swallowed 3E's `[H2]` / `[hover definition]` / `[body]` / `[hover]` / `[3 buttons]` lines and the next button's marker — "any other member" declines the row. XDLS905 4.0 / XDLS904 5.0: five free `[Activity]` anchors for six tiles — the sixth is consumed by its activity's OWN widget (XDLS905's modal owns `4A`; XDLS904's carousel owns `5E`), so "never a tile without a panel" declined the row. XDLS904's carousel had also recovered the WRONG id (`5F`, the next anchor's tail), so its box would have shipped as 5F with an `<h3>5E</h3>` title.

**The fix** (`ContentConverter.#cdTilePrepass`, data `interactive_builders.clickDrop.tile_grid.scrap_release` keys `release_marker_pattern` / `owned_anchor_counts`, env `CDSCRAPREL2_OFF`): (c) a scrap whose marker is the writer's `[Click Drop Activity N with (image) embedded image]` form releases its otherwise-refused members back to the page (the bare `[Click Drop Activity N]` of XDLS908 — a different gold — never matches); (d) ONLY when the ordinary anchor count falls short, an anchor consumed by the widget whose `activityOwner` it is counts as a panel, and that widget's box takes the anchor's own id. Both apply only to a row that would otherwise decline, so every row that built before is byte-identical.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **XDLS904_5_0, XDLS905_4_0, XDLS906_3_0** (+ their `_interactives.txt`): each page now carries the eighteen choice-tile classes and the gold's row + five paired `clickDropContent` panels (3B–3F / 4B–4F / 5B–5F). Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS**.

### 3. PROTECTED GATES

- Skeleton **55.4150 % → 55.4469 % @ 2491 (+0.0319pp)**, RAW 39.386 → 39.419 %; **≥50 1588 → 1591 (+3)**, ≥75 277, ≥90 26; **3 movers, all up: XDLS904_5_0 40.1 → 73.0 (+32.9), XDLS905_4_0 44.4 → 68.5 (+24.2), XDLS906_3_0 48.2 → 70.6 (+22.4)**; 0 movers outside the affected set; body ANY 235 → 232; cs 16745 / 198 / 888, clean 2591 / 2633, leak 52 / 42 EXACT; tags 9557 / 9557; every verifier RESULT ✓; selftests 50 green / 0 fail; the miner 195 CANDIDATE.
- Plateau (§4): +0.0319pp ≥ 0.02 — a real gain; **resets to 0 of 3**.

**Recorded, not built:** XDLS903 1.0 (a nameless numbered marker — the last declined choice-board page); XDLS904 5.0's 5E box lacks the gold's `dropbox` class (the carousel-owned box ends before its `Share your judgments` line + upload button, which render just after it).

**Ledger:** scoped #7 since the r490 FULL (1 of headroom — the FULL backstop is due at scoped #8) · data `interactive_builders.clickDrop.tile_grid.scrap_release` (`env2`, `release_marker_pattern`, `owned_anchor_counts`) · env `CDSCRAPREL2_OFF` · code `ContentConverter.#cdTilePrepass` · tools `_s46_scanend.cjs` (ALLM=1 prints every member), `_r497_finalise.py` · session 46 Round 8.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 497 (260620.60): THE XDLS CHOICE BOARD'S LAST DECLINED PAGES (session 46 Round 8) — the writer's [Click Drop Activity N "
                "with embedded image] scrap releases its captured lines; an anchor owned by its own widget counts as a panel. Env CDSCRAPREL2_OFF.\n"
                + '\tstatic AppVersion = "260620.60";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 497 BASELINE (the XDLS choice board's last declined pages, "
                "`CDSCRAPREL2_OFF`; SCOPED, scoped #7 since the r490 FULL; scoped_ship PASS): SCAFFOLD mean 55.4469% / >=50% 1591 / >=75% 277 / >=90% "
                "26 / RAW 39.419% @ 2491 pairs — +0.0319pp (3 movers, all up: XDLS904_5_0 +32.9, XDLS905_4_0 +24.2, XDLS906_3_0 +22.4), >=50 +3; "
                "body ANY 232; cs / clean / leak EXACT.** Previous: **ROUND 496 BASELINE")
so = so.replace(a11, "| `CDSCRAPREL2_OFF` | 497 | **THE XDLS CHOICE BOARD'S LAST DECLINED PAGES** (session 46 Round 8). Reverts "
                "`interactive_builders.clickDrop.tile_grid.scrap_release`'s r497 keys (`release_marker_pattern`, `owned_anchor_counts`): the "
                "writer's `[Click Drop Activity N with embedded image]` scrap and an anchor owned by its own widget decline the page's whole choice "
                "board again (XDLS904 5.0, XDLS905 4.0, XDLS906 3.0); byte-identical to r496. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.60` (round 497 — **the XDLS choice board's last declined pages**; `CDSCRAPREL2_OFF`; scoped #7 since the "
                "r490 FULL; 3 pages; skeleton 55.4469 % @ 2491, +0.0319pp, ≥50 +3).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r497.bak")
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
setv("build", '"260620.59"', '"260620.60"'); setv("round", "496", "497")
insert_before("_note_r496", '    "_note_r497": "Round 497 (session 46 Round 8, 2026-09-25) — THE XDLS CHOICE BOARD\'S LAST DECLINED PAGES (CDSCRAPREL2_OFF): '
              'XDLS904_5_0 40.1 -> 73.0, XDLS905_4_0 44.4 -> 68.5, XDLS906_3_0 48.2 -> 70.6; SCAFFOLD 55.4150 -> 55.4469 @ 2491 (+0.0319pp); RAW '
              '39.386 -> 39.419; >=50 1588 -> 1591; body ANY 235 -> 232; cs / clean / leak EXACT; scoped #7; scoped_ship PASS.",')
setv("pages_ge_50", "1588", "1591"); setv("raw_mean_pct", "39.39", "39.42")
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r497-finalise.bak")
i = find("- **ROUND 497 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈14:05, session 46 Round 8 — r497 (the XDLS choice board's last declined pages) SHIPPED and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r497** (260620.60); **LAST FULL = r490 (the s45 Round 10 backstop)**; ledger "
        "**scoped #7** (1 of headroom — the FULL backstop is due at scoped #8). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 "
        "pages) / `_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈13:30, session 46 Round 7"); prior = L[k]; del L[k]
k = find("- Before it: **r495**"); r495 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r496**"); L[k] = L[k].replace("- LAST SHIPPED: **r496**", "- Before it: **r496**", 1)
L.insert(k, "- LAST SHIPPED: **r497** (build 260620.60, 25 Sept ≈14:05, session 46 Round 8 — THE XDLS CHOICE BOARD'S LAST DECLINED PAGES, "
         "`CDSCRAPREL2_OFF`; SCOPED, **scoped #7 since the r490 FULL backstop**, scoped_ship PASS; **XDLS904_5_0 40.1 → 73.0, XDLS905_4_0 44.4 → "
         "68.5, XDLS906_3_0 48.2 → 70.6**; **skeleton 55.4150 → 55.4469 % @ 2491 (+0.0319pp)**, **≥50 1591 (+3)**, ≥75 277, ≥90 26, RAW 39.419 %; "
         "body ANY 232; cs / clean / leak EXACT; `gate_baseline.json` at r497; the miner 195 CANDIDATE).")
k = find("- Before them: **r494 → r467**")
L[k] = L[k].replace("- Before them: **r494 → r467** (260620.57 → 260620.34 — the carousel slide-table tail,",
                    "- Before them: **r495 → r467** (260620.58 → 260620.34 — the literal-tag leak, the carousel slide-table tail,", 1)
assert "r495 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r496")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r496", "- Plateau window (§4): **0 of 3** — r497 +0.0319pp (a real gain: reset); r496", 1)
k = find("- Standing facts: AppVersion **260620.59**")
L[k] = L[k].replace("AppVersion **260620.59** (r496 the XDLS choice board's stray marker — session 46 Round 7, 25 Sept); before it 260620.58",
                    "AppVersion **260620.60** (r497 the XDLS choice board's last declined pages — session 46 Round 8, 25 Sept); before it 260620.59 "
                    "(r496 the XDLS choice board's stray marker — session 46 Round 7); before it 260620.58", 1)
assert "260620.60" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s46-r8 (engine r497, build 260620.60, 25 Sept ≈13:35 → 14:05; compaction #1 at 13:36) · THE XDLS CHOICE BOARD'S LAST DECLINED "
         "PAGES (r496's scrap release extended: (c) the writer's `[Click Drop Activity N with embedded image]` scrap releases its captured lines, "
         "(d) an anchor owned by its own widget counts as a panel and gives that box its id) · SHIPPED scoped #7, scoped_ship PASS · XDLS904_5_0 "
         "**40.1 → 73.0**, XDLS905_4_0 **44.4 → 68.5**, XDLS906_3_0 **48.2 → 70.6** · skeleton +0.0319pp, ≥50 +3, body ANY −3 · plateau reset (0 of 3).")
k = find("- **(s46-r6 / r7) the XDLS choice board's declined pages")
L[k] = ("- **(s46-r6 → r8) the XDLS choice board's declined pages — XDLS906_5_0 FIXED by r496; XDLS906_3_0 / XDLS905_4_0 / XDLS904_5_0 FIXED by "
        "r497; ONE left:** XDLS903_1_0 (a nameless numbered marker — `ContentConverter.#cdTilePrepass`). **Residue:** XDLS904_5_0's 5E box "
        "(carousel-owned) lacks the gold's `dropbox` class — the carousel bundle ends before its `[Body] Share your judgments` + `[3 buttons]` "
        "upload line, which render just after the box.")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r495 + the r496 no-round line (verbatim, s46 r497)\n\n" + r495 + "\n" + prior + "\n"
    "\n## Session 46 — Round 8 (engine r497) — the XDLS choice board's last declined pages\n\n" + marker + "\n"
    "- **What shipped (r497, 260620.60):** `interactive_builders.clickDrop.tile_grid.scrap_release` keys `release_marker_pattern` / "
    "`owned_anchor_counts` (env `CDSCRAPREL2_OFF`). Probe OFF 0; ON XDLS904_5_0 / XDLS905_4_0 / XDLS906_3_0; scoped_ship PASS; +0.0319pp, ≥50 +3.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
