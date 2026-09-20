#!/usr/bin/env python3
"""_s29_r7_redtitle.py — the activity opener whose TITLE is typed INSIDE the red span (session 29 Round 7 PICK candidate):
`🔴[RED TEXT] [Activity 2A] Calculating soil type. [/RED TEXT]🔴` — the words after the bracket, still red. The r66 standalone
title rule reads `blackAfter` only, so an embedded title has no path. For every such span in every WT (modules with a Claude dir):
the free text, the activity id; the GOLD: an `<h3>` equal to the free text anywhere in the module (the box title) / a `<p>` /
absent; CLAUDE: the words anywhere in the module's HTML (h3 / p / note / absent). Per template | subject.
Run under WSL from CONVERTER_V2/reference/tests:  python3 ../../outputs/_s29_r7_redtitle.py
"""
import os, re, sys, json, glob, html as H, collections
sys.path.insert(0, ".")
import _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_"); GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]

def fold(t): return re.sub(r"[^a-z0-9]+", " ", H.unescape(re.sub(r"<[^>]+>", " ", t)).lower()).strip()
SPAN = re.compile(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴", re.S)
OPEN = re.compile(r"^\s*\[\s*activity\b", re.I)

def wt_text(code):
    d = _corpus.mdir(GOLD, code)
    if not d: return None
    fs = sorted(glob.glob(os.path.join(d, "*_parsed.txt")))
    fs = [f for f in fs if not re.search(r"media list", os.path.basename(f), re.I) or re.search(r"writers template", os.path.basename(f), re.I)]
    if not fs: return None
    return open(fs[-1], encoding="utf-8", errors="replace").read()

def module_html(d):
    out = []
    for f in sorted(glob.glob(os.path.join(d, "*.html"))):
        if re.search(r"acks|acknowledge|glossary", os.path.basename(f), re.I): continue
        out.append(open(f, encoding="utf-8", errors="replace").read())
    return "\n".join(out)

def where(html_text, f):
    """how the folded phrase f appears in the html: h3 / other heading / p / li / note / else present / absent"""
    if not f: return "absent"
    for tag, lab in (("h3", "h3"), ("h[1-6]", "h#"), ("p", "p"), ("li", "li")):
        for m in re.finditer(r"<(%s)\b([^>]*)>([\s\S]*?)</\1>" % tag, html_text):
            if "cv2-note" in m.group(2): continue
            if fold(m.group(3)) == f: return lab
    if f in fold(html_text): return "elsewhere"
    return "absent"

mods = _corpus.gate_mods(CLAUDE)
rows = []
for code in mods:
    wt = wt_text(code)
    if wt is None: continue
    cd = _corpus.mdir(CLAUDE, code); gd = _corpus.mdir(GOLD, code)
    ch = gh = None
    for m in SPAN.finditer(wt):
        s = m.group(1).strip()
        if not OPEN.match(s): continue
        # free text = after the LAST closing bracket of the span
        k = s.rfind("]")
        if k < 0: continue
        free = s[k + 1:].strip()
        brackets = s[:k + 1]
        free_c = re.sub(r"\*+", "", free).strip()
        if len(free_c) < 3 or not re.search(r"[A-Za-zĀāĒēĪīŌōŪū]", free_c): continue
        if re.search(r"\[", free_c): continue
        words = free_c.split()
        if len(words) > 12: kind = "long(>12w)"
        else: kind = "title"
        idm = re.search(r"\[\s*activity[^\]]*?(\d+(?:\.\d+)?\s*[a-z]?)\s*[\]:–—-]", brackets, re.I)
        aid = idm.group(1).replace(" ", "").upper() if idm else "-"
        if ch is None: ch = module_html(cd) if cd else ""; gh = module_html(gd) if gd else ""
        f = fold(free_c)
        rows.append({"code": code, "id": aid, "bracket": brackets[:60], "free": free_c[:70], "kind": kind,
                     "gold": where(gh, f), "claude": where(ch, f),
                     "tmpl": meta.get(code, {}).get("template_type", ""), "subj": meta.get(code, {}).get("subject", "")})
print("activity openers whose title rides INSIDE the red span:", len(rows), "| modules", len({r['code'] for r in rows}))
for kind in ("title", "long(>12w)"):
    R = [r for r in rows if r["kind"] == kind]
    print("\n%s: %d sites / %d modules" % (kind, len(R), len({r['code'] for r in R})))
    print("  gold renders the words as:", dict(collections.Counter(r["gold"] for r in R).most_common()))
    print("  claude renders the words as:", dict(collections.Counter(r["claude"] for r in R).most_common()))
    print("  gold x claude:", dict(collections.Counter((r["gold"], r["claude"]) for r in R).most_common()))
    G = collections.defaultdict(collections.Counter)
    for r in R: G[(r["tmpl"], r["subj"])][(r["gold"], r["claude"])] += 1
    print("  by group (gold,claude):")
    for k, c in sorted(G.items(), key=lambda x: -sum(x[1].values())):
        print("    %-13s %-26s n=%3d  %s" % (k[0], k[1][:26], sum(c.values()), dict(c.most_common(4))))
    print("  examples:")
    for r in R[:14]: print("    %s %s %s | «%s» → gold %s / claude %s" % (r["code"], r["id"], r["bracket"], r["free"], r["gold"], r["claude"]))
json.dump(rows, open(os.path.join(HERE, "_s29_r7_redtitle.json"), "w", encoding="utf-8"), indent=1)
