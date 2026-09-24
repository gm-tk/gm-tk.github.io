#!/usr/bin/env python3
"""ROUND 471 decline record (session 42 Round 10) — the two-column dragAndDrop tables (D10-3 build lane) measured and declined.
LOOP_STATE.md: marker cleared, Declined-classes entry, round-log line; the marker → archive. .bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
shutil.copyfile(S, S + ".pre-r471-decline.bak")
i = find("- **ROUND 471 IN FLIGHT — MEASURING"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 17:25 real clock, session 42 Round 10 — r471 (the two-column dragAndDrop tables) MEASURED "
        "and DECLINED; the probe-only data tweak restored byte-identical, `git status` clean). LAST SHIPPED **r470** (260620.35); **LAST "
        "FULL = r460**; ledger **scoped #4**.")
k = find("- **Before r471: no round in flight**"); prior = L[k]; del L[k]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 42 Round 10 (24 Sept 17:00 → 17:25) — THE TWO-COLUMN dragAndDrop TABLE (engine r471 — MEASURED, DECLINED; D10-3 "
         "build lane, the largest un-built type).** 209 declined bundles / 182 pages / 139 modules are refused by the r351 column builder's "
         "`min_columns 3` (`_s42_r9_declines.log`). Dumped (`outputs/_s42_r10_dd2dump.cjs` → `.json`, 258 two-column bundles) and matched "
         "to the paired gold widget (`_s42_r10_dd2match.py` → `.log`): NOT one authoring shape — pair / answer-key tables (red answers, "
         "`[Q1]` keys, `a | A` letter pairs), image | sentence tables, FIB sentence tables and category sorts mixed; the gold builds a "
         "2-column category sort (`layout=\"column\"`, 2 `ddColumn`s) for ≈ 27 of them. Sizing probe (`min_columns` 2 TEMPORARILY, the "
         "builder's own header / cell / item fences unchanged): **2 pages / 1 module build (ENGR102)** — the clean 2-column category sort "
         "is far below the per-shape 20-page floor. Re-open only for a writer-side discriminator of the category sort that the r351 "
         "fences would pass (e.g. heading-tagged headers `[H3] Agrees | [H3] Disagrees` — ENGC403, XGF9002 — currently refused by the "
         "header `[tag]` fence).")
k = find("## Round log")
L.insert(k + 1, "- s42-r10 (engine r471, 24 Sept 17:00 → 17:25) · THE TWO-COLUMN dragAndDrop TABLE (D10-3) · MEASURED (dump + gold match + a "
         "`min_columns 2` sizing probe: 2 pages / 1 module), DECLINED — not one authoring shape · plateau 2 of 3 (neither).")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 42 — Round 10 PICK (engine r471, DECLINED)\n\n" + marker + "\n" + prior + "\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
