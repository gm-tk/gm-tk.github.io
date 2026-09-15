#!/usr/bin/env python3
"""_r333_diffcheck.py — ROUND 333: classify every differing line the ON probe reports (`_r333_probe_on_0*.log`)
so the round can say exactly what changed and nothing else. Tallies removed ('-') and added ('+') lines by
a small pattern vocabulary; anything outside it is printed in full for inspection."""
import os, re, sys, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
logs = sorted(glob.glob(os.path.join(HERE, "_r333_probe_on_0*.log")))
if "--files" in sys.argv:
    logs = [a for a in sys.argv[sys.argv.index("--files") + 1:]]
CLASSES = [
    ("alert rhs open", re.compile(r'^<div class="alert(?: solid)? rhs">$')),
    ("alert summary open", re.compile(r'^<div class="alert(?: solid)? summary">$')),
    ("alert plain open", re.compile(r'^<div class="alert(?: solid)?">$')),
    ("alert top open", re.compile(r'^<div class="alert top">$')),
    ("alertActivity open", re.compile(r'^<div class="alertActivity">$')),
    ("side col (activity sidebar)", re.compile(r'^<div class="col-md-4 offset-md-0 col-12">$')),
    ("side col (alert top)", re.compile(r'^<div class="col-md-4 col-12">$')),
    ("row open", re.compile(r'^<div class="row">$')),
    ("content col open", re.compile(r'^<div class="col-md-8 col-12">$')),
    ("col-12 open", re.compile(r'^<div class="col-12">$')),
    ("div close", re.compile(r'^</div>$')),
    ("h4 lead", re.compile(r'^<h4>.*</h4>$')),
    ("cv2-note", re.compile(r'^<p class="cv2-note"')),
    ("p", re.compile(r'^<p>.*</p>$')),
    ("li/ul/ol", re.compile(r'^</?(ul|ol|li)\b')),
]
rem = collections.Counter(); add = collections.Counter(); other = collections.defaultdict(list)
pages = []; mods = set(); cur = None
for lg in logs:
    for ln in open(lg, encoding="utf-8", errors="replace"):
        ln = ln.rstrip("\n")
        m = re.match(r"^  ~ (\S+): -(\d+) \+(\d+)", ln)
        if m: cur = m.group(1); pages.append((cur, int(m.group(2)), int(m.group(3)))); continue
        m = re.match(r"^(\w+): identical", ln)
        if m and " changed 0" not in ln: mods.add(m.group(1))
        m = re.match(r"^     ([-+]) (.*)$", ln)
        if not m: continue
        sign, txt = m.group(1), m.group(2).strip()
        if txt.startswith("…"): continue
        cls = next((n for n, rx in CLASSES if rx.search(txt)), None)
        if cls is None:
            other[sign].append((cur, txt[:140])); cls = "OTHER"
        (rem if sign == "-" else add)[cls] += 1
print(f"changed pages {len(pages)} across {len(mods)} modules; logs {len(logs)}")
print("REMOVED:"); [print(f"  {v:5} {k}") for k, v in rem.most_common()]
print("ADDED:"); [print(f"  {v:5} {k}") for k, v in add.most_common()]
for sign in "-+":
    if other[sign]:
        print(f"\nOTHER {sign} ({len(other[sign])}):")
        for p, t in other[sign][:60]: print(f"  {sign} {p}: {t}")
