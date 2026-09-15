#!/usr/bin/env python3
"""_measure_r339_actinteractive.py — ROUND 339 PICK measurement (session 7 Round 2).

KB 01F: `activity` + ID (interactive) → `<div class="activity interactive" number="ID">`; 03A: every interactive sits inside an
activity wrapper, "typically class=activity interactive". Claude marks `interactive` at emit time (r50 forceInt — the activity-owner
bundle's own widget type) and in the r58 post-pass (a cv2-interactive placeholder declaring an interactive-task type). The r336
substitution ranking still shows `div.activity.interactive[number=1A] ⇐ div.activity[number=1A]` on 26 Standard modules.

This probe pairs every gold activity box with Claude's box of the SAME number on the paired page and tallies the `interactive`
token: gold-yes/Claude-no (the gap), gold-no/Claude-yes (the over-mark), agree. For each gap box it records what Claude's box
holds — a built widget (by class), a cv2-interactive hand-off (and its declared type), a video, an image, plain text — so the
discriminator can be read off. Per template family and subject.

Usage (from CONVERTER_V2/outputs, WSL): python3 _measure_r339_actinteractive.py → _r339_actinteractive.json + summary
"""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS); sys.path.insert(0, HERE)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
ROOT = os.path.join(HERE, "..", "..")
META = json.load(open(os.path.join(ROOT, "pageforge-site", "converter-v2", "data", "Module_Structure_Index.json"), encoding="utf-8")).get("module_meta", {})

ACT_RE = re.compile(r'<div class="([^"]*\bactivity\b[^"]*)"([^>]*)>', re.I)
NUM_RE = re.compile(r'number="([^"]*)"')
WIDGET_CLASSES = ["dragAndDrop", "ddContainer", "clickDrop", "dropQuiz", "mcq", "sCQuestion", "flipCard", "flip-card", "speechBubble", "bubble-", "carousel", "rotateBanner", "nav-tabs", "accordion", "hintSlider", "hintDrop", "TKmodal", "memoryGame", "typing", "imageLabel", "shapeHover", "glossary", "infoTrigger", "videoSection", "audioPlayer", "img-fluid", "table"]

def boxes(html):
    """[(number, classes, inner_html)] for every activity div; inner = a depth-balanced slice (approximate)."""
    out = []
    for m in ACT_RE.finditer(html):
        cls = m.group(1).split(); num = NUM_RE.search(m.group(0)); num = num.group(1).strip() if num else ""
        # depth-balanced inner slice
        i = m.end(); depth = 1; j = i
        tag = re.compile(r'<(/?)div\b[^>]*>', re.I)
        for t in tag.finditer(html, i):
            depth += -1 if t.group(1) else 1
            if depth == 0: j = t.start(); break
        out.append((num, cls, html[i:j]))
    return out

def content_kind(inner):
    kinds = []
    hand = re.search(r'cv2-interactive[^>]*>[\s\S]{0,400}?INTERACTIVE \(un-built\) #\d+: ([A-Za-z]+)', inner)
    if hand: kinds.append("handoff:" + hand.group(1))
    elif "cv2-interactive" in inner: kinds.append("handoff:?")
    for w in WIDGET_CLASSES:
        if re.search(r'class="[^"]*' + re.escape(w), inner): kinds.append("widget:" + w); break
    if not kinds: kinds.append("plain")
    return "+".join(kinds)

def main():
    rows = []
    for code in sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d))):
        meta = META.get(code, {}); tmpl = meta.get("template_type", os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code))))
        for n, cp, hp in pairs(code):
            if re.search(r'acks|acknowledge|glossary', os.path.basename(hp) + os.path.basename(cp), re.I): continue
            try:
                ch = open(cp, encoding="utf-8", errors="replace").read(); hh = open(hp, encoding="utf-8", errors="replace").read()
            except Exception: continue
            gb = {b[0]: b for b in boxes(hh) if b[0]}; cb = {b[0]: b for b in boxes(ch) if b[0]}
            for num, (gn, gcls, ginner) in gb.items():
                if num not in cb: continue
                cn, ccls, cinner = cb[num]
                gi = "interactive" in gcls; ci = "interactive" in ccls
                rows.append({"code": code, "template": tmpl, "subject": meta.get("subject", "?"), "page": os.path.basename(cp), "number": num,
                             "gold_interactive": gi, "claude_interactive": ci, "gold_cls": " ".join(gcls), "claude_cls": " ".join(ccls),
                             "claude_content": content_kind(cinner), "gold_content": content_kind(ginner)})
    json.dump({"rows": rows}, open(os.path.join(HERE, "_r339_actinteractive.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    def cell(rs):
        c = collections.Counter((r["gold_interactive"], r["claude_interactive"]) for r in rs)
        return f"agree-yes {c[(True,True)]:4d} · agree-no {c[(False,False)]:4d} · GAP gold-yes/claude-no {c[(True,False)]:4d} · OVER gold-no/claude-yes {c[(False,True)]:4d}"
    print(f"paired activity boxes (same number on the paired page): {len(rows)}")
    print("ALL:", cell(rows))
    for t in ("Standard", "Inquiry", "Fundamentals", "Bilingual"):
        rs = [r for r in rows if r["template"] == t]
        if rs: print(f"  {t:13s}", cell(rs))
    gap = [r for r in rows if r["gold_interactive"] and not r["claude_interactive"]]
    over = [r for r in rows if not r["gold_interactive"] and r["claude_interactive"]]
    print(f"\nGAP boxes {len(gap)} on {len({r['code']+'/'+r['page'] for r in gap})} pages / {len({r['code'] for r in gap})} modules — by what Claude's box holds:")
    for k, n in collections.Counter(r["claude_content"] for r in gap).most_common(25): print(f"  {n:4d}  {k}")
    print(f"\n  … and what the GOLD box holds for the same GAP boxes:")
    for k, n in collections.Counter(r["gold_content"] for r in gap).most_common(12): print(f"  {n:4d}  {k}")
    print(f"\nOVER boxes {len(over)} on {len({r['code']+'/'+r['page'] for r in over})} pages — by what Claude's box holds:")
    for k, n in collections.Counter(r["claude_content"] for r in over).most_common(12): print(f"  {n:4d}  {k}")
    # precision of each Claude-content signature for 'gold says interactive' among boxes Claude did NOT mark
    print("\nPRECISION per Claude-content signature among boxes Claude ships PLAIN (gold interactive share):")
    unmarked = [r for r in rows if not r["claude_interactive"]]
    byk = collections.defaultdict(list)
    for r in unmarked: byk[r["claude_content"]].append(r)
    for k, rs in sorted(byk.items(), key=lambda x: -len(x[1]))[:20]:
        g = sum(1 for r in rs if r["gold_interactive"]); pages = len({r['code']+'/'+r['page'] for r in rs if r["gold_interactive"]})
        print(f"  {k:36s} n={len(rs):4d}  gold-interactive {g:4d} ({g/len(rs):.2f})  gap pages {pages}")
    print("\nGAP by subject (≥ 5):")
    for k, n in collections.Counter(r["subject"] for r in gap).most_common(15):
        if n >= 5: print(f"  {n:4d}  {k}")

if __name__ == "__main__":
    main()
