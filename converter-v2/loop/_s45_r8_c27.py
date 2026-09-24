#!/usr/bin/env python3
"""Session 45 Round 8 — KB c27 per-shape check: in every Claude dropQuiz layout="paragraph", classify each <li> — EMBEDDED (words after
the dropdown, or a sentence the dropdown completes) vs STANDALONE (the text before the dropdown is a complete question ending ? or :,
and nothing but punctuation after it). KB c27 / 03C: standalone Q&A pairs → the list layout. Also every no-layout (list) build.
WSL, from outputs/: python3 _s45_r8_c27.py"""
import os, re, io, glob, collections
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CL = os.path.join(ROOT, "01-Claude_Modules_")
def strip(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()
agg = collections.Counter(); ex = collections.defaultdict(list); quizzes = collections.Counter()
for p in glob.glob(os.path.join(CL, "*", "*", "*.html")):
    s = io.open(p, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r'<div class="dropQuiz[^"]*"( layout="([^"]*)")?>', s):
        lay = m.group(2) or "(list)"
        seg = s[m.end():m.end() + 60000]
        end = seg.find('class="activityButton reset"')
        seg = seg[:end if end > 0 else len(seg)]
        kinds = collections.Counter()
        for li in re.findall(r"<li>([\s\S]*?)</li>", seg):
            if "dropDown" not in li: continue
            q = li.find('<div class="dropQuestion">')
            if q < 0: continue
            before = strip(li[:q]);
            # after = text after the dropQuestion block's closing (rough: after the last </div>)
            after = strip(li[li.rfind("</div>") + 6:]) if "</div>" in li else ""
            if re.search(r"[?:]\s*$", before) and not re.search(r"[A-Za-zĀ-ſ]", after):
                kinds["standalone"] += 1
                if len(ex[(lay, "standalone")]) < 4: ex[(lay, "standalone")].append(f"{os.path.basename(p)} «{before[-60:]}»")
            else:
                kinds["embedded"] += 1
        quizzes[(lay, "mixed" if len(kinds) > 1 else (next(iter(kinds)) if kinds else "none"))] += 1
        agg.update({(lay, k): v for k, v in kinds.items()})
print("dropQuiz roots by (layout, item kinds):", dict(quizzes))
print("items:", dict(agg))
for k, v in ex.items(): print(" ", k, " | ".join(v))
