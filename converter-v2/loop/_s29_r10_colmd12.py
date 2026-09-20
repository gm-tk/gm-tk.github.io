#!/usr/bin/env python3
"""_s29_r10_colmd12.py — the gold's `div.col-12.col-md-12` column (1734 in the gold vs 133 in Claude — the label census's biggest MISSING
container): its CONTEXT — the parent container (activity / alert / supervisor panel / body row …), the row's other columns, the column's
first child — per template+subject; and Claude's corresponding form on the paired page at the same content (the first child's text).
Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s29_r10_colmd12.py
"""
import os, re, sys, collections, json
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]
TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)\b([^>]*)>")
def cls(attrs):
    m = re.search(r'class="([^"]*)"', attrs); return sorted(m.group(1).split()) if m else []
def walk(html):
    """yield (path_labels, first_child_label, first_text) for every div whose class set == {col-12, col-md-12}"""
    stack = []; out = []; pending = []   # pending: frames of target cols awaiting their first child
    for m in TAG.finditer(html):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in ("br", "img", "hr", "input", "meta", "link", "source", "wbr") or attrs.rstrip().endswith("/"):
            if not closing:
                for fr in pending: fr["child"] = tag + ("." + ".".join(cls(attrs)) if cls(attrs) else "")
                pending = []
            continue
        if closing:
            if stack and stack[-1][0] == tag: stack.pop()
            continue
        c = cls(attrs); lab = tag + ("." + ".".join(c) if c else "")
        for fr in pending:
            fr["child"] = lab
            fr["text"] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html[m.end():m.end() + 160])).strip()[:50]
        pending = []
        if tag == "div" and set(c) == {"col-12", "col-md-12"}:
            fr = {"path": [s[1] for s in stack[-4:]], "child": "(empty)", "text": ""}
            out.append(fr); pending.append(fr)
        stack.append((tag, lab))
    return out
bygroup = collections.defaultdict(collections.Counter); byctx = collections.Counter(); bychild = collections.Counter(); pages = collections.defaultdict(set)
examples = collections.defaultdict(list); claude_at = collections.Counter()
for code in _corpus.gate_mods(CLAUDE):
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); grp = (mm.get("template_type", ""), mm.get("subject", ""))
    for t in prs:
        cp, hp = t[1], t[2]
        try: c = open(cp, encoding="utf-8").read(); g = open(hp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        found = walk(g)
        if not found: continue
        for fr in found:
            path = fr["path"]
            ctx = "other"
            joined = " ".join(path)
            for key in ("super-content", "supervisor", "activity", "alert", "whakatauki", "accContent", "clickDropContent", "fundamentalsPanel", "inquiryPanel", "tab-pane", "moduleMenu", "menu"):
                if key in joined: ctx = key; break
            byctx[ctx] += 1; bychild[fr["child"]] += 1; bygroup[grp][ctx] += 1; pages[ctx].add(hp)
            if len(examples[ctx]) < 3: examples[ctx].append((code, os.path.basename(hp), " › ".join(path[-3:]), fr["child"], fr["text"]))
            # Claude's column at the same content
            txt = fr["text"]
            if txt and len(txt) >= 12:
                i = c.find(txt[:30])
                if i >= 0:
                    before = c[max(0, i - 400):i]
                    mm2 = re.findall(r'<div class="([^"]*col[^"]*)"', before)
                    claude_at[(ctx, mm2[-1] if mm2 else "(no col)")] += 1
                else: claude_at[(ctx, "(text absent)")] += 1
print("gold col-12 col-md-12 columns by CONTEXT (ancestor):")
for k, v in byctx.most_common(): print(f"   {k:18s} {v:5d}  pages {len(pages[k])}")
print("\nby FIRST CHILD:")
for k, v in bychild.most_common(12): print(f"   {k:40s} {v}")
print("\nby (template, subject) x context:")
for grp, cnt in sorted(bygroup.items(), key=lambda x: -sum(x[1].values()))[:25]:
    print(f"   {str(grp)[:48]:48s} n={sum(cnt.values()):4d}  " + "  ".join(f"{k}={v}" for k, v in cnt.most_common(4)))
print("\nClaude's column at the same content (context, Claude's nearest preceding col class):")
for k, v in claude_at.most_common(25): print(f"   {k[0]:18s} {v:5d}  {k[1]}")
print("\nexamples:")
for ctx, ex in examples.items():
    for e in ex: print("  ", ctx, e)
