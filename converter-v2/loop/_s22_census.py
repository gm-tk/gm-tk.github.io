#!/usr/bin/env python3
"""Session 22 census over the gate's own pairs: class-level forms the spot check surfaced.
Counts per side (gold / Claude), per template family:
  alert forms        : div.alert bare vs alert solid vs alert <other>
  colour text        : elements with red-text / green-text / blue-text classes
  videoSection icon  : videoSection with vs without the `icon` class
  paddingR body col  : col-md-8 col-12 paddingR inside #body (outside activities is not separated)
  activity numbering : activity number="Nx" whose N != the page's lesson number (lesson pages only)
"""
import os, sys, re, json, collections
BASE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(BASE, "..", "reference", "tests"))
if BASE in sys.path:
    sys.path.remove(BASE)
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN

RE_ALERT = re.compile(r'<div\b[^>]*\bclass="([^"]*\balert\b[^"]*)"', re.I)
RE_COLOUR = re.compile(r'class="[^"]*\b(red|green|blue|orange|purple)-text\b', re.I)
RE_VIDEO = re.compile(r'<div\b[^>]*\bclass="([^"]*\bvideoSection\b[^"]*)"')
RE_PADR = re.compile(r'class="col-md-8 col-12 paddingR"')
RE_ACT = re.compile(r'<div\b[^>]*\bclass="[^"]*\bactivity\b[^"]*"[^>]*\bnumber="([^"]+)"')
RE_LESSON = re.compile(r'[._-](\d{1,2})(?:\.0|_0)?\.html$')

def lesson_no(name):
    m = RE_LESSON.search(name)
    return int(m.group(1)) if m else None

def scan(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    body = t.split("<body", 1)[1] if "<body" in t else t
    out = collections.Counter()
    for m in RE_ALERT.finditer(body):
        cls = set(m.group(1).split())
        if cls == {"alert"}: out["alert:bare"] += 1
        elif "solid" in cls: out["alert:solid"] += 1
        else: out["alert:other"] += 1
    out["colour"] += len(RE_COLOUR.findall(body))
    for m in RE_VIDEO.finditer(body):
        out["video:icon" if "icon" in m.group(1).split() else "video:plain"] += 1
    out["paddingR"] += len(RE_PADR.findall(body))
    return out, [m.group(1) for m in RE_ACT.finditer(body)]

def main():
    tot = collections.defaultdict(collections.Counter)   # (side, template) -> counter
    pages = collections.defaultdict(collections.Counter)  # (side, key) -> pages with >0
    mism = collections.defaultdict(list)                  # side -> [(code, page, nums)]
    for code in _corpus.gate_mods(CLAUDE):
        mm = _corpus.mdir(HUMAN, code)
        parent = os.path.basename(os.path.dirname(mm)) if mm else "flat"
        tmpl = parent if parent in _corpus.TEMPLATE_DIRS else "flat"
        for n, cp, hp in pairs(code):
            for side, p in (("gold", hp), ("claude", cp)):
                if not p or not os.path.exists(p):
                    continue
                c, acts = scan(p)
                tot[(side, tmpl)].update(c)
                for k, v in c.items():
                    if v: pages[(side, k)][code] += 1
                ln = lesson_no(os.path.basename(p))
                if ln and ln > 0 and acts:
                    bad = [a for a in acts if re.match(r'\d+', a) and int(re.match(r'\d+', a).group()) != ln]
                    if bad and len(bad) == len(acts):
                        mism[side].append((code, os.path.basename(p), acts[:4]))
    print("== per side / template ==")
    for k in sorted(tot):
        print(k, dict(sorted(tot[k].items())))
    print("== pages with >0, by key (modules) ==")
    for k in sorted(pages):
        print(k, "modules", len(pages[k]), "pages", sum(pages[k].values()))
    print("== lesson pages whose EVERY activity number disagrees with the lesson digit ==")
    for side in ("gold", "claude"):
        print(side, len(mism[side]), "pages /", len({x[0] for x in mism[side]}), "modules")
        for x in mism[side][:12]:
            print("   ", x)
    json.dump({"mism": mism}, open(os.path.join(BASE, "_s22_census.json"), "w"), indent=1)

main()
