#!/usr/bin/env python3
"""Session 37 Round 1 — THE ACTIVITY-BOX BOUNDARY, MEASURED AS A BOUNDARY (the corrected instrument).

WHY THIS EXISTS. Session 36's `_s36_r7_actbound.py` and this session's first attempt
(`_s37_r1_actclose.py`) both compared the SET OF ELEMENTS in a paired activity box. That conflates two
completely different things:

  * a genuine BOUNDARY defect — the box opens or closes in the wrong place, so text that belongs
    inside it is outside (or the reverse); and
  * a PARAGRAPH-SPLITTING difference — exactly the same text is inside both boxes, but one side
    breaks it into two `<p>` and the other into one, so every element hashes differently.

The second is not a boundary defect at all, and it is the larger population. ANZH101_2_0's «Tessellations»
box is the worked example: it was reported as over-capture with an "extra" first element, but the gold's
2D box carries that sentence too — the gold folds three sentences into one `<p>` and Claude splits them.
That is why both earlier instruments called this population "diffuse": they were measuring the wrong thing.

So compare the box's CONCATENATED TEXT, which is what a boundary actually moves:

    identical              — same text, same split                (nothing wrong)
    same text, split N/M   — same text, different paragraphing    (NOT a boundary defect)
    ends LATE              — Claude's text starts with the gold's and runs on past its end
    ends EARLY             — the gold's text starts with Claude's and Claude stops short
    starts EARLY           — Claude's text ends with the gold's and reaches back before its start
    starts LATE            — the gold's text ends with Claude's and Claude begins after its start
    both ends / disjoint   — neither is a prefix or suffix of the other

Only the four middle verdicts are boundary defects. Each is then keyed on the WRITER'S TAG at the seam —
for an end defect, the last structural tag before the first differing text; that is the shape that
decided the boundary, and it is what a converter rule has to key on.

Run under WSL:  python3 _s37_r1_actbound2.py
"""
import re, os, sys, glob, html, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus


def norm(s):
    return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


