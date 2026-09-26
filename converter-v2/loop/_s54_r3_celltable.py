#!/usr/bin/env python3
"""_s54_r3_celltable.py — session 54 Round 3: THE ONE-CELL ACTIVITY TABLE. Writers Templates that type an activity INSIDE a one-cell
table: `│ [Learning journal] 1D: Title / [Body] text …` (PWY). For every parsed WT (Writers Template files only), every TABLE block
with exactly one row and no cell separator (║) whose text opens with an optional red tag and an activity id (`1D:` / `2B -` /
`Activity 3A`), report: module, the lead tag, the id, and how Claude rendered that title text (inside an activity box / a hand-off
box / free / absent) vs the gold (activity box / free / absent). WSL, from reference/tests/:
    python3 ../../outputs/_s54_r3_celltable.py > ../../outputs/_s54_r3_celltable.log"""
import os, re, sys, glob, collections, html as H
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN

ID = re.compile(r"^\s*(?:🔴\[RED TEXT\]\s*(\[[^\]]*\](?:\s*\[[^\]]*\])*)\s*\[/RED TEXT\]🔴)?\s*(?:activity\s*)?(\d{1,2}[A-Za-z])\s*[:.\-–]\s*(.{3,80}?)\s*(?:/|$)", re.I)
fam = lambda m: re.sub(r"\d.*$", "", m)
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", H.unescape(s)).lower()).strip()


def where(pages, title):
    t = norm(title)[:40]
    if len(t) < 6: return "short"
    for p in pages:
        s = open(p, encoding="utf-8", errors="replace").read()
        i = norm(re.sub(r"<[^>]+>", " ", s)).find(t)
        if i < 0: continue
        # locate the raw position approximately: the first occurrence of the title's first 3 words in the raw html
        w = re.escape(" ".join(title.split()[:3]))
        m = re.search(w, s, re.I)
        if not m: return "found?"
        before = s[:m.start()]
        opens_int = before.rfind('class="cv2-interactive'); opens_act = before.rfind('class="activity')
        closes = before.rfind("<!-- /cv2-interactive")
        if opens_int > max(opens_act, closes): return "hand-off"
        if opens_act > -1 and before.count("<div") - before.count("</div") > 0 and opens_act > before.rfind('<div class="row">\n', 0, max(0, opens_act - 200)):
            # inside an activity box when the nearest opener is an activity (coarse)
            return "activity" if opens_act > before.rfind('class="alert') else "alert"
        return "free"
    return "absent"


rows = []
for mod in sorted(set(_corpus.gate_mods(CLAUDE))):
    hd = _corpus.mdir(HUMAN, mod); cd = _corpus.mdir(CLAUDE, mod)
    if not hd or not cd: continue
    for p in glob.glob(os.path.join(hd, "*_parsed.txt")):
        b = os.path.basename(p).lower()
        if "writers" not in b: continue
        lines = open(p, encoding="utf-8", errors="replace").read().split("\n")
        i = 0
        while i < len(lines):
            if lines[i].startswith("┌─── TABLE"):
                j = i + 1
                body = []
                while j < len(lines) and not lines[j].startswith("└─── END TABLE"):
                    body.append(lines[j]); j += 1
                cells = [l for l in body if l.startswith("│")]
                if len(cells) == 1 and "║" not in cells[0]:
                    m = ID.match(cells[0][1:].strip())
                    if m:
                        rows.append((mod, (m.group(1) or "").strip(), m.group(2), m.group(3).strip()))
                i = j
            i += 1
cnt = collections.Counter(); byfam = collections.Counter(); ex = collections.defaultdict(list)
for mod, tag, aid, title in rows:
    gp = glob.glob(os.path.join(_corpus.mdir(HUMAN, mod), "*.html")); cp = glob.glob(os.path.join(_corpus.mdir(CLAUDE, mod), "*.html"))
    k = (re.sub(r"\s+", " ", tag.lower())[:40] or "(no tag)", where(gp, title), where(cp, title))
    cnt[k] += 1; byfam[fam(mod)] += 1
    if len(ex[k]) < 3: ex[k].append(f"{mod} {aid}: {title[:50]}")
print(f"one-cell activity tables: {len(rows)} in {len(set(r[0] for r in rows))} modules; families {dict(byfam.most_common(12))}")
for k, c in cnt.most_common(40):
    print(f"  {c:4d}  lead {k[0]!r:42s} gold {k[1]:9s} claude {k[2]:9s}  e.g. {' | '.join(ex[k])}")
