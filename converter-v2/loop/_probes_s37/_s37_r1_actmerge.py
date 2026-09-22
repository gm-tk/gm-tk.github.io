#!/usr/bin/env python3
"""Session 37 Round 1 — CHARACTERISE the `[Activity N]` over-capture found by `_s37_r1_actclose.py`
(column B, 395 boxes / 138 modules: the first element Claude's box holds and the gold's does not sits
immediately after a NEW `[Activity N]` opener — Claude is running two writer activities into one box).

For each such case this prints the WT context around the un-honoured opener and answers:
  (a) what is the opener's LITERAL text (is it `[Activity 2]`, `[Activity]`, `[Activity 1B]`, …)?
  (b) is there a TITLE heading between the opener and the extra text, or is it a bare opener?
  (c) did Claude build ANY box whose title matches the gold's NEXT box, i.e. is the activity lost
      entirely or merely mis-bounded?
  (d) how many boxes does the gold have on the page vs Claude?

Run under WSL:  python3 _s37_r1_actmerge.py
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
    for n, p in index:
        if n == needle:
            return p
    if len(needle) >= 20:
        for n, p in index:
            if needle in n or (len(n) >= 20 and n in needle):
                return p
    return None


literal = collections.Counter()
between = collections.Counter()
lost = collections.Counter()
boxcount = collections.Counter()
ex = collections.defaultdict(list)
ctx_samples = []

codes = sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")})
for code in codes:
    try:
        pl = pairs(code)
    except Exception:
        continue
    wt = wt_text(code)
    if not wt:
        continue
    idx = wt_lines(wt)
    if not idx:
        continue
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
        ctitles = {t for t, _ in c if t}
        gtitles = [t for t, _ in g if t]
        cby = {t: tx for t, tx in c if t}
        for gi, (gt, gtx) in enumerate(g):
            if not gt or gt not in cby:
                continue
            ctx = cby[gt]
            gs, cs = set(gtx), set(ctx)
            onlyg = [x for x in gtx if x not in cs]
            onlyc = [x for x in ctx if x not in gs]
            if not onlyc or len(onlyc) <= len(onlyg):
                continue
            off = locate(idx, onlyc[0])
            if off is None:
                continue
            ts = [fold_tag(t) for t in TAG.findall(wt[:off])]
            struct = next((t for t in reversed(ts) if t not in INLINE), None)
            if struct != "activity n":
                continue

            # (a) the opener's literal text
            raw = [t for t in TAG.findall(wt[:off]) if fold_tag(t) not in INLINE]
            lit = re.sub(r'\s+', ' ', raw[-1]).strip() if raw else "?"
            literal[re.sub(r'\d+', '#', lit)[:30]] += 1

            # (b) what sits between the opener and the extra text
            opos = wt[:off].rfind("[" + raw[-1] + "]") if raw else -1
            mid = wt[opos:off] if opos >= 0 else ""
            midtags = [fold_tag(t) for t in TAG.findall(mid)]
            midtags = [t for t in midtags if t not in INLINE and t != "activity n"]
            if any(t.startswith("h") and len(t) == 2 and t[1].isdigit() for t in midtags):
                between["a HEADING tag between opener and text (a titled activity)"] += 1
            elif "activity heading" in " ".join(midtags):
                between["an [activity heading] between them"] += 1
            elif midtags:
                between["other tags between them: " + ",".join(sorted(set(midtags))[:3])] += 1
            else:
                between["NOTHING between them — a BARE opener with its text inline"] += 1

            # (c) did Claude build the gold's NEXT box at all?
            nxt = next((t for t, _ in g[gi + 1:] if t), None)
            if nxt is None:
                lost["the gold has no further titled box on the page"] += 1
            elif nxt in ctitles:
                lost["Claude DID build the gold's next box (mis-bounded, not lost)"] += 1
            else:
                lost["Claude did NOT build the gold's next box (the activity is LOST)"] += 1

            boxcount["gold %d boxes / claude %d" % (len(g), len(c))] += 1
            k = "%s" % re.sub(r'\d+', '#', lit)[:30]
            if len(ex[k]) < 6:
                ex[k].append("%s %s «%s» extra «%s»"
                             % (code, os.path.basename(cp), plain(gt)[:22], plain(onlyc[0])[:34]))
            if len(ctx_samples) < 10 and opos >= 0:
                ctx_samples.append("%s %s\n      WT: %s"
                                   % (code, os.path.basename(cp),
                                      re.sub(r'\s+', ' ', wt[opos:off + 90])[:330]))

tot = sum(literal.values())
print("=" * 100)
print("THE UN-HONOURED [Activity N] OPENER — %d boxes" % tot)
print("=" * 100)
print("\n(a) the opener's LITERAL form (digits folded to #):")
for k, v in literal.most_common(14):
    print("   %-34s %5d" % (k, v))
print("\n(b) what sits BETWEEN the opener and the text Claude wrongly kept in the previous box:")
for k, v in between.most_common(12):
    print("   %-62s %5d" % (k[:62], v))
print("\n(c) did Claude build the gold's NEXT box at all?")
for k, v in lost.most_common():
    print("   %-62s %5d" % (k, v))
print("\n(d) boxes on the page, gold vs Claude (top forms):")
for k, v in boxcount.most_common(12):
    print("   %-34s %5d" % (k, v))
print("\nexamples by opener form:")
for k, _ in literal.most_common(6):
    print("  [%s]" % k)
    for e in ex[k]:
        print("     " + e)
print("\nWT context samples (opener -> the text Claude kept in the PREVIOUS box):")
for s in ctx_samples:
    print("   " + s)
