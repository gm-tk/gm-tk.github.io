#!/usr/bin/env python3
"""THE DIFF MINER — LOOP__Autonomous_Rounds.md §1d (Round 0c, session 19, 17 September 2026).

WHY: sessions 15–18 each declared "exhaustion" on the r356 corpus, and Chris then opened ONE
module (BLL110) and found six derivable structural differences on its overview page alone.
Nothing had ever read the per-page structural diffs the PRIMARY gate's score is computed
from. This tool does exactly that, corpus-wide, and turns them into a ranked class queue.

WHAT IT DOES
  1. For every paired page (the skeleton gate's OWN pairing — _discrepancy_audit.pairs, the
     acks / glossary / references filter of _skeleton_compare — and its OWN population,
     _corpus.gate_mods), build the gold and Claude SCAFFOLD skeletons with the same tree,
     labels, widget collapse and note skip as _structural_skeleton.py, but keep every element
     as its own line (the gate's "N× repeated" collapse is a scoring convenience — a mined
     line must be quotable) with its TEXT and its REGION alongside the `tag#id.class` line.
  2. difflib-align the two signature sequences exactly as the gate does (autojunk=False) and
     tag every differing line: template family / Legacy-vs-Refresh / subject / series;
     REGION (module-code, title, module-menu, crumbs, phases-nav, body, activity, footer,
     acks); ELEMENT ROLE (parent > role; a lone inline wrapper folds into its parent, so the
     gold's `h4>span` vs Claude's `h5` is ONE class); DIRECTION — MISSING / EXTRA /
     SUBSTITUTED / MOVED; DERIVABLE-CONTENT — the gold line's text is in the module's parsed
     Writers Template under the round-110 tolerance (anchor_compare._phrase_present via
     _measure_ceiling.has_source); a structure-only difference is always derivable.
  3. Aggregate into CLASSES keyed by (region, parent, gold role, Claude role, direction) with
     pages, modules, the per-template / per-subject counts, the GOLD CONSENSUS per group (of
     gold pages where the region exists, the share carrying the gold form; for an EXTRA class
     the share NOT carrying Claude's form), the derivable share, the nearest KB lines, the
     §1b authority, and three example modules with the WT / gold / Claude lines quoted.
  4. The COMPLETENESS CENSUS for the repeating chrome (module menu, crumbs, phases nav,
     footer): the gold's text-bearing items whose text is in the WT vs what Claude rendered.
  5. Write outputs/_diff_miner.json and DIFF_QUEUE.md (folder root): chrome regions first
     (module-code → title → module-menu → crumbs / phases-nav → footer → acks → activity →
     body), then by modules affected. Candidate rule: modules ≥ 10 for a chrome class, pages
     ≥ 20 for a body / activity class, gold consensus ≥ 0.60 in at least one template or
     subject group THAT ITSELF REACHES THE FLOOR, and structure-only or derivable ≥ 0.60.
     Every class below the floor is still listed with its numbers.

USAGE (paths are dynamic — run from anywhere, under WSL like every other gate tool):
  python3 _diff_miner.py                     # full population → outputs/_diff_miner.json + DIFF_QUEUE.md
  python3 _diff_miner.py CODE [CODE …]       # scoped (writes _diff_miner_scoped.* unless --json / --md)
  python3 _diff_miner.py --json OUT --md OUT
  python3 _diff_miner.py --selftest          # LIVENESS + DETECTION (the r149 discipline)
"""
import os, sys, re, json, time, difflib, subprocess
from collections import defaultdict, Counter
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(BASE, "..", "..", ".."))
OUTPUTS = os.path.join(ROOT, "CONVERTER_V2", "outputs")
KB = os.path.join(ROOT, "00-Other-TK-Resources", "htmlconvertor-kb")
# reference/tests FIRST: outputs/ holds an OLD copy of _corpus.py (no gate_mods) that would shadow the gate's
for p in (OUTPUTS, BASE):
    if p in sys.path:
        sys.path.remove(p)
    sys.path.insert(0, p)
import _corpus
from _structural_skeleton import label, WIDGET_MARKERS, VOID, DROP
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import wt_blob, has_source, unorm, load_meta, kb_family

SKIP_PAGE = re.compile(r"acks|acknowledge|glossary|references", re.I)
NOTE_CLS = {"cv2-comment", "cv2-note"}
INLINE = {"span", "b", "i", "strong", "em", "u", "small", "sub", "sup", "a", "mark"}
TEXT_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "a", "span", "b", "i", "strong",
             "em", "u", "small", "caption", "figcaption", "label", "dt", "dd", "blockquote", "pre",
             "button", "summary", "legend", "div"}
CHROME = {"module-code": 0, "title": 1, "header": 1.5, "module-menu": 2, "crumbs": 3, "phases-nav": 3,
          "footer": 4, "acks": 5}
REGION_ORDER = dict(CHROME, activity=6, body=7, root=8)
CHROME_FLOOR_MODULES = 10
BODY_FLOOR_PAGES = 20
CONSENSUS_MIN = 0.60
DERIVABLE_MIN = 0.60
CENSUS_REGIONS = ("module-menu", "crumbs", "phases-nav", "footer")
# the region whose gold pages form a class's consensus DENOMINATOR (a page without the chip has no
# module-code region at all — the honest denominator is every page with a header)
DENOM_REGION = {"module-code": "header", "title": "header", "module-menu": "header", "header": "header",
                "crumbs": "body", "phases-nav": "body", "activity": "body", "body": "body",
                "footer": "root", "acks": "root", "root": "root"}
# a MISSING line in these regions carries no writer text (the module code, the nav links) — structure-only
STRUCTURE_REGIONS = {"module-code", "footer"}
GENERIC_TOKENS = {"div", "row", "col-12", "col-md-8", "p", "span", "ul", "li", "h1", "h2", "h3", "img",
                  "img-fluid", "b", "i", "a", "col-md-4", "col", "container-fluid"}
_WS = re.compile(r"\s+")


# ------------------------------------------------------------------------------------------------ tree + lines
class TNode:
    __slots__ = ("tag", "attrs", "kids", "own", "parent")

    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.kids, self.own, self.parent = tag, attrs, [], [], parent


