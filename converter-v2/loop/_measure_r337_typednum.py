#!/usr/bin/env python3
"""ROUND 337 PICK probe (loop session 6) — KB constraint 42: typed `<p>1. …</p>` numbering in Claude vs the gold's semantic <ol>.
Every Claude body <p> (outside cv2 dumps / notes / acks) whose text opens with `N.` or `N)`; grouped into RUNS of consecutive
numbered paragraphs; for each numbered paragraph the gold's element holding the same text (li / p / other / absent) and, when the
gold holds it as <li>, whether the gold's <li> text still carries the typed number. Also whether the run sits inside an activity box.
Writes _r337_typednum.json next to itself; prints the summary. Run from anywhere."""
import re, glob, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
NUM = re.compile(r'^\s*(\d{1,2})\s*[.)]\s+(\S.*)$', re.S)
def fold(t): return re.sub(r'[^a-z0-9]+', ' ', re.sub(r'<[^>]+>', '', t).lower()).strip()
def body(s):
    s = s.split('<div id="body"', 1)[-1]; s = re.sub(r'<div class="acks[\s\S]*', '', s)
    s = re.sub(r'<div class="cv2-interactive[\s\S]*?</div>\s*</div>\s*</div>', '<CV2/>', s)
    s = re.sub(r'<p class="cv2-(?:note|comment)"[^>]*>[\s\S]*?</p>', '', s); return s
DIV = re.compile(r'<div\b|</div>'); OPEN = re.compile(r'<div class="activity[^"]*"[^>]*>')
def spans(s):
    out = []
    for m in OPEN.finditer(s):
        d = 1
        for x in DIV.finditer(s, m.end()):
            d += 1 if x.group(0) == "<div" else -1
            if d == 0: out.append((m.start(), x.start())); break
    return out
stats = collections.Counter(); per_tmpl = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set); mods = collections.defaultdict(set)
gold_form = collections.Counter(); runs_hist = collections.Counter(); examples = []
for f in sorted(glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", "*", "*.html"))):
    tmpl = os.path.basename(os.path.dirname(os.path.dirname(f))); code = os.path.basename(os.path.dirname(f))
    s = body(open(f, encoding="utf-8", errors="replace").read()); sp = spans(s)
    # paragraphs in document order with positions
    paras = [(m.start(), m.group(1)) for m in re.finditer(r'<p(?:\s[^>]*)?>(.*?)</p>', s, re.S)]
    nums = [(pos, NUM.match(re.sub(r'<[^>]+>', '', t))) for pos, t in paras]
    # runs: consecutive paragraphs (by index) that are numbered
    run = []; runs = []
    for i, (pos, m) in enumerate(nums):
        if m: run.append((pos, m))
        else:
            if len(run) >= 2: runs.append(run)
            run = []
    if len(run) >= 2: runs.append(run)
    if not runs: continue
    gfiles = [g for g in glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", tmpl, code, "*.html")) if not re.search(r"acks|ackn", g, re.I)]
    G = " ".join(open(g, encoding="utf-8", errors="replace").read() for g in gfiles)
    gmap = {}
    # every gold li/p/... with (tag, list-kind, typed-number-in-text) keyed by its text with the typed number removed
    for mm in re.finditer(r'<(li|p|td|th|h[1-6])(?:\s[^>]*)?>(.*?)</\1>', G, re.S | re.I):
        raw = re.sub(r'<[^>]+>', '', mm.group(2)); numbered = bool(NUM.match(raw))
        kind = ""
        if mm.group(1).lower() == "li":
            pre = G[max(0, mm.start() - 4000):mm.start()]; o = pre.rfind("<ol"); u = pre.rfind("<ul"); kind = "ol" if o > u else "ul"
            if kind == "ol" and re.search(r'<ol[^>]*start=', pre[o:o + 60]): kind = "ol-start"
        gmap.setdefault(fold(re.sub(r'^\s*\d{1,2}\s*[.)]\s*', '', raw)), (mm.group(1).lower(), kind, numbered))
    for r in runs:
        runs_hist[min(len(r), 8)] += 1; inbox = any(a < r[0][0] < b for a, b in sp)
        stats["runs"] += 1; stats["runs_inbox" if inbox else "runs_outside"] += 1; per_tmpl[tmpl]["runs"] += 1
        pages[tmpl].add(f); mods[tmpl].add(code)
        for pos, m in r:
            stats["paras"] += 1
            k_full = fold(m.group(0)); k_text = fold(m.group(2))
            g = gmap.get(k_text)
            if g is None: gold_form["absent"] += 1
            else:
                tag, kind, numbered = g
                gold_form[(tag + ("/" + kind if kind else "")) + (" +typed number" if numbered else "")] += 1
        if len(examples) < 12: examples.append((code, os.path.basename(f), len(r), "inbox" if inbox else "outside", r[0][1].group(0)[:60].replace("\n", " ")))
print("runs", stats["runs"], "(inbox", stats["runs_inbox"], "/ outside", stats["runs_outside"], ") numbered paragraphs", stats["paras"])
print("run length histogram", dict(sorted(runs_hist.items())))
print("gold form of the same text:", dict(gold_form.most_common()))
for t in per_tmpl: print(f"  {t:12} runs {per_tmpl[t]['runs']} pages {len(pages[t])} modules {len(mods[t])}")
print("TOTAL pages", sum(len(v) for v in pages.values()), "modules", len(set().union(*mods.values())) if mods else 0)
for e in examples: print("  ", e)
json.dump({"stats": dict(stats), "gold_form": dict(gold_form), "pages": {t: sorted(os.path.relpath(p, ROOT) for p in v) for t, v in pages.items()}, "modules": {t: sorted(v) for t, v in mods.items()}}, open(os.path.join(HERE, "_r337_typednum.json"), "w", encoding="utf-8"), indent=1)
