#!/usr/bin/env python3
"""_s29_r7_boxtitle.py — DIFF_QUEUE #585 decomposed (activity MISSING h3, 384 pages / 190 modules): for every GOLD numbered
activity box whose FIRST visible element is an <h3> (the box title) on a paired page, where is that title in CLAUDE?
  claude box (same number) exists → h3 same text (MATCH) / a p with the text / the text elsewhere in the box / box has ANOTHER h3 /
  box without the text ; no same-number box → the text as a free h#/p on the page / inside a cv2 dump / absent from the page.
Plus the WT source of the title: a [H*] line, the opener's black tail, the opener's red span (embedded), a bare black line, absent.
Per template | subject. Run under WSL from CONVERTER_V2/reference/tests:  python3 ../../outputs/_s29_r7_boxtitle.py
"""
import os, re, sys, json, glob, html as H, collections
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_"); GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]

def fold(t): return re.sub(r"[^a-z0-9]+", " ", H.unescape(re.sub(r"<[^>]+>", " ", t)).lower()).strip()

def boxes(html):
    out = []; stack = []
    for m in re.finditer(r"<(/?)div\b([^>]*)>", html):
        if m.group(1):
            if stack:
                st = stack.pop()
                if st[1] is not None: out.append((st[1], st[0], html[st[2]:m.start()]))
        else:
            if m.group(2).rstrip().endswith("/"): continue
            cls = re.search(r'class="([^"]*)"', m.group(2)); c = cls.group(1) if cls else ""
            num = re.search(r'number="([^"]*)"', m.group(2))
            isact = bool(re.search(r"(^|\s)activity(\s|$)", c)) and "cv2" not in c
            stack.append((c, (num.group(1).upper() if num else "-") if isact else None, m.end()))
    return out

def first_el(inner):
    """(tag, text) of the first visible element inside a box (skipping wrapper divs / cv2 notes / comments)"""
    s = re.sub(r"<!--[\s\S]*?-->", " ", inner)
    for m in re.finditer(r"<(h[1-6]|p|ul|ol|table|img|iframe|div|a|span)\b([^>]*)>", s):
        tag = m.group(1)
        if tag == "div": continue
        if "cv2-note" in m.group(2) or "cv2-comment" in m.group(2): continue
        if tag in ("img", "iframe"): return tag, ""
        e = s.find("</%s>" % tag, m.end())
        return tag, fold(s[m.end():e if e > 0 else m.end() + 400])
    return "", ""

wt_cache = {}
def wt_lines(code):
    if code in wt_cache: return wt_cache[code]
    d = _corpus.mdir(GOLD, code); lines = []
    for f in sorted(glob.glob(os.path.join(d, "*_parsed.txt"))):
        if re.search(r"media list", os.path.basename(f), re.I) and not re.search(r"writers template", os.path.basename(f), re.I): continue
        lines += open(f, encoding="utf-8", errors="replace").read().split("\n")
    wt_cache[code] = lines; return lines

