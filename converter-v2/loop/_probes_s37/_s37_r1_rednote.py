#!/usr/bin/env python3
"""Session 37 Round 1 — THE MANDATED RED-NOTE FAMILY AS A PERMANENT FLOOR ON THE SCORE.

The activity-boundary instrument (`_s37_r1_actbound2.py`) found 762 boxes where Claude's box runs on
past the gold's end, and the seam text is repeatedly the writer's own production note
("Writer's note: can we make something like these please"). Corpus-wide the phrase appears 7,194 times
in Claude across 519 modules and 29 times in the gold across 9.

That is NOT a defect. KB constraints 37, 57, 59 and 88 REQUIRE it: a writer's own note/instruction is
rendered as a VISIBLE red **bold** `<p style="color: red; font-weight: bold;">Writers Note: …</p>`,
never a hidden comment, because comments have shipped to live modules and been missed. Constraint 81(c)
goes further and excludes the whole red-note family from Compare Mode in both directions, calling it
"developer scaffolding … never module content". The human gold has had these notes ACTIONED and removed
during production; PageForge is required to still be emitting them.

So the red-note family is a NAMED KB OVERRIDE (§1b) that can never match the gold, and every one of its
elements is an unmatchable element on the Claude side. This measures what that costs, so the loop stops
reading it as headroom: the count of red-note elements per paired page, their share of Claude's paired
element population, and the modules where they are heaviest.

Run under WSL:  python3 _s37_r1_rednote.py
"""
import re, os, sys, glob, html, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


ELEM = re.compile(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
PREFIX = re.compile(r"^\s*(writers?\s*note|red\s*flag|designer\s*/\s*developer\s*to\s*do|"
                    r"designer\s*note|note\s+from\s+[A-Z])", re.I)

per_prefix = collections.Counter()
mods = collections.defaultdict(set)
c_elems = 0
c_red = 0
g_elems = 0
g_red = 0
pages = 0
pages_with = 0
heavy = collections.Counter()
page_share = []

codes = sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")})
for code in codes:
    try:
        pl = pairs(code)
    except Exception:
        continue
    for n, cp, hp in pl:
        try:
            cs = open(cp, encoding="utf-8", errors="replace").read()
            gs = open(hp, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        pages += 1
        ce = [plain(m.group(2)) for m in ELEM.finditer(cs)]
        ge = [plain(m.group(2)) for m in ELEM.finditer(gs)]
        cr = [t for t in ce if PREFIX.match(t)]
        gr = [t for t in ge if PREFIX.match(t)]
        c_elems += len(ce)
        g_elems += len(ge)
        c_red += len(cr)
        g_red += len(gr)
        if cr:
            pages_with += 1
            heavy[code] += len(cr)
            if len(ce):
                page_share.append(len(cr) / len(ce))
        for t in cr:
            m = PREFIX.match(t)
            k = re.sub(r'\s+', ' ', m.group(1)).lower()
            k = "note from {author}" if k.startswith("note from") else k
            per_prefix[k] += 1
            mods[k].add(code)

print("=" * 96)
print("THE MANDATED RED-NOTE FAMILY ON THE PAIRED POPULATION (%d paired pages)" % pages)
print("=" * 96)
print("   Claude paired elements            %8d" % c_elems)
print("   ... of them red-note elements     %8d   = %.2f %% of everything Claude emits"
      % (c_red, 100.0 * c_red / max(1, c_elems)))
print("   gold paired elements              %8d" % g_elems)
print("   ... of them red-note elements     %8d   = %.2f %% (the human resolves and removes them)"
      % (g_red, 100.0 * g_red / max(1, g_elems)))
print("   paired pages carrying at least one %7d   = %.1f %% of paired pages"
      % (pages_with, 100.0 * pages_with / max(1, pages)))
if page_share:
    page_share.sort()
    print("   on those pages, the red-note share of the page: median %.1f %%, 90th pct %.1f %%, max %.1f %%"
          % (100 * page_share[len(page_share) // 2],
             100 * page_share[int(len(page_share) * 0.9)],
             100 * page_share[-1]))

print("\n   by prefix:")
for k, v in per_prefix.most_common():
    print("      %-34s %7d   modules %4d" % (k, v, len(mods[k])))

print("\n   the 15 heaviest modules (red-note elements on paired pages):")
for k, v in heavy.most_common(15):
    print("      %-14s %5d" % (k, v))
