#!/usr/bin/env python3
"""ROUND 337 PICK probe (loop session 6) — consecutive bare-<p> runs whose text opens with a number, in BOTH forms: the writer's
TYPED sequence (1. 2. 3.) and the extractor's Word-numbered-list marker (1. on every item); by nearest widget ancestor and template.
Writes _r337_numruns.json next to itself. Run from anywhere."""
import re, glob, os, collections, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
NUM = re.compile(r'^\s*(\d{1,2})\s*[.)]\s+\S')
W = re.compile(r'<div class="((?:accordion|accContent|tabs|tab-pane|clickDrop\w*|dropQuiz|mcq\w*|flipCard|front|back|carousel-caption|carousel|speechBubble|bubble\w*|hintSlider|hintDropContent|TKmodal|dragAndDrop|question|selfCheck|activity|alert\w*|super-content)[^"]*)"')
P = re.compile(r'<p>(?:(?!</p>)[\s\S])*</p>(?:\s*<p>(?:(?!</p>)[\s\S])*</p>)+')
runs_by = collections.Counter(); pages = collections.defaultdict(set); mods = set(); forms = collections.Counter(); by_tmpl = collections.Counter(); ex = []
for f in glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", "*", "*.html")):
    if re.search(r'acks|ackn', f, re.I): continue
    tmpl = os.path.basename(os.path.dirname(os.path.dirname(f))); code = os.path.basename(os.path.dirname(f))
    s = open(f, encoding='utf-8', errors='replace').read().split('<div id="body"', 1)[-1]; s = re.sub(r'<div class="acks[\s\S]*', '', s)
    s = re.sub(r'<div class="cv2-interactive[\s\S]*?</div>\s*</div>\s*</div>', '<CV2/>', s); s = re.sub(r'<p class="cv2-(?:note|comment)"[^>]*>[\s\S]*?</p>', '', s)
    for m in P.finditer(s):
        items = [re.sub(r'<[^>]+>', '', x) for x in re.findall(r'<p>((?:(?!</p>)[\s\S])*)</p>', m.group(0))]
        grp = []
        for t in items:
            mm = NUM.match(t)
            if not mm: break
            n = int(mm.group(1))
            if not grp or n == grp[-1] + 1 or (all(g == grp[0] for g in grp) and n == grp[0]): grp.append(n)
            else: break
        if len(grp) >= 2:
            form = 'typed-sequential' if grp[1] == grp[0] + 1 else ('word-list (all 1.)' if grp[0] == 1 else 'all-equal N')
            forms[form] += 1
            ws = [x.group(1).split()[0] for x in W.finditer(s[:m.start()])]; anc = ws[-1] if ws else 'none'
            runs_by[(form, anc)] += 1; pages[form].add(f); mods.add(code); by_tmpl[tmpl] += 1
            if len(ex) < 8: ex.append((code, os.path.basename(f), form, anc, items[0][:50]))
allp = set().union(*pages.values()) if pages else set()
print("forms", dict(forms)); print("pages", len(allp), "modules", len(mods), "by template", dict(by_tmpl))
for k, v in runs_by.most_common(24): print("  ", k, v)
for e in ex: print("  ", e)
json.dump({"forms": dict(forms), "pages": {k: sorted(os.path.relpath(p, ROOT) for p in v) for k, v in pages.items()}, "modules": sorted(mods), "runs_by": {f"{a}|{b}": v for (a, b), v in runs_by.items()}}, open(os.path.join(HERE, "_r337_numruns.json"), "w", encoding="utf-8"), indent=1)
