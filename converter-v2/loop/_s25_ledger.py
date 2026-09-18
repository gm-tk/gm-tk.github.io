#!/usr/bin/env python3
"""Session 25 — THE LOSS LEDGER: every lost percentage point of the skeleton SCAFFOLD mean attributed to a FAMILY, so the
honest remaining headroom is one table. For every unmatched skeleton line (the gate's own difflib alignment, weight
1 / (|gold| + |Claude|) per page):
  chrome            — module-code / title / header / module-menu / crumbs / phases-nav / footer / acks / root
  widget-line       — a collapsed WIDGET marker on either side (the D10-3 build gap + the human's substitutions, A1)
  editorial-gold    — a gold text line whose text is NOWHERE on Claude's page (the human's own additions — the ceiling)
  editorial-claude  — a Claude text line whose text is NOWHERE on the gold page (writer text the human dropped / rewrote)
  container-shift   — the text exists on the other page but in another container (activity ↔ free ↔ widget ↔ alert)
  merged-split      — the text is part of a longer element / reworded on the other page
  alignment-residue — the same pad+signature line is unmatched on BOTH sides of the page (order / alignment, not form)
  wrapper           — a structure-only line (row / col / ul / table …) with no twin on the other side
  tag-swap          — the text exists on the other page in the same container with another tag (h ↔ p, ul ↔ ol …)
Per template. Also the residual-only view (everything but chrome / widget / editorial).
  python3 _s25_ledger.py [prefix-filter]"""
import os, sys, re, difflib
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
    """family for one unmatched line"""
    if ln.region in CHROME: return "chrome"
    if ln.sig == "WIDGET": return "widget-line"
    key = ln.pad + ln.sig
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
    # structure-only line
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
detail = defaultdict(lambda: defaultdict(float)); formdetail = defaultdict(lambda: defaultdict(float)); emptydetail = defaultdict(lambda: defaultdict(float))
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        gs = [l.pad + l.sig for l in g]; cs = [l.pad + l.sig for l in c]
        gc = containers(g); cc = containers(c)
        w = 1.0 / max(len(gs) + len(cs), 1)
        sm = difflib.SequenceMatcher(None, gs, cs, autojunk=False)
        keys = ("ALL", f"template={tf}")
        for k in keys: N[k] += 1
        ug = []; uc = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal": continue
            ug += list(range(i1, i2)); uc += list(range(j1, j2))
        if not ug and not uc: continue
        gel = elements(hp); cel = elements(cp)
        # structure-only twin pools (pad+sig) of the unmatched lines, per side
        pool_g = Counter(gs[i] for i in ug if not (g[i].text and tag_of(g[i].sig) in TEXT_TAGS))
        pool_c = Counter(cs[j] for j in uc if not (c[j].text and tag_of(c[j].sig) in TEXT_TAGS))
        def attribute(lines, unmatched, conts, other, pool, side, path, direction):
            fams = {}
            for i in unmatched:
                fams[i] = classify(lines[i], conts[i], other, pool, side)
            uset = set(unmatched)
            # a wrapper takes the majority family of the UNMATCHED text lines it wraps; a wrapper whose wrapped text all
            # MATCHED (or that wraps nothing) is a wrapper-form difference — the structural residue the converter owns
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
                    fams[i] = "wrapper-empty"        # wraps no text at all (an empty row / col, a bare br / img wrapper)
                elif n_text_unmatched == 0:
                    fams[i] = "wrapper-form"         # its content matched, only the wrapper's form / level differs
                else:
                    fams[i] = "wrapper-of-alignment-residue"
            for i in unmatched:
                f = fams[i]
                for k in keys:
                    loss[k][f] += w; pagesets[k][f].add(path); detail[k][(f, direction, lines[i].region, tag_of(lines[i].sig))] += w
                    if f == "wrapper-form": formdetail[k][(direction, lines[i].region, conts[i], lines[i].sig)] += w
                    if f == "wrapper-empty": emptydetail[k][(direction, lines[i].region, conts[i], lines[i].sig)] += w
        attribute(g, ug, gc, cel, pool_c, "gold", hp, "MISSING")
        attribute(c, uc, cc, gel, pool_g, "claude", cp, "EXTRA")

for k in ("ALL", "template=Standard", "template=Inquiry", "template=Fundamentals", "template=Bilingual"):
    if not N[k]: continue
    n = N[k]; L = loss[k]; tot = sum(L.values()) / n * 100
    print(f"\n== {k} — pages {n}: total loss {tot:.2f}pp")
    for f, v in sorted(L.items(), key=lambda kv: -kv[1]):
        print(f"   {v/n*100:6.2f}pp  pages {len(pagesets[k][f]):5d}   {f}")
    resid = sum(v for f, v in L.items() if not (f == "chrome" or f == "widget-line" or f.startswith("editorial")))
    print(f"   → residual (not chrome / widget / editorial): {resid/n*100:.2f}pp")
    print("   top detail rows (family · direction · region · tag):")
    for key, v in sorted(detail[k].items(), key=lambda kv: -kv[1])[:24]:
        print(f"     {v/n*100:6.2f}pp  {key}")
    print("   wrapper-form detail (direction · region · container · signature):")
    for key, v in sorted(formdetail[k].items(), key=lambda kv: -kv[1])[:30]:
        print(f"     {v/n*100:6.2f}pp  {key}")
    print("   wrapper-empty detail (direction · region · container · signature):")
    for key, v in sorted(emptydetail[k].items(), key=lambda kv: -kv[1])[:30]:
        print(f"     {v/n*100:6.2f}pp  {key}")
