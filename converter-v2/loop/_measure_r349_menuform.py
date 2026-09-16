#!/usr/bin/env python3
"""_measure_r349_menuform.py — ROUND 349 (Chris's D10-9, KB c23 / 01B) — the measurement before any code.

Over every paired page whose #module-menu-content exists on both sides (the r341 void-aware parser, extended to keep the RAW
label text so colon / case are visible):
  A. the RESIDUE — every Claude learning / success LABEL in a LESSON menu that is not <h5>, by template and subject family,
     and the section TITLES Claude ships above them (01B 223: none);
  B. the WORDING — for each Claude label, the gold's exact string for the same label: does the gold re-word
     ("We are learning to:" → "We are learning:"?), and the gold's colon / case form — the form half of the normalisation;
  C. the OVERVIEW tab — Claude's "We are learning:" / "I can:" labels there (the r81 eng-family <p> form) vs the gold (01B 196–197: <h5>);
  D. the OSSC / "Ākonga will…" split — LABEL (short, colon) vs SENTENCE (the c70 lead-in that stays <p>).
Run under WSL from CONVERTER_V2/outputs: python3 _measure_r349_menuform.py  → _r349_menuform.json + the printed summary."""
import os, sys, re, json, collections
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T = os.path.normpath(os.path.join(HERE, "..", "reference", "tests")); sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, CLAUDE

VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "param", "track"}
def fold(s):
    s = re.sub(r"[‘’'`´]", "'", s); s = re.sub(r"[^\w\s']", " ", s.lower()); return re.sub(r"\s+", " ", s).strip()
class Menu(HTMLParser):
    """(tag, folded, raw) for p/h1-6/li leaves inside #module-menu-content; raw keeps punctuation + case"""
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack = []; self.depth_in = None; self.cur = None; self.buf = []; self.out = []; self.found = False
    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        a = dict(attrs)
        if a.get("id") == "module-menu-content": self.depth_in = len(self.stack); self.found = True
        self.stack.append(tag)
        if self.depth_in is not None and tag in ("p", "h1", "h2", "h3", "h4", "h5", "h6", "li") and self.cur is None: self.cur = tag; self.buf = []
    def handle_startendtag(self, tag, attrs): return
    def handle_endtag(self, tag):
        if tag in VOID: return
        if self.cur is not None and tag == self.cur:
            raw = re.sub(r"\s+", " ", "".join(self.buf)).strip(); t = fold(raw)
            if t: self.out.append((tag, t, raw))
            self.cur = None
        while self.stack:
            top = self.stack.pop()
            if top == tag: break
        if self.depth_in is not None and len(self.stack) <= self.depth_in: self.depth_in = None
    def handle_data(self, d):
        if self.cur is not None: self.buf.append(d)
def menu(path):
    m = Menu(); m.feed(open(path, encoding="utf-8", errors="replace").read()); return m.found, m.out

LEARN = re.compile(r"^(we(?:\s+are)?\s+learning\b|what are we learning|learning intentions?\b|ākonga will\b|akonga will\b|ākonga can\b|students will\b|i am learning to\b|walt\b|what am i learning|what will i learn)")
SUCC = re.compile(r"^(i can\b|you will (?:show|demonstrate) your understanding\b|success criteria\b|how will i know\b|wilf\b|you will be able to\b)")
TITLE = re.compile(r"^(learning intentions?|success criteria|how will i know(?: if i've learned it| i have learned it)?|what are we learning(?: today)?|lesson (?:objectives?|goals?)|ngā whāinga ako|nga whainga ako|whāinga ako|whainga ako|paearu angitu)$")
def role(t):
    if SUCC.match(t): return "success"
    if LEARN.match(t): return "learning"
    return None
def is_sentence(t):
    """a 'label' is short (≤ 7 words); the c70 OSSC lead-in is a sentence"""
    return len(t.split()) > 7

idx = json.load(open(os.path.join(T, "..", "..", "..", "pageforge-site", "converter-v2", "data", "Module_Structure_Index.json"), encoding="utf-8")).get("module_meta", {})
rows = []; ov_rows = []; titles = []; sent = collections.Counter(); sent_ex = []
pages = ov_pages = 0
for code in sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d))):
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code))); meta = idx.get(code, {}); subj = meta.get("subject", "?")
    for n, cp, hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary", os.path.basename(hp) + os.path.basename(cp), re.I): continue
        overview = "_0_0" in cp
        fc, ce = menu(cp); fg, ge = menu(hp)
        if not (fc and fg): continue
        if overview: ov_pages += 1
        else: pages += 1
        gmap = collections.defaultdict(list)
        for tag, t, raw in ge: gmap[t].append((tag, raw))
        gk = list(gmap.keys())
        prev = None
        for i, (tag, t, raw) in enumerate(ce):
            if tag == "li": prev = (tag, t); continue
            if not overview and TITLE.match(t):
                # a section title on a lesson page: what follows it?
                nxt = ce[i + 1] if i + 1 < len(ce) else None
                titles.append({"code": code, "template": tmpl, "subject": subj, "page": os.path.basename(cp), "tag": tag, "text": raw[:60],
                               "next": (nxt[0] + ":" + nxt[1][:30]) if nxt else None, "gold_has": bool(gmap.get(t))})
                prev = (tag, t); continue
            r = role(t)
            if not r: prev = (tag, t); continue
            if r == "learning" and re.match(r"^(ākonga|akonga)", t) or (r == "success" and t.startswith("you will be able")):
                kind = "sentence" if is_sentence(t) else "label"
                sent[(code[:4], kind, tag)] += 1
                if len(sent_ex) < 12: sent_ex.append({"code": code, "page": os.path.basename(cp), "tag": tag, "kind": kind, "text": raw[:90]})
                if kind == "sentence": prev = (tag, t); continue
            # the gold's matching label: exact folded text, else the same leading 3 words
            gold = gmap.get(t)
            if not gold:
                pre = " ".join(t.split()[:3]); cand = [k for k in gk if k.startswith(pre) and role(k)]
                gold = gmap[cand[0]] if cand else []
            gtag = "h5" if any(g[0] == "h5" for g in gold) else (gold[0][0] if gold else "absent")
            graw = next((g[1] for g in gold if g[0] == gtag), None)
            row = {"code": code, "template": tmpl, "subject": subj, "page": os.path.basename(cp), "role": r, "claude": tag, "raw": raw[:70],
                   "gold": gtag, "gold_raw": (graw or "")[:70], "reworded": bool(graw) and fold(graw) != t}
            (ov_rows if overview else rows).append(row)
            prev = (tag, t)

