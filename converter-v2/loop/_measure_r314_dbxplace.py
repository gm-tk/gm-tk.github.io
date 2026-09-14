#!/usr/bin/env python3
"""ROUND 314 (loop Round 1) — WHERE DOES THE UPLOAD BUTTON LAND: inside the activity box or after it?

The class (triangulated on XMES101 2D / XTAS101 1C, KB constraint 43): the writer puts a
dropbox marker INSIDE an activity ([Activity 2D] … [microphone, camera and video dropbox
buttons] [End page]); the human keeps the "Upload to dropbox" button INSIDE that activity box
and marks the box `activity dropbox`; Claude closes the box first and ships round 308's button
in its own row after it — so round 305's postpass (which only marks a box whose OWN span holds
the button) never fires, its documented 17% recall.

This probe measures, on BOTH sides and per series prefix:
  INSIDE   — an upload/dropbox/portfolio button whose position lies inside an activity div's
             depth-balanced span;
  TRAILING — a button that sits AFTER an activity's close and BEFORE the next activity opens
             (the candidate "belongs to the box it follows");
  FREE     — any other button (no activity before it on the page, or another boundary).
For the gold it gives the CONVENTION share (inside vs trailing) — the rule ships only where the
share is >= 0.60 in the group (LOOP §2 / r182 solidify). For Claude it gives the POPULATION the
fix would move, and cross-checks each trailing case against the Writers Template: is the
dropbox marker between that activity's opener and the next boundary? (the discriminator the
engine can read). Writes outputs/_r314_dbxplace.json and outputs/_r314_affected.txt.

USAGE: python3 _measure_r314_dbxplace.py [CODE …]
"""
import os, sys, re, json, glob
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
BTN = re.compile(r'<div class="(?:button|buttonD|externalButton)[^"]*">\s*(Upload to [Dd]ropbox\.?|Go to [Dd]ropbox\.?|Go to portfolio\.?)\s*</div>')
ACT = re.compile(r'<div class="(activity(?:\s[^"]*)?)"(?:\s+number="([^"]*)")?')
DIV = re.compile(r"<(/?)div\b", re.I)
WT_DBX = re.compile(r"\[[^\]\n]*(?:drop\s?box|upload)[^\]\n]*\]", re.I)
WT_ACT = re.compile(r"\[\s*activity\s*([0-9]+[a-z]?|[a-z]?[0-9]+)?\s*[\]:]", re.I)
WT_BOUND = re.compile(r"\[\s*(end activity|end page|lesson\b|end lesson|new page|title bar|h1)", re.I)


