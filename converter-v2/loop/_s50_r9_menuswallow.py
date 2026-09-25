"""_s50_r9_menuswallow.py — session 50 Round 9 PICK: pages whose MODULE MENU holds far more text than the gold's menu (the menu
partition swallowed the body). For every paired page: text chars inside #module-menu-content (Claude vs gold) and the page's total.
Run under WSL from CONVERTER_V2/reference/tests/:  python3 ../../outputs/_s50_r9_menuswallow.py → ../../outputs/_s50_r9_menuswallow.log"""
import os, sys, re, collections
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _corpus
CLAUDE = os.path.join(os.getcwd(), "..", "..", "..", "01-Claude_Modules_")


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack = []; self.menu = None; self.m = 0; self.t = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("br", "img", "hr", "input", "meta", "link", "source"): return
        a = dict(attrs)
        self.stack.append(tag)
        if a.get("id") == "module-menu-content" and self.menu is None: self.menu = len(self.stack)
    def handle_endtag(self, tag):
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k] == tag:
                del self.stack[k:]; break
        if self.menu is not None and len(self.stack) < self.menu: self.menu = None
    def handle_data(self, d):
        n = len(d.strip())
        if not n: return
        self.t += n
        if self.menu is not None: self.m += n


def meas(p):
    x = P()
    try: x.feed(open(p, encoding="utf-8", errors="ignore").read())
    except Exception: pass
    return x.m, x.t


rows = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    try: prs = list(DA.pairs(code))
    except Exception: continue
    for _, cp, hp in prs:
        cm, ct = meas(cp); gm, gt = meas(hp)
        if ct and cm >= 2000 and cm > 3 * max(gm, 300):
            rows.append((cm / ct, code, os.path.basename(cp), cm, ct, gm, gt))
rows.sort(reverse=True)
fam = collections.Counter(re.match(r"[A-Z]+", r[1]).group(0) for r in rows)
out = [f"pages whose module menu holds >= 2000 chars and > 3x the gold menu: {len(rows)} ({len({r[1] for r in rows})} modules)",
       "by family: " + ", ".join(f"{f} {n}" for f, n in fam.most_common())]
out += [f"  {r[1]:10s} {r[2]:26s} menu {r[3]:6d} / page {r[4]:6d} ({100*r[0]:3.0f} %)  gold menu {r[5]:5d} / page {r[6]:6d}" for r in rows[:60]]
open("../../outputs/_s50_r9_menuswallow.log", "w").write("\n".join(out) + "\n"); print("\n".join(out[:45]))
