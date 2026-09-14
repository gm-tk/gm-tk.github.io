#!/usr/bin/env python3
"""_measure_r320_dupheading.py — ROUND 320 (loop Round 7) measurement probe: KB constraint 47 + CL-0095.
On a LESSON page a body heading whose text — ignoring case / punctuation and a leading `Lesson N` (any
form) or `Label:` prefix — equals the header <h1><span> title is DROPPED (the header already shows it);
on the OVERVIEW page such a heading keeps its text but loses the label prefix.

Measures, for every paired Claude page (the gate's pairing):
  * the header title (first <h1><span>) and every body heading (h2-h5 inside #body, outside widgets is
    not distinguished — headings are compared by text);
  * headings that equal the title exactly (fold), or after a `Lesson N` strip, or after a `Word:` /
    `Word Word:` label strip; what the gold page does with the same heading (present / absent).
Paths are dynamic (CLAUDE.md §13). Run from anywhere:  python3 _measure_r320_dupheading.py
Writes _r320_dupheading.json next to itself and prints the summary.
"""
import os, re, sys, json, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE

H1 = re.compile(r"<h1><span>(.*?)</span></h1>", re.S)
HB = re.compile(r"<(h[2-5])\b[^>]*>(.*?)</\1>", re.S)
TAG = re.compile(r"<[^>]+>")
LESSON = re.compile(r"^\s*lesson\s+(\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten)\s*[:.\-–—]?\s*", re.I)
LABEL = re.compile(r"^\s*([A-Za-z][\wĀ-ſ]*(?:\s+[A-Za-z][\wĀ-ſ]*)?)\s*:\s*")

def fold(s):
    s = unicodedata.normalize("NFKD", TAG.sub("", s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("&amp;", "&").replace("&#39;", "'").replace("&ndash;", "-")
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def body(html):
    m = re.search(r'<div id="body".*?(?=<div id="footer"|<footer)', html, re.S)
    return m.group(0) if m else html

def title(html):
    m = re.search(r'<div id="header".*?<div id="body"', html, re.S); seg = m.group(0) if m else html[:8000]
    t = H1.findall(seg)
    return fold(t[0]) if t else ""

def classify(htext, ttl):
    """how the heading relates to the title: 'exact' | 'lesson-prefix' | 'label-prefix' | None."""
    f = fold(htext)
    if not ttl or not f: return None
    if f == ttl: return "exact"
    raw = TAG.sub("", htext)
    m = LESSON.match(raw)
    if m and fold(raw[m.end():]) == ttl: return "lesson-prefix"
    m = LABEL.match(raw)
    if m and fold(raw[m.end():]) == ttl: return "label-prefix"
    return None

def main():
    rows = []; C = collections.Counter(); fam = collections.defaultdict(collections.Counter)
    for code in _corpus.mods(CLAUDE):
        cdir = _corpus.mdir(CLAUDE, code); tmpl = os.path.basename(os.path.dirname(cdir)) if cdir else "?"
        for n, cp, hp in pairs(code):
            ch = open(cp, encoding="utf-8", errors="replace").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
            ttl = title(ch); gttl = title(gh)
            overview = (n == 0 or str(n).startswith("0."))
            gold_heads = [fold(t) for _, t in HB.findall(body(gh))]
            for tag, htext in HB.findall(body(ch)):
                kind = classify(htext, ttl)
                if not kind: continue
                f = fold(htext); raw = TAG.sub("", htext)
                m = LESSON.match(raw) or LABEL.match(raw)
                stripped = fold(raw[m.end():]) if (m and kind != "exact") else f
                in_gold_same = f in gold_heads; in_gold_stripped = stripped in gold_heads
                gold_has = "same" if in_gold_same else ("stripped" if in_gold_stripped else "absent")
                key = ("overview" if overview else "lesson", kind, gold_has)
                C[key] += 1; fam[tmpl][key[0] + "/" + kind] += 1
                rows.append({"code": code, "tmpl": tmpl, "page": os.path.basename(cp), "gold": os.path.basename(hp), "overview": overview,
                             "tag": tag, "heading": raw.strip()[:120], "title": ttl, "kind": kind, "gold_has": gold_has, "gold_title": gttl})
    summary = {"cases": len(rows), "by_page_type_kind_gold": {" | ".join(k): v for k, v in sorted(C.items())},
               "by_template": {k: dict(v) for k, v in fam.items()},
               "pages": len(set((r["code"], r["page"]) for r in rows)), "modules": len(set(r["code"] for r in rows))}
    json.dump({"summary": summary, "rows": rows}, open(os.path.join(HERE, "_r320_dupheading.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