class TextTree(HTMLParser):
    """_structural_skeleton.TreeBuilder with text kept (void-aware — CLAUDE.md §16 r315)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = TNode("#root", {})
        self.stack = [self.root]
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if self.skip_depth:
            if tag not in VOID:
                self.skip_depth += 1
            return
        if tag in DROP:
            if tag not in VOID:
                self.skip_depth = 1
            return
        n = TNode(tag, dict(attrs), self.stack[-1])
        self.stack[-1].kids.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        if self.skip_depth or tag in DROP:
            return
        self.stack[-1].kids.append(TNode(tag, dict(attrs), self.stack[-1]))

    def handle_endtag(self, tag):
        if self.skip_depth:
            self.skip_depth -= 1
            return
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not self.skip_depth and data and not data.isspace():
            self.stack[-1].own.append(data)


def _cls(n):
    return set((n.attrs.get("class") or "").split())


def _full_text(n, cap=400):
    parts = []

    def walk(x):
        if sum(len(p) for p in parts) > cap:
            return
        parts.extend(x.own)
        for k in x.kids:
            if not (_cls(k) & NOTE_CLS):
                walk(k)
    walk(n)
    return _WS.sub(" ", " ".join(parts)).strip()[:cap]


def node_text(n):
    own = _WS.sub(" ", " ".join(n.own)).strip()
    if own:
        return own[:400]
    if n.tag in TEXT_TAGS and n.tag != "div":
        return _full_text(n)
    return ""


_NUMVAL = re.compile(r"\[number=[^\]]*\]")


def role(n):
    """The element's label plus a lone inline wrapper's label — `h4>span`, `p>b`.
    Session 22: the `number=` VALUE is folded to `[number=*]` in the class ROLE (the diff itself still
    compares the full signature, so a differing number is still a differing line) — keyed by value, the
    activity-number class fragmented into one row per number and never reached the floor; folded, it is
    one row (`div.activity…[number=*]` SUBSTITUTED), measured and DECLINED in session 22 (r369)."""
    r = _NUMVAL.sub("[number=*]", label(n))
    kids = [k for k in n.kids if not (_cls(k) & NOTE_CLS)]
    if len(kids) == 1 and kids[0].tag in INLINE:
        r += ">" + label(kids[0])
    return r


def region_of(n, parent_region):
    eid = n.attrs.get("id") or ""
    cls = _cls(n)
    if eid in ("header", "module-head"):
        return "header"
    if eid in ("body", "container"):
        return "body"
    if eid in ("footer", "module-foot"):
        return "footer"
    if parent_region == "header":
        if eid == "module-code":
            return "module-code"
        if n.tag == "h1":
            return "title"
        if eid in ("module-head-buttons", "module-menu-content", "module-menu-button"):
            return "module-menu"
        return "header"
    if "acks" in cls or "acksLesson" in cls:
        return "acks"
    if parent_region in ("body", "root", None):
        if "crumbs" in cls:
            return "crumbs"
        if "phases" in cls:
            return "phases-nav"
    if "activity" in cls and parent_region in ("body", "root", None, "activity"):
        return "activity"
    return parent_region or "root"


class Line:
    __slots__ = ("pad", "sig", "depth", "region", "node", "role", "text", "parent_role", "idx")

    def __init__(self, pad, sig, depth, region, node, rl, text, parent_role):
        self.pad, self.sig, self.depth, self.region, self.node = pad, sig, depth, region, node
        self.role, self.text, self.parent_role, self.idx = rl, text, parent_role, -1


def page_lines(path):
    """The gate's scaffold skeleton, one line per element, with text + region. Returns
    (lines, meta). Widget subtrees collapse to WIDGET (both sides), converter notes skipped."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"<body\b[^>]*>(.*)</body>", raw, re.S | re.I)
    src = m.group(0) if m else raw
    tb = TextTree()
    tb.feed(src)
    body = next((k for k in tb.root.kids if k.tag == "body"), None)
    head = raw[:4000]
    legacy = bool(re.search(r"<html\b[^>]*\blevel=\"pr(m|inq)\"", head, re.I)) or 'id="container"' in raw
    out = []

    def walk(n, depth, reg, parent_role):
        if _cls(n) & NOTE_CLS:
            return
        pad = "  " * depth
        if _cls(n) & WIDGET_MARKERS:
            out.append(Line(pad + "WIDGET", "WIDGET", depth, reg, n, "WIDGET", "", parent_role))
            return
        r = region_of(n, reg)
        rl = role(n)
        out.append(Line(pad + label(n), label(n), depth, r, n, rl, node_text(n), parent_role))
        for k in n.kids:
            walk(k, depth + 1, r, rl)

    if body is None:
        for k in tb.root.kids:
            walk(k, 0, "root", "#root")
    else:
        walk(body, 0, "root", "#root")
    for i, ln in enumerate(out):
        ln.idx = i
    return out, {"legacy": legacy}


# ------------------------------------------------------------------------------------------------ chrome facts (alignment-free)
def page_facts(lines, code):
    """The repeating chrome as a SET of facts per page — header chip / head-buttons / menu / title count,
    footer ul class / links / order — so a missing link is one class, not three alignment fragments."""
    f = set()
    chip = [l for l in lines if l.region == "module-code" and l.node.tag == "div" and (l.node.attrs.get("id") == "module-code")]
    if chip:
        f.add("header:chip")
        t = (subtree_texts(chip[0].node, 1) or [""])[0].strip()
        if t.upper() == code.upper():
            f.add("header:chip=module-code")
        elif re.fullmatch(r"\d{1,2}", t):
            f.add("header:chip=lesson-number" + ("(00)" if t == "00" else ""))
        elif re.fullmatch(r"\d+(\.\d+)?", t):
            f.add("header:chip=decimal-number")
        elif t:
            f.add("header:chip=other")
        else:
            f.add("header:chip=empty")
    if any(l.node.attrs.get("id") == "module-head-buttons" for l in lines):
        f.add("header:head-buttons")
    if any(l.node.attrs.get("id") == "module-menu-content" for l in lines):
        f.add("header:menu-content")
    h1 = [l for l in lines if l.region == "title" and l.node.tag == "h1"]
    f.add(f"header:title-h1-count={min(len(h1), 3)}")
    if any(l.region == "footer" and l.node.attrs.get("id") in ("footer", "module-foot") for l in lines):
        f.add("footer:present")
        uls = [l for l in lines if l.region == "footer" and l.node.tag == "ul"]
        if uls:
            f.add("footer:ul=" + " ".join(sorted(_cls(uls[0].node))))
        keys = []
        for l in lines:
            if l.region == "footer" and l.node.tag == "a":
                a = l.node.attrs
                k = a.get("id") if a.get("id") in ("prev-lesson", "next-lesson") else ("home-nav" if "home-nav" in _cls(l.node) else "other")
                keys.append(k)
                f.add(f"footer:link={k}")
        f.add("footer:links=" + (",".join(keys) or "none"))
    inside = any(l.region == "footer" and l.node.attrs.get("id") == "footer" and l.node.parent is not None
                 and l.node.parent.attrs.get("id") == "body" for l in lines)
    if inside:
        f.add("footer:inside-body")
    if any(l.region == "crumbs" for l in lines):
        f.add("nav:crumbs")
    if any(l.region == "phases-nav" for l in lines):
        f.add("nav:phases")
    return f


# ------------------------------------------------------------------------------------------------ diff
def subtree_texts(n, k=5):
    """The first k texts of a subtree (its own, then its descendants'), widgets / notes skipped."""
    out = []

    def walk(x):
        if len(out) >= k:
            return
        if _cls(x) & (NOTE_CLS | WIDGET_MARKERS):
            return
        own = _WS.sub(" ", " ".join(x.own)).strip()
        if own:
            out.append(own[:400])
        for kid in x.kids:
            walk(kid)
    walk(n)
    return out


