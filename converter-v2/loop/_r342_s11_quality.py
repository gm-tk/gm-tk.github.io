#!/usr/bin/env python3
"""_r341_quality.py — ROUND 342 (session 11) proofs over the affected modules (outputs/_r342_s11_on/<code>/<page> = the ON output; disk = the
last-shipped corpus). (1) LEAK: the protected gate's own predicate (_structural_defect_audit.visible_text + LITERAL_TAG)
per page, disk vs ON — leaks must fall, never rise per module. (2) WORD-LOSS: the ON page must lose no writer word vs disk;
the only permitted losses are the literal tag tokens themselves (h3/body/image…) and converter notes (chrome). A module
whose page SET changed (near-red page boundaries now recognised) is compared module-wide (union of pages).
Run from reference/tests under WSL."""
import os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS); import _corpus
import _structural_defect_audit as A
OUT = os.path.join(HERE, "..", "..", "01-Claude_Modules_"); ON = os.path.join(HERE, "_r342_s11_on")
AFF = [l.strip() for l in open(os.path.join(HERE, "_r342_s11_affected.txt")) if l.strip()]
TAGWORDS = set("h1 h2 h3 h4 h5 h6 body image images text activity individual interactive embedded link video accordion tabs answer button add carousel rollover hintslider definition insert item quote important alert click drop dropdown list".split())
def leaks(html):
    body = html[html.find('id="body"'):] if 'id="body"' in html else html
    return len(list(A.LITERAL_TAG.finditer(A.visible_text(body))))
def words(html):
    """EVERY word the page carries — visible text, converter notes, hand-off dump text AND attribute values (info=, alt=,
    src=, href=) — so a word that merely MOVED (into a Writers Note, a widget box or a tooltip) is not reported lost."""
    body = html.split("<body", 1)[-1]
    body = re.sub(r"<script[\s\S]*?</script>", "", body)
    attrs = " ".join(re.findall(r'(?:info|alt|src|href|title)="([^"]*)"', body))
    t = re.sub(r"<[^>]+>", " ", body) + " " + attrs; t = re.sub(r"&[a-z#0-9]+;", " ", t)
    return collections.Counter(w.lower() for w in re.findall(r"[\w'’-]+", t))
tot_disk = tot_on = 0; rows = []; lost_all = collections.Counter(); worse = []
for c in AFF:
    dd = _corpus.mdir(OUT, c); od = os.path.join(ON, c)
    dpages = {f: open(os.path.join(dd, f), encoding="utf-8").read() for f in os.listdir(dd) if f.endswith(".html")}
    opages = {f: open(os.path.join(od, f), encoding="utf-8").read() for f in os.listdir(od) if f.endswith(".html")}
    ld = sum(leaks(h) for h in dpages.values()); lo = sum(leaks(h) for h in opages.values())
    tot_disk += ld; tot_on += lo
    wd = sum((words(h) for h in dpages.values()), collections.Counter()); wo = sum((words(h) for h in opages.values()), collections.Counter())
    lost = wd - wo; real = collections.Counter({w: n for w, n in lost.items() if w not in TAGWORDS and not re.fullmatch(r"\d+[a-z]?|[a-z]", w)})
    for w, n in real.items(): lost_all[w] += n
    if lo > ld: worse.append(c)
    rows.append((c, len(dpages), len(opages), ld, lo, sum(real.values()), [w for w, _ in real.most_common(6)]))
print("%-9s %5s %5s %6s %6s %6s  %s" % ("module", "pgD", "pgON", "leakD", "leakON", "lostW", "sample lost words (tag tokens + notes + dump text excluded)"))
for r in rows: print("%-9s %5d %5d %6d %6d %6d  %s" % r)
print("\nTOTAL leaks disk", tot_disk, "-> ON", tot_on, "| modules with MORE leaks:", worse or "none")
print("lost words overall (top 30):", lost_all.most_common(30))