def div_end(html, start):
    depth = 0
    for m in DIV.finditer(html, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
    return len(html)


def page_events(raw):
    acts = []
    for m in ACT.finditer(raw):
        acts.append({"cls": m.group(1), "num": m.group(2) or "", "start": m.start(), "end": div_end(raw, m.start())})
    btns = [(m.start(), m.group(1)) for m in BTN.finditer(raw)]
    rows = []
    for pos, label in btns:
        inside = [a for a in acts if a["start"] < pos < a["end"]]
        if inside:
            a = inside[-1]
            rows.append({"place": "inside", "act": a["num"], "cls": a["cls"], "label": label})
            continue
        prev = [a for a in acts if a["end"] <= pos]
        nxt = [a for a in acts if a["start"] > pos]
        if prev:
            a = prev[-1]
            rows.append({"place": "trailing", "act": a["num"], "cls": a["cls"], "label": label,
                         "gap_chars": pos - a["end"]})
        else:
            rows.append({"place": "free", "act": "", "cls": "", "label": label})
    return rows


def wt_text(code):
    d = _corpus.mdir(HUMAN, code)
    out = ""
    for pf in sorted(glob.glob(os.path.join(d, "*_parsed.txt"))):
        out += open(pf, encoding="utf-8", errors="replace").read() + "\n"
    return out


def wt_dropbox_inside_activity(wt, num):
    """Is a dropbox/upload marker between [Activity NUM]'s opener and the next boundary?"""
    if not num:
        return None
    lines = wt.splitlines()
    for i, ln in enumerate(lines):
        m = WT_ACT.search(ln)
        if m and (m.group(1) or "").lower() == num.lower():
            for j in range(i + 1, min(i + 80, len(lines))):
                l2 = lines[j]
                if WT_ACT.search(l2) or WT_BOUND.search(l2):
                    return False
                if WT_DBX.search(l2):
                    return True
            return False
    return None


def main():
    codes = [a for a in sys.argv[1:] if not a.startswith("-")] or _corpus.mods(HUMAN)
    res = {"gold": defaultdict(Counter), "claude": defaultdict(Counter)}
    affected = []
    claude_trailing = []
    gold_inside_marked = Counter()
    for code in codes:
        pre = re.match(r"[A-Z]+", code).group(0)
        fam = "BLL" if (pre == "BLL") else "nonBLL"
        for side, root in (("gold", HUMAN), ("claude", CLAUDE)):
            d = _corpus.mdir(root, code)
            if not os.path.isdir(d):
                continue
            wt = None
            for f in sorted(os.listdir(d)):
                if not f.lower().endswith(".html") or SKIP_PAGE.search(f):
                    continue
                raw = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
                for r in page_events(raw):
                    res[side][fam][r["place"]] += 1
                    res[side][pre][r["place"]] += 1
                    if side == "gold" and r["place"] == "inside":
                        gold_inside_marked[(fam, "dropbox" in r["cls"].split())] += 1
                    if side == "claude" and r["place"] == "trailing":
                        if wt is None:
                            wt = wt_text(code)
                        inwt = wt_dropbox_inside_activity(wt, r["act"])
                        claude_trailing.append({"module": code, "page": f, "activity": r["act"], "cls": r["cls"],
                                                "label": r["label"], "gap_chars": r["gap_chars"], "wt_marker_inside_activity": inwt})
                        if code not in affected:
                            affected.append(code)
    out = {"gold": {k: dict(v) for k, v in res["gold"].items()}, "claude": {k: dict(v) for k, v in res["claude"].items()},
           "gold_inside_marked": {f"{k[0]}:{'marked' if k[1] else 'plain'}": v for k, v in gold_inside_marked.items()},
           "claude_trailing": claude_trailing, "affected_modules": affected}
    json.dump(out, open(os.path.join(BASE, "_r314_dbxplace.json"), "w", encoding="utf-8"), indent=1)
    open(os.path.join(BASE, "_r314_affected.txt"), "w").write("\n".join(affected) + "\n")

    def line(side, key):
        c = res[side].get(key, Counter())
        tot = sum(c.values()) or 1
        return f"{side:6} {key:8} inside {c['inside']:5} ({c['inside']/tot:.0%})  trailing {c['trailing']:5} ({c['trailing']/tot:.0%})  free {c['free']:4}"
    print("UPLOAD-BUTTON PLACEMENT (round 314 probe)")
    for key in ("nonBLL", "BLL"):
        print(" ", line("gold", key)); print(" ", line("claude", key))
    print("  gold inside boxes, modifier present:", dict(out["gold_inside_marked"]))
    tr = claude_trailing
    inwt = Counter(str(t["wt_marker_inside_activity"]) for t in tr)
    print(f"  CLAUDE trailing buttons {len(tr)} across {len(affected)} modules; WT marker inside the activity span: {dict(inwt)}")
    nb = [t for t in tr if not t["module"].startswith("BLL")]
    print(f"  of which non-BLL: {len(nb)} buttons / {len({t['module'] for t in nb})} modules; "
          f"WT-inside {sum(1 for t in nb if t['wt_marker_inside_activity'])}")
    byp = Counter(re.match(r"[A-Z]+", t["module"]).group(0) for t in nb)
    print("  non-BLL trailing by prefix:", dict(byp.most_common(15)))
    print("  gold inside/trailing by prefix (non-BLL prefixes with >= 5 buttons):")
    for pre, c in sorted(res["gold"].items(), key=lambda kv: -sum(kv[1].values())):
        if pre in ("BLL", "nonBLL") or sum(c.values()) < 5:
            continue
        tot = sum(c.values())
        cc = res["claude"].get(pre, Counter())
        print(f"    {pre:7} gold inside {c['inside']:4} trailing {c['trailing']:4} ({c['inside']/tot:.0%} inside) | claude inside {cc['inside']:4} trailing {cc['trailing']:4}")
    print(f"  wrote _r314_dbxplace.json, _r314_affected.txt ({len(affected)} modules)")


if __name__ == "__main__":
    main()
