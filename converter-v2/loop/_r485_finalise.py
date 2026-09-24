#!/usr/bin/env python3
"""ROUND 485 finalise (session 44 Round 11 — the title bar's language-boundary split, TITLELANGSPLIT_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 485," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.48";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 484 BASELINE"; a11 = "| `TPLAUTOQUIZ_OFF` | 484 |"; a14 = "- **Build:** `260620.48` (round 484"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
k79 = "| 79 | Lesson page `<h1><span>` = the lesson's own title"; assert sk.count(k79) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 485 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈03:00, session 44 Round 9", "- LAST SHIPPED: **r484**",
          "- Before it: **r483**", "- Before them: **r482**", "- Plateau window (§4): **0 of 3** — r484", "- Standing facts: AppVersion 260620.48",
          "## Round log", "**Next session starts with:**", "## Session 44 — Round 11 PICK (engine r485)"):
    find(p)
entry = """## 2026-09-25 (round 485, build 260620.49) — THE TITLE BAR'S LANGUAGE-BOUNDARY SPLIT: an English run then a Māori run typed with no separator ("Online Bullying Whakaweti ā-ipurangi") ships as the two header `<h1><span>`s

### 1. WHAT CHANGED

**The find** (session 44 Round 11 — the miner's CHROME row #4, `title MISSING h1>span`, re-read by module on the Online Safety overviews): the writer typed the bilingual pair with NO separator, the Te Reo run only highlighted (`*Online Bullying* ✅*Whakaweti ā-ipurangi*`, `*OSSC301 Scams* ✅*Ngā Tāware*`, `*OSSM301 Social Media* ✅*Pāhopori*`, GEO1004 / TWHK901 / XDLS901 / XMES203 / MXEX101 likewise); the title-bar chain (pipe / line break / 2+ spaces / punctuation / dash / character / ALL-CAPS case) never splits at the English → Māori word boundary, so Claude shipped ONE joined span where the gold ships two. (The row's other shapes stay class C: the unfilled `MODULE TITLE TE REO` placeholder — OSBY101 / 201; English-only title bars whose Te Reo title the gold takes from the series — OSAH501 / OSAI501 / OSBY501 / OSGM201 / OSGM501 / OSSC501.)

**The fix:** `ContentConverter.#bilingualLangSplit`, the LAST fallback of the chain: split before the longest tail of words that are all Māori-lettered (no b c d f j l q s v x y z), open with a capital and carry a macron, the head holding a non-Māori letter and the tail no longer than 3× the head; then the two-language guard. Data `header.title_split.lang_boundary_split` {enabled, env, require_macron, tail_upper_first, max_tail_ratio 3}; env **`TITLELANGSPLIT_OFF`**, byte-identical OFF. Two over-fires found by the prototype probe and guarded: CHI1005's lower-case Māori-lettered English "routine"; ENGS101's "Exploring Te Ika a Māui" (a place name — the gold keeps one title).

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 3222 / 3222 identical**; ON 18 pages / 9 modules (CHI1005 GEO1004 MXEX101 OSBY301 OSSC301 OSSM301 TWHK901 XDLS901 XMES203 — CHI1005 outside the scored population by D14-21; its lesson pages' module-title fallback is now the English title alone, c79's single-h1 fallback). Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS**.

### 3. PROTECTED GATES

- Skeleton **55.3280 % → 55.3463 % @ 2491 (+0.0184pp)**, RAW 39.224 → 39.231 %; ≥50 1582; **≥75 275 → 277 (+2: GEO1004_0_0 70.4 → 80.0, XMES203_0_0 72.0 → 78.9)**; **≥90 25 → 26 (OSSC301_0_0 88.9 → 96.9)**; 7 movers, **7 up / 0 down** (pp-sum +45.7; OSSM301 +7.4, OSBY301 +6.8, XDLS901 +6.1, TWHK901 +0.9).
- compare_structure / body / clean / leak EXACT; every verifier RESULT line ✓; selftests green; the miner 195 CANDIDATE.
- Plateau (§4): +0.0184pp (< 0.02) but ≥75 +2 / ≥90 +1 — protected buckets moved: neither counts nor resets; **0 of 3**.

