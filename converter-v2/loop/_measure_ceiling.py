#!/usr/bin/env python3
"""ROUND 0 (LOOP__Autonomous_Rounds.md §1) — THE CEILING INSTRUMENT.

For every human-gold page, take each TEXT-BEARING BLOCK of the page (heading, paragraph,
list item, table cell, caption, …) and test — fuzzily, with the round-110 matcher's
tolerance (anchor_compare._phrase_present: verbatim, OR the 6-word head, OR any 3 consecutive
words holding a >=6-char content word) — whether that text exists ANYWHERE in the module's
parsed Writers Template (the `*_parsed.txt`, which carries the Media List too).

A block with NO source in the WT is structure no converter rule can derive from the raw
inputs — the human developer authored it from verbal writer feedback or their own judgement.
The share of such blocks is the NON-DERIVABLE share; (1 - share) is the CEILING the skeleton
SCAFFOLD gate can approach. Every progress report from Round 0 on states the score as
"X% of achievable" = scaffold mean / ceiling, beside the raw number.

TWO REFINEMENTS, both reported side by side so nothing is hidden:
  * SCAFFOLD scope vs FULL scope — blocks inside a WIDGET subtree (the same WIDGET_MARKERS
    the skeleton collapses) are excluded from the SCAFFOLD figure, because the PRIMARY gate
    never sees them; the FULL figure keeps them (it pairs with the skeleton's RAW number).
  * BOILERPLATE — a no-source text that recurs in >= BOILER_MIN_MODULES distinct modules'
    gold ("We are learning:", "Go to dropbox", the kaiako-contact copy…) is a CONVENTION a
    rule CAN emit (the KB documents most of them), so it is NOT part of the ceiling. The
    "net" share removes it; the "raw" share keeps it. The top boilerplate strings are
    listed so the split is inspectable.

POPULATIONS: every gold module dir that has a parsed WT (454 minus the WT-less). The HEADLINE
is the PAIRED population — the gold pages the skeleton gate actually scores (pairs() from
_discrepancy_audit, acks/glossary/references pages excluded exactly as _skeleton_compare
does) — so the ceiling is apples-to-apples with the round-313 baseline. compare_set
membership and the KB template family are carried as flags for grouping.

GROUPING (§1b template awareness): template folder (Standard/Bilingual/Fundamentals/Inquiry),
HTML sub-type (template= attr + body class per KB 06_TEMPLATE_RECOGNITION), Legacy vs Refresh
(level="prm" / #container), subject + series (Module_Structure_Index.json module_meta), and a
KB-family heuristic by code prefix (14_SUBJECT_GLOBAL_PARAMETERS families).

OUTLIERS (§1b): the paired pages with the highest net no-source share are listed with samples
of their unsourced text, so a page that will never score well is visible, not mysterious.

Text normalisation is Unicode-aware (macrons and CJK survive; punctuation and markdown
emphasis are deleted without inserting spaces, so `M**ā**ori` == `Māori`) — a strict
improvement on anchor_compare.norm, which is ASCII-only; the matcher's tolerance logic is
reused verbatim.

USAGE (paths are dynamic — CLAUDE.md §13; run from anywhere):
  python3 _measure_ceiling.py                       # full corpus → _ceiling_r0.json + _ceiling_r0.md
  python3 _measure_ceiling.py CODE [CODE …]         # scoped (writes nothing unless --json/--md given)
  python3 _measure_ceiling.py --json OUT --md OUT   # explicit output paths
  python3 _measure_ceiling.py --selftest            # LIVENESS + DETECTION (r149 discipline)
"""
import os, sys, re, json, time
from html.parser import HTMLParser
from collections import defaultdict, Counter

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(BASE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)
import _corpus                                   # nesting-aware corpus paths (round 128)
from anchor_compare import _phrase_present       # THE round-110 tolerance, reused verbatim
from _discrepancy_audit import pairs             # THE gate's page pairing (content first, numeric fallback)
from _structural_skeleton import WIDGET_MARKERS, DROP, VOID

HUMAN = os.path.join(ROOT, "01-Finalized_Modules_")
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
DATA = os.path.join(ROOT, "CONVERTER_V2", "data")
COMPARE_SET = os.path.join(TESTS, "compare_set.txt")
DEFAULT_BASELINE = os.path.join(BASE, "_r313_sk_final.json")
DEFAULT_JSON = os.path.join(BASE, "_ceiling_r0.json")
DEFAULT_MD = os.path.join(BASE, "_ceiling_r0.md")

BLOCK_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "blockquote",
              "figcaption", "caption", "dt", "dd", "label", "summary", "legend", "pre"}
NOTE_CLS = {"cv2-note", "cv2-comment"}          # converter notes — never in gold, skipped for parity
BOILER_MIN_MODULES = 5                          # scaffold_sig MIN_MODULES — a convention needs 5 modules
SKIP_PAGE = re.compile(r"acks|acknowledge|glossary|references", re.I)   # _skeleton_compare's page filter
RED_MARK = re.compile(r"\U0001f534\[RED TEXT\]|\[/RED TEXT\]\U0001f534")
_WS = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\s]|_")

