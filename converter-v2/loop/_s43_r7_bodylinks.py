#!/usr/bin/env python3
"""Session 43 Round 7 — body inline anchors, gold vs Claude: every <a href="http…"> BEFORE the acknowledgements block whose parent is a
<p> / <li> / <td> and whose visible text is words (not the URL itself, not a button), counted per corpus (paired pages), plus the
Claude anchors that are buttons. Quick census: does Claude ever render a writer's inline link inside prose?"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
A = re.compile(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', re.S)
def count(path, c):
    s = open(path, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    i = s.find('<div class="acks')
    if i >= 0: s = s[:i]
    for m in A.finditer(s):
        inner = m.group(2)
        txt = re.sub(r"<[^>]+>", "", inner).strip()
        if 'class="button' in inner or "externalButton" in inner or 'class="' in inner and "button" in inner: c["button"] += 1; continue
        if re.match(r"https?://", txt): c["url-text"] += 1; continue
        c["inline words"] += 1
G, C = collections.Counter(), collections.Counter()
for code in sorted(_corpus.gate_mods(CLAUDE)):
    for _k, cp, gp in pairs(code):
        try: count(gp, G); count(cp, C)
        except Exception: pass
print("gold  ", dict(G)); print("claude", dict(C))
