#!/usr/bin/env python3
"""anchor_compare.py — the triangulated comparison harness.

CONSOLIDATES full_compare.py (element model + matcher + diff), _wt_human_align.py
(WT-tag anchor) and menu_gate.cjs (menu populated/empty) into one diagnostic tool.
Spec: reference/Comparison_Harness_Design_Spec.md.

Per human<->Claude page pair:
  0 PAIR pages          content-fingerprint (heading words) Jaccard, positional fallback
  1 EXTRACT elements    region (header/menu/body/footer/acks) + FULL ancestor bundle + text
  2 MATCH content       exact -> first-tokens -> token-Jaccard, banded (high/uncertain)
  3 ANCHOR to WT        fuzzy-locate the human text in the parsed.txt -> governing [tag]
  3.5 TAG vs BUILT      does the tag's element TYPE match what the human BUILT?  if a
                        widget was swapped (e.g. [flip card] -> human carousel) -> SKIP (C)
  4 DIFF the bundle     strip content -> compare the row/col/callout/widget wrapper ladder
  6 REPORT              per-series rollup (default) + JSON

This is a DIAGNOSTIC, not a protected gate. It is allowed to be loose; its job is to
point you at the divergence and pre-sort bug vs editorial, not to pass/fail a build.

USAGE:
  python3 anchor_compare.py                  # per-series rollup over the whole corpus
  python3 anchor_compare.py CODE [CODE ...]  # those modules, page by page
  python3 anchor_compare.py --page CODE N    # full side-by-side for one page
  python3 anchor_compare.py --json OUT.json  # also dump every per-element record
  python3 anchor_compare.py --self CODE      # null test: human vs human (score must be ~0)

  --- the SAFETY NET (run after every converter change) -----------------------
  python3 anchor_compare.py --audit          # THE ONE COMMAND: coverage + regression + rule catalogue
  python3 anchor_compare.py --coverage       # whole-corpus records/pairing audit (0 silent drops; loud)
  python3 anchor_compare.py --coverage --json OUT.json   # + dump per-module coverage detail
  python3 anchor_compare.py --rules          # child->ancestor structural-rule catalogue (miner)
  python3 anchor_compare.py --rules2         # round-161 granularity catalogue (group/region/form/composition)
  python3 anchor_compare.py --regress        # the row.supervisor tool-regression check

COVERAGE never fails closed and silent (round 144): it lists every module that produces 0 records
or has pages that can't pair, and exits non-zero on a TOOL failure (a pairing bug / null-test
violation / regression miss) — a genuine DATA gap (Claude never built a module; the human side is an
acks-only stub) is reported loudly but does not trip the exit.
"""
import json
import _corpus  # round128: nesting-aware corpus paths
import os
import re
import sys
import difflib
import html as _html
from collections import Counter, defaultdict
from html.parser import HTMLParser
import scaffold_sig as ss            # WS2: the shared granular scaffold signature
import granular_consensus as gc      # WS2: reads data/Granular_Scaffold_Registry.json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..", "..", "..")
HUMAN = os.path.join(ROOT, "01-Finalized_Modules_")
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
DATA = os.path.join(BASE, "..", "..", "data")

# ---- tunable constants (decisions §9; calibrate via the precision probe) ------
MATCH_STRONG = 0.70      # token-Jaccard at/above this => a HIGH-confidence match
MATCH_WEAK = 0.45        # 0.45..0.70 => an UNCERTAIN match (shown, half-weighted)
WT_ANCHOR_MIN = 0.55     # min difflib ratio to accept a Writers-Template anchor
PAGE_PAIR_MIN = 0.20     # min heading-word Jaccard to pair two pages by content
CONSENSUS_FLOOR = 0.15     # a scaffold signature with >= this share is an ACCEPTED variant
CONSENSUS_COVERAGE = 0.60  # accepted variants must cover >= this share for a reliable consensus
CONSENSUS_MIN_N = 5        # min human instances before a tag has a reliable consensus
CONSENSUS_PATH = os.path.join(DATA, "Scaffold_Consensus.json")
# WS2 — GRANULAR CONSENSUS (default ON). The scaffold signature now carries the full
# row/col-width/wrapper ancestor ladder (scaffold_sig.granular_sig) and consensus_reading
# adjudicates a differing pair against the GRANULAR registry at the finest reliable grouping
# (series -> phase -> prefix -> subject -> corpus) instead of the flat, scaffold-blind
# Scaffold_Consensus. Set GRANULAR_SIG_OFF=1 to revert BOTH the signature and the reading to
# the legacy blind li@list behaviour (A/B reversal).
GRANULAR = os.environ.get("GRANULAR_SIG_OFF") != "1"
MACRO_WEIGHT = 1.0         # flat score added per SECTION-level (macro) divergence — these
                           # whole-chunk oversights must dominate the granular element diff
W = {"human_only": 3.0, "claude_only": 1.5, "wrapper_missing": 2.0, "wrapper_extra": 1.0,
     "width_diff": 1.0, "level_diff": 1.0, "tag_diff": 1.0, "nesting_diff": 1.0,
     "loop_broken": 2.0,
     # ancestor-class ladder diff (round-143.2 fix): a semantic class on one side's wrapper chain
     # that the other lacks (e.g. `row supervisor` vs `row`) — the child-dictates-ancestor signal.
     "wrapper_class_missing": 1.5, "wrapper_class_extra": 0.75,
     # Stage 4.7 (Chris, CEDO102) — the WT-DERIVABLE buckets. A human_only that the writer
     # TAGGED and the human FAITHFULLY built, but Claude dropped, is a high-confidence converter
     # BUG (not editorial) — weighted ABOVE a plain human_only so it floats to the top of triage.
     "wt_loss": 4.0, "tag_leak": 2.0}

REGIONS = {"header", "menu", "body", "footer", "acks"}

# --- acks-location exclusion (Chris, 2026-06-25) -------------------------------
# New modules place acknowledgements on the OVERVIEW page; previously-developed
# modules keep them on the final lesson page. That placement difference is EXPECTED
# policy, not a divergence — so by default the acks section is excluded from:
#   • Stage 0  page pairing            (sig_of: acks words don't influence the fingerprint)
#   • Stage 0.5 MACRO anatomy diff     (macro_diff: no acks_section finding)
#   • Stage 4  per-region content diff (compare_page: the acks region isn't compared)
# Set ACKSLOC_COMPARE=1 to restore the old behaviour (treat acks like any other region).
# NOTE: with the default, a fully-MISSING acks (absent on every page) is also no longer
# flagged — acks always exist somewhere under current policy, so this is acceptable.
COMPARE_ACKS = os.environ.get("ACKSLOC_COMPARE") == "1"

# --- Stage 2.5: reconcile the leftovers (Chris, 2026-06-25) --------------------
# Before a leftover is declared human_only/claude_only (a genuine loss/leak), search the
# WHOLE other side — every region, every page, + collapsed-widget text — for where the
# content actually went. Measured: ~17-26% of "apparently lost" content is present-but-the
# -single-pass-matcher-missed-it (up to 36% HPFUN / 45% MXDB-MathJax via cross-region/page
# relocation). Reclassify those as a MILD "present, just placed/shaped differently"
# divergence instead of a full loss, so human_only/claude_only mean GENUINELY-ABSENT only.
# Set RECONCILE_OFF=1 to revert to the raw single-pass buckets.
RECONCILE = os.environ.get("RECONCILE_OFF") != "1"

# REWORDING-TOLERANT relocation (Chris, 2026-06-25). The human's finished HTML has been
# through revisions, so a moved element is usually ALSO reworded — its word-overlap with
# Claude's version drops below the strict 0.6 'relocated' bar AND the 'reworded' near-miss
# test only looked on the SAME page. Result: content that was BOTH moved AND reworded fell
# through the gap and was wrongly called a loss (the dominant false-alarm, ~88% measured
# round 110). With RECONTOL on (default), the relocation search accepts a twin ANYWHERE when
# the overlap is moderate (>=0.42) AND a DISTINCTIVE word is shared (a content word >=6 chars
# — a place name / key term that survives a rewrite), or when most of the element's
# distinctive words are contained in a longer (expanded) Claude element. The distinctive-word
# requirement is the safeguard: two unrelated paragraphs that merely share common words ('the',
# 'is') are NOT matched, so a GENUINELY-absent loss is still reported. Chris's spec: match by
# content tied to the same Writers-Template tag (its distinctive words ARE that tag's content),
# never by exact text or page position; ignore vastly-different content. Set RECONTOL_OFF=1 to
# revert to the strict 0.6 / same-page-only behaviour.
RECONTOL = os.environ.get("RECONTOL_OFF") != "1"

# --- Stage 4.7: WT-DERIVABLE divergence audit (Chris, CEDO102, 2026-06-25) ------
# The triangulation the harness exists for is WT tag -> human element -> Claude element.
# Stage 2.5 makes "missing" trustworthy (GENUINELY absent), but it then dropped the genuinely-
# absent element into a flat, low-priority human_only — so a CONVERTER BUG (the writer tagged it,
# the human built it, Claude derivably should have too, but DIDN'T) was buried, exactly as
# CEDO102's dropped Understand/Know/Do menu curriculum slipped past the first full run.
# Stage 4.7 RE-READS every genuinely-absent / extra / mismatched element against the WT and
# splits it into a DERIVABLE bug (Claude got it wrong and the WT+human prove what it should be)
# vs an EDITORIAL difference (no WT anchor, or the human itself deviated from the tag — Stage 3.5).
#   • wt_loss          — WT-tagged + human built the tag's family + Claude MISSING  (the headline)
#   • tag_leak         — Claude emitted a literal '[tag]' (a raw-tag conversion failure)
#   • wt_type_mismatch — matched pair: human built the WT family, Claude built a DIFFERENT one
# General across EVERY element + region (not a menu-curriculum special-case). Diagnostic-only —
# touches the diagnostic side (compare_page / report), never the protected skeleton-gate API.
# Set WTLOSS_OFF=1 to revert (wt_loss -> human_only, no tag_leak / wt_type_mismatch boost).
WTAUDIT = os.environ.get("WTLOSS_OFF") != "1"
# Phase-1 widget fairness: content the human built INSIDE an interactive widget / interactive
# activity is intentionally a PLACEHOLDER on Claude's side (the harness never compares widget
# internals, per the design spec). Such a 'loss' is the known Phase-1 limitation, NOT a converter
# bug — so it stays a plain human_only and is never elevated to wt_loss. A human element is
# widget-internal when its WT tag implies a widget OR its ancestor bundle carries one of these
# class markers ('interactive' = the activity-interactive wrapper; the rest are widget classes).
WIDGET_INTERNAL_MARKERS = ("interactive", "clickdrop", "flipcard", "flip-card", "carousel",
                           "accordion", "draganddrop", "dragdrop", "ddcontainer",
                           "questioncontainer", "speechbubble", "hintslider", "shapehover",
                           "memorygame", "crossword", "tabcontent", "selfcheck")
RECON_W = {"relocated": 0.5, "merged": 0.5, "split": 0.5, "hidden": 0.75,
           "reworded": 0.25, "short": 0.1}   # short: mostly noise, but a big cluster still nudges

WIDGET_CLASSES = {
    "dragAndDrop", "accordion", "carousel", "flipCard", "clickDrop", "infoTrigger",
    "multiChoiceQuiz", "speechBubble", "tabs", "dropDown", "modal", "reorder",
    "wordHighlighter", "typing", "audioTrigger", "dropQuiz", "hint", "radioQuiz",
    "selectionBox", "slider", "selfCheck", "wordDrag", "hintSlider", "imageLabel",
    "imageZoom", "bingo", "memoryGame", "selfReflection", "wordSelect", "stopWatch",
    "rotateBanner", "shapeHover", "wordFind", "sliderChart", "sketcher", "crossword",
    "randomSelect", "timeline", "puzzle", "glossary", "diceRoller", "translateSection",
    "numberLine", "cv2-interactive",
}
CALLOUT_CLASSES = {"alert", "important", "whakatauki", "wananga", "quoteText", "activity"}
# Pure layout / width / ubiquitous tokens the ancestor-class diff must NOT surface (col widths are
# owned by width_diff; callout wrappers by wrapper_missing/extra; row + padding are structural noise).
WRAP_IGNORE = {"row", "paddingl", "paddingr", "padding", "container", "container-fluid",
               "no-gutters", "col"}
CONTENT_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th",
                "figcaption", "blockquote", "label", "button", "a"}
