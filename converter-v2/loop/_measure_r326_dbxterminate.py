#!/usr/bin/env python3
"""ROUND 326 (loop session 4, Round 1 PICK) — DOES THE UPLOAD BUTTON TERMINATE ITS ACTIVITY BOX?

The r0b / Round-1 follow-up ("the dropbox bundle terminates its activity"): the gold keeps the
"Upload to dropbox" button as the activity box's LAST content child in 87% (non-BLL) / 97% (BLL)
of boxes (r314 measurement). After r314 put the button INSIDE the box and r320 restored the
writer's order around it, a Claude box can still carry content AFTER the button (the box stays
open to the next auto-close boundary and swallows the following body). This probe measures, on
the CURRENT corpus:

  GOLD   per template family / subject prefix: boxes holding an upload button — button LAST vs a
         TAIL after it (and what the tail is).
  CLAUDE the population: boxes with a tail after the button; for each tail, where the gold puts
         that text: OUTSIDE the box (→ the box should have closed at the button), INSIDE the
         box after the button (→ gold keeps it — leave alone), or NOWHERE (editorial / dropped).

Notes (cv2-note / cv2-comment) are gate-invisible and are NOT counted as tail content.
Writes outputs/_r326_dbxterminate.json + outputs/_r326_affected.txt (modules whose Claude
pages carry an OUTSIDE-class tail). USAGE: python3 _measure_r326_dbxterminate.py [CODE …]
"""
import os, sys, re, json, unicodedata
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(BASE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)
import _corpus

HUMAN = os.path.join(ROOT, "01-Finalized_Modules_")
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
SKIP_PAGE = re.compile(r"acks|acknowledge|glossary|references", re.I)
BTN = re.compile(r'<div class="(?:button|buttonD|externalButton)[^"]*">\s*(Upload to [Dd]ropbox\.?|Go to [Dd]ropbox\.?|Go to portfolio\.?)\s*</div>')
ACT = re.compile(r'<div class="(activity(?:\s[^"]*)?)"(?:\s+number="([^"]*)")?')
DIV = re.compile(r"<(/?)div\b", re.I)
NOTE = re.compile(r'<div class="cv2-(?:note|comment)[^"]*"')
TAG = re.compile(r"<[^>]+>")


