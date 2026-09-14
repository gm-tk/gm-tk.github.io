#!/usr/bin/env python3
"""ROUND 0b (LOOP__Autonomous_Rounds.md §1c) — THE KB AMALGAMATION FACTS.

The corpus facts behind `KB_AMALGAMATION_STATUS.md`: for every front-facing knowledge-base rule
that leaves a checkable signature in a finished page, count how many gold pages and how many
Claude pages carry it (so a rule's status — CAPTURED-LIVE / CAPTURED-INERT / NOT CAPTURED — rests
on the output, not on the changelog's word), and size every rule's SCOPE from the Writers
Templates (how many modules the rule can touch at all). Diagnostic only: reads the corpus, moves
no gate, changes no output. Writes `outputs/_r0b_kbfacts.json` and prints the summary table.

USAGE:  python3 _measure_r0b_kbstatus.py [--json OUT]
"""
import os, sys, re, json, time
from html.parser import HTMLParser
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(BASE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, pkey

HUMAN = os.path.join(ROOT, "01-Finalized_Modules_")
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
DATA = os.path.join(ROOT, "CONVERTER_V2", "data")
OUT = os.path.join(BASE, "_r0b_kbfacts.json")

VOID = {"img", "br", "input", "col", "hr", "meta", "link", "source", "area", "base", "wbr"}
LAZY_HOSTS = {"carousel", "flipCard", "dragAndDrop", "clickDrop", "memoryGame", "rotateBanner",
              "bannerContainer", "canvasContainer"}
SKIP_PAGE = re.compile(r"acks|acknowledge|glossary|references", re.I)


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


class Tree(HTMLParser):
    """Ancestor-aware facts: lazy images inside moving widgets; the first column class inside
    each activity wrapper; div.button / div.externalButton labels."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.img_in_host = 0
        self.lazy_in_host = 0
        self.lazy_total = 0
        self.activity_inner = []
        self.buttons = []
        self.ext_buttons = []
        self._btn = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get("class") or "").split())
        in_host = bool(cls & LAZY_HOSTS) or any(f["cls"] & LAZY_HOSTS for f in self.stack)
        if tag == "img":
            lazy = a.get("loading") == "lazy"
            self.lazy_total += lazy
            if in_host:
                self.img_in_host += 1
                self.lazy_in_host += lazy
            return
        if tag in VOID:
            return
        if tag == "div" and any(c.startswith("col") for c in cls):
            for f in reversed(self.stack):
                if f["act"]:
                    if not f["col_found"]:
                        f["col_found"] = True
                        self.activity_inner.append(" ".join(sorted(c for c in cls if c.startswith("col"))))
                    break
        frame = {"tag": tag, "cls": cls, "act": "activity" in cls, "col_found": False,
                 "btn": ("button" in cls or "externalButton" in cls), "ext": "externalButton" in cls, "txt": []}
        self.stack.append(frame)

    def handle_data(self, d):
        for f in reversed(self.stack):
            if f["btn"]:
                f["txt"].append(d)
                break

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                for f in self.stack[i:]:
                    if f["btn"]:
                        t = re.sub(r"\s+", " ", "".join(f["txt"])).strip()
                        (self.ext_buttons if f["ext"] else self.buttons).append(t)
                del self.stack[i:]
                break


def page_facts(path):
    raw = read(path)
    hs = raw.find('id="header"')
    bs = raw.find('id="body"')
    fs = raw.find('id="footer"')
    header = raw[hs:bs] if (hs >= 0 and bs > hs) else ""
    # the footer NAV only — the acknowledgements block sits AFTER the footer and its source
    # links must not count as footer anchors (the first cut counted them: 513 gold pages)
    fm = re.search(r"<ul\b[^>]*class=\"[^\"]*footer-nav[^\"]*\"[^>]*>(.*?)</ul>", raw[fs:] if fs >= 0 else "", re.S | re.I)
    footer = fm.group(1) if fm else ""
    acks_cls = re.search(r'<div class="(acks[^"]*)"', raw)
    htm = re.search(r"<html\b[^>]*>", raw[:3000], re.I)
    html_tag = htm.group(0) if htm else ""
    h1s = [strip_tags(m) for m in re.findall(r"<h1\b[^>]*>(.*?)</h1>", header, re.S | re.I)]
    h1_spans = [strip_tags(m) for m in re.findall(r"<h1\b[^>]*>\s*<span[^>]*>(.*?)</span>\s*</h1>", header, re.S | re.I)]
    t = Tree()
    try:
        t.feed(re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I))
    except Exception:
        pass
    acts = re.split(r'<div class="activity', raw)[1:]
    quiz_shells = 0
    quiz_shells_with_content = 0
    for chunk in acts:
        head = chunk.split('<div class="activity', 1)[0]
        if "Go to quiz" in head:
            quiz_shells += 1
            if re.search(r"<(ol|ul)\b|mcq|dropQuiz|radioQuiz", head):
                quiz_shells_with_content += 1
    body_h = re.findall(r"<h([2-6])\b[^>]*>(.*?)</h\1>", raw[bs:fs] if (bs >= 0 and fs > bs) else raw, re.S | re.I)
    body_h_texts = [strip_tags(x[1]) for x in body_h]
    return {
        "has_body": bool(re.search(r"<body\b", raw, re.I)),
        "body_class": (re.search(r"<body\b[^>]*class=\"([^\"]*)\"", raw, re.I) or [None, ""])[1] if re.search(r"<body\b[^>]*class=", raw, re.I) else "",
        "template_attr": (re.search(r'template="([^"]*)"', html_tag) or [None, ""])[1] if 'template="' in html_tag else "",
        "learning_support": "learningSupport" in html_tag,
        "h1s": h1s, "h1_spans": h1_spans,
        "footer_hrefs_nonempty": sum(1 for h in re.findall(r"<a\b[^>]*href=\"([^\"]*)\"", footer) if h.strip()),
        "footer_anchors": len(re.findall(r"<a\b[^>]*href=", footer)),
        "acks_typed": len(re.findall(r"every effort has been made|parts of this resource were created|currentYear", raw, re.I)),
        "acks_template_cls": bool(re.search(r'class="acks[^"]*acksTemplate', raw)),
        "acks_present": 'class="acks' in raw,
        "acks_cls": acks_cls.group(1) if acks_cls else "",
        "buttons_trailing_period": len(re.findall(r'<div class="(?:button|externalButton)">[^<]*\.\s*</div>', raw)),
        "lang_cls": dict(Counter(re.findall(r'class="[^"]*\b(jp-text|ch-text|pinyin)\b', raw))),
        "cjk_chars": len(re.findall(r"[぀-ヿ一-鿿]", raw)),
        "img_in_host": t.img_in_host, "lazy_in_host": t.lazy_in_host, "lazy_total": t.lazy_total,
        "activity_inner": t.activity_inner,
        "buttons": t.buttons, "ext_buttons": t.ext_buttons,
        "go_to_quiz": raw.count("Go to quiz"), "quiz_shells": quiz_shells, "quiz_shells_with_content": quiz_shells_with_content,
        "supervisor_new": raw.count("super-content-button"), "supervisor_legacy": raw.count("supervisorContainer"),
        "embed_pdf_new": raw.count('class="embedPDF"'), "embed_pdf_generic": raw.count("embed-responsive"),
        "ai_guidelines_old_name": raw.count("Suspected use in Assessments for Years"),
        "red_notes": len(re.findall(r"color:\s*red", raw, re.I)),
        "body_headings": body_h_texts,
        "col8_in_col8": len(re.findall(r'class="col-md-8 col-12"[^<]*<div class="row"[^<]*<div class="col-md-8 col-12"', raw)),
        "col10_activity": len(re.findall(r'<div class="col-md-10[^"]*">\s*<div class="activity', raw)),
    }


def wt_facts(code):
    d = _corpus.mdir(HUMAN, code)
    pf = sorted(f for f in os.listdir(d) if f.endswith("_parsed.txt")) if os.path.isdir(d) else []
    if not pf:
        return None
    txt = read(os.path.join(d, pf[0]))
    tb = [ln for ln in txt.splitlines() if re.search(r"\[\s*(H1 )?TITLE BAR\s*\]", ln, re.I)]
    return {
        "mtkquiz": bool(re.search(r"\[\s*mtk\s*quiz", txt, re.I)),
        "ai_guidelines": bool(re.search(r"AI (Use )?Guide", txt)),
        "fundamental_label": bool(re.search(r"FUNdamental\s*:", txt)),
        "lesson_n_h2": len(re.findall(r"\[H2\][^\n]*\bLesson \d", txt)),
        "external_link": len(re.findall(r"\[\s*external link", txt, re.I)),
        "title_bar_two_pipes": any(ln.count("|") >= 2 for ln in tb),
        "supervisor": bool(re.search(r"\[\s*supervisor", txt, re.I)),
        "lesson_overview_tag": bool(re.search(r"\[\s*lesson overview\s*\]", txt, re.I)),
        "emoji": bool(re.search(r"[\U0001F300-\U0001FAFF☀-➿]", txt)),
        "cjk": bool(re.search(r"[぀-ヿ一-鿿]", txt)),
        "audiovisual": bool(re.search(r"\[\s*audiovisual package", txt, re.I)),
        "dropbox": bool(re.search(r"dropbox", txt, re.I)),
        "istock_dual_id": len(re.findall(r"gm\d+-\d+", txt)),
        "captions": len(re.findall(r"\[\s*caption", txt, re.I)),
        "pages_tag": len(re.findall(r"\[\s*(LESSON|End page)", txt, re.I)),
    }


def main():
    args = sys.argv[1:]
    out = OUT
    if "--json" in args:
        out = args[args.index("--json") + 1]
    t0 = time.time()
    meta = {}
    try:
        meta = json.load(open(os.path.join(DATA, "Module_Structure_Index.json"), encoding="utf-8")).get("module_meta", {})
    except Exception:
        pass
    codes = _corpus.mods(HUMAN)
    gold, claude, wt = {}, {}, {}
    lesson_title = {"paired_lesson_pages": 0, "claude_title_matches_gold": 0, "claude_title_is_module_title": 0,
                    "gold_title_is_module_title": 0, "claude_dual_h1": 0, "gold_dual_h1": 0,
                    "claude_has_lesson_prefix": 0, "gold_has_lesson_prefix": 0, "claude_empty_title": 0,
                    "mismatch_samples": []}
    for i, code in enumerate(codes):
        hdir, cdir = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
        wt[code] = wt_facts(code)
        gp = {f: page_facts(os.path.join(hdir, f)) for f in sorted(os.listdir(hdir)) if f.lower().endswith(".html") and not SKIP_PAGE.search(f)}
        gold[code] = gp
        if os.path.isdir(cdir):
            cp = {f: page_facts(os.path.join(cdir, f)) for f in sorted(os.listdir(cdir)) if f.lower().endswith(".html") and not SKIP_PAGE.search(f)}
            claude[code] = cp
            # constraint 79: lesson page <h1><span> = the lesson's own title
            ov_g = next((gp[f] for f in gp if pkey(f, code) == 0.0), None)
            module_title = (ov_g["h1_spans"][0].lower() if ov_g and ov_g["h1_spans"] else None)
            for _, cpath, hpath in pairs(code):
                cb, hb = os.path.basename(cpath), os.path.basename(hpath)
                if cb not in cp or hb not in gp or pkey(hb, code) == 0.0:
                    continue
                g, c = gp[hb], cp[cb]
                if not g["h1_spans"] or not c["h1_spans"]:
                    continue
                lesson_title["paired_lesson_pages"] += 1
                gt, ct = g["h1_spans"][0].lower(), c["h1_spans"][0].lower()
                if gt == ct:
                    lesson_title["claude_title_matches_gold"] += 1
                if module_title and ct == module_title:
                    lesson_title["claude_title_is_module_title"] += 1
                if module_title and gt == module_title:
                    lesson_title["gold_title_is_module_title"] += 1
                if len(c["h1_spans"]) >= 2:
                    lesson_title["claude_dual_h1"] += 1
                if len(g["h1_spans"]) >= 2:
                    lesson_title["gold_dual_h1"] += 1
                if re.match(r"lesson \d", ct):
                    lesson_title["claude_has_lesson_prefix"] += 1
                if re.match(r"lesson \d", gt):
                    lesson_title["gold_has_lesson_prefix"] += 1
                if not ct.strip():
                    lesson_title["claude_empty_title"] += 1
                if gt != ct and len(lesson_title["mismatch_samples"]) < 60 and (i % 7 == 0):
                    lesson_title["mismatch_samples"].append({"module": code, "gold_page": hb, "claude_page": cb,
                                                             "gold": g["h1_spans"][:2], "claude": c["h1_spans"][:2],
                                                             "gold_h1s": g["h1s"][:3], "claude_h1s": c["h1s"][:3]})
        if (i + 1) % 50 == 0:
            print(f"  … {i + 1}/{len(codes)} modules {time.time() - t0:.0f}s", file=sys.stderr, flush=True)

    def agg(side):
        pages = [p for m in side.values() for p in m.values()]
        mods = len(side)
        ai = Counter(x for p in pages for x in p["activity_inner"])
        btn = Counter(b for p in pages for b in p["buttons"])
        ext = Counter(b for p in pages for b in p["ext_buttons"])
        xmods = {m: v for m, v in side.items() if m.startswith("X")}
        cjk_pages = [p for p in pages if p["cjk_chars"] > 0]
        return {
            "modules": mods, "pages": len(pages),
            "pages_missing_body_tag": sum(1 for p in pages if not p["has_body"]),
            "pages_footer_hrefs_nonempty": sum(1 for p in pages if p["footer_hrefs_nonempty"]),
            "footer_anchors_nonempty": sum(p["footer_hrefs_nonempty"] for p in pages),
            "footer_anchors": sum(p["footer_anchors"] for p in pages),
            "pages_acks_present": sum(1 for p in pages if p["acks_present"]),
            "pages_acks_template_cls": sum(1 for p in pages if p["acks_template_cls"]),
            "pages_acks_typed_statements": sum(1 for p in pages if p["acks_typed"]),
            "acks_wrapper_classes": dict(Counter(p["acks_cls"] for p in pages if p["acks_cls"]).most_common(6)),
            "buttons_trailing_period": sum(p["buttons_trailing_period"] for p in pages),
            "x_modules": len(xmods),
            "x_pages": sum(len(v) for v in xmods.values()),
            "x_pages_learning_support": sum(1 for v in xmods.values() for p in v.values() if p["learning_support"]),
            "nonx_pages_learning_support": sum(1 for m, v in side.items() if not m.startswith("X") for p in v.values() if p["learning_support"]),
            "cjk_pages": len(cjk_pages),
            "cjk_pages_with_lang_cls": sum(1 for p in cjk_pages if p["lang_cls"]),
            "lang_cls_spans": dict(sum((Counter(p["lang_cls"]) for p in pages), Counter())),
            "img_in_moving_hosts": sum(p["img_in_host"] for p in pages),
            "lazy_in_moving_hosts": sum(p["lazy_in_host"] for p in pages),
            "lazy_total": sum(p["lazy_total"] for p in pages),
            "activity_inner_col": dict(ai.most_common(8)),
            "activities_with_inner_col": sum(ai.values()),
            "button_labels_top": dict(btn.most_common(15)),
            "ext_button_count": sum(ext.values()),
            "ext_button_go_to_website": ext.get("Go to website", 0),
            "go_to_dropbox": btn.get("Go to dropbox", 0) + btn.get("Go to Dropbox", 0),
            "upload_to_dropbox": sum(v for k, v in btn.items() if k.lower().startswith("upload to dropbox")),
            "bare_dropbox": btn.get("Dropbox", 0),
            "go_to_quiz": sum(p["go_to_quiz"] for p in pages),
            "quiz_shells": sum(p["quiz_shells"] for p in pages),
            "quiz_shells_with_content": sum(p["quiz_shells_with_content"] for p in pages),
            "supervisor_new": sum(p["supervisor_new"] for p in pages),
            "supervisor_legacy": sum(p["supervisor_legacy"] for p in pages),
            "embed_pdf_new": sum(p["embed_pdf_new"] for p in pages),
            "embed_pdf_generic": sum(p["embed_pdf_generic"] for p in pages),
            "ai_guidelines_old_name": sum(p["ai_guidelines_old_name"] for p in pages),
            "col10_activity": sum(p["col10_activity"] for p in pages),
            "red_note_pages": sum(1 for p in pages if p["red_notes"]),
            "red_notes": sum(p["red_notes"] for p in pages),
            "template_attr": dict(Counter(p["template_attr"] for p in pages).most_common(8)),
            "body_class": dict(Counter(p["body_class"] for p in pages).most_common(8)),
        }

    wt_ok = {k: v for k, v in wt.items() if v}
    def wt_count(key, pred=bool):
        return sorted(k for k, v in wt_ok.items() if pred(v[key]))
    scope = {
        "modules_with_wt": len(wt_ok),
        "mtkquiz": wt_count("mtkquiz"), "ai_guidelines": wt_count("ai_guidelines"),
        "fundamental_label": wt_count("fundamental_label"), "lesson_n_h2": wt_count("lesson_n_h2"),
        "external_link": wt_count("external_link"), "title_bar_two_pipes": wt_count("title_bar_two_pipes"),
        "supervisor": wt_count("supervisor"), "lesson_overview_tag": wt_count("lesson_overview_tag"),
        "emoji": wt_count("emoji"), "cjk": wt_count("cjk"), "audiovisual": wt_count("audiovisual"),
        "dropbox": wt_count("dropbox"), "istock_dual_id": wt_count("istock_dual_id"), "captions": wt_count("captions"),
    }
    # KB family membership by prefix (scopes from Subject_Global_Parameters.json + KB 14)
    fam_prefixes = {
        "14.7 BLL": (["BLL"], ["BLLR"]), "14.9 BLLR": (["BLLR"], []), "14.10 MiW/WJ": (["WJ"], []),
        "14.5 H&PE FUNdamentals": (["HPFUN", "PHEFUN"], []), "14.8 HPE content": (["HES", "PHE", "PES", "HPE", "HPRE"], ["PHEFUN", "HPFUN"]),
        "14.6 LS": (["XLP", "XDLS", "XLS", "LS", "SLO", "SL"], []), "X-prefixed (c89)": (["X"], []),
        "14.1 Languages": (["CHFUN", "JPNFUN", "JAPFUN", "CHIFUN", "GE", "FR", "SPA", "SAM", "JPN", "CH"], ["CHFUN0"] and []),
        "14.2 Pathways": (["PWO", "PADO", "PATH", "PW"], []), "14.3 Taonga": (["ARFUN", "ARWHA", "ART", "ARTFUN", "TAO"], []),
        "14.4 CED P5": (["CEDT5", "CEDK5", "CEDO5", "CEDR5", "CEDW5", "CEDC5"], []), "14.12 Technology": (["TEFUN", "TECH"], []),
        "OSSC (c70)": (["OSSC"], []),
    }
    families = {}
    for fam, (inc, exc) in fam_prefixes.items():
        mods_ = sorted(c for c in codes if any(c.startswith(p) for p in inc) and not any(c.startswith(p) for p in exc))
        families[fam] = {"modules": len(mods_), "with_claude_dir": sum(1 for c in mods_ if c in claude),
                         "gold_pages": sum(len(gold.get(c, {})) for c in mods_),
                         "claude_pages": sum(len(claude.get(c, {})) for c in mods_), "codes": mods_}
    rep = {"meta": {"tool": "_measure_r0b_kbstatus.py", "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "gold_modules": len(gold), "claude_modules": len(claude), "seconds": round(time.time() - t0)},
           "gold": agg(gold), "claude": agg(claude), "lesson_title_c79": lesson_title,
           "scope_counts": {k: (v if isinstance(v, int) else len(v)) for k, v in scope.items()},
           "scope_modules": {k: v for k, v in scope.items() if isinstance(v, list)},
           "families": families}
    json.dump(rep, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    g, c = rep["gold"], rep["claude"]
    print(f"KB FACTS (round 0b) — gold {g['modules']} modules / {g['pages']} pages · Claude {c['modules']} / {c['pages']} · {rep['meta']['seconds']}s")
    keys = ["pages_missing_body_tag", "pages_footer_hrefs_nonempty", "pages_acks_present", "pages_acks_template_cls",
            "pages_acks_typed_statements", "buttons_trailing_period", "x_pages", "x_pages_learning_support", "nonx_pages_learning_support",
            "cjk_pages", "cjk_pages_with_lang_cls", "img_in_moving_hosts", "lazy_in_moving_hosts", "lazy_total",
            "activities_with_inner_col", "ext_button_count", "ext_button_go_to_website", "go_to_dropbox", "upload_to_dropbox",
            "bare_dropbox", "go_to_quiz", "quiz_shells", "quiz_shells_with_content", "supervisor_new", "supervisor_legacy",
            "embed_pdf_new", "embed_pdf_generic", "ai_guidelines_old_name", "col10_activity", "red_note_pages", "red_notes"]
    print(f"  {'fact':36} {'gold':>8} {'claude':>8}")
    for k in keys:
        print(f"  {k:36} {g[k]:>8} {c[k]:>8}")
    print("  activity inner col  gold:", g["activity_inner_col"])
    print("  activity inner col  claude:", c["activity_inner_col"])
    print("  lang classes gold:", g["lang_cls_spans"], " claude:", c["lang_cls_spans"])
    print("  template attr gold:", g["template_attr"]); print("  template attr claude:", c["template_attr"])
    print("  body class gold:", g["body_class"]); print("  body class claude:", c["body_class"])
    print("  button labels gold:", g["button_labels_top"]); print("  button labels claude:", c["button_labels_top"])
    print("  acks wrapper classes gold:", g["acks_wrapper_classes"]); print("  acks wrapper classes claude:", c["acks_wrapper_classes"])
    print("  lesson title (c79):", {k: v for k, v in lesson_title.items() if k != "mismatch_samples"})
    for s in lesson_title["mismatch_samples"][:30]:
        print(f"     {s['module']:9} {s['gold_page']:22} gold={s['gold']} | claude={s['claude']}")
    print("  WT scope counts:", rep["scope_counts"])
    print("  families:", {k: (v["modules"], v["with_claude_dir"], v["gold_pages"]) for k, v in families.items()})
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
