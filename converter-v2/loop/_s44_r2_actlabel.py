#!/usr/bin/env python3
"""Session 44 Round 2 — the BILINGUAL "Activity NX: | Ngohe NX:" section opener (KB 07B §7 "Activity Structure").
For every Writers Template table (all modules, so the class is sized corpus-wide) classify the section opener:
  H1   — a `[H1] N.M` keystone opener (BilingualBuilder.bilingualSectionNum)
  LES  — a `[H2] Lesson N` opener (bilingualLessonNum)
  ACT  — the first content row is an "Activity NX:" / "Ngohe NX:" label pair and neither of the above fires  <- the candidate
For each ACT table: the title (the next row's [H2] text, reo column), whether the NEXT table is an `[Activity: Embedded]` table,
and where the title lands in the GOLD pages vs the CLAUDE pages of the module (inside div.activity / free / absent).
WSL, from outputs/: python3 _s44_r2_actlabel.py"""
import os, re, sys, glob, collections, io
from html.parser import HTMLParser
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
RED = re.compile(r"🔴|\[/?RED TEXT\]")
def clean(s): return re.sub(r"\s+", " ", RED.sub("", s).replace("*", "").replace("✅", "")).strip()
def tables(path):
    out, cur = [], None
    for ln in io.open(path, encoding="utf-8", errors="replace"):
        s = ln.rstrip("\n")
        if s.startswith("┌─── TABLE"): cur = []; continue
        if s.startswith("└─── END TABLE"):
            if cur is not None: out.append(cur)
            cur = None; continue
        if cur is not None and s.startswith("│ ") and not s.startswith("│ │"):
            cur.append([c.strip() for c in s[2:].split("║")])
    return out
SEC = re.compile(r"\[\s*H1\s*\]\s*(\d{1,2}\.\d{1,2})\b", re.I)
LES = re.compile(r"\[\s*h2\s*\]\s*(?:lesson|hei\s*mahi|ngohe)\s+(\d+)", re.I)
ACT = re.compile(r"^\s*(?:activity|ngohe)\s*\d+\s*[\.\d]*\s*[a-z]?\s*:?\s*$", re.I)
EMB = re.compile(r"\[\s*activity\s*:\s*embedded", re.I)
def is_header(r): return len(r) >= 2 and re.match(r"^\s*english\s*$", clean(r[0]), re.I) and re.search(r"reo|māori", clean(r[1]), re.I)
def norm(t): return re.sub(r"[^\wĀ-ſ ]+", "", re.sub(r"\s+", " ", t)).strip().lower()
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.st = []; s.blocks = []; s.cur = None
    def handle_starttag(s, t, a):
        if t in ("br", "img", "hr", "input", "source", "meta", "link", "audio"): return
        cls = dict(a).get("class") or ""
        s.st.append((t, cls))
        if t in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th"): s.cur = [t, [], [x for x in s.st]]
    def handle_endtag(s, t):
        if s.cur and s.cur[0] == t:
            txt = "".join(s.cur[1]); s.blocks.append((t, norm(txt), s.cur[2])); s.cur = None
        while s.st:
            x = s.st.pop()
            if x[0] == t: break
    def handle_data(s, d):
        if s.cur: s.cur[1].append(d)
def where(stack):
    cl = " ".join(c for _, c in stack)
    if "cv2-int-raw" in cl or "cv2-interactive" in cl: return "handoff"
    if re.search(r"\bactivity\b", cl): return "activity"
    if "moduleMenu" in cl or "module-menu" in cl: return "menu"
    if re.search(r"\balert", cl): return "alert"
    return "free"
def page_blocks(d):
    bl = []
    for p in sorted(glob.glob(os.path.join(d, "*.html"))):
        try: x = P(); x.feed(io.open(p, encoding="utf-8", errors="replace").read()); bl += [(os.path.basename(p), *b) for b in x.blocks]
        except Exception: pass
    return bl
