#!/usr/bin/env python3
"""Session 30 Round 3 PICK — THE SASSOON WRITING FONT (KB 14.7 BLL: any text the ākonga must read or interact with): where does
the gold apply `sassoon-text` / `sassoonI-text`? Over every gold page of the BLL / TRR / other modules: the sassoon carriers by
(tag, whole-element or inner span, parent/box context), and for the same contexts the share of elements WITHOUT sassoon, so a
≥ 0.60 context can be found. Also what the text is (single letter / word / sentence) and whether Claude's page has the text.
Output: _s30_r3_sassoon.out"""
import os, sys, re, json, glob
from collections import Counter, defaultdict
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, HUMAN
from anchor_compare import CLAUDE
BOX = {"activity", "alert", "alertActivity", "supervisor", "super-content", "bingo", "dragAndDrop", "flipCard", "carousel", "accordion", "tabs", "clickDrop", "table-responsive", "moduleMenu", "wordSelect", "memoryGame", "typing", "multiChoiceQuiz", "dropQuiz", "reorder", "wordDrag", "audioImage", "speechBubble"}
SAS = ("sassoon-text", "sassoonI-text")

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.els = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        self.stack.append({"tag": tag, "cls": cls, "text": [], "kids": []})
        if len(self.stack) > 1: self.stack[-2]["kids"].append((tag, cls))
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                txt = re.sub(r"\s+", " ", "".join(rec["text"])).strip()
                if tag in ("p", "li", "td", "th", "h2", "h3", "h4", "h5", "span", "b") and txt:
                    box = next((c for s in reversed(self.stack[:i]) for c in s["cls"] if c in BOX), "body")
                    par = self.stack[i - 1]["tag"] if i > 0 else "?"
                    sas = next((c for c in rec["cls"] if c in SAS), None)
                    kidsas = any(any(c in SAS for c in k[1]) for k in rec["kids"])
                    self.els.append({"tag": tag, "par": par, "box": box, "sas": sas, "kidsas": kidsas, "text": txt})
                del self.stack[i:]; break
    def handle_data(self, d):
        for s in self.stack: s["text"].append(d)

def kind(t):
    t = t.strip("‘’'\"“” ")
    if len(t) <= 2: return "letter"
    if " " not in t: return "word"
    if len(t.split()) <= 4: return "phrase"
    return "sentence"

def main():
    by = defaultdict(Counter); pages = Counter(); mods = Counter(); kinds = Counter(); ex = defaultdict(list)
    for code in _corpus.mods(HUMAN):
        pref = re.match(r"[A-Z]+", code).group(0) if re.match(r"[A-Z]+", code) else code
        d = _corpus.mdir(HUMAN, code)
        for f in glob.glob(os.path.join(d, "*.html")):
            if re.search(r"acks|glossary|references", os.path.basename(f), re.I): continue
            p = P(); p.feed(open(f, encoding="utf-8", errors="replace").read())
            has = False
            for e in p.els:
                if e["tag"] in ("span", "b"):
                    if e["sas"]:
                        by[(pref, "inner-" + e["tag"], e["par"], e["box"])]["sas"] += 1; kinds[(pref, "inner", kind(e["text"]))] += 1; has = True
                        if len(ex[(pref, "inner", e["par"], e["box"])]) < 3: ex[(pref, "inner", e["par"], e["box"])].append(e["text"][:40])
                    continue
                key = (pref, e["tag"], e["box"])
                if e["sas"]: by[key]["whole-sas"] += 1; has = True; kinds[(pref, "whole", kind(e["text"]))] += 1
                elif e["kidsas"]: by[key]["inner-sas"] += 1; has = True
                else: by[key]["none"] += 1
            if has: pages[pref] += 1; mods[(pref, code)] += 1
    L = ["GOLD sassoon usage — pages by prefix: " + str(pages.most_common(12))]
    L.append("modules by prefix: " + str(Counter(k[0] for k in mods).most_common(12)))
    L.append("text kinds: " + str(kinds.most_common(16)))
    L.append("BLOCK elements by (prefix, tag, box): whole-sas / inner-sas / none — contexts where sassoon (whole or inner) >= 0.60 and n >= 20:")
    rows = []
    for k, t in by.items():
        if k[1].startswith("inner-"): continue
        n = sum(t.values())
        if n < 20: continue
        s = (t["whole-sas"] + t["inner-sas"]) / n
        rows.append((s, n, k, dict(t)))
    for s, n, k, t in sorted(rows, key=lambda r: (-r[0], -r[1])):
        if s >= 0.30: L.append(f"  {str(k):50s} n={n:5d} sas {s:.2f} {t}")
    L.append("INNER spans (prefix, span/b, parent, box) top 20:")
    for k, t in sorted(((k, t) for k, t in by.items() if k[1].startswith("inner-")), key=lambda kv: -sum(kv[1].values()))[:20]:
        L.append(f"  {str(k):55s} {sum(t.values())}  e.g. {ex.get((k[0], 'inner', k[2], k[3]), [])}")
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r3_sassoon.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt[:8000])
main()
