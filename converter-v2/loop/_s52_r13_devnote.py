#!/usr/bin/env python3
"""_s52_r13_devnote.py — session 52 Round 13: learner-visible body blocks (outside the hand-off boxes, not red notes) that read as a
note TO the developer / Creative Services ('Designer, …', 'Note to developer', 'CS:', 'Creative Services', 'please (make|create|
add|insert|use) …', 'can we / could we …'), gold vs Claude, by cue. Regex-level. WSL."""
import re, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
P = re.compile(r"<(p|li)\b([^>]*)>(.*?)</\1>", re.S)
CUES = [("designer/developer", re.compile(r"^(?:note (?:to|for) (?:the )?(?:designer|developer|dev)|(?:dear )?(?:designer|developer|dev)s?\b[,:])", re.I)),
        ("creative services / CS", re.compile(r"^(?:cs\b\s*[:,-]|creative services\b)", re.I)),
        ("please make/create/add…", re.compile(r"^please (?:make|create|add|insert|use|embed|put|place|build|design|link|include)\b", re.I)),
        ("can/could we…", re.compile(r"^(?:can|could) (?:we|you|this|these|the)\b.*\?$", re.I)),
        ("note from <name>", re.compile(r"^note from [A-Z]", re.I))]
def spans_of(s):
    out = []
    for h in re.finditer(r'<div class="cv2-interactive[^"]*"', s):
        d = 0
        for x in re.finditer(r"<(/?)div\b[^>]*>", s[h.start():]):
            d += -1 if x.group(1) else 1
            if d == 0: out.append((h.start(), h.start() + x.end())); break
    return out
for side, root in (("GOLD", R + "/01-Finalized_Modules_"), ("CLAUDE", R + "/01-Claude_Modules_")):
    st = collections.Counter(); pages = collections.defaultdict(set); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
    for f in glob.glob(root + "/*/*/*.html"):
        mod = f.split("/")[-2]
        s = open(f, encoding="utf-8", errors="replace").read(); b = s.find('id="body"'); e = s.find('class="acks'); sp = spans_of(s)
        if b < 0: continue
        for m in P.finditer(s, b):
            if e > 0 and m.start() > e: break
            if "cv2-note" in m.group(2) or any(a <= m.start() < z for a, z in sp): continue
            t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(3))).strip()
            k = next((n for n, rx in CUES if rx.search(t)), None)
            if not k: continue
            st[k] += 1; pages[k].add(f); mods[k].add(mod)
            if len(ex[k]) < 3: ex[k].append(f"{mod}: {t[:90]}")
    print(side)
    for k, n in st.most_common():
        print(f"  {n:4d} / {len(pages[k]):3d} pages / {len(mods[k]):3d} mods  {k}")
        for x in ex[k]: print("      e.g.", x)
