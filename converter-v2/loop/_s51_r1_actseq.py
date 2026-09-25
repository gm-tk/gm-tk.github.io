#!/usr/bin/env python3
"""_s51_r1_actseq.py — session 51 Round 1 PICK: the ordered activity-box NUMBER sequence of every paired page (the skeleton
gate's own pairing), gold vs Claude. The skeleton line of a box carries its number (`div.activity[number=4B]`), so ONE extra
or missing box shifts every later number on the page. Classes:
  EQUAL     — the same sequence
  EXTRA1    — Claude's sequence is the gold's with ONE box inserted (a phantom box that shifts the rest)
  MISSING1  — Claude lacks one of the gold's boxes
  SHIFTED   — same count, different labels
  OTHER     — anything else
For EXTRA1 / MISSING1 it reports where the sequences first diverge and how many later boxes carry a shifted number.
WSL, from reference/tests/. Writes outputs/_s51_r1_actseq.tsv."""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE

TAG = re.compile(r"<div\b[^>]*>", re.I)
CLS = re.compile(r'class="([^"]*)"', re.I)
NUM = re.compile(r'\bnumber="([^"]*)"', re.I)


def seq(path):
    try:
        html = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    m = re.search(r'<div[^>]*id="body"', html)
    body = html[m.start():] if m else html
    out = []
    for t in TAG.finditer(body):
        c = CLS.search(t.group(0)); n = NUM.search(t.group(0))
        if c and n and re.search(r"\bactivity\b", c.group(1)):
            out.append(n.group(1).strip())
    return out


def classify(g, c):
    if g == c: return "EQUAL", -1, 0
    if len(c) == len(g) + 1:
        for k in range(len(c)):
            if c[:k] + c[k + 1:] == g: return "EXTRA1", k, sum(1 for a, b in zip(c[k + 1:], g[k:]) if a != b)
            if c[:k] != g[:k]: break
    if len(g) == len(c) + 1:
        for k in range(len(g)):
            if g[:k] + g[k + 1:] == c: return "MISSING1", k, sum(1 for a, b in zip(g[k + 1:], c[k:]) if a != b)
            if g[:k] != c[:k]: break
    if len(g) == len(c): return "SHIFTED", next(i for i, (a, b) in enumerate(zip(g, c)) if a != b), 0
    return "OTHER", -1, 0


def main():
    mods = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
    cnt = collections.Counter(); fam = collections.defaultdict(collections.Counter); rows = []
    for code in mods:
        for n, cp, hp in pairs(code):
            if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
            if re.search(r"acks|acknowledge|glossary", os.path.basename(cp), re.I): continue
            g, c = seq(hp), seq(cp)
            if g is None or c is None: continue
            k, at, shifted = classify(g, c)
            cnt[k] += 1; fam[re.sub(r"\d.*$", "", code)][k] += 1
            if k != "EQUAL":
                rows.append((k, code, os.path.basename(cp), at, shifted, " ".join(g), " ".join(c)))
    print("pairs:", sum(cnt.values()), dict(cnt))
    ex = [r for r in rows if r[0] == "EXTRA1"]
    print("EXTRA1 pages", len(ex), "modules", len({r[1] for r in ex}), "later boxes shifted", sum(r[4] for r in ex))
    mi = [r for r in rows if r[0] == "MISSING1"]
    print("MISSING1 pages", len(mi), "modules", len({r[1] for r in mi}), "later boxes shifted", sum(r[4] for r in mi))
    print("by family (EXTRA1 / MISSING1 / SHIFTED / OTHER):")
    for f, c in sorted(fam.items(), key=lambda kv: -(kv[1]["EXTRA1"] + kv[1]["MISSING1"])):
        if c["EXTRA1"] + c["MISSING1"] + c["SHIFTED"] + c["OTHER"]:
            print(f"  {f:8s} {c['EXTRA1']:3d} {c['MISSING1']:3d} {c['SHIFTED']:3d} {c['OTHER']:3d}  (equal {c['EQUAL']})")
    with open("../../outputs/_s51_r1_actseq.tsv", "w") as fh:
        fh.write("# class\tcode\tpage\tat\tshifted\tgold\tclaude\n")
        for r in rows: fh.write("\t".join(map(str, r)) + "\n")


main()
