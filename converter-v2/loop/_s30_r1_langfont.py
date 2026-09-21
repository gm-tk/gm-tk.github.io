#!/usr/bin/env python3
"""Session 30 Round 1 PICK probe — the language-font classes (KB constraint 92 / CL-0093: `jp-text` / `ch-text` /
`pinyin` are MANDATORY on every run; the conversion applies them).

Over the skeleton gate's own pairing (gate_mods + pairs): for every gold page count the CJK runs (Han + kana) in
text nodes and whether each sits inside an element carrying ch-text / jp-text; the same for Claude's page (expected:
unwrapped). A run is DERIVABLE when the same run text is in Claude's page (Claude only ships WT text). Also the
`pinyin` spans: count and whether the span's text is in Claude's page. Per module: template, prefix, the wrap class,
the carrier tag, the parent tag ladder. Output: outputs/_s30_r1_langfont.out (+ .json).
"""
import os, sys, re, json
from collections import Counter, defaultdict
from html.parser import HTMLParser
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, HUMAN
from anchor_compare import CLAUDE

CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿豈-﫿＀-￯　-〿]+")
HAN = re.compile(r"[㐀-䶿一-鿿豈-﫿]")
KANA = re.compile(r"[぀-ヿ]")
LANG_CLS = {"ch-text", "jp-text", "pinyin"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, classes)
        self.runs = []           # (run_text, wrap_cls or None, carrier_tag, parent_tag)
        self.lang_spans = []     # (cls, tag, text, parent)
        self.cur = None
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get("class") or "").split())
        if tag in ("script", "style"):
            self.skip += 1
        self.stack.append((tag, cls, []))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        # pop to the matching tag
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                t, cls, texts = self.stack[i]
                if cls & LANG_CLS:
                    parent = self.stack[i - 1][0] if i > 0 else "?"
                    for c in cls & LANG_CLS:
                        self.lang_spans.append((c, t, "".join(texts).strip(), parent))
                del self.stack[i:]
                break
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
    def handle_data(self, data):
        if self.skip or not self.stack:
            return
        # record text into every open lang element
        for t, cls, texts in self.stack:
            if cls & LANG_CLS:
                texts.append(data)
        for m in CJK.finditer(data):
            run = m.group(0)
            if not (HAN.search(run) or KANA.search(run)):
                continue   # punctuation-only run
            wrap = None; carrier = None
            for t, cls, _ in reversed(self.stack):
                lc = cls & {"ch-text", "jp-text"}
                if lc:
                    wrap = sorted(lc)[0]; carrier = t; break
            parent = self.stack[-1][0]
            self.runs.append((run, wrap, carrier, parent))

def parse(path):
    p = P()
    with open(path, encoding="utf-8", errors="replace") as f:
        p.feed(f.read())
    return p