# ROUND 315 (loop Round 2): HTML void elements. html.parser fires handle_starttag for a plain
# <br>/<img> with NO matching handle_endtag, but handle_startendtag (start + end) for <br />.
# Both trees below pushed every start tag and popped on every end tag, so a plain void left a
# phantom stack entry and a permanently inflated depth: the widget-skip never released, the
# wrapper chain drifted, and ATree dropped any <p> holding a <br> (its </p> met "br" on the
# stack top). Voids are now never pushed and their (synthetic) end tags ignored, so <br> and
# <br /> parse identically -- exposed when round 315 moved the corpus to the KB's XHTML form.
VOID_TAGS = {"img", "br", "meta", "link", "input", "hr", "source", "wbr", "area", "base", "col", "embed", "track"}
STRUCT = {"div", "section", "ul", "ol", "table", "tr", "tbody", "thead", "dl"}
COL_RE = re.compile(r"^col(-|$)")
NOTE_PREFIX = ("red flag", "cs ", "kate scanlon", "nadia stanton", "caroline schwer",
               "simon vita", "amanda griffiths", "creative services")


def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", (t or "").lower())).strip()


def fold(s):
    s = re.sub(r"<[^>]+>", " ", s or "").lower().replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9' ]+", " ", s)).strip()


# ---- tag lexicon: WT tag -> (canonical, directive) for the Stage 3.5 guard ----
def load_lexicon():
    try:
        lex = json.load(open(os.path.join(DATA, "Tag_Lexicon.json"), encoding="utf-8"))
    except Exception:
        return {}
    a2 = {}
    for canon, spec in lex.get("tags", {}).items():
        d = spec.get("directive", "")
        a2[fold(canon)] = (canon, d)
        for a in spec.get("aliases", []):
            a2.setdefault(fold(a), (canon, d))
    return a2


LEX = load_lexicon()
CALLOUT_TAGS = {"alert", "important", "whakatauki", "whakatauaki", "wananga", "quote",
                "quote text", "wa nanga", "activity"}


def implied_type(tagtext):
    """Family the WT tag ASKS FOR: heading/callout/list/table/widget/text/unknown."""
    if not tagtext:
        return ("unknown", "")
    key = fold(tagtext)
    cand = [key, re.sub(r"\s*\d+[a-z]?$", "", key).strip(), key.split()[0] if key else ""]
    for c in cand:
        if c and c in LEX:
            canon, d = LEX[c]
            if d == "INTERACTIVE":
                return ("widget", canon)
            if re.match(r"h[1-6]$", canon) or canon in ("title", "title bar", "heading"):
                return ("heading", canon)
            if canon in CALLOUT_TAGS or "activity" in canon:
                return ("callout", canon)
            if canon in ("bullet", "bullets", "list", "numbered list", "ul", "ol"):
                return ("list", canon)
            if canon == "table":
                return ("table", canon)
            return ("text", canon)
    if re.match(r"h[1-6]$", key) or "head" in key or "title" in key:
        return ("heading", key)
    if "activity" in key:
        return ("callout", "activity")
    if any(w in key for w in ("flip", "carousel", "accordion", "drag", "click", "speech",
                              "tab", "slider", "quiz", "memory", "reorder", "hover", "modal",
                              "bingo", "crossword", "word")):
        return ("widget", key.split()[0])
    return ("unknown", key)


# ----------------------------------------------------------------- HTML parse --
class ATree(HTMLParser):
    """Flat element list. Each content node carries region + the full structural
    ancestor bundle inside that region + col + level + normalised text. Widget
    subtrees collapse to one node, but we keep a text SIGNATURE of their content
    so a widget can still be content-matched + anchored (the Stage 3.5 guard)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.stack = []          # (depth, tag, classes)
        self.rstack = []         # (depth, region-name)
        self.elements = []
        self.skip_depth = None   # inside a widget subtree
        self.win = None          # the widget node being captured
        self.wbuf = None         # its inner text buffer
        self._txt = None
        self._node = None

    def _region(self):
        return self.rstack[-1][1] if self.rstack else "pre"

    def _bundle(self):
        rd = self.rstack[-1][0] if self.rstack else -1
        return [" ".join(cl) if cl else t
                for (d, t, cl) in self.stack if d > rd and t in STRUCT]

    def _nearest_col(self):
        for (d, t, cl) in reversed(self.stack):
            cols = [c for c in cl if COL_RE.match(c)]
            if cols:
                return " ".join(sorted(cols))
        return ""

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return                      # ROUND 315: a void never enters the stack
        a = dict(attrs)
        cl = (a.get("class") or "").split()
        rid = a.get("id")
        name = None
        if rid == "header":
            name = "header"
        elif rid == "module-menu-content":
            name = "menu"
        elif rid == "body":
            name = "body"
        elif rid == "footer":
            name = "footer"
        elif "acks" in cl:
            name = "acks"
        if name:
            self.rstack.append((self.depth, name))
        if self.skip_depth is None and any(c in WIDGET_CLASSES for c in cl):
            w = next(c for c in cl if c in WIDGET_CLASSES)
            self.win = {"tag": "WIDGET", "widget": w, "region": self._region(),
                        "bundle": self._bundle(), "col": self._nearest_col(),
                        "level": None}
            self.wbuf = []
            self.skip_depth = self.depth
        self.stack.append((self.depth, tag, cl))
        self.depth += 1
        if self.skip_depth is None and tag in CONTENT_TAGS:
            self._txt = []
            self._node = {"tag": tag, "region": self._region(), "bundle": self._bundle(),
                          "col": self._nearest_col(),
                          "level": int(tag[1]) if re.match(r"h[1-6]$", tag) else None}

    def handle_data(self, data):
        if self.skip_depth is not None and self.wbuf is not None:
            self.wbuf.append(data)
        elif self._txt is not None:
            self._txt.append(data)

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return                      # ROUND 315: the synthetic end of a self-closed void
        self.depth -= 1
        if self._node is not None and self.stack and self.stack[-1][1] == tag \
                and tag == self._node["tag"]:
            txt = norm("".join(self._txt))
            if txt and len(txt) >= 2 and not txt.startswith(NOTE_PREFIX):
                self._node["text"] = txt
                self.elements.append(self._node)
            self._node = None
            self._txt = None
        if self.stack:
            self.stack.pop()
        if self.skip_depth is not None and self.depth <= self.skip_depth:
            if self.win is not None:
                self.win["text"] = norm(" ".join(self.wbuf))[:160]
                self.elements.append(self.win)
            self.win = None
            self.wbuf = None
            self.skip_depth = None
        while self.rstack and self.depth <= self.rstack[-1][0]:
            self.rstack.pop()


_CACHE = {}


def aparse(path):
    if path in _CACHE:
        return _CACHE[path]
    t = ATree()
    try:
        raw = open(path, encoding="utf-8", errors="ignore").read()
        t.raw = raw
        t.feed(raw)
    except Exception:
        pass
    _CACHE[path] = t
    return t


# ----------------------------------------------------------------- WT anchor ---
def wt_items(code):
    # returns (items, idx, idxm) — the early returns MUST be 3-tuples or run()/report_page/
    # consensus_accumulate crash unpacking them. A module with no parsed.txt (e.g. some bilingual
    # modules) simply has no WT anchor: every downstream anchor() then returns ("", 0.0) — fine.
    d = _corpus.mdir(HUMAN, code)
    if not os.path.isdir(d):
        return [], {}, {}
    pf = [f for f in os.listdir(d) if f.endswith("_parsed.txt")]
    if not pf:
        return [], {}, {}
    items = []
    for raw in open(os.path.join(d, pf[0]), encoding="utf-8", errors="replace"):
        line = raw.rstrip("\n")
        tags = [t for t in re.findall(r"\[\s*([A-Za-z][^\]\n]{0,28}?)\s*\]", line)
                if not re.match(r"/?\s*red text", t, re.I)]
        txt = re.sub(r"\U0001f534\[RED TEXT\]|\[/RED TEXT\]\U0001f534", "", line)
        txt = re.sub(r"\[[^\]\n]{0,30}\]", "", txt)
        f = fold(txt)
        ft = tags[0].strip().lower() if tags else ""
        if f or ft:
            items.append((ft, f))
    idx = defaultdict(list)
    idxm = defaultdict(list)   # Stage 4.7 — multi-word index (each item under its first 4 folded
    for k, (_, f) in enumerate(items):   # words) so anchor_loss can find a LABEL-prefixed item
        if f:                            # ('know the earth…') from the human's first word ('the')
            ws = f.split()               # WITHOUT a full O(items) rescan per leftover (the timeout).
            idx[ws[0]].append(k)
            for w in dict.fromkeys(ws[:4]):
                idxm[w].append(k)
    return items, idx, idxm


def anchor(text, wt, idx):
    tf = fold(text)
    if not tf or not wt:
        return ("", 0.0)
    w0 = tf.split()[0]
    cand = idx.get(w0) or range(min(len(wt), 220))
    best, br = -1, 0.0
    for k in cand:
        r = difflib.SequenceMatcher(None, tf[:80], wt[k][1][:80]).ratio()
        if r > br:
            br, best = r, k
    if best < 0 or br < WT_ANCHOR_MIN:
        return ("", round(br, 2))
    tag, k = wt[best][0], best
    while not tag and k > 0:
        k -= 1
        tag = wt[k][0]
    return (tag, round(br, 2))


def anchor_loss(text, wt, idx, idxm):
    """A STRONGER anchor used ONLY by the Stage 4.7 loss/leak audit (the shared anchor() is left
    untouched so matched-pair / Stage-3.5 numbers — and the self-test — never move).

    The shared anchor() keys candidates on the human element's FIRST WORD, so it misses a WT item
    that PREFIXES the prose with the curriculum LABEL: human '<p>The Earth is…</p>' (first word
    'the') never reaches WT '[H2] **Know:** The Earth is…' (indexed under 'know'), and the leading
    'know ' also offsets difflib — the Know/Do sections the human copy-edited score ~0.4 and are
    wrongly called editorial. anchor_loss looks the human's first word up in idxm (the MULTI-word
    index — every item under its first 4 words), so the label-prefixed item is a CANDIDATE without
    an O(items) rescan, then difflib-matches it on the full item AND the item minus a 1–2-word
    label, with a containment/prefix fallback. Length-gated (>=8 folded chars)."""
    tag, conf = anchor(text, wt, idx)
    if conf >= WT_ANCHOR_MIN or not wt:
        return tag, conf
    tf = fold(text)
    if len(tf) < 8:
        return tag, conf
    cand = idxm.get(tf.split()[0], [])
    if len(cand) > 80:        # a very common first word ('the'/'a'/…) — too many candidates to
        return tag, conf      # rescan affordably; the cheap anchor's verdict stands
    best, br = -1, conf
    for k in cand:
        f = wt[k][1]
        if not f:
            continue
        variants = [f]
        parts = f.split(" ")
        if len(parts) > 2:
            variants.append(" ".join(parts[1:]))   # minus a 1-word label ('know …')
            variants.append(" ".join(parts[2:]))    # minus a 2-word label ('whainga ako …')
        for fc in variants:
            r = difflib.SequenceMatcher(None, tf[:90], fc[:90]).ratio()
            if r > br:
                br, best = r, k
    if best < 0 or br < WT_ANCHOR_MIN:
        for k in cand:                    # containment / prefix fallback (un-edited prose, bare label)
            f = wt[k][1]
            if f and ((tf in f) or (len(f) >= 8 and (f.startswith(tf) or tf.startswith(f)))):
                best, br = k, max(br, 0.72)
                break
    if best < 0 or br < WT_ANCHOR_MIN:
        return tag, conf
    t, j = wt[best][0], best
    while not t and j > 0:
        j -= 1
        t = wt[j][0]
    return (t, round(br, 2)) if t else (tag, conf)


# --------------------------------------------------------------- Stage 3.5 -----
def built_type(el):
    if el.get("widget"):
        return ("widget", el["widget"])
    tag = el["tag"]
    if re.match(r"h[1-6]$", tag):
        return ("heading", tag)
    for cn in callout_names(el["bundle"]):
        return ("callout", cn)
    if tag == "li" or any(b in ("ul", "ol") for b in el["bundle"]):
        return ("list", tag)
    if tag in ("td", "th") or any("table" in b for b in el["bundle"]):
        return ("table", tag)
    return ("text", tag)


def _wnorm(name):
    return fold(name).replace(" ", "")


def element_swap(implied, built):
    """SKIP only a CONFIDENT widget-vs-widget swap (the case Chris flagged: the WT
    tag names interactive X, the human built a different interactive Y). Names are
    normalised so 'speech bubble' (WT) == 'speechBubble' (class). A non-widget
    implied type (a mis-anchored sub-tag like [image]/[front]/[body]) is NOT a swap
    — we'd rather under-skip than hide a real build failure."""
    if implied[0] == "widget" and built[0] == "widget":
        if _wnorm(implied[1]) == _wnorm(built[1]):
            return None
        return f"{implied[1]} -> {built[1]}"
    return None


# ------------------------------------------------------------- bundle diff -----
def callout_names(bundle):
    s = set()
    for b in bundle:
        for t in b.split():
            if t in CALLOUT_CLASSES:
                s.add(t)
    return s