# KB 14_SUBJECT_GLOBAL_PARAMETERS families, by code prefix (HEURISTIC — grouping only)
KB_FAMILY = [
    (re.compile(r"^BLLR"), "BLLR (14.9)"), (re.compile(r"^BLL"), "BLL (14.7)"),
    (re.compile(r"^WJ"), "MiW/WJ (14.10)"), (re.compile(r"^(HPFUN|PHEFUN)"), "H&PE FUNdamentals (14.5)"),
    (re.compile(r"^(HPRE|HPE)"), "HPE content (14.8)"), (re.compile(r"^(XLP|XDLS|LS)"), "LS (14.6)"),
    (re.compile(r"^X"), "X-prefixed other (learningSupport)"),
    (re.compile(r"^(CHFUN|JPNFUN|JAPFUN|CHIFUN|GE|FR|SPA|SAM|JPN|CH)"), "Languages (14.1)"),
    (re.compile(r"^PW"), "Pathways (14.2)"), (re.compile(r"^(ART|ARFUN)"), "Taonga/Arts (14.3)"),
    (re.compile(r"^CED"), "CED (14.4)"), (re.compile(r"^(TEFUN|TECH)"), "Technology (14.12)"),
]


def kb_family(code):
    for rx, name in KB_FAMILY:
        if rx.match(code):
            return name
    return "no KB family"


def unorm(t):
    """Unicode-aware fold: lowercase, apostrophes + ALL punctuation + markdown marks DELETED
    (no space inserted, so `M**ā**ori` == `Māori`, `N**ew* *Z**ealand*` == `New Zealand`),
    whitespace collapsed. Macrons and CJK survive (anchor_compare.norm strips them)."""
    t = (t or "").replace("\xa0", " ").lower()
    t = t.replace("’", "").replace("‘", "").replace("'", "")
    t = _PUNCT.sub("", t)
    return _WS.sub(" ", t).strip()


def has_source(norm, blob):
    """The round-110 tolerance (verbatim / 6-word head / 3-word window with a >=6-char word),
    with ONE guard: a 1-2 word block must match on WORD BOUNDARIES (a bare substring test
    would find 'know' inside 'knowledge')."""
    if not norm:
        return False
    if len(norm.split()) <= 2:
        return (" " + norm + " ") in blob
    return _phrase_present(norm, blob)


def has_source_loose(norm, words):
    """The LOOSE upper bound: every content word (>= 4 chars) of the block occurs somewhere in
    the WT as a whole word. Catches short rewordings the round-110 test refuses ("Type of
    farming" vs the writer's "Farming type"); over-generous on generic prose. Reported as the
    other end of a band — never the headline."""
    cw = [w for w in norm.split() if len(w) >= 4]
    if not cw:
        return False
    return all(w in words for w in cw)


WT_TAG = re.compile(r"\[\s*(H[1-6]|body|title bar|activity|lesson|image|alert|button)\b", re.I)


def wt_blob(code):
    """The module's whole parsed input — the UNION of every `*_parsed.txt` in the gold dir
    (Writers Template, Media List, or the combined 'Writers Template + Media List' file) —
    folded, space-padded, plus its whole-word set and a usability verdict.

    THE ROUND-0 TRAP (caught by block-level validation): 151 modules carry TWO parsed files,
    and `<CODE> Media List_parsed.txt` sorts BEFORE `<CODE> Writers Template_parsed.txt`, so a
    'first file' read scores the whole module against the wrong document (CHFUN01, PNR102,
    CEDO501 … all read as ~100% unsourced). Reading the union is right anyway: a caption in
    the Media List IS writer input a rule can read. `usable` is False when NO parsed file
    looks like a Writers Template (fewer than 3 structural tags) — such a module has no
    measurable source and is EXCLUDED from the ceiling populations and listed.
    Returns (blob, words, usable, n_files) or None when the module has no parsed txt at all.
    (anchor_compare.wt_items has the same first-file read — noted for a later repair.)"""
    d = _corpus.mdir(HUMAN, code)
    if not os.path.isdir(d):
        return None
    pf = sorted(f for f in os.listdir(d) if f.endswith("_parsed.txt"))
    if not pf:
        return None
    texts, usable = [], False
    for f in pf:
        txt = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
        if len(WT_TAG.findall(txt)) >= 3:
            usable = True
        texts.append(RED_MARK.sub(" ", txt))
    blob = " " + unorm("\n".join(texts)) + " "
    return blob, set(blob.split()), usable, len(pf)


