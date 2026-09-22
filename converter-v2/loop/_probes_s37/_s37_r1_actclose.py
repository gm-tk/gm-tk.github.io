#!/usr/bin/env python3
"""Session 37 Round 1 PICK — THE ACTIVITY-BOX BOUNDARY, KEYED ON THE WRITER'S SHAPE (a new instrument).

Session 36's `_s36_r7_actbound.py` keyed on the RENDERED box: it matched 4,617 paired activity boxes by
title and reported over-capture 2,410 / under-capture 1,572 — a population so diffuse that no class came
out of it. It was keyed on the OUTPUT, which is the wrong side: it can say THAT a box ended in the wrong
place but never WHICH WRITER SHAPE put it there, and a converter rule has to be keyed on the writer's tag.

This instrument asks the WT-side question instead. For every paired activity box matched by title:

  * UNDER-CAPTURE (the gold's box holds content Claude's does not) — take the FIRST gold element Claude's
    box is missing, find that text in the module's Writers Template, and read the LAST WRITER TAG before it.
    That tag is the shape that CLOSED CLAUDE'S BOX EARLY.

  * OVER-CAPTURE (Claude's box holds content the gold's does not) — take the FIRST element Claude has that
    the gold's box lacks, find it in the WT, and read the last writer tag before it. That tag is the shape
    THE HUMAN TREATED AS A CLOSER AND CLAUDE DID NOT.

Cross-tabulated by tag, with the module count per tag, so a shape that closes early on 20+ pages across
10+ modules is a derivable class and a shape that is spread one-per-module is not.

Run under WSL:  python3 _s37_r1_actclose.py
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


def boxes(s):
    """every div.activity subtree -> (title, [normalised texts in document order])"""
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


def fold_tag(t):
    """canonical key for a writer tag: '[H3]' -> 'H3', '[Activity 1A]' -> 'Activity N',
    '[Alert box: blue]' -> 'Alert box'."""
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.split(r'[:;]', t)[0].strip()
    t = re.sub(r'\b\d+[A-Za-z]?\b', 'N', t)
    t = re.sub(r'\bN\s+N\b', 'N', t)
    return t.lower()


# ---- WT index: normalised text -> character offset, per module ------------------
def wt_text(code):
    gdir = (glob.glob(ROOT + "/01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    if not gdir:
        return ""
    buf = []
    for t in sorted(glob.glob(gdir + "*parsed.txt")):
        b = os.path.basename(t)
        if re.search(r'media\s*list', b, re.I) and not re.search(r'writer', b, re.I):
            continue                                   # a Media-List-only dump is not the WT
        buf.append(open(t, encoding="utf-8", errors="replace").read())
    return "\n".join(buf)


def wt_lines(wt):
    """(normalised text, char offset) for every non-empty WT line, with its tags stripped"""
    out = []
    pos = 0
    for line in wt.split("\n"):
        bare = TAG.sub(' ', line)
        n = norm(bare)
        if len(n) >= 8:
            out.append((n, pos))
        pos += len(line) + 1
    return out


def locate(index, needle):
    """offset of the WT line whose normalised text best carries `needle` (exact, then containment)"""
    for n, p in index:
        if n == needle:
            return p
    if len(needle) >= 20:
        for n, p in index:
            if needle in n or (len(n) >= 20 and n in needle):
                return p
    return None


# INLINE markup — colour, weight and link spans the writer wraps around words. These say nothing
# about where a container ends, so the first run of this instrument was swamped by them
# ([/red text] took 729 of the 1,614 under-captures and 1,205 of the 2,361 over-captures).
# The tag that decides a boundary is the last STRUCTURAL one before the text.
INLINE = {
    "red text", "/red text", "bold", "/bold", "italic", "/italic", "italics", "/italics",
    "underline", "/underline", "highlight", "/highlight", "link", "hyperlink", "url",
    "correct", "correct answer", "incorrect", "answer", "caption", "alt text", "alt",
    "front", "back", "hover", "important", "bold text", "/bold text", "colour", "color",
}


def tag_before(wt, off):
    """the last STRUCTURAL writer tag at or before `off` (inline markup skipped), plus the
    last tag of any kind — the second is kept so an inline-only neighbourhood is still visible."""
    ts = [fold_tag(t) for t in TAG.findall(wt[:off])]
    if not ts:
        return None, None
    struct = next((t for t in reversed(ts) if t not in INLINE), None)
    return struct, ts[-1]


early = collections.Counter()
early_mods = collections.defaultdict(set)
early_ex = collections.defaultdict(list)
late = collections.Counter()
late_mods = collections.defaultdict(set)
late_ex = collections.defaultdict(list)
seen = collections.Counter()

codes = sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")})
for code in codes:
    try:
        pl = pairs(code)
    except Exception:
        continue
    wt = wt_text(code)
    if not wt:
        seen["module with NO Writers Template dump"] += 1
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
        cby = {t: tx for t, tx in c if t}
        for gt, gtx in g:
            if not gt or gt not in cby:
                continue
            ctx = cby[gt]
            gs, cs = set(gtx), set(ctx)
            onlyg = [x for x in gtx if x not in cs]
            onlyc = [x for x in ctx if x not in gs]
            if not onlyg and not onlyc:
                seen["box identical"] += 1
                continue
            page = os.path.basename(cp)
            if len(onlyg) > len(onlyc) and onlyg:
                seen["under-capture (Claude's box ends early)"] += 1
                off = locate(idx, onlyg[0])
                if off is None:
                    early["(the lost text is not in the WT dump)"] += 1
                    early_mods["(the lost text is not in the WT dump)"].add(code)
                    continue
                t1, t0 = tag_before(wt, off)
                key = t1 if t1 else "(no tag before it)"
                early[key] += 1
                early_mods[key].add(code)
                if len(early_ex[key]) < 5:
                    early_ex[key].append("%s %s «%s» -> lost «%s»"
                                         % (code, page, plain(gt)[:26], plain(onlyg[0])[:40]))
            elif len(onlyc) > len(onlyg) and onlyc:
                seen["over-capture (Claude's box runs on)"] += 1
                off = locate(idx, onlyc[0])
                if off is None:
                    late["(the extra text is not in the WT dump)"] += 1
                    late_mods["(the extra text is not in the WT dump)"].add(code)
                    continue
                t1, t0 = tag_before(wt, off)
                key = t1 if t1 else "(no tag before it)"
                late[key] += 1
                late_mods[key].add(code)
                if len(late_ex[key]) < 5:
                    late_ex[key].append("%s %s «%s» -> extra «%s»"
                                        % (code, page, plain(gt)[:26], plain(onlyc[0])[:40]))
            else:
                seen["same size, different content"] += 1

print("=" * 100)
print("ACTIVITY-BOX BOUNDARY, KEYED ON THE WRITER'S TAG  (session 37 Round 1 PICK)")
print("=" * 100)
for k, v in seen.most_common():
    print("   %-44s %6d" % (k, v))

print("\n" + "-" * 100)
print("A. CLAUDE'S BOX ENDS EARLY — the writer tag immediately before the FIRST LOST element")
print("   (this is the shape that closed the box; the gold kept going)")
print("-" * 100)
print("   %-44s %6s  %8s" % ("writer tag before the lost text", "boxes", "modules"))
for k, v in early.most_common(28):
    print("   %-44s %6d  %8d" % (k[:44], v, len(early_mods[k])))

print("\n" + "-" * 100)
print("B. CLAUDE'S BOX RUNS ON — the writer tag immediately before the FIRST EXTRA element")
print("   (this is the shape the HUMAN treated as a closer and Claude did not)")
print("-" * 100)
print("   %-44s %6s  %8s" % ("writer tag before the extra text", "boxes", "modules"))
for k, v in late.most_common(28):
    print("   %-44s %6d  %8d" % (k[:44], v, len(late_mods[k])))

print("\nexamples — A (ends early), the top shapes:")
for k, _ in early.most_common(8):
    if k.startswith("("):
        continue
    print("  [%s]" % k)
    for e in early_ex[k]:
        print("     " + e)
print("\nexamples — B (runs on), the top shapes:")
for k, _ in late.most_common(8):
    if k.startswith("("):
        continue
    print("  [%s]" % k)
    for e in late_ex[k]:
        print("     " + e)
