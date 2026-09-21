#!/usr/bin/env python3
"""Session 30 Round 1 — the gold's language-span FORM census: for every ch-text / jp-text / pinyin element in the
gold pages of the language modules — the carrier tag, its parent, whether it holds child elements (and which), the
non-CJK characters inside the span (run-boundary rule), whether the span text starts / ends with a non-CJK char,
and the run-splitting: how many spans hold a space / ASCII punctuation / digits / Latin letters."""
import os, sys, re, json
from collections import Counter
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import HUMAN
CJKCH = re.compile(r"[぀-ヿ㐀-䶿一-鿿豈-﫿＀-￯　-〿]")
HANKANA = re.compile(r"[぀-ヿ㐀-䶿一-鿿豈-﫿]")
LANG = {"ch-text", "jp-text", "pinyin"}
MODS = ["CHI1003", "CHI1004", "CHI1005", "CHFUN01", "CHFUN04", "CHFUN05", "CHFUN06", "CHFUN07", "CHFUN08", "CHWHA", "JPN1004", "JPFUN01", "JPFUN02"]

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.spans = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = set((a.get("class") or "").split())
        rec = {"tag": tag, "cls": cls, "text": [], "kids": [], "parent": self.stack[-1]["tag"] if self.stack else "?", "pcls": self.stack[-1]["cls"] if self.stack else set()}
        if self.stack:
            self.stack[-1]["kids"].append(tag)
        self.stack.append(rec)
    def handle_startendtag(self, tag, attrs):
        if self.stack:
            self.stack[-1]["kids"].append(tag)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if rec["cls"] & LANG:
                    self.spans.append(rec)
                del self.stack[i:]
                break
    def handle_data(self, d):
        for r in self.stack:
            r["text"].append(d)

def main():
    L = []
    tot = Counter(); nonCJK = Counter(); edge = Counter(); par = Counter(); kids = Counter(); carrier = Counter()
    pin_chars = Counter(); pin_edge = Counter(); pin_words = Counter(); pin_par = Counter()
    ex = []
    for code in MODS:
        d = _corpus.mdir(HUMAN, code)
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"):
                continue
            p = P()
            p.feed(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())
            for s in p.spans:
                cls = sorted(s["cls"] & LANG)[0]
                txt = "".join(s["text"])
                tot[cls] += 1
                carrier[(cls, s["tag"])] += 1
                par[(cls, s["parent"])] += 1
                kids[(cls, tuple(sorted(set(s["kids"]))))] += 1
                if cls in ("ch-text", "jp-text"):
                    t = txt.strip()
                    for ch in t:
                        if not CJKCH.match(ch):
                            nonCJK[ch] += 1
                    if t:
                        edge[("start", "cjk" if CJKCH.match(t[0]) else repr(t[0]))] += 1
                        edge[("end", "cjk" if CJKCH.match(t[-1]) else repr(t[-1]))] += 1
                    if t and not HANKANA.search(t):
                        ex.append((code, f, cls, t[:60]))
                    # inner tokens: does the run contain spaces / latin / digits?
                    if " " in t: tot["cjk_with_space"] += 1
                    if re.search(r"[A-Za-z]", t): tot["cjk_with_latin"] += 1
                    if re.search(r"[0-9]", t): tot["cjk_with_digit"] += 1
                    if re.search(r"[　-〿＀-￯]", t): tot["cjk_with_cjkpunct"] += 1
                    if re.search(r"[()\[\]/.,:;!?]", t): tot["cjk_with_asciipunct"] += 1
                else:
                    t = txt.strip()
                    pin_par[s["parent"]] += 1
                    for ch in t:
                        if ch in "áéíóúǎěǐǒǔàèìòùǖǘǚǜü": pin_chars["tone_nonmacron"] += 1
                        elif ch in "āēīōū": pin_chars["macron"] += 1
                    if not re.search(r"[áéíóúǎěǐǒǔàèìòùǖǘǚǜüĀĒĪŌŪāēīōūÁÉÍÓÚǍĚǏǑǓÀÈÌÒÙ]", t): pin_chars["no_tone_at_all"] += 1
                    elif not re.search(r"[áéíóúǎěǐǒǔàèìòùǖǘǚǜüÁÉÍÓÚǍĚǏǑǓÀÈÌÒÙ]", t): pin_chars["macron_only"] += 1
                    else: pin_chars["has_nonmacron_tone"] += 1
                    if " " in t: pin_words["multiword"] += 1
                    else: pin_words["single"] += 1
                    if t and t[-1] in ".?!。": pin_words["ends_punct"] += 1
                    if len(ex) < 40 and not re.search(r"[áéíóúǎěǐǒǔàèìòùǖǘǚǜü]", t):
                        ex.append((code, f, "pinyin-no-nonmacron-tone", t[:60]))
    L.append(f"totals {dict(tot)}")
    L.append(f"carrier {dict(carrier.most_common(12))}")
    L.append(f"parent {dict(par.most_common(20))}")
    L.append(f"kids {dict(kids.most_common(12))}")
    L.append(f"nonCJK chars inside ch/jp spans: {dict(nonCJK.most_common(40))}")
    L.append(f"edges: {dict(edge.most_common(20))}")
    L.append(f"pinyin chars {dict(pin_chars)}; words {dict(pin_words)}; parents {dict(pin_par.most_common(10))}")
    L.append("examples (no-HanKana ch/jp spans; pinyin spans with no non-macron tone):")
    for e in ex[:60]:
        L.append("  " + " | ".join(e))
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r1_langspans.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt)

main()
