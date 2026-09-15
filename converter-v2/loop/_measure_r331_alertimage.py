#!/usr/bin/env python3
"""_measure_r331_alertimage.py — ROUND 331 (loop session 5, Round 2) measurement probe: the human's ACTIVITY IMAGE
SIDEBAR (`row > col-md-8 [activity …] + col-md-4 offset-md-0 > div.alertImage > img`; KB 05B "Activity + AlertImage
Pairing", 02B "Interactive activity + alertImage pairing") — 332 gold pages, Claude 0.

WHAT IT MEASURES, page-paired through the gate's own pairing (`_discrepancy_audit.pairs`):
  GOLD side, per alertImage sidebar: the sibling column's activity (number=, classes: dropbox / interactive /
    alertPadding), how many <img> the activity itself still holds, the sidebar image's src.
  CLAUDE side, per activity box (cv2 dumps excluded): number=, classes, the <img> count inside the box and
    WHERE the last image sits (last content child before the button / elsewhere), whether the box holds a
    dropbox button.
  THE CROSS-TAB (matched by number=): of the gold sidebar activities, how many Claude boxes hold an image
    (RECALL of "image inside the box" as the signal); of the Claude boxes holding an image, how many gold
    activities carry a sidebar (PRECISION) — split by dropbox / interactive / plain, per template folder.
Paths are dynamic (CLAUDE.md §13). Run from anywhere:  python3 _measure_r331_alertimage.py
Writes _r331_alertimage.json next to itself and prints the summary.
"""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
from anchor_compare import HUMAN