**Ledger:** scoped #3 since the r482 FULL · data `header.title_split.lang_boundary_split` · env `TITLELANGSPLIT_OFF` · code `ContentConverter.#bilingualLangSplit` · tools `_s44_r11_pick.py`, `_r485_{regen,postship}.sh`, `_r485_finalise.py` · session 44 Round 11.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 485 (260620.49): THE TITLE BAR'S LANGUAGE-BOUNDARY SPLIT (session 44 Round 11) — an English run then a Māori run with no "
                "separator ships as the two header h1 spans (ContentConverter.#bilingualLangSplit). Env TITLELANGSPLIT_OFF.\n" + '\tstatic AppVersion = "260620.49";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 485 BASELINE (the title bar's language-boundary split, "
                "`TITLELANGSPLIT_OFF`; SCOPED, scoped #3 since the r482 FULL; scoped_ship PASS): SCAFFOLD mean 55.3463% / >=50% 1582 / >=75% 277 / "
                ">=90% 26 / RAW 39.231% @ 2491 pairs — +0.0184pp (7 up / 0 down); cs / body / clean / leak EXACT.** Previous: **ROUND 484 BASELINE")
so = so.replace(a11, "| `TITLELANGSPLIT_OFF` | 485 | **THE TITLE BAR'S LANGUAGE-BOUNDARY SPLIT** (session 44 Round 11). Reverts "
                "`header.title_split.lang_boundary_split`: an English run then a Māori run with no separator ships as ONE joined h1 span again — 9 "
                "modules / 18 pages; byte-identical to r484. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.49` (round 485 — **the title bar's language-boundary split**; `TITLELANGSPLIT_OFF`; scoped #3 since the r482 "
                "FULL; 9 modules; skeleton 55.3463 % @ 2491, +0.0184pp, ≥75 +2, ≥90 +1).\n" + a14)
wr(PO, so); print("OG ok")
KL = sk.split("\n"); i79 = [i for i, l in enumerate(KL) if l.startswith(k79)][0]
KL[i79] = KL[i79].replace("| ContentConverter header titles;", "**r485 (session 44 Round 11): the bilingual PAIR typed with no separator (an "
                          "English run then a highlighted Māori run) splits at the language boundary — `header.title_split.lang_boundary_split`, "
                          "`TITLELANGSPLIT_OFF`; 9 modules; gold two spans on every measured overview.** | ContentConverter header titles;", 1)
assert "r485 (session 44 Round 11)" in KL[i79]
wr(PK, "\n".join(KL)); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r485.bak")
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
setv("build", '"260620.48"', '"260620.49"'); setv("round", "484", "485")
insert_before("_note_r484", '    "_note_r485": "Round 485 (session 44 Round 11, 2026-09-25) — THE TITLE BAR LANGUAGE-BOUNDARY SPLIT (TITLELANGSPLIT_OFF): 9 modules / '
              '18 pages; SCAFFOLD 55.3280 -> 55.3463 @ 2491 (+0.0184pp, 7 up / 0 down); RAW 39.224 -> 39.231; >=75 275 -> 277; >=90 25 -> 26; cs / '
              'body / clean / leak EXACT; scoped #3 since the r482 FULL; scoped_ship PASS.",')
