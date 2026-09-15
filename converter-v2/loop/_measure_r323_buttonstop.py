#!/usr/bin/env python3
"""ROUND 323 measure — KB row 55's text defect: button labels ending in a full stop (the KB's canonical
labels 'Go to dropbox' / 'Go to portfolio' / 'Upload to Dropbox' / 'Go to website' / 'Go to quiz' carry
no terminal punctuation; the r0b audit counted 420 Claude buttons vs 3 gold). For every Claude and gold
page: each button div (button / externalButton / supervisor …) with its label; the share whose label ends
in a full stop (and other terminal punctuation), per template family, subject family and button class;
the label list. Writes outputs/_r323_buttonstop.json."""
import os, re, json, glob, collections
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
BTN = re.compile(r'<div class="((?:button|externalButton|activityButton)[^"]*)"[^>]*>(.*?)</div>', re.S | re.I)
TAG = re.compile(r'<[^>]+>')
def subject_of(code):
    for p in ("HPRE", "ANZH", "BLLR", "BLL", "CED", "ENGC", "ENGI", "ENGJ", "ENGR", "ENGS", "ENG", "ENF", "EXP", "EXB", "EXI", "MX", "SCCH", "SCPH", "SC", "SS", "TE", "AR", "HES", "PHE", "PES", "HIS", "OS", "PNR", "TRR", "XGF", "XLP", "XMES", "XDLS", "XTAS", "XW", "XF", "AGH", "CH", "HP", "TW"):
        if code.startswith(p): return p
    return re.match(r'[A-Z]+', code).group(0)
def scan(root):
    rows = []
    for tmpl in sorted(os.listdir(root)):
        td = os.path.join(root, tmpl)
        if not os.path.isdir(td): continue
        for code in sorted(os.listdir(td)):
            for f in sorted(glob.glob(os.path.join(td, code, "*.html"))):
                s = open(f, encoding="utf-8", errors="replace").read()
                for m in BTN.finditer(s):
                    cls = m.group(1).split()[0]
                    if "activityButton" in m.group(1): continue   # widget chrome (Reset / Check answers) — the builder's own
                    label = TAG.sub("", m.group(2)).replace("&nbsp;", " ").strip()
                    if not label or len(label) > 120: continue
                    end = label[-1]
                    rows.append({"tmpl": tmpl, "code": code, "subject": subject_of(code), "page": os.path.basename(f), "cls": cls,
                                 "label": label, "stop": end == ".", "punct": end if end in ".:;!?," else ""})
    return rows
def share(rows, key):
    g = collections.defaultdict(lambda: [0, 0])
    for r in rows: g[r[key]][1] += 1; g[r[key]][0] += r["stop"]
    return {k: {"stop": v[0], "buttons": v[1], "share": round(v[0] / v[1], 3)} for k, v in g.items()}
gold = scan(GOLD); claude = scan(CLAUDE)
cs = [r for r in claude if r["stop"]]
out = {"gold_buttons": len(gold), "gold_stop": sum(r["stop"] for r in gold), "gold_stop_labels": collections.Counter(r["label"] for r in gold if r["stop"]).most_common(10),
       "gold_other_punct": collections.Counter(r["punct"] for r in gold if r["punct"] and not r["stop"]).most_common(),
       "claude_buttons": len(claude), "claude_stop": len(cs), "claude_stop_pages": len({(r["code"], r["page"]) for r in cs}), "claude_stop_modules": len({r["code"] for r in cs}),
       "claude_other_punct": collections.Counter(r["punct"] for r in claude if r["punct"] and not r["stop"]).most_common(),
       "claude_by_template": share(claude, "tmpl"), "claude_by_subject": share(claude, "subject"), "claude_by_class": share(claude, "cls"),
       "claude_stop_labels": collections.Counter(r["label"] for r in cs).most_common(40),
       "claude_stop_modules_list": sorted({r["code"] for r in cs})}
json.dump(out, open(os.path.join(ROOT, "CONVERTER_V2", "outputs", "_r323_buttonstop.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"gold: {out['gold_stop']}/{out['gold_buttons']} buttons end in a full stop; labels {out['gold_stop_labels']}; other terminal punctuation {out['gold_other_punct']}")
print(f"claude: {out['claude_stop']}/{out['claude_buttons']} buttons end in a full stop on {out['claude_stop_pages']} pages / {out['claude_stop_modules']} modules; other terminal punctuation {out['claude_other_punct']}")
print("by template:", {k: f"{v['stop']}/{v['buttons']}" for k, v in sorted(out["claude_by_template"].items())})
print("by class:", {k: f"{v['stop']}/{v['buttons']}" for k, v in sorted(out["claude_by_class"].items())})
print("by subject (stop/buttons):", " ".join(f"{k}:{v['stop']}/{v['buttons']}" for k, v in sorted(out["claude_by_subject"].items(), key=lambda kv: -kv[1]['stop']) if v['stop']))
print("top labels:", out["claude_stop_labels"][:25])