def bundle_classes(bundle):
    """EVERY semantic class token on the ancestor div-chain (the full ladder, un-normalised),
    minus the layout/width/callout tokens already owned by width_diff / wrapper_missing. This is
    the fix for the round-143.2 miss: diff_bundle's callout/col/role reductions THREW AWAY every
    other class token, so a `row` vs `row supervisor` (a deep child dictating the top row's class)
    was invisible. Keeping the raw tokens here means such a difference is ALWAYS in the diff
    window — no ancestor class is ever normalised away."""
    s = set()
    for b in bundle:
        for t in b.split():
            if COL_RE.match(t):          # col widths -> width_diff owns these
                continue
            if t in CALLOUT_CLASSES:     # callout wrappers -> wrapper_missing/extra owns these
                continue
            if t.lower() in WRAP_IGNORE:  # pure layout noise
                continue
            s.add(t)
    return s


def roles(bundle):
    out = []
    for b in bundle:
        toks = b.split()
        if "row" in toks:
            out.append("row")
        elif any(COL_RE.match(t) for t in toks):
            out.append("col")
        elif any(t in CALLOUT_CLASSES for t in toks):
            out.append(sorted(t for t in toks if t in CALLOUT_CLASSES)[0])
        elif b in ("ul", "ol"):
            out.append("list")
        elif b in ("table", "tr", "tbody", "thead"):
            out.append("table")
        elif "videoSection" in toks or "ratio" in toks:
            out.append("video")
        else:
            out.append("div")
    return out


def diff_bundle(ce, he):
    v = []
    hc, cc = callout_names(he["bundle"]), callout_names(ce["bundle"])
    for m in sorted(hc - cc):
        v.append(f"wrapper_missing({m})")
    for m in sorted(cc - hc):
        v.append(f"wrapper_extra({m})")
    # FULL ancestor-class ladder diff — the round-143.2 fix. Any SEMANTIC class present on one
    # side's ancestor chain and absent on the other's (e.g. the human's `row supervisor` vs a
    # bare Claude `row`) surfaces here; it is never collapsed away by roles()/callout_names.
    hcl, ccl = bundle_classes(he["bundle"]), bundle_classes(ce["bundle"])
    for m in sorted(hcl - ccl):
        v.append(f"wrapper_class_missing({m})")
    for m in sorted(ccl - hcl):
        v.append(f"wrapper_class_extra({m})")
    if ce["col"] != he["col"]:
        v.append(f"width_diff({he['col'] or '-'} -> {ce['col'] or '-'})")
    if he["level"] and ce["level"] and he["level"] != ce["level"]:
        v.append(f"level_diff(h{he['level']} -> h{ce['level']})")
    if ce["tag"] != he["tag"] and not (he["level"] and ce["level"]) \
            and "WIDGET" not in (ce["tag"], he["tag"]):
        v.append(f"tag_diff({he['tag']} -> {ce['tag']})")
    if not v:
        hr, cr = roles(he["bundle"]), roles(ce["bundle"])
        if hr != cr:
            v.append(f"nesting_diff({'>'.join(hr) or '.'} vs {'>'.join(cr) or '.'})")
    return v


# ------------------------------------------------------- Stage 4.5: consensus --
# Accumulate every human instance of each WT tag corpus-wide, derive the MAJORITY
# scaffold, and judge Claude against that consensus — so one developer's mistake
# can't read as a Claude bug (reuses the majority/deviation method of
# build_convention_registry.py / Style_Anchor_Registry_Majority_And_Deviations).
_CONSENSUS = None


def canon_tag(tagtext):
    """Resolve a raw WT tag to its canonical lexicon name so [H2]/[h 2]/[heading 2]
    all group together; fall back to the folded text."""
    key = fold(tagtext)
    for c in (key, re.sub(r"\s*\d+[a-z]?$", "", key).strip(), key.split()[0] if key else ""):
        if c and c in LEX:
            return LEX[c][0]
    return key


def sig_of_element(el):
    """Scaffold signature. GRANULAR (default): the full row/col-WIDTH/wrapper ancestor
    ladder (scaffold_sig.granular_sig) — so a col-md-6 bullet and a col-md-12 bullet get
    DIFFERENT sigs and a width/wrapper outlier is visible. LEGACY (GRANULAR_SIG_OFF=1):
    the width- and depth-agnostic li@list form (callout/list/table/video markers only)."""
    if GRANULAR:
        return ss.granular_sig(el)
    return ss.blind_sig(el, CALLOUT_CLASSES, roles)


def consensus_accumulate(codes):
    """tag-key (region|canon_tag) -> Counter(signature) across human modules."""
    counts = defaultdict(Counter)
    examples = defaultdict(lambda: defaultdict(list))
    for code in codes:
        wt, idx, _ = wt_items(code)
        if not wt:
            continue
        hdir = _corpus.mdir(HUMAN, code)
        if not os.path.isdir(hdir):
            continue
        for f in os.listdir(hdir):
            if not f.endswith(".html"):
                continue
            T = aparse(os.path.join(hdir, f))
            for e in T.elements:
                if e["region"] not in REGIONS or not (e.get("text") or e.get("widget")):
                    continue
                tag, conf = anchor(e.get("text", ""), wt, idx)
                if not tag or conf < WT_ANCHOR_MIN:
                    continue
                key = f"{e['region']}|{canon_tag(tag)}"
                s = ss.blind_sig(e, CALLOUT_CLASSES, roles)   # legacy flat file stays blind
                counts[key][s] += 1
                if code not in examples[key][s]:
                    examples[key][s].append(code)
    return counts, examples


def _merge_consensus(files):
    counts = defaultdict(Counter)
    examples = defaultdict(lambda: defaultdict(list))
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        for key, sigs in d.get("counts", {}).items():
            for s, n in sigs.items():
                counts[key][s] += n
        for key, sx in d.get("examples", {}).items():
            for s, mods in sx.items():
                for m in mods:
                    if m not in examples[key][s]:
                        examples[key][s].append(m)
    reg = {}
    for key, c in counts.items():
        N = sum(c.values())
        ranked = c.most_common()
        canonical = [s for s, n in ranked if n / N >= CONSENSUS_FLOOR]
        coverage = sum(n for s, n in ranked if n / N >= CONSENSUS_FLOOR) / N if N else 0
        # a consensus is RELIABLE only when the accepted variants genuinely dominate;
        # a fragmented tag (e.g. heading LEVEL, which the human re-levels by context)
        # has no reliable consensus and falls back to single-instance Stage 4.
        reliable = N >= CONSENSUS_MIN_N and coverage >= CONSENSUS_COVERAGE and bool(canonical)
        reg[key] = {"n": N, "reliable": reliable, "coverage": round(coverage, 3),
                    "canonical": canonical,
                    "top": [{"sig": s, "n": n, "share": round(n / N, 3),
                             "mods": examples[key][s][:6]} for s, n in ranked[:6]]}
    return reg


def load_consensus():
    global _CONSENSUS
    if _CONSENSUS is None:
        try:
            _CONSENSUS = json.load(open(CONSENSUS_PATH, encoding="utf-8"))
        except Exception:
            _CONSENSUS = {}
    return _CONSENSUS


def consensus_reading(region, wtag, ce, he, code=None):
    """Adjudicate a differing matched pair against the corpus. Returns None or a verdict
    dict {verdict, level, group, majority, majority_share, n_modules, claude_sig, human_sig}
    where verdict ∈ {human_outlier, claude_vs_consensus, both_offnorm}.

    GRANULAR (default): consult the GRANULAR registry at the FINEST reliable grouping for
    `code` (series -> phase -> prefix -> subject -> corpus) — the scaffold-aware adjudication
    (BLL244 col-md-12 human vs the BLL col-md-6 majority -> human_outlier).
    LEGACY (GRANULAR_SIG_OFF=1): the flat corpus-canonical Scaffold_Consensus set."""
    cs, hs = sig_of_element(ce), sig_of_element(he)
    if cs == hs:
        return None
    if GRANULAR:
        # PRECEDENCE-FIRST (Chris): what did the previously-developed sibling build? -> then
        # corpus only as a labelled fallback. doc-14 is layered on by the vetting workflow.
        return gc.adjudicate(region, canon_tag(wtag) if wtag else None,
                             ce.get("widget") or ce["tag"], code or "", cs, hs)
    if not wtag:
        return None
    info = load_consensus().get(f"{region}|{canon_tag(wtag)}")
    if not info or not info.get("reliable") or not info.get("canonical"):
        return None
    canonical = set(info["canonical"])
    cc, hc = cs in canonical, hs in canonical
    verdict = ("human_outlier" if (cc and not hc)
               else "claude_vs_consensus" if (hc and not cc) else "both_offnorm")
    return {"verdict": verdict, "level": "corpus", "group": "ALL",
            "majority": None, "majority_share": None, "n_modules": info.get("n"),
            "claude_sig": cs, "human_sig": hs}


def _consensus_evidence(cr):
    """A short human-readable tag for the authority that decided a verdict (round 180: the
    6-level cascade) — leading with the deciding LEVEL + reference; corpus/escalate labelled
    as the weak last resort they are."""
    if not cr:
        return ""
    a = cr.get("authority")
    share = cr.get("majority_share")
    pct = f"{share:.0%}" if isinstance(share, (int, float)) else "?"
    if a == "doc14":
        return f"[L1 doc14 {cr.get('reference')} token={cr.get('reference_sig')}]"
    if a == "series_precedence":
        return f"[L2 series {cr.get('reference')} built {cr.get('reference_sig', '')}]"
    if a == "phase_precedence":
        return f"[L3 phase {cr.get('reference')} maj={cr.get('reference_sig')} {pct}/{cr.get('n_modules')}m]"
    if a in ("subject_template_consensus", "subject_consensus", "corpus_consensus"):
        lname = {"subject_template_consensus": "L4 subj+tmpl", "subject_consensus": "L5 subject",
                 "corpus_consensus": "L6 corpus(last-resort)"}[a]
        return f"[{lname} {cr.get('reference')} maj={cr.get('reference_sig')} {pct}/{cr.get('n_modules')}m]"
    if a == "none" or cr.get("escalate"):
        return "[ESCALATE — no clean precedent]"
    # legacy CASCADE6_OFF authorities
    if a in ("sibling_precedence", "sibling_precedence_mixed") and cr.get("reference"):
        mark = "≈(series mixed)" if a == "sibling_precedence_mixed" else ""
        return f"[sibling {cr['reference']} built {cr.get('reference_sig', '')}{mark}]"
    if cr.get("majority"):
        return (f"[corpus-fallback {cr.get('level')}:{cr.get('group')} maj={cr['majority']} "
                f"{cr['majority_share']:.0%}/{cr['n_modules']}m]")
    return ""


# ----------------------------------------------------------------- matching ----
def first_tokens(t, n=8):
    return " ".join(t.split()[:n])


def _match_text(cels, hels):
    """exact text -> first-8-tokens / token-Jaccard, greedy one-to-one, banded."""
    hby = defaultdict(list)
    for i, e in enumerate(hels):
        hby[e["text"]].append(i)
    usedh, matched, conly = set(), [], []
    for ce in cels:
        idxs = [i for i in hby.get(ce["text"], []) if i not in usedh]
        if idxs and len(ce["text"]) >= 2:
            usedh.add(idxs[0])
            matched.append((ce, hels[idxs[0]], "exact", 1.0))
            continue
        ct = set(ce["text"].split())
        c8 = first_tokens(ce["text"])
        best, bi, bstrong = 0.0, None, False
        if len(ct) >= 3:
            for i, he in enumerate(hels):
                if i in usedh:
                    continue
                ht = set(he["text"].split())
                if not ht:
                    continue
                j = len(ct & ht) / len(ct | ht)
                strong = (j >= MATCH_STRONG and len(ct) >= 4) or \
                         (c8 and c8 == first_tokens(he["text"]) and len(ct) >= 4)
                sc = 1.0 if strong else j
                if sc > best:
                    best, bi, bstrong = sc, i, strong
        if bi is not None and best >= MATCH_WEAK:
            band = "high" if (best >= MATCH_STRONG or bstrong) else "uncertain"
            usedh.add(bi)
            matched.append((ce, hels[bi], band, round(best, 2)))
        else:
            conly.append(ce)
    holy = [hels[i] for i in range(len(hels)) if i not in usedh]
    return matched, conly, holy


