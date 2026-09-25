"""_s50_r3_unclasstable.py — session 50 Round 3 PICK: every UNCLASSIFIED hand-off box on the paired Claude pages that holds a
<table> — where does the GOLD put that table's text? (a plain <table> in the body / activity, inside a built widget, elsewhere,
absent). Per family (code prefix) and template. Run under WSL from CONVERTER_V2/reference/tests/:
    python3 ../../outputs/_s50_r3_unclasstable.py [CODES…]  → ../../outputs/_s50_r3_unclasstable.{log,json}"""
import os, sys, re, json, collections
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _corpus

WIDGETS = {"dragAndDrop", "multiChoiceQuiz", "clickDrop", "flipCard", "flipCardsContainer", "dropQuiz", "accordion", "carousel",
           "typing", "modal", "selfCheck", "reorder", "tabs", "radioQuiz", "selectionBox", "speechBubble", "slider", "hint",
           "hintSlider", "memoryGame", "wordFind", "crossword", "sketcher", "bingo", "wordSelect", "wordDrag", "timeline", "puzzle"}
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


class P(HTMLParser):
    """Text nodes with (in_table, widget_class_or_None, in_activity, in_cv2box, cv2_label)."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.nodes = []; self.label = None
    def handle_starttag(self, tag, attrs):
        if tag in ("br", "img", "hr", "input", "meta", "link", "source"): return
        cls = (dict(attrs).get("class") or "").split()
        self.stack.append((tag, cls))
    def handle_endtag(self, tag):
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k][0] == tag:
                del self.stack[k:]; break
    def handle_data(self, d):
        t = d.strip()
        if not t: return
        m = re.match(r"⚙ INTERACTIVE \(un-built\) #\d+: (\w+)", t)
        if m: self.label = m.group(1)
        in_table = any(tg == "table" for tg, _ in self.stack)
        widget = next((c for _, cl in self.stack for c in cl if c in WIDGETS), None)
        act = any("activity" in cl for _, cl in self.stack)
        cv2 = any(any(c.startswith("cv2-interactive") for c in cl) for _, cl in self.stack)
        self.nodes.append((t, in_table, widget, act, cv2, self.label if cv2 else None))


def parse(p):
    x = P()
    try: x.feed(open(p, encoding="utf-8", errors="ignore").read())
    except Exception: pass
    return x.nodes


CLAUDE = os.path.join(os.getcwd(), "..", "..", "..", "01-Claude_Modules_")
codes = sys.argv[1:] or sorted(_corpus.gate_mods(CLAUDE))
fate = collections.Counter(); byfam = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
boxes = 0
for code in codes:
    try: prs = list(DA.pairs(code))
    except Exception: continue
    fam = re.match(r"[A-Z]+", code).group(0)
    for _, cp, hp in prs:
        cn = parse(cp)
        # the unclassified boxes' table cells, grouped per box label occurrence
        cells = [(t, lab) for (t, tb, w, a, cv2, lab) in cn if cv2 and tb and lab == "unclassified" and len(norm(t)) >= 8]
        if not cells: continue
        gn = parse(hp)
        gtxt = [(norm(t), tb, w, a) for (t, tb, w, a, cv2, lab) in gn]
        # one verdict per page (the box cells together): majority fate of up to 6 cells
        votes = collections.Counter()
        for t, _ in cells[:6]:
            k = norm(t)
            hit = next(((tb, w, a) for (g, tb, w, a) in gtxt if k and (k in g or (len(g) >= 8 and g in k))), None)
            if hit is None: votes["absent"] += 1
            elif hit[1]: votes["widget:" + hit[1]] += 1
            elif hit[0]: votes["plain-table" + ("-in-activity" if hit[2] else "")] += 1
            else: votes["free-text" + ("-in-activity" if hit[2] else "")] += 1
        v = votes.most_common(1)[0][0]
        boxes += 1; fate[v] += 1; byfam[fam][v] += 1
        if len(ex[v]) < 6: ex[v].append(f"{os.path.basename(cp)}: {cells[0][0][:60]}")
out = {"pages": boxes, "fate": fate.most_common(), "by_family": {f: c.most_common() for f, c in sorted(byfam.items(), key=lambda kv: -sum(kv[1].values()))}, "examples": ex}
json.dump(out, open("../../outputs/_s50_r3_unclasstable.json", "w"), indent=1, ensure_ascii=False)
with open("../../outputs/_s50_r3_unclasstable.log", "w") as fh:
    fh.write(f"paired pages with an unclassified box holding a table: {boxes}\nFATE (page majority): {fate.most_common()}\n\nBY FAMILY (pages):\n")
    for f, c in sorted(byfam.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(c.values()); pl = sum(v for k, v in c.items() if k.startswith("plain-table"))
        fh.write(f"  {f:8s} {n:4d}  plain-table {pl/n:.2f}  {c.most_common(4)}\n")
    fh.write("\nEXAMPLES:\n" + "\n".join(f"  {k}: {v}" for k, v in ex.items()) + "\n")
print(open("../../outputs/_s50_r3_unclasstable.log").read()[:3000])
