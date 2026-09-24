#!/usr/bin/env python3
"""ROUND 479 finalise (session 44 Round 2 — KB 07B: the bilingual proverb table is the whakatauki box, PROVERBBOX_OFF) —
BUILD_CHANGELOG.md (prepend), Config.js AppVersion 260620.42 -> 260620.43, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (build / round /
notes / skeleton / cs), KB_AMALGAMATION_STATUS.md (a §D 07B row), LOOP_STATE.md (marker cleared, Position, plateau, round log, next-session
line, Follow-up; the PICK → archive). Line edits only; .bak kept; nothing written until every anchor is found. WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 479," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.42";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 478 BASELINE"; a11 = "| `LEADLINKS_OFF` | 478 |"; a14 = "- **Build:** `260620.42` (round 478"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK); KL = sk.split("\n")
kd = [i for i, l in enumerate(KL) if l.startswith('| ~~—~~ | 07B MTK "Activity Structure" — the `[Activity: Embedded]')]; assert len(kd) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 479 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈00:05, session 44 Round 1", "- LAST SHIPPED: **r478**",
          "- Before it: **r477**", "- Before them: **r476**", "- Plateau window (§4): **2 of 3** — r478", "- Standing facts: AppVersion 260620.42",
          "## Round log", "**Next session starts with:**", "## Session 44 — Round 2 PICK (engine r479)", "- **(r453) The TRR family's LESSON pages"):
    find(p)

entry = """## 2026-09-25 (round 479, build 260620.43) — KB 07B "WHAKATAUKI / PROVERB": the bilingual proverb table (`[H1] Proverb ║ [H1] Whakataukī`) renders as ONE `div.whakatauki` — the heading row dropped, the proverb (+ its author) inside, commentary after

### 1. WHAT CHANGED

**The find** (session 44 Round 2 — the loss ledger by family re-cut on r478, `outputs/_s44_r2_famloss.py`: TRR1 is the lowest-scoring large family, 68 pages at 41.6 %; its pages triangulated with `outputs/_s44_skdump.py` / `_s44_famdiff.py`): 21 of the 23 Bilingual Writers Templates write the module's proverb as a bilingual table row `[H1] Proverb ║ [H1] Whakataukī | Whakatauākī:` followed by `[Body] <english> ║ [Body] <māori>` (`outputs/_s44_r2_proverb.cjs`; TRR104 / TRR105 have no Claude build). The gold renders a `div.whakatauki` on **23 / 23** Bilingual modules (`outputs/_s44_r2_whakform.py`) with the heading row dropped (22 / 23 — TRR108 keeps it as two h2s); Claude rendered **0**: `h3 reo "Whakataukī | Whakatauākī:"` + `h3 eng "Proverb"` + loose paragraphs — `BilingualBuilder.bilingualContainer` builds the box only for a table led by a `[Whakatauki]` TAG, which these tables never carry, so the row reached `bilingualRows` as ordinary content.

