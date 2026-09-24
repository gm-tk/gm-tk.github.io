#!/usr/bin/env python3
"""THE PLACEMENT CENSUS (LOOP §1g — Chris's D14-S1, 24 Sept 2026; built in session 42 as the lane's measurement-tool round).

WHERE DOES THE HUMAN PUT IT vs WHERE DOES CLAUDE PUT IT. The skeleton SCAFFOLD collapses every widget container (the module
menu's `div.tabs` included) to one WIDGET line, the miner's menu census counts text presence, and compare_structure reads #body
only — so a section in the wrong menu pane, a paragraph swallowed by a hand-off box, or a note moved out of its activity box scores
nothing anywhere. This tool locates CONTENT, not tags: every text block (h1–h6, p, li, td, th, figcaption, dt, dd) on the gold page
and on Claude's paired page is tagged with its CONTAINER PATH —

  header:chip | header:title | header:other
  menu:<pane>            the module menu; <pane> = the nav label canonicalised (Overview / Knowledge / Practices / Information /
                         Standards / LI / Lesson / paneN) or `flat` when the menu has no tabs
  body[:panelN]:<kind>[:side]
                         kind = the innermost special container: widget:<type> (the skeleton's WIDGET_MARKERS + the hand-off
                         box `cv2-int-raw`), activity, alert, acks, or free; panelN = the Inquiry panel; `:side` = a narrow
                         column (col-*-3 / col-*-4)
  footer | other

— then gold blocks are matched to Claude blocks by text (exact → 40-character prefix → token Jaccard ≥ 0.7 on the paired page;
then exact / prefix on the module's other Claude pages = OTHER-PAGE; else ABSENT, split by whether the text is in the module's
Writers Template: ABSENT-inWT is a derivable loss, ABSENT-notWT is the developer's own words). It reports the TRANSITION TABLE
(gold region → Claude region) with blocks / pages / modules, the per-family and per-template shares, candidate flags against the
§1d floors (chrome = header / menu / footer: 10 modules; body: 20 pages; a share ≥ 0.60 in a family or template group), and
examples; the same for HEADINGS alone (sections); and the derivable losses by region.

It folds the four session-41 probes: `_r460_rawmenu.py` (the menu-only view → the menu:<pane> regions), `_s41_r8_kppane.py`
(which pane holds a named section → the heading table), `_s41_r8_lost.py` (WT text the gold carries and no Claude page carries →
ABSENT-inWT), `_s41_r10_boxtitle2.py` (where an activity box's title landed → body:activity vs elsewhere).

Population: `_corpus.gate_mods()` — the D14-21 / D10-6 exclusions are never measured. Pairing: the skeleton gate's own
`_discrepancy_audit.pairs()`.

Usage (WSL, from CONVERTER_V2/reference/tests):
  python3 ../../outputs/_placement_census.py                       # full census → outputs/_placement_census.{md,json}
  python3 ../../outputs/_placement_census.py --codes TRR102 PNR101 # scoped
  python3 ../../outputs/_placement_census.py --out _pc_r466        # outputs/_pc_r466.{md,json}
"""
import os, re, sys, json, time, collections, html as H
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
import _corpus
import _discrepancy_audit as DA
from anchor_compare import CLAUDE, HUMAN
from _structural_skeleton import WIDGET_MARKERS, body_source

O = os.path.abspath(os.path.join("..", "..", "outputs"))
BLOCK = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "figcaption", "dt", "dd"}
VOID = {"img", "br", "input", "col", "hr", "meta", "link", "source", "area", "base", "wbr"}
DROP = {"script", "style", "noscript", "svg"}
WIDGETS = set(WIDGET_MARKERS) | {"cv2-int-raw", "cv2-interactive"}
NARROW = re.compile(r"^col-(?:sm-|md-|lg-|xl-)?[34]$")
CHROME = ("header", "menu", "footer")

