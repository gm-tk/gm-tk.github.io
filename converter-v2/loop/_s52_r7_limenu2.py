#!/usr/bin/env python3
"""_s52_r7_limenu2.py — session 52 Round 7 (strict): on every Claude page carrying r509's 'no learning intentions' red flag, the
first learning-intentions LABEL block in the BODY (the whole block text is a label: 'We are learning (to):', 'Learning
intention(s)', 'Success criteria', 'How will I know …', 'I can:', 'Whāinga ako …', 'Paearu …') — its position (block index
from the body start), its tag, and whether the paired gold page's MENU holds that label. Per family + the label forms.
WSL, from reference/tests/:  python3 ../../outputs/_s52_r7_limenu2.py"""
import os, re, sys, collections
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import compare_structure as CS
import _corpus
LAB = re.compile(r"^(?:we are learning(?: to| about| how)?|learning intentions?|success criteria|how will i know[^.]{0,40}|i can|whāinga ako[^.]{0,40}|paearu[^.]{0,40}|we will be learning(?: to)?|in this lesson we are learning(?: to)?)\s*[:?.…]*$", re.I)
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.blocks = []; self.cur = None; self.inbody = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id") == "body": self.inbody = True
        if self.inbody and tag in ("p", "h2", "h3", "h4", "h5", "h6", "li") and self.cur is None:
            self.cur = [tag, [], a.get("class") or ""]
    def handle_endtag(self, tag):
        if self.cur and tag == self.cur[0]:
            t = re.sub(r"\s+", " ", "".join(self.cur[1])).strip()
            if t and "cv2-note" not in self.cur[2]: self.blocks.append((self.cur[0], t))
            self.cur = None
    def handle_data(self, d):
        if self.cur: self.cur[1].append(d)
def body_blocks(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p.blocks
def menu_text(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    a = s.find('id="module-menu-content"'); b = s.find('id="body"')
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s[a:b] if a >= 0 and b > a else "")).lower()
st = collections.defaultdict(collections.Counter); forms = collections.Counter(); pos = collections.Counter(); ex = []
mods = sorted(m for m in _corpus.gate_mods(CS.CLAUDE) if os.path.isdir(_corpus.mdir(CS.CLAUDE, m)))
pages_hit = collections.defaultdict(set)
for mod in mods:
    fam = re.sub(r"\d.*$", "", mod)
    for n, cp, hp in pairs(mod):
        if "To Do: Lesson menu:" not in open(cp, encoding="utf-8", errors="replace").read(): continue
        bl = body_blocks(cp)
        k = next((i for i, (t, x) in enumerate(bl) if LAB.match(x)), None)
        if k is None: st["ALL"]["no label in body"] += 1; continue
        lab = bl[k][1].lower().rstrip(":?.… ")
        gm = menu_text(hp)
        ing = lab[:18] in gm
        key = ("label in body@" + ("<=6" if k <= 6 else ">6")) + (" / GOLD menu has it" if ing else " / gold menu lacks it")
        st["ALL"][key] += 1; st[fam][key] += 1
        if ing and k <= 6:
            forms[f"{bl[k][0]}:{lab[:24]}"] += 1; pages_hit[fam].add(os.path.basename(cp))
            if len(ex) < 10: ex.append(f"{os.path.basename(cp)} @{k} <{bl[k][0]}> {bl[k][1][:40]!r}")
print("ALL", dict(st["ALL"]))
print("pages (label near the top, gold menu has it):", sum(len(v) for v in pages_hit.values()), "in", len(pages_hit), "families")
print({f: len(v) for f, v in sorted(pages_hit.items(), key=lambda x: -len(x[1]))})
print("forms:", forms.most_common(14))
for x in ex: print("   ", x)