setv("mean_scaffold_pct", "55.33", "55.35"); setv("pages_ge_75", "275", "277"); setv("raw_mean_pct", "39.22", "39.23")
insert_before("_note_r482_state", '    "_note_r485_state": "r485 (the title-bar language split): SCAFFOLD 55.3463 @ 2491, RAW 39.231; 7 movers (7 up / 0 down).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r485-finalise.bak")
i = find("- **ROUND 485 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈03:25, session 44 Round 11 — r485 (the title bar's language-boundary split) SHIPPED and committed; "
        "the in-flight marker is cleared). LAST SHIPPED **r485** (260620.49); **LAST FULL = r482 (the s44 backstop)**; ledger **scoped #3** (5 of "
        "headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈03:00, session 44 Round 9"); prior = L[k]; del L[k]
k = find("- Before it: **r483**"); r483 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r484**"); L[k] = L[k].replace("- LAST SHIPPED: **r484**", "- Before it: **r484**", 1)
L.insert(k, "- LAST SHIPPED: **r485** (build 260620.49, 25 Sept ≈03:25, session 44 Round 11 — THE TITLE BAR'S LANGUAGE-BOUNDARY SPLIT, "
         "`TITLELANGSPLIT_OFF`; SCOPED, **scoped #3 since the r482 FULL backstop**, scoped_ship PASS; **skeleton 55.3280 → 55.3463 % @ 2491 "
         "(+0.0184pp, 7 up / 0 down)**, ≥50 1582, **≥75 277 (+2)**, **≥90 26 (+1)**, RAW 39.231 %; cs / body / clean / leak EXACT; "
         "`gate_baseline.json` at r485; the miner 195 CANDIDATE).")
k = find("- Before them: **r482**")
L[k] = L[k].replace("- Before them: **r482**", "- Before them: **r483** (260620.47, KB c38 template autoCheck — verbatim → "
                    "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r483 (verbatim, s44 r485)'), **r482**", 1)
k = find("- Plateau window (§4): **0 of 3** — r484")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r484", "- Plateau window (§4): **0 of 3** — r485 +0.0184pp but ≥75 +2 / ≥90 +1 "
                    "(protected buckets moved: neither); r484", 1)
k = find("- Standing facts: AppVersion 260620.48")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.48 (r484", "- Standing facts: AppVersion 260620.49 (r485 the title-bar language split — "
                    "session 44 Round 11, 25 Sept); before it 260620.48 (r484", 1)
k = find("## Round log")
L.insert(k + 1, "- s44-r11 (engine r485, build 260620.49, 25 Sept 03:10 → ≈03:25) · THE TITLE BAR'S LANGUAGE-BOUNDARY SPLIT (the miner's chrome row "
         "#4 re-read: an English run + a highlighted Māori run with no separator → two h1 spans; two over-fires guarded) · SHIPPED scoped #3, "
         "scoped_ship PASS · 9 modules / 18 pages · skeleton +0.0184pp (7 up / 0 down), ≥75 +2, ≥90 +1 · plateau 0 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r485** (260620.49, "
        "the title-bar language split); LAST FULL = **r482** (the s44 backstop); ledger scoped #3; plateau **0 of 3**; 2,491 pairs; census 552 / "
        "545 / 2,679. Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs "
        "Chris #17–#19, #22.")
k = find("## Session 44 — Round 11 PICK (engine r485)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 44 — Round 11 PICK (engine r485) — THE TITLE BAR'S LANGUAGE-BOUNDARY SPLIT — SHIPPED; the PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md 'Session 44 — Round 11 PICK (engine r485) + what shipped'; the one-line summary is the s44-r11 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r483 (verbatim, s44 r485)\n\n" + r483 + "\n"
    "\n## Session 44 — Round 11 PICK (engine r485) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r485, 260620.49):** `header.title_split.lang_boundary_split` (env `TITLELANGSPLIT_OFF`; require_macron, tail_upper_first, "
    "max_tail_ratio 3) — ContentConverter.#bilingualLangSplit as the chain's last fallback. Probe OFF 3222 identical; ON 18 pages / 9 modules; "
    "scoped_ship PASS; +0.0184pp, 7 up / 0 down, ≥75 +2, ≥90 +1.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