def fold(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", t)).strip()


def div_span(s, start):
    """Return the index just past the </div> that balances the <div at `start`."""
    depth = 0
    for m in DIV.finditer(s, start):
        if m.group(1):
            depth -= 1
            if depth == 0:
                return s.find(">", m.start()) + 1
        else:
            depth += 1
    return len(s)


def strip_notes(s):
    """Remove cv2-note / cv2-comment subtrees (balanced)."""
    out, i = [], 0
    while True:
        m = NOTE.search(s, i)
        if not m:
            out.append(s[i:]); break
        out.append(s[i:m.start()])
        i = div_span(s, m.start())
    return "".join(out)


def top_children(inner):
    """Split a box's inner HTML into top-level element chunks (balanced on div/ol/ul/p/table...)."""
    chunks, i, n = [], 0, len(inner)
    tag = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(/?)>")
    VOID = {"br", "img", "hr", "input", "source", "meta", "link"}
    pos = 0
    while pos < n:
        m = tag.search(inner, pos)
        if not m:
            t = inner[pos:].strip()
            if t: chunks.append(("#text", inner[pos:]))
            break
        if m.start() > pos and inner[pos:m.start()].strip():
            chunks.append(("#text", inner[pos:m.start()]))
        if m.group(1):  # stray close
            pos = m.end(); continue
        name = m.group(2).lower()
        if name in VOID or m.group(3):
            chunks.append((name, inner[m.start():m.end()])); pos = m.end(); continue
        # balance this element by name
        depth, j = 0, m.start()
        sub = re.compile(r"<(/?)%s\b[^>]*>" % re.escape(name), re.I)
        end = None
        for mm in sub.finditer(inner, m.start()):
            if mm.group(1):
                depth -= 1
                if depth == 0:
                    end = mm.end(); break
            else:
                depth += 1
        if end is None: end = n
        chunks.append((name, inner[m.start():end])); pos = end
    return chunks


def boxes(s):
    """Yield (cls, number, inner_html_without_notes) for each activity box on a page."""
    for m in ACT.finditer(s):
        end = div_span(s, m.start())
        open_end = s.find(">", m.end()) + 1
        inner = s[open_end:end]
        inner = inner[: inner.rfind("</div>")] if inner.rstrip().endswith("</div>") else inner
        yield m.group(1), m.group(2) or "", strip_notes(inner), m.start(), end


def analyse_box(inner):
    """Return (has_button, tail_chunks) — tail = top-level chunks after the LAST upload button chunk."""
    kids = [k for k in top_children(inner) if k[1].strip()]
    idx = None
    for i, (name, html) in enumerate(kids):
        if BTN.search(html):
            idx = i
    if idx is None:
        return False, []
    return True, kids[idx + 1:]


def pages(d):
    out = {}
    for f in sorted(os.listdir(d)):
        if not f.lower().endswith(".html") or SKIP_PAGE.search(f):
            continue
        m = re.search(r"[_\-](\d+)[._](\d+)\.html$", f) or re.search(r"[_\-](\d+)\.html$", f)
        if not m: continue
        key = "%s.%s" % (m.group(1), m.group(2)) if m.lastindex == 2 else "%s.0" % m.group(1)
        out[key] = os.path.join(d, f)
    return out


def main(argv):
    codes = argv or _corpus.mods(HUMAN)
    gold_stats = defaultdict(Counter)   # group -> {last, tail}
    gold_tail_kinds = Counter()
    claude_rows = []
    claude_stats = defaultdict(Counter)
    affected = set()
    for code in codes:
        hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
        if not (os.path.isdir(hd) and os.path.isdir(cd)):
            continue
        tmpl = os.path.basename(os.path.dirname(hd))
        prefix = re.match(r"[A-Z]+", code).group(0) if re.match(r"[A-Z]+", code) else code
        grp = "%s|%s" % (tmpl, "BLL" if prefix == "BLL" else "nonBLL")
        gp, cp = pages(hd), pages(cd)
        for key, path in gp.items():
            s = open(path, encoding="utf-8", errors="replace").read()
            for cls, num, inner, a, b in boxes(s):
                hb, tail = analyse_box(inner)
                if not hb: continue
                if tail:
                    gold_stats[grp]["tail"] += 1
                    gold_tail_kinds[",".join(k[0] for k in tail[:3])] += 1
                else:
                    gold_stats[grp]["last"] += 1
        for key, path in cp.items():
            s = open(path, encoding="utf-8", errors="replace").read()
            gpath = gp.get(key)
            gs = open(gpath, encoding="utf-8", errors="replace").read() if gpath else ""
            gs_boxes = list(boxes(gs)) if gs else []
            gfold = fold(TAG.sub(" ", gs)) if gs else ""
            for cls, num, inner, a, b in boxes(s):
                hb, tail = analyse_box(inner)
                if not hb: continue
                if not tail:
                    claude_stats[grp]["last"] += 1
                    continue
                claude_stats[grp]["tail"] += 1
                # where does the gold put the tail's first text?
                ttxt = fold(TAG.sub(" ", " ".join(k[1] for k in tail)))
                probe = " ".join(ttxt.split()[:8])
                where = "no-gold-page" if not gs else "nowhere"
                if gs and probe and probe in gfold:
                    where = "outside"
                    for gcls, gnum, ginner, ga, gb in gs_boxes:
                        gi = fold(TAG.sub(" ", ginner))
                        if probe in gi:
                            ghb, gtail = analyse_box(ginner)
                            gtf = fold(TAG.sub(" ", " ".join(k[1] for k in gtail))) if gtail else ""
                            where = "inside-after-button" if (ghb and probe in gtf) else "inside-other-box"
                            break
                claude_stats[grp][where] += 1
                if where == "outside":
                    affected.add(code)
                claude_rows.append({"code": code, "page": os.path.basename(path), "tmpl": tmpl, "box": num or cls,
                                    "tail_tags": [k[0] for k in tail], "tail_len": len(ttxt),
                                    "tail_text": ttxt[:120], "gold": where})
    res = {"gold_by_group": {g: dict(c) for g, c in gold_stats.items()},
           "gold_tail_shapes_top": gold_tail_kinds.most_common(15),
           "claude_by_group": {g: dict(c) for g, c in claude_stats.items()},
           "claude_tail_rows": claude_rows,
           "affected_modules": sorted(affected)}
    tot_g = Counter()
    for c in gold_stats.values(): tot_g.update(c)
    tot_c = Counter()
    for c in claude_stats.values(): tot_c.update(c)
    res["gold_total"] = dict(tot_g); res["claude_total"] = dict(tot_c)
    pages_aff = len({(r["code"], r["page"]) for r in claude_rows if r["gold"] == "outside"})
    res["outside_pages"] = pages_aff
    with open(os.path.join(BASE, "_r326_dbxterminate.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    with open(os.path.join(BASE, "_r326_affected.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(affected)) + "\n")
    print("GOLD boxes with upload button:", dict(tot_g))
    for g, c in sorted(gold_stats.items()):
        n = c["last"] + c["tail"]
        print("  %-24s last %4d / %4d = %.2f" % (g, c["last"], n, c["last"] / n if n else 0))
    print("GOLD tail shapes:", gold_tail_kinds.most_common(8))
    print("CLAUDE boxes with upload button:", dict(tot_c))
    for g, c in sorted(claude_stats.items()):
        print("  %-24s" % g, dict(c))
    print("CLAUDE tail rows:", len(claude_rows), "| gold-OUTSIDE pages:", pages_aff, "| modules:", len(affected))


if __name__ == "__main__":
    main(sys.argv[1:])
