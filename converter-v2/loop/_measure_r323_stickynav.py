#!/usr/bin/env python3
"""ROUND 323 measure — the `stickyNav.js` <head> include (KB 14A/14B/14D: Languages P1-4 every page,
CED P5, HPE Fundamentals + help page; the gold carries it far wider). For every gold page: is there a
LIVE <script … stickyNav.js … class="stickyNav"> in <head> (a commented-out one counts as OFF), and
where does it sit (the element before it)? Grouped by template family / subject family / series and
per module; the same for the Claude corpus. Writes outputs/_r323_stickynav.json and prints the shares."""
import os, re, json, glob, collections, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
LIVE = re.compile(r'<script[^>]*stickyNav\.js[^>]*>\s*</script>', re.I)
COMMENTED = re.compile(r'<!--\s*<script[^>]*stickyNav\.js', re.I)
HEAD = re.compile(r'<head[^>]*>(.*?)</head>', re.I | re.S)

def series_of(code):
    m = re.match(r'([A-Z]+)', code); return m.group(1) if m else code
def subject_of(code):
    # first 2-3 letters family: BLL, ENG, MX, SC, HPE(HES/PHE/PES/HPRE), CED, TE, AR, SS, ANZH, EX, X(learningSupport)…
    for p in ("HPRE", "ANZH", "BLLR", "BLL", "CED", "ENG", "ENF", "EXP", "EXB", "MX", "SC", "SS", "TE", "AR", "HES", "PHE", "PES", "HIS", "OS", "PNR", "TRR", "XGF", "XLP", "XMES", "XDLS", "XTAS", "AGH", "CH", "JPN", "HP"):
        if code.startswith(p): return p
    return series_of(code)[:2]

def scan(root):
    rows = []
    for tmpl in sorted(os.listdir(root)):
        td = os.path.join(root, tmpl)
        if not os.path.isdir(td): continue
        for code in sorted(os.listdir(td)):
            md = os.path.join(td, code)
            if not os.path.isdir(md): continue
            for f in sorted(glob.glob(os.path.join(md, "*.html"))):
                try: s = open(f, encoding="utf-8", errors="replace").read()
                except Exception: continue
                h = HEAD.search(s); head = h.group(1) if h else s[:6000]
                live = LIVE.search(head); comm = COMMENTED.search(head)
                prev = None
                if live:
                    before = head[:live.start()].rstrip()
                    m = re.findall(r'<(link|script|meta|title)\b[^>]*>', before, re.I)
                    tags = re.findall(r'<(?:link|script)\b[^>]*>', before, re.I)
                    prev = (tags[-1][:90] if tags else None)
                rows.append({"tmpl": tmpl, "code": code, "series": series_of(code), "subject": subject_of(code),
                             "page": os.path.basename(f), "live": bool(live), "commented": bool(comm and not live),
                             "form": (live.group(0)[:120] if live else None), "prev": prev})
    return rows

def shares(rows, key):
    g = collections.defaultdict(lambda: [0, 0, 0])
    for r in rows:
        k = r[key]; g[k][1] += 1
        if r["live"]: g[k][0] += 1
        if r["commented"]: g[k][2] += 1
    return {k: {"live": v[0], "pages": v[1], "commented": v[2], "share": round(v[0] / v[1], 3)} for k, v in g.items()}

gold = scan(GOLD); claude = scan(CLAUDE)
out = {"gold_pages": len(gold), "gold_live": sum(r["live"] for r in gold), "gold_commented": sum(r["commented"] for r in gold),
       "claude_pages": len(claude), "claude_live": sum(r["live"] for r in claude),
       "gold_by_template": shares(gold, "tmpl"), "gold_by_subject": shares(gold, "subject"), "gold_by_series": shares(gold, "series"),
       "gold_by_module": shares(gold, "code"),
       "forms": collections.Counter(r["form"] for r in gold if r["live"]).most_common(6),
       "prev": collections.Counter(r["prev"] for r in gold if r["live"]).most_common(8)}
json.dump(out, open(os.path.join(ROOT, "CONVERTER_V2", "outputs", "_r323_stickynav.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"gold: {out['gold_live']}/{out['gold_pages']} pages LIVE ({out['gold_live']/out['gold_pages']:.1%}), commented-out {out['gold_commented']}; claude: {out['claude_live']}/{out['claude_pages']}")
print("by template:"); [print(f"  {k:<14} {v['live']:>5}/{v['pages']:<5} {v['share']:.2f}  (commented {v['commented']})") for k, v in sorted(out["gold_by_template"].items())]
print("by subject family (share, pages):"); [print(f"  {k:<6} {v['share']:.2f} {v['live']:>5}/{v['pages']:<5} commented {v['commented']}") for k, v in sorted(out["gold_by_subject"].items(), key=lambda kv: -kv[1]['pages'])]
mods = out["gold_by_module"]
full = sum(1 for v in mods.values() if v["share"] >= 0.99); none = sum(1 for v in mods.values() if v["live"] == 0); mixed = len(mods) - full - none
print(f"modules: {len(mods)} — all pages live {full}, none {none}, MIXED {mixed}")
print("mixed modules:", " ".join(f"{k}({v['live']}/{v['pages']})" for k, v in sorted(mods.items()) if 0 < v['live'] < v['pages'])[:1500])
print("forms:", out["forms"][:3]); print("element before it:", out["prev"][:5])
