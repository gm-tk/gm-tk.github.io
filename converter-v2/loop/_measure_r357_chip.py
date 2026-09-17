#!/usr/bin/env python3
"""ROUND 357 PICK probe (loop session 19, Round 1 — the diff miner's first chrome class, DIFF_QUEUE F15 / F14):
THE #module-code CHIP'S PRESENCE per registry group, on BOTH page types.

Generalises the r336 instrument (_measure_r336_funchip.py — overview only, per base) to every PAIRED page of the
skeleton gate's population: for each (template, base, level) group and each page type (overview / lesson) it takes
the gold's chip PRESENCE share and majority FORM (absent / full-code / padded-number / decimal / free-text), Claude's
actual presence share and form, and the value the registry RESOLVES (outputs/_r357_resolved.json from
_r336_resolve_all.cjs). A group is a CLASS row when the gold's presence solidifies (share >= 0.60 of its paired
pages) and Claude's presence disagrees on >= 0.50 of them. The class is judged at the chrome floor (10 modules
over all class rows). Only PRESENCE is in play: the chip's text form is KB-status row 16's settled PARTIAL
(CL-0069 deliberately did not codify the padding) and the skeleton gate cannot see it.

Run from anywhere (WSL): python3 _measure_r357_chip.py  -> _r357_chip.json + _r357_chip.log next to itself.
"""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN

res = json.load(open(os.path.join(HERE, "_r357_resolved.json"), encoding="utf-8"))
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)


def base_level(code):
    m = re.match(r"([A-Z]+)(\d)", code)
    return (m.group(1), m.group(1) + m.group(2)) if m else (code, code)


def chip_form(html, code):
    h = html.split('<div id="header"', 1)[-1].split('<div id="body"', 1)[0]
    h = re.sub(r"<!--[\s\S]*?-->", "", h)
    m = re.search(r'id="module-code"[^>]*>\s*<h1>(.*?)</h1>', h, re.S)
    if not m:
        return "absent"
    t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    if t.upper() == code.upper():
        return "full-code"
    if re.fullmatch(r"\d\d", t):
        return "padded-number"
    if re.fullmatch(r"\d+(\.\d+)?", t):
        return "decimal"
    return "free-text"


groups = collections.defaultdict(lambda: {"gold": collections.Counter(), "claude": collections.Counter(), "pages": 0,
                                          "modules": set(), "agree": 0, "disagree_pages": [], "resolved": collections.Counter()})
codes = sorted(c for c in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, c)))
for code in codes:
    gdir = _corpus.mdir(HUMAN, code)
    tmpl = os.path.basename(os.path.dirname(gdir))
    base, level = base_level(code)
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or re.search(r"acks|acknowledge|glossary", os.path.basename(cp), re.I):
            continue
        ptype = "overview" if n == 0 else "lesson"
        gf = chip_form(open(hp, encoding="utf-8", errors="replace").read(), code)
        cf = chip_form(open(cp, encoding="utf-8", errors="replace").read(), code)
        g = groups[(tmpl, base, level, ptype)]
        g["gold"][gf] += 1; g["claude"][cf] += 1; g["pages"] += 1; g["modules"].add(code)
        g["resolved"][str((res.get(code, {}).get("module_code") or {}).get(ptype))] += 1
        if (gf == "absent") == (cf == "absent"):
            g["agree"] += 1
        else:
            g["disagree_pages"].append(f"{code}/{os.path.basename(cp)} gold={gf} claude={cf}")

rows = []
for k in sorted(groups):
    g = groups[k]
    n = g["pages"]
    gold_present = n - g["gold"]["absent"]
    claude_present = n - g["claude"]["absent"]
    gshare = gold_present / n
    gold_conv = "present" if gshare >= 0.60 else ("absent" if gshare <= 0.40 else "tie")
    dis = n - g["agree"]
    form = g["gold"].most_common(1)[0][0]
    flag = "CLASS" if (gold_conv != "tie" and dis / n >= 0.50) else ("partial" if dis else "")
    rows.append({"template": k[0], "base": k[1], "level": k[2], "ptype": k[3], "pages": n, "modules": len(g["modules"]),
                 "gold_present_share": round(gshare, 2), "gold_forms": dict(g["gold"]), "gold_majority_form": form,
                 "claude_present_share": round(claude_present / n, 2), "claude_forms": dict(g["claude"]),
                 "resolved": dict(g["resolved"]), "disagree_pages": dis, "gold_convention": gold_conv, "flag": flag,
                 "module_list": sorted(g["modules"]), "samples": g["disagree_pages"][:4]})
cls = [r for r in rows if r["flag"] == "CLASS"]
partial = [r for r in rows if r["flag"] == "partial"]
lines = [f"r357 chip probe — {len(codes)} modules, {sum(r['pages'] for r in rows)} paired pages, {len(rows)} (template, base, level, page-type) groups",
         f"CLASS rows: {len(cls)} — modules {len({m for r in cls for m in r['module_list']})}, pages disagreeing {sum(r['disagree_pages'] for r in cls)}", ""]
for r in cls:
    lines.append(f"CLASS {r['template']:12} {r['base']:7} {r['level']:8} {r['ptype']:8} n={r['pages']:3} mods={r['modules']:2} gold present {r['gold_present_share']:.2f} {r['gold_forms']} | "
                 f"claude present {r['claude_present_share']:.2f} {r['claude_forms']} | resolved {r['resolved']} | disagree {r['disagree_pages']} | e.g. {r['samples'][:2]}")
lines.append("")
lines.append(f"PARTIAL rows (some disagreement, under 0.50 or a gold tie): {len(partial)} — pages {sum(r['disagree_pages'] for r in partial)}")
for r in partial:
    lines.append(f"  part {r['template']:12} {r['base']:7} {r['level']:8} {r['ptype']:8} n={r['pages']:3} mods={r['modules']:2} gold {r['gold_present_share']:.2f} ({r['gold_convention']}) claude {r['claude_present_share']:.2f} resolved {r['resolved']} disagree {r['disagree_pages']} e.g. {r['samples'][:1]}")
open(os.path.join(HERE, "_r357_chip.log"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
json.dump(rows, open(os.path.join(HERE, "_r357_chip.json"), "w", encoding="utf-8"), indent=1)
print("\n".join(lines[:2]))
print(f"wrote _r357_chip.json / _r357_chip.log ({len(lines)} lines)")