def diff_lines(g, c):
    """difflib on the gate's padded signature lines (autojunk=False, the r355 instrument).
    Returns (direction, gold_line|None, claude_line|None, carried) tuples.
      * a lone inline wrapper (span / b / a …) whose parent is itself a differing line is FOLDED
        into the parent BEFORE pairing — its parent's role (`h4>span`) carries it;
      * inside a replace block the survivors pair positionally; a pair at different depths and
        different tags is not a substitution but one MISSING + one EXTRA;
      * MOVED = a missing gold line whose (signature, text) is an extra Claude line elsewhere;
      * CARRIED = a one-sided line whose parent is one-sided the same way (the top line of a
        missing / extra subtree is the class; its descendants ride with it)."""
    sm = difflib.SequenceMatcher(None, [x.pad for x in g], [x.pad for x in c], autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    diff_ids = set()
    for op, i1, i2, j1, j2 in ops:
        diff_ids.update(id(x.node) for x in g[i1:i2])
        diff_ids.update(id(x.node) for x in c[j1:j2])

    def keep(x):
        n = x.node
        return not (n.tag in INLINE and n.parent is not None and id(n.parent) in diff_ids)

    out = []
    for op, i1, i2, j1, j2 in ops:
        G = [x for x in g[i1:i2] if keep(x)]
        C = [x for x in c[j1:j2] if keep(x)]
        n = min(len(G), len(C))
        for k in range(n):
            gl, cl = G[k], C[k]
            if gl.depth == cl.depth or gl.node.tag == cl.node.tag:
                out.append(["SUBSTITUTED", gl, cl])
            else:
                out.append(["MISSING", gl, None]); out.append(["EXTRA", None, cl])
        out += [["MISSING", x, None] for x in G[n:]]
        out += [["EXTRA", None, x] for x in C[n:]]
    # MOVED: a missing gold line whose (sig, text) is an extra Claude line elsewhere on the page
    extra_by_key = defaultdict(list)
    for k, (d, gl, cl) in enumerate(out):
        if d == "EXTRA" and cl.text and len(cl.text.split()) >= 2:
            extra_by_key[(cl.sig, unorm(cl.text))].append(k)
    consumed = set()
    for k in range(len(out)):
        if out[k] is None:
            continue
        d, gl, cl = out[k]
        if d == "MISSING" and gl.text and len(gl.text.split()) >= 2:
            key = (gl.sig, unorm(gl.text))
            cands = [j for j in extra_by_key.get(key, []) if j not in consumed]
            if cands:
                j = cands[0]
                consumed.add(j)
                out[k] = ["MOVED", gl, out[j][2]]
                out[j] = None
    out = [x for x in out if x]
    # CARRIED: descendants of a one-sided line, one-sided the same way
    dir_of = {}
    for d, gl, cl in out:
        if gl is not None:
            dir_of[id(gl.node)] = d
        if cl is not None:
            dir_of[id(cl.node)] = d
    final = []
    for d, gl, cl in out:
        n = (gl if gl is not None else cl).node
        pd = dir_of.get(id(n.parent)) if n.parent is not None else None
        carried = (d == "MISSING" and pd in ("MISSING", "MOVED")) or (d == "EXTRA" and pd in ("EXTRA", "MOVED"))
        final.append((d, gl, cl, carried))
    return final


# ------------------------------------------------------------------------------------------------ WT
_WT_CACHE = {}
_WT_LINES = {}


def wt_of(code):
    if code not in _WT_CACHE:
        _WT_CACHE[code] = wt_blob(code)
    return _WT_CACHE[code]


def wt_line_for(code, text):
    """The parsed-WT line that carries the block's distinctive phrase (for the example quote)."""
    if code not in _WT_LINES:
        d = _corpus.mdir(HUMAN, code)
        lines = []
        if os.path.isdir(d):
            for f in sorted(x for x in os.listdir(d) if x.endswith("_parsed.txt")):
                for ln in open(os.path.join(d, f), encoding="utf-8", errors="replace"):
                    s = ln.strip()
                    if s:
                        lines.append((s[:220], " " + unorm(s) + " "))
        _WT_LINES[code] = lines
    n = unorm(text)
    w = n.split()
    needles = []
    if len(w) <= 2:
        needles.append(" " + n + " ")
    else:
        needles.append(n)
        if len(w) >= 6:
            needles.append(" ".join(w[:6]))
        for i in range(len(w) - 2):
            win = w[i:i + 3]
            if max(len(x) for x in win) >= 6:
                needles.append(" ".join(win))
    for raw, folded in _WT_LINES[code]:
        for nd in needles:
            if nd in folded:
                return raw
    return ""


# ------------------------------------------------------------------------------------------------ KB
_KB_INDEX = None
REGION_TERMS = {
    "module-code": ["module-code"], "title": ["<h1><span>", "h1 title", "lesson title", "module title"],
    "header": ["#header", "header"], "module-menu": ["module-menu", "modulemenu", "module menu", "lesson menu"],
    "crumbs": ["crumbs", "inquirypanel", "side-nav", "inquiry"], "phases-nav": ["phases", "phaselink", "fundamentalspanel", "phase nav"],
    "footer": ["footer-nav", "#footer", "prev-lesson", "next-lesson", "home-nav", "footer"],
    "acks": ["acks", "acknowledg"], "activity": ["activity"], "body": [], "root": [],
}


def kb_index():
    global _KB_INDEX
    if _KB_INDEX is None:
        _KB_INDEX = []
        for dp, _, fs in os.walk(KB):
            if "/.git" in dp.replace("\\", "/") or "Claude outputs" in dp:
                continue
            for f in fs:
                if f.endswith(".md"):
                    p = os.path.join(dp, f)
                    rel = os.path.relpath(p, KB).replace("\\", "/")
                    try:
                        for i, ln in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
                            if len(ln) > 8:
                                _KB_INDEX.append((rel, i, ln.rstrip("\n"), ln.lower()))
                    except OSError:
                        pass
    return _KB_INDEX


def role_tokens(r):
    toks = set()
    for part in re.split(r"[>#.\[\]=\s]+", r):
        if part and part not in GENERIC_TOKENS and len(part) >= 3 and not part.isdigit():
            toks.add(part.lower())
    return toks


def kb_lookup(region, gold_role, claude_role, parent, limit=3):
    terms = [t.lower() for t in REGION_TERMS.get(region, [])]
    toks = role_tokens(gold_role) | role_tokens(claude_role) | role_tokens(parent)
    toks -= {"widget"}
    hits = []
    if not toks and not terms:
        return hits
    for rel, i, ln, low in kb_index():
        tok_hit = [t for t in toks if t in low]
        term_hit = any(t in low for t in terms)
        if region in ("body", "root", "activity"):
            ok = len(tok_hit) >= 2 or (tok_hit and term_hit)
        else:
            ok = term_hit and tok_hit
        if ok:
            hits.append(f"{rel}:{i} — {ln.strip()[:150]}")
            if len(hits) >= limit:
                break
    return hits


# ------------------------------------------------------------------------------------------------ mine
def region_floor(region):
    return ("modules", CHROME_FLOOR_MODULES) if region in CHROME else ("pages", BODY_FLOOR_PAGES)


def mine(codes, quiet=False, log=None):
    meta = load_meta()
    t0 = time.time()
    classes = {}          # key -> record
    presence_gold = defaultdict(lambda: defaultdict(Counter))    # (region, parent>role) -> group -> {page: count}
    presence_claude = defaultdict(lambda: defaultdict(Counter))
    region_pages_gold = defaultdict(lambda: defaultdict(set))  # region -> group -> set(pages)
    region_pages_claude = defaultdict(lambda: defaultdict(set))
    group_pages = defaultdict(set)                                # group -> set(pages)
    facts_gold = defaultdict(lambda: defaultdict(set))            # fact -> group -> set(pages)
    facts_claude = defaultdict(lambda: defaultdict(set))
    fact_classes = {}                                             # (direction, fact) -> record
    census = []
    per_page = []
    skipped, no_wt = [], set()
    npairs = 0
    mods_seen = set()
    for mi, code in enumerate(codes):
        mm = meta.get(code, {})
        tdir = _corpus.mdir(HUMAN, code)
        parent = os.path.basename(os.path.dirname(tdir))
        template = parent if parent in _corpus.TEMPLATE_DIRS else (mm.get("template_type") or "flat")
        subject = mm.get("subject") or "None"
        series = mm.get("series") or code[:5]
        wt = wt_of(code)
        blob = wt[0] if wt else ""
        if not wt:
            no_wt.add(code)
        for n, cp, hp in pairs(code):
            if SKIP_PAGE.search(os.path.basename(hp)) or re.search(r"acks|acknowledge|glossary", os.path.basename(cp), re.I):
                continue
            try:
                g, gmeta = page_lines(hp)
                c, cmeta = page_lines(cp)
            except Exception as e:
                skipped.append((code, os.path.basename(cp), f"{type(e).__name__}: {e}"[:80]))
                continue
            npairs += 1
            mods_seen.add(code)
            page = f"{code}/{os.path.basename(cp)}"
            legacy = "Legacy" if gmeta["legacy"] else "Refresh"
            ptype = "overview" if n == 0 else "lesson"
            groups = {"template": template, "era": legacy, "subject": subject, "series": series,
                      "template+era": f"{template}/{legacy}", "ptype": ptype,
                      "template+ptype": f"{template}/{ptype}", "subject+ptype": f"{subject}/{ptype}"}
            gkeys = [f"{k}={v}" for k, v in groups.items()]
            for gk in gkeys + ["ALL"]:
                group_pages[gk].add(page)
            # presence (consensus denominators / numerators)
            for side, lines, pres, rpages in (("gold", g, presence_gold, region_pages_gold),
                                               ("claude", c, presence_claude, region_pages_claude)):
                seen_regions = set()
                for ln in lines:
                    seen_regions.add(ln.region)
                    key = (ln.region, f"{ln.parent_role} > {ln.role}")
                    for gk in gkeys + ["ALL"]:
                        pres[key][gk][page] += 1
                for r in seen_regions:
                    for gk in gkeys + ["ALL"]:
                        rpages[r][gk].add(page)
            # the alignment-free chrome facts
            fg, fc = page_facts(g, code), page_facts(c, code)
            for fact in fg:
                for gk in gkeys + ["ALL"]:
                    facts_gold[fact][gk].add(page)
            for fact in fc:
                for gk in gkeys + ["ALL"]:
                    facts_claude[fact][gk].add(page)
            for direction, facts in (("MISSING", fg - fc), ("EXTRA", fc - fg)):
                for fact in facts:
                    fr = fact_classes.get((direction, fact))
                    if fr is None:
                        fr = fact_classes[(direction, fact)] = {"direction": direction, "fact": fact, "pages": set(), "modules": set(),
                                                                "groups": defaultdict(lambda: {"pages": set(), "modules": set()}),
                                                                "examples": [], "ex_mods": set()}
                    fr["pages"].add(page); fr["modules"].add(code)
                    for gk in gkeys:
                        fr["groups"][gk]["pages"].add(page); fr["groups"][gk]["modules"].add(code)
                    if code not in fr["ex_mods"] and len(fr["examples"]) < 3:
                        fr["ex_mods"].add(code)
                        pre = fact.split(":", 1)[0] + ":"
                        fr["examples"].append({"module": code, "page": os.path.basename(cp), "gold_page": os.path.basename(hp),
                                               "gold_facts": sorted(x for x in fg if x.startswith(pre)),
                                               "claude_facts": sorted(x for x in fc if x.startswith(pre))})
            # the diff
            diffs = diff_lines(g, c)
            page_rec = {"module": code, "page": os.path.basename(cp), "gold": os.path.basename(hp),
                        "template": template, "era": legacy, "subject": subject, "series": series,
                        "gold_lines": len(g), "claude_lines": len(c), "diff_lines": len(diffs),
                        "diff_lines_top": sum(1 for x in diffs if not x[3]),
                        "by_region": Counter(), "by_dir": Counter()}
            key_of_node = {}
            for d, gl, cl, carried in diffs:
                region = (gl.region if gl is not None else cl.region)
                page_rec["by_region"][region] += 1
                page_rec["by_dir"][d] += 1
                n = (gl if gl is not None else cl).node
                if carried:
                    # ride with the nearest non-carried ancestor's class
                    p = n.parent
                    while p is not None and id(p) not in key_of_node:
                        p = p.parent
                    if p is not None:
                        classes[key_of_node[id(p)]]["lines_carried"] += 1
                    continue
                grole = gl.role if gl is not None else ""
                crole = cl.role if cl is not None else ""
                parent_ctx = (gl.parent_role if gl is not None else cl.parent_role)
                key = (region, parent_ctx, grole, crole, d)
                if d == "MOVED":
                    key = (region, parent_ctx, grole, f"→ {cl.region}", d)
                key_of_node[id(n)] = key
                if cl is not None:
                    key_of_node[id(cl.node)] = key
                rec = classes.get(key)
                if rec is None:
                    rec = classes[key] = {"region": region, "parent": parent_ctx, "gold": grole, "claude": crole,
                                          "direction": d, "pages": set(), "modules": set(), "lines": 0, "lines_carried": 0,
                                          "derivable": 0, "not_derivable": 0, "structure_only": 0,
                                          "groups": defaultdict(lambda: {"pages": set(), "modules": set()}),
                                          "examples": [], "ex_mods": set()}
                rec["pages"].add(page); rec["modules"].add(code); rec["lines"] += 1
                for gk in gkeys:
                    rec["groups"][gk]["pages"].add(page); rec["groups"][gk]["modules"].add(code)
                # derivable content: a MISSING line is judged on its own text, else on its subtree's texts
                texts = ([gl.text] if (gl is not None and gl.text) else (subtree_texts(gl.node) if gl is not None else []))
                if d != "MISSING" or not texts or region in STRUCTURE_REGIONS:
                    kind = "structure"
                    rec["structure_only"] += 1; rec["derivable"] += 1
                    der = True
                    text = texts[0] if texts else ""
                else:
                    hits = [has_source(unorm(t), blob) if blob else False for t in texts]
                    der = sum(hits) * 2 >= len(hits)
                    kind = "content"
                    rec["derivable" if der else "not_derivable"] += 1
                    text = next((t for t, h in zip(texts, hits) if h), texts[0])
                if code not in rec["ex_mods"] and len(rec["examples"]) < 3:
                    rec["ex_mods"].add(code)
                    gt = (gl.text or (subtree_texts(gl.node, 1) or [""])[0]) if gl is not None else ""
                    ct = (cl.text or (subtree_texts(cl.node, 1) or [""])[0]) if cl is not None else ""
                    ex = {"module": code, "page": os.path.basename(cp), "gold_page": os.path.basename(hp),
                          "gold_line": (f"{gl.pad}" + (f"  «{gt[:120]}»" if gt else "")) if gl is not None else "—",
                          "claude_line": (f"{cl.pad}" + (f"  «{ct[:120]}»" if ct else "")) if cl is not None else "—",
                          "kind": kind, "derivable": der,
                          "wt_line": (wt_line_for(code, text) if (text and der and kind == "content") else "")}
                    rec["examples"].append(ex)
            per_page.append(page_rec)
            # completeness census for the chrome
            for r in CENSUS_REGIONS:
                gi = [ln for ln in g if ln.region == r and ln.text and ln.sig != "WIDGET"]
                ci = [ln for ln in c if ln.region == r and ln.text and ln.sig != "WIDGET"]
                if not gi and not ci:
                    continue
                cblob = " " + unorm(" \n ".join(x.text for x in ci)) + " "
                g_in_wt = [x for x in gi if blob and has_source(unorm(x.text), blob)]
                misses = [x for x in g_in_wt if not has_source(unorm(x.text), cblob)]
                census.append({"module": code, "page": os.path.basename(cp), "region": r, "template": template,
                               "subject": subject, "gold_items": len(gi), "gold_in_wt": len(g_in_wt),
                               "claude_items": len(ci), "derivable_misses": len(misses),
                               "miss_samples": [f"{x.pad.strip()} «{x.text[:80]}»" for x in misses[:3]]})
        if log and (mi % 25 == 0 or mi == len(codes) - 1):
            with open(log, "a", encoding="utf-8") as fh:
                fh.write(f"{time.strftime('%H:%M:%S')} {mi + 1}/{len(codes)} {code} pairs={npairs} classes={len(classes)}\n")
        if not quiet and mi % 50 == 0:
            print(f"  … {mi + 1}/{len(codes)} modules, {npairs} pairs, {len(classes)} classes [{time.time() - t0:.0f}s]", flush=True)
    # ---- finalise classes
    rows = []
    for key, rec in classes.items():
        region = rec["region"]
        unit, floor = region_floor(region)
        gold_key = (region, f"{rec['parent']} > {rec['gold']}")
        claude_key = (region, f"{rec['parent']} > {rec['claude']}")
        dregion = DENOM_REGION.get(region, region)
        # multiplicity: a MISSING class on pages where the gold carries K of the element asks "how many gold
        # pages carry ≥ K" (a second title h1 is a convention only where second h1s are); an EXTRA class asks
        # "how many gold pages carry FEWER than Claude's K"
        pg = sorted(presence_gold[gold_key]["ALL"].get(p, 0) for p in rec["pages"])
        pc = sorted(presence_claude[claude_key]["ALL"].get(p, 0) for p in rec["pages"])
        K = max(1, pg[len(pg) // 2]) if (pg and rec["direction"] in ("MISSING", "MOVED")) else 1
        Kc = max(1, pc[len(pc) // 2]) if (pc and rec["direction"] == "EXTRA") else 1

        def _cons(gk):
            denom = len(region_pages_gold[dregion].get(gk, ()))
            if not denom:
                return 0.0, 0.0, 0
            if rec["direction"] == "EXTRA":
                have = sum(1 for p, n in presence_gold[claude_key].get(gk, {}).items() if n >= Kc)
                cons = (denom - have) / denom
            else:
                have = sum(1 for p, n in presence_gold[gold_key].get(gk, {}).items() if n >= K)
                cons = have / denom
            cform = len(presence_gold[claude_key].get(gk, ())) / denom if rec["claude"] else 0.0
            return cons, cform, denom

        groups_out = {}
        best = None
        for gk, gv in rec["groups"].items():
            cons, cform, denom = _cons(gk)
            size = len(gv["modules"]) if unit == "modules" else len(gv["pages"])
            passes = size >= floor and cons >= CONSENSUS_MIN
            groups_out[gk] = {"pages": len(gv["pages"]), "modules": len(gv["modules"]), "gold_region_pages": denom,
                              "consensus": round(cons, 3), "claude_form_in_gold": round(cform, 3), "passes_floor_and_consensus": passes}
            if passes and (best is None or (cons, size) > (best[1], best[2])):
                best = (gk, cons, size)
        total_lines = rec["lines"]
        der_share = rec["derivable"] / total_lines if total_lines else 0.0
        structure_only = rec["structure_only"] == total_lines
        size_all = len(rec["modules"]) if unit == "modules" else len(rec["pages"])
        cons_all, _cf_all, denom_all = _cons("ALL")
        if size_all < floor:
            status = "BELOW FLOOR"
        elif best is None:
            status = "BELOW CONSENSUS (no group ≥ 0.60 at the floor)"
        elif not (structure_only or der_share >= DERIVABLE_MIN):
            status = "NOT DERIVABLE (content share < 0.60)"
        else:
            status = "CANDIDATE"
        if best is not None and best[0].startswith("template=") is False and status == "CANDIDATE":
            pass
        rows.append({
            "region": region, "parent": rec["parent"], "gold_form": rec["gold"], "claude_form": rec["claude"],
            "direction": rec["direction"], "pages": len(rec["pages"]), "modules": len(rec["modules"]),
            "lines": total_lines, "lines_carried": rec["lines_carried"], "unit": unit, "floor": floor, "size": size_all,
            "consensus_all": round(cons_all, 3), "gold_region_pages_all": denom_all, "gold_k": K, "claude_k": Kc,
            "derivable_share": round(der_share, 3), "structure_only": structure_only,
            "not_derivable_lines": rec["not_derivable"],
            "best_group": {"group": best[0], "consensus": round(best[1], 3), "size": best[2]} if best else None,
            "status": status, "groups": groups_out, "examples": rec["examples"],
            "module_list": sorted(rec["modules"])[:60],
        })
    rows.sort(key=lambda r: (REGION_ORDER.get(r["region"], 9), -r["modules"], -r["pages"], r["direction"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    # KB lookup for the rows that matter (top 120 + every candidate)
    for r in rows:
        if r["rank"] <= 120 or r["status"] == "CANDIDATE":
            r["kb_hits"] = kb_lookup(r["region"], r["gold_form"], r["claude_form"], r["parent"])
            r["authority"] = ("1 — KB rule (verify the hit's scope)" if r["kb_hits"] else
                              ("3 — the module's own gold (group consensus ≥ 0.60)" if r["best_group"] else
                               "4/none — no KB rule, no group consensus ≥ 0.60 at the floor"))
        else:
            r["kb_hits"] = []; r["authority"] = ""
    # census aggregate
    cagg = {}
    for r in CENSUS_REGIONS:
        recs = [x for x in census if x["region"] == r]
        miss_pages = [x for x in recs if x["derivable_misses"] > 0]
        cagg[r] = {"pages_with_region": len(recs), "gold_items": sum(x["gold_items"] for x in recs),
                   "gold_in_wt": sum(x["gold_in_wt"] for x in recs), "claude_items": sum(x["claude_items"] for x in recs),
                   "derivable_misses": sum(x["derivable_misses"] for x in recs),
                   "pages_with_misses": len(miss_pages), "modules_with_misses": len({x["module"] for x in miss_pages}),
                   "by_template": {t: {"pages_with_misses": len([x for x in miss_pages if x["template"] == t]),
                                       "modules_with_misses": len({x["module"] for x in miss_pages if x["template"] == t}),
                                       "derivable_misses": sum(x["derivable_misses"] for x in miss_pages if x["template"] == t)}
                                   for t in sorted({x["template"] for x in recs})},
                   "worst": sorted(miss_pages, key=lambda x: -x["derivable_misses"])[:8]}
    # the chrome FACT classes (alignment-free): one row per (direction, fact)
    fact_rows = []
    for (direction, fact), fr in fact_classes.items():
        groups_out = {}
        best = None
        for gk, gv in fr["groups"].items():
            denom = len(group_pages.get(gk, ()))
            have = len(facts_gold[fact].get(gk, ()))
            cons = ((have if direction == "MISSING" else denom - have) / denom) if denom else 0.0
            cshare = len(facts_claude[fact].get(gk, ())) / denom if denom else 0.0
            size = len(gv["modules"])
            passes = size >= CHROME_FLOOR_MODULES and cons >= CONSENSUS_MIN
            groups_out[gk] = {"pages": len(gv["pages"]), "modules": size, "group_pages": denom, "gold_share": round(have / denom, 3) if denom else 0.0,
                              "claude_share": round(cshare, 3), "consensus": round(cons, 3), "passes_floor_and_consensus": passes}
            if passes and (best is None or (cons, size) > (best[1], best[2])):
                best = (gk, cons, size)
        denom = len(group_pages.get("ALL", ()))
        have = len(facts_gold[fact].get("ALL", ()))
        cons_all = ((have if direction == "MISSING" else denom - have) / denom) if denom else 0.0
        nmod = len(fr["modules"])
        status = ("BELOW FLOOR" if nmod < CHROME_FLOOR_MODULES else
                  ("CANDIDATE" if best else "BELOW CONSENSUS (no group ≥ 0.60 at the floor)"))
        fact_rows.append({"direction": direction, "fact": fact, "region": fact.split(":", 1)[0], "pages": len(fr["pages"]), "modules": nmod,
                          "gold_share_all": round(have / denom, 3) if denom else 0.0, "consensus_all": round(cons_all, 3),
                          "best_group": {"group": best[0], "consensus": round(best[1], 3), "size": best[2]} if best else None,
                          "status": status, "groups": groups_out, "examples": fr["examples"], "module_list": sorted(fr["modules"])[:60]})
    fact_rows.sort(key=lambda r: ({"header": 0, "nav": 1, "footer": 2}.get(r["region"], 3), -r["modules"], -r["pages"]))
    # class-shaped census rows (the §1d item 4 "gold 6 / Claude 2" class)
    census_rows = []
    for r in CENSUS_REGIONS:
        a = cagg[r]
        unit, floor = region_floor(r)
        size = a["modules_with_misses"]
        census_rows.append({"region": r, "class": f"{r} completeness: the WT had it, the gold rendered it, Claude did not",
                            "pages": a["pages_with_misses"], "modules": size, "derivable_misses": a["derivable_misses"],
                            "status": "CANDIDATE (verify by eye — text presence, not position)" if size >= floor else "BELOW FLOOR",
                            "by_template": a["by_template"]})
    summary = {
        "pairs": npairs, "modules": len(mods_seen), "modules_requested": len(codes), "modules_without_wt": sorted(no_wt),
        "skipped_parse_errors": len(skipped), "skipped": skipped[:20], "classes": len(rows),
        "candidates": sum(1 for r in rows if r["status"] == "CANDIDATE"),
        "below_floor": sum(1 for r in rows if r["status"] == "BELOW FLOOR"),
        "diff_lines_total": sum(p["diff_lines"] for p in per_page),
        "diff_lines_by_region": dict(sum((Counter(p["by_region"]) for p in per_page), Counter())),
        "diff_lines_by_direction": dict(sum((Counter(p["by_dir"]) for p in per_page), Counter())),
        "seconds": round(time.time() - t0, 1),
    }
    for p in per_page:
        p["by_region"] = dict(p["by_region"]); p["by_dir"] = dict(p["by_dir"])
    summary["chrome_fact_classes"] = len(fact_rows)
    summary["chrome_fact_candidates"] = sum(1 for r in fact_rows if r["status"] == "CANDIDATE")
    return {"summary": summary, "classes": rows, "chrome_facts": fact_rows, "census": cagg, "census_rows": census_rows, "per_page": per_page}


# ------------------------------------------------------------------------------------------------ report
def _git_head():
    try:
        return subprocess.check_output(["git", "-C", os.path.join(ROOT, "pageforge-site"), "rev-parse", "--short", "HEAD"],
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "?"


def _der(r):
    return "structure-only" if r["structure_only"] else f"{r['derivable_share']:.2f}"


def _grp(r, prefix):
    out = []
    for gk, gv in sorted(r["groups"].items(), key=lambda kv: -kv[1]["modules"]):
        if gk.startswith(prefix):
            out.append(f"{gk.split('=', 1)[1]} {gv['modules']}m/{gv['pages']}p c={gv['consensus']:.2f}")
    return "; ".join(out[:6])


def write_md(res, path, corpus_note):
    s = res["summary"]
    L = [f"# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)", "",
         f"**Produced:** {time.strftime('%Y-%m-%d %H:%M NZST')} by `reference/tests/_diff_miner.py` on the CURRENT corpus "
         f"({corpus_note}). **Population:** the skeleton gate's own — {s['pairs']} paired pages / {s['modules']} modules "
         f"(compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: "
         f"{s['skipped_parse_errors']} (must be 0); modules without a parsed WT: {len(s['modules_without_wt'])}. "
         f"Run time {s['seconds']} s.", "",
         f"**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing "
         f"skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY "
         f"gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; "
         f"EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same "
         f"text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying "
         f"the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the "
         f"module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.", "",
         f"**Candidate rule (§1d).** modules ≥ {CHROME_FLOOR_MODULES} for a chrome class (module-code / title / header / "
         f"module-menu / crumbs / phases-nav / footer / acks), pages ≥ {BODY_FLOOR_PAGES} for a body / activity class; "
         f"gold consensus ≥ {CONSENSUS_MIN:.2f} in at least one template or subject group that itself reaches the floor; "
         f"structure-only or derivable share ≥ {DERIVABLE_MIN:.2f}. A class below the floor is listed, never dropped. "
         f"A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement "
         f"before any code — this table is the queue, not the verdict.", "",
         "## Summary", "",
         f"- differing skeleton lines: {s['diff_lines_total']} — by direction {s['diff_lines_by_direction']}",
         f"- by region: {dict(sorted(s['diff_lines_by_region'].items(), key=lambda kv: REGION_ORDER.get(kv[0], 9)))}",
         f"- classes: {s['classes']} — CANDIDATE {s['candidates']}, below floor {s['below_floor']}, the rest below consensus / not derivable",
         ""]
    L += ["## Completeness census — the repeating chrome (§1d item 4)", "",
          "| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |",
          "|---|---|---|---|---|---|---|---|---|"]
    for cr in res["census_rows"]:
        a = res["census"][cr["region"]]
        L.append(f"| {cr['region']} | {a['pages_with_region']} | {a['gold_items']} | {a['gold_in_wt']} | {a['claude_items']} | "
                 f"{a['derivable_misses']} | {a['pages_with_misses']} | {a['modules_with_misses']} | {cr['status']} |")
    L.append("")
    for cr in res["census_rows"]:
        a = res["census"][cr["region"]]
        bt = "; ".join(f"{t} {v['modules_with_misses']}m/{v['pages_with_misses']}p/{v['derivable_misses']} misses" for t, v in a["by_template"].items())
        L.append(f"- **{cr['region']}** by template: {bt}")
        for w in a["worst"][:4]:
            L.append(f"  - {w['module']} {w['page']}: gold {w['gold_items']} items ({w['gold_in_wt']} in WT) / Claude {w['claude_items']} — "
                     f"{w['derivable_misses']} derivable misses, e.g. " + " · ".join(w["miss_samples"][:2]))
    L += ["", "## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)", "",
          "A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / "
          "`=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, "
          "`footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, "
          "`footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the "
          "reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.", "",
          "| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |", "|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(res.get("chrome_facts", []), 1):
        bg = f"{r['best_group']['group']} c={r['best_group']['consensus']:.2f} n={r['best_group']['size']}" if r["best_group"] else "—"
        L.append(f"| F{i} | {r['direction']} | `{r['fact']}` | {r['pages']} | {r['modules']} | {r['gold_share_all']:.2f} | {r['consensus_all']:.2f} | {bg} | {r['status']} |")
    L.append("")
    for i, r in enumerate(res.get("chrome_facts", []), 1):
        if r["status"] != "CANDIDATE":
            continue  # 17 Sept 2026: detail blocks for CANDIDATE facts only (size discipline); the table above lists the rest
        L.append(f"### F{i} · {r['direction']} `{r['fact']}` — {r['status']} (pages {r['pages']} / modules {r['modules']})")
        for pref in ("template+ptype=", "subject="):
            items = sorted([(k, v) for k, v in r["groups"].items() if k.startswith(pref)], key=lambda kv: -kv[1]["modules"])[:8]
            L.append(f"- by {pref[:-1]}: " + "; ".join(f"{k.split('=', 1)[1]} {v['modules']}m/{v['pages']}p gold {v['gold_share']:.2f} Claude {v['claude_share']:.2f} c={v['consensus']:.2f}" for k, v in items))
        for ex in r["examples"]:
            L.append(f"- **{ex['module']}** {ex['page']} ↔ {ex['gold_page']}: gold {ex['gold_facts']} · Claude {ex['claude_facts']}")
        L.append(f"- modules: {', '.join(r['module_list'][:24])}{' …' if len(r['module_list']) > 24 else ''}")
        L.append("")
    L += ["", "## The ranked queue — chrome regions first, then by modules affected", "",
          "| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    shown = [r for r in res["classes"] if r["rank"] <= 100 or r["status"] == "CANDIDATE"]  # 17 Sept 2026: 150 → 100 (size discipline)
    for r in shown:
        bg = f"{r['best_group']['group']} c={r['best_group']['consensus']:.2f} n={r['best_group']['size']}" if r["best_group"] else "—"
        der = "structure" if r["structure_only"] else f"{r['derivable_share']:.2f}"
        kb = "yes" if r["kb_hits"] else "—"
        L.append(f"| {r['rank']} | {r['region']} | {r['direction']} | `{r['parent'][:40]}` | `{r['gold_form'][:50] or '—'}` | "
                 f"`{r['claude_form'][:50] or '—'}` | {r['pages']} | {r['modules']} | {r['consensus_all']:.2f} of {r['gold_region_pages_all']} | "
                 f"{bg} | {der} | {kb} | {r['status']} |")
    # --- 17 Sept 2026 (Chris): the details + below-floor sections moved to a COMPANION file so that
    # DIFF_QUEUE.md stays small enough to be read whole by a session (the 728 KB single file caused
    # context-compaction thrashing). The companion is never read whole: grep a rank, sed the range.
    MAIN = L
    dpath = os.path.join(OUTPUTS, "_diff_queue_details.md")
    MAIN += ["", "## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`",
             "Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the",
             "below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' "
             "CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25",
             "candidates' detail blocks are repeated below for convenience.", ""]
    L = ["# _diff_queue_details.md — companion of DIFF_QUEUE.md (LOOP §1d). NEVER read whole; grep a rank, sed a range.", ""]
    L += ["", "## Candidate and top-row details (three example modules each — WT / gold / Claude quoted)", ""]
    detail = [r for r in res["classes"] if r["status"] == "CANDIDATE" or r["rank"] <= 40]
    top25 = {r["rank"] for r in [x for x in res["classes"] if x["status"] == "CANDIDATE"][:25]}
    _detail_start = len(L)
    for r in detail:
        L.append(f"### #{r['rank']} · {r['region']} · {r['direction']} · `{r['parent']}` › gold `{r['gold_form'] or '—'}` vs Claude `{r['claude_form'] or '—'}` — {r['status']}")
        L.append(f"- pages {r['pages']} / modules {r['modules']} / lines {r['lines']}; consensus (all) {r['consensus_all']:.2f} of {r['gold_region_pages_all']} gold pages with the region; "
                 f"derivable {_der(r)} ({r['not_derivable_lines']} lines with no WT source)")
        L.append(f"- by template: {_grp(r, 'template=')}")
        L.append(f"- by subject: {_grp(r, 'subject=')}")
        L.append(f"- by era: {_grp(r, 'era=')}")
        L.append(f"- authority (§1b): {r['authority']}")
        for h in r["kb_hits"]:
            L.append(f"  - KB: {h}")
        for ex in r["examples"]:
            L.append(f"- **{ex['module']}** {ex['page']} ↔ {ex['gold_page']} ({ex['kind']}, derivable={ex['derivable']})")
            L.append(f"  - gold: `{ex['gold_line'].strip()[:200]}`")
            L.append(f"  - Claude: `{ex['claude_line'].strip()[:200]}`")
            if ex["wt_line"]:
                L.append(f"  - WT: `{ex['wt_line'][:200]}`")
        L.append(f"- modules: {', '.join(r['module_list'][:24])}{' …' if len(r['module_list']) > 24 else ''}")
        L.append("")
    # copy the top-25 candidate blocks into the main file
    cur = None
    for ln in L[_detail_start:]:
        if ln.startswith("### #"):
            try: cur = int(ln[5:].split(" ")[0])
            except ValueError: cur = None
        if cur in top25:
            MAIN.append(ln)
    L += ["## Below the floor (every remaining class with ≥ 2 modules — recorded, never dropped)", "",
          "| # | region | dir | parent › gold › Claude | pages | modules | consensus | derivable |", "|---|---|---|---|---|---|---|---|"]
    for r in res["classes"]:
        if r["rank"] > 150 and r["modules"] >= 2 and r["status"] != "CANDIDATE":
            L.append(f"| {r['rank']} | {r['region']} | {r['direction']} | `{r['parent'][:30]}` › `{r['gold_form'][:36] or '—'}` › `{r['claude_form'][:36] or '—'}` | "
                     f"{r['pages']} | {r['modules']} | {r['consensus_all']:.2f} | {_der(r)} |")
    singles = sum(1 for r in res["classes"] if r["modules"] < 2)
    L += ["", f"({singles} single-module classes are in the JSON only.)", ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(MAIN))
    with open(dpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print(f"wrote {path} ({sum(len(x)+1 for x in MAIN)//1024} KB) + {dpath} ({sum(len(x)+1 for x in L)//1024} KB)")


# ------------------------------------------------------------------------------------------------ selftest
def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        gold = os.path.join(td, "g.html"); cl = os.path.join(td, "c.html")
        open(gold, "w", encoding="utf-8").write(
            '<html template="combo"><body class="inquiry container-fluid"><div id="header"><h1><span>Title</span></h1>'
            '<div id="module-menu-content" class="moduleMenu"><div class="row"><div class="col-md-6 col-12 paddingR">'
            '<h4><span>Learning intentions</span></h4><p>Ākonga will:</p><ul><li>read</li></ul></div></div></div></div>'
            '<div id="body"><div class="crumbs"><div class="showing"><p>Overview</p></div><div><p>Phase two</p></div></div>'
            '<div class="row"><div class="col-md-8 col-12"><h3>Introduction</h3><p>Welcome to the whakataukī module about kererū birds.</p></div></div>'
            '<div class="accordion"><div class="accHead"><h4>x</h4></div></div></div>'
            '<div id="footer"><ul class="footer-nav inquiry-nav"><li><a id="next-lesson">n</a></li></ul></div></body></html>')
        open(cl, "w", encoding="utf-8").write(
            '<html template="combo"><body class="inquiry container-fluid"><div id="header"><div id="module-code"><h1>BLL110</h1></div>'
            '<h1><span>Title</span></h1><div id="module-menu-content" class="moduleMenu"><div class="row">'
            '<div class="col-md-6 col-12 paddingR"><h5>Learning intentions</h5><h5>Ākonga will:</h5><ul><li>read</li></ul></div></div></div></div>'
            '<div id="body"><div class="crumbs"><div class="showing"><p>Overview</p></div></div>'
            '<div class="row"><div class="col-md-8 col-12"><h3>Introduction</h3><p class="cv2-note">note</p></div></div>'
            '<div class="accordion"><p>inside widget</p></div></div>'
            '<div id="footer"><ul class="footer-nav inquiry-nav"><li><a id="next-lesson">n</a></li></ul></div></body></html>')
        g, gm = page_lines(gold); c, cm = page_lines(cl)
        regs = {ln.region for ln in g}
        assert {"title", "module-menu", "crumbs", "body", "footer"} <= regs, regs
        assert any(ln.sig == "WIDGET" for ln in g) and any(ln.sig == "WIDGET" for ln in c), "widget collapse"
        assert not any("cv2-note" in ln.sig for ln in c), "converter note must be skipped"
        d = diff_lines(g, c)
        top = [x for x in d if not x[3]]
        kinds = {(x[0], (x[1] if x[1] is not None else x[2]).region, (x[1].role if x[1] is not None else ""),
                  (x[2].role if x[2] is not None else "")) for x in top}
        assert ("EXTRA", "module-code", "", "div#module-code") in kinds, kinds
        assert any(x[3] and x[0] == "EXTRA" and x[2].node.tag == "h1" and x[2].region == "module-code" for x in d), "the chip's h1 must be CARRIED"
        assert any(k[0] == "SUBSTITUTED" and k[1] == "module-menu" and k[2] == "h4>span" and k[3] == "h5" for k in kinds), kinds
        assert any(k[0] == "SUBSTITUTED" and k[1] == "module-menu" and k[2] == "p" and k[3] == "h5" for k in kinds), kinds
        assert any(k[0] == "MISSING" and k[1] == "crumbs" and k[2] == "div" for k in kinds), kinds
        assert any(x[3] and x[0] == "MISSING" and x[1].region == "crumbs" and x[1].node.tag == "p" for x in d), "the crumb's p must be CARRIED"
        assert any(k[0] == "MISSING" and k[1] == "body" and k[2] == "p" for k in kinds), kinds
        assert not any((x[1] if x[1] is not None else x[2]).node.tag == "span" for x in d), "the lone span must fold into h4>span"
        print("LIVENESS ok — regions, widget collapse, note skip, the h4>span→h5 role fold, EXTRA module-code (+ carried h1), MISSING crumb (+ carried p) + body p")
        fg, fc = page_facts(g, "BLL110"), page_facts(c, "BLL110")
        assert "header:chip" not in fg and {"header:chip", "header:chip=module-code"} <= fc, (fg, fc)
        assert {"footer:present", "footer:ul=footer-nav inquiry-nav", "footer:link=next-lesson", "footer:links=next-lesson", "nav:crumbs"} <= fg, fg
        assert "header:title-h1-count=1" in fg and "header:menu-content" in fg
        print("FACTS ok — the chrome facts read the chip, the footer links and the crumbs as sets")
        # derivable: the body p's text vs a WT blob
        blob = " " + unorm("Welcome to the whakataukī module about kererū birds and more") + " "
        assert has_source(unorm("Welcome to the whakataukī module about kererū birds."), blob)
        assert not has_source(unorm("A sentence the writer never typed anywhere at all."), blob)
        print("DERIVABLE ok — the round-110 tolerance decides content derivability")
        # detection: a raising pair is counted
        try:
            page_lines(os.path.join(td, "missing.html")); raise AssertionError("must raise")
        except FileNotFoundError:
            print("DETECTION ok — a missing page raises (mine() counts it as skipped, never hides it)")
    print("SELFTEST PASS")


def main():
    argv = sys.argv[1:]
    if "--selftest" in argv:
        selftest(); return
    js = md = None; codes = []; i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--json":
            js = argv[i + 1]; i += 2; continue
        if a == "--md":
            md = argv[i + 1]; i += 2; continue
        if a.startswith("-"):
            i += 1; continue
        codes.append(a); i += 1
    scoped = bool(codes)
    if not codes:
        codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
    js = js or os.path.join(OUTPUTS, "_diff_miner_scoped.json" if scoped else "_diff_miner.json")
    md = md or (os.path.join(OUTPUTS, "_diff_miner_scoped.md") if scoped else os.path.join(ROOT, "DIFF_QUEUE.md"))
    log = os.path.join(OUTPUTS, "_diff_miner_progress.log")
    open(log, "w").close()
    print(f"DIFF MINER over {len(codes)} modules …", flush=True)
    res = mine(codes, log=log)
    s = res["summary"]
    corpus_note = f"pageforge-site HEAD {_git_head()}; Claude corpus {len(_corpus.mods(CLAUDE))} dirs"
    res["summary"]["corpus_note"] = corpus_note
    with open(js, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, default=lambda o: sorted(o) if isinstance(o, set) else str(o))
    write_md(res, md, corpus_note)
    print(f"pairs {s['pairs']} / modules {s['modules']} / parse errors {s['skipped_parse_errors']} / diff lines {s['diff_lines_total']} / "
          f"classes {s['classes']} (CANDIDATE {s['candidates']}, below floor {s['below_floor']}) in {s['seconds']} s")
    print(f"wrote {js}\nwrote {md}")


if __name__ == "__main__":
    main()
