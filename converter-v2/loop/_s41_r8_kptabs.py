#!/usr/bin/env python3
"""Session 41 Round 8 PICK — THE MODULE-MENU "Knowledge" / "Practices" TABS. Per gate module: the gold module-menu tab labels vs
the Claude ones; modules whose gold menu carries a Knowledge / Practice(s) tab; the WT line forms that head those blocks; whether
the Claude menu carries them; and the empty "Learning Intentions" panes on Claude's side (a heading with no list after it).
Run under WSL from CONVERTER_V2/reference/tests."""
import os, re, sys, glob, collections, html as H
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN

def menu_tabs(p):
    s = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(r'id="module-menu-content"(.*?)<div id="body"', s, re.S)
    if not m: return None, ""
    blk = m.group(1)
    ul = re.search(r'<ul class="nav nav-tabs">(.*?)</ul>', blk, re.S)
    tabs = [H.unescape(re.sub(r"<[^>]+>", "", t)).strip() for t in re.findall(r"<li[^>]*>(.*?)</li>", ul.group(1), re.S)] if ul else []
    return tabs, blk
def first_page(d, code):
    c = sorted(glob.glob(os.path.join(d, f"{code}_0_0.html"))) or sorted(glob.glob(os.path.join(d, f"{code}*_0_0.html"))) or sorted(glob.glob(os.path.join(d, "*.html")))
    return c[0] if c else None

KP = re.compile(r"^\s*(knowledge|practices?)\s*$", re.I)
fam = collections.Counter(); forms = collections.Counter(); ex = []
tot = 0; claude_has = 0; empty_li = collections.Counter()
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    gp, cp = first_page(hd, code), first_page(cd, code)
    if not (gp and cp): continue
    gt, gb = menu_tabs(gp); ct, cb = menu_tabs(cp)
    if gt is None: continue
    ct = ct or []
    # empty LI heading panes on Claude's side
    n_empty = len(re.findall(r"<h5>Learning Intentions</h5>\s*</div>", cb)) if cb else 0
    if n_empty: empty_li[code] = n_empty
    if not any(KP.match(t) for t in gt): continue
    tot += 1
    has = any(KP.match(t) for t in ct)
    claude_has += has
    fam[re.sub(r"\d.*", "", code)] += 1
    wts = [f for f in glob.glob(os.path.join(hd, "*_parsed.txt")) if "media list_parsed" not in f.lower()]
    wt = open(wts[0], encoding="utf-8", errors="replace").read() if wts else ""
    for ln in wt.splitlines():
        l = re.sub(r"🔴\[/?RED TEXT\]\s*|\[/RED TEXT\]🔴|[*_​]", "", ln).strip()
        if re.search(r"^(year\s+\d+\s+|level\s+\d+\s+)?(knowledge|practices?)\b\s*:?\s*$", l, re.I):
            forms[re.sub(r"\d+", "N", l.lower())] += 1
    ex.append(f"{code:9s} gold={gt} claude={ct}")
print(f"gold menus with a Knowledge/Practice tab: {tot} modules; Claude carries one in {claude_has}")
print("families:", fam.most_common())
print("WT heading forms:", forms.most_common(20))
print(f"Claude menus with an EMPTY 'Learning Intentions' pane: {len(empty_li)} modules, {sum(empty_li.values())} panes; families:",
      collections.Counter(re.sub(r"\d.*", "", c) for c in empty_li).most_common())
for e in ex[:40]: print(e[:300])
print("empty-LI modules:", " ".join(sorted(empty_li))[:1500])
