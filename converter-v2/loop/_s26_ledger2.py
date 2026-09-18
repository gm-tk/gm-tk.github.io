#!/usr/bin/env python3
"""Session 26 — THE SCORE-BAND LEDGER + THE CHROME SPLIT (a new angle on the s25 loss ledger).

Two questions the s25 ledger could not answer:
  (1) On the NEAR-MISS pages (the gate's own scaffold ≥ 0.75, and the 0.60–0.75 band) — where everything else is right —
      what is still unmatched?  A family that repeats there is the cleanest signal of a mechanical, derivable class,
      because editorial noise is by definition low on those pages.
  (2) The 5.74pp "chrome" family — split by (direction · region · signature) with the MODULE count, so every
      chrome cell can be checked against the recorded overrides (D10-9 h5, 01B lesson menu, the zero-padded chip,
      the r360 footer sets, the r317 acks form) and anything NOT covered is named.

The classification code is the s25 ledger's, unchanged (the gate's own difflib alignment, weight 1/(|gold|+|Claude|)).
Per-page scores: outputs/_s24_r386_sk_final.json (the current baseline).
  python3 _s26_ledger2.py [prefix-filter]"""
import os, sys, re, json, difflib
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
import _corpus
from _diff_miner import page_lines, unorm, TextTree, _cls, node_text
import _structural_skeleton
from _structural_skeleton import WIDGET_MARKERS
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
flt = args[0] if args else ""
CHROME = {"module-code", "title", "header", "module-menu", "crumbs", "phases-nav", "footer", "acks", "root"}
TEXT_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "b", "strong", "a", "span", "label", "caption", "figcaption", "button", "i", "em")

SCORES = {}
for pg in json.load(open(os.path.join(OUTPUTS, "_s24_r386_sk_final.json")))["per_page"]:
    SCORES[pg["page"]] = pg["scaffold"]

def band(s):
    if s is None: return "band=unscored"
    if s >= 0.90: return "band=90+"
    if s >= 0.75: return "band=75-90"
    if s >= 0.60: return "band=60-75"
    if s >= 0.40: return "band=40-60"
    return "band=<40"

def fold(t):
    return re.sub(r"[^a-z0-9]+", " ", unorm(t or "").lower()).strip()

def containers(lines):
    out = []; stack = []
    for ln in lines:
        d = ln.depth
        while stack and stack[-1][0] >= d: stack.pop()
        cont = next((s[1] for s in reversed(stack) if s[1]), None) or "free"
        out.append(cont)
        s = ln.sig
        k = "activity" if s.startswith("div.activity") else "alert" if s.startswith("div.alert") else "panel" if ("Panel" in s or s.startswith("div.introduction")) else None
        stack.append((d, k))
    return out

