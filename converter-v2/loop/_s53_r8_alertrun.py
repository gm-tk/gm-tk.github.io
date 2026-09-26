#!/usr/bin/env python3
"""_s53_r8_alertrun.py — session 53 Round 8: THE ALERT WHOSE TITLE IS A HEADING — how far does the gold's box run? Two writer forms
(outputs/_s52_items): (A) an EMPTY `[Alert]` / `[Important]` then a `[Hn]` (or `[Body]`) item; (B) a `[Hn]` item whose own span co-tags
alert / important (`[Alert] [H3] Key questions`, not rhs / right). For each site: the heading, then the FOLLOWING items up to the next
heading / callout / activity / widget / page boundary — each located on the gold paired page: inside an alert chain or not; and on
Claude's page. Reports per form: the heading gold-in-alert share, and per following position (1st, 2nd, …) and kind (black, bullet,
body tag) the gold-in-alert share — the stop rule the gold follows. WSL, from reference/tests/:
    python3 ../../outputs/_s53_r8_alertrun.py > ../../outputs/_s53_r8_alertrun.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
sys.path.append(os.path.abspath(os.path.join("..", "..", "outputs")))
import _corpus
import _discrepancy_audit as DA
from anchor_compare import CLAUDE, HUMAN
import _placement_census as PC

O = os.path.abspath(os.path.join("..", "..", "outputs"))
famof = lambda m: re.sub(r"\d.*$", "", m)
CALL = ("alert", "important")
STOP_DIR = {"CONTAINER_OPEN", "CONTAINER_CLOSE", "INTERACTIVE", "PAGE_BOUNDARY", "SECTION_MARKER"}

def items_of(mod):
    p = os.path.join(O, "_s52_items", mod + ".tsv")
    if not os.path.exists(p): return []
    out = []
    for line in open(p, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 9: continue
        pg, k, typ, tag, dirv, bold, ttext, payload, txt = f[:9]
        body = payload if typ == "tag" else txt
        raw = re.sub(r"<[^>]+>", "", body)
        out.append({"pg": int(pg), "type": typ, "tag": tag, "dir": dirv, "ttext": ttext, "raw": raw,
                    "bullet": bool(re.match(r"\s*(?:\*+\s*)?[•]", raw)), "t": PC.norm(re.sub(r"\*+", "", raw))})
    return out

def is_head(it): return it["type"] == "tag" and re.fullmatch(r"h[2-6]", it["tag"] or "") is not None
def kind(it):
    if it["type"] == "black": return "bullet" if it["bullet"] else "black"
    if it["type"] == "tag" and it["tag"] in ("body", "body text"): return "body"
    return None

head_stats = collections.defaultdict(collections.Counter); pos = collections.defaultdict(collections.Counter)
knd = collections.defaultdict(collections.Counter); sites = collections.Counter(); mods = collections.defaultdict(set); pages = collections.defaultdict(set)
ex = collections.defaultdict(list); runlen = collections.defaultdict(collections.Counter)
for mod in sorted(m for m in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, m)) and os.path.isdir(_corpus.mdir(HUMAN, m))):
    items = items_of(mod)
    if not items: continue
    cand = []
    for x, it in enumerate(items):
        if it["type"] == "tag" and it["tag"] in CALL and it["dir"] == "CONTAINER_OPEN" and not it["t"] \
                and not re.search(r"\b(rhs|rhc|right|side|close)\b", it["ttext"], re.I):
            y = x + 1
            while y < len(items) and items[y]["type"] == "black" and not items[y]["t"]: y += 1
            if y < len(items) and items[y]["pg"] == it["pg"] and is_head(items[y]): cand.append(("A", y))
        elif is_head(it) and re.search(r"\b(alert|important)\b", it["ttext"], re.I) and not re.search(r"\b(rhs|rhc|right|side)\b", it["ttext"], re.I):
            cand.append(("B", x))
    if not cand: continue
    prs = DA.pairs(mod)
    if not prs: continue
    gix, cix = {}, {}; pgof = {}
    for n, cp, hp in prs:
        for tag, t, raw, reg in PC.parse(hp):
            if len(t) >= 8: gix.setdefault(t[:40], reg); pgof.setdefault(t[:40], os.path.basename(cp))
        for tag, t, raw, reg in PC.parse(cp):
            if len(t) >= 8: cix.setdefault(t[:40], reg)
    for form, h in cand:
        hk = items[h]["t"][:40]
        if len(hk) < 8 or hk not in gix: continue
        g_al = "alert" in gix[hk]; c_al = "alert" in cix.get(hk, "")
        head_stats[form][(g_al, c_al)] += 1; sites[form] += 1; mods[form].add(mod); pages[form].add(pgof.get(hk))
        if len(ex[form]) < 6: ex[form].append(f"{mod} {items[h]['ttext'][:26]!r} {hk[:34]!r} gold {'ALERT' if g_al else 'free'} claude {'ALERT' if c_al else 'free'}")
        if not g_al: continue
        n = 0; run = 0; broke = False
        for y in range(h + 1, len(items)):
            it = items[y]
            if it["pg"] != items[h]["pg"]: break
            if it["type"] == "black" and not it["t"]: continue
            k = kind(it)
            if k is None: break                  # a heading / callout / activity / widget / table / other tag ends the walk
            if len(it["t"]) < 8 or it["t"][:40] not in gix: continue
            n += 1
            inside = "alert" in gix[it["t"][:40]]
            pos[form][(min(n, 6), inside)] += 1; knd[form][(k, inside)] += 1
            if inside and not broke: run += 1
            else: broke = True
        runlen[form][min(run, 8)] += 1
for form in ("A", "B"):
    print(f"## FORM {form}: {sites[form]} sites / {len(mods[form])} modules / {len(pages[form])} pages")
    print("   heading (gold in alert, claude in alert):", dict(head_stats[form]))
    for e in ex[form]: print("     e.g.", e)
    print("   following item by position (gold inside the alert?):", ", ".join(f"#{p} in {pos[form][(p, True)]} / out {pos[form][(p, False)]}" for p in range(1, 7)))
    print("   by kind:", ", ".join(f"{k} in {knd[form][(k, True)]} / out {knd[form][(k, False)]}" for k in ("black", "bullet", "body")))
    print("   run length inside the gold alert after the heading:", sorted(runlen[form].items()))
    print()
