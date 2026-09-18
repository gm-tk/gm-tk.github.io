#!/usr/bin/env python3
"""STRUCTURAL SKELETON — Chris's text-immune structural comparison (round 50).

Converts a full HTML page into a simplified structural skeleton of <body>: ALL
rendered text removed, each element shown as `tag#id.class[attr=val]`, indentation =
nesting depth, identical sibling structures collapsed to "N× repeated[ block of K]:".

WHY: the element-level discrepancy audit only compares TEXT-MATCHED elements (~30% of a
page) and is defeated by the developer rewording content — so it can't measure whether
Claude's STRUCTURE matches the human's. Stripping the text and comparing the skeletons
compares 100% of the structure, rewording-immune. This is the right primary measurement.

USAGE:
  python3 _structural_skeleton.py <page.html>                 # print the skeleton
  python3 _structural_skeleton.py --diff <claude.html> <human.html>   # unified structural diff
  (see _skeleton_compare.py for the corpus-wide similarity measurement)
"""
import sys, re
from html.parser import HTMLParser

VOID = {"img", "br", "input", "col", "hr", "meta", "link", "source", "area", "base", "wbr"}
DROP = {"script", "style", "noscript", "svg", "path"}
KEEP_ATTR = ["number", "layout", "answer", "colour", "color", "role", "data-type"]

# WIDGET subtrees — built (human) or placeholder (Claude). Collapsing these to one
# `WIDGET` marker on BOTH sides isolates the SCAFFOLD (rows/cols/activities/sections +
# widget POSITIONS) from the by-design Phase-1 placeholder gap (we don't build most
# widget internals yet, so comparing them is unfair). Set via skeleton(path, scaffold=True).
WIDGET_MARKERS = {
    "cv2-interactive", "speechBubble", "accordion", "hintSlider", "flipCard", "clickDrop",
    "wordSelect", "wordHighlighter", "reorder", "dropQuiz", "dropDown", "rotateBanner",
    "dragAndDrop", "carousel", "memoryGame", "tabs", "multiChoiceQuiz", "bingo", "radioQuiz",
    "wordDrag", "selfCheck", "modal", "typing", "crossword", "puzzle", "timeline", "bannerContainer",
    "imageZoom", "imageLabel", "sketcher", "diceRoller", "stopWatch", "numberLine", "sliderChart",
}


class Node:
    __slots__ = ("tag", "attrs", "kids")
    def __init__(self, tag, attrs):
        self.tag = tag; self.attrs = attrs; self.kids = []


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {})
        self.stack = [self.root]
        self.skip_depth = 0
    def handle_starttag(self, tag, attrs):
        if self.skip_depth:
            if tag not in VOID: self.skip_depth += 1
            return
        if tag in DROP:
            if tag not in VOID: self.skip_depth = 1
            return
        n = Node(tag, dict(attrs))
        self.stack[-1].kids.append(n)
        if tag not in VOID:
            self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        if self.skip_depth or tag in DROP: return
        self.stack[-1].kids.append(Node(tag, dict(attrs)))
    def handle_endtag(self, tag):
        if self.skip_depth:
            self.skip_depth -= 1; return
        if tag in VOID: return
        # pop to the matching open tag (tolerant of malformed nesting)
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]; break


def label(node):
    s = node.tag
    a = node.attrs
    if a.get("id"): s += "#" + a["id"]
    # ROUND 386 (the autonomous loop's session 24 Round 10 — a measurement-tool round): the class tokens render
    # SORTED. HTML class order carries no structure, but 97 gold pages write `class="col-12 col-md-8"` (366 lines)
    # where Claude writes `col-md-8 col-12`, and the source-order label could never match them — 77 pages moved,
    # 76 up (XDLS906_4_0 +15.1), +0.087pp corpus mean: an instrument correction, never a gain.
    cls = sorted((a.get("class") or "").split())
    if cls: s += "." + ".".join(cls)
    for k in KEEP_ATTR:
        # ROUND 190: `if a[k]` (was `a[k] != ""`) — a VALUELESS/bare attribute (html.parser
        # stores it as None, e.g. the human gold's `<div class="accordion" layout>`) used to
        # pass the guard and crash None.strip(), silently dropping 238 pairs from the PRIMARY
        # gate. A bare attr means "default" and carries no structural information — it now
        # contributes NO token (measured: Claude ships no `layout` on the paired accordions,
        # so both sides agree; gold's VALUED layout=standard/speech/… still renders).
        if k in a and a[k]:
            s += f"[{k}={a[k].strip()}]"
    return s


_SCAFFOLD = False   # module flag: collapse widget subtrees to a single WIDGET marker