def match_region(cels, hels):
    """Content nodes match by TEXT; widgets match by exact TYPE (so an empty-text
    widget still pairs with its counterpart, and a SWAPPED widget — different type —
    stays unmatched, to be ruled on by the Stage 3.5 guard)."""
    cc = [e for e in cels if e["tag"] != "WIDGET"]
    hc = [e for e in hels if e["tag"] != "WIDGET"]
    matched, conly, holy = _match_text(cc, hc)
    cw = [e for e in cels if e["tag"] == "WIDGET"]
    hw = [e for e in hels if e["tag"] == "WIDGET"]
    hbt = defaultdict(list)
    for i, e in enumerate(hw):
        hbt[e["widget"]].append(i)
    usedh = set()
    for ce in cw:
        lst = [i for i in hbt.get(ce["widget"], []) if i not in usedh]
        if lst:
            usedh.add(lst[0])
            matched.append((ce, hw[lst[0]], "widget", 1.0))
        else:
            conly.append(ce)
    holy += [hw[i] for i in range(len(hw)) if i not in usedh]
    return matched, conly, holy


# ----------------------------------------------------------------- per page ----
def by_region(els):
    d = defaultdict(list)
    for e in els:
        if e["region"] in REGIONS and ("text" in e or e.get("widget")):
            d[e["region"]].append(e)
    return d


def menu_li_count(els):
    return sum(1 for e in els if e["region"] == "menu" and e["tag"] == "li")


# ----------------------------------------------- Stage 0.5: page anatomy (macro)
def norm_class(s):
    return " ".join(sorted((s or "").split()))


def page_anatomy(raw):
    """The DISTILLED big-chunk anatomy of a whole page: the <body> TEMPLATE class and
    which landmark SECTIONS exist (menu, crumbs, inquiry/fundamentals panels, acks,
    mathjax, footer variant). Coarse on purpose — it catches a whole section one side
    has and the other doesn't (e.g. a spurious module menu on a Fundamentals page)
    BEFORE the granular element diff buries it."""
    raw = raw or ""
    bc = re.search(r'<body[^>]*class="([^"]*)"', raw)
    body_class = bc.group(1).strip() if bc else ""
    menu_li, menu_tabs = 0, False
    a = raw.find('id="module-menu-content"')
    if a >= 0:
        b = raw.find('id="body"', a)
        menu = raw[a:b if b > a else len(raw)]
        menu = re.sub(r'<!--[\s\S]*?-->', ' ', menu)          # ignore commented-out menu
        menu_li = sum(1 for m in re.findall(r'<li\b[^>]*>([\s\S]*?)</li>', menu)
                      if re.sub(r'<[^>]+>', '', m).strip())
        menu_tabs = 'nav-tabs' in menu
    fn = re.search(r'class="(footer-nav[^"]*)"', raw)
    return {
        "body_class": body_class,
        "menu_li": menu_li, "menu_tabs": menu_tabs,
        "crumbs": 'class="crumbs"' in raw,
        "inquiry": ('inquiryPanel' in raw) or ('inquiry' in body_class),
        "fundamentals": ('fundamentalsPanel' in raw) or ('class="phases"' in raw)
                        or ('fundamentals' in body_class),
        "acks": ('class="acks"' in raw) or ('"acks"' in raw),
        "mathjax": ('mathjax' in raw.lower()) or ('tex-mml' in raw.lower()),
        "footer_nav": fn.group(1) if fn else "",
    }


def macro_diff(c, h):
    """SECTION-level divergences (the big picture) — reported first, weighted high."""
    d = []
    if norm_class(c["body_class"]) != norm_class(h["body_class"]):
        d.append(f"body_class(H:{h['body_class'] or '-'} | C:{c['body_class'] or '-'})")
    if (h["menu_li"] == 0) != (c["menu_li"] == 0):
        side = "C-has/H-none" if h["menu_li"] == 0 else "H-has/C-none"
        d.append(f"menu_section({side} H{h['menu_li']}/C{c['menu_li']})")
    section_keys = ("crumbs", "inquiry", "fundamentals", "acks", "mathjax") if COMPARE_ACKS \
        else ("crumbs", "inquiry", "fundamentals", "mathjax")
    for k in section_keys:
        if c[k] != h[k]:
            d.append(f"{k}_section(H:{'y' if h[k] else 'n'}/C:{'y' if c[k] else 'n'})")
    if c["menu_tabs"] != h["menu_tabs"]:
        d.append(f"menu_archetype(H-tabs:{h['menu_tabs']}/C-tabs:{c['menu_tabs']})")
    if norm_class(c["footer_nav"]) != norm_class(h["footer_nav"]):
        d.append(f"footer_nav(H:{h['footer_nav'] or '-'}/C:{c['footer_nav'] or '-'})")
    return d


# ----------------------------------------------- Stage 2.5: reconcile leftovers
def _toks(t):
    return set(t.split())


def _contained(small, stoks, big, btoks):
    """small element's text lives inside the big one (prefix substring or token subset)."""
    if not small or not big:
        return False
    if small[:60] in big:
        return True
    return len(stoks) >= 4 and stoks <= btoks


def _is_fragment(piece, whole):
    """piece is a literal chunk of whole."""
    return len(piece) >= 10 and piece[:24] in whole


def build_corpus(pairs, side):
    """Every content node + collapsed-widget text on ONE side across the module's paired
    pages — the search space the reconciler walks. side 'c' = Claude, 'h' = human.
    'blob' = all of that side's text concatenated (cross-page), for the rewording-tolerant
    PHRASE-presence net (a distinctive contiguous phrase surviving anywhere = present)."""
    content, widgets = [], []
    for pk, cf, cT, hf, hT in pairs:
        T = cT if side == "c" else hT
        for e in T.elements:
            txt = e.get("text", "")
            if e.get("tag") == "WIDGET":
                widgets.append((pk, txt, _toks(txt)))
            elif e.get("region") in REGIONS and txt:
                content.append((pk, e["region"], e["tag"], txt, _toks(txt)))
    blob = " ".join(c[3] for c in content) + " " + " ".join(w[1] for w in widgets)
    return {"content": content, "widgets": widgets, "blob": blob}


def _phrase_present(text, blob):
    """A DISTINCTIVE contiguous phrase of `text` survives in `blob` — the rewording-tolerant
    'is this content here at all?' test. Matches the validated round-110 discriminator: the
    6-word head, or ANY 3 consecutive words holding a >=6-char content word (a name/term that
    survives a rewrite). Contiguity + a distinctive word keep genuinely-different content
    (which shares only scattered common words) a real loss."""
    if not blob:
        return False
    if text and text in blob:           # whole element survives VERBATIM (length-independent —
        return True                     # catches short plain captions: "make your bed", "fold them")
    w = text.split()
    if len(w) >= 6 and " ".join(w[:6]) in blob:
        return True
    for i in range(len(w) - 2):
        win = w[i:i + 3]
        if max((len(x) for x in win), default=0) >= 6 and " ".join(win) in blob:
            return True
    return False


def build_corpus_all(code, side, self_test=False):
    """Reconciler search space = the ENTIRE other side of the module (ALL pages), not just the
    PAIRED ones. Critical when one side has more pages than the other (e.g. Claude split a lesson
    into 16 files, the human into 5): pair_pages drops the 11 unpaired Claude pages, so content
    RELOCATED onto them was invisible and wrongly called a loss. Same shape as build_corpus.
    (RECONTOL path; self_test reads Claude's side from the human dir like pair_pages.)"""
    d = _corpus.mdir((HUMAN if self_test else CLAUDE) if side == "c" else HUMAN, code)  # round128 nested
    content, widgets, raw_blobs = [], [], []
    if os.path.isdir(d):
        for f in sorted([x for x in os.listdir(d) if x.endswith(".html")], key=page_key):
            path = os.path.join(d, f)
            T = aparse(path)
            pk = page_key(f)
            for e in T.elements:
                txt = e.get("text", "")
                if e.get("tag") == "WIDGET":
                    widgets.append((pk, txt, _toks(txt)))
                elif e.get("region") in REGIONS and txt:
                    content.append((pk, e["region"], e["tag"], txt, _toks(txt)))
            # RAW page text (incl. WIDGET internals, which aparse COLLAPSES away) for the
            # phrase-presence net: Chris's spec is "is the content in the Claude FILE", and a
            # moved caption often lands inside a collapsed Claude widget — invisible to the
            # parsed elements, but present in the raw file. Normalised the same way as element
            # text so the substring test is apples-to-apples.
            try:
                raw = open(path, encoding="utf-8", errors="ignore").read()
                raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
                raw_blobs.append(norm(_html.unescape(re.sub(r"<[^>]+>", " ", raw)).replace("\xa0", " ")))
            except Exception:
                pass
    blob = " ".join(raw_blobs)
    return {"content": content, "widgets": widgets, "blob": blob}


def reconcile(el, pk, region, corpus):
    """Where did this 'missing/extra' element actually go? Walk the priority ladder and
    return (reason, detail); reason None = genuinely absent. Reasons: short / hidden /
    merged / split / relocated / reworded. (Cross-language pairing can't happen — te-reo
    and English share no tokens, so the Jaccard/substring tests never fire across them.)"""
    text = el.get("text", "")
    T = _toks(text)
    if len(T) < 3:
        return "short", None
    content, widgets = corpus["content"], corpus["widgets"]
    # 1) hidden inside a collapsed widget (same page)
    for (wp, wtext, wtoks) in widgets:
        if wp == pk and _contained(text, T, wtext, wtoks):
            return "hidden", "widget"
    # 2) merged: contained in a single LONGER element (same page)
    for (cp, creg, ctag, ctext, ctoks) in content:
        if cp == pk and len(ctoks) > len(T) + 3 and _contained(text, T, ctext, ctoks):
            return "merged", f"{creg}/{ctag}"
    # 3) split: spread across >=2 fragments (same page)
    frags = [ctoks for (cp, creg, ctag, ctext, ctoks) in content
             if cp == pk and _is_fragment(ctext, text)]
    if len(frags) >= 2 and len(set().union(*frags) & T) >= 0.6 * len(T):
        return "split", f"{len(frags)} pieces"
    # 4) relocated: a twin in another region (same page) or on another page.
    #    REWORDING-TOLERANT (RECONTOL, default on): a moved element is usually ALSO reworded,
    #    so its overlap drops below the strict 0.6. Accept a moderate overlap (>=0.42) when a
    #    DISTINCTIVE content word is shared (>=6 chars — a name/term that survives a rewrite),
    #    or when most of this element's distinctive words are contained in a longer (expanded)
    #    Claude element. The distinctive-word requirement keeps genuinely-different content a
    #    real loss (two paragraphs sharing only common words do NOT match).
    best = (0.0, None, None)
    for (cp, creg, ctag, ctext, ctoks) in content:
        if cp == pk and creg == region:
            continue
        if not (T and ctoks):
            continue
        inter = T & ctoks
        j = len(inter) / len(T | ctoks)
        if RECONTOL:
            dshare = sum(1 for w in inter if len(w) >= 6)
            cont = len(inter) / len(T)
            if j >= 0.6 or (j >= 0.42 and dshare >= 1) or (cont >= 0.66 and dshare >= 2):
                where = f"{creg} p{cp}" if cp != pk else f"{creg} same-page"
                return "relocated", where
        if j > best[0]:
            best = (j, cp, creg)
    if best[0] >= 0.6:
        where = f"{best[2]} p{best[1]}" if best[1] != pk else f"{best[2]} same-page"
        return "relocated", where
    # 5) reworded: near-miss in the SAME region/page (just under the matcher's 0.45)
    for (cp, creg, ctag, ctext, ctoks) in content:
        if cp == pk and creg == region:
            j = len(T & ctoks) / len(T | ctoks) if (T and ctoks) else 0.0
            if 0.30 <= j < 0.45:
                return "reworded", None
    # 6) REWORDING-TOLERANT presence net (RECONTOL, default on): the element was moved AND
    #    reworded/restructured — split, merged or expanded across a differently-paginated page —
    #    so no single Claude element is a clean twin, but a DISTINCTIVE contiguous phrase of it
    #    still survives somewhere in Claude's text. This is the round-110 measured fix for the
    #    dominant false alarm (content present, just moved + reworded). Genuinely-absent content
    #    has no surviving distinctive phrase, so it stays a real loss.
    if RECONTOL and _phrase_present(text, corpus.get("blob", "")):
        return "relocated", "phrase"
    return None, None


def _recon_apply(rec, cnt, reason, detail, side):
    """Stamp a reconciled disposition onto the record + tally it. side 'human'/'claude'."""
    if reason == "short":
        rec.update(disposition=f"{side}_short", framework="C (tiny cell — can't judge)",
                   verdict=["short_fragment"], reconciled="short")
        cnt["short"] += 1
    else:
        rec.update(disposition=f"{side}_present",
                   framework="C (present — matcher relocated/reshaped)",
                   verdict=[reason + (f"({detail})" if detail else "")], reconciled=reason)
        cnt["reconciled"] += 1
        cnt[f"recon_{reason}"] += 1
        cnt["_recon_score"] += RECON_W.get(reason, 0.5)