def locate(bl, title):
    n = norm(title)
    if len(n) < 2: return "short"
    hits = [where(st) for pg, t, tx, st in bl if tx == n and t[0] == "h"] or [where(st) for pg, t, tx, st in bl if tx == n]
    if not hits: return "absent"
    for k in ("activity", "handoff", "alert", "free", "menu"):
        if k in hits: return k
    return hits[0]
kinds = collections.Counter(); per = collections.defaultdict(collections.Counter); ex = []
gold_where = collections.Counter(); cl_where = collections.Counter(); pair = collections.Counter(); fam_pair = collections.defaultdict(collections.Counter)
nextemb = collections.Counter()
for tdir in sorted(glob.glob(os.path.join(GOLD, "*", "*"))):
    code = os.path.basename(tdir)
    wts = [p for p in glob.glob(os.path.join(tdir, "*_parsed.txt")) if "writers template" in p.lower()] or glob.glob(os.path.join(tdir, "*_parsed.txt"))
    if not wts: continue
    T = []
    for w in wts: T += tables(w)
    acts = []
    for ti, rows in enumerate(T):
        if not rows or len(rows[0]) < 2: continue
        head3 = " ".join(clean(" ".join(r)) for r in rows[:3])
        s0 = 1 if is_header(rows[0]) else 0
        if SEC.search(" ".join(" ".join(r) for r in rows[:3]).replace("*", "")): kinds["H1"] += 1; per[code]["H1"] += 1; continue
        if len(rows) > s0 and LES.search(" ".join(rows[s0]).replace("*", "")): kinds["LES"] += 1; per[code]["LES"] += 1; continue
        if len(rows) > s0 + 1 and len(rows[s0]) >= 2 and all(ACT.match(clean(c)) for c in rows[s0][:2]):
            kinds["ACT"] += 1; per[code]["ACT"] += 1
            tr = rows[s0 + 1]
            reo = clean(re.sub(r"\[[^\]]*\]", "", tr[1] if len(tr) > 1 else tr[0])); eng = clean(re.sub(r"\[[^\]]*\]", "", tr[0]))
            nxt = T[ti + 1] if ti + 1 < len(T) else []
            emb = bool(nxt and EMB.search(" ".join(" ".join(r) for r in nxt[:2])))
            nextemb[emb] += 1
            acts.append((reo, eng, emb, "h2" in (tr[0] + tr[-1]).lower()))
    if not acts: continue
    cdir = os.path.join(CL, os.path.basename(os.path.dirname(tdir)), code)
    if not os.path.isdir(cdir):
        cands = glob.glob(os.path.join(CL, "*", code)); cdir = cands[0] if cands else None
    gb = page_blocks(tdir); cb = page_blocks(cdir) if cdir else []
    for reo, eng, emb, h2 in acts:
        t = reo or eng
        g = locate(gb, t); c = locate(cb, t)
        gold_where[g] += 1; cl_where[c] += 1; pair[(g, c, emb)] += 1
        fam = re.match(r"[A-Z]+\d?", code).group(0); fam_pair[fam][(g, c)] += 1
        if len(ex) < 40 and g == "activity" and c != "activity": ex.append((code, t[:50], emb, g, c))
print("table openers over all WTs:", dict(kinds))
print("modules with ACT tables:", {k: v["ACT"] for k, v in per.items() if v["ACT"]})
print("ACT followed by an [Activity: Embedded] table:", dict(nextemb))
print("gold title location:", dict(gold_where)); print("claude title location:", dict(cl_where))
print("(gold, claude, next-is-embedded):")
for k, v in pair.most_common(): print("  ", k, v)
print("per family (gold, claude):")
for f, c in sorted(fam_pair.items()): print("  ", f, dict(c.most_common()))
print("examples gold=activity, claude elsewhere:")
for e in ex[:25]: print("  ", e)