TEXT = re.compile(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
TAG = re.compile(r'\[([^\[\]\n]{1,60})\]')
INLINE = {"red text", "/red text", "bold", "/bold", "italic", "/italic", "italics", "/italics",
          "underline", "/underline", "highlight", "/highlight", "link", "hyperlink", "url",
          "correct", "correct answer", "incorrect", "answer", "caption", "alt text", "alt",
          "front", "back", "hover", "important", "bold text", "/bold text", "colour", "color"}


def fold_tag(t):
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.split(r'[:;]', t)[0].strip()
    t = re.sub(r'\b\d+[A-Za-z]?\b', 'N', t)
    return t.lower()


def boxes(s):
    out = []
    for m in re.finditer(r'<div[^>]*class="[^"]*\bactivity\b[^"]*"[^>]*>', s):
        start = m.end()
        depth = 1
        i = len(s)
        for t in re.finditer(r'<div\b[^>]*>|</div>', s[start:]):
            depth += 1 if t.group(0) != "</div>" else -1
            if depth == 0:
                i = start + t.start()
                break
        sub = s[start:i]
        texts = [norm(x.group(2)) for x in TEXT.finditer(sub) if len(norm(x.group(2))) >= 8]
        title = next((norm(x.group(2)) for x in TEXT.finditer(sub) if x.group(1).startswith("h")), "")
        out.append((title, texts))
    return out


def wt_text(code):
    gdir = (glob.glob(ROOT + "/01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    if not gdir:
        return ""
    buf = []
    for t in sorted(glob.glob(gdir + "*parsed.txt")):
        b = os.path.basename(t)
        if re.search(r'media\s*list', b, re.I) and not re.search(r'writer', b, re.I):
            continue
        buf.append(open(t, encoding="utf-8", errors="replace").read())
    return "\n".join(buf)


def wt_lines(wt):
    out, pos = [], 0
    for line in wt.split("\n"):
        n = norm(TAG.sub(' ', line))
        if len(n) >= 8:
            out.append((n, pos))
        pos += len(line) + 1
    return out


def locate(index, needle):
    if len(needle) < 12:
        return None
    for n, p in index:
        if n == needle:
            return p
    for n, p in index:
        if needle[:60] in n or (len(n) >= 20 and n in needle):
            return p
    return None


def struct_tag(wt, off):
    ts = [fold_tag(t) for t in TAG.findall(wt[:off])]
    return next((t for t in reversed(ts) if t not in INLINE), None)


verdict = collections.Counter()
vmods = collections.defaultdict(set)
seam = collections.defaultdict(collections.Counter)
seam_mods = collections.defaultdict(lambda: collections.defaultdict(set))
ex = collections.defaultdict(list)
splitform = collections.Counter()

codes = sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")})
for code in codes:
    try:
        pl = pairs(code)
    except Exception:
        continue
    wt = wt_text(code)
    idx = wt_lines(wt) if wt else []
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I):
            continue
        try:
            g = boxes(open(hp, encoding="utf-8", errors="replace").read())
            c = boxes(open(cp, encoding="utf-8", errors="replace").read())
        except Exception:
            continue
        if not g or not c:
            continue
        cby = {}
        for t, tx in c:
            if t and t not in cby:
                cby[t] = tx
        for gt, gtx in g:
            if not gt or gt not in cby:
                continue
            ctx = cby[gt]
            G, C = "".join(gtx), "".join(ctx)
            if not G or not C:
                continue
            page = os.path.basename(cp)
            tail = "%s %s «%s»" % (code, page, plain(gt)[:24])

            if G == C:
                v = ("identical" if len(gtx) == len(ctx)
                     else "same text, DIFFERENT paragraph split (not a boundary defect)")
                if len(gtx) != len(ctx):
                    splitform["gold %d -> claude %d" % (len(gtx), len(ctx))] += 1
                verdict[v] += 1
                vmods[v].add(code)
                continue

            if C.startswith(G):
                v, extra_at = "box ends LATE (Claude runs on past the gold's end)", C[len(G):]
            elif G.startswith(C):
                v, extra_at = "box ends EARLY (Claude stops short of the gold's end)", G[len(C):]
            elif C.endswith(G):
                v, extra_at = "box starts EARLY (Claude reaches back before the gold's start)", C[:len(C) - len(G)]
            elif G.endswith(C):
                v, extra_at = "box starts LATE (Claude begins after the gold's start)", G[:len(G) - len(C)]
            else:
                verdict["both ends / disjoint — not a single-seam defect"] += 1
                vmods["both ends / disjoint — not a single-seam defect"].add(code)
                continue

            verdict[v] += 1
            vmods[v].add(code)
            if idx:
                off = locate(idx, extra_at[:80])
                k = struct_tag(wt, off) if off is not None else None
                k = k or "(seam text not found in the WT dump)"
            else:
                k = "(module has no WT dump)"
            seam[v][k] += 1
            seam_mods[v][k].add(code)
            if len(ex[(v, k)]) < 4:
                ex[(v, k)].append("%s  seam «%s»" % (tail, plain(extra_at)[:44]))

tot = sum(verdict.values())
print("=" * 104)
print("ACTIVITY-BOX BOUNDARY, MEASURED AS A BOUNDARY — %d paired boxes matched by title" % tot)
print("=" * 104)
for k, v in verdict.most_common():
    print("   %-62s %6d   modules %4d" % (k[:62], v, len(vmods[k])))

print("\n   the paragraph-split forms (same text both sides), top 12:")
for k, v in splitform.most_common(12):
    print("      %-26s %5d" % (k, v))

for v in ["box ends LATE (Claude runs on past the gold's end)",
          "box ends EARLY (Claude stops short of the gold's end)",
          "box starts EARLY (Claude reaches back before the gold's start)",
          "box starts LATE (Claude begins after the gold's start)"]:
    if not seam.get(v):
        continue
    print("\n" + "-" * 104)
    print("%s — %d boxes" % (v.upper(), verdict[v]))
    print("   the WRITER TAG at the seam:")
    for k, n in seam[v].most_common(12):
        print("      %-44s %5d   modules %4d" % (k[:44], n, len(seam_mods[v][k])))
    for k, _ in seam[v].most_common(4):
        if k.startswith("("):
            continue
        print("      e.g. [%s]:" % k)
        for e in ex[(v, k)]:
            print("         " + e)
