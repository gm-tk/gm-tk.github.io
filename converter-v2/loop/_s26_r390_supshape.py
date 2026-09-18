#!/usr/bin/env python3
"""Session 26 Round 4 candidate — THE SUPERVISOR PANEL'S CONTENT RUN: what the writer typed after a [Supervisor note] /
[Supervisor button] opener (the item sequence to the first STRUCTURAL tag) and what the GOLD panel holds.
For every gold page with a top-level non-activity super-content panel: the gold panel's text elements (the reference), the
WT items after the matching opener (matched by the panel's first text), and which WT items the gold panel CONTAINS — so the
gold's own gather rule can be read: does the gold panel run through an inline red span (a `[link to X]` at the end of a
bullet), through a `[body]` tag, to the next heading / activity / widget?
  python3 _s26_r390_supshape.py"""
import os, sys, re, glob
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
import _corpus
from _diff_miner import page_lines, unorm
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta

meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
RED = re.compile(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴", re.S)
TEXT_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "b", "strong", "a", "span", "label")
def fold(t): return re.sub(r"[^a-z0-9]+", " ", unorm(t or "").lower()).strip()
def tag_of(sig):
    m = re.match(r"([a-z0-9]+)", sig); return m.group(1) if m else sig
def subtree_end(L, i):
    d = L[i].depth; j = i + 1
    while j < len(L) and L[j].depth > d: j += 1
    return j
def wt_lines(code):
    d = _corpus.mdir(HUMAN, code); out = []
    for f in sorted(glob.glob(os.path.join(d, "*_parsed.txt"))):
        n = os.path.basename(f).lower()
        if "media list" in n and "writers template" not in n: continue
        try: out += open(f, encoding="utf-8", errors="replace").read().split("\n")
        except Exception: pass
    return [l for l in out if l.strip()]
STRUCT = re.compile(r"^\[\s*(activity|h[1-6]\b|alert|important|supervisor|lesson|end page|title|tab\b|tabs|accordion|carousel|flip|click|drag|drop|modal|video|image|embed|quiz|interactive|button|audio|whakatauki|wananga|end supervisor|end of supervisor|new page|page \d)", re.I)
INLINE = re.compile(r"^\[\s*(link|external link|hyperlink|hover|rollover|definition|define)", re.I)
def item_kind(line):
    reds = [m.group(1).strip() for m in RED.finditer(line)]
    black = RED.sub(" ", line).strip()
    kinds = []
    for r in reds:
        rl = r.lower()
        if not rl.startswith("["): kinds.append("red-prose"); continue
        if STRUCT.search(rl): kinds.append("STRUCT:" + rl.split()[0].strip("[]").lower()); continue
        if rl.startswith("[body") or rl.startswith("[list") or rl.startswith("[bullet"): kinds.append("body-tag"); continue
        if INLINE.search(rl): kinds.append("inline-tag"); continue
        kinds.append("other-tag:" + rl[:14])
    if not reds: return "black", black
    return "+".join(kinds) + ("(+black)" if black else ""), black

SHAPE = defaultdict(Counter); EX = defaultdict(list); RUN = defaultdict(Counter)
for code in sorted(fam):
    tf = fam[code]; subject = (meta.get(code, {}) or {}).get("subject") or "None"
    grp = f"{tf}/{subject}"
    lines = wt_lines(code)
    for n, cp, hp in pairs(code):
        try:
            g, _ = page_lines(hp)
        except Exception:
            continue
        for i, l in enumerate(g):
            if not l.sig.startswith("div.row.super-content"): continue
            # the gold panel's text (skip the h3 label)
            e = subtree_end(g, i)
            texts = [fold(x.text) for x in g[i + 1:e] if x.text and tag_of(x.sig) in TEXT_TAGS and tag_of(x.sig) != "h3"]
            if not texts: continue
            first = texts[0][:40]
            # find the WT line holding the panel's first text
            wi = next((k for k, wl in enumerate(lines) if first and first in fold(RED.sub(" ", wl))), None)
            if wi is None: continue
            # walk the WT items from there; classify each; is it in the gold panel?
            seq = []; stop = None
            last_in = -1
            for k in range(wi, min(wi + 25, len(lines))):
                kind, black = item_kind(lines[k])
                if kind.startswith("STRUCT") or "STRUCT" in kind: stop = kind; break
                inpanel = bool(black) and any(fold(black)[:40] and fold(black)[:40] in t or (t[:40] and t[:40] in fold(black)) for t in texts)
                seq.append((kind, inpanel))
                if inpanel: last_in = len(seq) - 1
            # the RUN rule: after the last in-panel item, what kinds sit between panel items (skipped by the gold)?
            skipped = Counter(k for k, ip in seq[:last_in + 1] if not ip)
            for k2 in skipped: RUN[grp][k2] += skipped[k2]
            after = [k for k, ip in seq[last_in + 1:]][:2]
            key = f"stop={stop or 'run-end'}; skipped-inside={sorted(skipped) or '-'}; after-panel={after or '-'}"
            SHAPE[grp][key] += 1
            if len(EX[grp]) < 3: EX[grp].append(f"{os.path.basename(hp)[:-5]}: {[(k[:22], ip) for k, ip in seq[:8]]} stop={stop}")
print("==== the gold panel's run, per template/subject: what the gold skipped INSIDE the panel (kinds between panel items) ====")
for grp in sorted(RUN, key=lambda x: -sum(RUN[x].values())):
    print(f"   {grp:40s} panels={sum(SHAPE[grp].values()):3d}  skipped-inside={dict(RUN[grp].most_common())}")
print("\n==== per group: the top shapes ====")
for grp in sorted(SHAPE, key=lambda x: -sum(SHAPE[x].values())):
    print(f"-- {grp} (n={sum(SHAPE[grp].values())})")
    for k, v in SHAPE[grp].most_common(6): print(f"     {v:3d}  {k}")
    for e in EX[grp]: print("       ex:", e[:230])