def compare_page(code, module, page, cT, hT, wt, idx, idxm=None, corpora=None):
    """Return (records, counts). counts drive the score."""
    recs = []
    cR, hR = by_region(cT.elements), by_region(hT.elements)
    cnt = defaultdict(float)
    cnt["menu_li_h"] = menu_li_count(hT.elements)
    cnt["menu_li_c"] = menu_li_count(cT.elements)
    # Stage 0.5 — MACRO: distilled whole-page anatomy first, so a missing/extra SECTION
    # (e.g. a spurious menu on a Fundamentals page) leads the report, not buried granular nits.
    md = macro_diff(page_anatomy(getattr(cT, "raw", "")), page_anatomy(getattr(hT, "raw", "")))
    for m in md:
        recs.append({"module": module, "page": page, "region": "MACRO",
                     "disposition": "macro", "framework": "B", "verdict": [m],
                     "wt_tag": "", "wt_confidence": 0.0, "human": None, "claude": None,
                     "text_sig": m})
    cnt["macro"] = len(md)
    if md:
        cnt["_macro_txt"] = "; ".join(md)
    for region in (REGIONS if COMPARE_ACKS else REGIONS - {"acks"}):
        matched, conly, holy = match_region(cR.get(region, []), hR.get(region, []))
        for ce, he, band, score in matched:
            wtag, wconf = anchor(he.get("text", ""), wt, idx)
            imp, blt = implied_type(wtag), built_type(he)
            swap = element_swap(imp, blt) if (wtag and wconf >= WT_ANCHOR_MIN
                                              and imp[0] != "unknown") else None
            rec = {"module": module, "page": page, "region": region, "match": band,
                   "match_score": score, "wt_tag": wtag, "wt_confidence": wconf,
                   "implied": "/".join(imp), "built": "/".join(blt),
                   "human": {"element": he["tag"], "col": he["col"], "level": he["level"],
                             "bundle": he["bundle"]},
                   "claude": {"element": ce["tag"], "col": ce["col"], "level": ce["level"],
                              "bundle": ce["bundle"]},
                   "text_sig": he.get("text", "")[:60]}
            if swap:
                rec["disposition"] = "SKIP"
                rec["framework"] = "C (element changed in revision)"
                rec["verdict"] = [f"element_swap({swap})"]
                cnt["skipped"] += 1
            else:
                v = diff_bundle(ce, he)
                creading = consensus_reading(region, wtag, ce, he, module) if v else None
                verdict_str = creading["verdict"] if creading else None
                rec["consensus"] = creading
                cnt["matched"] += 1
                # the finest-reliable-grouping evidence is the PRIMARY signal, surfaced
                # ahead of the raw width_diff (WS2): "col-md-6 matches 93% of BLL / human is
                # the outlier" rather than an unqualified width_diff.
                evid = _consensus_evidence(creading)
                if verdict_str == "human_outlier":
                    # the PAIRED human deviates from the corpus norm; Claude matches
                    # it -> the human is the outlier, NOT a Claude bug. Not scored.
                    rec["disposition"] = "human_outlier"
                    rec["framework"] = "C (human outlier vs corpus consensus)"
                    rec["verdict"] = v + [f"human_outlier{evid}"]
                    cnt["human_outlier"] += 1
                else:
                    rec["disposition"] = "diff"
                    rec["framework"] = "B" if v else "A"
                    rec["verdict"] = v or ["identical"]
                    w = 0.5 if band == "uncertain" else 1.0
                    if verdict_str == "claude_vs_consensus":
                        w *= 1.5   # corroborated by the corpus majority -> boost
                        rec["verdict"] = v + [f"claude_vs_consensus{evid}"]
                    # Stage 4.7 — WT TYPE MISMATCH: the human built the WT tag's FAMILY but Claude
                    # built a DIFFERENT family (a derivable Claude type error — the WT+human prove
                    # what Claude should have produced). Boost + flag (not editorial: imp==human).
                    if (WTAUDIT and v and wconf >= WT_ANCHOR_MIN and imp[0] != "unknown"
                            and imp[0] == blt[0] and built_type(ce)[0] != imp[0]):
                        rec["verdict"] = rec["verdict"] + [
                            f"wt_type_mismatch({imp[0]}->{built_type(ce)[0]})"]
                        cnt["wt_type_mismatch"] += 1
                        w *= 1.5
                    for item in v:
                        cnt[item.split("(")[0]] += w
            recs.append(rec)
        for he in holy:
            wtag, wconf = anchor(he.get("text", ""), wt, idx)   # cheap anchor for every leftover
            rec = {"module": module, "page": page, "region": region,
                   "wt_tag": wtag, "wt_confidence": wconf, "claude": None,
                   "human": {"element": he["tag"], "col": he["col"],
                             "level": he["level"], "bundle": he["bundle"]},
                   "text_sig": he.get("text", "")[:60]}
            if he["tag"] == "WIDGET" and wtag and wconf >= WT_ANCHOR_MIN:
                sw = element_swap(implied_type(wtag), built_type(he))
                if sw:
                    rec.update(disposition="SKIP",
                               framework="C (element changed in revision)",
                               verdict=[f"element_swap({sw})"])
                    cnt["skipped"] += 1
                    recs.append(rec)
                    continue
            # Stage 2.5 — is this 'lost' content actually present somewhere on Claude's side?
            reason, detail = (reconcile(he, page, region, corpora["claude"])
                              if (RECONCILE and corpora) else (None, None))
            if reason:
                _recon_apply(rec, cnt, reason, detail, "human")
            else:
                # Stage 4.7 — WT-DERIVABLE LOSS: genuinely absent from Claude AND confidently
                # anchored to a Writers-Template tag → WT-derived content the converter dropped =
                # a high-confidence BUG, not an editorial human-only. A confident anchor already
                # means the TEXT is in the WT (editorial human-ADDED content anchors weakly →
                # stays human_only); the Stage-3.5 element_swap SKIP above already carved off the
                # one genuinely-editorial case (the human built a DIFFERENT widget than the tag).
                # We deliberately do NOT require the built type to equal the tag's implied family:
                # a '[H2] **Label:** prose' yields BOTH a heading AND its prose <p>, and the prose
                # (built 'text' ≠ implied 'heading') is just as WT-derived and just as dropped.
                # PERF: pay for the stronger label-aware anchor ONLY here (a GENUINE loss, after
                # reconcile failed) and ONLY when the cheap anchor was weak — so the corpus run
                # doesn't anchor_loss every reconciled/short leftover too.
                if WTAUDIT and wconf < WT_ANCHOR_MIN:
                    wtag, wconf = anchor_loss(he.get("text", ""), wt, idx, idxm or {})
                    rec["wt_tag"], rec["wt_confidence"] = wtag, wconf
                imp, blt = implied_type(wtag), built_type(he)
                hb = [b.lower() for b in he.get("bundle", [])]
                widget_internal = (imp[0] == "widget"
                                   or any(any(m in b for m in WIDGET_INTERNAL_MARKERS) for b in hb))
                if WTAUDIT and wconf >= WT_ANCHOR_MIN and wtag and not widget_internal:
                    rec.update(disposition="wt_loss",
                               framework=f"A/B (WT-derivable: [{wtag}] in WT + built by human, dropped by Claude)",
                               verdict=[f"wt_loss([{wtag}]->{blt[1]})"])
                    cnt["wt_loss"] += 1
                else:
                    rec.update(disposition="human_only", framework="B", verdict=["human_only"])
                    cnt["human_only"] += 1
            recs.append(rec)
        for ce in conly:
            wtag, wconf = anchor(ce.get("text", ""), wt, idx)
            rec = {"module": module, "page": page, "region": region,
                   "wt_tag": wtag, "wt_confidence": wconf, "human": None,
                   "claude": {"element": ce["tag"], "col": ce["col"],
                              "level": ce["level"], "bundle": ce["bundle"]},
                   "text_sig": ce.get("text", "")[:60]}
            # Stage 2.5 — is this 'extra' content actually present somewhere on the human side?
            reason, detail = (reconcile(ce, page, region, corpora["human"])
                              if (RECONCILE and corpora) else (None, None))
            if reason:
                _recon_apply(rec, cnt, reason, detail, "claude")
            elif WTAUDIT and re.search(r"\[\s*[A-Za-z][^\]\n]{0,28}\]", ce.get("text", "")):
                # Stage 4.7 — a LITERAL '[tag]' surviving in Claude's text is a raw-tag conversion
                # FAILURE (the converter emitted the Writers-Template tag verbatim instead of
                # building the element it names). High signal: the human never ships a raw [tag].
                rec.update(disposition="tag_leak", framework="A (raw [tag] leaked into output)",
                           verdict=["tag_leak"])
                cnt["tag_leak"] += 1
            else:
                rec.update(disposition="claude_only", framework="B", verdict=["claude_only"])
                cnt["claude_only"] += 1
            recs.append(rec)
    # WS2 — MENU TAB-LABEL consensus. Overview nav-tabs collapse into a widget in the
    # element model, so read them straight and flag any tab whose label deviates from the
    # corpus positional majority (ENGS102 tab-2 'Learning' vs 'Information' 97/103). When
    # Claude matches the majority and only the human deviates, it is a human_outlier — not
    # a Claude bug. Diagnostic-only; never scored into _score.
    if GRANULAR:
        hraw, craw = getattr(hT, "raw", "") or "", getattr(cT, "raw", "") or ""
        kind = "overview" if str(page).lstrip("-_").split(".")[0].split("_")[0] in ("0", "00") else "lesson"
        for f in gc.tab_verdict(module, hraw, kind):
            claude_labels = ss.nav_tab_labels(craw) or []
            claude_here = claude_labels[f["position"]] if f["position"] < len(claude_labels) else None
            human_out = (claude_here == f["majority"]) or (claude_here != f["label"])
            recs.append({"module": module, "page": page, "region": "menu",
                         "disposition": "human_outlier" if human_out else "diff",
                         "framework": "C (human outlier vs corpus consensus)" if human_out else "B",
                         "wt_tag": "", "wt_confidence": 0.0,
                         "consensus": {"verdict": "human_outlier" if human_out else "diff",
                                       "level": "corpus", "group": "overview-tabs",
                                       "majority": f["majority"], "majority_share": f["majority_share"],
                                       "n_modules": f["n"]},
                         "human": {"element": "TAB", "col": None, "level": None, "tab_label": f["label"]},
                         "claude": {"element": "TAB", "col": None, "level": None, "tab_label": claude_here},
                         "verdict": [f"tab_label_outlier(pos{f['position']}: '{f['label']}' vs "
                                     f"corpus maj '{f['majority']}' {f['majority_share']:.0%}/{f['n']}m)"],
                         "text_sig": f"tab{f['position']}"})
            if human_out:
                cnt["human_outlier"] += 1
    # menu loop: human menu populated but Claude menu empty (the menu_gate signal)
    if cnt["menu_li_h"] >= 1 and cnt["menu_li_c"] == 0:
        cnt["loop_broken"] += 1
    elements = (cnt["matched"] + cnt["human_only"] + cnt["claude_only"]
                + cnt["reconciled"] + cnt["short"] + cnt["wt_loss"] + cnt["tag_leak"])
    sc = sum(W.get(k, 0.0) * cnt[k] for k in W) + cnt["_recon_score"]
    cnt["_score"] = round(sc / max(elements, 1) + MACRO_WEIGHT * cnt["macro"], 3)
    cnt["_elements"] = elements
    return recs, cnt


# ------------------------------------------------------------------ pairing ----
def page_key(name):
    m243 = re.search(r"_(\d+)_(\d+(?:_\d+)*)\.html$", name)   # ROUND 243: the library-form name CODE_L_S.html
    if m243:                                                    # (both sides may carry it now)
        return float(f"{m243.group(1)}.{m243.group(2).split('_')[0]}")
    m = re.findall(r"(\d+(?:\.\d+)?)", name.rsplit("-", 1)[-1].rsplit("_", 1)[-1])
    return float(m[0]) if m else 0.0


def sig_of(T):
    w = set()
    for e in T.elements:
        if e.get("level") and "text" in e and (COMPARE_ACKS or e.get("region") != "acks"):
            w |= set(e["text"].split())
    return w


def pair_pages(code, self_test=False):
    cdir = _corpus.mdir(HUMAN if self_test else CLAUDE, code)   # round128 nested layout: MUST
    hdir = _corpus.mdir(HUMAN, code)                            # resolve via _corpus, not a raw join
    if not (os.path.isdir(cdir) and os.path.isdir(hdir)):
        return []
    cf = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=page_key)
    hf = sorted([f for f in os.listdir(hdir) if f.endswith(".html")], key=page_key)
    cP = {f: aparse(os.path.join(cdir, f)) for f in cf}
    hP = {f: aparse(os.path.join(hdir, f)) for f in hf}
    cs = {f: sig_of(cP[f]) for f in cf}
    hs = {f: sig_of(hP[f]) for f in hf}
    usedh, prelim = set(), []
    for f in cf:
        best, bj = None, 0.0
        for g in hf:
            if g in usedh:
                continue
            a, b = cs[f], hs[g]
            j = len(a & b) / len(a | b) if (a and b) else 0.0
            if j > bj:
                bj, best = j, g
        if best and bj >= PAGE_PAIR_MIN:
            usedh.add(best)
            prelim.append((f, best))
        else:
            prelim.append((f, None))
    remh = [g for g in hf if g not in usedh]
    ri, out = 0, []
    for f, g in prelim:
        if g is None and ri < len(remh):
            g = remh[ri]
            ri += 1
        if g:
            out.append((page_key(g), f, cP[f], g, hP[g]))
    return out


