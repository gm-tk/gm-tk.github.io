#!/usr/bin/env python3
"""Session 44 Round 3 — two TRR-lesson sub-classes sized over every Bilingual module (Claude corpus vs gold):
 (b) the IDENTICAL reo / eng pair: Claude `<X reo>T</X>` immediately followed by `<X eng>T</X>` with the same text T — how often does the
     gold carry T once vs twice (same page), per element tag;
 (c) the audio-word line: gold `p.center-text.sassoonI-text` (with span.audioButton) — how many, and what Claude has for the same text.
WSL, from outputs/: python3 _s44_r3_bilpairs.py"""
import os, re, glob, io, collections, html as H
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_", "Bilingual"); CL = os.path.join(ROOT, "01-Claude_Modules_", "Bilingual")
def norm(t): return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", t))).strip().lower()
PAIR = re.compile(r"<(h[1-6]|p|li)\s+reo>(.*?)</\1>\s*<\1\s+eng>(.*?)</\1>", re.S)
EL = re.compile(r"<(h[1-6]|p|li)\b[^>]*>(.*?)</\1>", re.S)
tot = collections.Counter(); ex = collections.defaultdict(list); pages = collections.defaultdict(set); mods = collections.defaultdict(set)
aud_g = collections.Counter(); aud_c = collections.Counter(); aud_ex = []
def goldpage(code, cpage):
    d = os.path.join(GOLD, code)
    base = cpage.replace(".html", "")
    for cand in (cpage, base.replace("_0", ".0") + ".html", re.sub(r"_(\d+)_(\d+)$", r"_\1.\2", base) + ".html", re.sub(r"_(\d+)_(\d+)$", r".0\1", base) + ".html"):
        p = os.path.join(d, cand)
        if os.path.exists(p): return p
    m = re.search(r"_(\d+)_(\d+)", cpage)
    if m:
        for p in glob.glob(os.path.join(d, "*.html")):
            if re.search(rf"[_.]0?{m.group(1)}[_.]{m.group(2)}\b", os.path.basename(p)) or re.search(rf"\.0?{m.group(1)}\.html$", p): return p
    return None
for cdir in sorted(glob.glob(os.path.join(CL, "*"))):
    code = os.path.basename(cdir)
    for cp in sorted(glob.glob(os.path.join(cdir, "*.html"))):
        cs = io.open(cp, encoding="utf-8", errors="replace").read()
        gp = goldpage(code, os.path.basename(cp))
        gs = io.open(gp, encoding="utf-8", errors="replace").read() if gp else ""
        gcount = collections.Counter((m.group(1), norm(m.group(2))) for m in EL.finditer(gs))
        gtext = collections.Counter(norm(m.group(2)) for m in EL.finditer(gs))
        for m in PAIR.finditer(cs):
            t, a, b = m.group(1), norm(m.group(2)), norm(m.group(3))
            if not a or a != b: continue
            n = gtext.get(a, 0)
            k = (t, "gold-once" if n == 1 else "gold-twice" if n >= 2 else "gold-absent" if gp else "no-gold-page")
            tot[k] += 1; pages[k].add(code + "/" + os.path.basename(cp)); mods[k].add(code)
            if len(ex[k]) < 4: ex[k].append(f"{code}/{os.path.basename(cp)} «{a[:30]}»")
        for m in re.finditer(r'<p[^>]*class="[^"]*sassoonI-text[^"]*"[^>]*>(.*?)</p>', gs, re.S):
            txt = norm(m.group(1)); aud_g[code] += 1
            where = "claude-h" if re.search(rf"<h[1-6][^>]*>\s*{re.escape(txt)}\s*</h[1-6]>", norm_c := cs, re.I) else "other"
            aud_c[where] += 1
            if len(aud_ex) < 8: aud_ex.append(f"{code}/{os.path.basename(cp)} «{txt[:30]}» {where}")
print("(b) identical reo/eng pairs in Claude, by the gold's count of that text on the paired page:")
for k, v in sorted(tot.items(), key=lambda x: -x[1]):
    print(f"  {k[0]:3} {k[1]:13} {v:5d} pairs / {len(pages[k]):3d} pages / {len(mods[k]):2d} modules  e.g. {'; '.join(ex[k][:3])}")
print("(c) gold audio-word lines p.sassoonI-text:", sum(aud_g.values()), "in", len(aud_g), "modules", dict(aud_g.most_common(12)))
print("    Claude has the same text as a heading:", dict(aud_c)); [print("   ", e) for e in aud_ex]