def elements(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    src = _structural_skeleton.body_source(raw)
    tb = TextTree(); tb.feed(src)
    exact = defaultdict(list); longs = []
    def walk(n, cont):
        c = _cls(n); cont2 = cont
        if n.attrs.get("id") in ("header", "module-menu-content", "footer") or (c & {"acks", "acksTemplate"}): cont2 = "header"
        elif cont in ("free", "alert", "activity"):
            if c & WIDGET_MARKERS: cont2 = "widget"
            elif any(t.startswith("activity") for t in c): cont2 = "activity"
            elif any(t.startswith("alert") for t in c) and cont == "free": cont2 = "alert"
        if n.tag in TEXT_TAGS:
            t = node_text(n)
            if t:
                ft = fold(t); exact[ft].append((n.tag, cont2))
                if len(ft) >= 25: longs.append((ft, n.tag, cont2))
        for k in n.kids: walk(k, cont2)
    body = next((k for k in tb.root.kids if k.tag == "body"), None)
    walk(body if body is not None else tb.root, "free")
    return exact, longs

def tag_of(sig):
    m = re.match(r"([a-z0-9]+)", sig); return m.group(1) if m else sig

def classify(ln, cont, other, other_unmatched_sigs, side):
    key = ln.pad + ln.sig
    if ln.region in CHROME:
        # a chrome line whose exact pad+signature is ALSO unmatched on the other side is an alignment casualty
        # (difflib lost the block because a neighbour differs), not a form difference — split it out
        if other_unmatched_sigs.get(key, 0) > 0:
            other_unmatched_sigs[key] -= 1
            return "chrome-aligned"
        return "chrome"
    if ln.sig == "WIDGET": return "widget-line"
    txt = fold(ln.text) if ln.text else ""
    tag = tag_of(ln.sig)
    if txt and tag in TEXT_TAGS:
        exact, longs = other
        hits = exact.get(txt)
        if hits:
            same_cont = [h for h in hits if h[1] == cont]
            if same_cont:
                return "alignment-residue" if any(h[0] == tag for h in same_cont) else "tag-swap"
            oc = hits[0][1]
            return f"container-shift:{cont}->{oc}"
        if len(txt) >= 15:
            for ft, t2, c2 in longs:
                if txt in ft: return "merged-split"
            w = txt.split()
            if len(w) >= 6:
                head = " ".join(w[:5])
                for ft, t2, c2 in longs:
                    if head in ft: return "merged-split"
        return "editorial-" + side
    if other_unmatched_sigs.get(key, 0) > 0:
        other_unmatched_sigs[key] -= 1
        return "alignment-residue"
    return "wrapper"

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
loss = defaultdict(lambda: defaultdict(float)); N = Counter(); pagesets = defaultdict(lambda: defaultdict(set))
detail = defaultdict(lambda: defaultdict(float)); detailpages = defaultdict(lambda: defaultdict(set)); detailmods = defaultdict(lambda: defaultdict(set))
chrome = defaultdict(lambda: defaultdict(float)); chromepages = defaultdict(lambda: defaultdict(set)); chromemods = defaultdict(lambda: defaultdict(set))
chrome_ex = defaultdict(lambda: defaultdict(list))
region = defaultdict(lambda: defaultdict(float))
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        sc = SCORES.get(os.path.basename(cp))
        gs = [l.pad + l.sig for l in g]; cs = [l.pad + l.sig for l in c]
        gc = containers(g); cc = containers(c)
        w = 1.0 / max(len(gs) + len(cs), 1)
        sm = difflib.SequenceMatcher(None, gs, cs, autojunk=False)
        keys = ("ALL", band(sc), f"template={tf}")
        for k in keys: N[k] += 1
        ug = []; uc = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal": continue
            ug += list(range(i1, i2)); uc += list(range(j1, j2))
        if not ug and not uc: continue
        gel = elements(hp); cel = elements(cp)
        pool_g = Counter(gs[i] for i in ug if g[i].region in CHROME or not (g[i].text and tag_of(g[i].sig) in TEXT_TAGS))
        pool_c = Counter(cs[j] for j in uc if c[j].region in CHROME or not (c[j].text and tag_of(c[j].sig) in TEXT_TAGS))
        def attribute(lines, unmatched, conts, other, pool, side, path, direction):
            fams = {}
            for i in unmatched:
                fams[i] = classify(lines[i], conts[i], other, pool, side)
            uset = set(unmatched)
            for i in unmatched:
                if fams[i] != "wrapper": continue
                d = lines[i].depth; j = i + 1; sub = Counter(); n_text = 0; n_text_unmatched = 0
                while j < len(lines) and lines[j].depth > d:
                    if lines[j].text and tag_of(lines[j].sig) in TEXT_TAGS:
                        n_text += 1
                        if j in uset:
                            n_text_unmatched += 1
                            fj = fams.get(j, "wrapper")
                            if fj != "wrapper": sub[fj.split(":")[0] if fj.startswith("container-shift") else fj] += 1
                    elif lines[j].sig == "WIDGET":
                        n_text += 1
                        if j in uset: n_text_unmatched += 1; sub["widget-line"] += 1
                    j += 1
                if sub:
                    fams[i] = "wrapper-of-" + sub.most_common(1)[0][0]
                elif n_text == 0:
                    fams[i] = "wrapper-empty"
                elif n_text_unmatched == 0:
                    fams[i] = "wrapper-form"
                else:
                    fams[i] = "wrapper-of-alignment-residue"
            for i in unmatched:
                f = fams[i]
                ln = lines[i]
                dk = (f, direction, ln.region, conts[i], ln.sig)
                for k in keys:
                    loss[k][f] += w; pagesets[k][f].add(path)
                    detail[k][dk] += w; detailpages[k][dk].add(path); detailmods[k][dk].add(code)
                    region[k][(ln.region, direction)] += w
                    if f in ("chrome", "chrome-aligned"):
                        ck = (direction, ln.region, ln.sig)
                        chrome[k][ck] += w; chromepages[k][ck].add(path); chromemods[k][ck].add(code)
                        if len(chrome_ex[k][ck]) < 3 and (ln.text or "").strip():
                            chrome_ex[k][ck].append((code, (ln.text or "")[:60]))
        attribute(g, ug, gc, cel, pool_c, "gold", hp, "MISSING")
        attribute(c, uc, cc, gel, pool_g, "claude", cp, "EXTRA")

ORDER = ["ALL", "band=90+", "band=75-90", "band=60-75", "band=40-60", "band=<40", "template=Standard", "template=Inquiry", "template=Fundamentals", "template=Bilingual"]
for k in ORDER:
    if not N[k]: continue
    n = N[k]; L = loss[k]; tot = sum(L.values()) / n * 100
    print(f"\n== {k} — pages {n}: total loss {tot:.2f}pp (mean score ≈ {100-tot:.1f})")
    for f, v in sorted(L.items(), key=lambda kv: -kv[1])[:16]:
        print(f"   {v/n*100:6.2f}pp  pages {len(pagesets[k][f]):5d}   {f}")
    print("   by REGION (region · direction):")
    for key, v in sorted(region[k].items(), key=lambda kv: -kv[1])[:14]:
        print(f"     {v/n*100:6.2f}pp  {key}")
    print("   top detail rows (family · direction · region · container · signature) — pp · pages · modules:")
    for key, v in sorted(detail[k].items(), key=lambda kv: -kv[1])[:40]:
        print(f"     {v/n*100:6.2f}pp  p={len(detailpages[k][key]):4d} m={len(detailmods[k][key]):3d}  {key}")
    if k in ("ALL", "template=Standard", "template=Inquiry", "template=Fundamentals", "template=Bilingual", "band=75-90", "band=60-75"):
        print("   CHROME split (direction · region · signature) — pp · pages · modules · examples:")
        for key, v in sorted(chrome[k].items(), key=lambda kv: -kv[1])[:40]:
            ex = "; ".join(f"{c}:{t}" for c, t in chrome_ex[k][key][:2])
            print(f"     {v/n*100:6.2f}pp  p={len(chromepages[k][key]):4d} m={len(chromemods[k][key]):3d}  {key}  {ex}")
