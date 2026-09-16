#!/usr/bin/env python3
"""_measure_r344_c47.py — ROUND 344 (the autonomous loop, session 12 — Chris's D10-1: KB constraint 47 in full).

The c47 TARGET on a lesson page is the FIRST RENDERED FREE-BODY heading — the first h2–h5 inside #body that is
NOT inside an activity box / widget / hand-off box (the r320 tool compared every heading by text and so counted
activity-box titles rendered by activityOpen — ENGI101 "Being Frank" — and later section repeats as cases) —
whose text equals the header <h1><span> title under the c47 test: case, punctuation and a leading `Lesson N`
label (any form) ignored.  The gold's treatment of that heading (present anywhere in its body / absent) sizes
the gain half (gold-absent → the page moves gold-ward) and the NAMED-override half (gold-kept).

Per page it records the comparison LADDER the engine's seam walks:
  exact          — the existing compare (Utils.Fold + whitespace removed) already matches → the de-dup SHOULD have
                   fired; it survives only because an EARLIER heading spent the first-heading slot (the MXEO202
                   mechanism: a consumed heading must not spend the slot — `first_rendered_heading`)
  lesson-prefix  — matches after the r75/r324 `Lesson N` strip on both sides (same slot mechanism)
  punct          — matches only once every non-letter/digit is dropped (`ignore_punctuation`: HIS1001's curly
                   quotes, ENGR202's italicised `*:*`, PES1002's `**` markers + the writer's trailing note)
Bilingual (body class reoTranslate) pages are listed but EXCLUDED from the target (KB 07B governs the MTK section
heading — the more specific rule wins). The overview page is strip-only (r320) and is reported separately.

Sibling (D10-1): header titles that still carry a markdown marker (`*`) — listed with the gold's title.

Paths are dynamic (CLAUDE.md §13). Run from anywhere under WSL:  python3 _measure_r344_c47.py [--all]
  default: the scored population (_corpus.gate_mods); --all: every module dir (the affected-set scan, §10a step 1).
Writes _r344_c47.json (+ _affected_r344.txt with --all) next to itself and prints the summary.
"""
import os, re, sys, json, html, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, CLAUDE

H1 = re.compile(r"<h1><span>(.*?)</span></h1>", re.S)
TOK = re.compile(r"<(/?)(div|h[2-5]|section|aside)\b([^>]*)>", re.S)
HEND = re.compile(r"</h[2-5]\s*>", re.S)
TAG = re.compile(r"<[^>]+>")
CLS = re.compile(r'class="([^"]*)"')
IDA = re.compile(r'id="([^"]*)"')
# a heading under any of these containers is NOT free body (activity boxes, built widgets, hand-off boxes, notes, menus)
BOXED = re.compile(r"\b(activity|cv2-interactive|cv2-note|cv2-comment|accordion|carousel|flipCard|clickDrop|dragAndDrop|"
                   r"tabs?|tab-content|modal|selfCheck|infoTrigger|hint|hintSlider|shapeHover|speechBubble|dropDown|card|"
                   r"alert|panel|mtkQuiz|wordDrag|slider|glossary)\b", re.I)
BOXED_ID = re.compile(r"^(module-menu|module-menu-content|footer|acknowledgements|acks)")
LESSON = re.compile(r"^lesson\s*#?\s*(\d+(?:\.\d+)?[a-z]?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b"
                    r"\s*(continued)?\s*[:.\-–—]?\s*", re.I)

def plain(s):
    """rendered heading/title → the engine's `text` (tags gone, entities decoded, markdown markers dropped)."""
    return html.unescape(TAG.sub("", s)).replace("*", "").strip()