def tally(label, rs, key="claude"):
    c = collections.Counter(r[key] for r in rs)
    print(f"{label:52s} n={len(rs):4d} pages={len(set((r['code'], r['page']) for r in rs)):4d} mods={len(set(r['code'] for r in rs)):3d} | {dict(c.most_common(6))}")
print(f"paired LESSON pages with a menu on both sides: {pages}; OVERVIEW pages: {ov_pages}")
print("\nA. LESSON-menu labels (role learning/success; the OSSC sentences excluded) — Claude's tag:")
tally("  ALL", rows); tally("  Claude <h5>", [r for r in rows if r["claude"] == "h5"], "gold")
RES = [r for r in rows if r["claude"] != "h5"]
tally("  RESIDUE (Claude not <h5>)", RES, "gold")
print("  residue by template:")
for t in ("Standard", "Bilingual", "Fundamentals", "Inquiry"): tally(f"    {t}", [r for r in RES if r["template"] == t], "gold")
print("  residue by subject (n>=3):")
bys = collections.defaultdict(list)
for r in RES: bys[r["subject"]].append(r)
for k, rs in sorted(bys.items(), key=lambda kv: -len(kv[1])):
    if len(rs) >= 3: tally(f"    {k}", rs, "gold")
print("  residue by Claude tag / role:")
tally("    learning", [r for r in RES if r["role"] == "learning"], "claude"); tally("    success", [r for r in RES if r["role"] == "success"], "claude")
print(f"\n  section TITLES Claude ships on lesson pages: {len(titles)} on {len(set((x['code'], x['page']) for x in titles))} pages / {len(set(x['code'] for x in titles))} modules")
tc = collections.Counter((x["tag"], x["text"][:28]) for x in titles)
for (tag, tx), n in tc.most_common(10): print(f"    {n:4d}  {tag}:{tx}")
print(f"    gold keeps the same title: {sum(1 for x in titles if x['gold_has'])} of {len(titles)}")
print("\nB. WORDING — the gold's string for Claude's label (lesson pages, gold label found):")
FOUND = [r for r in rows if r["gold"] != "absent"]
print(f"  gold re-words the label: {sum(1 for r in FOUND if r['reworded'])} of {len(FOUND)}")
byw = collections.defaultdict(collections.Counter)
for r in FOUND: byw[fold(r["raw"])[:24]][fold(r["gold_raw"])[:40]] += 1
for k, c in sorted(byw.items(), key=lambda kv: -sum(kv[1].values()))[:10]: print(f"    {k:26s} -> {dict(c.most_common(4))}")
print("  the gold's EXACT strings (case / colon), top 12:")
gs = collections.Counter(r["gold_raw"] for r in FOUND)
for s, n in gs.most_common(12): print(f"    {n:4d}  {s!r}")
print("  Claude's EXACT strings, top 12:")
cs = collections.Counter(r["raw"] for r in rows)
for s, n in cs.most_common(12): print(f"    {n:4d}  {s!r}")
print("\nC. OVERVIEW tab labels (We are learning / I can …) — Claude's tag vs the gold's:")
tally("  ALL", ov_rows); tally("  Claude <p>", [r for r in ov_rows if r["claude"] == "p"], "gold"); tally("  Claude <h5>", [r for r in ov_rows if r["claude"] == "h5"], "gold")
print("  Claude <p> overview labels by subject:")
bys = collections.defaultdict(list)
for r in ov_rows:
    if r["claude"] == "p": bys[r["subject"]].append(r)
for k, rs in sorted(bys.items(), key=lambda kv: -len(kv[1]))[:12]: tally(f"    {k}", rs, "gold")
print("\nD. 'Ākonga will…' / 'you will be able to…' in Claude's lesson menus — LABEL (≤7 words) vs SENTENCE, by series prefix:")
for (pre, kind, tag), n in sorted(sent.items(), key=lambda kv: -kv[1])[:16]: print(f"    {n:4d}  {pre} {kind} <{tag}>")
for x in sent_ex: print(f"    e.g. {x['code']} {x['page']} <{x['tag']}> {x['kind']}: {x['text']}")
json.dump({"lesson_pages": pages, "overview_pages": ov_pages, "rows": rows, "overview_rows": ov_rows, "titles": titles,
           "sentences": {f"{p} {k} {t}": n for (p, k, t), n in sent.items()}},
          open(os.path.join(HERE, "_r349_menuform.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
