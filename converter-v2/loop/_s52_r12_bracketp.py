#!/usr/bin/env python3
"""_s52_r12_bracketp.py — session 52 Round 12: body paragraphs (outside the hand-off boxes, not red notes) whose visible text OPENS
with a '[' bracket — a writer's bracket rendered as learner text. Grouped by the bracket's first words; gold vs Claude counts;
and a URL-with-text paragraph census ('Source: https://…'). Regex-level. WSL."""
import re, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
P = re.compile(r"<(p|li|h[2-6])\b([^>]*)>(.*?)</\1>", re.S)
def spans_of(s):
    out = []
    for h in re.finditer(r'<div class="cv2-interactive[^"]*"', s):
        d = 0
        for x in re.finditer(r"<(/?)div\b[^>]*>", s[h.start():]):
            d += -1 if x.group(1) else 1
            if d == 0: out.append((h.start(), h.start() + x.end())); break
    return out
def census(root):
    st = collections.Counter(); pages = collections.defaultdict(set); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
    url = collections.Counter(); urlp = set()
    for f in glob.glob(root + "/*/*/*.html"):
        mod = f.split("/")[-2]
        s = open(f, encoding="utf-8", errors="replace").read(); b = s.find('id="body"'); e = s.find('class="acks'); sp = spans_of(s)
        if b < 0: continue
        for m in P.finditer(s, b):
            if e > 0 and m.start() > e: break
            if "cv2-note" in m.group(2) or any(a <= m.start() < z for a, z in sp): continue
            t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(3))).strip()
            if t.startswith("["):
                k = re.sub(r"[^a-z ]", "", t[1:].split("]")[0].lower())[:22].strip() or "(empty)"
                st[k] += 1; pages[k].add(f); mods[k].add(mod)
                if len(ex[k]) < 2: ex[k].append(f"{mod}: {t[:80]}")
            elif re.search(r"https?://", m.group(3)) and not re.fullmatch(r"\s*(?:<a\b[^>]*>)?\s*https?://\S+\s*(?:</a>)?\s*", m.group(3)):
                if re.search(r">\s*https?://", m.group(3)) or re.search(r"(?<![\"=])https?://", re.sub(r"<[^>]+>", " ", m.group(3))):
                    url["url-in-text"] += 1; urlp.add(f)
    return st, pages, mods, ex, url, urlp
for side, root in (("GOLD", R + "/01-Finalized_Modules_"), ("CLAUDE", R + "/01-Claude_Modules_")):
    st, pages, mods, ex, url, urlp = census(root)
    print(side, "bracket-opening blocks:", sum(st.values()), "on", len(set().union(*pages.values())) if pages else 0, "pages;", "visible URL inside text:", url["url-in-text"], "on", len(urlp), "pages")
    for k, n in st.most_common(14):
        print(f"  {n:4d} / {len(pages[k]):3d} pages / {len(mods[k]):3d} mods  [{k}]   e.g. {ex[k][0][:110]}")
