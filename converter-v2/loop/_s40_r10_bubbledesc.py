"""SESSION 40 ROUND 10 (24 Sept 2026) — the §3 MEASURE step: D13-9 part 1's residue — a built speech bubble whose SPEECH carries
the writer's IMAGE DESCRIPTION line ("avatar Tina" — the words after an `[Image]` tag, before the red "from:" seam / the iStock
title), because the bubble consumed the same-block image as its avatar and rendered the image item's own words as a paragraph.

For every Claude page with a `speechBubble` row: every <p> inside a `bubble-basic` div; a paragraph is an IMAGE-DESCRIPTION leak
when the module's parsed Writers Template carries it right after an `[Image]`-family tag (`[Image]`, `[RHSImage]`, `[Image N]` …).
Counts per module / family, and whether the gold carries the same words anywhere on the module.
Run under WSL:  python3 _s40_r10_bubbledesc.py > _s40_r10_bubbledesc.log
"""
import html as H, os, re, collections, glob

ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
CL, GO = f"{ROOT}/01-Claude_Modules_", f"{ROOT}/01-Finalized_Modules_"
BUB = re.compile(r'<div class="bubble-basic[^"]*">(.*?)</div>\s*</div>', re.S)
P = re.compile(r"<p>(.*?)</p>", re.S)
IMGTAG = re.compile(r"\[\s*(?:RHS\s*)?image(?:\s*\d+)?\s*\]", re.I)


def norm(s):
    s = H.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'")).strip().lower()


def wt_image_lines(mod):
    out = set()
    for f in glob.glob(f"{GO}/*/{mod}/*parsed*.txt"):
        for line in open(f, encoding="utf8", errors="ignore"):
            if not IMGTAG.search(line):
                continue
            after = IMGTAG.split(line, 1)[1]
            after = re.sub(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴", " | ", after)   # a red run ends the description
            after = after.replace("🔴[RED TEXT]", " | ").replace("[/RED TEXT]🔴", " ")
            desc = norm(after.split(" | ")[0].replace("**", "").replace("__", ""))
            if 2 <= len(desc) <= 80:
                out.add(desc)
    return out


def main():
    hits = collections.Counter()
    pages = collections.defaultdict(set)
    bubbles = collections.Counter()
    gold_has = {}
    samples = []
    for d in sorted(glob.glob(f"{CL}/*/*/")):
        mod = os.path.basename(d.rstrip("/"))
        files = sorted(glob.glob(f"{d}*.html"))
        texts = {f: open(f, encoding="utf8", errors="ignore").read() for f in files}
        if not any("speechBubble" in t for t in texts.values()):
            continue
        descs = None
        for f, t in texts.items():
            for bm in BUB.finditer(t):
                bubbles[mod] += 1
                for pm in P.finditer(bm.group(1)):
                    w = norm(pm.group(1))
                    if not w:
                        continue
                    if descs is None:
                        descs = wt_image_lines(mod)
                    if w in descs:
                        hits[mod] += 1
                        pages[mod].add(os.path.basename(f))
                        if mod not in gold_has:
                            gold = " ".join(norm(open(g, encoding="utf8", errors="ignore").read()) for g in glob.glob(f"{GO}/*/{mod}/*.html"))
                            gold_has[mod] = gold
                        if len(samples) < 30:
                            samples.append((mod, os.path.basename(f), w, w in gold_has[mod]))
    print(f"image-description paragraphs inside built bubbles: {sum(hits.values())} on {sum(len(v) for v in pages.values())} pages / {len(hits)} modules")
    for mod, n in hits.most_common():
        print(f"  {mod}: {n} leaks on {len(pages[mod])} pages (of {bubbles[mod]} bubbles)")
    fam = collections.Counter()
    for mod, n in hits.items():
        fam[re.match(r"[A-Z]+", mod).group(0)] += n
    print("by prefix:", fam.most_common())
    for s in samples:
        print("  sample:", s)


if __name__ == "__main__":
    main()
