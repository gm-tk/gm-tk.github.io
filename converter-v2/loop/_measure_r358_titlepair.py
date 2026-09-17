#!/usr/bin/env python3
"""ROUND 358 PICK probe (loop session 19, Round 2 — the diff miner's TITLE class, DIFF_QUEUE F1 / #4):
THE GOLD'S SECOND TITLE `<h1><span>` — where does it come from, and can a rule derive it?

For every paired page of the skeleton gate's population: the header title h1 texts on both sides (the #module-code h1
excluded), the WT title source line for that page (the overview's [TITLE BAR] line, a lesson's [LESSON n] / first [H1] / [H2]
line, found by the round-110 phrase test on the gold's FIRST title), and, when the gold has MORE h1s than Claude:
  * SOURCE of the extra gold h1: 'wt-separated' (the extra text sits in the WT title line beside the first title, separated
    by one of |, ' - ', ' – ', ' — ', '/', ':' or a line break), 'wt-elsewhere' (in the WT but not on that line),
    'glued-in-claude' (Claude's single h1 contains the gold's extra text), 'placeholder' (the human's own 'TE REO required'
    / red-styled h1), 'not-in-wt' (the human's own — class C);
  * the separator the WT used; the template / subject / page type; whether Claude's h1 count is 0.
Aggregates per (template, page type) and per subject: the gold's ≥2-h1 share, the derivable share, the separator census.
Run from anywhere (WSL): python3 _measure_r358_titlepair.py -> _r358_titlepair.{json,log} next to itself.
"""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
for p in (HERE, TESTS):
    if p in sys.path:
        sys.path.remove(p)
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import wt_blob, has_source, unorm, load_meta

SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
SEPS = [("|", r"\|"), (" – ", r"\s–\s"), (" — ", r"\s—\s"), (" - ", r"\s-\s"), ("/", r"\s/\s"), (":", r":\s"), ("newline", r"\n")]
meta = load_meta()


def header_h1s(html):
    h = html.split('<div id="header"', 1)[-1].split('<div id="body"', 1)[0]
    h = re.sub(r"<!--[\s\S]*?-->", "", h)
    h = re.sub(r'<div id="module-code">[\s\S]*?</div>', "", h)
    out = []
    for m in re.finditer(r"<h1([^>]*)>([\s\S]*?)</h1>", h):
        attrs, inner = m.group(1), m.group(2)
        t = re.sub(r"<[^>]+>", " ", inner)
        t = re.sub(r"\s+", " ", t).strip()
        out.append({"text": t, "red": ("color: red" in attrs or "color:red" in attrs)})
    return out


_WT = {}


def wt_lines(code):
    if code not in _WT:
        d = _corpus.mdir(HUMAN, code); lines = []
        if os.path.isdir(d):
            for f in sorted(x for x in os.listdir(d) if x.endswith("_parsed.txt")):
                for ln in open(os.path.join(d, f), encoding="utf-8", errors="replace"):
                    s = ln.rstrip("\n")
                    if s.strip():
                        lines.append(s)
        _WT[code] = lines
    return _WT[code]


def find_title_line(code, first_title):
    """The WT line carrying the gold's first title (verbatim fold, else the 6-word head / 3-word window)."""
    n = unorm(first_title); w = n.split()
    if not n:
        return None
    needles = [n] + ([" ".join(w[:6])] if len(w) >= 6 else []) + [" ".join(w[i:i + 3]) for i in range(len(w) - 2) if max(len(x) for x in w[i:i + 3]) >= 6]
    for raw in wt_lines(code):
        f = " " + unorm(raw) + " "
        for nd in needles:
            if (" " + nd + " ") in f or (len(w) > 2 and nd in f):
                return raw
    return None


rows = []
codes = sorted(c for c in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, c)))
for code in codes:
    gdir = _corpus.mdir(HUMAN, code); tmpl = os.path.basename(os.path.dirname(gdir))
    subject = (meta.get(code) or {}).get("subject") or "None"
    wt = wt_blob(code); blob = wt[0] if wt else ""
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or re.search(r"acks|acknowledge|glossary", os.path.basename(cp), re.I):
            continue
        ptype = "overview" if n == 0 else "lesson"
        g = header_h1s(open(hp, encoding="utf-8", errors="replace").read())
        c = header_h1s(open(cp, encoding="utf-8", errors="replace").read())
        rec = {"module": code, "page": os.path.basename(cp), "gold_page": os.path.basename(hp), "template": tmpl, "subject": subject,
               "ptype": ptype, "gold_n": len(g), "claude_n": len(c), "gold": [x["text"] for x in g], "claude": [x["text"] for x in c],
               "extra": [], "source": None, "sep": None, "wt_line": None}
        if len(g) > len(c):
            first = g[0]["text"]
            line = find_title_line(code, first) if first else None
            rec["wt_line"] = (line or "")[:200]
            cl_join = " " + unorm(" ".join(x["text"] for x in c)) + " "
            for x in g[1:]:
                t = x["text"]; nt = unorm(t)
                if not nt:
                    src = "empty"
                elif x["red"] or re.search(r"te reo (required|needed|title)|insert|placeholder", nt):
                    src = "placeholder"
                elif nt in cl_join or (len(nt.split()) >= 3 and has_source(nt, cl_join)):
                    src = "glued-in-claude"
                elif line and (nt in unorm(line) or (len(nt.split()) >= 3 and has_source(nt, " " + unorm(line) + " "))):
                    src = "wt-separated"
                    for name, rx in SEPS:
                        if re.search(rx, line):
                            rec["sep"] = name; break
                elif blob and (nt in blob or (len(nt.split()) >= 3 and has_source(nt, blob))):
                    src = "wt-elsewhere"
                else:
                    src = "not-in-wt"
                rec["extra"].append({"text": t[:120], "source": src})
            # the page's headline source = the first extra h1's source
            rec["source"] = rec["extra"][0]["source"] if rec["extra"] else None
            if rec["source"] == "glued-in-claude":
                for name, rx in SEPS:
                    if line and re.search(rx, line):
                        rec["sep"] = name; break
        rows.append(rec)

