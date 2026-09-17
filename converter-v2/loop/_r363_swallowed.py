#!/usr/bin/env python3
"""r363 PICK — decompose the r362 residue: the gold's activity h3 sits INSIDE Claude's capture (swallowed).
For each swallowed box, find the gold h3's text in the module's parsed WT and classify the WT line."""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, TESTS); sys.path.insert(0, HERE)
import _corpus
from anchor_compare import HUMAN
RED = re.compile(r"\U0001f534\[RED TEXT\]|\[/RED TEXT\]\U0001f534")
def norm(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
def wt_lines(code):
    d = _corpus.mdir(HUMAN, code)
    fs = [f for f in os.listdir(d) if f.endswith("_parsed.txt")]
    fs.sort(key=lambda f: -os.path.getsize(os.path.join(d, f)))
    if not fs: return []
    return [l.rstrip("\n") for l in open(os.path.join(d, fs[0]), encoding="utf-8", errors="replace")]
rows = json.load(open(os.path.join(HERE, "_r362_actlead.json"), encoding="utf-8"))
sw = [r for r in rows if r.get("swallowed")]
print("swallowed boxes", len(sw))
cache = {}
kinds = collections.Counter(); ex = collections.defaultdict(list)
for r in sw:
    code = r["module"]; h3 = norm(r["gold_h3"] or "")
    if not h3:
        kinds["no-h3-text"] += 1; continue
    if code not in cache: cache[code] = wt_lines(code)
    lines = cache[code]
    hit = None
    for i, l in enumerate(lines):
        nl = norm(RED.sub("", l))
        if h3 and (h3 == nl or (len(h3) > 8 and h3 in nl)):
            hit = i; break
    if hit is None:
        kinds["not-in-wt"] += 1; ex["not-in-wt"].append((code, r["page"], r["number"], (r["gold_h3"] or "")[:40])); continue
    raw = RED.sub("", lines[hit]).strip()
    prev = ""
    for j in range(hit - 1, max(-1, hit - 4), -1):
        if lines[j].strip(): prev = RED.sub("", lines[j]).strip(); break
    if re.match(r"^\s*\[(activity|interactive)[^\]]*\]\s*\S", raw, re.I):
        k = "on-activity-tag-line"
    elif re.match(r"^\s*\[h[1-6]\]", raw, re.I):
        k = "h-tagged-line"
    elif re.match(r"^\s*\[(activity|interactive)[^\]]*\]", prev, re.I):
        k = "plain-line-after-tag"
    elif re.match(r"^\s*\[", raw):
        k = "other-tag-line:" + re.match(r"^\s*\[([^\]]{0,25})", raw).group(1).lower().split(":")[0].strip()
    elif raw.startswith("**") or raw.startswith("*"):
        k = "bold/italic-plain-line"
    else:
        k = "plain-line"
    kinds[k] += 1
    if len(ex[k]) < 6: ex[k].append((code, r["page"], r["number"], raw[:70], "PREV:" + prev[:50]))
for k, v in kinds.most_common(): print(f"{v:4}  {k}")
for k, v in ex.items():
    print("==", k)
    for e in v: print("   ", e)

print("\n=== on-activity-tag-line decomposed: opening widget × tag-line shape ===")
shape = collections.Counter(); shape_ex = collections.defaultdict(list); mods = collections.defaultdict(set); pages = collections.defaultdict(set)
for r in sw:
    code = r["module"]; h3 = norm(r["gold_h3"] or "")
    if not h3: continue
    lines = cache.get(code) or wt_lines(code); cache[code] = lines
    hit = None
    for i, l in enumerate(lines):
        nl = norm(RED.sub("", l))
        if h3 == nl or (len(h3) > 8 and h3 in nl): hit = i; break
    if hit is None: continue
    raw = RED.sub("", lines[hit]).strip()
    if not re.match(r"^\s*\[(activity|interactive)[^\]]*\]\s*\S", raw, re.I): continue
    tags = re.findall(r"\[([^\]]+)\]", raw)
    first = tags[0].lower()
    if len(tags) >= 2: sh = "two-tags-on-line"
    elif re.search(r"[–:-]\s*\w", first) and re.search(r"quiz|drag|drop|click|match|carousel|flip|accordion|modal|tab|slider|sort|reorder|checkbox|fill", first): sh = "widget-in-activity-tag"
    else: sh = "plain-[Activity N]-title"
    k = (r["claude_first"].split(":")[-1], sh)
    shape[k] += 1; mods[k].add(code); pages[k].add(code + "/" + r["page"])
    if len(shape_ex[k]) < 5: shape_ex[k].append((code, r["page"], r["number"], raw[:80]))
for k, v in shape.most_common():
    print(f"{v:4}  boxes / {len(mods[k])} modules / {len(pages[k])} pages  {k}")
    for e in shape_ex[k]: print("      ", e)

print("\n=== the plain-[Activity N]-title sub-class by the TAG on the title line ===")
tagk = collections.Counter(); tmods = collections.defaultdict(set); tpages = collections.defaultdict(set); tex = collections.defaultdict(list)
for r in sw:
    code = r["module"]; h3 = norm(r["gold_h3"] or "")
    if not h3: continue
    lines = cache.get(code) or wt_lines(code); cache[code] = lines
    hit = None
    for i, l in enumerate(lines):
        nl = norm(RED.sub("", l))
        if h3 == nl or (len(h3) > 8 and h3 in nl): hit = i; break
    if hit is None: continue
    raw = RED.sub("", lines[hit]).strip()
    m = re.match(r"^\s*\[([^\]]+)\]\s*(\S.*)$", raw)
    if not m: continue
    tag = re.sub(r"\s+", " ", m.group(1).strip().lower())
    tag = re.sub(r"\b\d+[a-z]?\b", "N", tag)
    k = (r["claude_first"].split(":")[-1], tag)
    tagk[k] += 1; tmods[k].add(code); tpages[k].add(code + "/" + r["page"])
    if len(tex[k]) < 3: tex[k].append((code, r["page"], r["number"], raw[:70]))
for k, v in tagk.most_common(25):
    print(f"{v:4}  boxes / {len(tmods[k])} modules / {len(tpages[k])} pages  {k}")
    for e in tex[k]: print("      ", e)
