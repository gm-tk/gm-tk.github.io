#!/usr/bin/env python3
"""Session 41 Round 8 — the Knowledge / Practices POPULATION (KB 67 canonical tab set). Per gate module: does a Knowledge or
Practices section heading reach the CLAUDE module menu (any <h4>/<h5>/<p><b> heading whose text is Knowledge / Practice(s), an
optional "Year N" / "Level N" lead, an optional colon) — and does the GOLD menu give it its own nav tab? The counter-population
(the heading reaches the menu, gold keeps it IN a pane) is what decides whether the promotion can be corpus-wide.
Also: WT carries a Knowledge heading but NEITHER menu shows it (lost). Run under WSL from CONVERTER_V2/reference/tests."""
import os, re, sys, glob, collections, html as H
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN

HEAD = re.compile(r"<(h[2-6])[^>]*>(.*?)</\1>|<p>\s*<(?:b|strong)>(.*?)</(?:b|strong)>\s*</p>", re.S | re.I)
KP = re.compile(r"^(?:year\s+\d+\s+|level\s+\d+\s+)?(knowledge|practices?)\s*:?\s*$", re.I)
def menu(p):
    s = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(r'id="module-menu-content"(.*?)<div id="body"', s, re.S)
    if not m: return None, []
    blk = m.group(1)
    ul = re.search(r'<ul class="nav nav-tabs">(.*?)</ul>', blk, re.S)
    tabs = [H.unescape(re.sub(r"<[^>]+>", "", t)).strip() for t in re.findall(r"<li[^>]*>(.*?)</li>", ul.group(1), re.S)] if ul else []
    heads = []
    for h in HEAD.finditer(blk):
        t = H.unescape(re.sub(r"<[^>]+>", "", h.group(2) or h.group(3) or "")).strip()
        k = KP.match(t)
        if k: heads.append(k.group(1).lower().rstrip("s") + ("s" if k.group(1).lower().startswith("practice") else ""))
    return tabs, heads
def first(d, code):
    c = sorted(glob.glob(os.path.join(d, f"{code}_0_0.html"))) or sorted(glob.glob(os.path.join(d, "*_0_0.html"))) or sorted(glob.glob(os.path.join(d, "*.html")))
    return c[0] if c else None
def phase_of(cd):
    try:
        import json
        j = json.load(open(os.path.join(cd, "_run.json"), encoding="utf-8"))
        return (j.get("resolvedRules") or {}).get("template_phase") or j.get("template_phase") or "?"
    except Exception: return "?"
cls = collections.Counter(); rows = collections.defaultdict(list); grp = collections.defaultdict(collections.Counter)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    gp, cp = first(hd, code), first(cd, code)
    if not (gp and cp): continue
    gt, gh = menu(gp); ct, ch = menu(cp)
    if gt is None or ct is None: continue
    gtab = any(KP.match(t) for t in gt); ctab = any(KP.match(t) for t in ct)
    if not (ch or ctab or gtab or gh): continue
    if ctab and gtab: k = "BOTH-TAB"
    elif gtab and ch: k = "GOLD-TAB, claude in-pane"
    elif gtab: k = "GOLD-TAB, claude has no heading"
    elif ch and gh: k = "BOTH IN-PANE (counter)"
    elif ch: k = "claude in-pane, gold none"
    elif ctab: k = "CLAUDE-TAB only"
    else: k = "gold in-pane, claude none"
    cls[k] += 1; rows[k].append(f"{code}  gold={gt} claude={ct} ch={ch} gh={gh}")
    grp[re.match(r"[A-Z]+", code).group(0)][k] += 1
for k, n in cls.most_common(): print(f"{n:4d} {k}")
print()
for f, c in sorted(grp.items()): print(f"{f:7s}", dict(c))
for k in cls:
    print(f"\n== {k}")
    for r in rows[k][:40]: print("  ", r[:260])
