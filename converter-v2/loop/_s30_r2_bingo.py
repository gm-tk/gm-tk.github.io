#!/usr/bin/env python3
"""Session 30 Round 2 PICK census — THE LETTER-GRID BINGO (the BLL family's `[Self check]` + a table of letters with the
red cells = correct → the gold's `div.bingo.col-12 > div.bingoContainer[grid] > div.number[value=correct] > p`).
GOLD side: every bingoContainer on every gold page (all modules): module, page, grid attr, cells, correct cells, the cell's
inner form (p / p.sassoon-text / span.audioTrigger / audioName pattern), the h4 card title, the button row, the wrapper
(`bingo col-12`), the box it sits in (activity class + number) and the box's outer column.
WT side: every `[Self check]` red tag in the parsed WTs followed (within 3 lines) by a TABLE: the table's cell count, red
cell count, the lead sentence, per module. Output: _s30_r2_bingo.out"""
import os, sys, re, glob, json
from collections import Counter, defaultdict
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import HUMAN
from anchor_compare import CLAUDE

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.bingos = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        rec = {"tag": tag, "cls": cls, "attrs": a, "text": [], "kids": []}
        if self.stack: self.stack[-1]["kids"].append(rec)
        self.stack.append(rec)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                rec = self.stack[i]
                if "bingoContainer" in rec["cls"]:
                    # ancestors: the bingo wrapper, the activity box, the outer column
                    anc = self.stack[:i]
                    wrap = next((s for s in reversed(anc) if "bingo" in s["cls"]), None)
                    box = next((s for s in reversed(anc) if s["tag"] == "div" and "activity" in s["cls"]), None)
                    col = next((s for s in reversed(anc) if s["tag"] == "div" and any(c.startswith("col-") for c in s["cls"])), None)
                    self.bingos.append({"rec": rec, "wrap": wrap, "box": box, "col": col})
                del self.stack[i:]; break
    def handle_data(self, d):
        for r in self.stack: r["text"].append(d)

def cell_form(cell):
    """describe a div.number cell: p / p.sassoon-text / p > span.audioTrigger …"""
    parts = []
    def walk(n, depth=0):
        lab = n["tag"] + ("." + ".".join(sorted(n["cls"])) if n["cls"] else "")
        if n["tag"] == "span" and n["attrs"].get("audioname"): lab += "[audioName]"
        parts.append(lab)
        for k in n["kids"]: walk(k, depth + 1)
    for k in cell["kids"]: walk(k)
    return ">".join(parts)

