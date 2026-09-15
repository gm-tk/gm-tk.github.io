#!/usr/bin/env python3
"""ROUND 324 measure — the c79 residual: every paired lesson page whose Claude <h1><span> title differs from
the gold's, classified by the DIFFERENCE (the mechanism that would fix it): trailing punctuation only;
case/whitespace only; code prefix only; 'Lesson N' prefix; Claude = module title while the gold has its own
title (and where that gold title comes from in the parsed WT: [H2] Lesson N, first heading, boundary tag…);
gold = module title (the KB rejects); pair order (decision 4); other. Per template family. Writes
outputs/_r324_lessontitles.json. Run from FINAL_MODULE_DATA (WSL)."""
import os, re, sys, json, glob, collections, unicodedata
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"))
import _corpus
HUMAN = os.path.join(ROOT, "01-Finalized_Modules_"); CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
H1 = re.compile(r"<h1[^>]*>\s*<span[^>]*>(.*?)</span>\s*</h1>", re.S | re.I)
def spans(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip() for t in H1.findall(s)]
def fold(t):
    t = unicodedata.normalize("NFKD", t.lower()); t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", "", t).strip()
def pkey(f, code):
    m = re.search(r"[_\-](\d+)[._](\d+)\.html$", f) or re.search(r"[_\-](\d+)\.html$", f)
    return (float(m.group(1)) if m and not m.lastindex == 2 else float(f"{m.group(1)}.{m.group(2)}")) if m else None
def pages(d, code):
    out = {}
    for f in sorted(os.listdir(d)):
        if not f.lower().endswith(".html"): continue
        k = pkey(f, code)
        if k is not None: out[k] = os.path.join(d, f)
    return out
def wt_text(code):
    d = _corpus.mdir(HUMAN, code)
    for f in os.listdir(d):
        if f.endswith("_parsed.txt"): return open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
    return ""
cls = collections.Counter(); per_tmpl = collections.defaultdict(collections.Counter); samples = collections.defaultdict(list)
src = collections.Counter()
codes = _corpus.mods(HUMAN)
for code in codes:
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    if not os.path.isdir(cd): continue
    tmpl = os.path.basename(os.path.dirname(hd))
    gp, cp = pages(hd, code), pages(cd, code)
    ov = gp.get(0.0); mod_title = fold(spans(ov)[0]) if ov and spans(ov) else None
    wt = None
    for k in sorted(cp):
        if k == 0.0 or k not in gp: continue
        g, c = spans(gp[k]), spans(cp[k])
        if not g or not c: continue
        gt, ct = g[0], c[0]
        if fold(gt) == fold(ct) and len(g) == len(c):
            if gt == ct: cls["exact"] += 1
            elif gt.rstrip(".!:") == ct.rstrip(".!:") or ct.endswith(".") and not gt.endswith("."): cls["punct-only"] += 1; samples["punct-only"].append((code, k, gt, ct))
            else: cls["case/ws/macron-only"] += 1
            per_tmpl[tmpl]["match"] += 1; continue
        # differing
        if fold(gt) == fold(ct) and len(g) != len(c):
            kind = "pair-count (gold dual vs claude single or v.v.)"
        elif fold(ct) == mod_title and fold(gt) != mod_title:
            kind = "claude=module-title, gold=own"
            # where is the gold title in the WT?
            wt = wt if wt is not None else wt_text(code)
            gfold = fold(gt); lines = [l for l in wt.splitlines() if fold(l) and gfold and gfold in fold(l)]
            tag = None
            for l in lines[:3]:
                m = re.search(r"\[(H[1-3]|Lesson[^\]]*|Title[^\]]*|New page[^\]]*|Page[^\]]*|Activity[^\]]*)\]", l, re.I)
                tag = (m.group(1).split()[0].upper() if m else "plain-line"); break
            src[tag or "not-in-WT"] += 1
            samples[kind].append((code, k, gt, ct, tag or "not-in-WT"))
        elif fold(gt) == mod_title and fold(ct) != mod_title:
            kind = "gold=module-title (KB rejects)"
        elif re.match(r"^" + re.escape(code.lower()), fold(ct)) and fold(ct).replace(code.lower(), "").strip() == fold(gt):
            kind = "code-prefix only"; samples[kind].append((code, k, gt, ct))
        elif re.match(r"lesson (\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b", fold(ct)) and not re.match(r"lesson", fold(gt)):
            kind = "'Lesson N' prefix"; samples[kind].append((code, k, gt, ct))
        elif len(g) >= 2 and len(c) >= 2 and fold(g[0]) == fold(c[1]) and fold(g[1]) == fold(c[0]):
            kind = "pair order (decision 4)"
        elif fold(ct).rstrip(" .") == fold(gt).rstrip(" ."):
            kind = "punct-only"; samples[kind].append((code, k, gt, ct))
        else:
            kind = "other (editorial / different source)"
            if len(samples[kind]) < 40: samples[kind].append((code, k, gt, ct))
        cls[kind] += 1; per_tmpl[tmpl][kind] += 1
out = {"classes": dict(cls), "per_template": {k: dict(v) for k, v in per_tmpl.items()}, "gold_own_title_source_tag": dict(src),
       "samples": {k: v[:40] for k, v in samples.items()}}
json.dump(out, open(os.path.join(ROOT, "CONVERTER_V2", "outputs", "_r324_lessontitles.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("classes:", json.dumps(cls, indent=1)); print("gold own-title source tag (for claude=module-title):", dict(src))
for k in ("punct-only", "code-prefix only", "'Lesson N' prefix"):
    print("--", k, samples[k][:8])
print("-- claude=module-title, gold=own:", samples["claude=module-title, gold=own"][:12])
