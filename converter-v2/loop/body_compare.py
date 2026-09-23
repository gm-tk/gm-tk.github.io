"""body_compare.py — per-page #body content-PLACEMENT comparison: Claude vs human.

WHY (Chris, 2026-06-15): the scaffold audit measures structure counts; this finds
whole PAGES that break down — where the converter mis-bounds the writer content so
an interactive widget OVER-CAPTURES the rest of the page, leaves an EMPTY container,
or buries free body text inside a widget the human renders as free body. The
XGF9001-00 page is the exemplar (flipCard #3 swallowed the rest of the page).

It compares text VOLUME and PLACEMENT (not exact wording), so on-the-fly writer
edits don't break it. The key trick: both sides EXCLUDE interactive/widget subtrees
when counting "free body" blocks, so we measure how much free body the converter
LOST into a widget vs the human.

PER PAGE (Claude vs the matching human page), inside #body:
  • over_capture  — fraction of the page's body text held by the SINGLE largest
    interactive placeholder (.cv2-interactive). Runaway widget = high.
  • multi_type    — how many DISTINCT widget types the biggest placeholder absorbed
    (its banner "type: A + B + C …"). A bundle that ate 6 widget types is a runaway.
  • lost_blocks   — human free-body blocks minus Claude free-body blocks (both
    EXCLUDING widget subtrees). High = the converter pulled free body into a widget.
  • empty_widgets — placeholders with no member content (just the banner).

A page is BROKEN when a widget over-captures AND the human keeps that content as
free body (lost_blocks high) — which rules out legitimately single-widget pages.

USAGE:  python3 body_compare.py            (all pages)  |  python3 body_compare.py XGF9001 …
Writes body_compare.json and prints the worst-broken pages + the totals.
"""
import json
import _corpus  # round128: nesting-aware corpus paths
import os
import re
import sys
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.abspath(__file__))
CLAUDE = os.path.join(BASE, "..", "..", "..", "01-Claude_Modules_")
HUMAN = os.path.join(BASE, "..", "..", "..", "01-Finalized_Modules_")
DATA = os.path.join(BASE, "..", "..", "data")

# widget classes to exclude when counting FREE body (rendered human widgets +
# the converter's placeholder). Built from the wrapper catalogue + the obvious extras.
wrap = json.load(open(os.path.join(DATA, "Interactive_Wrapper_Catalogue.json")))
WIDGET = {"cv2-interactive"}
for it in wrap["interactives"]:
    for c in it.get("classes", []):
        WIDGET.add(c)
    for v in it.get("variants", []):
        for c in v.get("classes", []):
            WIDGET.add(c)
WIDGET |= {"flipCardsContainer", "flipCard", "bannerContainer", "rotateBanner", "carousel",
           "wordHighlighter", "bubble-basic", "speechBubble", "accordion", "hintSlider", "tabs",
           "dropContainer", "dragContainer", "question", "clickDropContent", "engagementTrigger",
           "memCard", "wordSearch", "crossword", "selfCheck", "sketcher", "audioTrigger", "infoTrigger"}
WIDGET = {c for c in WIDGET if not c.startswith("col-")
          and c not in {"row", "img-fluid", "table", "table-responsive", "ratio", "ratio-16x9",
                        "videoSection", "button", "buttonS", "buttonT", "d-block", "w-100",
                        "img-thumbnail", "alert", "important", "whakatauki"}}

VOID = {"img", "br", "meta", "link", "input", "hr", "source", "wbr"}
BLOCK = {"p", "h1", "h2", "h3", "h4", "h5", "ul", "ol", "li"}
BANNER_RE = re.compile(r"INTERACTIVE \(un-built\) #\d+: ([^—]+)")
# ROUND 235 — the hand-off wrapper's reference-code label (chrome, not member content)
REF_LABEL_RE = re.compile(r"[A-Z][A-Z0-9]*-INT-\d{2,}-\d{2,}-[A-Za-z][A-Za-z0-9]*")


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9āēīōū ]", "", s.lower())).strip()


