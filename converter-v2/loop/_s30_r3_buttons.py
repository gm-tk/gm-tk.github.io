#!/usr/bin/env python3
"""Session 30 Round 3 PICK — THE MISSING `div.button`: for every gold `div.button` (and `div.buttonD` / externalButton) on a paired
page, its text; is that text on Claude's page (a) as a button, (b) as other markup (which tag), (c) absent? And the reverse: Claude's
buttons whose text the gold has as a non-button. Per text-family (journal / upload / download / watch / link / other) and per
(template, subject). Output: _s30_r3_buttons.out"""
import os, sys, re, json
from collections import Counter, defaultdict
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, HUMAN
from anchor_compare import CLAUDE
META = json.load(open("/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/data/Module_Structure_Index.json", encoding="utf-8")).get("module_meta", {})
BTN = {"button", "buttonD", "externalButton", "activityButton"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.buttons = []; self.texts = []   # texts: (tag, cls, text) for every element with direct text
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        self.stack.append({"tag": tag, "cls": cls, "text": [], "href": a.get("href")})
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                txt = re.sub(r"\s+", " ", "".join(rec["text"])).strip()
                if tag == "div" and (set(rec["cls"]) & BTN):
                    self.buttons.append((sorted(set(rec["cls"]) & BTN)[0], txt))
                elif txt and tag not in ("div", "body", "html", "script", "style", "section"):
                    self.texts.append((tag, " ".join(rec["cls"]), txt))
                del self.stack[i:]; break
    def handle_data(self, d):
        for r in self.stack: r["text"].append(d)

def parse(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read()); return p
def fold(t): return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()
def fam(t):
    t = t.lower()
    if "journal" in t: return "journal"
    if "upload" in t or "dropbox" in t or "drop box" in t: return "upload"
    if "download" in t: return "download"
    if "watch" in t or "video" in t: return "watch"
    if "quiz" in t: return "quiz"
    if re.match(r"^(go to|open|visit|read|see|view|click|explore|listen|play)\b", t): return "goto/open/…"
    return "other"

def main():
    tot = Counter(); byfam = defaultdict(Counter); bygrp = defaultdict(Counter); ex = defaultdict(list); rev = Counter()
    for code in _corpus.gate_mods(CLAUDE):
        pr = pairs(code)
        if not pr: continue
        m = META.get(code, {}); grp = (m.get("template_type") or "?", m.get("subject") or "?")
        for _k, cp, hp in pr:
            g = parse(hp); c = parse(cp)
            cb = Counter(fold(t) for _, t in c.buttons)
            ct = defaultdict(list)
            for tag, cls, t in c.texts: ct[fold(t)].append((tag, cls))
            cpage = fold(open(cp, encoding="utf-8", errors="replace").read())
            for kind, t in g.buttons:
                f = fold(t)
                if not f: continue
                if cb[f] > 0: cb[f] -= 1; res = "button"
                elif f in ct: res = "other:" + ct[f][0][0] + ("." + ct[f][0][1].split()[0] if ct[f][0][1] else "")
                elif len(f) >= 12 and f in cpage: res = "other:inline"
                else: res = "absent"
                tot[res.split(":")[0]] += 1; byfam[fam(t)][res.split(":")[0]] += 1; bygrp[grp][res.split(":")[0]] += 1
                if res.startswith("other") and len(ex[res]) < 6: ex[res].append(f"{code} {os.path.basename(cp)}: «{t[:60]}»")
                if res.startswith("other"): tot["other-detail:" + res] += 1
            gb = Counter(fold(t) for _, t in g.buttons)
            for kind, t in c.buttons:
                f = fold(t)
                if gb[f] > 0: gb[f] -= 1
                else: rev[fam(t)] += 1
    L = ["GOLD buttons on the paired pages → on Claude's page as:", f"  {dict((k, v) for k, v in tot.items() if not k.startswith('other-detail'))}"]
    L.append("  other-markup detail: " + str(Counter({k[13:]: v for k, v in tot.items() if k.startswith("other-detail")}).most_common(12)))
    L.append("by text family:")
    for f, t in sorted(byfam.items(), key=lambda kv: -sum(kv[1].values())): L.append(f"  {f:14s} {dict(t)}")
    L.append("by (template, subject) n >= 30 — button / other / absent:")
    for k, t in sorted(bygrp.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(t.values())
        if n < 30: continue
        L.append(f"  {str(k):52s} n={n:4d} button {t['button']/n:.2f} other {t['other']/n:.2f} absent {t['absent']/n:.2f}")
    L.append("Claude buttons the gold lacks (by family): " + str(dict(rev)))
    L.append("examples (gold button, Claude has the text as other markup):")
    for k, v in ex.items():
        L.append(f"  [{k}]")
        for e in v: L.append("    " + e)
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r3_buttons.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt[:7000])
main()
