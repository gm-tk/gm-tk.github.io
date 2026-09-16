#!/usr/bin/env python3
"""_measure_r348_menulabels.py — the D10-9 pre-measurement (queue item 6: KB c23 / 01B lesson-menu labels everywhere).
Reuses the r341 void-aware #module-menu-content parser. Over every paired LESSON page: (1) the GOLD's label wording by ROLE
(learning / success) per module — the success wording ("i can" vs "you will show your understanding by") against the code's
level digit + series = the year-level table 01B lines 240–244 need; (2) the gold's section-title lines above / between the
labels (does the gold keep "Learning intentions" / "How will I know…" on a lesson page? 01B line 223 says drop); (3) every
Claude lead-in wording in the menu (the ROLE classifier's input) with its gold tag. Run under WSL: python3 _measure_r348_menulabels.py
Writes _r348_menulabels.json and prints the summary."""
import os, sys, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T = os.path.normpath(os.path.join(HERE, "..", "reference", "tests")); sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
# import only the parser pieces (the r341 module runs its census at import — read them by exec of the top part instead)
src = open(os.path.join(HERE, "_measure_r341_menulabels.py"), encoding="utf-8").read().split("idx = json.load(")[0]
ns = {"__file__": os.path.join(HERE, "_measure_r341_menulabels.py")}; exec(compile(src, "r341_parser", "exec"), ns); menu = ns["menu"]; fold = ns["fold"]

LEARN = re.compile(r"^(we(?:\s+are)?\s+learning\b|what are we learning|learning intentions?\b|ākonga will\b|akonga will\b|ākonga can\b|students will\b|i am learning to\b|walt\b)")
SUCC = re.compile(r"^(i can\b|you will (?:show|demonstrate) your understanding\b|success criteria\b|how will i know\b|wilf\b|you will be able to\b)")
TITLE = re.compile(r"^(learning intentions?|success criteria|how will i know(?: if i've learned it)?|what are we learning(?: today)?|lesson (?:objectives?|goals?))$")
def role(t):
    if SUCC.match(t): return "success"
    if LEARN.match(t): return "learning"
    return None
def succ_form(t):
    if t.startswith("i can"): return "i can"
    if re.match(r"you will (?:show|demonstrate) your understanding", t): return "you will show your understanding by"
    if t.startswith("success criteria"): return "success criteria"
    if t.startswith("how will i know"): return "how will i know"
    return "other"
idx = json.load(open(os.path.join(T, "..", "..", "..", "pageforge-site", "converter-v2", "data", "Module_Structure_Index.json"), encoding="utf-8")).get("module_meta", {})
per_mod = {}; lead_c = collections.Counter(); lead_gold = collections.defaultdict(collections.Counter); titles_g = collections.Counter(); titles_g_pages = 0; pages = 0
for code in sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d))):
    meta = idx.get(code, {}); digit = re.sub(r"^[A-Z]+", "", code)[:1]
    pm = per_mod.setdefault(code, {"series": meta.get("series"), "subject": meta.get("subject"), "digit": digit, "gold_success": collections.Counter(), "gold_learning_tag": collections.Counter(), "gold_success_tag": collections.Counter(), "gold_titles": collections.Counter(), "pages": 0})
    for n, cp, hp in pairs(code):
        if "_0_0" in cp or re.search(r"acks|acknowledge|glossary", os.path.basename(hp) + os.path.basename(cp), re.I): continue
        fc, ce = menu(cp); fg, ge = menu(hp)
        if not (fc and fg): continue
        pages += 1; pm["pages"] += 1
        seen_title = False
        for tag, t in ge:
            if tag == "li": continue
            if TITLE.match(t): pm["gold_titles"][f"{tag}:{t[:32]}"] += 1; titles_g[f"{tag}:{t[:32]}"] += 1; seen_title = True; continue
            r = role(t)
            if r == "success": pm["gold_success"][succ_form(t)] += 1; pm["gold_success_tag"][tag] += 1
            elif r == "learning": pm["gold_learning_tag"][tag] += 1
        if seen_title: titles_g_pages += 1
        gmap = collections.defaultdict(list)
        for tag, t in ge: gmap[t].append(tag)
        for tag, t in ce:
            if tag == "li": continue
            r = role(t)
            if not r: continue
            lead = " ".join(t.split()[:4]); lead_c[(r, lead)] += 1
            g = gmap.get(t) or []
            if not g:
                pre = " ".join(t.split()[:3]); cand = [k for k in gmap if k.startswith(pre)]
                g = gmap[cand[0]] if cand else []
            lead_gold[(r, lead)]["h5" if "h5" in g else (g[0] if g else "absent")] += 1
# the year-level table: success wording by (series, digit)
tab = collections.defaultdict(collections.Counter)
for code, pm in per_mod.items():
    for form, n in pm["gold_success"].items(): tab[(pm["series"] or "?", pm["digit"])][form] += n
out = {"pages": pages, "gold_success_wording_by_series_digit": {f"{s} | {d}": dict(c.most_common()) for (s, d), c in sorted(tab.items())},
       "gold_section_titles_on_lesson_pages": {"pages_with_a_title": titles_g_pages, "of_pages": pages, "titles": dict(titles_g.most_common(20))},
       "claude_leadins_by_role": {f"{r} | {l}": {"n": n, "gold": dict(lead_gold[(r, l)].most_common())} for (r, l), n in lead_c.most_common(40)},
       "per_module": {c: {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in pm.items()} for c, pm in per_mod.items() if pm["pages"]}}
json.dump(out, open(os.path.join(HERE, "_r348_menulabels.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("paired lesson pages with a menu on both sides:", pages)
print("\nGOLD success-label wording by series | level digit  (the 01B year-level table: 'I can:' years 7–10, 'You will show…' years 1–6):")
for k, v in out["gold_success_wording_by_series_digit"].items(): print(f"  {k:32s} {v}")
print("\nGOLD section titles kept on lesson pages (01B line 223 says none):", out["gold_section_titles_on_lesson_pages"]["pages_with_a_title"], "of", pages)
for k, v in out["gold_section_titles_on_lesson_pages"]["titles"].items(): print(f"  {v:4d}  {k}")
print("\nCLAUDE lead-ins in the menu by role (top 40) with the gold's tag for the same label:")
for k, v in out["claude_leadins_by_role"].items(): print(f"  {v['n']:4d}  {k:60s} gold {v['gold']}")
# modules where the gold mixes both success forms
mixed = [c for c, pm in per_mod.items() if len([f for f in pm["gold_success"] if f in ("i can", "you will show your understanding by")]) > 1]
print("\nmodules whose gold uses BOTH 'I can' and 'You will show…':", len(mixed), mixed[:20])
