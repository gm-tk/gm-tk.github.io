#!/usr/bin/env python3
"""Session 30 Round 3 PICK — THE WRITER'S BOLD, PAIRED: for every `<b>` / `<strong>` on Claude's paired pages, its context
(parent tag / class ladder; whole-element bold or partial; the text) → on the gold page: the same text inside a <b>/<strong>
(kept), present as plain text (STRIPPED), inside a heading (h2–h5 — promoted), or absent. Per context, per (template, subject),
plus the reverse (gold bold Claude lacks: by context). Output: _s30_r3_bold.out"""
import os, sys, re, json
from collections import Counter, defaultdict
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, HUMAN
from anchor_compare import CLAUDE
META = json.load(open("/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/data/Module_Structure_Index.json", encoding="utf-8")).get("module_meta", {})
BOX = {"alert", "activity", "supervisor", "super-content", "whakatauki", "wananga", "accordion", "tabs", "flipCard", "carousel", "clickDrop", "cv2-interactive", "table-responsive", "moduleMenu", "acks"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.bolds = []; self.heads = []; self.plain = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        self.stack.append({"tag": tag, "cls": cls, "text": [], "kids": 0, "own": []})
        if len(self.stack) > 1: self.stack[-2]["kids"] += 1
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                txt = re.sub(r"\s+", " ", "".join(rec["text"])).strip()
                if tag in ("b", "strong") and txt:
                    par = self.stack[i - 1] if i > 0 else None
                    ptxt = re.sub(r"\s+", " ", "".join(par["text"])).strip() if par else ""
                    box = next((c for s in reversed(self.stack[:i]) for c in s["cls"] if c in BOX), "body")
                    whole = bool(par) and ptxt == txt
                    self.bolds.append({"text": txt, "parent": par["tag"] if par else "?", "pcls": " ".join(par["cls"]) if par else "", "box": box, "whole": whole})
                elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and txt:
                    self.heads.append(txt)
                elif tag in ("p", "li", "td", "th") and txt:
                    self.plain.append(txt)
                del self.stack[i:]; break
    def handle_data(self, d):
        for r in self.stack: r["text"].append(d)

def parse(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p
def fold(t): return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()

def main():
    ctx = defaultdict(Counter); grp = defaultdict(Counter); ex = defaultdict(list); tot = Counter(); rev = Counter()
    for code in _corpus.gate_mods(CLAUDE):
        pr = pairs(code)
        if not pr: continue
        m = META.get(code, {}); g = (m.get("template_type") or "?", m.get("subject") or "?")
        for _k, cp, hp in pr:
            c = parse(cp); h = parse(hp)
            hb = Counter(fold(b["text"]) for b in h.bolds)
            hh = set(fold(t) for t in h.heads)
            hpl = set(fold(t) for t in h.plain)
            htxt = fold(open(hp, encoding="utf-8", errors="replace").read())
            for b in c.bolds:
                f = fold(b["text"])
                if len(f) < 3: continue
                if hb[f] > 0: hb[f] -= 1; res = "kept"
                elif f in hh: res = "heading"
                elif f in hpl: res = "stripped(whole)"
                elif len(f) >= 8 and f in htxt: res = "stripped(inline)"
                else: res = "absent"
                key = (b["parent"], "whole" if b["whole"] else "part", b["box"])
                ctx[key][res] += 1; grp[g][res] += 1; tot[res] += 1
                if res.startswith("stripped") and len(ex[key]) < 3: ex[key].append(f"{code} {os.path.basename(cp)}: «{b['text'][:50]}» in {b['parent']}.{b['pcls'][:20]}")
            cb = Counter(fold(b["text"]) for b in c.bolds)
            for b in h.bolds:
                f = fold(b["text"])
                if cb[f] > 0: cb[f] -= 1
                else: rev[(b["parent"], "whole" if b["whole"] else "part", b["box"])] += 1
    L = [f"CLAUDE bold on the paired pages → on the gold: {dict(tot)}"]
    L.append("by context (parent, whole/part, box) n >= 30 — kept / heading / stripped / absent:")
    for k, t in sorted(ctx.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(t.values())
        if n < 30: continue
        st = t["stripped(whole)"] + t["stripped(inline)"]
        L.append(f"  {str(k):48s} n={n:5d} kept {t['kept']/n:.2f} heading {t['heading']/n:.2f} stripped {st/n:.2f} absent {t['absent']/n:.2f}")
    L.append("by (template, subject) n >= 50:")
    for k, t in sorted(grp.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(t.values())
        if n < 50: continue
        st = t["stripped(whole)"] + t["stripped(inline)"]
        L.append(f"  {str(k):52s} n={n:5d} kept {t['kept']/n:.2f} heading {t['heading']/n:.2f} stripped {st/n:.2f} absent {t['absent']/n:.2f}")
    L.append("REVERSE — gold bold Claude lacks, by context (top 12): " + str(rev.most_common(12)))
    L.append("examples (stripped):")
    for k, v in list(ex.items())[:14]:
        L.append(f"  {k}: " + " | ".join(v))
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r3_bold.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt[:8000])
main()
