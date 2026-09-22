#!/usr/bin/env python3
"""Session 35 Round 1 PICK measurement — A PANEL OPENER SWALLOWED BY AN OPEN WIDGET BOX.
For every Claude page carrying the inquiry shell (div.crumbs), take the gold's crumb labels that Claude's crumbs lack and
say WHERE that label's text sits on Claude's page: inside a `cv2-interactive` hand-off box (SWALLOWED), inside a built
widget, as ordinary body text in an earlier panel (MERGED), or nowhere. Also scans EVERY Claude page (not only the shell
pages) for a `[Tab N]` / `[New side tab]` / `[Phase N]` opener line that the writer typed and that now sits inside a
hand-off box as `<p><b>label</b></p>` — the scanner's capture ran through a page-structure marker.
Run under WSL: python3 _s35_r1_swallowtab.py
"""
import re, os, glob, html, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"

def crumb_labels(h):
    m = re.search(r'<div class="crumbs"[^>]*>(.*?)</div>\s*(?:<div class="inquiryPanel|<div class="row|<div class="col)', h, re.S)
    if not m:
        return []
    labs = []
    for d in re.findall(r'<div\b[^>]*>(.*?)</div>', m.group(1), re.S):
        t = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', d))).strip()
        labs.append(t)
    return labs

def norm(s):
    return re.sub(r'[^a-z0-9āēīōū]+', '', s.lower())

def boxes(h):
    """(start, end) spans of every cv2-interactive hand-off box (depth-tracked)."""
    out = []
    for m in re.finditer(r'<div class="cv2-interactive"', h):
        i = m.start(); depth = 0; j = i
        for t in re.finditer(r'<div\b|</div>', h[i:]):
            if t.group(0) == '</div>':
                depth -= 1
                if depth == 0:
                    j = i + t.end(); break
            else:
                depth += 1
        out.append((i, j))
    return out

def where(h, label):
    n = norm(label)
    if not n:
        return 'empty'
    # find the label as the full text of a p / h element — every match; a box hit wins
    bx = boxes(h); found = None
    for m in re.finditer(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', h, re.S):
        t = norm(re.sub(r'<[^>]+>', ' ', m.group(2)))
        if t == n:
            pos = m.start()
            if any(a <= pos < b for a, b in bx):
                return 'SWALLOWED-in-box'
            found = 'in-body'
    if found:
        return found
    if n in norm(h):
        return 'in-text (not an element)'
    return 'nowhere'

per_module = collections.OrderedDict()
by_where = collections.Counter()
for gdir in sorted(glob.glob(R + "01-Finalized_Modules_/*/*/")):
    code = os.path.basename(gdir.rstrip("/"))
    tmpl = gdir.rstrip("/").split("/")[-2]
    cdir = (glob.glob(R + "01-Claude_Modules_/*/" + code + "/") or [None])[0]
    if not cdir:
        continue
    gpages = [p for p in sorted(glob.glob(gdir + "*.html")) if "acks" not in os.path.basename(p).lower()]
    cpages = [p for p in sorted(glob.glob(cdir + "*.html")) if "acks" not in os.path.basename(p).lower()]
    gshell = [(p, open(p, encoding="utf-8", errors="replace").read()) for p in gpages]
    gshell = [(p, h) for p, h in gshell if 'class="crumbs"' in h]
    cshell = [(p, open(p, encoding="utf-8", errors="replace").read()) for p in cpages]
    cshell = [(p, h) for p, h in cshell if 'class="crumbs"' in h]
    if not gshell or not cshell:
        continue
    # pair by page index when both are multi-page, else single ↔ first
    pairs = []
    if len(gshell) == 1 or len(cshell) == 1:
        pairs = [(gshell[0], cshell[0])]
    else:
        def key(p):
            m = re.search(r'_(\d+)[._](\d+)\.html$', os.path.basename(p))
            return (int(m.group(1)), int(m.group(2))) if m else (99, 99)
        gm = {key(p): (p, h) for p, h in gshell}
        cm = {key(p): (p, h) for p, h in cshell}
        for k in gm:
            if k in cm:
                pairs.append((gm[k], cm[k]))
    for (gp, gh), (cp, ch) in pairs:
        gl = crumb_labels(gh); cl = crumb_labels(ch)
        cset = {norm(x) for x in cl}
        gonly = [x for x in gl if norm(x) and norm(x) not in cset and len(x) < 60]
        gpan = len(re.findall(r'<div class="inquiryPanel', gh)); cpan = len(re.findall(r'<div class="inquiryPanel', ch))
        if gpan == cpan or not gonly:
            continue
        for x in gonly:
            w = where(ch, x)
            by_where[w] += 1
            per_module.setdefault(code, []).append((os.path.basename(cp), x, w))

print("=== gold-only crumb labels on PANELS-DIFF pages, by where the text sits on Claude's page ===")
for k, v in by_where.most_common():
    print("  %-26s %d" % (k, v))
print()
for code, items in per_module.items():
    print("== " + code)
    for pg, x, w in items:
        print("   %-22s %-26s «%s»" % (pg[:22], w, x[:60]))

# corpus-wide: an opener typed by the writer that now sits inside a hand-off box
print()
print("=== corpus-wide: writer opener lines inside a Claude hand-off box (every page) ===")
OPEN = re.compile(r'\[\s*(?:tab|new side tab|new tab|phase|lesson)\s*\d*\s*\]', re.I)
hits = collections.Counter(); ex = []
for cdir in sorted(glob.glob(R + "01-Claude_Modules_/*/*/")):
    code = os.path.basename(cdir.rstrip("/"))
    gdir = (glob.glob(R + "01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    if not gdir:
        continue
    wt = ""
    for t in glob.glob(gdir + "*parsed.txt"):
        wt += open(t, encoding="utf-8", errors="replace").read()
    # body openers: a [Tab N] red tag followed by a label on the same line
    openers = []
    for line in wt.split("\n"):
        m = re.search(r'\[/RED TEXT\]\s*🔴?\s*(.+)$', line)
        if m and OPEN.search(line):
            lab = re.sub(r'\*+', '', m.group(1)).strip()
            if lab and not OPEN.search(lab):
                openers.append(lab)
    if not openers:
        continue
    for cp in glob.glob(cdir + "*.html"):
        if "acks" in os.path.basename(cp).lower():
            continue
        ch = open(cp, encoding="utf-8", errors="replace").read()
        bx = boxes(ch)
        if not bx:
            continue
        for lab in openers:
            n = norm(lab)
            if len(n) < 4:
                continue
            for m in re.finditer(r'<p><b>([^<]*)</b></p>', ch, re.S):
                if norm(m.group(1)) == n:
                    if any(a <= m.start() < b for a, b in bx):
                        hits[code] += 1
                        if len(ex) < 40:
                            ex.append((code, os.path.basename(cp), lab))
                        break
print("modules with ≥ 1 swallowed opener:", len(hits), "— openers swallowed:", sum(hits.values()))
for code, pg, lab in ex:
    print("   %-10s %-24s «%s»" % (code, pg[:24], lab[:50]))
