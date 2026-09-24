#!/usr/bin/env python3
"""Session 45 Round 9 — every ALERT-family tag (alert / important / alert box / alert solid / alert.top / side alert …) that sits inside a
lesson's `[Lesson Overview] … [Lesson content]` block in a Writers Template: its text (a WALT lead — 'in this lesson you', 'we are
learning', 'you will' — or not), and where the gold puts that text (menu / body / absent), per module. The r147 section-stop ends the
lesson menu at any alert; the gold's HIS1003 / HIS1004 keep the WALT sentence of such an alert in the menu. WSL, from outputs/."""
import os, re, io, sys, glob, json, collections, html as H
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s45_r7_emptymenu.py"), encoding="utf-8").read().split("pp = json.load")[0])
RED = re.compile(r"🔴\[RED TEXT\]|\[/RED TEXT\]🔴")
LO = re.compile(r"\[\s*lesson\s+overview\b", re.I); LC = re.compile(r"\[\s*lesson\s+content\b", re.I)
ALERT = re.compile(r"\[\s*((?:important|alert|side alert|rhs alert|alert\.top|alert top|alert box|alert solid|coloured box|important box)[^\]]{0,40})\]", re.I)
WALT = re.compile(r"^(?:in this lesson,? you|we are learning|you will|this lesson)", re.I)
pages = collections.defaultdict(list)
for code in _corpus.gate_mods(GOLD):
    gd = _corpus.mdir(GOLD, code)
    gp = {}
    for p in glob.glob(os.path.join(gd, "*.html")):
        gm, gb = split_regions(p); gp[os.path.basename(p)] = (gm, gb)
    wts = [p for p in glob.glob(os.path.join(gd, "*_parsed.txt")) if "writers template" in p.lower()]
    lines = []
    for w in wts: lines += io.open(w, encoding="utf-8", errors="replace").read().split("\n")
    inlo = False
    for i, ln in enumerate(lines):
        raw = RED.sub(" ", ln)
        if LO.search(raw): inlo = True; continue
        if LC.search(raw) or re.search(r"\[\s*(?:end page|lesson\s*#?\s*\d*\s*\])", raw, re.I): inlo = False; continue
        if not inlo: continue
        m = ALERT.search(raw)
        if not m: continue
        text = raw[m.end():].strip()
        j = i
        while len(n(text)) < 15 and j + 1 < len(lines) and j < i + 3:
            j += 1; text = RED.sub(" ", lines[j]).strip()
        key = " ".join(n(text).split()[:7])
        if not key: continue
        where = "absent"
        for g, (gm, gb) in gp.items():
            if key in gm: where = "menu"; break
            if key in gb: where = "body"
        kind = "WALT" if WALT.search(re.sub(r"^[\*\s]+", "", text)) else "other"
        pages[(kind, m.group(1).strip().lower()[:20], where)].append(code)
tot = collections.Counter()
for k, v in sorted(pages.items(), key=lambda x: -len(x[1])):
    tot[(k[0], k[2])] += len(v)
    print(f"{len(v):4d}  {k}  modules {sorted(set(v))[:10]}")
print("\nby (text kind, gold placement):", dict(tot))