def wt_source(code, f):
    """how the title text f appears in the WT"""
    if not f: return "absent"
    best = "absent"
    for ln in wt_lines(code):
        fl = fold(ln)
        if f not in fl: continue
        raw = ln.strip()
        red = "🔴[RED TEXT]" in raw
        # strip red markers for the shape tests
        body = re.sub(r"🔴\[/?RED TEXT\]🔴", "", raw).strip()
        if re.match(r"^\s*\[\s*h[1-6]\s*\]", body, re.I): return "[H#] line"
        if re.search(r"\[\s*activity[^\]]*\]", body, re.I):
            # opener line: is the title inside the red span or black after it?
            spans = re.findall(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴", raw, re.S)
            inred = any(f in fold(sp) for sp in spans)
            return "opener red-embedded" if inred else "opener black tail"
        if re.match(r"^\s*\[", body): best = "other [tag] line"
        elif fl == f: best = "bare black line" if best == "absent" else best
        elif best == "absent": best = "inside a longer line"
    return best

mods = _corpus.gate_mods(CLAUDE)
rows = []
for code in mods:
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); g = (mm.get("template_type", ""), mm.get("subject", ""))
    for t in prs:
        cp, hp = t[1], t[2]
        try: c = open(cp, encoding="utf-8").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        cb = {}
        for n, cl, inner in boxes(c):
            cb.setdefault(n, []).append(inner)
        cfold = fold(c)
        for num, cl, inner in boxes(gh):
            tag, txt = first_el(inner)
            if tag != "h3" or not txt or num == "-": continue
            f = txt
            if num in cb:
                found = "box: no title text"
                for ci in cb[num]:
                    ft, ftxt = first_el(ci)
                    cf = fold(ci)
                    if ft == "h3" and ftxt == f: found = "MATCH (h3 first)"; break
                    if re.search(r"<h3\b[^>]*>%s</h3>" % re.escape(f), fold(re.sub(r"<(/?)h3\b[^>]*>", r"<\1h3>", ci)) if False else "", re.I): pass
                    if ft == "h3" and ftxt != f: found = "box: ANOTHER h3 first"
                    elif ft == "p" and ftxt == f: found = "box: title as p"
                    elif f in cf: found = "box: text inside (not first)" if found == "box: no title text" else found
                    if found.startswith("MATCH"): break
            else:
                if f in cfold:
                    # free on the page?
                    m = re.search(r"<(h[1-6]|p)\b[^>]*>([^<]*)</\1>", c)
                    hit = None
                    for m in re.finditer(r"<(h[1-6]|p)\b([^>]*)>([\s\S]*?)</\1>", c):
                        if "cv2-" in m.group(2): continue
                        if fold(m.group(3)) == f: hit = m.group(1); break
                    found = ("no box: free " + hit) if hit else ("no box: in a cv2 dump" if re.search(r"cv2-interactive[\s\S]{0,4000}" + re.escape(txt[:20]), fold(c)) else "no box: text elsewhere")
                else:
                    found = "no box: absent from page"
            rows.append({"code": code, "page": os.path.basename(cp), "num": num, "title": txt[:60], "claude": found, "wt": wt_source(code, f), "tmpl": g[0], "subj": g[1]})

print("GOLD numbered activity boxes opening with an <h3> title on paired pages:", len(rows), "| pages", len({(r['code'], r['page']) for r in rows}), "| modules", len({r['code'] for r in rows}))
C = collections.Counter(r["claude"] for r in rows)
print("\nCLAUDE renders the title as:")
for k, v in C.most_common(): print("  %4d  %s" % (v, k))
print("\nWT source of the title (all):", dict(collections.Counter(r["wt"] for r in rows).most_common()))
NM = [r for r in rows if not r["claude"].startswith("MATCH")]
print("\nNON-MATCH %d — WT source x Claude rendering:" % len(NM))
X = collections.Counter((r["wt"], r["claude"]) for r in NM)
for k, v in X.most_common(30): print("  %4d  %-24s → %s" % (v, k[0], k[1]))
print("\nNON-MATCH by group (top Claude renderings):")
G = collections.defaultdict(collections.Counter)
for r in NM: G[(r["tmpl"], r["subj"])][r["claude"]] += 1
for k, c in sorted(G.items(), key=lambda x: -sum(x[1].values()))[:16]:
    tot = sum(1 for r in rows if (r["tmpl"], r["subj"]) == k)
    print("  %-13s %-26s non-match %3d / %3d  %s" % (k[0], k[1][:26], sum(c.values()), tot, dict(c.most_common(3))))
print("\nexamples per (wt, claude) class:")
seen = collections.Counter()
for r in NM:
    k = (r["wt"], r["claude"])
    if seen[k] >= 3: continue
    seen[k] += 1
    print("  [%s → %s] %s %s «%s»" % (k[0], k[1], r["page"], r["num"], r["title"]))
json.dump(rows, open(os.path.join(HERE, "_s29_r7_boxtitle.json"), "w", encoding="utf-8"), indent=1)
