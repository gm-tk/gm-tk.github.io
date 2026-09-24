#!/usr/bin/env python3
"""Session 45 Round 7 — the discriminator for "the lesson's learning intentions sit in Claude's BODY while its lesson menu is empty":
every paired LESSON page whose Claude #module-menu-content is empty and whose Claude body carries a WALT lead (we are learning / in this
lesson you are|will / learning intentions / you will show your understanding) — the enclosing container of that lead in Claude's body
(alert / table / accordion / box / activity / free) and its POSITION (index of the lead among the body's top-level rows), and where the
GOLD puts the same sentence (menu / body / absent). Per module and per container. WSL, from outputs/: python3 _s45_r7_waltbody.py"""
import os, re, io, json, sys, collections, html as H
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s45_r7_emptymenu.py"), encoding="utf-8").read().split("pp = json.load")[0])
LEAD = re.compile(r"(we are learning|in this lesson,? you (?:are|will)|learning intentions?|you will show your understanding)", re.I)
def body_html(path):
    s = io.open(path, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    b = s.find('id="body"')
    return s[s.find(">", b) + 1:] if b >= 0 else s
def container_of(h, pos):
    pre = h[:pos]
    # the innermost open div class among the known wrappers
    stack = []
    for m in re.finditer(r"<(/?)(div|table|td)\b([^>]*)>", pre):
        if m.group(1):
            if stack: stack.pop()
        else:
            cls = re.search(r'class="([^"]*)"', m.group(3)); stack.append((m.group(2), cls.group(1) if cls else ""))
    for tag, cls in reversed(stack):
        if tag in ("table", "td"): return "table"
        for k in ("cv2-interactive", "accordion", "alert", "activity", "whakatauki", "quoteText"):
            if re.search(r"\b" + k + r"\b", cls): return k
    return "free"
pp = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_diff_miner.json"), encoding="utf-8"))["per_page"]
agg = collections.Counter(); per = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
for rec in pp:
    code, cpage, gpage = rec["module"], rec["page"], rec["gold"]
    if re.search(r"_0_0\.html$", cpage): continue
    cpath = os.path.join(_corpus.mdir(CL, code), cpage); gpath = os.path.join(_corpus.mdir(GOLD, code), gpage)
    cm, cb = split_regions(cpath)
    if cm: continue
    ch = body_html(cpath)
    txt = re.sub(r"<[^>]+>", " ", ch)
    m = LEAD.search(txt)
    if not m: continue
    # the lead's position in the raw html (first occurrence of the matched words)
    pos = ch.lower().find(m.group(1).lower().split()[0] + " " + m.group(1).lower().split()[1]) if len(m.group(1).split()) > 1 else ch.lower().find(m.group(1).lower())
    cont = container_of(ch, pos) if pos >= 0 else "?"
    rows_before = len(re.findall(r'<div class="row"', ch[:max(pos, 0)]))
    # the sentence: 6 words from the lead
    sent = n(txt[m.start():m.start() + 160]); key = " ".join(sent.split()[:7])
    gm, gb = split_regions(gpath)
    where = "menu" if key and key in gm else ("body" if key and key in gb else "absent")
    k = (cont, "early" if rows_before <= 2 else "late", where)
    agg[k] += 1; per[code][where] += 1
    if len(ex[k]) < 4: ex[k].append(f"{code}/{cpage}")
print("lesson pages: Claude menu empty + a WALT lead in Claude's body — (container, position, gold placement):")
for k, v in agg.most_common(): print(f"  {v:4d}  {k}  e.g. {' '.join(ex[k])}")
tot = collections.Counter()
for c, v in per.items(): tot.update(v)
print("\nby gold placement:", dict(tot), "modules", len(per))