class Blocks(HTMLParser):
    """Collect every text-bearing block of a page with its widget/region context. A block's
    text is its own inline content; a nested block (li > p) owns its own text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.blocks = []
        self.skip = 0

    def _ctx(self):
        return self.stack[-1] if self.stack else {"widget": False, "region": None, "note": False}

    def handle_starttag(self, tag, attrs):
        if self.skip:
            if tag not in VOID:
                self.skip += 1
            return
        if tag in DROP:
            if tag not in VOID:
                self.skip = 1
            return
        if tag == "br":
            self._text(" ")
            return
        a = dict(attrs)
        cls = set((a.get("class") or "").split())
        eid = a.get("id") or ""
        p = self._ctx()
        note = p["note"] or bool(cls & NOTE_CLS)
        widget = p["widget"] or bool(cls & WIDGET_MARKERS)
        region = p["region"]
        if eid in ("header", "body", "footer"):
            region = eid
        elif "acks" in cls:
            region = "acks"
        if tag in VOID:
            return
        frame = {"tag": tag, "widget": widget, "region": region, "note": note, "block": None}
        if tag in BLOCK_TAGS and not note:
            self.blocks.append({"tag": tag, "parts": [], "in_widget": widget, "region": region})
            frame["block"] = len(self.blocks) - 1
        self.stack.append(frame)

    def handle_startendtag(self, tag, attrs):
        if tag == "br" and not self.skip:
            self._text(" ")

    def handle_endtag(self, tag):
        if self.skip:
            self.skip -= 1
            return
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not self.skip:
            self._text(data)

    def _text(self, s):
        for f in reversed(self.stack):
            if f["block"] is not None:
                self.blocks[f["block"]]["parts"].append(s)
                return


def page_blocks(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"<body\b[^>]*>(.*)</body>", raw, re.S | re.I)
    src = m.group(0) if m else raw
    p = Blocks()
    p.feed(src)
    out = []
    for b in p.blocks:
        t = _WS.sub(" ", "".join(b["parts"])).strip()
        n = unorm(t)
        if not n or not re.search(r"\w", n):
            continue
        out.append({"tag": b["tag"], "text": t[:200], "norm": n,
                    "in_widget": b["in_widget"], "region": b["region"]})
    head = raw[:4000]
    tm = re.search(r"<html\b[^>]*\btemplate=\"([^\"]*)\"", head, re.I)
    bm = re.search(r"<body\b[^>]*\bclass=\"([^\"]*)\"", raw, re.I)
    legacy = bool(re.search(r"<html\b[^>]*\blevel=\"pr(m|inq)\"", head, re.I)) or 'id="container"' in raw
    bcls = set((bm.group(1) if bm else "").split())
    tattr = tm.group(1) if tm else ""
    if "reoTranslate" in bcls:
        sub = "Bilingual"
    elif "fundamentals" in bcls:
        sub = "Fundamentals"
    elif "inquiry" in bcls:
        sub = "Inquiry"
    elif tattr == "combo":
        sub = "Combo"
    else:
        sub = "Standard"
    return out, {"legacy": legacy, "template_attr": tattr, "subtype": sub, "has_body": bool(m)}


def load_meta():
    try:
        d = json.load(open(os.path.join(DATA, "Module_Structure_Index.json"), encoding="utf-8"))
        return d.get("module_meta", {})
    except Exception:
        return {}


def load_compare_set():
    try:
        return {c.strip() for c in open(COMPARE_SET, encoding="utf-8") if c.strip()}
    except Exception:
        return set()


def template_dir(code):
    d = _corpus.mdir(HUMAN, code)
    parent = os.path.basename(os.path.dirname(d))
    return parent if parent in _corpus.TEMPLATE_DIRS else "flat"


def measure(codes, min_boiler=BOILER_MIN_MODULES, quiet=False):
    meta = load_meta()
    cset = load_compare_set()
    pages, no_wt, no_claude, unusable_wt = [], [], [], []
    multi_parsed = 0
    text_modules = defaultdict(set)
    t0 = time.time()
    for i, code in enumerate(codes):
        hdir = _corpus.mdir(HUMAN, code)
        if not os.path.isdir(hdir):
            continue
        wb = wt_blob(code)
        if wb is None:
            no_wt.append(code)
            continue
        blob, words, usable, n_files = wb
        if n_files > 1:
            multi_parsed += 1
        if not usable:
            unusable_wt.append(code)
            continue
        cdir = _corpus.mdir(CLAUDE, code)
        has_claude = os.path.isdir(cdir)
        if not has_claude:
            no_claude.append(code)
        paired = {}
        if has_claude:
            for _, cp, hp in pairs(code):
                hb, cb = os.path.basename(hp), os.path.basename(cp)
                if SKIP_PAGE.search(hb) or SKIP_PAGE.search(cb):
                    continue
                paired[hb] = cb
        mm = meta.get(code, {})
        tdir = template_dir(code)
        for f in sorted(x for x in os.listdir(hdir) if x.lower().endswith(".html")):
            if SKIP_PAGE.search(f):
                continue
            blocks, pm = page_blocks(os.path.join(hdir, f))
            for b in blocks:
                b["src"] = has_source(b["norm"], blob)
                b["src_loose"] = b["src"] or has_source_loose(b["norm"], words)
                if not b["src"]:
                    text_modules[b["norm"]].add(code)
            pages.append({"module": code, "page": f, "template_dir": tdir, "subtype": pm["subtype"],
                          "template_attr": pm["template_attr"], "legacy": pm["legacy"],
                          "subject": str(mm.get("subject")), "series": str(mm.get("series")),
                          "prefix": str(mm.get("prefix") or re.match(r"[A-Z]+", code).group(0)),
                          "kb_family": kb_family(code), "in_compare_set": code in cset,
                          "has_claude_dir": has_claude, "paired": f in paired,
                          "claude_page": paired.get(f), "_blocks": blocks})
        if not quiet and (i + 1) % 25 == 0:
            print(f"  … {i + 1}/{len(codes)} modules, {len(pages)} pages, {time.time() - t0:.0f}s",
                  file=sys.stderr, flush=True)
    boiler = {t for t, ms in text_modules.items() if len(ms) >= min_boiler}
    for r in pages:
        bl = r.pop("_blocks")
        sc = [b for b in bl if not b["in_widget"]]
        ns_all = [b for b in bl if not b["src"]]
        ns_sc = [b for b in sc if not b["src"]]
        net_sc = [b for b in ns_sc if b["norm"] not in boiler]
        net_all = [b for b in ns_all if b["norm"] not in boiler]
        loose_sc = [b for b in net_sc if not b["src_loose"]]
        loose_all = [b for b in net_all if not b["src_loose"]]
        r.update({
            "blocks_full": len(bl), "blocks_scaffold": len(sc),
            "nosrc_full_raw": len(ns_all), "nosrc_scaffold_raw": len(ns_sc),
            "nosrc_full_net": len(net_all), "nosrc_scaffold_net": len(net_sc),
            "nosrc_full_loose": len(loose_all), "nosrc_scaffold_loose": len(loose_sc),
            "boiler_scaffold": len(ns_sc) - len(net_sc),
            "share_scaffold_raw": (len(ns_sc) / len(sc)) if sc else None,
            "share_scaffold_net": (len(net_sc) / len(sc)) if sc else None,
            "share_scaffold_loose": (len(loose_sc) / len(sc)) if sc else None,
            "share_full_raw": (len(ns_all) / len(bl)) if bl else None,
            "share_full_net": (len(net_all) / len(bl)) if bl else None,
            "share_full_loose": (len(loose_all) / len(bl)) if bl else None,
            "samples": [f"<{b['tag']}> {b['text'][:110]}" for b in net_sc[:5]],
            "boiler_samples": [f"<{b['tag']}> {b['text'][:60]}" for b in ns_sc if b["norm"] in boiler][:3],
        })
    boiler_rows = sorted(((len(ms), t) for t, ms in text_modules.items() if t in boiler), reverse=True)
    return pages, boiler_rows, no_wt, no_claude, unusable_wt, multi_parsed


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return (sum(xs) / len(xs)) if xs else None


def summarise(rows):
    sc_rows = [r for r in rows if r["blocks_scaffold"]]
    out = {"pages": len(rows), "modules": len({r["module"] for r in rows}),
           "blocks_scaffold": sum(r["blocks_scaffold"] for r in rows),
           "blocks_full": sum(r["blocks_full"] for r in rows),
           "mean_share_scaffold_raw": _mean([r["share_scaffold_raw"] for r in sc_rows]),
           "mean_share_scaffold_net": _mean([r["share_scaffold_net"] for r in sc_rows]),
           "mean_share_scaffold_loose": _mean([r["share_scaffold_loose"] for r in sc_rows]),
           "mean_share_full_raw": _mean([r["share_full_raw"] for r in rows]),
           "mean_share_full_net": _mean([r["share_full_net"] for r in rows]),
           "mean_share_full_loose": _mean([r["share_full_loose"] for r in rows])}
    bs = out["blocks_scaffold"] or 1
    bf = out["blocks_full"] or 1
    out["pooled_share_scaffold_raw"] = sum(r["nosrc_scaffold_raw"] for r in rows) / bs
    out["pooled_share_scaffold_net"] = sum(r["nosrc_scaffold_net"] for r in rows) / bs
    out["pooled_share_scaffold_loose"] = sum(r["nosrc_scaffold_loose"] for r in rows) / bs
    out["pooled_share_full_raw"] = sum(r["nosrc_full_raw"] for r in rows) / bf
    out["pooled_share_full_net"] = sum(r["nosrc_full_net"] for r in rows) / bf
    out["pooled_share_full_loose"] = sum(r["nosrc_full_loose"] for r in rows) / bf
    m = out["mean_share_scaffold_net"]
    out["ceiling_scaffold"] = (1 - m) if m is not None else None
    ml = out["mean_share_scaffold_loose"]
    out["ceiling_scaffold_loose"] = (1 - ml) if ml is not None else None
    mf = out["mean_share_full_net"]
    out["ceiling_full"] = (1 - mf) if mf is not None else None
    mfl = out["mean_share_full_loose"]
    out["ceiling_full_loose"] = (1 - mfl) if mfl is not None else None
    return out


def group_by(rows, key):
    g = defaultdict(list)
    for r in rows:
        g[str(r[key])].append(r)
    return {k: summarise(v) for k, v in sorted(g.items(), key=lambda kv: -len(kv[1]))}


def load_baseline(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
        pp = d["per_page"]
        return {"path": path, "pages": len(pp),
                "scaffold_mean": sum(p["scaffold"] for p in pp) / len(pp),
                "raw_mean": sum(p["raw"] for p in pp) / len(pp),
                "by_claude_page": {p["page"]: p for p in pp}}
    except Exception as e:
        return {"path": path, "error": f"{type(e).__name__}: {e}"}


def pct(x, nd=1):
    return "—" if x is None else f"{100 * x:.{nd}f}%"


def build_report(pages, boiler_rows, no_wt, no_claude, baseline, codes_requested, unusable_wt=(), multi_parsed=0):
    paired = [r for r in pages if r["paired"]]
    cs_paired = [r for r in paired if r["in_compare_set"]]
    summary = {"all_gold_pages": summarise(pages), "paired": summarise(paired),
               "compare_set_paired": summarise(cs_paired)}
    achievable = {}
    if baseline and "scaffold_mean" in baseline:
        ceil = summary["paired"]["ceiling_scaffold"]
        ceil_l = summary["paired"]["ceiling_scaffold_loose"]
        ceil_f = summary["paired"]["ceiling_full"]
        ceil_fl = summary["paired"]["ceiling_full_loose"]
        achievable = {"baseline": os.path.basename(baseline["path"]), "baseline_pages": baseline["pages"],
                      "scaffold_mean": baseline["scaffold_mean"], "raw_mean": baseline["raw_mean"],
                      "ceiling_scaffold": ceil, "ceiling_scaffold_loose": ceil_l,
                      "ceiling_full": ceil_f, "ceiling_full_loose": ceil_fl,
                      "scaffold_of_achievable": (baseline["scaffold_mean"] / ceil) if ceil else None,
                      "scaffold_of_achievable_loose": (baseline["scaffold_mean"] / ceil_l) if ceil_l else None,
                      "raw_of_achievable": (baseline["raw_mean"] / ceil_f) if ceil_f else None,
                      "raw_of_achievable_loose": (baseline["raw_mean"] / ceil_fl) if ceil_fl else None}
        # per-page join: each paired page's own score against its own ceiling
        ratios = []
        for r in paired:
            sk = baseline["by_claude_page"].get(r["claude_page"])
            if sk and r["share_scaffold_net"] is not None:
                c = 1 - r["share_scaffold_net"]
                if c >= 0.05:
                    ratios.append(min(1.0, sk["scaffold"] / c))
                    r["scaffold_score"] = sk["scaffold"]
                    r["scaffold_of_achievable"] = min(1.0, sk["scaffold"] / c)
        achievable["per_page_mean_of_achievable"] = _mean(ratios)
        achievable["per_page_joined"] = len(ratios)
    groups = {k: group_by(paired, k) for k in ("template_dir", "subtype", "legacy", "kb_family", "subject", "prefix")}
    outliers = sorted([r for r in paired if r["share_scaffold_net"] is not None
                       and r["share_scaffold_net"] >= 0.5 and r["blocks_scaffold"] >= 8],
                      key=lambda r: (-r["share_scaffold_net"], -r["blocks_scaffold"]))
    per_mod = defaultdict(list)
    for r in paired:
        if r["share_scaffold_net"] is not None:
            per_mod[r["module"]].append(r["share_scaffold_net"])
    worst_modules = sorted(((_mean(v), k, len(v)) for k, v in per_mod.items()), reverse=True)
    return {"meta": {"tool": "_measure_ceiling.py", "round": 0, "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
                     "modules_requested": len(codes_requested), "modules_measured": len({r["module"] for r in pages}),
                     "modules_without_wt": no_wt, "modules_without_claude_dir": no_claude,
                     "modules_unusable_wt": list(unusable_wt), "modules_with_multiple_parsed_files": multi_parsed,
                     "boiler_min_modules": BOILER_MIN_MODULES,
                     "method": "block has a WT source if anchor_compare._phrase_present (round-110 tolerance) "
                               "finds it in the UNION of the module's folded parsed files (WT + Media List); "
                               "1-2 word blocks need a word-boundary match; SCAFFOLD scope excludes WIDGET_MARKERS "
                               "subtrees; NET removes boilerplate (no-source texts recurring in >= boiler_min_modules "
                               "modules); LOOSE = every >=4-char word of the block present in the WT (upper bound)"},
            "summary": summary, "achievable": achievable, "groups": groups,
            "boilerplate_top": [{"modules": n, "text": t[:120]} for n, t in boiler_rows[:200]],
            "boilerplate_count": len(boiler_rows),
            "outliers": [{k: r[k] for k in ("module", "page", "template_dir", "subtype", "kb_family", "subject",
                                             "blocks_scaffold", "nosrc_scaffold_net", "share_scaffold_net",
                                             "scaffold_score", "samples") if k in r} for r in outliers],
            "worst_modules": [{"module": k, "pages": n, "mean_share_scaffold_net": m} for m, k, n in worst_modules[:40]],
            "pages": pages}


def write_md(rep, path):
    s = rep["summary"]
    a = rep["achievable"]
    L = []
    L.append("# Round 0 — THE CEILING (what no converter rule can ever close)\n")
    L.append(f"Generated {rep['meta']['generated']} by `outputs/_measure_ceiling.py`. "
             f"Modules measured {rep['meta']['modules_measured']} / requested {rep['meta']['modules_requested']}; "
             f"without a parsed WT (skipped): {', '.join(rep['meta']['modules_without_wt']) or 'none'}; "
             f"parsed files present but none looks like a Writers Template (skipped): "
             f"{', '.join(rep['meta'].get('modules_unusable_wt', [])) or 'none'}; "
             f"modules read from the UNION of {rep['meta'].get('modules_with_multiple_parsed_files', 0)}×2+ parsed files; "
             f"gold-only (no Claude dir, never paired): {len(rep['meta']['modules_without_claude_dir'])}.\n")
    L.append("**Plain English.** A *block* is one piece of text on the human's finished page (a heading, a paragraph, "
             "a bullet, a table cell). A block has a *source* when the same words — or a distinctive run of them — "
             "appear anywhere in the writer's template. Blocks with **no source** were written by the developer "
             "(verbal feedback, house copy): no rule that reads the template can produce them. **Boilerplate** is "
             "no-source text that recurs across many modules (a convention a rule CAN emit), so the honest ceiling "
             "removes it (**net**). *Scaffold scope* ignores text inside interactive widgets, because the primary "
             "skeleton gate ignores widget internals too.\n")
    L.append("## Headline (the PAIRED population — the pages the skeleton gate scores)\n")
    p = s["paired"]
    L.append(f"- pages {p['pages']} / modules {p['modules']} / text blocks (scaffold scope) {p['blocks_scaffold']}")
    L.append(f"- no-source share, scaffold scope: per-page mean **raw {pct(p['mean_share_scaffold_raw'])} → net {pct(p['mean_share_scaffold_net'])}** "
             f"(pooled raw {pct(p['pooled_share_scaffold_raw'])} → net {pct(p['pooled_share_scaffold_net'])})")
    L.append(f"- no-source share, full scope (widget internals included): per-page mean raw {pct(p['mean_share_full_raw'])} → net {pct(p['mean_share_full_net'])}")
    L.append(f"- **CEILING (scaffold) = {pct(p['ceiling_scaffold'])}** (round-110 test) — loose upper bound {pct(p['ceiling_scaffold_loose'])} "
             f"(every content word of the block found somewhere in the WT) · ceiling (full) = {pct(p['ceiling_full'])} / loose {pct(p['ceiling_full_loose'])}")
    if a:
        L.append(f"- baseline `{a['baseline']}` ({a['baseline_pages']} pairs): SCAFFOLD mean {pct(a['scaffold_mean'], 3)} / RAW mean {pct(a['raw_mean'], 3)}")
        L.append(f"- **SCAFFOLD {pct(a['scaffold_mean'], 2)} = {pct(a['scaffold_of_achievable'])} of achievable** "
                 f"(band {pct(a['scaffold_of_achievable_loose'])}–{pct(a['scaffold_of_achievable'])}: the loose ceiling gives the lower figure); "
                 f"RAW {pct(a['raw_mean'], 2)} = {pct(a['raw_of_achievable'])} of its own ceiling (band {pct(a['raw_of_achievable_loose'])}–{pct(a['raw_of_achievable'])}); "
                 f"per-page mean of (score ÷ own ceiling) = {pct(a['per_page_mean_of_achievable'])} over {a['per_page_joined']} joined pages")
    L.append("")
    L.append("| population | pages | modules | blocks (scaffold) | mean no-source raw | mean no-source NET | mean no-source LOOSE | ceiling (scaffold) | ceiling loose | mean full raw | mean full NET |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for k, lab in (("paired", "paired (gate population)"), ("compare_set_paired", "compare_set ∩ paired"), ("all_gold_pages", "ALL gold pages with a WT")):
        q = s[k]
        L.append(f"| {lab} | {q['pages']} | {q['modules']} | {q['blocks_scaffold']} | {pct(q['mean_share_scaffold_raw'])} | {pct(q['mean_share_scaffold_net'])} | {pct(q['mean_share_scaffold_loose'])} | {pct(q['ceiling_scaffold'])} | {pct(q['ceiling_scaffold_loose'])} | {pct(q['mean_share_full_raw'])} | {pct(q['mean_share_full_net'])} |")
    L.append("")
    for gk, title in (("template_dir", "Template family (folder)"), ("subtype", "HTML sub-type (KB 06)"),
                      ("legacy", "Legacy (True) vs Refresh (False)"), ("kb_family", "KB subject family (14.x, prefix heuristic)"),
                      ("subject", "Subject (Module_Structure_Index)"), ("prefix", "Series prefix")):
        L.append(f"## By {title} — paired population\n")
        L.append("| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for g, q in rep["groups"][gk].items():
            L.append(f"| {g} | {q['pages']} | {q['modules']} | {pct(q['mean_share_scaffold_raw'])} | {pct(q['mean_share_scaffold_net'])} | {pct(q['mean_share_scaffold_loose'])} | {pct(q['ceiling_scaffold'])} | {pct(q['ceiling_scaffold_loose'])} | {pct(q['pooled_share_scaffold_net'])} |")
        L.append("")
    L.append(f"## Boilerplate — no-source text recurring in ≥ {rep['meta']['boiler_min_modules']} modules ({rep['boilerplate_count']} strings; top 60)\n")
    L.append("These are conventions a rule can emit (most are documented in the KB); they are removed from the NET figures.\n")
    L.append("| modules | text |")
    L.append("|---|---|")
    for b in rep["boilerplate_top"][:60]:
        L.append(f"| {b['modules']} | {b['text'].replace('|', '¦')} |")
    L.append("")
    L.append(f"## Outlier pages — paired pages whose NET no-source share ≥ 50% with ≥ 8 blocks ({len(rep['outliers'])} pages; top 60)\n")
    L.append("These pages will score low against gold no matter what the converter does; the samples show the developer-authored text.\n")
    L.append("| page | family | sub-type | KB family | blocks | no-source (net) | share | skeleton score | samples of unsourced text |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for o in rep["outliers"][:60]:
        smp = " ¦ ".join(x.replace("|", "¦") for x in o["samples"][:3])
        L.append(f"| {o['page']} | {o['template_dir']} | {o['subtype']} | {o['kb_family']} | {o['blocks_scaffold']} | {o['nosrc_scaffold_net']} | {pct(o['share_scaffold_net'])} | {pct(o.get('scaffold_score'))} | {smp} |")
    L.append("")
    L.append("## Worst modules by mean NET no-source share (paired pages; top 40)\n")
    L.append("| module | pages | mean NET no-source share |")
    L.append("|---|---|---|")
    for w in rep["worst_modules"]:
        L.append(f"| {w['module']} | {w['pages']} | {pct(w['mean_share_scaffold_net'])} |")
    L.append("")
    open(path, "w", encoding="utf-8").write("\n".join(L))


def selftest():
    import tempfile
    html = ('<html lang="en" level="" template="1-3"><head><title>x</title><script>var a="<p>no</p>";</script></head>'
            '<body class="container-fluid"><div id="header"><h1><span>Kai and place</span></h1></div>'
            '<div id="body"><div class="row"><div class="col-md-8 col-12">'
            '<h3>Where does my kai come from?</h3>'
            '<p>In short, agriculture and horticulture connect people to places.</p>'
            '<p>The developer wrote this brand new sentence about invisible unicorns.</p>'
            '<ul><li><p>Understand purpose and place of production.</p></li><li>Know:</li></ul>'
            '<div class="accordion"><div class="accHead"><h4>Inside a widget panel heading</h4></div></div>'
            '<p class="cv2-note">Writers Note: this must be skipped</p>'
            '<table><tr><th>Type of farming</th><td>M&#257;ori</td></tr></table>'
            '</div></div></div><div id="footer"><ul class="footer-nav"><li><a href=""></a></li></ul></div></body></html>')
    wt = ("MODULE METADATA\n\U0001f534[RED TEXT] [TITLE BAR] [/RED TEXT]\U0001f534__***Kai and place***__ *|* Ka ahu\n"
          "\U0001f534[RED TEXT] [H3] [/RED TEXT]\U0001f534 Where does my kai come from?\n"
          "[Body] *Agriculture and horticulture connect people to locations of purposeful production.*\n"
          "• *Understand purpose and place of production is influenced.*\n[H2] **Know:**\n M**ā**ori settlement\n"
          "Farming type\n")
    with tempfile.TemporaryDirectory() as td:
        hp = os.path.join(td, "T1.00.html")
        open(hp, "w", encoding="utf-8").write(html)
        blocks, pm = page_blocks(hp)
        blob = " " + unorm(RED_MARK.sub(" ", wt)) + " "
        words = set(blob.split())
        texts = {b["norm"]: b for b in blocks}
        assert not has_source("type of farming", blob) and has_source_loose("type of farming", words), \
            "the short reworded block is NO SOURCE under round-110 but SOURCED under the loose bound"
        assert not has_source_loose("the developer wrote this brand new sentence about invisible unicorns", words), \
            "the loose bound must still reject genuinely new text"
        assert len(blocks) >= 6, f"LIVENESS: expected >= 6 blocks, got {len(blocks)}"
        assert pm["subtype"] == "Standard" and pm["template_attr"] == "1-3" and not pm["legacy"]
        assert "writers note this must be skipped" not in texts, "cv2-note must be excluded"
        assert "no" not in texts, "script content must be dropped"
        w = texts["inside a widget panel heading"]
        assert w["in_widget"], "a block inside .accordion must be in_widget"
        assert texts["kai and place"]["region"] == "header"
        assert has_source("kai and place", blob), "verbatim title must match"
        assert has_source(texts["in short agriculture and horticulture connect people to places"]["norm"], blob), \
            "REWORDED sentence with a distinctive 3-word run must match (round-110 tolerance)"
        assert not has_source(texts["the developer wrote this brand new sentence about invisible unicorns"]["norm"], blob), \
            "DETECTION: a developer-authored sentence must be NO SOURCE"
        assert has_source("know", blob) and not has_source("knowledge", blob), "1-2 word blocks match on word boundaries"
        assert unorm("M**ā**ori") == "māori" == unorm("Māori"), unorm("M**ā**ori")
        assert unorm("N**ew* *Z**ealand*") == "new zealand"
        assert has_source(texts["māori"]["norm"], blob), "macron text must survive the fold and match"
        assert unorm("要/会 comparison") == "要会 comparison", "CJK must survive the fold"
        # the round-0 trap: a module with TWO parsed files must be read as their UNION, and a
        # dir holding only a Media List is UNUSABLE (no Writers Template to source from)
        md = os.path.join(td, "M1")
        os.makedirs(md)
        open(os.path.join(md, "M1 Media List_parsed.txt"), "w", encoding="utf-8").write(
            "MEDIA LIST TEMPLATE\nUse this media list template\nItem 1 photo of a tractor\n")
        open(os.path.join(md, "M1 Writers Template_parsed.txt"), "w", encoding="utf-8").write(wt)
        _orig = _corpus.mdir
        _corpus.mdir = lambda root, *parts: md if parts and parts[0] == "M1" else _orig(root, *parts)
        try:
            b2, w2, usable2, n2 = wt_blob("M1")
            assert n2 == 2 and usable2, "two parsed files, the WT one makes the module usable"
            assert has_source("kai and place", b2) and " tractor " in b2, "the UNION carries both files"
            os.remove(os.path.join(md, "M1 Writers Template_parsed.txt"))
            b3, w3, usable3, n3 = wt_blob("M1")
            assert n3 == 1 and not usable3, "a Media-List-only dir is UNUSABLE, never scored as 100% unsourced"
        finally:
            _corpus.mdir = _orig
        # boilerplate: a no-source text seen in >= BOILER_MIN_MODULES modules is a convention
        tm = defaultdict(set)
        for i in range(BOILER_MIN_MODULES):
            tm["we are learning"].add(f"M{i}")
        tm["unique developer copy"].add("M0")
        boiler = {t for t, ms in tm.items() if len(ms) >= BOILER_MIN_MODULES}
        assert boiler == {"we are learning"}, boiler
    print("LIVENESS ok — blocks extracted, header/body/widget/note context correct")
    print("DETECTION ok — reworded text matches, developer-authored text is NO SOURCE, boilerplate splits")
    print("SELFTEST PASS")


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        selftest()
        return
    codes, i, json_out, md_out, baseline_path, no_write = [], 0, None, None, DEFAULT_BASELINE, False
    while i < len(args):
        a = args[i]
        if a == "--json":
            json_out = args[i + 1]; i += 2; continue
        if a == "--md":
            md_out = args[i + 1]; i += 2; continue
        if a == "--baseline":
            baseline_path = args[i + 1]; i += 2; continue
        if a == "--no-write":
            no_write = True; i += 1; continue
        if a.startswith("-"):
            i += 1; continue
        codes.append(a); i += 1
    if not codes:
        codes = _corpus.mods(HUMAN)
        json_out = json_out or DEFAULT_JSON
        md_out = md_out or DEFAULT_MD
    t0 = time.time()
    pages, boiler_rows, no_wt, no_claude, unusable_wt, multi_parsed = measure(codes)
    baseline = load_baseline(baseline_path) if baseline_path else None
    rep = build_report(pages, boiler_rows, no_wt, no_claude, baseline, codes, unusable_wt, multi_parsed)
    s = rep["summary"]["paired"]
    a = rep["achievable"]
    print(f"CEILING (round 0) — {rep['meta']['modules_measured']} modules, {len(pages)} gold pages, "
          f"{s['pages']} paired ({time.time() - t0:.0f}s); {multi_parsed} modules read from 2+ parsed files")
    print(f"  no WT (skipped): {', '.join(no_wt) or 'none'}; no WT-like parsed file (skipped): {', '.join(unusable_wt) or 'none'}")
    print(f"  PAIRED scaffold-scope no-source share: mean raw {pct(s['mean_share_scaffold_raw'])} → NET {pct(s['mean_share_scaffold_net'])}; "
          f"pooled raw {pct(s['pooled_share_scaffold_raw'])} → NET {pct(s['pooled_share_scaffold_net'])}")
    print(f"  CEILING scaffold {pct(s['ceiling_scaffold'])} (loose {pct(s['ceiling_scaffold_loose'])}) / full {pct(s['ceiling_full'])} "
          f"(loose {pct(s['ceiling_full_loose'])}); boilerplate strings {rep['boilerplate_count']}")
    if a and a.get("scaffold_of_achievable") is not None:
        print(f"  BASELINE {a['baseline']}: SCAFFOLD {pct(a['scaffold_mean'], 3)} = {pct(a['scaffold_of_achievable'])} of achievable "
              f"(band {pct(a['scaffold_of_achievable_loose'])}–{pct(a['scaffold_of_achievable'])}); "
              f"RAW {pct(a['raw_mean'], 3)} = {pct(a['raw_of_achievable'])} of achievable; per-page mean {pct(a['per_page_mean_of_achievable'])}")
    print(f"  outlier pages (net ≥ 50%, ≥ 8 blocks): {len(rep['outliers'])}")
    if not no_write:
        if json_out:
            json.dump(rep, open(json_out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            print(f"  wrote {json_out}")
        if md_out:
            write_md(rep, md_out)
            print(f"  wrote {md_out}")


if __name__ == "__main__":
    main()