# ------------------------------------------------------------------- driver ----
def run(codes, self_test=False):
    pages, allrecs = [], []
    for code in codes:
        module = code
        wt, idx, idxm = wt_items(code)
        pairs = list(pair_pages(code, self_test))
        corpora = ({"claude": build_corpus_all(code, "c", self_test) if RECONTOL else build_corpus(pairs, "c"),
                    "human": build_corpus_all(code, "h", self_test) if RECONTOL else build_corpus(pairs, "h")}
                   if RECONCILE else None)
        for pk, cf, cT, hf, hT in pairs:
            recs, cnt = compare_page(code, module, str(pk), cT, hT, wt, idx, idxm, corpora)
            allrecs.extend(recs)
            pages.append((code, str(pk), cnt))
    return pages, allrecs


def series_of(code):
    m = re.match(r"[A-Za-z]+", code)
    return m.group(0) if m else code


def top_reason(cnt):
    order = ["wt_loss", "tag_leak", "loop_broken", "human_only", "wrapper_missing",
             "wrapper_class_missing", "tag_diff", "width_diff", "level_diff", "wrapper_extra",
             "wrapper_class_extra", "nesting_diff", "wt_type_mismatch", "claude_only"]
    bits = [(f"** {k}×{int(cnt[k])} **" if k in ("wt_loss", "tag_leak") else f"{k}×{int(cnt[k])}")
            for k in order if cnt.get(k)]
    if cnt.get("reconciled"):
        rb = ", ".join(f"{r[6:]} {int(cnt[r])}" for r in
                       ("recon_relocated", "recon_merged", "recon_split",
                        "recon_hidden", "recon_reworded") if cnt.get(r))
        bits.append(f"(reconciled {int(cnt['reconciled'])}: {rb})")
    if cnt.get("short"):
        bits.append(f"(short {int(cnt['short'])})")
    if cnt.get("skipped"):
        bits.append(f"(skipped {int(cnt['skipped'])})")
    if cnt.get("human_outlier"):
        bits.append(f"(human-outlier {int(cnt['human_outlier'])})")
    if cnt.get("_macro_txt"):
        bits.insert(0, "MACRO[" + str(cnt["_macro_txt"]) + "]")
    return ", ".join(bits) or "clean"


def report_rollup(pages):
    bymod = defaultdict(list)
    for code, pk, cnt in pages:
        bymod[code].append((pk, cnt))
    modscore = {c: round(sum(x[1]["_score"] for x in v) / len(v), 3)
                for c, v in bymod.items()}
    byser = defaultdict(list)
    for c in bymod:
        byser[series_of(c)].append(c)
    serscore = {s: round(sum(modscore[c] for c in cs) / len(cs), 3)
                for s, cs in byser.items()}
    # Stage 4.7 — the WT-DERIVABLE BUG headline LEADS the report so a tagged-but-dropped element
    # (the CEDO102 class) can never be buried under the granular per-series nits again. wt_loss =
    # writer tagged it + human built it + Claude dropped it; tag_leak = a raw [tag] survived.
    tot_loss = int(sum(cnt.get("wt_loss", 0) for _, _, cnt in pages))
    tot_leak = int(sum(cnt.get("tag_leak", 0) for _, _, cnt in pages))
    bug_pages = [(c, pk, cnt) for c, pk, cnt in pages if cnt.get("wt_loss") or cnt.get("tag_leak")]
    if bug_pages:
        bymod_bug = defaultdict(lambda: [0, 0])
        for c, pk, cnt in bug_pages:
            bymod_bug[c][0] += int(cnt.get("wt_loss", 0))
            bymod_bug[c][1] += int(cnt.get("tag_leak", 0))
        print("=" * 80)
        print(f"WT-DERIVABLE LOSSES — probable CONVERTER BUGS   "
              f"(wt_loss {tot_loss} / tag_leak {tot_leak}  over {len(bug_pages)} pages "
              f"/ {len(bymod_bug)} modules)")
        print("  the writer TAGGED it and the human built that tag's element, but Claude "
              "DROPPED or leaked it")
        print("  -> drill in:  python3 anchor_compare.py --module <CODE>   (lists each lost element + its WT tag)")
        print("=" * 80)
        for c in sorted(bymod_bug, key=lambda c: -(bymod_bug[c][0] + bymod_bug[c][1]))[:40]:
            wl, tl = bymod_bug[c]
            worst = max(bymod[c], key=lambda x: x[1].get("wt_loss", 0) + x[1].get("tag_leak", 0))
            bits = (f"wt_loss {wl}" if wl else "") + (f"  tag_leak {tl}" if tl else "")
            print(f"   {c:9} {bits:24} worst p{worst[0]}: {top_reason(worst[1])[:108]}")
        print()
    print(f"ANCHOR_COMPARE — per-series rollup | {len(bymod)} modules, "
          f"{len(pages)} pages | worst-first\n")
    for s in sorted(byser, key=lambda s: -serscore[s]):
        print(f"== {s}  (series score {serscore[s]}) ==")
        for c in sorted(byser[s], key=lambda c: -modscore[c]):
            worst = max(bymod[c], key=lambda x: x[1]["_score"])
            print(f"   {c:9} score {modscore[c]:5}   worst p{worst[0]}: "
                  f"{top_reason(worst[1])}")
        print()


def report_module(code):
    pages, _ = run([code])
    print(f"ANCHOR_COMPARE — {code}, page by page\n")
    for c, pk, cnt in sorted(pages, key=lambda x: -x[2]["_score"]):
        print(f"  page {pk:5}  score {cnt['_score']:5}  elements {int(cnt['_elements'])}"
              f"  menu_li h{int(cnt['menu_li_h'])}/c{int(cnt['menu_li_c'])}"
              f"   {top_reason(cnt)}")


def report_page(code, n):
    wt, idx, idxm = wt_items(code)
    target = float(n)
    pairs = list(pair_pages(code))
    corpora = ({"claude": build_corpus_all(code, "c") if RECONTOL else build_corpus(pairs, "c"),
                "human": build_corpus_all(code, "h") if RECONTOL else build_corpus(pairs, "h")}
               if RECONCILE else None)
    for pk, cf, cT, hf, hT in pairs:
        if abs(pk - target) > 0.001:
            continue
        recs, cnt = compare_page(code, code, str(pk), cT, hT, wt, idx, idxm, corpora)
        print(f"=== {code} page {pk}  (human {hf} <-> claude {cf}) ===")
        print(f"score {cnt['_score']} | elements {int(cnt['_elements'])} | "
              f"menu_li human {int(cnt['menu_li_h'])} / claude {int(cnt['menu_li_c'])}\n")
        for r in recs:
            if r["verdict"] == ["identical"]:
                continue
            tag = f"[{r['wt_tag']}]@{r['wt_confidence']}" if r.get("wt_tag") else "[no-anchor]"
            print(f"  {r['region']:6} {r['disposition']:11} {tag:22} {', '.join(r['verdict'])}")
            if r.get("human"):
                print(f"         H: {r['human']['element']:6} «{r['text_sig']}»  "
                      f"{'>'.join(roles(r['human']['bundle'])) or '.'}")
            if r.get("claude"):
                print(f"         C: {r['claude']['element']:6} "
                      f"{'>'.join(roles(r['claude']['bundle'])) or '.'}")
        return
    print(f"no paired page {n} for {code}")


# ===========================================================================
# COMPATIBILITY API — absorbed VERBATIM from the retired full_compare.py.
# This is the shared element model + matcher that _skeleton_compare.py (the
# PROTECTED skeleton gate, via CLAUDE), _discrepancy_audit.py and the
# outputs/_measure_*.py tools import. Kept byte-faithful so every one of those
# (and the gate) behaves EXACTLY as before. anchor_compare's own diagnostic
# uses ATree / aparse / match_region above; this block is purely for importers.
# ===========================================================================
SCAFFOLD_TAGS = {"div", "section", "ul", "ol", "table", "tr", "img", "iframe",
                 "audio", "span", "strong", "em"}
CV2_COMMENT_AUTHORS = ("kate scanlon", "nadia stanton", "caroline schwer",
                       "simon vita", "amanda griffiths", "creative services")


class Tree(HTMLParser):
    """Flat element list with depth, classes, region, text + the wrapper chain
    (row/col/callout/activity). (Absorbed from full_compare.py verbatim.)"""

    def __init__(self):
        super().__init__()
        self.depth = 0
        self.stack = []
        self.region = "pre"
        self.inv = Counter()
        self.elements = []
        self.skip_depth = None
        self._txt = None
        self._node = None

    def _chain(self):
        ch = []
        for (t, cl) in self.stack:
            if t != "div" and t != "section":
                continue
            if "row" in cl:
                ch.append("row")
            elif any(COL_RE.match(c) for c in cl):
                ch.append("col")
            elif "activity" in cl:
                ch.append("activity")
            elif any(c in {"alert", "important", "whakatauki", "wananga", "quoteText"} for c in cl):
                ch.append("callout")
        return tuple(ch)

    def _nearest_col(self):
        for (t, cl) in reversed(self.stack):
            cols = sorted(c for c in cl if COL_RE.match(c))
            if cols:
                return " ".join(cols)
        return ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        rid = a.get("id")
        if rid in ("header", "body", "footer"):
            self.region = rid
        if "acks" in cls:
            self.region = "acks"
        if self.skip_depth is None:
            self.inv[tag] += 1
            if cls:
                self.inv[f"{tag}.{'.'.join(sorted(cls))}"] += 1
            if any(c in WIDGET_CLASSES for c in cls):
                wtype = next(c for c in cls if c in WIDGET_CLASSES)
                self.elements.append({"tag": "WIDGET", "text": f"::{wtype}",
                                      "chain": self._chain(), "level": None,
                                      "col": self._nearest_col(), "region": self.region})
                self.skip_depth = self.depth
        if tag in VOID_TAGS:
            return                      # ROUND 315: counted in the inventory, never on the stack
        self.stack.append((tag, cls))
        self.depth += 1
        if self.skip_depth is None and tag in CONTENT_TAGS:
            self._txt = []
            self._node = {"tag": tag, "chain": self._chain(),
                          "level": int(tag[1]) if re.match(r"h[1-6]$", tag) else None,
                          "col": self._nearest_col(), "region": self.region}

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return                      # ROUND 315: the synthetic end of a self-closed void
        self.depth -= 1
        if self.stack:
            self.stack.pop()
        if self.skip_depth is not None and self.depth <= self.skip_depth:
            self.skip_depth = None
        if self._node is not None and tag == self._node["tag"]:
            txt = norm("".join(self._txt))
            if (txt and len(txt) >= 3 and not txt.startswith("red flag") and not txt.startswith("cs ")
                    and not txt.startswith(CV2_COMMENT_AUTHORS)):
                self._node["text"] = txt
                self.elements.append(self._node)
            self._node = None
            self._txt = None

    def handle_data(self, data):
        if self._txt is not None:
            self._txt.append(data)


def parse(path):
    t = Tree()
    try:
        t.feed(open(path, encoding="utf-8", errors="ignore").read())
    except Exception:
        pass
    return t


def match_elements(cels, hels):
    """Greedy text match: exact normalised text, then token-overlap >=0.8.
    Returns (matched_pairs, claude_only, human_only). (From full_compare.py.)"""
    hby = defaultdict(list)
    for i, e in enumerate(hels):
        hby[e["text"]].append(i)
    used_h = set()
    matched, c_only = [], []
    for ce in cels:
        idxs = [i for i in hby.get(ce["text"], []) if i not in used_h]
        if idxs:
            used_h.add(idxs[0])
            matched.append((ce, hels[idxs[0]]))
            continue
        ct = set(ce["text"].split())
        best, bi = 0.0, None
        if len(ct) >= 4:
            for i, he in enumerate(hels):
                if i in used_h or he["tag"] != ce["tag"]:
                    continue
                ht = set(he["text"].split())
                ov = len(ct & ht) / max(len(ct | ht), 1)
                if ov > best:
                    best, bi = ov, i
        if bi is not None and best >= 0.8:
            used_h.add(bi)
            matched.append((ce, hels[bi]))
        else:
            c_only.append(ce)
    h_only = [hels[i] for i in range(len(hels)) if i not in used_h]
    return matched, c_only, h_only


