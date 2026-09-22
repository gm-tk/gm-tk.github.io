#!/usr/bin/env python3
"""Session 36 Round 6 PICK measurement — THE SENTENCE THAT RESOLVED TO A TAG. A writer's bracketed note to the developer that
carries no addressee prefix ("[Keep all other content in the Introduction]", "[Insert the completed table below]") is matched by
the normaliser's EMBEDDED-alias fallback and becomes a structural tag — on CEDR302 that turned the page's first item into a
`title bar` SECTION_MARKER, which then made the whole page's front matter the module menu (89 menu elements).
Measure, over every parsed Writers Template: bracket fragments of >= `min_words` words whose tag came from the EMBEDDED fallback
(not exact / payload / head / de-numbered), grouped by the canonical tag and the directive, with the module count.
Run under WSL (from reference/tests, via node for the normaliser): this is the PYTHON half — it only counts candidates by regex
over the alias list, so the node probe `_s36_r6_sentencetag.cjs` is the authority; this script sizes the population quickly."""
import re, os, sys, glob, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
GOLD = ROOT + "/01-Finalized_Modules_"
RED = re.compile(r'\U0001f534\[RED TEXT\](.*?)\[/RED TEXT\]\U0001f534', re.S)
BRACKET = re.compile(r'\[([^\]]{3,200})\]')
lex = json.load(open(ROOT + "/pageforge-site/converter-v2/data/Tag_Lexicon.json", encoding="utf-8"))
alias = {}
for canon, d in lex["tags"].items():
    for a in d["aliases"]:
        alias.setdefault(a.strip().lower(), (canon, d["directive"]))
cues = json.load(open(ROOT + "/pageforge-site/converter-v2/data/Instruction_Cues.json", encoding="utf-8"))
pref = [p.lower() for p in cues["addressee_prefixes"]]
MINW = int(sys.argv[1]) if len(sys.argv) > 1 else 5
tab = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
for wt in sorted(glob.glob(GOLD + "/*/*/*Writers*parsed.txt")):
    code = wt.split("/")[-2]
    txt = open(wt, encoding="utf-8", errors="replace").read()
    for m in RED.finditer(txt):
        raw = m.group(1)
        b = BRACKET.search(raw)
        if not b: continue
        frag = re.sub(r'\s+', ' ', b.group(1)).strip()
        low = frag.lower()
        if any(low.startswith(p) for p in pref): continue          # the addressee guard already catches it
        words = low.replace(":", " ").split()
        if len(words) < MINW: continue
        if low in alias: continue                                   # an exact alias, however long
        # the embedded fallback: the longest alias present on a word boundary
        best = None
        for a, (canon, directive) in alias.items():
            if len(a) < 3: continue
            if re.search(r'(?:^|[\s:;,.|/(\[+-])' + re.escape(a) + r'(?:$|[\s:;,.|/)\]#\d+-])', " " + low + " "):
                if best is None or len(a) > len(best[0]): best = (a, canon, directive)
        if not best: continue
        tab["%-18s %-16s" % (best[1], best[2])] += 1
        mods["%s|%s" % (best[1], best[2])].add(code)
        k = "%s|%s" % (best[1], best[2])
        if len(ex[k]) < 4: ex[k].append("%s: [%s]" % (code, frag[:78]))
print("bracket fragments of >= %d words, no addressee prefix, resolved only by the EMBEDDED alias fallback: %d" % (MINW, sum(tab.values())))
for k, v in tab.most_common(24):
    key = "|".join(k.split())
    print("   %-38s %4d   modules %3d" % (k, v, len(mods.get(key, ()))))
print("\nexamples:")
for k, v in sorted(ex.items(), key=lambda kv: -len(mods[kv[0]]))[:14]:
    print("  %-34s (modules %d)" % (k, len(mods[k])))
    for e in v: print("     " + e)
