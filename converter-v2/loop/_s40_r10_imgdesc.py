"""SESSION 40 ROUND 10 (24 Sept 2026) — the §3 MEASURE step: does the writer's `[Image] <description>` line ship as a visible <p>
next to the image, and does the gold ship those words?

For every module: the parsed Writers Template's image-description lines (the words right after an `[Image]`-family tag, up to
the first red run / iStock title — the same reading as _s40_r10_bubbledesc.py); for each description (>= 2 words, <= 80 chars):
is it a whole <p> on a Claude page, and are its words anywhere in the gold's HTML (comments stripped)? A description the gold
never ships but Claude prints is the class; one the gold also prints is a caption the gold keeps.
Run under WSL:  python3 _s40_r10_imgdesc.py > _s40_r10_imgdesc.log
"""
import html as H, os, re, collections, glob

ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
CL, GO = f"{ROOT}/01-Claude_Modules_", f"{ROOT}/01-Finalized_Modules_"
IMGTAG = re.compile(r"\[\s*(?:RHS\s*)?image(?:\s*\d+)?\s*\]", re.I)
P = re.compile(r"<p>(.*?)</p>", re.S)


def norm(s):
    s = H.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'")).strip().lower()


def descs(mod):
    out = collections.Counter()
    for f in glob.glob(f"{GO}/*/{mod}/*parsed*.txt"):
        if "media list" in f.lower() and "writers" not in f.lower():
            continue
        for line in open(f, encoding="utf8", errors="ignore"):
            if not IMGTAG.search(line):
                continue
            after = IMGTAG.split(line, 1)[1]
            after = re.sub(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴", " | ", after)
            after = after.replace("🔴[RED TEXT]", " | ").replace("[/RED TEXT]🔴", " ").replace("║", " | ")
            d = norm(after.split(" | ")[0].replace("**", "").replace("__", ""))
            d = re.sub(r"https?:\S+", "", d).strip(" -–:")
            if 2 <= len(d.split()) and len(d) <= 80:
                out[d] += 1
    return out


def main():
    tot = collections.Counter()
    per_mod = collections.Counter()
    fam = collections.Counter()
    samples = []
    for d in sorted(glob.glob(f"{CL}/*/*/")):
        mod = os.path.basename(d.rstrip("/"))
        ds = descs(mod)
        if not ds:
            continue
        cps = collections.Counter()
        for f in glob.glob(f"{d}*.html"):
            for pm in P.finditer(open(f, encoding="utf8", errors="ignore").read()):
                w = norm(pm.group(1))
                if w in ds:
                    cps[w] += 1
        if not cps:
            continue
        gold = " ".join(norm(re.sub(r"<!--.*?-->", " ", open(g, encoding="utf8", errors="ignore").read(), flags=re.S))
                        for g in glob.glob(f"{GO}/*/{mod}/*.html"))
        for w, n in cps.items():
            ing = w in gold
            tot["claude_p"] += n
            tot["gold_has" if ing else "gold_lacks"] += n
            if not ing:
                per_mod[mod] += n
                fam[os.path.basename(os.path.dirname(d.rstrip("/")))] += n
                if len(samples) < 40:
                    samples.append((mod, w))
    print("image-description <p> on Claude pages:", dict(tot))
    print("gold-lacks by template family:", fam.most_common())
    print("gold-lacks modules:", len(per_mod), "top:", per_mod.most_common(20))
    for s in samples:
        print("  sample:", s)


if __name__ == "__main__":
    main()
