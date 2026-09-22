#!/usr/bin/env python3
"""Session 37 Round 2 PICK — DOES THE WRITER NAME THE WIDGET TYPE THE SCANNER LEFT UNCLASSIFIED?

Round 1 decomposed the paired activity boxes and found the mass is the un-built-widget hand-off
population (D10-3 / Needs Chris #4). Inside it, one group is NOT a build question: 326 paired boxes /
153 modules where the scanner emitted an `unclassified` hand-off — it saw `[Activity N]` with a data
table ahead and NO recognised interactive keyword, so it could not say what widget to build. Its own
red flag says so: "widget type must be identified from the captured content".

ANZH104 3A is the worked example. The Writers Template says:

    [Activity embedded]  word find
    [H3]  3A Clothing Word Find
    TABLE of clothing words

`word find` is a REGISTERED ALIAS of the `word find` tag in Tag_Lexicon.json. The type is named — in
the writer's free text beside the tag rather than inside the brackets — and the scanner never reads it.

TagNormaliser ALREADY scans folded free text for INTERACTIVE aliases (the `qualifier_alias_demote`
path, round 217), but only as a BOOLEAN: "does this span name a widget?", used to decide keep-or-demote.
The alias it found is thrown away and never used to classify the bundle. That is the gap this measures.

For every unclassified hand-off on disk: pull its activity id out of the red-flag line, find that
opener in the module's Writers Template, take the window from the opener to the first table, and ask
whether it contains a known INTERACTIVE alias (>= 4 chars, the round-217 rule). Report the share and
the types, per module family, so the round can be scoped.

Run under WSL:  python3 _s37_r2_unclass.py
"""
import re, os, sys, glob, json, io, html, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
CV2 = os.path.join(ROOT, "CONVERTER_V2")


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def fold(s):
    return re.sub(r'[^a-z0-9 ]+', ' ', s.lower())


# ---- the lexicon's INTERACTIVE aliases (the same set round 217 scans) ----------
lex = json.load(io.open(os.path.join(CV2, "data", "Tag_Lexicon.json"), encoding="utf-8"))
ALIAS = []
for tag, d in lex["tags"].items():
    if isinstance(d, dict) and d.get("directive") == "INTERACTIVE":
        for a in (d.get("aliases") or []):
            a = str(a).lower().strip()
            if len(a) >= 4:
                ALIAS.append((a, tag))
ALIAS.sort(key=lambda x: -len(x[0]))          # longest alias wins

RED = re.compile(r'INTERACTIVE \(un-built\) #\d+:\s*unclassified\s*—\s*([^<—]{1,40}?)\s*—', re.I)


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


found = collections.Counter()
types = collections.Counter()
tmods = collections.defaultdict(set)
nomods = set()
yesmods = set()
ex = collections.defaultdict(list)
noex = []
total = 0

for f in sorted(glob.glob(ROOT + "/01-Claude_Modules_/*/*/*.html")):
    s = open(f, encoding="utf-8", errors="replace").read()
    if "unclassified" not in s:
        continue
    code = os.path.basename(os.path.dirname(f))
    ids = [m.group(1).strip() for m in RED.finditer(s)]
    if not ids:
        continue
    wt = wt_text(code)
    if not wt:
        continue
    for act in ids:
        total += 1
        num = (re.search(r'([0-9]+[A-Za-z]?)', act) or [None, None])[1]
        win = ""
        if num:
            for m in re.finditer(r'\[\s*activity[^\]]*\]', wt, re.I):
                seg = wt[m.start():m.start() + 700]
                if re.search(r'\b' + re.escape(num) + r'\b', seg[:260], re.I):
                    cut = seg.find("TABLE")
                    win = seg[:cut if cut > 0 else 700]
                    break
        if not win:
            found["(the opener was not located in the WT dump)"] += 1
            continue
        fw = fold(plain(win))
        hit = next(((a, t) for a, t in ALIAS if a in fw), None)
        if hit:
            found["the writer NAMES a known widget type in the free text"] += 1
            types[hit[1]] += 1
            tmods[hit[1]].add(code)
            yesmods.add(code)
            if len(ex[hit[1]]) < 4:
                ex[hit[1]].append("%s %s «%s» -> alias «%s»"
                                  % (code, os.path.basename(f), act, hit[0]))
        else:
            found["no known alias anywhere in the opener window"] += 1
            nomods.add(code)
            if len(noex) < 12:
                noex.append("%s %s «%s»: %s" % (code, os.path.basename(f), act,
                                                re.sub(r'\s+', ' ', plain(win))[:110]))

print("=" * 96)
print("UNCLASSIFIED HAND-OFFS — DOES THE WRITER NAME THE TYPE?  (%d boxes on disk)" % total)
print("=" * 96)
for k, v in found.most_common():
    print("   %-58s %5d   = %.1f %%" % (k[:58], v, 100.0 * v / max(1, total)))
print("\n   modules with at least one nameable box: %d;  with none: %d"
      % (len(yesmods), len(nomods - yesmods)))

print("\n   the type the writer's free text names:")
for k, v in types.most_common(25):
    print("      %-24s %5d   modules %4d" % (k, v, len(tmods[k])))

print("\n   examples (nameable):")
for k, _ in types.most_common(8):
    for e in ex[k]:
        print("      " + e)
print("\n   examples (NOT nameable — what the window actually says):")
for e in noex:
    print("      " + e)
