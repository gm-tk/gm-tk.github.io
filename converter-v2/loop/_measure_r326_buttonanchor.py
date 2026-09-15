#!/usr/bin/env python3
"""ROUND 326 (loop session 4, Round 1) — IS A CALL-TO-ACTION BUTTON ALWAYS AN ANCHOR?

The KB's universal button form (05D_COMP14_BUTTONS_TABLES_COLUMNS lines 11 / 58-59 / 83):
    <a href="URL" target="_blank"><div class="button">Button text</div></a>
and the gold agrees: a `div.button` / `div.buttonD` that is NOT a JS-driven widget button
(clickDrop / TKmodalButton / rSBtn) sits inside an <a> in ~99% of cases — even when the developer
has not wired the target yet (`href=""` / `href="#"`, 240+ gold buttons). Claude's generic
[button] emit (`Emit_Templates.buttons.button.form`) is the BARE `<div class="button">{label}</div>`
unless a URL was absorbed, so hundreds of upload / journal / quiz / plain buttons ship without the
anchor the skeleton gate can see.

Measures, on BOTH sides, per template family × subject prefix × label category
(upload / journal / quiz / download / other): wrapped (by href kind) vs bare. The gold's wrapped
share is the convention test (LOOP §3: >= 0.60 per group or DECLINE); Claude's bare count is the
population the fix moves. Writes outputs/_r326_buttonanchor.json + _r326_affected.txt.
USAGE: python3 _measure_r326_buttonanchor.py [CODE …]
"""
import os, re, sys, json
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(BASE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)
import _corpus

HUMAN = os.path.join(ROOT, "01-Finalized_Modules_")
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
SKIP_PAGE = re.compile(r"acks|acknowledge|glossary|references", re.I)
BTN = re.compile(r'<div class="((?:button|buttonD)(?:\s[^"]*)?)">\s*(.*?)\s*</div>', re.S)
JS_CLASSES = {"clickDrop", "TKmodalButton", "rSBtn", "externalButton"}
UPLOAD = re.compile(r"^(Upload to [Dd]ropbox|Go to [Dd]ropbox|Go to portfolio)\.?$")
A_TAIL = re.compile(r"<a\s[^>]*>$")


def category(label, mods):
    l = label.lower()
    if UPLOAD.match(label): return "upload"
    if re.match(r"go to (the )?quiz", l): return "quiz"
    if "downloadButton" in mods: return "download"
    if "journal" in l: return "journal"
    return "other"


def href_kind(a):
    m = re.search(r'href="([^"]*)"', a)
    h = m.group(1) if m else ""
    if h in ("", "#"): return "a:empty"
    if "quickLink" in h: return "a:d2l"
    return "a:url"


def scan(root, codes):
    by_group = defaultdict(Counter)      # (tmpl, prefix, cat) -> {wrapped, bare}
    by_cat = defaultdict(Counter)        # cat -> {a:empty, a:d2l, a:url, bare}
    bare_pages = set(); bare_mods = set(); bare_rows = []
    for code in codes:
        d = _corpus.mdir(root, code)
        if not os.path.isdir(d): continue
        tmpl = os.path.basename(os.path.dirname(d))
        prefix = re.match(r"[A-Z]+", code).group(0) if re.match(r"[A-Z]+", code) else code
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html") or SKIP_PAGE.search(f): continue
            s = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
            for m in BTN.finditer(s):
                mods = m.group(1).split()
                if any(x in JS_CLASSES for x in mods): continue
                label = re.sub(r"<[^>]+>", "", m.group(2)).strip()
                if len(label) > 80 or "\n" in label: continue
                cat = category(label, mods)
                pre = s[:m.start()].rstrip()
                a = A_TAIL.search(pre)
                kind = href_kind(a.group(0)) if a else "bare"
                by_group[(tmpl, prefix, cat)]["wrapped" if a else "bare"] += 1
                by_cat[cat][kind] += 1
                if not a:
                    bare_pages.add((code, f)); bare_mods.add(code)
                    bare_rows.append([code, f, mods[0], cat, label[:60]])
    return by_group, by_cat, bare_pages, bare_mods, bare_rows


def main(argv):
    codes = argv or _corpus.mods(HUMAN)
    g_grp, g_cat, g_pages, g_mods, _ = scan(HUMAN, codes)
    c_grp, c_cat, c_pages, c_mods, c_rows = scan(CLAUDE, [c for c in codes if os.path.isdir(_corpus.mdir(CLAUDE, c))])
    # convention per template family and per category (gold)
    def share(cnt):
        n = cnt["wrapped"] + cnt["bare"]
        return (cnt["wrapped"] / n if n else None, n)
    per_tmpl = defaultdict(Counter); per_prefix = defaultdict(Counter); per_cat = defaultdict(Counter)
    for (t, p, c), cnt in g_grp.items():
        per_tmpl[t].update(cnt); per_prefix[p].update(cnt); per_cat[c].update(cnt)
    claude_tmpl = defaultdict(Counter); claude_cat = defaultdict(Counter)
    for (t, p, c), cnt in c_grp.items():
        claude_tmpl[t].update(cnt); claude_cat[c].update(cnt)
    res = {
        "gold_by_template": {t: {"share_wrapped": share(c)[0], "n": share(c)[1]} for t, c in per_tmpl.items()},
        "gold_by_category": {t: {"share_wrapped": share(c)[0], "n": share(c)[1], "href_kinds": dict(g_cat[t])} for t, c in per_cat.items()},
        "gold_by_prefix": {t: {"share_wrapped": share(c)[0], "n": share(c)[1]} for t, c in sorted(per_prefix.items())},
        "gold_prefixes_below_060": [p for p, c in per_prefix.items() if share(c)[0] is not None and share(c)[0] < 0.60],
        "claude_by_template": {t: dict(c) for t, c in claude_tmpl.items()},
        "claude_by_category": {t: {**dict(c), "href_kinds": dict(c_cat[t])} for t, c in claude_cat.items()},
        "claude_bare_total": sum(c["bare"] for c in c_grp.values()),
        "claude_bare_pages": len(c_pages), "claude_bare_modules": len(c_mods),
        "claude_bare_rows": c_rows,
    }
    with open(os.path.join(BASE, "_r326_buttonanchor.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    with open(os.path.join(BASE, "_r326_affected.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(c_mods)) + "\n")
    print("GOLD wrapped share by template:", {t: "%.3f (n=%d)" % (v["share_wrapped"] or 0, v["n"]) for t, v in res["gold_by_template"].items()})
    print("GOLD wrapped share by category:", {t: "%.3f (n=%d)" % (v["share_wrapped"] or 0, v["n"]) for t, v in res["gold_by_category"].items()})
    print("GOLD prefixes below 0.60:", res["gold_prefixes_below_060"],
          "| prefixes measured:", len(res["gold_by_prefix"]))
    print("GOLD href kinds:", {t: v["href_kinds"] for t, v in res["gold_by_category"].items()})
    print("CLAUDE by template:", res["claude_by_template"])
    print("CLAUDE by category:", {t: {k: v for k, v in d.items() if k != "href_kinds"} for t, d in res["claude_by_category"].items()})
    print("CLAUDE BARE total %d on %d pages / %d modules" % (res["claude_bare_total"], res["claude_bare_pages"], res["claude_bare_modules"]))


if __name__ == "__main__":
    main(sys.argv[1:])
