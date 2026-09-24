#!/usr/bin/env python3
"""Session 41 Round 9 — THE AUDIO-IMAGE POPULATION. Every gate module's Writers Template docx (word/document.xml paragraphs, in
order, table cells included): the `[Audio Image …]` tag lines (KB 01D `audio image` / `audioimage` → audio_image), the shape of
the 1–4 lines that follow ([Item N] [Image] desc / [Item N] [Audio] name — either order), the tag variants; against the gold's
`div.audioImage` count and Claude's. Run under WSL from CONVERTER_V2/reference/tests."""
import os, re, sys, glob, zipfile, collections, html as H
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN
TAG = re.compile(r"\[\s*audio\s*-?\s*image[^\]]*\]", re.I)
IMG = re.compile(r"\[\s*(?:image|photo)\s*\]", re.I)
AUD = re.compile(r"\[\s*audio\s*\]", re.I)
def paras(docx):
    try: x = zipfile.ZipFile(docx).read("word/document.xml").decode("utf8", "replace")
    except Exception: return []
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", x, re.S):
        t = H.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))).strip()
        if t: out.append(t)
    return out
variants = collections.Counter(); shapes = collections.Counter(); rows = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    wts = [f for f in glob.glob(os.path.join(hd, "*.docx")) if "media list" not in f.lower() or "writers template" in f.lower()]
    tags = 0; ok = 0
    for f in wts:
        P = paras(f)
        for i, t in enumerate(P):
            m = TAG.search(t)
            if not m: continue
            tags += 1
            variants[re.sub(r"\s+", " ", m.group(0).lower())] += 1
            nxt = P[i + 1:i + 3]
            rest = t[m.end():].strip()
            seq = ([rest] if rest else []) + nxt
            sh = "".join("I" if IMG.search(s) else ("A" if AUD.search(s) else ("T" if TAG.search(s) else "x")) for s in seq[:2])
            shapes[sh] += 1
            ok += sh in ("IA", "AI")
    g = sum(open(p, encoding="utf-8", errors="replace").read().count('class="audioImage"') for p in glob.glob(os.path.join(hd, "*.html")))
    c = sum(open(p, encoding="utf-8", errors="replace").read().count('class="audioImage"') for p in glob.glob(os.path.join(cd, "*.html")))
    if tags or g: rows.append((code, tags, ok, g, c))
print("tag variants:", variants.most_common(12))
print("following-line shapes (I image, A audio, T another tag, x other):", shapes.most_common(10))
print(f"modules with tags {sum(1 for r in rows if r[1])}; tags {sum(r[1] for r in rows)}; IA/AI {sum(r[2] for r in rows)}; gold audioImage {sum(r[3] for r in rows)}; claude {sum(r[4] for r in rows)}")
for r in sorted(rows, key=lambda r: -r[3]): print(f"  {r[0]:9s} tags {r[1]:3d}  IA/AI {r[2]:3d}  gold audioImage {r[3]:3d}  claude {r[4]:3d}")