def main():
    out = {}
    mods_ = _corpus.gate_mods(CLAUDE)
    tot = Counter()
    per_mod = {}
    for code in mods_:
        pr = pairs(code)
        if not pr:
            continue
        rows = []
        for _k, cpath, hpath in pr:
            cp, hp = os.path.basename(cpath), os.path.basename(hpath)
            g = parse(hpath); c = parse(cpath)
            if not g.runs and not c.runs and not g.lang_spans and not c.lang_spans:
                continue
            ctext_runs = Counter(r[0] for r in c.runs)
            g_w = sum(1 for r in g.runs if r[1]); g_u = len(g.runs) - g_w
            g_deriv = sum(1 for r in g.runs if r[0] in ctext_runs)
            g_deriv_w = sum(1 for r in g.runs if r[0] in ctext_runs and r[1])
            c_w = sum(1 for r in c.runs if r[1]); c_u = len(c.runs) - c_w
            py = [s for s in g.lang_spans if s[0] == "pinyin"]
            # Claude page text for pinyin derivability
            ctxt = open(cpath, encoding="utf-8", errors="replace").read()
            py_deriv = sum(1 for s in py if s[2] and s[2] in ctxt)
            kinds = Counter(r[1] for r in g.runs if r[1])
            carriers = Counter(r[2] for r in g.runs if r[1])
            parents = Counter(r[3] for r in g.runs)
            cparents = Counter(r[3] for r in c.runs)
            rows.append(dict(cp=cp, hp=hp, g_runs=len(g.runs), g_wrapped=g_w, g_unwrapped=g_u, g_derivable=g_deriv,
                             g_derivable_wrapped=g_deriv_w, c_runs=len(c.runs), c_wrapped=c_w, c_unwrapped=c_u,
                             g_pinyin=len(py), g_pinyin_derivable=py_deriv, c_pinyin=sum(1 for s in c.lang_spans if s[0]=="pinyin"),
                             kinds=dict(kinds), carriers=dict(carriers), g_parents=dict(parents), c_parents=dict(cparents),
                             g_kana=sum(1 for r in g.runs if KANA.search(r[0])), c_kana=sum(1 for r in c.runs if KANA.search(r[0]))))
        if rows:
            per_mod[code] = rows
    # ---- report
    L = []
    L.append("SESSION 30 ROUND 1 PROBE — the language-font wrap (KB constraint 92 / CL-0093) over the gate's pairing")
    L.append(f"modules with any CJK run or lang span on a paired page: {len(per_mod)}")
    L.append("")
    L.append("per module: pages | GOLD runs wrapped / unwrapped (consensus) | gold runs derivable (in Claude text) | CLAUDE runs wrapped / unwrapped | pinyin gold / derivable / Claude | kinds | carriers")
    agg = Counter()
    for code, rows in sorted(per_mod.items(), key=lambda kv: -sum(r["g_runs"] for r in kv[1])):
        s = Counter()
        kinds = Counter(); carriers = Counter(); gp = Counter(); cpar = Counter()
        for r in rows:
            for k in ("g_runs","g_wrapped","g_unwrapped","g_derivable","g_derivable_wrapped","c_runs","c_wrapped","c_unwrapped","g_pinyin","g_pinyin_derivable","c_pinyin","g_kana","c_kana"):
                s[k] += r[k]
            kinds.update(r["kinds"]); carriers.update(r["carriers"]); gp.update(r["g_parents"]); cpar.update(r["c_parents"])
        pages_c = sum(1 for r in rows if r["c_runs"])
        pages_g = sum(1 for r in rows if r["g_runs"])
        cons = (s["g_wrapped"] / s["g_runs"]) if s["g_runs"] else 0
        L.append(f"  {code:9s} pages g{pages_g}/c{pages_c} | gold {s['g_wrapped']}/{s['g_unwrapped']} ({cons:.2f}) | deriv {s['g_derivable']} (wrapped {s['g_derivable_wrapped']}) | claude {s['c_wrapped']}/{s['c_unwrapped']} | pinyin {s['g_pinyin']}/{s['g_pinyin_derivable']}/{s['c_pinyin']} | kana g{s['g_kana']} c{s['c_kana']} | {dict(kinds)} | {dict(carriers.most_common(4))} | gold parents {dict(gp.most_common(5))} | claude parents {dict(cpar.most_common(5))}")
        agg.update(s)
        agg["pages_c"] += pages_c; agg["pages_g"] += pages_g
        agg["mods_c"] += 1 if pages_c else 0
    L.append("")
    L.append(f"TOTAL gold runs {agg['g_runs']} wrapped {agg['g_wrapped']} / unwrapped {agg['g_unwrapped']} (consensus {agg['g_wrapped']/max(1,agg['g_runs']):.2f}); derivable {agg['g_derivable']} (wrapped {agg['g_derivable_wrapped']}); Claude runs {agg['c_runs']} wrapped {agg['c_wrapped']} unwrapped {agg['c_unwrapped']} on {agg['pages_c']} pages / {agg['mods_c']} modules; pinyin gold {agg['g_pinyin']} derivable {agg['g_pinyin_derivable']} Claude {agg['c_pinyin']}")
    L.append("")
    L.append("per page (modules with Claude runs):")
    for code, rows in sorted(per_mod.items()):
        for r in rows:
            if r["c_runs"] or r["g_runs"] >= 5:
                L.append(f"  {code} {r['cp']} ~ {r['hp']}: gold {r['g_runs']} (w{r['g_wrapped']}/u{r['g_unwrapped']}, deriv {r['g_derivable']}) claude {r['c_runs']} (w{r['c_wrapped']}) pinyin {r['g_pinyin']}/{r['g_pinyin_derivable']}/{r['c_pinyin']} kinds {r['kinds']} gparents {dict(Counter(r['g_parents']).most_common(4))} cparents {dict(Counter(r['c_parents']).most_common(4))}")
    txt = "\n".join(L)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r1_langfont.out"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r1_langfont.json"), "w", encoding="utf-8") as f:
        json.dump(per_mod, f, ensure_ascii=False, indent=0)
    print(txt[:6000])

if __name__ == "__main__":
    main()