**The fix** (KB 07B §7 "Whakatauki / Proverb": `<div class="whakatauki"><p reo>…</p><p eng>…</p>` + an optional author line; the TRR107 h3 variation named): `BilingualBuilder.bilingualRows` — a row whose folded English cell matches `proverb_box.eng_head_pattern` and Māori cell `reo_head_pattern` (red markers, `[tags]`, bold stripped) is dropped and the NEXT row renders through the new `#proverbBox` as ONE box in the table's own column: the proverb paragraph(s), joined while a quote is still open (TRR203 / TRR304's two-line proverb), bold / italic stripped, Māori first; a trailing short line (≤ 6 words, no terminal punctuation) is the author — in both cells `p > span reo + span eng` (the TRR102 / 103 / 106 gold), one identical name a plain `p` (PMT101); a heading-led cell keeps its heading + paragraphs inside, reo block then eng block (TRR107); any other paragraph is commentary AFTER the box (TRR114's gold); media after that. Data `Emit_Templates.elements.dual_language.proverb_box` {enabled, env, eng_head_pattern, reo_head_pattern, open, close, author_max_words 6}; env **`PROVERBBOX_OFF`**, byte-identical OFF.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 3222 / 3222 identical**; ON 22 pages / 21 modules (PMT101 PNR101 PNR102 PNR104 PNR107 TRR102 TRR103 TRR106–TRR116 TRR203 TRR301 TRR304 — `outputs/_affected_r479.txt`, the 21 predicted by the WT census exactly; PNR101 twice — its module-content table on 0.0 repeats the proverb).
- Regeneration of the 21 + the 12-module spot-check (`_r479_regen.sh`): 0 truly stale, 12 / 12 byte-identical; `scoped_ship.sh` containment OK (21 ⊆ 21); its decomposition flagged ≥50 −1 → committed NAMED (`_r479_commit_named.sh`, `--accept-named "skeleton pages >=50%"`).

### 3. PROTECTED GATES

- Skeleton **55.2333 % → 55.2477 % @ 2491 (+0.0144pp)**, RAW 39.194 → 39.200 %; 22 movers (**20 up / 2 down**, pp-sum +35.9), none outside the affected set: PNR107_0_0 +7.8, TRR301_0_0 +5.8, TRR203_0_0 +5.5, TRR110_1_0 +4.7, TRR106_1_0 +2.6, TRR116_1_0 +2.3 …; **≥50 1577 → 1576 — NAMED: TRR108_0_0 50.9 → 49.5** (the one gold, 1 / 23, that keeps the writer's "Whakataukī | Proverb" heading row above its box); TRR114_0_0 63.9 → 63.0 (the gold holds TRR114's proverb on page 1.0); ≥75 275; ≥90 25.
- compare_structure **exact 16759 → 16771 (+12), missing 903 → 872 (−31)**, EXTRA 208; body ANY 238; clean 2587 / 2633; leak 75 / 46 — held or improved; every verifier RESULT line ✓; 17 selftests + the skeleton selftest green (50 PASS / GREEN, 0 FAIL); the feature index green; the miner 197 CANDIDATE.
- Plateau (§4): a KB-rule round; neither counts nor resets: **2 of 3** stands.

**Ledger:** scoped #5 since the r474 FULL · data `elements.dual_language.proverb_box` · env `PROVERBBOX_OFF` · code `BilingualBuilder.bilingualRows` / `#proverbCfg` / `#isProverbHead` / `#proverbBox` · tools `_s44_r2_{famloss,actlabel,whakform,pick}.py`, `_s44_r2_proverb.cjs`, `_s44_{skdump,famdiff}.py`, `_r479_{regen,commit_named,postship}.sh`, `_r479_finalise.py` · session 44 Round 2.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 479 (260620.43): KB 07B WHAKATAUKI (session 44 Round 2). The bilingual `[H1] Proverb ║ [H1] Whakataukī` row + its "
                "proverb row render as ONE div.whakatauki (BilingualBuilder.#proverbBox). Env PROVERBBOX_OFF.\n"
                '\tstatic AppVersion = "260620.43";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 479 BASELINE (KB 07B the bilingual proverb table is the "
                "whakatauki box, `PROVERBBOX_OFF`; SCOPED, scoped #5 since the r474 FULL): SCAFFOLD mean 55.2477% / >=50% 1576 / >=75% 275 / "
                ">=90% 25 / RAW 39.200% @ 2491 pairs — +0.0144pp (20 up / 2 down); ≥50 −1 NAMED (TRR108_0_0 50.9 → 49.5, the one gold that "
                "keeps the proverb heading); cs exact 16771 (+12), missing 872 (−31); body / clean / leak EXACT.** Previous: **ROUND 478 BASELINE")
so = so.replace(a11, "| `PROVERBBOX_OFF` | 479 | **KB 07B THE BILINGUAL PROVERB TABLE IS THE WHAKATAUKI BOX** (session 44 Round 2). Reverts "
                "`elements.dual_language.proverb_box`: the `[H1] Proverb ║ [H1] Whakataukī` row + its proverb row render as two headings + loose "
                "paragraphs again — 21 modules / 22 pages; byte-identical to r478. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.43` (round 479 — **KB 07B: the bilingual proverb table is the whakatauki box**; `PROVERBBOX_OFF`; scoped "
                "#5 since the r474 FULL; 21 modules; skeleton 55.2477 % @ 2491, +0.0144pp, ≥50 −1 NAMED; cs exact 16771, missing 872).\n" + a14)
