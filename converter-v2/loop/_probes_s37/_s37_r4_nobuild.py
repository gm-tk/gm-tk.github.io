#!/usr/bin/env python3
"""Session 37 Round 4 PICK — THE BOXES WHERE THE GOLD BUILT A WIDGET AND CLAUDE BUILT NOTHING.
Round 1's decomposition of the paired activity boxes (_s37_r1_disjoint.py) found 205 boxes / 124
modules where the gold's activity box carries widget markup and Claude's carries NEITHER a built
widget NOR a cv2-int-ref hand-off box — the writer's interactive was not recognised at all, so
nothing was captured and nothing was flagged. That is different from the un-built-widget hand-off
population (D10-3 / Needs Chris #4, where the converter KNOWS it declined): here the converter never
saw an interactive. A silent miss is a recognition defect and squarely in the loop's lane.
This asks WHICH GOLD WIDGET it is and whether the Writers Template carries a tag for it.
Run under WSL:  python3 _s37_r4_nobuild.py"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"))
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
def plain(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
TEXT = re.compile(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
REDNOTE = re.compile(r"^\s*(writers?\s*note|red\s*flag|designer\s*/\s*developer\s*to\s*do"
                     r"|designer\s*note|note\s+from\s+[A-Z])", re.I)
WIDGETCLS = re.compile(r'cv2-int-ref|cv2-int-raw|hintDrop|clickDrop|dragDrop|flipCard|speechBubble'
                       r'|accordion|carousel|tabContent|modal|wordHighlighter|quiz', re.I)
# what the GOLD built, named by the class the human's template uses
GOLDKIND = [("flipCard", r'flip-?card'), ("clickDrop", r'clickDrop'), ("dragDrop", r'dragDrop|hintDrop'),
            ("speechBubble", r'speechBubble'), ("accordion", r'accordion'), ("carousel", r'carousel'),
            ("tabs", r'tabContent|nav-tabs'), ("modal", r'TKmodal|\bmodal\b'),
            ("wordHighlighter", r'wordHighlighter'), ("quiz", r'quiz')]
def boxes(s):
    out = []
    for m in re.finditer(r'<div[^>]*class="[^"]*\bactivity\b[^"]*"[^>]*>', s):
        st = m.end(); d = 1; i = len(s)
        for t in re.finditer(r'<div\b[^>]*>|</div>', s[st:]):
            d += 1 if t.group(0) != "</div>" else -1
            if d == 0: i = st + t.start(); break
        sub = s[st:i]
        tx = [norm(x.group(2)) for x in TEXT.finditer(sub)
              if len(norm(x.group(2))) >= 8 and not REDNOTE.match(plain(x.group(2)))]
        ti = next((norm(x.group(2)) for x in TEXT.finditer(sub) if x.group(1).startswith("h")), "")
        out.append((ti, tx, sub))
    return out
def wt_text(code):
    gd = (glob.glob(ROOT + "/01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    if not gd: return ""
    b = []
    for t in sorted(glob.glob(gd + "*parsed.txt")):
        n = os.path.basename(t)
        if re.search(r'media\s*list', n, re.I) and not re.search(r'writer', n, re.I): continue
        b.append(open(t, encoding="utf-8", errors="replace").read())
    return "\n".join(b)
_WTIDX = {}
kind = collections.Counter(); kmods = collections.defaultdict(set)
pairk = collections.Counter(); pmods = collections.defaultdict(set); ex = collections.defaultdict(list)
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    wt = wt_text(code)
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        try:
            g = boxes(open(hp, encoding="utf-8", errors="replace").read())
            c = boxes(open(cp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        if not g or not c: continue
        cby = {}
        for t, tx, sub in c:
            if t and t not in cby: cby[t] = (tx, sub)
        for gt, gtx, gsub in g:
            if not gt or gt not in cby: continue
            ctx, csub = cby[gt]
            G, C = "".join(gtx), "".join(ctx)
            if not G or not C: continue
            if G == C or C.startswith(G) or G.startswith(C) or C.endswith(G) or G.endswith(C): continue
            if not WIDGETCLS.search(gsub): continue
            if WIDGETCLS.search(csub): continue                 # Claude built or flagged something
            k = next((nm for nm, rx in GOLDKIND if re.search(rx, gsub, re.I)), "other/unnamed")
            kind[k] += 1; kmods[k].add(code)
            # is there ANY interactive-looking writer tag near that title in the WT?
            # `gt` is ALREADY normalised (letters+digits, no spaces), so searching the RAW WT for it
            # never matches — the first run of this instrument reported "title not found in the WT"
            # for 197 of 205 boxes purely because of that. Build a normalised WT with an index back
            # to raw offsets and look the title up there.
            j = -1
            if wt and gt:
                if code not in _WTIDX:
                    raw, idx = [], []
                    for ci, ch in enumerate(wt.lower()):
                        if ch.isalnum():
                            raw.append(ch); idx.append(ci)
                    _WTIDX[code] = ("".join(raw), idx)
                nwt, idx = _WTIDX[code]
                k2 = nwt.find(gt[:22])
                if k2 >= 0: j = idx[k2]
            win = wt[max(0, j - 500):j + 500] if j > 0 else ""
            has = bool(re.search(r'\[[^\]]*(interactive|drag|drop|flip|card|match|quiz|accordion|carousel|tab|modal|hover|slider|memory|highlight|sort|order)[^\]]*\]', win, re.I))
            pk = "%s | %s" % (k, "a widget-ish WT tag IS near the title" if has else
                              "NO widget-ish WT tag near the title" if win else "(title not found in the WT)")
            pairk[pk] += 1; pmods[pk].add(code)
            if len(ex[pk]) < 4: ex[pk].append("%s %s «%s»" % (code, os.path.basename(cp), plain(gt)[:24]))
print("GOLD BUILT A WIDGET, CLAUDE BUILT NOTHING AND FLAGGED NOTHING — %d boxes" % sum(kind.values()))
print("=" * 92)
for k, v in kind.most_common(): print("   %-24s %4d  mods %4d" % (k, v, len(kmods[k])))
print("\n   cross-tabbed with the Writers Template:")
for k, v in pairk.most_common(14): print("   %-72s %4d  mods %3d" % (k[:72], v, len(pmods[k])))
print()
for k, _ in pairk.most_common(6):
    print("  " + k); [print("     " + e) for e in ex[k]]