# ---- aggregate
def agg(key):
    out = {}
    for k in sorted({key(r) for r in rows}):
        rs = [r for r in rows if key(r) == k]
        gold2 = [r for r in rs if r["gold_n"] >= 2]
        miss = [r for r in rs if r["gold_n"] > r["claude_n"]]
        src = collections.Counter(r["source"] for r in miss)
        sep = collections.Counter(r["sep"] for r in miss if r["source"] in ("wt-separated", "glued-in-claude"))
        out[k] = {"pages": len(rs), "modules": len({r["module"] for r in rs}), "gold_ge2": len(gold2), "gold_ge2_share": round(len(gold2) / len(rs), 3) if rs else 0,
                  "claude_ge2": sum(1 for r in rs if r["claude_n"] >= 2), "gold_more_than_claude": len(miss), "modules_missing": len({r["module"] for r in miss}),
                  "source": dict(src), "derivable": src["wt-separated"] + src["glued-in-claude"] + src["wt-elsewhere"], "sep": dict(sep),
                  "claude_zero": sum(1 for r in rs if r["claude_n"] == 0), "claude_more": sum(1 for r in rs if r["claude_n"] > r["gold_n"])}
    return out
by_tp = agg(lambda r: f"{r['template']}/{r['ptype']}")
by_subj = agg(lambda r: r["subject"])
miss = [r for r in rows if r["gold_n"] > r["claude_n"]]
src_all = collections.Counter(r["source"] for r in miss)
sep_all = collections.Counter(r["sep"] for r in miss if r["source"] in ("wt-separated", "glued-in-claude"))
L = [f"r358 title-pair probe — {len(rows)} paired pages / {len(codes)} modules",
     f"gold has MORE title h1s than Claude: {len(miss)} pages / {len({r['module'] for r in miss})} modules; sources {dict(src_all)}",
     f"  derivable (wt-separated + glued-in-claude + wt-elsewhere): {src_all['wt-separated'] + src_all['glued-in-claude'] + src_all['wt-elsewhere']}; separators among them {dict(sep_all)}",
     f"Claude has MORE than the gold: {sum(1 for r in rows if r['claude_n'] > r['gold_n'])} pages; Claude ZERO title h1: {sum(1 for r in rows if r['claude_n'] == 0)} pages {[r['module'] + '/' + r['page'] for r in rows if r['claude_n'] == 0][:8]}", ""]
L.append("BY template / page type:")
for k, v in by_tp.items():
    L.append(f"  {k:24} pages {v['pages']:4} gold≥2 {v['gold_ge2']:4} ({v['gold_ge2_share']:.2f}) claude≥2 {v['claude_ge2']:4} | gold>claude {v['gold_more_than_claude']:4} pages / {v['modules_missing']:3} mods: {v['source']} derivable {v['derivable']} seps {v['sep']}")
L.append("BY subject (gold>claude pages only where > 0):")
for k, v in sorted(by_subj.items(), key=lambda kv: -kv[1]["gold_more_than_claude"]):
    if v["gold_more_than_claude"]:
        L.append(f"  {k[:34]:34} pages {v['pages']:4} gold≥2 {v['gold_ge2_share']:.2f} | gold>claude {v['gold_more_than_claude']:4} / {v['modules_missing']:3} mods: {v['source']} seps {v['sep']}")
L.append(""); L.append("EXAMPLES (first 3 per source):")
for s in ("wt-separated", "glued-in-claude", "wt-elsewhere", "placeholder", "not-in-wt"):
    for r in [x for x in miss if x["source"] == s][:3]:
        L.append(f"  [{s}] {r['module']} {r['page']} ({r['template']}/{r['ptype']}, sep {r['sep']}): gold {r['gold']} | claude {r['claude']} | WT «{(r['wt_line'] or '')[:140]}»")
open(os.path.join(HERE, "_r358_titlepair.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
json.dump({"rows": rows, "by_template_ptype": by_tp, "by_subject": by_subj}, open(os.path.join(HERE, "_r358_titlepair.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("\n".join(L[:4])); print(f"wrote _r358_titlepair.json / .log ({len(L)} lines)")