# round 72 — whitelisted Word-comment notes ("<Author>: …", class cv2-comment) are
# Claude-only (the human strips every comment) → not counted as free body content.
# round 219 — the ledger note scheme (CL-0010) renders them "Note from <Author>: …";
# the "note from" lead is excluded too, the bare author names kept for a
# NOTESCHEME_OFF (legacy-form) corpus. Parity: keep both, never drop either.
CV2_COMMENT_AUTHORS = ("note from", "kate scanlon", "nadia stanton", "caroline schwer",
                       "simon vita", "amanda griffiths", "creative services",
                       # ROUND 235 REPAIR — CLAUDE.md §9 has always documented that this
                       # gate excludes Claude's converter-added notes from the text match
                       # (the human strips them, so they have no counterpart); the tuple
                       # only ever carried the Word-comment author subset. The r235
                       # hand-off wrapper moved the lead notes INSIDE the (excluded)
                       # wrapper, which exposed the gap: a "Writers Note:" lead counted
                       # as a Claude free block before the round and not after, shifting
                       # lost_blocks by pure note relocation. Completing the documented
                       # prefix set makes both states count identically (r219 prefixes +
                       # the legacy forms, folded):
                       "writers note", "red flag", "designerdeveloper to do",
                       "cs ", "cs:", "red flag:")


