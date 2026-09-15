#!/usr/bin/env python3
"""_measure_r330_sectionid.py — ROUND 330 (loop session 5, Round 1) measurement probe: the writer's
BARE SECTION-ID heading (`[H1] 1.1` / `[H1] 2.3` — a numbered section label with no words) in the
Bilingual / MTK Writers Templates, and what each side of the corpus does with it.

KB 07B (MTK content patterns, "Activity Structure"): the section's activity box carries the id as its
`number` attribute in DECIMAL form (`<div class="activity" number="1.1">`); the id is never a heading.

WHAT IT MEASURES (every gold module dir — all 454 — reading the Writers Template .docx DIRECTLY,
because 13 TRR modules ship no parsed WT text; the combined "Writers Template + Media List.docx"
files are included, the Media-List-only docx excluded):
  * per module: the bare section ids the writer wrote (`[H1] N.M`, `[H2] N.M`, or an untagged bare
    `N.M` cell/paragraph), grouped by template folder and subject family;
  * gold: activity boxes carrying number="N.M" (decimal) / number="NL" (letter) / no number; any
    heading whose whole text is a bare N.M (the phantom form);
  * Claude: the same counts — the phantom `<hN>N.M</hN>` headings and the activity boxes' number
    attributes; per page, for the pairing the skeleton gate uses.
Paths are dynamic (CLAUDE.md §13). Run from anywhere:  python3 _measure_r330_sectionid.py
Writes _r330_sectionid.json next to itself and prints the summary.
"""
import os, re, sys, json, zipfile, collections
from xml.etree import ElementTree as ET
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests"))
sys.path.insert(0, TESTS)
import _corpus
from anchor_compare import CLAUDE, HUMAN

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
SECID_TAGGED = re.compile(r"^\s*\[(H[1-4])\]\s*(\d{1,2}\.\d{1,2})\s*[:.]?\s*$", re.I)
SECID_BARE = re.compile(r"^\s*(\d{1,2}\.\d{1,2})\s*[:.]?\s*$")
ACT = re.compile(r'<div class="([^"]*\bactivity\b[^"]*)"([^>]*)>')
NUM = re.compile(r'number="([^"]*)"')
HEAD = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1>", re.S)
TAG = re.compile(r"<[^>]+>")


def docx_lines(path):
    """Paragraph texts in body order; table cells contribute one line per cell paragraph."""
    try:
        z = zipfile.ZipFile(path)
        root = ET.fromstring(z.read("word/document.xml"))
    except Exception:
        return []
    out = []
    for p in root.iter(W + "p"):
        out.append("".join(t.text or "" for t in p.iter(W + "t")))
    return out


def wt_docx(gdir):
    names = [f for f in os.listdir(gdir) if f.lower().endswith(".docx") and not f.startswith("~$")]
    keep = []
    for f in names:
        low = f.lower()
        if "media list" in low and "writers template" not in low and "writer's template" not in low:
            continue                      # Media-List-only docx
        keep.append(os.path.join(gdir, f))
    return keep


