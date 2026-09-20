#!/usr/bin/env python3
"""_s29_r10_boxforms.py — the r8 boxcol census generalised to the CALLOUT / panel containers: for every div whose class-set contains a
listed head class (alert, alertActivity, whakatauki, supervisor, super-content, quote, wananga, choice, fundamentalsPanel, inquiryPanel,
accContent, clickDropContent), the container's FIRST-CHILD LADDER (up to 2 levels of wrapper divs + the first content tag) gold vs Claude,
per subject|template group — the top gold form vs the top Claude form, flagged when they differ at consensus >= 0.60.
Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s29_r10_boxforms.py
"""
import os, re, sys, json, collections
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]
HEADS = {"alert", "alertActivity", "whakatauki", "supervisor", "super-content", "quote", "wananga", "choice", "fundamentalsPanel",
         "inquiryPanel", "accContent", "clickDropContent", "activity"}
TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)\b([^>]*)>")

def label(tag, attrs):
    m = re.search(r'class="([^"]*)"', attrs)
    cls = sorted(t for t in (m.group(1).split() if m else []) if not t.startswith("cv2"))
    return tag + ("." + ".".join(cls) if cls else "")

def containers(html):
    """yield (headclass, ladder) — ladder = the first-child chain: wrapper divs (class labels) until the first non-div content tag"""
    stack = []   # (label, is_head, want_children_count, ladder list)
    for m in TAG.finditer(html):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in ("br", "img", "hr", "input", "meta", "link", "source", "wbr"):
            for fr in stack:
                if fr[1] and fr[3] is not None and len(fr[3]) < 4 and fr[4]:
                    fr[3].append(label(tag, attrs)); fr[4] = False
            continue
        if closing:
            if stack and stack[-1][0] == tag: stack.pop()
            continue
        if attrs.rstrip().endswith("/"): continue
        lab = label(tag, attrs)
        cls = set(lab.split(".")[1:]) if tag == "div" else set()
        head = tag == "div" and bool(cls & HEADS)
        # record this open tag as the next ladder step for every open head frame still collecting
        for fr in stack:
            if fr[1] and fr[4]:
                fr[3].append(lab)
                if tag != "div" or len(fr[3]) >= 4: fr[4] = False
        if head:
            fr = [tag, True, 0, [], True, sorted(cls & HEADS)]
            stack.append(fr)
            yield_later.append(fr)
        else:
            stack.append([tag, False, 0, None, False, None])

yield_later = []
def scan(html):
    global yield_later
    yield_later = []
    containers(html)
    out = []
    for fr in yield_later:
        heads = "+".join(fr[5]); ladder = " › ".join(fr[3]) if fr[3] else "(empty)"
        out.append((heads, ladder))
    return out

mods = _corpus.gate_mods(CLAUDE)
G = collections.defaultdict(collections.Counter); C = collections.defaultdict(collections.Counter)
Gp = collections.defaultdict(set); Cp = collections.defaultdict(set)
for code in mods:
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); g = (mm.get("template_type", ""), mm.get("subject", ""))
    for t in prs:
        cp, hp = t[1], t[2]
        try: c = open(cp, encoding="utf-8").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        for heads, ladder in scan(gh): G[(g, heads)][ladder] += 1; Gp[(g, heads, ladder)].add(hp)
        for heads, ladder in scan(c): C[(g, heads)][ladder] += 1; Cp[(g, heads, ladder)].add(cp)
print("== container first-child ladder: gold top form vs Claude top form, per (template, subject) x head class; n >= 15 ==")
rows = []
for k, cnt in G.items():
    n = sum(cnt.values())
    if n < 15: continue
    top, tv = cnt.most_common(1)[0]
    cc = C.get(k, collections.Counter()); cn = sum(cc.values())
    if not cn: continue
    ctop, ctv = cc.most_common(1)[0]
    share = tv / n; cshare = ctv / cn
    differs = ctop != top and share >= 0.60
    claude_pages = len(Cp[(k[0], k[1], ctop)])
    rows.append((differs, n, k, top, share, cn, ctop, cshare, claude_pages, cc.get(top, 0)))
rows.sort(key=lambda r: (not r[0], -r[1]))
for differs, n, k, top, share, cn, ctop, cshare, cpages, cgoldform in rows:
    flag = "  <-- DIFFERS" if differs else ""
    print(f"  {str(k[0])[:42]:42s} {k[1]:22s} gold n={n:4d} {top[:60]:60s} {share:.2f} | claude n={cn:4d} {ctop[:60]:60s} {cshare:.2f} (claude pages {cpages}; claude has gold form {cgoldform}){flag}")

# ---- detail: the top 5 forms both sides for a few groups
for key in [(("Inquiry", "1-10 Blended Literacy"), "inquiryPanel"), (("Fundamentals", "1-10 English"), "fundamentalsPanel"), (("Standard", "1-10 Science"), "alert"), (("Fundamentals", "1-10 Writing (MiW)"), "alert"), (("Standard", "1-10 Technology"), "alert")]:
    print("\n==", key)
    for side, D, P in (("gold", G, Gp), ("claude", C, Cp)):
        cnt = D.get(key, collections.Counter()); n = sum(cnt.values())
        for form, v in cnt.most_common(5):
            print(f"   {side:6s} {v:4d}/{n:<4d} pages {len(P[(key[0], key[1], form)]):3d}  {form[:110]}")
