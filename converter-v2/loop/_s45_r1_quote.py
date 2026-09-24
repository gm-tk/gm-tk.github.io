#!/usr/bin/env python3
"""Session 45 Round 1 — KB 01F / 05D `quote` (`<p class="quoteText">"Quote"</p><p class="quoteAck">Attribution</p>`).
(A) every writer [quote] tag (aliases quote / quotetext / quotation / pull quote) in every Writers Template of the scored population:
    the quoted text, and the element that carries it in the GOLD and in CLAUDE (tag.class + the enclosing container class).
(B) the reverse: every gold p.quoteText / p.quoteAck — which writer tag (if any) stands on the WT line that carries its text.
WSL, from outputs/: python3 _s45_r1_quote.py > _s45_r1_quote.log"""
import os, re, sys, glob, io, collections, html as H
from html.parser import HTMLParser
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
def norm(t): return re.sub(r"[^\wĀ-ſ ]+", "", re.sub(r"\s+", " ", H.unescape(t))).strip().lower()
VOID = ("br", "img", "hr", "input", "source", "meta", "link", "audio", "wbr", "col")
BLOCK = ("p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "figcaption", "blockquote")
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.st = []; s.out = []; s.cur = None
    def handle_starttag(s, t, a):
        if t in VOID: return
        d = dict(a); cls = d.get("class") or ""
        s.st.append((t, cls))
        if t in BLOCK and s.cur is None:
            s.cur = {"tag": t, "cls": cls, "txt": [], "st": list(s.st[:-1]), "depth": len(s.st)}
    def handle_endtag(s, t):
        if s.cur is not None and t == s.cur["tag"] and len(s.st) == s.cur["depth"]:
            s.cur["txt"] = norm("".join(s.cur["txt"])); s.out.append(s.cur); s.cur = None
        while s.st:
            if s.st.pop()[0] == t: break
    def handle_data(s, d):
        if s.cur is not None: s.cur["txt"].append(d)
def blocks(d):
    out = []
    for p in sorted(glob.glob(os.path.join(d, "*.html"))):
        x = P()
        try: x.feed(io.open(p, encoding="utf-8", errors="replace").read())
        except Exception: continue
        for b in x.out: b["page"] = os.path.basename(p)
        out += x.out
    return out
def container(b):
    for t, c in reversed(b["st"]):
        if re.search(r"\b(quoteText|whakatauki|alert|activity|cv2-interactive|accContent|tab-pane|carousel|card)\b", c):
            return re.search(r"\b(quoteText|whakatauki|alert|activity|cv2-interactive|accContent|tab-pane|carousel|card)\b", c).group(1)
    return "free"
def form(b):
    c = " ".join(sorted(x for x in b["cls"].split() if x in ("quoteText", "quoteAck", "quoteTextReg")))
    return b["tag"] + ("." + c if c else "")
def find(bl, key):
    for b in bl:
        if key and key in b["txt"]: return b
    return None
TAGRE = re.compile(r"\[\s*(quote|quotetext|quotation|pull quote)\s*\]", re.I)
def clean(line):
    line = re.sub(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴", " ", line)
    line = re.sub(r"\[[^\]]{0,40}\]", " ", line)
    return norm(line.replace("*", ""))
ANYTAG = re.compile(r"\[\s*([A-Za-z][A-Za-z0-9 _\-/]{0,30})\s*\]")
def main():
    global A
    A = collections.Counter(); Aex = collections.defaultdict(list); Amods = collections.defaultdict(set)
    B = collections.Counter(); Bex = collections.defaultdict(list); Bmods = collections.defaultdict(set)
    ntag = 0; tagmods = set()
    for code in _corpus.gate_mods(GOLD):
        gd = _corpus.mdir(GOLD, code); cd = _corpus.mdir(CL, code)
        wts = [p for p in glob.glob(os.path.join(gd, "*_parsed.txt")) if "writers template" in os.path.basename(p).lower()]
        if not wts: continue
        lines = []
        for w in wts: lines += io.open(w, encoding="utf-8", errors="replace").read().split("\n")
        gbl = blocks(gd); cbl = blocks(cd) if os.path.isdir(cd) else []
        # (A)
        for i, ln in enumerate(lines):
            if not TAGRE.search(ln): continue
            ntag += 1; tagmods.add(code)
            txt = clean(ln); j = i
            while len(txt) < 12 and j + 1 < len(lines) and j < i + 3:
                j += 1; txt = clean(lines[j])
            key = txt[:40]
            g = find(gbl, key); c = find(cbl, key)
            k = ((form(g) + " in " + container(g)) if g else "ABSENT", (form(c) + " in " + container(c)) if c else "ABSENT")
            A[k] += 1; Amods[k].add(code)
            if len(Aex[k]) < 4: Aex[k].append(f"{code} «{key[:50]}»")
        # (B)
        for g in gbl:
            if "quoteText" not in g["cls"] and "quoteAck" not in g["cls"]: continue
            key = g["txt"][:40]
            if len(key) < 8: continue
            tag = "NOT-IN-WT"
            for ln in lines:
                if key in norm(ln.replace("*", "")) or key in clean(ln):
                    t = [m.group(1).strip().lower() for m in ANYTAG.finditer(ln) if m.group(1).strip().upper() not in ("RED TEXT", "/RED TEXT")]
                    tag = ("tag:" + t[0]) if t else "untagged"
                    break
            c = find(cbl, key)
            k = (form(g), tag, (form(c) + " in " + container(c)) if c else "ABSENT")
            B[k] += 1; Bmods[k].add(code)
            if len(Bex[k]) < 3: Bex[k].append(f"{code}/{g['page']} «{key[:45]}»")
    print(f"(A) writer [quote] tags: {ntag} in {len(tagmods)} modules")
    for k, n in A.most_common():
        print(f"  {n:4d} {len(Amods[k]):3d}m  gold={k[0]:34s} claude={k[1]:34s} {' | '.join(Aex[k])}")
    print(f"\n(B) gold quoteText / quoteAck blocks: {sum(B.values())} in {len(set().union(*Bmods.values())) if Bmods else 0} modules")
    for k, n in B.most_common(40):
        print(f"  {n:4d} {len(Bmods[k]):3d}m  gold={k[0]:22s} wt={k[1]:22s} claude={k[2]:30s} {' | '.join(Bex[k])}")
if __name__ == "__main__":
    main()