def page_facts(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    acts = []
    for m in ACT.finditer(s):
        n = NUM.search(m.group(2))
        acts.append(n.group(1) if n else None)
    phantom = []
    # body headings only (h2-h6 after the header block) — the header's <h1>1.0</h1> lesson number is not a section id
    body = s.split('<div id="body"', 1)[1] if '<div id="body"' in s else s
    for m in HEAD.finditer(body):
        t = re.sub(r"\s+", " ", TAG.sub("", m.group(2))).strip()
        if m.group(1) != "1" and SECID_BARE.match(t):
            phantom.append((m.group(1), t))
    return {"activities": acts, "dec": sum(1 for a in acts if a and re.fullmatch(r"\d+\.\d+", a)),
            "let": sum(1 for a in acts if a and re.fullmatch(r"\d+[A-Za-z]", a)),
            "unnum": sum(1 for a in acts if not a), "phantom": phantom}


def main():
    rows = []
    by_tmpl = collections.defaultdict(lambda: collections.Counter())
    by_fam = collections.defaultdict(lambda: collections.Counter())
    codes = sorted(_corpus.mods(HUMAN))
    for code in codes:
        gdir = _corpus.mdir(HUMAN, code)
        if not gdir or not os.path.isdir(gdir):
            continue
        tmpl = os.path.basename(os.path.dirname(gdir))
        fam = re.match(r"[A-Za-z]+", code).group(0).upper()
        ids_tagged, ids_bare = [], []
        for d in wt_docx(gdir):
            for line in docx_lines(d):
                m = SECID_TAGGED.match(line)
                if m:
                    ids_tagged.append((m.group(1).upper(), m.group(2))); continue
                m = SECID_BARE.match(line)
                if m:
                    ids_bare.append(m.group(1))
        gold_pages = sorted(f for f in os.listdir(gdir) if f.lower().endswith(".html"))
        gold = {"pages": len(gold_pages), "dec": 0, "let": 0, "unnum": 0, "phantom": 0, "ids": []}
        for f in gold_pages:
            pf = page_facts(os.path.join(gdir, f))
            gold["dec"] += pf["dec"]; gold["let"] += pf["let"]; gold["unnum"] += pf["unnum"]
            gold["phantom"] += len(pf["phantom"])
            gold["ids"] += [a for a in pf["activities"] if a]
        cdir = _corpus.mdir(CLAUDE, code)
        claude = {"pages": 0, "dec": 0, "let": 0, "unnum": 0, "phantom": 0, "phantom_pages": [], "ids": []}
        if cdir and os.path.isdir(cdir):
            cpages = sorted(f for f in os.listdir(cdir) if f.lower().endswith(".html"))
            claude["pages"] = len(cpages)
            for f in cpages:
                pf = page_facts(os.path.join(cdir, f))
                claude["dec"] += pf["dec"]; claude["let"] += pf["let"]; claude["unnum"] += pf["unnum"]
                if pf["phantom"]:
                    claude["phantom"] += len(pf["phantom"]); claude["phantom_pages"].append([f, len(pf["phantom"])])
                claude["ids"] += [a for a in pf["activities"] if a]
        n_writer = len(ids_tagged)            # the TAGGED form is the signal; an untagged bare N.M is a maths decimal in Standard WTs
        if n_writer == 0 and claude["phantom"] == 0 and gold["dec"] == 0:
            continue
        # the writer's ids vs the gold's decimal numbers: how many writer ids appear as a gold number
        wset = {i for _, i in ids_tagged}
        gset = set(gold["ids"])
        row = {"code": code, "tmpl": tmpl, "fam": fam, "writer_tagged": ids_tagged, "writer_bare": ids_bare,
               "writer_n": n_writer, "writer_ids_in_gold_number": len(wset & gset), "writer_ids": sorted(wset),
               "gold": gold, "claude": claude}
        rows.append(row)
        c = by_tmpl[tmpl]; c["modules"] += 1; c["writer_ids"] += n_writer
        c["gold_dec"] += gold["dec"]; c["gold_let"] += gold["let"]; c["gold_unnum"] += gold["unnum"]; c["gold_phantom"] += gold["phantom"]
        c["claude_phantom"] += claude["phantom"]; c["claude_phantom_pages"] += len(claude["phantom_pages"])
        c["claude_dec"] += claude["dec"]; c["claude_let"] += claude["let"]; c["claude_unnum"] += claude["unnum"]
        if n_writer: c["modules_with_writer_ids"] += 1
        f_ = by_fam[fam]
        f_["modules"] += 1; f_["writer_ids"] += n_writer; f_["gold_dec"] += gold["dec"]; f_["gold_let"] += gold["let"]
        f_["claude_phantom"] += claude["phantom"]; f_["claude_phantom_pages"] += len(claude["phantom_pages"])
        f_["claude_unnum"] += claude["unnum"]
        if n_writer: f_["modules_with_writer_ids"] += 1
    out = {"rows": rows, "by_template": {k: dict(v) for k, v in by_tmpl.items()}, "by_family": {k: dict(v) for k, v in by_fam.items()}}
    json.dump(out, open(os.path.join(HERE, "_r330_sectionid.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"modules with a writer section-id, a gold decimal number or a Claude phantom heading: {len(rows)}")
    print("\nBY TEMPLATE FOLDER:")
    for k, v in sorted(by_tmpl.items()):
        print(f"  {k:14} " + " ".join(f"{a}={b}" for a, b in sorted(v.items())))
    print("\nBY SUBJECT FAMILY:")
    for k, v in sorted(by_fam.items()):
        print(f"  {k:8} " + " ".join(f"{a}={b}" for a, b in sorted(v.items())))
    print("\nPER MODULE (writer ids | gold dec/let/unnum/phantom | claude phantom(pages)/dec/let/unnum | writer ids found as a gold number):")
    for r in rows:
        g, c = r["gold"], r["claude"]
        print(f"  {r['code']:9} {r['tmpl']:12} writer={r['writer_n']:3} ({len(r['writer_tagged'])} tagged/{len(r['writer_bare'])} bare)"
              f" | gold {g['dec']:3}/{g['let']:3}/{g['unnum']:3}/{g['phantom']:2}"
              f" | claude ph {c['phantom']:3}({len(c['phantom_pages']):2}) {c['dec']:3}/{c['let']:3}/{c['unnum']:3}"
              f" | in-gold {r['writer_ids_in_gold_number']}/{len(r['writer_ids'])}")
    tot_ph = sum(r["claude"]["phantom"] for r in rows); tot_pp = sum(len(r["claude"]["phantom_pages"]) for r in rows)
    print(f"\nTOTAL Claude phantom section-id headings: {tot_ph} on {tot_pp} pages / {sum(1 for r in rows if r['claude']['phantom'])} modules")
    print("wrote _r330_sectionid.json")


if __name__ == "__main__":
    main()