wr(PO, so); print("OG ok")
KL.insert(kd[0] + 1, "| ~~—~~ | 07B MTK \"Whakatauki / Proverb\" — the bilingual proverb (`[H1] Proverb ║ [H1] Whakataukī` + the proverb row) is "
          "`div.whakatauki` holding `p reo` + `p eng` (+ the author), the heading row dropped; commentary after the box | **SHIPPED round 479 "
          "(2026-09-25, session 44 Round 2)** — `elements.dual_language.proverb_box`, `PROVERBBOX_OFF`; 21 modules / 22 pages; Claude boxes 0 → 21 "
          "modules (the gold 23 / 23); +0.0144pp, cs exact +12 / missing −31; TRR108 (the one gold keeping the heading) NAMED. |")
wr(PK, "\n".join(KL)); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r479.bak")
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
setv("build", '"260620.42"', '"260620.43"'); setv("round", "478", "479")
insert_before("_note_r478", '    "_note_r479": "Round 479 (session 44 Round 2, 2026-09-25) — KB 07B THE BILINGUAL PROVERB TABLE IS THE WHAKATAUKI BOX '
              '(PROVERBBOX_OFF): 21 modules / 22 pages; SCAFFOLD 55.2333 -> 55.2477 @ 2491 (+0.0144pp, 20 up / 2 down); RAW 39.194 -> 39.200; '
              '>=50 1577 -> 1576 NAMED (TRR108_0_0 50.9 -> 49.5, the one gold keeping the proverb heading); cs exact 16759 -> 16771, missing 903 -> 872; '
              'body / clean / leak EXACT; scoped #5 since the r474 FULL; committed NAMED.",')
setv("mean_scaffold_pct", "55.23", "55.25"); setv("pages_ge_50", "1577", "1576"); setv("raw_mean_pct", "39.19", "39.2")
insert_before("_note_r478_state", '    "_note_r479_state": "r479 (the whakatauki box): SCAFFOLD 55.2477 @ 2491, RAW 39.200; 22 movers (20 up / 2 down).",')
setv("exact_chain", "16759", "16771"); setv("claude_missing_container", "903", "872")
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r479-finalise.bak")
i = find("- **ROUND 479 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈00:40, session 44 Round 2 — r479 (KB 07B, the bilingual proverb table is the whakatauki box) "
        "SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r479** (260620.43); **LAST FULL = r474**; ledger **scoped #5** "
        "(3 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈00:05, session 44 Round 1"); prior = L[k]; del L[k]
k = find("- Before it: **r477**"); r477 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r478**"); L[k] = L[k].replace("- LAST SHIPPED: **r478**", "- Before it: **r478**", 1)
L.insert(k, "- LAST SHIPPED: **r479** (build 260620.43, 25 Sept ≈00:40, session 44 Round 2 — KB 07B THE BILINGUAL PROVERB TABLE IS THE "
         "WHAKATAUKI BOX, `PROVERBBOX_OFF`; SCOPED, **scoped #5 since the r474 FULL**, committed NAMED; **skeleton 55.2333 → 55.2477 % @ 2491 "
         "(+0.0144pp, 20 up / 2 down)**, **≥50 1576 (−1 NAMED: TRR108_0_0)**, ≥75 275, ≥90 25, RAW 39.200 %; **cs exact 16771 (+12), missing 872 "
         "(−31)**; body / clean / leak EXACT; `gate_baseline.json` at r479; the miner 197 CANDIDATE).")
k = find("- Before them: **r476**")
L[k] = L[k].replace("- Before them: **r476**", "- Before them: **r477** (260620.41, KB c75 for gathered body text — verbatim → "
                    "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r477 (verbatim, s44 r479)'), **r476**", 1)
