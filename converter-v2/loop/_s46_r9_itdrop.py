#!/usr/bin/env python3
"""Session 46 Round 9 — the hover definitions ListsAndRuns.inlineMarkup DROPS (no clean anchor right before the sentinel): attribute
each TRACE_ITDROP line of the `itdrop` probe logs to its module (the next `CODE: identical …` line), then look the def up in the gold:
does the gold build it (an info= starting with the same words), and what is the gold's anchor + the char after the anchor?
WSL, from outputs/: TRACE_ITDROP=1 bash _s42_probe_run.sh itdrop ON; python3 _s46_r9_itdrop.py > _s46_r9_itdrop.log"""
import os, re, sys, glob, io, json, collections, html as H
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(OUT, "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
def nz(t): return re.sub(r"[^a-z0-9ā-ž]+", "", H.unescape(re.sub(r"<[^>]+>", "", t)).lower())
drops = []
for f in sorted(glob.glob(os.path.join(OUT, "_itdrop_probe_ON_0*.log"))):
    pend = []
    for ln in io.open(f, encoding="utf-8", errors="replace"):
        if ln.startswith("ITDROP\t"):
            _, pre, d = ln.rstrip("\n").split("\t"); pend.append((json.loads(pre), json.loads(d)))
        else:
            m = re.match(r"^([A-Z0-9]+): identical", ln)
            if m:
                drops += [(m.group(1), p, d) for p, d in pend]; pend = []
seen = set(); uniq = []
for r in drops:
    if r not in seen: seen.add(r); uniq.append(r)
gcache = {}
def gold_infos(code):
    if code not in gcache:
        out = []
        try: gd = _corpus.mdir(GOLD, code)
        except Exception: gd = None
        for p in sorted(glob.glob(os.path.join(gd, "*.html"))) if gd else []:
            s = io.open(p, encoding="utf-8", errors="replace").read()
            for m in re.finditer(r'<span[^>]*class="infoTrigger"[^>]*info="([^"]*)"[^>]*>(.*?)</span\s*>(.{0,3})', s, re.S):
                out.append((nz(m.group(1)), H.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip(), H.unescape(m.group(3))))
        gcache[code] = out
    return gcache[code]
kind = collections.Counter(); byprev = collections.Counter(); gold_after = collections.Counter(); mods = collections.Counter(); rows = []
for code, pre, d in uniq:
    prev = pre.rstrip()[-1:] if pre.rstrip() else "∅"
    tail = pre.rstrip()
    k = ("punct" if prev in ".?!,:;)”\"'" else "tag>" if prev == ">" else "bracket" if prev in "[" else "empty" if prev == "∅" else "other")
    dk = nz(d)[:18]
    g = next(((a, aft) for (i, a, aft) in gold_infos(code) if dk and i.startswith(dk)), None)
    kind[(k, "gold-builds" if g else "gold-no")] += 1; byprev[prev] += 1; mods[code] += 1
    if g: gold_after[(prev, "anchor-ends-" + (g[0][-1:] if g[0] else "∅"))] += 1
    rows.append(f"  {code:9s} {k:7s} {('GOLD anchor «' + g[0][:30] + '»') if g else 'gold-no':44s} pre «{pre[-38:]}» def «{d[:34]}»")
print(f"dropped hover definitions: {len(drops)} ({len(uniq)} unique) in {len(mods)} modules")
print("by the char before the sentinel x gold:", dict(kind.most_common()))
print("prev char:", dict(byprev.most_common()))
print("gold's anchor end for the punct cases:", dict(gold_after.most_common(20)))
print("modules:", dict(mods.most_common(40)))
print("\n".join(rows))