class Body(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.in_body = None
        self.widget = None       # depth of the nearest widget subtree (any WIDGET class)
        self.cv2 = None          # depth of the nearest .cv2-interactive (Claude placeholder)
        self.cv2_id = 0
        self.cv2_key = None
        self.cv2_text = {}       # placeholder -> member chars (excl banner)
        self.cv2_banner = {}     # placeholder -> banner type string
        self.free_blocks = []    # free-body text blocks (OUTSIDE any widget)
        self.all_chars = 0
        self._buf = []
        self._banner_pending = False
        self._note = None        # depth of a cv2-note/cv2-comment <p> inside the cv2 wrapper (r235)

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        eid = a.get("id") or ""
        self.stack.append(tag)
        if eid == "body":
            self.in_body = len(self.stack) - 1
            return
        if self.in_body is None:
            return
        if self.cv2 is None and "cv2-interactive" in cls:
            self.cv2 = len(self.stack) - 1
            self.cv2_id += 1
            self.cv2_key = self.cv2_id
            self.cv2_text.setdefault(self.cv2_key, 0)
        if self.widget is None and any(c in WIDGET for c in cls):
            self.widget = len(self.stack) - 1
        # ROUND 235 REPAIR (with the label/arrow skip in handle_data): a retained
        # writer-instruction note (cv2-note / cv2-comment) inside the hand-off
        # wrapper used to sit OUTSIDE the box (the r72 lead position) where its
        # text never counted as cv2 member content — keep that exclusion now the
        # note travels inside the wrapper.
        if self.cv2 is not None and self._note is None and tag == "p" and any("cv2-note" in c or "cv2-comment" in c for c in cls):
            self._note = len(self.stack) - 1
        if self.cv2 is not None and tag == "p":
            self._banner_pending = True

    def handle_data(self, data):
        if self.in_body is None:
            return
        t = data.strip()
        if not t:
            return
        if self.cv2 is not None and self._banner_pending:
            mt = BANNER_RE.search(t)
            if mt:
                self.cv2_banner[self.cv2_key] = mt.group(1)
                self._banner_pending = False
                return
            self._banner_pending = False
        # ROUND 235 REPAIR (the r190/defect-audit tool-repair class): the hand-off
        # wrapper's own chrome — the reference-code label ("CODE-INT-NN-SS-type")
        # and the ▼/▲ expand/collapse arrow — is box FURNITURE, not captured member
        # content. Counting it as cv2 member text masked genuinely-EMPTY boxes and
        # inflated over-capture shares; skip it so this gate keeps measuring
        # exactly what it measured before the wrapper existed.
        if self.cv2 is not None and (REF_LABEL_RE.fullmatch(t) or t in ("▼", "▲")):
            return
        self.all_chars += len(t)
        if self.cv2 is not None and self._note is None:
            self.cv2_text[self.cv2_key] += len(t)
        if self.widget is None:          # genuinely free body
            self._buf.append(t)

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        if self.widget is None and tag in BLOCK and self._buf:
            blk = norm(" ".join(self._buf))
            if len(blk) >= 3 and not blk.startswith(CV2_COMMENT_AUTHORS):
                self.free_blocks.append(blk)
            self._buf = []
        while self.stack:
            tt = self.stack.pop()
            depth = len(self.stack)
            if self._note is not None and depth <= self._note:
                self._note = None
            if self.cv2 is not None and depth <= self.cv2:
                self.cv2 = None
                self.cv2_key = None
            if self.widget is not None and depth <= self.widget:
                self.widget = None
            if self.in_body is not None and depth <= self.in_body:
                self.in_body = None
            if tt == tag:
                break


def parse(path):
    p = Body()
    try:
        p.feed(open(path, encoding="utf8", errors="ignore").read())
    except Exception:
        pass
    return p


def pkey(name):
    m243 = re.search(r"_(\d+)_(\d+(?:_\d+)*)\.html$", name)   # ROUND 243: the library-form name CODE_L_S.html
    if m243:                                                    # (both sides may carry it now)
        return float(f"{m243.group(1)}.{m243.group(2).split('_')[0]}")
    nums = re.findall(r"(\d+(?:\.\d+)?)", name.rsplit("-", 1)[-1].rsplit("_", 1)[-1])
    return float(nums[0]) if nums else 0


def main():
    mods = sys.argv[1:] or sorted(d for d in _corpus.gate_mods(CLAUDE)   # r343: minus compare_exclusions.txt
                                  if os.path.isdir(_corpus.mdir(CLAUDE, d)))
    out = []
    for mod in mods:
        cdir, hdir = _corpus.mdir(CLAUDE, mod), _corpus.mdir(HUMAN, mod)
        if not os.path.isdir(cdir) or not os.path.isdir(hdir):
            continue
        cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=pkey)
        # ROUND 440 (D13-6): the gold listing goes through compare_gold_pages.txt (_corpus.gold_pages; GOLDPAGES_OFF=1 = all).
        hpages = sorted(_corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=pkey)
        hparsed = [parse(os.path.join(hdir, f)) for f in hpages]
        for i, cf in enumerate(cpages):
            cp = parse(os.path.join(cdir, cf))
            hp = hparsed[i] if i < len(hparsed) else None
            total = max(1, cp.all_chars)
            wvals = list(cp.cv2_text.values())
            max_w = max(wvals) if wvals else 0
            big_key = max(cp.cv2_text, key=cp.cv2_text.get) if cp.cv2_text else None
            big_banner = cp.cv2_banner.get(big_key, "")
            multi = len(set(t.strip() for t in big_banner.split("+"))) if big_banner else 0
            empty = sum(1 for v in wvals if v < 40)
            hfree = len(hp.free_blocks) if hp else 0
            lost = hfree - len(cp.free_blocks)
            out.append({
                "page": f"{mod}/{cf}", "module": mod,
                "over_capture": round(max_w / total, 2), "biggest_widget_chars": max_w,
                "multi_type": multi, "n_widgets": len(wvals), "empty_widgets": empty,
                "claude_free_blocks": len(cp.free_blocks), "human_free_blocks": hfree,
                "lost_blocks": lost, "biggest_banner": big_banner.strip()[:60],
            })
    json.dump(out, open(os.path.join(BASE, "body_compare.json"), "w"), indent=1)

    def flags(r):
        f = []
        if r["over_capture"] >= 0.40 and r["biggest_widget_chars"] > 400 and r["lost_blocks"] >= 3:
            f.append(f"OVER-CAPTURE {int(r['over_capture']*100)}% (human keeps {r['lost_blocks']} blocks free)")
        if r["multi_type"] >= 4:
            f.append(f"ABSORBED {r['multi_type']} widget types")
        if r["empty_widgets"]:
            f.append(f"{r['empty_widgets']} EMPTY widget(s)")
        return f

    rows = [(r, flags(r)) for r in out]
    broken = [(r, f) for r, f in rows if f]
    # rank: real over-captures first (by lost_blocks), then multi-type, then empties
    broken.sort(key=lambda x: (-(x[0]["lost_blocks"] if x[0]["over_capture"] >= 0.4 else 0),
                               -x[0]["multi_type"], -x[0]["empty_widgets"]))
    n = len(out)
    n_over = sum(1 for r in out if r["over_capture"] >= 0.4 and r["biggest_widget_chars"] > 400 and r["lost_blocks"] >= 3)
    n_multi = sum(1 for r in out if r["multi_type"] >= 4)
    n_empty = sum(1 for r in out if r["empty_widgets"])
    print(f"BODY-CONTENT BREAKDOWN — {n} pages compared (free-body excludes widget subtrees both sides)")
    print(f"  OVER-CAPTURE (a widget ate body the human keeps free): {n_over} pages")
    print(f"  RUNAWAY ABSORPTION (one widget absorbed >=4 types):     {n_multi} pages")
    print(f"  EMPTY interactive container:                            {n_empty} pages")
    print(f"  pages with ANY breakdown flag:                          {len(broken)}\n")
    print("WORST-BROKEN PAGES (top 30):")
    for r, f in broken[:30]:
        print(f"  {r['page']:30} | {'; '.join(f)}")
    # module-level rollup
    bymod = {}
    for r, f in broken:
        bymod.setdefault(r["module"], 0)
        bymod[r["module"]] += 1
    print("\nMODULES WITH THE MOST BROKEN PAGES:")
    for m, c in sorted(bymod.items(), key=lambda x: -x[1])[:15]:
        print(f"  {m}: {c} broken page(s)")


if __name__ == "__main__":
    main()