def norm(s):
    s = H.unescape(s).lower()
    s = re.sub(r"[‘’“”'\"`*_]", "", s)
    s = re.sub(r"[^0-9a-zāēīōū]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def canon_pane(label, i):
    t = norm(label)
    for keys, name in ((("knowledge", "mātauranga", "matauranga"), "Knowledge"), (("practice", "tikanga"), "Practices"),
                       (("information", "mataara", "info"), "Information"), (("standard", "paerewa"), "Standards"),
                       (("learning intention", "success criteria", "whāinga", "whainga"), "LI"),
                       (("overview", "whakataki", "tirohanga", "introduction"), "Overview"), (("lesson", "akoranga"), "Lesson")):
        if any(k in t for k in keys): return name
    return f"pane{i + 1}"

class Page(HTMLParser):
    """Streams one page: a stack of open elements (tag, id, classes); every block element opens a record whose region is
    computed from the stack at its start; text goes to the innermost open block."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.blocks = []; self.open = []; self.skip = 0
        self.menu_panes = 0; self.nav = []; self.in_nav = False; self.panels = 0
    def ctx(self):
        region, kind, side, pane, panel = "other", "free", False, None, None
        for tag, eid, cls, extra in self.stack:
            if eid == "header": region, kind = "header", "other"
            elif eid == "module-code": kind = "chip"
            elif eid == "module-menu-content": region, kind = "menu", "flat"
            elif eid == "body": region, kind = "body", "free"
            elif eid == "footer": region, kind = "footer", ""
            if region == "menu" and "tab-pane" in cls: pane = extra
            if region == "body":
                if "inquiryPanel" in cls: panel = extra
                if cls & WIDGETS: kind = "widget:" + sorted(cls & WIDGETS)[0]
                elif kind.startswith("widget:"): pass
                elif "activity" in cls: kind = "activity"
                elif "alert" in cls or any(c.startswith("alert") for c in cls): kind = "alert"
                elif "acks" in cls or "acksLesson" in cls or "acksTemplate" in cls: kind = "acks"
                if any(NARROW.match(c) for c in cls): side = True
                elif any(c.startswith("col-") for c in cls): side = False
        if any(("acks" in c[2] or "acksTemplate" in c[2] or "acksLesson" in c[2]) for c in self.stack):
            return "acks", ""
        if region == "menu":
            return "menu", ("pane", pane) if pane is not None else "flat"
        if region == "header":
            return "header", kind if kind in ("chip",) else "other"
        if region == "body":
            k = kind + (":side" if side and not kind.startswith("widget") else "")
            return "body", ((f"panel{panel}:" if panel else "") + k)
        return region, kind
    def handle_starttag(self, tag, attrs):
        if self.skip:
            if tag not in VOID: self.skip += 1
            return
        if tag in DROP: self.skip = 1; return
        if tag in VOID: return
        a = dict(attrs); cls = set((a.get("class") or "").split()); eid = a.get("id") or ""
        extra = None
        in_menu = any(s[1] == "module-menu-content" for s in self.stack)
        if in_menu and "tab-pane" in cls: extra = self.menu_panes; self.menu_panes += 1
        if "inquiryPanel" in cls: self.panels += 1; extra = self.panels
        if tag == "ul" and "nav-tabs" in cls and in_menu: self.in_nav = True
        self.stack.append((tag, eid, cls, extra))
        if tag in BLOCK:
            self.open.append({"tag": tag, "ctx": self.ctx(), "text": [], "depth": len(self.stack), "nav": self.in_nav})
    def handle_endtag(self, tag):
        if self.skip:
            self.skip -= 1; return
        if tag in VOID: return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                depth = i + 1
                while self.open and self.open[-1]["depth"] >= depth:
                    b = self.open.pop(); self.emit(b)
                if tag == "ul" and self.in_nav: self.in_nav = False
                del self.stack[i:]; break
    def handle_data(self, d):
        if self.skip or not self.open: return
        self.open[-1]["text"].append(d)
    def emit(self, b):
        raw = re.sub(r"\s+", " ", "".join(b["text"])).strip()
        if not raw: return
        if b["nav"]:
            if b["tag"] == "li": self.nav.append(raw)
            return
        self.blocks.append((b["tag"], norm(raw), raw[:90], b["ctx"]))
    def finish(self):
        while self.open: self.emit(self.open.pop())
        out = []
        for tag, t, raw, (reg, sub) in self.blocks:
            if reg == "menu" and isinstance(sub, tuple):
                i = sub[1]; lab = self.nav[i] if i is not None and i < len(self.nav) else ""
                sub = canon_pane(lab, i or 0)
            out.append((tag, t, raw, f"{reg}:{sub}" if sub else reg))
        return out

_cache = {}
def parse(path):
    if path in _cache: return _cache[path]
    try: s = open(path, encoding="utf-8", errors="replace").read()
    except OSError: return []
    p = Page()
    try: p.feed(body_source(s)); p.close()
    except Exception: pass
    r = p.finish(); _cache[path] = r; return r

def keep(t): return len(t) >= 20 or len(t.split()) >= 4
def jacc(a, b):
    A, B = set(a.split()), set(b.split())
    return len(A & B) / max(1, len(A | B))
def coarse(r):
    # the transition key: menu keeps its pane, body keeps kind (+side), panels are folded (panelN -> panel)
    return re.sub(r"panel\d+:", "panel:", r)

def wt_shingles(hd):
    txt = ""
    for f in os.listdir(hd) if os.path.isdir(hd) else []:
        if f.endswith("_parsed.txt") and ("media list_parsed" not in f.lower() or "writers template" in f.lower()):   # the combined WT + ML file is a WT (OPERATING_GUIDE §16)
            txt += " " + open(os.path.join(hd, f), encoding="utf-8", errors="replace").read()
    txt = re.sub(r"🔴|\[/?RED TEXT\]", " ", txt); txt = re.sub(r"\[[^\]]{0,60}\]", " ", txt)
    w = norm(txt).split()
    return set(" ".join(w[i:i + 4]) for i in range(max(0, len(w) - 3))), " ".join(w)
def in_wt(t, sh, flat):
    w = t.split()
    if len(w) < 4: return f" {t} " in f" {flat} "
    g = [" ".join(w[i:i + 4]) for i in range(len(w) - 3)]
    return sum(1 for x in g if x in sh) / len(g) >= 0.5

def main():
    args = sys.argv[1:]; out = "_placement_census"; codes = None
    if "--out" in args: i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
    if "--codes" in args: i = args.index("--codes"); codes = args[i + 1:]
    mods = sorted(_corpus.gate_mods(CLAUDE))
    if codes: mods = [c for c in mods if c in set(codes)]
    t0 = time.time()
    T = collections.Counter(); TP = collections.defaultdict(set); TM = collections.defaultdict(set)
    TF = collections.defaultdict(collections.Counter); TT = collections.defaultdict(collections.Counter)
    HT = collections.Counter(); HM = collections.defaultdict(set); HP = collections.defaultdict(set)
    GX = collections.defaultdict(collections.Counter)            # gold region totals by family (matched on the page)
    GA = collections.defaultdict(collections.Counter)            # gold region totals by family (every fate)
    CY = collections.defaultdict(collections.Counter)            # claude region totals by family (matched on the page)
    EX = collections.defaultdict(list); HEX = collections.defaultdict(list)
    fates = collections.Counter(); npairs = 0; tmpl_of = {}
    for code in mods:
        hd = _corpus.mdir(HUMAN, code); cd = _corpus.mdir(CLAUDE, code)
        tmpl = os.path.basename(os.path.dirname(os.path.normpath(hd))); tmpl_of[code] = tmpl
        fam = re.match(r"[A-Z]+", code).group(0)
        sh, flat = wt_shingles(hd)
        mod_claude = collections.defaultdict(list)
        for f in sorted(os.listdir(cd)) if os.path.isdir(cd) else []:
            if f.endswith(".html"):
                for tag, t, raw, reg in parse(os.path.join(cd, f)):
                    if keep(t): mod_claude[t].append((f, reg)); mod_claude["\x00" + t[:40]].append((f, reg))
        for _, cp, hp in DA.pairs(code):
            npairs += 1; page = os.path.basename(cp)
            G = [b for b in parse(hp) if keep(b[1])]; C = [b for b in parse(cp) if keep(b[1])]
            used = [False] * len(C); Cset = [set(b[1].split()) for b in C]
            by_t = collections.defaultdict(list); by_p = collections.defaultdict(list)
            for j, (tag, t, raw, reg) in enumerate(C): by_t[t].append(j); by_p[t[:40]].append(j)
            for tag, t, raw, greg in G:
                j = None
                for pool in (by_t.get(t, []), by_p.get(t[:40], []) if len(t) >= 40 else []):
                    free = [k for k in pool if not used[k]]
                    if free:
                        j = next((k for k in free if C[k][3] == greg), free[0]); break
                if j is None:
                    best, bj = 0.0, None; A = set(t.split())
                    for k, B in enumerate(Cset):
                        if used[k]: continue
                        s = len(A & B) / max(1, len(A | B))
                        if s > best: best, bj = s, k
                    if best >= 0.7: j = bj
                GA[fam][coarse(greg)] += 1
                if j is not None:
                    used[j] = True; creg = C[j][3]
                    a, b = coarse(greg), coarse(creg)
                    GX[fam][a] += 1; CY[fam][b] += 1
                    if a == b: fates["SAME"] += 1; continue
                    fates["MOVED"] += 1
                    key = (a, b); T[key] += 1; TP[key].add(f"{code}/{page}"); TM[key].add(code); TF[key][fam] += 1; TT[key][tmpl] += 1
                    if len(EX[key]) < 8 and all(e[0] != code for e in EX[key][:4]): EX[key].append((code, page, tag, C[j][0], raw))
                    if tag[0] == "h" and tag[1:].isdigit():
                        HT[key] += 1; HM[key].add(code); HP[key].add(f"{code}/{page}")
                        if len(HEX[key]) < 6: HEX[key].append((code, page, tag, C[j][0], raw))
                    continue
                other = mod_claude.get(t) or (mod_claude.get("\x00" + t[:40]) if len(t) >= 40 else None)
                if other and any(f != page for f, _ in other):
                    fate = "OTHER-PAGE"
                else:
                    fate = "ABSENT-inWT" if in_wt(t, sh, flat) else "ABSENT-notWT"
                fates[fate] += 1
                a = coarse(greg); key = (a, fate)
                T[key] += 1; TP[key].add(f"{code}/{page}"); TM[key].add(code); TF[key][fam] += 1; TT[key][tmpl] += 1
                if len(EX[key]) < 8 and all(e[0] != code for e in EX[key][:4]): EX[key].append((code, page, tag, "—", raw))
                if tag[0] == "h" and tag[1:].isdigit():
                    HT[key] += 1; HM[key].add(code); HP[key].add(f"{code}/{page}")
                    if len(HEX[key]) < 6: HEX[key].append((code, page, tag, "—", raw))
        _cache.clear()
    dt = time.time() - t0
    # ---------------------------------------------------------------- report
    fam_mods = collections.Counter(re.match(r"[A-Z]+", c).group(0) for c in mods)
    def is_chrome(r): return r.split(":")[0] in CHROME
    def cand(key):
        a, b = key
        chrome = is_chrome(a) or is_chrome(b)
        floor_ok = len(TM[key]) >= 10 if chrome else len(TP[key]) >= 20
        # the consistency share per FAMILY group: of the gold's region-a blocks in that family (every fate), the share with this
        # fate; only a group holding >= 3 of the class's modules may define it (one module is never a consensus)
        best = None
        for fam, n in TF[key].items():
            fm = sum(1 for c in TM[key] if re.match(r"[A-Z]+", c).group(0) == fam)
            if fm < 3: continue
            share = n / max(1, GA[fam][a])
            if best is None or share > best[1]: best = (fam, share, n, fm)
        return floor_ok, best
    def flag_of(key, ok, best):
        a, b = key
        if b == "ABSENT-notWT": return "not derivable"
        if a == "acks" or b == "acks": return "acks gate"
        if a.startswith("body:") and "widget:" in a and "widget:cv2" in b: return "un-built widget (A1)"
        if ok and best and best[1] >= 0.60: return "CANDIDATE"
        return "floor ok" if ok else "below floor"
    L = []
    L.append(f"# THE PLACEMENT CENSUS (LOOP §1g, D14-S1) — where the human puts it vs where Claude puts it\n")
    L.append(f"Generated {time.strftime('%Y-%m-%d %H:%M')} by `outputs/_placement_census.py` over {len(mods)} modules / {npairs} "
             f"paired pages (`_corpus.gate_mods()`; the skeleton gate's pairing) in {dt:.0f} s. A block = one h1–h6 / p / li / td / th "
             f"/ figcaption / dt / dd with ≥ 20 characters or ≥ 4 words; the module menu's nav labels are not blocks.\n")
    tot = sum(fates.values())
    L.append("## Summary — the fate of every gold block\n")
    for k in ("SAME", "MOVED", "OTHER-PAGE", "ABSENT-inWT", "ABSENT-notWT"):
        L.append(f"- **{k}**: {fates[k]} ({100 * fates[k] / max(1, tot):.1f} %)")
    L.append(f"- total gold blocks: {tot}\n")
    L.append("`SAME` = Claude has the text on the paired page in the same container path; `MOVED` = on the paired page in a DIFFERENT "
             "container (the table below); `OTHER-PAGE` = only on another Claude page of the module; `ABSENT-inWT` = on no Claude page "
             "but in the Writers Template (a derivable loss); `ABSENT-notWT` = the developer's own words (not derivable).\n")
    L.append("## 1. The transition table — gold region → Claude region (MOVED, OTHER-PAGE and ABSENT), largest first\n")
    L.append("Floors (§1d / §1g): a chrome transition (header / menu / footer on either side) needs 10 modules; a body transition 20 "
             "pages. `share` = of the gold's region-A blocks in the best family (that Claude has anywhere), the share that took this "
             "fate — a consistent placement at ≥ 0.60 over the floor is a CANDIDATE.\n")
    L.append("| # | gold region | Claude region / fate | blocks | pages | modules | best family (share, blocks, modules) | templates | flag |")
    L.append("|---:|---|---|---:|---:|---:|---|---|---|")
    ranked = sorted(T, key=lambda k: -T[k]); js = []
    for i, key in enumerate(ranked[:150], 1):
        ok, best = cand(key)
        flag = flag_of(key, ok, best)
        tm = ", ".join(f"{t} {n}" for t, n in TT[key].most_common(3))
        bf = f"{best[0]} ({best[1]:.2f}, {best[2]}, {best[3]})" if best else ""
        L.append(f"| {i} | `{key[0]}` | `{key[1]}` | {T[key]} | {len(TP[key])} | {len(TM[key])} | {bf} | {tm} | {flag} |")
        js.append({"rank": i, "gold": key[0], "claude": key[1], "blocks": T[key], "pages": len(TP[key]), "modules": len(TM[key]),
                   "families": dict(TF[key].most_common()), "templates": dict(TT[key]), "flag": flag,
                   "best_family": list(best) if best else None, "examples": EX[key][:8], "module_list": sorted(TM[key])})
    L.append("\n## 2. Headings only (the SECTIONS) — gold region → Claude region / fate\n")
    L.append("| gold region | Claude region / fate | headings | pages | modules | examples |")
    L.append("|---|---|---:|---:|---:|---|")
    for key in sorted(HT, key=lambda k: -HT[k])[:60]:
        ex = "; ".join(f"{c} {p} <{g}>→<{cl}> “{r[:50]}”" for c, p, g, cl, r in HEX[key][:3])
        L.append(f"| `{key[0]}` | `{key[1]}` | {HT[key]} | {len(HP[key])} | {len(HM[key])} | {ex} |")
    L.append("\n## 3. Region agreement — of the gold's blocks in region A that Claude has on the paired page, the share it keeps in A\n")
    agg_g = collections.Counter(); agg_same = collections.Counter()
    for fam, c in GX.items():
        for r, n in c.items(): agg_g[r] += n
    for key, n in T.items():
        pass
    moved_from = collections.Counter()
    for (a, b), n in T.items():
        if not b.startswith(("OTHER", "ABSENT")): moved_from[a] += n
    L.append("| gold region | matched on page | kept in region | moved | agreement |")
    L.append("|---|---:|---:|---:|---:|")
    for r, n in agg_g.most_common(40):
        mv = moved_from[r]
        L.append(f"| `{r}` | {n} | {n - mv} | {mv} | {(n - mv) / max(1, n):.3f} |")
    L.append("\n## 4. Examples for the 25 largest transitions\n")
    for key in ranked[:25]:
        L.append(f"### `{key[0]}` → `{key[1]}` — {T[key]} blocks / {len(TP[key])} pages / {len(TM[key])} modules")
        L.append("families: " + ", ".join(f"{f} {n}" for f, n in TF[key].most_common(8)))
        for c, p, g, cl, r in EX[key][:6]:
            L.append(f"- {c} `{p}` <{g}>→<{cl}> “{r}”")
        L.append("")
    md = os.path.join(O, out + ".md"); jf = os.path.join(O, out + ".json")
    open(md, "w", encoding="utf-8").write("\n".join(L) + "\n")
    json.dump({"generated": time.strftime("%Y-%m-%d %H:%M"), "modules": len(mods), "pairs": npairs, "fates": dict(fates),
               "transitions": js, "headings": [{"gold": a, "claude": b, "headings": HT[(a, b)], "pages": len(HP[(a, b)]),
                                                "modules": sorted(HM[(a, b)]), "examples": HEX[(a, b)]} for a, b in sorted(HT, key=lambda k: -HT[k])[:120]]},
              open(jf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"placement census: {len(mods)} modules / {npairs} pairs / {tot} gold blocks in {dt:.0f} s — " +
          " ".join(f"{k} {fates[k]}" for k in ("SAME", "MOVED", "OTHER-PAGE", "ABSENT-inWT", "ABSENT-notWT")))
    print(f"wrote {md}\nwrote {jf}")

if __name__ == "__main__":
    main()