def main():
    g = Counter(); gm = defaultdict(Counter); rows = []
    for code in _corpus.mods(HUMAN):
        d = _corpus.mdir(HUMAN, code)
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"): continue
            p = P(); p.feed(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())
            for b in p.bingos:
                rec = b["rec"]; cells = [k for k in rec["kids"] if "number" in k["cls"]]
                corr = sum(1 for k in cells if (k["attrs"].get("value") or "") == "correct")
                forms = Counter(cell_form(k) for k in cells)
                texts = ["".join(k["text"]).strip() for k in cells]
                letters = all(len(t) <= 2 for t in texts)
                an = [k for k in cells]
                audio = Counter()
                def walk(n):
                    if n["tag"] == "span" and n["attrs"].get("audioname") is not None:
                        audio[re.sub(r"[A-Za-z]$", "X", n["attrs"]["audioname"])] += 1
                    for k in n["kids"]: walk(k)
                for k in cells: walk(k)
                wrap = b["wrap"]; wcls = " ".join(sorted(wrap["cls"])) if wrap else "(none)"
                h4 = any(k["tag"] == "h4" for k in (wrap["kids"] if wrap else []))
                btn = any("activityButton" in kk["cls"] for k in (wrap["kids"] if wrap else []) for kk in k.get("kids", []))
                box = b["box"]; bcls = " ".join(sorted(box["cls"])) if box else "(none)"; num = box["attrs"].get("number") if box else None
                col = " ".join(sorted(c for c in b["col"]["cls"] if c.startswith("col-") or c.startswith("offset"))) if b["col"] else "(none)"
                rows.append(dict(code=code, page=f, grid=rec["attrs"].get("grid"), cells=len(cells), correct=corr, forms=dict(forms), letters=letters,
                                 audio=dict(audio), wrap=wcls, h4=h4, btn=btn, box=bcls, num=num, col=col, texts=texts[:12]))
                g["widgets"] += 1; gm[code]["widgets"] += 1
    L = [f"GOLD bingo widgets: {g['widgets']} on {len({(r['code'], r['page']) for r in rows})} pages / {len(gm)} modules"]
    L.append("  per module: " + ", ".join(f"{c} {n['widgets']}" for c, n in sorted(gm.items(), key=lambda kv: -kv[1]['widgets'])))
    L.append("  grid: " + str(Counter(r["grid"] for r in rows).most_common()))
    L.append("  cells: " + str(Counter(r["cells"] for r in rows).most_common(10)))
    L.append("  correct: " + str(Counter(r["correct"] for r in rows).most_common(10)))
    L.append("  letters-only cells: " + str(Counter(r["letters"] for r in rows)))
    L.append("  wrapper: " + str(Counter(r["wrap"] for r in rows).most_common()))
    L.append("  h4 card title: " + str(Counter(r["h4"] for r in rows)) + "; button row: " + str(Counter(r["btn"] for r in rows)))
    L.append("  box: " + str(Counter(r["box"] for r in rows).most_common(6)))
    L.append("  outer col: " + str(Counter(r["col"] for r in rows).most_common(6)))
    cf = Counter()
    for r in rows:
        for k, v in r["forms"].items(): cf[k] += v
    L.append("  cell forms: " + str(cf.most_common(8)))
    au = Counter()
    for r in rows:
        for k, v in r["audio"].items(): au[k] += v
    L.append("  audioName patterns: " + str(au.most_common(8)))
    L.append("  sample rows:")
    for r in rows[:8]:
        L.append(f"    {r['code']} {r['page']} grid={r['grid']} cells={r['cells']} correct={r['correct']} box={r['box']}#{r['num']} col={r['col']} texts={r['texts']}")
    # ---- WT side
    L.append(""); L.append("WT `[Self check]` tags followed by a table (parsed WTs, all modules):")
    wt = Counter(); wtm = defaultdict(Counter); ex = []
    for code in _corpus.mods(HUMAN):
        d = _corpus.mdir(HUMAN, code)
        for f in glob.glob(os.path.join(d, "*_parsed.txt")):
            lines = open(f, encoding="utf-8", errors="replace").read().split("\n")
            for i, ln in enumerate(lines):
                if re.search(r"\[\s*self[\s-]?check\s*\]", ln, re.I):
                    wt["tags"] += 1; wtm[code]["tags"] += 1
                    # a table within the next 4 lines?
                    j = next((k for k in range(i + 1, min(i + 5, len(lines))) if "TABLE" in lines[k] and "┌" in lines[k]), None)
                    if j is None:
                        wt["no_table"] += 1; continue
                    cells = []; k = j + 1
                    while k < len(lines) and "END TABLE" not in lines[k]:
                        if lines[k].startswith("│"):
                            cells += [c.strip() for c in lines[k][1:].split("║")]
                        k += 1
                    red = sum(1 for c in cells if "[RED TEXT]" in c)
                    plain = [re.sub(r"🔴\[RED TEXT\]|\[/RED TEXT\]🔴", "", c).strip() for c in cells]
                    letters = all(len(c) <= 2 for c in plain if c)
                    wt["with_table"] += 1; wtm[code]["with_table"] += 1
                    wt["letter_grid" if letters else "other_table"] += 1; wtm[code]["letter_grid" if letters else "other_table"] += 1
                    wt[f"cells={len(cells)}"] += 1
                    if len(ex) < 12: ex.append(f"    {code}: {re.sub(r'🔴.*?🔴', '', ln).strip()[:70]} | cells {len(cells)} red {red} letters={letters} → {plain[:8]}")
    L.append(f"  tags {wt['tags']}; with a table {wt['with_table']} (letter grid {wt['letter_grid']} / other {wt['other_table']}); no table {wt['no_table']}")
    L.append("  cell counts: " + ", ".join(f"{k}:{v}" for k, v in wt.items() if k.startswith("cells=")))
    L.append("  per module (tags / with table / letter grid): " + ", ".join(f"{c} {n['tags']}/{n['with_table']}/{n['letter_grid']}" for c, n in sorted(wtm.items(), key=lambda kv: -kv[1]['with_table'])))
    L += ex
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r2_bingo.out"), "w", encoding="utf-8").write(txt + "\n")
    json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r2_bingo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(txt[:9000])

main()