def balanced(s, start):
    """index just past the </div> that closes the <div at `start`."""
    depth = 0; i = start
    for m in re.finditer(r"<div\b|</div>", s[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0: return start + m.end()
    return len(s)

def strip_cv2(s):
    out = []; i = 0
    while True:
        m = re.search(r'<div class="[^"]*cv2-interactive[^"]*"', s[i:])
        if not m: out.append(s[i:]); break
        st = i + m.start(); out.append(s[i:st]); i = balanced(s, st)
    return "".join(out)

def body(s):
    return s.split('<div id="body"', 1)[1] if '<div id="body"' in s else s

def activities(html):
    """[(number, classes, inner_html)] for every <div class="…activity…"> box."""
    res = []
    for m in re.finditer(r'<div class="([^"]*\bactivity\b[^"]*)"([^>]*)>', html):
        n = re.search(r'number="([^"]*)"', m.group(2)); end = balanced(html, m.start())
        res.append((n.group(1) if n else None, m.group(1), html[m.end():end]))
    return res

def gold_sidebars(html):
    """[(activity number, activity classes, imgs inside the activity, sidebar img src)] per alertImage."""
    out = []
    for m in re.finditer(r'<div class="col-md-[34][^"]*"[^>]*>\s*<div class="alertImage">', html):
        st = m.start(); end = balanced(html, st)
        src = re.search(r'<img[^>]*src="([^"]*)"', html[st:end]); src = src.group(1) if src else ""
        # the sibling column BEFORE this one in the same row: find the enclosing row start
        # the innermost <div class="row"> that ENCLOSES the sidebar column (skip rows already closed before it)
        row_st = html.rfind('<div class="row">', 0, st)
        while row_st >= 0 and balanced(html, row_st) <= st:
            row_st = html.rfind('<div class="row">', 0, row_st)
        if row_st < 0: row_st = 0
        seg = html[row_st:st]
        acts = activities(seg)
        if acts:
            n, cls, inner = acts[0]
            out.append((n, cls, len(re.findall(r"<img\b", inner)), src, "before"))
        else:
            # the activity may follow the sidebar (image-first rows)
            after = html[end:balanced(html, row_st)]
            acts = activities(after)
            if acts:
                n, cls, inner = acts[0]; out.append((n, cls, len(re.findall(r"<img\b", inner)), src, "after"))
            else:
                out.append((None, "(no activity in row)", 0, src, "none"))
    return out

def claude_boxes(html):
    html = strip_cv2(html); out = []
    for n, cls, inner in activities(html):
        imgs = re.findall(r"<img\b[^>]*>", inner)
        has_btn = bool(re.search(r'class="button', inner))
        # is the last image the last content element before a trailing button / the box end?
        tail = re.sub(r"<(/?)(div|a)\b[^>]*>", "", inner)   # drop wrappers
        tail_els = re.findall(r"<(h[1-6]|p|ul|ol|img|table|iframe|audio|video)\b", tail)
        last_is_img = bool(tail_els) and tail_els[-1] == "img"
        # image immediately followed only by the button anchor(s)
        m = re.search(r"<img\b[^>]*>(?:\s*</div>)*\s*(?:<a [^>]*>\s*<div class=\"button[^\"]*\">[^<]*</div>\s*</a>\s*)+\s*(?:</div>\s*)*$", inner)
        out.append((n, cls, len(imgs), has_btn, last_is_img, bool(m)))
    return out

def main():
    codes = sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
    rows = []; gold_total = collections.Counter(); tmpl_of = {}
    cross = collections.defaultdict(collections.Counter)   # tmpl -> outcome counter
    gold_cls = collections.Counter(); gold_imgs_inside = collections.Counter(); gold_pos = collections.Counter()
    claude_img_boxes = collections.defaultdict(collections.Counter)
    for code in codes:
        cdir = _corpus.mdir(CLAUDE, code); tmpl = os.path.basename(os.path.dirname(cdir)); tmpl_of[code] = tmpl
        for n, cp, hp in pairs(code):
            if re.search(r'acks|acknowledge|glossary', os.path.basename(hp), re.I): continue
            g = body(open(hp, encoding="utf-8", errors="replace").read())
            c = body(open(cp, encoding="utf-8", errors="replace").read())
            gs = gold_sidebars(g); cb = claude_boxes(c)
            gold_total[tmpl] += len(gs)
            gmap = {x[0]: x for x in gs if x[0]}
            cmap = {x[0]: x for x in cb if x[0]}
            for gn, gcls, gimgs, src, pos in gs:
                kind = "dropbox" if "dropbox" in gcls else "interactive" if "interactive" in gcls else "plain"
                gold_cls[(tmpl, kind)] += 1; gold_imgs_inside[gimgs > 0] += 1; gold_pos[pos] += 1
                cx = cmap.get(gn)
                if cx is None: cross[tmpl]["gold sidebar: no Claude box with that number"] += 1
                elif cx[2] > 0: cross[tmpl]["gold sidebar: Claude box HOLDS an image (recall hit)"] += 1
                else: cross[tmpl]["gold sidebar: Claude box holds NO image (writer image elsewhere / none)"] += 1
                rows.append({"code": code, "page": os.path.basename(cp), "gold_num": gn, "gold_cls": gcls, "gold_imgs_inside": gimgs, "src": src,
                             "pos": pos, "claude": cx})
            for cn, ccls, cimgs, has_btn, last_img, img_then_btn in cb:
                if cimgs == 0: continue
                kind = "dropbox" if "dropbox" in ccls else "interactive" if "interactive" in ccls else "plain"
                gx = gmap.get(cn)
                claude_img_boxes[tmpl][(kind, "img-then-button" if img_then_btn else "last-is-img" if last_img else "img-elsewhere", "gold SIDEBAR" if gx else "gold no sidebar")] += 1
    print("GOLD alertImage sidebars on paired pages, per template:", dict(gold_total))
    print("  sibling activity kind:", {f"{t}/{k}": v for (t, k), v in sorted(gold_cls.items())})
    print("  gold activity still holds an <img> inside:", dict(gold_imgs_inside), "| sidebar position vs activity:", dict(gold_pos))
    print("\nCROSS-TAB (matched by number=):")
    for t, cnt in sorted(cross.items()):
        for k, v in cnt.most_common(): print(f"  {t:12} {v:5}  {k}")
    print("\nCLAUDE boxes holding an image (cv2 dumps excluded) — kind / image position / gold outcome:")
    for t, cnt in sorted(claude_img_boxes.items()):
        for k, v in sorted(cnt.items(), key=lambda x: -x[1]): print(f"  {t:12} {v:5}  {k}")
    json.dump({"gold_total": dict(gold_total), "rows": rows,
               "claude_img_boxes": {t: {" | ".join(k): v for k, v in c.items()} for t, c in claude_img_boxes.items()}},
              open(os.path.join(HERE, "_r331_alertimage.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote _r331_alertimage.json")

if __name__ == "__main__":
    main()