k = find("- Plateau window (§4): **2 of 3** — r478")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r478", "- Plateau window (§4): **2 of 3** — r479 a KB-rule round (+0.0144pp; "
                    "neither counts nor resets); r478", 1)
k = find("- Standing facts: AppVersion 260620.42")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.42 (r478", "- Standing facts: AppVersion 260620.43 (r479 KB 07B the bilingual "
                    "whakatauki box — session 44 Round 2, 25 Sept); before it 260620.42 (r478", 1)
k = find("## Round log")
L.insert(k + 1, "- s44-r2 (engine r479, build 260620.43, 25 Sept 00:05 → ≈00:40) · KB 07B THE BILINGUAL PROVERB TABLE IS THE WHAKATAUKI BOX "
         "(found on the loss ledger's TRR1 lane: 21 / 23 Bilingual WTs, gold 23 / 23 boxes, Claude 0) · SHIPPED scoped #5, committed NAMED · 21 "
         "modules / 22 pages · skeleton +0.0144pp (20 up / 2 down), ≥50 −1 NAMED (TRR108_0_0), cs exact +12 / missing −31 · plateau 2 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r479** (260620.43, "
        "KB 07B the bilingual whakatauki box); LAST FULL = **r474**; ledger scoped #5; plateau **2 of 3**; 2,491 pairs; census 552 / 545 / 2,679. "
        "Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("- **(r453) The TRR family's LESSON pages")
L.insert(k, "- **(s44-r2) THE TRR1 LESSON-PAGE LANE — the loss ledger's lowest-scoring large family (68 pages, 41.6 % on r478; its 55 lesson pages "
         "18–51 %).** `_s44_famdiff.py '^TRR1' --pages '_[1-9]'` ranks its line classes (activity EXTRA p 492 / body EXTRA p 356 — hand-off "
         "dumps + the unboxed intros; body EXTRA / MISSING div.row; activity EXTRA audio 247; p>b bold 336 …). Taken: the whakatauki box (r479). "
         "Left, each measured: (a) the `Activity NX: ║ Ngohe NX:` + `[H2]` intro table the gold boxes TOGETHER with the following `[Activity: "
         "Embedded]` table (KB 07B 'Activity Structure') — 52 tables in TRR116 (43) / TRR106 (9) only, gold boxes the title 47 / 50, Claude 0 — "
         "≈ 12 pages / 2 modules, a §1d family-dialect candidate (`_s44_r2_actlabel.py`); (b) the reo = eng identical heading pair (`h3 reo Hea` + "
         "`h3 eng Hea`) the gold ships ONCE; (c) the `[AudioHover]` / `[H2] word` / `[Audio]` line the gold ships as `p.center-text.sassoonI-text > "
         "span.audioButton + span` (Claude: h3 ×2 + audio ×2); (d) the phonics letter rows (`p>b a e i o u`) the gold builds as the audioImage grid "
         "(TRR102); (e) writer bold inside bilingual prose (gold plain). Size each per family before a round.")
k = find("## Session 44 — Round 2 PICK (engine r479)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 44 — Round 2 PICK (engine r479) — KB 07B THE BILINGUAL PROVERB TABLE IS THE WHAKATAUKI BOX — SHIPPED; the PICK + "
         "what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 44 — Round 2 PICK (engine r479) + what shipped'; the one-line summary is the "
         "s44-r2 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r477 (verbatim, s44 r479)\n\n" + r477 + "\n"
    "\n## Session 44 — Round 2 PICK (engine r479) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r479, 260620.43):** `elements.dual_language.proverb_box` (env `PROVERBBOX_OFF`) — bilingualRows drops the proverb "
    "heading row and #proverbBox renders the next row as one div.whakatauki (proverb joined while a quote is open, bold / italic stripped; "
    "author span pair / plain p; heading-led cell kept whole; commentary + media after). Probe OFF 3222 identical; ON 22 pages / 21 modules; "
    "two fixes during the round (`&quot;` in the quote count — TRR203; one identical author name → plain p — PMT101); scoped_ship containment "
    "OK, ≥50 −1 → committed NAMED; skeleton +0.0144pp (20 up / 2 down); cs exact +12, missing −31.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
