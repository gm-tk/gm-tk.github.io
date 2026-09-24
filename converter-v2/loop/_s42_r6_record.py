#!/usr/bin/env python3
"""Session 42 Round 6 — a PICK pass with no engine change: the placement census's P6 / P7 and the derivable-loss rows split by the
writer's tag (`_s42_wtctx.py`), the census's combined-WT fix. LOOP_STATE.md: a Declined-classes entry, the follow-up line, the
round-log line. .bak kept. Run under WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
shutil.copyfile(S, S + ".pre-s42-r6.bak")
k = find("## Declined classes")
L.insert(k + 1, "- **Session 42 Round 6 (24 Sept 16:00 → ≈16:30) — a PICK pass, no engine change: the placement census's P6 / P7 DECLINED as "
         "class C, and an instrument fix.** Split by the writer's tag (`outputs/_s42_wtctx.py`, now with a 40-line look-back for the widget's "
         "own tag word and an ABSENT mode that checks `{CODE}_interactives.txt`): gold ACCORDION → Claude free text 1,131 blocks — only "
         "207 (18 %) have an accordion tag within 40 lines above; TABS → free 604 — 149 (25 %); WORD HIGHLIGHTER → free 394 — 123 (31 %, "
         "all WJFUN — the r410 tile dialect); the gold SIDE COLUMN → main column 149 — captions / untagged; the rest is the developer's own "
         "widget or layout choice with no writer tag (class C). The tagged residues are scattered run-end under-capture (a follow-up, "
         "below floor per family). **Instrument fix:** the census and the probe dropped the 286 combined `Writers Template + Media "
         "List_parsed.txt` files as \"media list\" (the OPERATING_GUIDE §16 trap) — fixed; ABSENT-inWT 8,983 → 16,889 (10.3 %). The "
         "`body:free / body:activity → ABSENT` decomposition: 5,133 / 5,145 blocks are not WT text; the `[body]`-tagged \"drops\" "
         "sampled are the gold REWORDING the WT (AGH1005 \"healthy nature…\" drops the writer's Māori opening) — the census's on-page "
         "Jaccard, not the probe's exact-prefix check, is the measure. Logs `outputs/_s42_wtctx_{accfree,tabsfree,whl,side,freeabsent,"
         "actabsent}.log`.")
k = find("- **(s42-r3) THE PLACEMENT CENSUS")
L[k] = L[k].replace("(P6) gold widget → Claude free text:", "(P6 — DECLINED s42-r6, class C: 69–82 % untagged) gold widget → Claude free text:", 1)
L[k] = L[k].replace("(P7) `body:free:side → body:free`", "(P7 — DECLINED s42-r6, class C) `body:free:side → body:free`", 1)
L[k] = L[k].replace("SAME 39.6 % / MOVED 22.7 % / OTHER-PAGE 5.0 % / ABSENT-inWT 5.5 % / ABSENT-notWT 27.1 %", "SAME 39.6 % / MOVED 22.7 % / OTHER-PAGE 5.0 % / ABSENT-inWT 10.3 % / ABSENT-notWT 22.3 % (after the s42-r6 combined-WT fix)", 1)
assert "DECLINED s42-r6, class C: 69" in L[k] and "after the s42-r6 combined-WT fix" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s42-r6 (no engine change, 24 Sept 16:00 → ≈16:30) · a PICK pass on the placement census: P6 (gold widget → Claude free "
         "text) and P7 (the side column) DECLINED as class C (69–82 % carry no writer tag); the census's combined-WT filter fixed "
         "(ABSENT-inWT 5.5 → 10.3 %); the miner's chrome rows confirmed dispositioned · plateau 2 of 3 (neither).")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
