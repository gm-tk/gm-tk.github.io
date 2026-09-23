"""SESSION 40 ROUND 10 — split _s40_r10_imgdesc.py's population by the rest of the [Image] line: does it carry an iStock title /
stock-site words / a URL after the description (the stock-descriptor shape), or an instruction cue? Run under WSL."""
import re, collections, glob, os, importlib.util
spec = importlib.util.spec_from_file_location("m", "_s40_r10_imgdesc.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
STOCK = re.compile(r"istock|stock (?:photo|illustration|vector|image)|download image now|shutterstock|getty|https?://|www\.", re.I)
CUE = re.compile(r"\b(?:please|can (?:we|you|an)|could|source|create|recreate|choose|insert|snip|graph from|taken from)\b", re.I)
res = collections.Counter(); mods = collections.defaultdict(collections.Counter)
for d in sorted(glob.glob(f"{m.CL}/*/*/")):
    mod = os.path.basename(d.rstrip("/"))
    shape = {}
    for f in glob.glob(f"{m.GO}/*/{mod}/*parsed*.txt"):
        if "media list" in f.lower() and "writers" not in f.lower():
            continue
        for line in open(f, encoding="utf8", errors="ignore"):
            if not m.IMGTAG.search(line):
                continue
            after = m.IMGTAG.split(line, 1)[1]
            a2 = re.sub(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴", " | ", after).replace("🔴[RED TEXT]", " | ").replace("[/RED TEXT]🔴", " ").replace("║", " | ")
            parts = a2.split(" | ", 1)
            desc = m.norm(parts[0].replace("**", "").replace("__", "")); desc = re.sub(r"https?:\S+", "", desc).strip(" -–:")
            rest = after[len(parts[0]):] if len(parts) > 1 else ""
            if 2 <= len(desc.split()) and len(desc) <= 80:
                k = "cue" if CUE.search(desc) else ("stock" if STOCK.search(rest) or STOCK.search(parts[0]) else "plain")
                shape[desc] = k
    if not shape:
        continue
    cps = collections.Counter()
    for f in glob.glob(f"{d}*.html"):
        for pm in m.P.finditer(open(f, encoding="utf8", errors="ignore").read()):
            w = m.norm(pm.group(1))
            if w in shape:
                cps[w] += 1
    if not cps:
        continue
    gold = " ".join(m.norm(re.sub(r"<!--.*?-->", " ", open(g, encoding="utf8", errors="ignore").read(), flags=re.S)) for g in glob.glob(f"{m.GO}/*/{mod}/*.html"))
    for w, n in cps.items():
        key = (shape[w], "gold_has" if w in gold else "gold_lacks")
        res[key] += n; mods[key][mod] += n
for k, n in sorted(res.items()):
    print(k, n, "modules", len(mods[k]), mods[k].most_common(8))