def render(node, indent=0):
    """render a node subtree to a list of indented skeleton lines (kids collapsed)."""
    pad = "  " * indent
    if _SCAFFOLD:
        cls = set((node.attrs.get("class") or "").split())
        if cls & WIDGET_MARKERS:
            return [pad + "WIDGET"]
    lines = [pad + label(node)]
    lines += render_children(node.kids, indent + 1)
    return lines


def render_children(kids, indent):
    # round 72 — Claude-only NOTES are skipped: the human strips EVERY comment AND every
    # converter note, so they have no structural counterpart. cv2-comment = whitelisted
    # Word comments; cv2-note = the CS / RED FLAG retained-instruction notes. This brings
    # the skeleton into parity with the text gates (which already exclude "cs "/"red flag")
    # and makes Part B's before-the-box note repositioning structurally inert. Every level.
    _NOTE_CLS = {"cv2-comment", "cv2-note"}
    kids = [k for k in kids if not (_NOTE_CLS & set((k.attrs.get("class") or "").split()))]
    # render each child to its block of lines, then collapse consecutive repeats
    blocks = [render(k, indent) for k in kids]
    out = []
    i = 0
    n = len(blocks)
    pad = "  " * indent
    while i < n:
        # find the smallest K>=1 whose block repeats consecutively from i
        found_k = found_n = 0
        for K in range(1, (n - i) // 2 + 1):
            if blocks[i:i + K] == blocks[i + K:i + 2 * K]:
                N = 2
                while i + (N + 1) * K <= n and blocks[i:i + K] == blocks[i + N * K:i + (N + 1) * K]:
                    N += 1
                found_k, found_n = K, N
                break
        if found_k:
            if found_k == 1:
                out.append(f"{pad}┌ {found_n}× repeated:")
            else:
                out.append(f"{pad}┌ {found_n}× repeated block of {found_k}:")
            for b in blocks[i:i + found_k]:
                out += ["  " + ln for ln in b]   # indent the collapsed block one extra level
            i += found_k * found_n
        else:
            out += blocks[i]
            i += 1
    return out


def body_source(html):
    """ROUND 382 (the autonomous loop's session 24 Round 6 — a measurement-tool round, the r190 / r315 / r355
    class): the page's <body> element as a string, the ONE reader every gate shares. The old idiom
    `<body …>(.*)</body>` fell back to the WHOLE document when it failed: 99 gold pages (the CED NCEA
    family, ENGR202 / 301, MXEO401, XTAS101, MXFU401) have no <body> element at all — <div id="header">
    sits directly under <html> — so their skeleton carried html / head / meta / title lines, and
    BLL144-1.0's <body> has no close tag, so its content sat one level deeper than Claude's and matched
    nothing (4.6 %). Measured over the 96 paired pages: 96 up / 0 down, pp-sum +313 = +0.16pp corpus mean
    — an instrument correction, never a gain. An unclosed <body> runs to the end of the document; a page
    with no body at all is the content after </head> wrapped in a BARE <body> (no class is invented — the
    one line honestly mismatches Claude's body.container-fluid)."""
    m = re.search(r"<body\b[^>]*>(.*)</body>", html, re.S | re.I)
    if m:
        return m.group(0)
    mb = re.search(r"<body\b[^>]*>", html, re.I)
    if mb:
        return re.sub(r"</html>\s*$", "", html[mb.start():].rstrip()) + "</body>"
    mh = re.search(r"</head>", html, re.I)
    tail = html[mh.end():] if mh else html
    tail = re.sub(r"</html>\s*$", "", tail.rstrip())
    return "<body>" + tail + "</body>"



def skeleton(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    src = body_source(html)   # ROUND 382: the shared body reader (was the bare regex + a whole-document fallback)
    tb = TreeBuilder(); tb.feed(src)
    # the <body> node (first body under root) or root's kids
    body = next((k for k in tb.root.kids if k.tag == "body"), None)
    header = ("OSAI401-01.html — Simplified structural skeleton of <body>\n"
              + "=" * 59 + "\nAll rendered text content removed; only HTML tags retained.\n")
    if body is None:
        return "\n".join(render_children(tb.root.kids, 0))
    return "\n".join(render(body, 0))


def main():
    args = sys.argv[1:]
    if args and args[0] == "--diff":
        import difflib
        a = skeleton(args[1]).splitlines()
        b = skeleton(args[2]).splitlines()
        sys.stdout.write("\n".join(difflib.unified_diff(b, a, "human", "claude", lineterm="")) + "\n")
    elif args:
        print(skeleton(args[0]))


if __name__ == "__main__":
    main()
