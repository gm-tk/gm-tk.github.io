#!/usr/bin/env python3
"""Session 26 — EXTENDED (from _s25_after.py): the r51 `row_breaks.after` rule ("content following a closed callout / activity / widget always starts a
fresh row", verified on 2 pages in June 2026) measured on today's corpus: for every alert / activity / WIDGET that is a
direct child of a top-level body column, is it the column's LAST child (the next content opens a new row) or is it
FOLLOWED by more content in the same column (the gold flows on)? Gold vs Claude, per template / subject, with what
follows. python3 _s26_after2.py [prefix-filter] — every block type that closes a column: whakatauki, button, table, img, video, iframe, audio, blockquote, alert VARIANTS, plus the s25 three"""
import os, sys, re
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
sys.path.insert(0, TESTS)
import _corpus
from _skeleton_compare import _skel
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
flt = args[0] if args else ""

def ind(l): return len(l) - len(l.lstrip(" "))

def kind(lbl):
    s = lbl.strip()
    if s == "WIDGET": return "WIDGET"
    if s.startswith("div.activity"): return "activity"
    if s.startswith("div.alertActivity"): return "alertActivity"
    if s.startswith("div.alert"):
        toks = s.split("[")[0].split(".")[1:]
        return "alert" if toks == ["alert"] else "alert." + ".".join(t for t in toks if t != "alert")
    if s.startswith("div.whakatauki"): return "whakatauki"
    if s.startswith("div.button"): return "button"
    if s.startswith("blockquote"): return "blockquote"
    if s.startswith("iframe"): return "iframe"
    if s.startswith("audio"): return "audio"
    if s.startswith("┌"): return "repeat"
    m = re.match(r"(h[1-6])\b", s)
    if m: return m.group(1)
    if s.startswith("p") and (len(s) == 1 or s[1] in ".>[ "): return "p"
    if s.startswith("img"): return "img"
    if s.startswith("ul") or s.startswith("ol"): return "list"
    if s.startswith("div.") and "videoSection" in s: return "video"
    if s.startswith("div.table-responsive") or s.startswith("table"): return "table"
    if s.startswith("a") and (len(s) == 1 or s[1] in ".>[ "): return "a"
    if s.startswith("br"): return "br"
    if s.startswith("div.row"): return "row"
    return s.split(".")[0].split("[")[0]

def columns(lines):
    """for each top-level row's column: the list of kid kinds (depth base+6)"""
    bi = None
    for i, l in enumerate(lines):
        if l.strip().startswith("div#body") and ind(l) <= 4:
            bi = i; break
    if bi is None: return []
    base = ind(lines[bi])
    out = []
    i = bi + 1; n = len(lines)
    while i < n and ind(lines[i]) > base:
        if ind(lines[i]) == base + 2 and lines[i].strip().startswith("div.row"):
            j = i + 1
            while j < n and ind(lines[j]) > base + 2:
                if ind(lines[j]) == base + 4 and lines[j].strip().startswith("div.col"):
                    k = j + 1; kids = []
                    while k < n and ind(lines[k]) > base + 4:
                        if ind(lines[k]) == base + 6: kids.append(kind(lines[k]))
                        k += 1
                    out.append(kids); j = k
                else:
                    j += 1
            i = j
        else:
            i += 1
    return out

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
TARGETS = ("alert", "alert.solid", "alert.top", "alert.rhs", "alertActivity", "whakatauki", "button", "table", "img", "video", "iframe", "audio", "blockquote", "activity", "WIDGET", "list", "p")
agg = defaultdict(lambda: {"gold": defaultdict(Counter), "claude": defaultdict(Counter), "pages": 0})
pages_follow = defaultdict(set); mods_follow = defaultdict(set); pages_any = defaultdict(set)
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    subject = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g = columns(_skel(hp, True)); c = columns(_skel(cp, True))
        except Exception:
            continue
        for k in ("ALL", f"template={tf}", f"subject={subject}"):
            agg[k]["pages"] += 1
            for side, cols in (("gold", g), ("claude", c)):
                for kids in cols:
                    for idx, kk in enumerate(kids):
                        if kk in TARGETS:
                            nxt = kids[idx + 1] if idx + 1 < len(kids) else None
                            agg[k][side][kk]["LAST in column" if nxt is None else f"followed by {nxt}"] += 1
                            if side == "gold": pages_any[(k, kk)].add(hp)
                            if nxt is not None and side == "gold": pages_follow[(k, kk)].add(hp); mods_follow[(k, kk)].add(code)

def line(c):
    t = sum(c.values()) or 1
    return ", ".join(f"{k} {v} ({v/t:.2f})" for k, v in c.most_common(7))
for k in sorted(agg, key=lambda k: (0 if k == "ALL" else 1 if k.startswith("template=") else 2, -agg[k]["pages"])):
    A = agg[k]
    if A["pages"] < 30: continue
    print(f"\n== {k} — pages {A['pages']}")
    for kk in TARGETS:
        gt = sum(A["gold"][kk].values()); ct = sum(A["claude"][kk].values())
        if gt + ct < 20: continue
        fl = sum(v for x, v in A["gold"][kk].items() if x != "LAST in column")
        cfl = sum(v for x, v in A["claude"][kk].items() if x != "LAST in column")
        flag = "  <== CANDIDATE" if (fl/max(gt,1) >= 0.60 and cfl/max(ct,1) <= 0.40 and len(pages_follow[(k, kk)]) >= 20 and len(mods_follow[(k, kk)]) >= 10) else ""
        print(f"  {kk:13s} gold   n={gt:5d} followed-on {fl/max(gt,1):.2f} (pages {len(pages_follow[(k, kk)])} / {len(pages_any[(k, kk)])}, mods {len(mods_follow[(k, kk)])}): {line(A['gold'][kk])}{flag}")
        print(f"  {'':13s} claude n={ct:5d} followed-on {cfl/max(ct,1):.2f}: {line(A['claude'][kk])}")