def fold(s):
    """Utils.Fold + whitespace removed — the engine's existing compare key."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"').replace(" ", " ")
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", "", s.strip().lower())

def strip_lesson(s):
    m = LESSON.match(s.strip())
    return s[m.end():] if m and s[m.end():].strip() else s

def punct(s):
    return re.sub(r"[^a-z0-9]+", "", fold(s))

def ladder(htext_plain, title_plain):
    if not title_plain or not htext_plain: return None
    if fold(htext_plain) == fold(title_plain): return "exact"
    if fold(strip_lesson(htext_plain)) == fold(strip_lesson(title_plain)): return "lesson-prefix"
    if punct(strip_lesson(htext_plain)) == punct(strip_lesson(title_plain)): return "punct"
    return None

def body_of(page):
    m = re.search(r'<div id="body"[^>]*>', page)
    if not m: return ""
    end = re.search(r'<div id="footer"|<footer\b', page[m.end():])
    return page[m.end(): m.end() + end.start()] if end else page[m.end():]

def headings(body):
    """[(text_raw, boxed:bool, level)] for every h2–h5 in document order, boxed = inside a widget/box container."""
    out = []; stack = []; pos = 0
    for m in TOK.finditer(body):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3) or ""
        if tag.startswith("h"):
            if closing: continue
            e = HEND.search(body, m.end()); raw = body[m.end(): e.start()] if e else ""
            c = CLS.search(attrs); hcls = c.group(1) if c else ""
            boxed = any(BOXED.search(k) for k in stack) or bool(re.search(r"\bgoJournal\b", hcls))
            out.append((raw, boxed, int(tag[1])))
            continue
        if closing:
            if stack: stack.pop()
        else:
            if attrs.rstrip().endswith("/"): continue
            c = CLS.search(attrs); i = IDA.search(attrs)
            key = (c.group(1) if c else "") + " " + ("#" + i.group(1) if i else "")
            if i and BOXED_ID.match(i.group(1)): key += " cv2-note"
            stack.append(key)
    return out

def titles(page):
    m = re.search(r'<div id="header".*?<div id="body"', page, re.S); seg = m.group(0) if m else page[:12000]
    return H1.findall(seg)

def main():
    scan_all = "--all" in sys.argv
    codes = _corpus.mods(CLAUDE) if scan_all else _corpus.gate_mods(CLAUDE)
    rows = []; sib = []; C = collections.Counter(); byT = collections.defaultdict(collections.Counter)
    byS = collections.defaultdict(collections.Counter); later = collections.Counter(); inbox = collections.Counter()
    affected = set(); npages = 0
    for code in codes:
        cdir = _corpus.mdir(CLAUDE, code); tmpl = os.path.basename(os.path.dirname(cdir)) if cdir else "?"
        subj = re.match(r"[A-Z]+", code).group(0) if re.match(r"[A-Z]+", code) else code
        for n, cp, hp in pairs(code):
            npages += 1
            ch = open(cp, encoding="utf-8", errors="replace").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
            bil = bool(re.search(r'<body class="[^"]*\breoTranslate\b', ch))
            overview = (n == 0 or str(n).startswith("0."))
            ct = titles(ch); gt = titles(gh)
            title_raw = ct[0] if ct else ""; title_p = plain(title_raw)
            if "*" in html.unescape(TAG.sub("", title_raw)):
                sib.append({"code": code, "tmpl": tmpl, "page": os.path.basename(cp), "title": html.unescape(TAG.sub("", title_raw))[:120],
                            "gold_title": html.unescape(TAG.sub("", gt[0]))[:120] if gt else ""})
            hs = headings(body_of(ch))
            if not hs: continue
            free = [(r, b, l) for (r, b, l) in hs if not b]
            # the inbox class: the very first heading is boxed AND equals the title (ENGI101 'Being Frank') — KEEP, not a target
            if hs[0][1] and ladder(plain(hs[0][0]), title_p):
                inbox[tmpl] += 1
            if not free: continue
            fraw, _, flevel = free[0]; fp = plain(fraw)
            kind = ladder(fp, title_p)
            # also try each title half on a reoTranslate pair header (informational only — 07B excludes the template)
            if not kind and bil and len(ct) > 1: kind = ladder(fp, plain(ct[1]))
            # later repeats (informational): any free heading after the first equal to the title
            for r, _, _ in free[1:]:
                if ladder(plain(r), title_p): later[tmpl] += 1; break
            if not kind: continue
            gbody = body_of(gh); gheads = [plain(r) for r, _, _ in headings(gbody)]
            gfree = [plain(r) for r, b, _ in headings(gbody) if not b]
            gold_has = "same" if any(punct(x) == punct(fp) for x in gheads) else "absent"
            gold_first_dup = bool(gfree) and ladder(gfree[0], plain(gt[0]) if gt else "") is not None
            excluded = "07B" if bil else ("overview" if overview else "")
            row = {"code": code, "tmpl": tmpl, "subj": subj, "page": os.path.basename(cp), "gold": os.path.basename(hp), "overview": overview,
                   "bilingual": bil, "excluded": excluded, "level": flevel, "heading": fp[:120], "title": title_p[:120],
                   "gold_title": plain(gt[0])[:120] if gt else "", "kind": kind, "gold_has": gold_has, "gold_first_is_dup": gold_first_dup}
            rows.append(row)
            if excluded: C[("excluded-" + excluded, kind, gold_has)] += 1; continue
            C[("target", kind, gold_has)] += 1; byT[tmpl][kind + "/" + gold_has] += 1; byS[subj][gold_has] += 1
            affected.add(code)
    tgt = [r for r in rows if not r["excluded"]]
    summary = {"population": "all" if scan_all else "gate_mods", "modules": len(codes), "pages_scanned": npages,
               "target_pages": len(tgt), "target_modules": len(set(r["code"] for r in tgt)),
               "target_gold_absent(gain)": sum(1 for r in tgt if r["gold_has"] == "absent"),
               "target_gold_kept(named override)": sum(1 for r in tgt if r["gold_has"] == "same"),
               "by_kind_gold": {" | ".join(k): v for k, v in sorted(C.items())},
               "by_template": {k: dict(v) for k, v in byT.items()}, "by_subject": {k: dict(v) for k, v in sorted(byS.items())},
               "later_repeats_not_target(by tmpl)": dict(later), "inbox_first_heading_equal_title_KEEP(by tmpl)": dict(inbox),
               "sibling_titles_with_markers": len(sib), "sibling_modules": len(set(s["code"] for s in sib))}
    json.dump({"summary": summary, "rows": rows, "sibling": sib}, open(os.path.join(HERE, "_r344_c47.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    if scan_all:
        open(os.path.join(HERE, "_affected_r344.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(sorted(affected)) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