def _read_pages(files):
    pages = []
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        for p in d.get("pages", []):
            cnt = dict(p)
            code, pk = cnt.pop("module"), cnt.pop("page")
            pages.append((code, pk, cnt))
    return pages


def all_codes():
    return sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))


# =====================================================================  COVERAGE
# The SAFETY-NET pass (Chris): a tool you run after every change must NEVER fail
# closed and silent. This sweeps the WHOLE corpus (union of human+Claude module
# codes, all four templates) and reports every module that produces 0 records or
# has pages that could not pair — loudly, and exits non-zero on a TOOL failure
# (a pairing bug / null-test violation / regression miss). A genuine DATA gap
# (Claude never built the module, or the human side is an acks-only stub) is
# reported just as loudly but does NOT trip the exit — there is nothing the tool
# can do about missing inputs, and a permanent red would erode the safety net.
def coverage_codes():
    return sorted(set(_corpus.mods(HUMAN)) | set(_corpus.mods(CLAUDE)))


def template_of(code):
    for base in (HUMAN, CLAUDE):
        for t in _corpus.TEMPLATE_DIRS:
            if os.path.isdir(os.path.join(base, t, code)):
                return t
    return "?"


def _html_files(d):
    return sorted([f for f in os.listdir(d) if f.endswith(".html")]) if os.path.isdir(d) else []


# reasons an absent side is a DATA gap (nothing the tool can fix) vs a TOOL failure
DATA_GAP_REASONS = {"no_claude_html", "no_human_html", "no_comparable_content"}
TOOL_FAIL_REASONS = {"zero_pairs"}


def coverage_scan(codes):
    """Per-module coverage diagnostics. Cheap (pairing + element counts, NO reconcile), so it
    sweeps the whole corpus inside the sandbox wall. A module is a HARD DROP (0 records) when a
    side has no HTML, nothing pairs, or the paired pages carry no comparable content; a module is
    PARTIAL when it pairs but one side has extra pages with no counterpart (the human's different
    sub-pagination — expected asymmetry, surfaced not hidden)."""
    body_regions = REGIONS if COMPARE_ACKS else REGIONS - {"acks"}
    rows = []
    for code in codes:
        cfiles, hfiles = _html_files(_corpus.mdir(CLAUDE, code)), _html_files(_corpus.mdir(HUMAN, code))
        pairs = pair_pages(code) if (cfiles and hfiles) else []
        els = 0
        for pk, cf, cT, hf, hT in pairs:
            hR = by_region(hT.elements)
            els += sum(len(hR.get(r, [])) for r in body_regions)
        paired_c = {cf for _, cf, _, _, _ in pairs}
        paired_h = {hf for _, _, _, hf, _ in pairs}
        uc = [f for f in cfiles if f not in paired_c]
        uh = [f for f in hfiles if f not in paired_h]
        if not cfiles:
            drop = "no_claude_html"
        elif not hfiles:
            drop = "no_human_html"
        elif not pairs:
            drop = "zero_pairs"
        elif els == 0:
            drop = "no_comparable_content"
        else:
            drop = None
        rows.append({"code": code, "template": template_of(code), "nc": len(cfiles),
                     "nh": len(hfiles), "pairs": len(pairs), "els": els,
                     "unpaired_c": uc, "unpaired_h": uh, "drop": drop})
    return rows


def selfpair_bad(code):
    """Cheap null-test proxy: in self mode every page MUST pair to ITSELF (its fingerprint
    matches itself best) → self-score 0. Returns pages that self-paired to a DIFFERENT page
    (empty = passes). A violation is a genuine pairing bug, so it trips the exit code."""
    return [(cf, hf) for pk, cf, cT, hf, hT in pair_pages(code, self_test=True) if cf != hf]


MENU_COL_RE = re.compile(r"\bcol(-[a-z]+)?-\d+\b")

def menu_pane1_cols(raw):
    """ROUND 166 — the tabs-menu pane-1 col census (the ENGJ402 class): for a page whose
    module menu is a TABS shell, return the list of col-class strings that are DIRECT div
    children of tab-pane 1's first row (None = no tabs menu on the page)."""
    a = raw.find('id="module-menu-content"')
    if a < 0:
        return None
    b = raw.find('id="body"', a)
    menu = raw[a:b if b > a else len(raw)]
    close_c, open_c = menu.find("-->"), menu.find("<!--")
    if close_c >= 0 and (open_c < 0 or close_c < open_c):
        menu = menu[close_c + 3:]
    menu = re.sub(r"<!--[\s\S]*?-->", " ", menu)
    if "nav-tabs" not in menu:
        return None
    pm = re.search(r'<div class="tab-pane"[^>]*>', menu)
    if not pm:
        return None
    nxt = menu.find('<div class="tab-pane"', pm.end())
    seg = menu[pm.end():nxt if nxt > 0 else len(menu)]
    rm = re.search(r'<div class="row[^"]*"[^>]*>', seg)
    if not rm:
        return []
    cols, depth = [], 1
    for t in re.finditer(r"<(/?)div\b([^>]*)>", seg[rm.end():]):
        if t.group(1) == "/":
            depth -= 1
            if depth <= 0:
                break
        else:
            depth += 1
            if depth == 2:
                c = re.search(r'class="([^"]*)"', t.group(2))
                if c and MENU_COL_RE.search(c.group(1)):
                    cols.append(c.group(1).strip())
    return cols


def menu_structure_scan(codes):
    """ROUND 166 (Chris's safety-net ask, ENGJ402) — per module, the OVERVIEW tabs-menu
    pane-1 col-COUNT + col-form, human vs Claude: the whole-region structural diff no
    gate could see (the menu is #header-scoped, and the pre-166 miner layout-form lens
    was body-only — the tab-1 one-col miss sat invisible for 80+ rounds). Findings are
    reported by --audit like coverage partials; the DETECTION property is regress_menu."""
    rows = []
    for code in codes:
        try:
            cdir, hdir = _corpus.mdir(CLAUDE, code), _corpus.mdir(HUMAN, code)
            cfs = sorted(f for f in os.listdir(cdir) if f.endswith(".html"))
            hfs = sorted(f for f in os.listdir(hdir) if f.endswith(".html") and "-RR_" not in f)
        except OSError:
            continue
        def overview(files, base, dirname):
            for f in files:
                rest = f[len(dirname):] if f.startswith(dirname) else f
                m = re.match(r"^[\s._-]*(\d+)(?:[._-](\d+))?\.html$", rest)
                if (m and int(m.group(1)) == 0 and int(m.group(2) or 0) == 0) or rest == ".html":
                    try:
                        return open(os.path.join(base, f), encoding="utf-8", errors="ignore").read()
                    except OSError:
                        return None
            return None
        craw, hraw = overview(cfs, cdir, code), overview(hfs, hdir, code)
        if craw is None or hraw is None:
            continue
        cc, hc = menu_pane1_cols(craw), menu_pane1_cols(hraw)
        if cc is None and hc is None:
            continue
        rows.append({"code": code, "c_n": len(cc) if cc is not None else None,
                     "h_n": len(hc) if hc is not None else None,
                     "c_form": " + ".join(cc or []), "h_form": " + ".join(hc or [])})
    mism = [r for r in rows if r["c_n"] is not None and r["h_n"] is not None
            and r["c_n"] != r["h_n"]]
    return rows, mism


def regress_menu():
    """ROUND 166 — the menu-structure check's own DETECTION proof (the r149 selftest
    semantics: a check that cannot fail is vacuous). Take the real human ENGJ402_0.0
    (tab-pane-1 = TWO cols) and a synthetic PRE-166 one-col page (the second pane-1 col
    div collapsed — the round-165 Claude shape) and confirm the col-count comparator
    flags the pair. Returns (True|False|None, msg); None = fixture unavailable (SKIP)."""
    try:
        hraw = open(os.path.join(_corpus.mdir(HUMAN, "ENGJ402"), "ENGJ402_0.0.html"),
                    encoding="utf-8", errors="ignore").read()
    except Exception as e:
        return (None, f"fixture unavailable ({e})")
    hc = menu_pane1_cols(hraw)
    if not hc or len(hc) < 2:
        return (None, "fixture changed: human ENGJ402_0.0 pane-1 is no longer two-col")
    # synthesize the pre-166 one-col shape from the human page itself: drop the second
    # pane-1 col's OPENING class (its content flows on; the col census falls to 1)
    broken = hraw.replace('<div class="col-md-6 col-12 paddingL">', "<div>", 1)
    bc = menu_pane1_cols(broken)
    if bc is None or len(bc) != 1:
        return (False, f"synthetic collapse did not produce a one-col pane (got {bc})")
    if len(hc) != len(bc):
        return (True, f"flags pane-1 col-count {len(bc)} vs {len(hc)} (the r165 miss is now caught)")
    return (False, "MISS: comparator saw no col-count difference on the collapsed pane")


def regress_supervisor():
    """The TOOL's own regression test for the round-143.2 miss (Chris): the widened
    ancestor-class diff MUST flag a `row` vs `row supervisor` difference. Take the real human
    BLL241-2.0 (which has `row supervisor`) and a synthetic PRE-143.2 Claude (its `supervisor`
    stripped) and confirm diff_bundle emits wrapper_class_missing(supervisor) on the matched
    note. Returns (True|False|None, msg); None = fixture unavailable/changed (SKIP)."""
    try:
        hraw = open(os.path.join(_corpus.mdir(HUMAN, "BLL241"), "BLL241-2.0.html"),
                    encoding="utf-8", errors="ignore").read()
        craw = open(os.path.join(_corpus.mdir(CLAUDE, "BLL241"), "BLL241-02.html"),
                    encoding="utf-8", errors="ignore").read()
    except Exception as e:
        return (None, f"fixture unavailable ({e})")
    if 'class="row supervisor"' not in hraw:
        return (None, "fixture changed: human BLL241-2.0 no longer carries row.supervisor")
    hT = ATree(); hT.feed(hraw)
    broken = ATree(); broken.feed(craw.replace('class="row supervisor"', 'class="row"'))
    matched, _, _ = match_region(by_region(broken.elements).get("body", []),
                                 by_region(hT.elements).get("body", []))
    for ce, he, band, score in matched:
        if any("wrapper_class_missing(supervisor)" in v for v in diff_bundle(ce, he)):
            return (True, "flags row -> row supervisor (the 143.2 miss is now caught)")
    return (False, "MISS: did not flag the supervisor ancestor-class difference")


def report_coverage(codes):
    rows = coverage_scan(codes)
    drops = [r for r in rows if r["drop"]]
    partial = [r for r in rows if not r["drop"] and (r["unpaired_c"] or r["unpaired_h"])]
    bytmpl = defaultdict(lambda: [0, 0, 0])   # modules, covered, dropped
    for r in rows:
        b = bytmpl[r["template"]]
        b[0] += 1
        b[2 if r["drop"] else 1] += 1
    covered = len(rows) - len(drops)
    print("=" * 80)
    print(f"ANCHOR_COMPARE COVERAGE — {covered}/{len(rows)} modules produce records"
          f"  ({len(drops)} hard drops, {len(partial)} partial)")
    print("=" * 80)
    print(f"  {'template':13}{'modules':>9}{'covered':>9}{'dropped':>9}")
    for t in ("Standard", "Inquiry", "Fundamentals", "Bilingual", "?"):
        if t in bytmpl:
            m, c, d = bytmpl[t]
            print(f"  {t:13}{m:9}{c:9}{d:9}")
    tool_fail_drops = [r for r in drops if r["drop"] in TOOL_FAIL_REASONS]
    data_gap_drops = [r for r in drops if r["drop"] in DATA_GAP_REASONS]
    if drops:
        print("\n" + "!" * 80)
        print(f"!!  {len(drops)} MODULES PRODUCE ZERO RECORDS  "
              f"({len(tool_fail_drops)} tool-failure, {len(data_gap_drops)} data-gap) "
              f"— none silently skipped")
        print("!" * 80)
        for r in sorted(drops, key=lambda r: (r["drop"] not in TOOL_FAIL_REASONS, r["template"], r["code"])):
            kind = "TOOL-FAIL" if r["drop"] in TOOL_FAIL_REASONS else "data-gap "
            print(f"  {kind} {r['code']:9} [{r['template']:12}] {r['drop']:22} "
                  f"claude_html={r['nc']} human_html={r['nh']}")
    else:
        print("\n  no hard drops — every module produces records.")
    if partial:
        uc = sum(len(r["unpaired_c"]) for r in partial)
        uh = sum(len(r["unpaired_h"]) for r in partial)
        print(f"\n  PARTIAL — {len(partial)} modules: {uc} claude + {uh} human pages have no "
              f"counterpart (page-count asymmetry, expected; full list in --json)")
        for r in sorted(partial, key=lambda r: -(len(r["unpaired_c"]) + len(r["unpaired_h"])))[:8]:
            print(f"     {r['code']:9} C={r['nc']} H={r['nh']}  unpaired: claude "
                  f"{len(r['unpaired_c'])}, human {len(r['unpaired_h'])}")
    badself = [(r["code"], b) for r in rows if not r["drop"] for b in [selfpair_bad(r["code"])] if b]
    if badself:
        print(f"\n  NULL-TEST FAIL: {len(badself)} modules self-pair a page to a DIFFERENT page:")
        for c, b in badself[:10]:
            print(f"     {c}: {b}")
    else:
        print("\n  null-test proxy: every covered module self-pairs each page to itself.")
    ok, msg = regress_supervisor()
    flag = "PASS" if ok else ("SKIP" if ok is None else "FAIL")
    print(f"  row.supervisor regression [{flag}]: {msg}")
    # ROUND 166 — the MENU-STRUCTURE check (Chris's safety-net ask, ENGJ402): overview
    # tabs-menu pane-1 col-count human vs Claude. Mismatches are FINDINGS (reported, like
    # coverage partials — some are principled declines); the regression failing is a TOOL
    # failure and trips the exit code.
    mrows, mmism = menu_structure_scan([r["code"] for r in rows])
    print(f"  menu-structure: {len(mrows)} tabs-overview pairs, "
          f"{len(mmism)} pane-1 col-count mismatches"
          + ("" if not mmism else " — " + ", ".join(
              f"{m['code']}(C{m['c_n']}/H{m['h_n']})" for m in mmism[:10])
              + (" …" if len(mmism) > 10 else "")))
    mok, mmsg = regress_menu()
    mflag = "PASS" if mok else ("SKIP" if mok is None else "FAIL")
    print(f"  menu-structure regression [{mflag}]: {mmsg}")
    exit_bad = bool(tool_fail_drops or badself or ok is False or mok is False)
    print("\n  RESULT:", "TOOL FAILURE (see above)" if exit_bad
          else "trustworthy — 0 silent drops, null-test clean, regression held")
    print()
    return rows, (1 if exit_bad else 0)


