#!/usr/bin/env python3
"""Session 43 Round 4 PICK — WHICH WRITER TAG'S CONTENT DOES THE CONVERTER LOSE? The corrected lost-text probe (_s43_lost2.py: WT
6-word shingles the gold carries outside its acks that no Claude page / worklist carries), each lost RUN (consecutive lost shingles)
mapped back to its Writers Template line and the nearest red [tag] at or above it (within 10 lines; the line's own leading tag
first). Aggregated: tag → lost runs / lost shingles / modules / families, with examples. Also: whether the lost line is itself RED
(the writer's red = an instruction the converter drops by design — the gold chose to show it) or black.
Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s43_r4_losttags.py > ../../outputs/_s43_r4_losttags.log"""
import os, re, sys, glob, html, collections
sys.path.insert(0, os.getcwd()); sys.path.append(os.path.join("..", "..", "outputs"))
import _corpus
from anchor_compare import CLAUDE, HUMAN
import importlib.util
spec = importlib.util.spec_from_file_location("L2", os.path.join("..", "..", "outputs", "_s43_lost2.py"))
src = open(spec.origin, encoding="utf-8").read().split("rows = []")[0]      # the helpers only (norm, page_text, shingles_list, K)
ns = {}; exec(compile(src, spec.origin, "exec"), ns)
norm, page_text, shingles_list, K = ns["norm"], ns["page_text"], ns["shingles_list"], ns["K"]
TAG = re.compile(r"🔴\[RED TEXT\]\s*\[([^\]\[]{1,50})\]")
def fam(code): return re.match(r"[A-Z]+", code).group(0)
agg = collections.Counter(); sh = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
famc = collections.defaultdict(collections.Counter); redc = collections.Counter()
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    if not (os.path.isdir(hd) and os.path.isdir(cd)): continue
    wts = [f for f in glob.glob(os.path.join(hd, "*_parsed.txt")) if "media list_parsed" not in f.lower() or "writers template" in f.lower()]
    if not wts: continue
    lines = []
    for f in wts: lines += open(f, encoding="utf-8", errors="replace").read().splitlines()
    # word stream with the line index of every word
    words, wline = [], []
    for li, l in enumerate(lines):
        for w in norm(l).split(): words.append(w); wline.append(li)
    wl = [" ".join(words[i:i + K]) for i in range(0, max(0, len(words) - K + 1))]
    g = set(shingles_list(norm(" ".join(page_text(p) for p in glob.glob(os.path.join(hd, "*.html"))))))
    ctext = " ".join(page_text(p) for p in glob.glob(os.path.join(cd, "*.html")))
    ctext += " " + " ".join(open(p, encoding="utf-8", errors="replace").read() for p in glob.glob(os.path.join(cd, "*_interactives.txt")))
    c = set(shingles_list(norm(ctext)))
    lost = [i for i, x in enumerate(wl) if x in g and x not in c]
    runs = []; cur = None
    for i in lost:
        if cur and i == cur[1] + 1: cur[1] = i
        else:
            if cur: runs.append(cur)
            cur = [i, i]
    if cur: runs.append(cur)
    for a, b in runs:
        li = wline[a + K // 2]
        tag = None
        for j in range(li, max(-1, li - 11), -1):
            m = TAG.search(lines[j])
            if m: tag = m.group(1).strip().lower()[:30]; break
        tag = tag or "(no tag within 10 lines)"
        tag = re.sub(r"\d+", "N", tag)
        is_red = "🔴" in lines[li] and not norm(re.sub(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴", " ", lines[li]))
        n = b - a + 1
        agg[tag] += 1; sh[tag] += n; mods[tag].add(code); famc[tag][fam(code)] += n; redc[(tag, is_red)] += n
        if len(ex[tag]) < 3: ex[tag].append(f"{code}: " + " ".join(words[a:a + K + min(n, 10)])[:110])
print("tag | runs | lost shingles | modules | red-line share | families | examples")
for t, n in sorted(sh.items(), key=lambda kv: -kv[1])[:40]:
    rs = redc[(t, True)] / max(1, n)
    print(f"{t:30s} | {agg[t]:5d} | {n:6d} | {len(mods[t]):4d} | {rs:.2f} | {dict(famc[t].most_common(5))} | {' ;; '.join(ex[t])[:260]}")
print("TOTAL lost shingles", sum(sh.values()), "runs", sum(agg.values()))
