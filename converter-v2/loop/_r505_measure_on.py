#!/usr/bin/env python3
"""claude-audit Phase 3 (the loop's session 40 Round 5) — the [RHS alert] family MEASURE (answer 4 of Chris's approved
claude-audit changes; the r182 solidify rule decides). Population: every Writers Template tag matching [rhs alert…],
[right-hand alert…], [alert box rhs…], [alert rhs…] (+ the other right-hand spellings the brief lists — [alert box right
hand side…], [rhc alert…]). For each tag: the writer's text (the black text after the tag on its line, else the next
non-empty line), then in the module's GOLD pages and in its CLAUDE pages the element that carries that text, classified:
  side-alertActivity  an alertActivity inside a col-md-4 / col-md-3 side column
  side-alert-top      an 'alert top' (or other alert) inside a side column
  alert               a full-width div.alert (any modifier)
  bubble-thought      a speechBubble with layout="thought"
  bubble              any other speech bubble
  side-other          a side column (col-md-4 / col-md-3) with no alert
  body                anything else (a body paragraph)
  absent              the text is not on any page
Reports per spelling and overall; shares of the gold shapes; Claude vs gold agreement. Writes _rhsalert_measure.{json,log}."""
import os, re, io, json, glob, collections, unicodedata
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TAG = re.compile(r"\[\s*(?:(?:rhs|rhc)\s+alert|right[\s-]*hand(?:\s+side)?\s+alert|alert\s+box\s+(?:rhs|rhc|right[\s-]*hand(?:\s+side)?)|alert\s+(?:rhs|rhc|right[\s-]*hand(?:\s+side)?))\b[^\]]*\]", re.I)
RED = re.compile(r"\U0001F534\[RED TEXT\]|\[/RED TEXT\]\U0001F534")
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "area", "col", "embed", "wbr", "track", "param", "base"}
def fold(s):
    s = unicodedata.normalize("NFKD", s); s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack = []; self.nodes = []
    def handle_starttag(self, t, a):
        if t in VOID: return
        d = dict(a); self.stack.append((t, d.get("class") or "", d.get("layout") or ""))
    def handle_endtag(self, t):
        if t in VOID: return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == t: del self.stack[i:]; break
    def handle_data(self, d):
        if d.strip(): self.nodes.append((d, list(self.stack)))
def classify(anc):
    classes = [c for _, c, _ in anc]; lay = [l for _, _, l in anc]
    for (t, c, l) in reversed(anc):
        if "speechbubble" in c.lower() or re.search(r"\bbubble", c.lower()):
            return "bubble-thought" if any(x == "thought" for x in lay) else "bubble"
    # ROUND 505 (D15-18, the D15 report's correction 4): the humans also write a plain col-4 / col-3 side column (r333 counted both)
    side = any(re.search(r"\bcol-(?:md-)?[34]\b", c) for c in classes)
    if any("alertActivity" in c for c in classes): return "side-alertActivity" if side else "alertActivity"
    if any(re.search(r"(^|\s)alert(\s|$)", c) for c in classes): return "side-alert-top" if side else "alert"
    return "side-other" if side else "body"
cache = {}
def pages(d):
    if d not in cache:
        out = []
        for f in sorted(glob.glob(os.path.join(d, "*.html"))):
            s = io.open(f, encoding="utf-8", errors="replace").read()
            s = re.sub(r"<!--[\s\S]*?-->", "", s)
            p = P(); p.feed(s)
            out.append((os.path.basename(f), [(fold(t), anc) for t, anc in p.nodes]))
        cache[d] = out
    return cache[d]
def locate(d, snippet):
    for fn, nodes in pages(d):
        for ft, anc in nodes:
            if snippet and snippet in ft: return fn, classify(anc)
    # a snippet split over inline nodes: try the first 3 words
    short = " ".join(snippet.split()[:3])
    for fn, nodes in pages(d):
        for ft, anc in nodes:
            if len(short) > 8 and short in ft: return fn, classify(anc)
    return None, "absent"