def granular_selftest():
    """Prove the GRANULAR consensus fires — liveness + detection, never vacuous.
    T1 LIVENESS  the registry loads and is populated.
    T2 DETECTION a BLL menu pair (human col-md-12 vs Claude col-md-6) -> human_outlier;
                 the reverse -> claude_vs_consensus; identical sigs -> None.
    T3 TAB       ENGS102's overview tab-2 'Learning' is flagged vs the 'Information' majority."""
    import _corpus as _cp
    fails = []
    reg = gc.load()
    nkeys = len(reg.get("elements", {}))
    if nkeys < 40:
        fails.append(f"registry thin/empty ({nkeys} element-keys)")
    else:
        print(f"  OK   registry loaded: {nkeys} element-keys, "
              f"{reg['_meta'].get('_modules_measured')} modules")
    e6 = {"tag": "h5", "widget": None, "bundle": ["row", "col-12 col-md-6"]}
    e12 = {"tag": "h5", "widget": None, "bundle": ["row", "col-12 col-md-12"]}
    s6, s12 = sig_of_element(e6), sig_of_element(e12)
    v1 = gc.scaffold_verdict("menu", None, "h5", "BLL244", s6, s12)
    if v1 and v1["verdict"] == "human_outlier" and "col-md-6" in (v1["majority"] or ""):
        print(f"  OK   BLL244 human col-md-12 vs Claude col-md-6 -> human_outlier "
              f"[{v1['level']}:{v1['group']} {v1['majority_share']:.0%}/{v1['n_modules']}m]")
    else:
        fails.append(f"BLL244 pair not human_outlier ({v1})")
    v2 = gc.scaffold_verdict("menu", None, "h5", "BLL244", s12, s6)
    if not (v2 and v2["verdict"] == "claude_vs_consensus"):
        fails.append(f"reverse pair not claude_vs_consensus ({v2})")
    if gc.scaffold_verdict("menu", None, "h5", "BLL244", s6, s6) is not None:
        fails.append("identical sigs did not return None")
    hd = _cp.mdir(HUMAN, "ENGS102")
    tabhit = None
    if hd and os.path.isdir(hd):
        for f in sorted(os.listdir(hd)):
            if not f.endswith(".html"):
                continue
            raw = open(os.path.join(hd, f), encoding="utf-8", errors="ignore").read()
            for t in gc.tab_verdict("ENGS102", raw, "overview"):
                if t["position"] == 1 and t["label"].lower() == "learning" \
                        and t["majority"].lower() == "information":
                    tabhit = t
    if tabhit:
        print(f"  OK   ENGS102 tab-2 'Learning' flagged vs majority 'Information' "
              f"({tabhit['majority_share']:.0%}/{tabhit['n']}m)")
    else:
        fails.append("ENGS102 tab-2 'Learning' not flagged vs 'Information'")
    # round 180 — the 6-LEVEL cascade reachability proof (each level fires, doc-14 overrides,
    # escalate fires). Folded in so the standard --granular-selftest gate covers the cascade.
    print("  --- 6-level precedence cascade (granular_consensus.cascade_selftest) ---")
    if gc.cascade_selftest() != 0:
        fails.append("6-level cascade_selftest FAILED (a level is unreachable)")
    for f in fails:
        print("  FAIL:", f)
    print("GRANULAR SELFTEST:", "PASS" if not fails else "FAIL")
    return 0 if not fails else 1


def main():
    argv = sys.argv[1:]
    if "--granular-selftest" in argv:
        sys.exit(granular_selftest())
    if "--cascade-selftest" in argv:
        sys.exit(gc.cascade_selftest())
    if "--page" in argv:
        i = argv.index("--page")
        report_page(argv[i + 1], argv[i + 2])
        return
    if "--self" in argv:
        i = argv.index("--self")
        pages, _ = run([argv[i + 1]], self_test=True)
        for c, pk, cnt in pages:
            print(f"  {c} p{pk}: self-score {cnt['_score']} (must be ~0)")
        return
    if "--coverage" in argv:
        # SAFETY-NET pass: whole-corpus records/pairing audit + null-test proxy + the
        # row.supervisor tool regression. Exits non-zero ONLY on a tool failure.
        jout = None
        if "--json" in argv:
            i = argv.index("--json"); jout = argv[i + 1]
        codes = [a for a in argv if not a.startswith("--") and a not in (jout or "",)]
        codes = codes or coverage_codes()
        rows, rc = report_coverage(codes)
        if jout:
            json.dump({"modules": rows}, open(jout, "w"), indent=1)
            print(f"  wrote per-module coverage detail -> {jout}")
        sys.exit(rc)
    if "--regress" in argv:
        ok, msg = regress_supervisor()
        print(f"row.supervisor regression [{'PASS' if ok else ('SKIP' if ok is None else 'FAIL')}]: {msg}")
        sys.exit(0 if ok is not False else 1)
    if "--rules" in argv:
        # child->ancestor structural-rule catalogue — the standing companion miner this tool drives
        import subprocess
        miner = os.path.join(BASE, "..", "..", "outputs", "_measure_child_ancestor_classes.py")
        sys.exit(subprocess.call([sys.executable, miner]))
    if "--rules2" in argv:
        # round 161: the GRANULARITY miner (per-group / region / layout-form / composition /
        # style-transfer rules). Re-mines from the chunk caches; if they are missing, prints the
        # chunked recipe (each step fits the 45s sandbox wall).
        import subprocess
        miner = os.path.join(BASE, "..", "..", "outputs", "_mine_rendering_rules.py")
        cache = os.path.join(BASE, "..", "..", "outputs", "_rrm_cache")
        if not os.path.isdir(cache) or not any(f.startswith("scan_") for f in os.listdir(cache)):
            print("no scan caches yet — run (one sandbox call each):\n"
                  "  python3 ../../outputs/_mine_rendering_rules.py --vocab\n"
                  "  python3 ../../outputs/_mine_rendering_rules.py --scan H 0 4   (… 1 2 3)\n"
                  "  python3 ../../outputs/_mine_rendering_rules.py --scan C 0 2   (… 1)\n"
                  "  python3 ../../outputs/_mine_rendering_rules.py --merge")
            sys.exit(2)
        sys.exit(subprocess.call([sys.executable, miner, "--merge"]))
    if "--audit" in argv:
        # THE ONE COMMAND (Chris's bar): whole-corpus coverage safety-net + the row.supervisor
        # regression + the child->ancestor rule catalogue, in a single run. Round 161: ALSO
        # reports the granularity catalogue's known-answer selftest when that catalogue exists
        # (reads the cached Rendering_Rules_Catalogue.json — no re-mine; a FAIL is loud and
        # fails the audit, the r97-104 silent-pass lesson).
        import subprocess
        rows, rc = report_coverage(coverage_codes())
        print("\n" + "-" * 80)
        sys.stdout.flush()   # flush the buffered coverage report BEFORE the subprocess writes
        miner = os.path.join(BASE, "..", "..", "outputs", "_measure_child_ancestor_classes.py")
        subprocess.call([sys.executable, miner])
        cat = os.path.join(BASE, "..", "..", "outputs", "Rendering_Rules_Catalogue.json")
        if os.path.exists(cat):
            print("-" * 80)
            sys.stdout.flush()
            m2 = os.path.join(BASE, "..", "..", "outputs", "_mine_rendering_rules.py")
            rc2 = subprocess.call([sys.executable, m2, "--selftest"])
            rc = rc or rc2
        sys.exit(rc)
    if "--build-consensus" in argv:
        # accumulate human tag->scaffold counts (chunk-friendly; --json for a partial)
        i = argv.index("--build-consensus")
        rest = argv[i + 1:]
        jout = None
        if "--json" in rest:
            j = rest.index("--json"); jout = rest[j + 1]; rest = rest[:j] + rest[j + 2:]
        if "--series" in rest:
            s = rest.index("--series"); codes = [d for d in all_codes() if d.startswith(rest[s + 1])]
        else:
            codes = [a for a in rest if not a.startswith("--")] or all_codes()
        counts, examples = consensus_accumulate(codes)
        out = jout or CONSENSUS_PATH
        json.dump({"counts": {k: dict(v) for k, v in counts.items()},
                   "examples": {k: dict(sx) for k, sx in examples.items()}},
                  open(out, "w"), indent=1)
        print(f"consensus partial: {len(counts)} tag-keys from {len(codes)} modules -> {out}")
        return
    if "--merge-consensus" in argv:
        i = argv.index("--merge-consensus")
        files = [a for a in argv[i + 1:] if not a.startswith("--")]
        reg = _merge_consensus(files)
        json.dump(reg, open(CONSENSUS_PATH, "w"), indent=1)
        rel = sum(1 for v in reg.values() if v["reliable"])
        print(f"consensus registry: {len(reg)} tag-keys ({rel} reliable, N>={CONSENSUS_MIN_N})"
              f" -> {CONSENSUS_PATH}")
        return
    if "--consensus" in argv:
        i = argv.index("--consensus")
        pat = argv[i + 1] if len(argv) > i + 1 else ""
        reg = load_consensus()
        for k in sorted(reg):
            if pat.lower() in k.lower():
                v = reg[k]
                print(f"{k}  N={v['n']} reliable={v['reliable']} canonical={v['canonical']}")
                for t in v["top"]:
                    print(f"     {t['share']:<5} {t['sig']:30} n={t['n']:<4} e.g. {', '.join(t['mods'][:4])}")
        return
    if "--merge" in argv:
        # combine chunk JSONs (written with --json) into one corpus rollup + dump
        i = argv.index("--merge")
        files = [a for a in argv[i + 1:] if not a.startswith("--")]
        pages = _read_pages(files)
        report_rollup(pages)
        outj = os.path.join(BASE, "..", "..", "outputs", "anchor_compare.json")
        json.dump({"pages": [{"module": c, "page": p, **cnt} for c, p, cnt in pages]},
                  open(outj, "w"), indent=1)
        print(f"\nmerged {len(files)} parts -> outputs/anchor_compare.json ({len(pages)} pages)")
        return
    jout = None
    if "--json" in argv:
        i = argv.index("--json")
        jout = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if "--series" in argv:
        i = argv.index("--series")
        pre = argv[i + 1]
        codes = [d for d in all_codes() if d.startswith(pre)]
    else:
        codes = [a for a in argv if not a.startswith("--")]
    if len(codes) == 1 and not jout:
        report_module(codes[0])
        return
    if not codes:
        codes = all_codes()
    pages, allrecs = run(codes)
    report_rollup(pages)
    if jout:
        json.dump({"pages": [{"module": c, "page": p, **{k: v for k, v in cnt.items()}}
                             for c, p, cnt in pages], "elements": allrecs},
                  open(jout, "w"), indent=1)
        print(f"\nwrote {jout}  ({len(allrecs)} element records)")


if __name__ == "__main__":
    main()
