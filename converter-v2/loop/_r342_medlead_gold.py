#!/usr/bin/env python3
"""_r342_medlead_gold.py — ROUND 342 gap 2 (the media element's EMBEDDED LEAD): does the human's
page KEEP the words a writer typed inside the media tag's own red span ("[audio] snail, paint,
trail" / "[video 1] The letter t -")?  Reads the rows _measure_r342_media_embedded.cjs wrote
(_r342_medemb_on_*.json = the r342-ON population, _r342_medemb_off_*.json = pre-existing) and,
for every row, searches EVERY gold page of the module for the lead's first N words (folded:
lower-case, punctuation stripped).  Reports the KEEP share per tag and per population, and the
per-template split — the §3 step-3 solidify test for option (a) of gap 2.  Run under WSL.
"""
import glob, json, os, re, sys, html
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
N = 4   # words of the lead that must appear in order

def fold(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = s.lower().replace("’", "'").replace("‘", "'")
    s = re.sub(r"[^\w\s]", " ", s, flags=re.U)
    return re.sub(r"\s+", " ", s).strip()

_gold_cache = {}
def gold_text(code):
    if code in _gold_cache: return _gold_cache[code]
    hits = glob.glob(os.path.join(GOLD, "*", code)) + glob.glob(os.path.join(GOLD, code))
    txt = []
    for d in hits:
        if not os.path.isdir(d): continue
        for f in os.listdir(d):
            if f.endswith(".html"):
                try:
                    with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh:
                        txt.append(fold(fh.read()))
                except Exception: pass
    _gold_cache[code] = (" ".join(txt), os.path.basename(os.path.dirname(hits[0])) if hits else "?")
    return _gold_cache[code]

def load(pattern):
    rows = []
    for f in sorted(glob.glob(os.path.join(HERE, pattern))):
        with open(f, encoding="utf-8") as fh: rows.extend(json.load(fh))
    return [r for r in rows if "err" not in r]

on = load("_r342_medemb_on_*.json"); off = load("_r342_medemb_off_*.json")
key = lambda r: (r["code"], r["page"], r["tag"], r["raw"])
offk = {key(r) for r in off}
def judge(rows, label):
    per = defaultdict(lambda: [0, 0]); tpl = defaultdict(lambda: [0, 0]); kept_ex = []; lost_ex = []
    for r in rows:
        words = fold(r["lead"]).split()
        if not words: continue
        needle = " ".join(words[:N])
        gtxt, template = gold_text(r["code"])
        k = needle in gtxt
        per[r["tag"]][0 if k else 1] += 1; tpl[template][0 if k else 1] += 1
        (kept_ex if k else lost_ex).append(f"{r['code']} {r['page']} {r['tag']} | {r['lead'][:60]}")
    tot_k = sum(v[0] for v in per.values()); tot_l = sum(v[1] for v in per.values())
    print(f"== {label}: {tot_k + tot_l} sites — gold KEEPS the lead words {tot_k} ({tot_k / max(1, tot_k + tot_l):.2f}) / drops {tot_l}")
    for t, (k, l) in sorted(per.items(), key=lambda kv: -(kv[1][0] + kv[1][1])):
        print(f"   {t:14s} keep {k:4d} / drop {l:4d}  share {k / max(1, k + l):.2f}")
    for t, (k, l) in sorted(tpl.items()):
        print(f"   [{t}] keep {k} / drop {l}  share {k / max(1, k + l):.2f}")
    print("   kept e.g.:"); [print("     " + e) for e in kept_ex[:8]]
    print("   dropped e.g.:"); [print("     " + e) for e in lost_ex[:8]]
    return per

judge([r for r in on if key(r) not in offk], "ON-ONLY (the r342 hyperlinked class)")
judge(off, "PRE-EXISTING (OFF state, MediaBuilder.media drops the lead today)")
# audio only, un-built video (no url) vs built video
built = [r for r in off if r["tag"] in ("video", "embed") and r["url"]]
unbuilt = [r for r in off if r["tag"] in ("video", "embed") and not r["url"]]
judge(built, "PRE-EXISTING video/embed WITH a url (the r80 title-drop applies to a built embed)")
judge(unbuilt, "PRE-EXISTING video/embed WITHOUT a url (un-built — red flag + caption today)")