rows = []
for wt in glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", "*", "*", "*Writers Template*_parsed.txt")):
    gdir = os.path.dirname(wt); code = os.path.basename(gdir); tpl = os.path.basename(os.path.dirname(gdir))
    cdirs = ([os.path.join(HERE, os.environ["ON_DIR"], code)] if os.path.isdir(os.path.join(HERE, os.environ.get("ON_DIR", "-"), code)) else []) + glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", code)) + glob.glob(os.path.join(ROOT, "01-Claude_Modules_", code))
    lines = io.open(wt, encoding="utf-8", errors="replace").read().split("\n")
    for i, ln in enumerate(lines):
        plain = RED.sub(" ", ln)
        for m in TAG.finditer(plain):
            after = re.sub(r"\[[^\]]*\]", " ", plain[m.end():]).replace("*", " ").strip()
            j = i + 1
            # ROUND 505 (correction 4): a table-marker line (┌─── TABLE ───, └─── END TABLE ───) and a cell's │ rails are not the
            # writer's text (the six TEDC402 rows had read the marker as the tag's text)
            TBL = re.compile(r"^[\s│]*[┌└├]")
            while (not after or TBL.match(after)) and j < len(lines) and j <= i + 6:
                after = re.sub(r"\[[^\]]*\]", " ", RED.sub(" ", lines[j])).replace("*", " ").strip(); j += 1
            after = after.strip("│ ").strip()
            if TBL.match(after): after = ""
            snip = " ".join(fold(after).split()[:7])
            spelling = re.sub(r"\s+", " ", re.sub(r"[^a-z ]", " ", m.group(0).lower())).strip()
            spelling = re.sub(r"\b(with|text|box|and|the|of|a)\b", lambda x: x.group(0), spelling)[:40]
            g = locate(gdir, snip) if snip else (None, "no text")
            c = locate(cdirs[0], snip) if (snip and cdirs) else (None, "no claude dir" if not cdirs else "no text")
            rows.append(dict(code=code, template=tpl, tag=m.group(0)[:60], spelling=spelling, text=after[:80], gold=g[1], gold_page=g[0], claude=c[1], claude_page=c[0]))
log = [f"[RHS alert] family: {len(rows)} tags / {len({r['code'] for r in rows})} modules"]
gc = collections.Counter(r["gold"] for r in rows)
found = [r for r in rows if r["gold"] not in ("absent", "no text")]
log.append("GOLD shape, all tags: " + ", ".join(f"{k} {v}" for k, v in gc.most_common()))
fc = collections.Counter(r["gold"] for r in found)
log.append(f"GOLD shape where the text is found ({len(found)} tags / {len({r['code'] for r in found})} modules): " + ", ".join(f"{k} {v} ({v/len(found):.2f})" for k, v in fc.most_common()))
log.append("CLAUDE shape now (found tags): " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r["claude"] for r in found).most_common()))
agree = sum(1 for r in found if r["gold"] == r["claude"]); log.append(f"Claude = gold on {agree} / {len(found)}")
log.append("\nby template: " + "; ".join(f"{t}: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r['gold'] for r in found if r['template'] == t).most_common(4)) for t in sorted({r['template'] for r in found})))
log.append("\nby gold shape x claude shape:")
for (g, c), n in collections.Counter((r["gold"], r["claude"]) for r in found).most_common(20): log.append(f"  {n:3d}  gold {g:20s} claude {c}")
log.append("\nexamples:")
for r in found[:30]: log.append(f"  {r['code']:9s} {r['tag'][:38]:38s} gold={r['gold']:18s} claude={r['claude']:18s} {r['text'][:50]!r}")
io.open(os.path.join(HERE, os.environ.get("OUT", "_rhsalert_measure") + ".log"), "w", encoding="utf-8", newline="").write("\n".join(log) + "\n")
json.dump(rows, io.open(os.path.join(HERE, os.environ.get("OUT", "_rhsalert_measure") + ".json"), "w", encoding="utf-8", newline=""), indent=1, ensure_ascii=False)
print("\n".join(log[:12]))
