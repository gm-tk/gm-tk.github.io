#!/usr/bin/env python3
"""_s54_r2_emptybox.py — session 54 Round 2: the writer's EMPTY callout boxes left after r541 ("Red Flag: Empty [alert]" /
[important] / [whakatauki] / [quote] / [supervisor note]). For each: what Claude put right after the box (the first block of the
next content, tag + text), and whether the GOLD paired page holds that text inside a callout box (alert / important /
whakatauki / quoteText / activity) — i.e. would gathering the next block into the empty box match the gold? Tallied by the next
block's tag and by family. WSL, from reference/tests/:  python3 ../../outputs/_s54_r2_emptybox.py"""
import os, re, sys, collections, html as H
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _corpus
from anchor_compare import CLAUDE
import compare_structure as CS

EMPTY = re.compile(r'Red Flag: Empty \[(alert|important|whakatauki|quote|supervisor note)\]', re.I)
BLOCK = re.compile(r'<(h[1-6]|p|ul|ol|table|img|div class="(?:videoSection|audio|activity|alert|row)[^"]*"|iframe|audio|a)\b[^>]*>', re.I)
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", H.unescape(re.sub(r"<[^>]+>", " ", s)).lower())).strip()
fam = lambda m: re.sub(r"\d.*$", "", m)
tally = collections.Counter(); gold_boxed = collections.Counter(); byfam = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
mods = sorted(set(_corpus.gate_mods(CLAUDE)))
for mod in mods:
    for n, cp, hp in pairs(mod):
        s = open(cp, encoding="utf-8").read()
        if "Red Flag: Empty [" not in s: continue
        gp = CS.parse_page(hp)
        gtext = [(norm(e["text"]), set(e["chain"])) for e in gp.elements]
        for m in EMPTY.finditer(s):
            # the end of the empty box's row: 5 closing divs after the note
            i = m.end(); k = 0
            for _ in range(5):
                j = s.find("</div>", i)
                if j < 0: break
                i = j + 6
            nb = BLOCK.search(s, i)
            if not nb: continue
            tag = nb.group(1).split()[0].lower().replace('div', 'div.' + (re.search(r'class="([^" ]+)', nb.group(0)) or [None, "?"])[1]) if nb.group(1).lower().startswith("div") else nb.group(1).lower()
            # the next block's text: up to the next tag close of the same kind (approx: 300 chars of stripped text)
            txt = norm(s[nb.end(): nb.end() + 600])[:60]
            key = (m.group(1).lower(), tag)
            tally[key] += 1; byfam[key][fam(mod)] += 1
            boxed = "?"
            if len(txt) >= 12:
                hit = [ch for t, ch in gtext if t and (t.startswith(txt[:40]) or txt[:40] in t)]
                if hit: boxed = "boxed" if any(ch & CS.CALLOUT_CLASSES for ch in hit) else "free"
                else: boxed = "notfound"
            gold_boxed[(key, boxed)] += 1
            if len(ex[key]) < 4: ex[key].append(f"{os.path.basename(cp)} {txt[:50]!r} gold:{boxed}")
print("empty boxes by (writer tag, next block):")
for key, c in tally.most_common():
    g = {b: gold_boxed[(key, b)] for b in ("boxed", "free", "notfound", "?")}
    print(f"  {c:4d}  {key[0]:16s} → {key[1]:20s} gold boxed {g['boxed']} / free {g['free']} / notfound {g['notfound']} / short {g['?']}   {dict(byfam[key].most_common(5))}")
    for e in ex[key]: print("        e.g.", e)
