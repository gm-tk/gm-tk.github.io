#!/usr/bin/env python3
"""ROUND 453 — refresh reference/tests/gate_baseline.json IN PLACE (line edits; the file mixes escaped and raw Unicode, so a
json re-dump would rewrite hundreds of unrelated lines). Every protected field + the r453 notes. Writes a .pre-r453.bak.
Run under WSL from anywhere."""
import io, os, json, shutil
P = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests", "gate_baseline.json"))
shutil.copyfile(P, P + ".pre-r453.bak")
L = io.open(P, encoding="utf-8").read().split("\n")
def setv(key, old, new, occurrence=1):
    n = 0
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": ') :
            n += 1
            if n == occurrence:
                assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
                L[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}')
                return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            L.insert(i, line); return
    raise SystemExit(f"anchor not found {key}")
def insert_after_idx(i, line):
    L.insert(i + 1, line)

N_META = ('    "_note_r453": "Round 453 (session 41 Round 1, 2026-09-24; the loss ledger\'s lowest large family + the recognition lane) — '
          'THE TABLE-CELL TITLE BAR OPENS THE DOCUMENT + THE MTK OVERVIEW-TABLE TABS (KB 07A §4 / 07D §19.1): the TRR family types its '
          '[TITLE BAR] inside a bilingual table cell the content-start chain never read, so the overview tables (and TRR116 lessons 1–4, '
          'TRR107 lesson 1, TRR304 lesson 1) were trimmed as front matter; now kept and composed into the KB 5-tab bilingual menu, the '
          '[H1] TRR900 introduction unfolded as body. TABLETB_OFF / REOOVTABS_OFF. SCOPED ship #1 since the r452 FULL (the 20 Bilingual '
          'modules + 12 spot-check): 13 modules / 59 files changed, 10 pages NEW. POPULATION 2477 -> 2487 pairs (§1e): the PRE-EXISTING '
          '2477 pairs 54.7484 -> 54.7695 (+0.0211pp; 12 up / 2 down — TRR107_1.0 / 2.0 NAMED, the gold lesson pages are EMPTY shells); '
          'the whole population 54.7079 (-0.0405pp = the 10 restored pages entering at a 39.4 % mean); >=50 1544 -> 1549, >=75 260 -> 265. '
          'cs matched 18178 -> 18463: exact 15657 -> 15855, missing 796 -> 840 (+44, every one on the +285 newly compared restored elements; '
          'no pre-existing element lost its container); body ANY 237 -> 238 (+1 TRR108_0_0 — its introduction holds the writer\'s own '
          '[Tabs: …] widget request, a hand-off box, A1); clean 2613/2658 -> 2623/2668; leak 75/45 HELD. Accepted as NAMED '
          '(_fastloop_diff --accept-named, outputs/_r453_fastloop_named.log; the split outputs/_r453_popsplit.log / _r453_split3.log).",')
N_SK = ('    "_note_r453_state": "r453 (the table-cell title bar + the MTK overview-table tabs): pairs 2477 -> 2487 (+10 restored TRR pages). '
        'PRE-EXISTING population 54.7484 -> 54.7695 (+0.0211pp); whole 54.7079. Movers 14 (12 up / 2 down, pp-sum +217.3 incl. the '
        're-paired overviews); 0 outside the affected set. outputs/_r453_sk_final.json, _r453_skdelta.log, _r453_popsplit.log.",')
N_CS = ('    "_note_r453": "r453: matched 18178 -> 18463 (+285 restored TRR overview / lesson elements); exact 15657 -> 15855; EXTRA 199 held; '
        'missing 796 -> 840 (+44 — all on the newly compared restored content: TRR304 lesson 1 +28 on +148 matched, the six '
        'overview introductions +2 each; the modules whose page set did not change moved +0); row-wrap 24 held. NAMED.",')
N_BC = ('    "_note_r453": "r453: pages 2658 -> 2668; ANY 237 -> 238 (+1 TRR108_0_0 over-capture 0.88 — the restored introduction table carries '
        'the writer\'s [Tabs: Can these tabs please be an option at the top of the page …] request, so the scanner hands it off as a tabs '
        'widget (A1, the r235 hand-off box); before r453 the whole introduction was trimmed). over 58 -> 59, runaway 5, empty 176. NAMED.",')
N_DF = ('    "_note_r453": "r453: 2613/2658 -> 2623/2668 clean (the 10 restored pages are clean); leak 75 occ / 45 pages HELD.",')

setv("build", '"260620.23"', '"260620.24"'); setv("round", "452", "453")
insert_before("_note_r452", N_META)
setv("mean_scaffold_pct", "54.75", "54.71"); setv("median_scaffold_pct", "55.7", "55.8")
setv("pages_ge_50", "1544", "1549"); setv("pages_ge_75", "260", "265"); setv("pages_ge_90", "23", "23")
setv("raw_mean_pct", "38.6", "38.7"); setv("pairs", "2477", "2487")
insert_before("_note_r452_state", N_SK)
i = setv("exact_chain", "15657", "15855"); setv("claude_extra_container", "199", "199")
setv("claude_missing_container", "796", "840"); i = setv("row_wrap_missing", "24", "24"); insert_after_idx(i, N_CS)
setv("any_breakdown", "237", "238"); setv("over_capture", "58", "59"); setv("runaway", "5", "5")
i = setv("empty_container", "176", "176"); insert_after_idx(i, N_BC)
setv("clean_pages", "2613", "2623"); setv("total_pages", "2658", "2668"); setv("clean_pct", "98.31", "98.31")
setv("literal_tag_leak_occ", "75", "75"); i = setv("leak_pages", "45", "45"); insert_after_idx(i, N_DF)
out = "\n".join(L)
json.loads(out)
tmp = P + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, P)
print("gate_baseline.json refreshed to r453;", os.path.getsize(P), "bytes")
