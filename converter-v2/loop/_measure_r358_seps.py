#!/usr/bin/env python3
"""ROUND 358 PICK probe, part 2 (the r182 SOLIDIFY test) — WHEN A WRITER'S TITLE LINE CARRIES A NON-PIPE BILINGUAL
SEPARATOR, DOES THE HUMAN SPLIT IT INTO TWO <h1><span>?

For every paired page: the WT title line = the line that carries the gold's FIRST header h1 (else Claude's first h1)
under the round-110 test. On that line (tags / red marks / markdown stripped, a leading 'Lesson N' / module code stripped)
look for a candidate separator — ' – ', ' — ', ' - ', ' / ', ' | ', ': ' — that splits the text into two non-empty halves
of which EXACTLY ONE looks Māori (a macron, else the r321 alphabet test: only the letters a e i o u h k m n p r t w ng wh
plus macrons and spaces). Tally, per separator and per template / page type: candidate pages, gold split (h1 count ≥ 2
with the second h1 fold-equal to one half), gold glued (one h1 holding both halves), gold other; Claude split / glued.
Also the RAW separator census over every candidate line regardless of the Māori test (so a hyphen inside an English title
is visible as the reason a bare-separator rule would over-split).
Run from anywhere (WSL): python3 _measure_r358_seps.py -> _r358_seps.{json,log}
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
from _measure_ceiling import unorm, load_meta
from _measure_r358_titlepair import header_h1s, wt_lines, find_title_line, SKIP

meta = load_meta()
MACRON = re.compile(r"[āēīōūĀĒĪŌŪ]")
SEPS = [(" – ", r"\s[–—]\s"), (" - ", r"\s-\s"), (" / ", r"\s/\s"), (" | ", r"\s?\|\s?"), (": ", r":\s")]
RED = re.compile(r"\U0001f534\[RED TEXT\]|\[/RED TEXT\]\U0001f534|\[[^\]]*\]|\*+")


def looks_maori(s):
    t = unorm(s)
    if not t:
        return False
    if MACRON.search(s):
        return True
    letters = re.sub(r"[^a-zāēīōū]", "", t)
    if len(letters) < 3:
        return False
    # the Māori alphabet: a e i o u h k m n p r t w (ng, wh are digraphs of these)
    return re.fullmatch(r"[aeiouhkmnprtwāēīōū]+", letters) is not None


def clean_line(raw, code):
    s = RED.sub(" ", raw)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^(%s)\s*[\-–—:]?\s*" % re.escape(code), "", s, flags=re.I)
    s = re.sub(r"^lesson\s*\d+(\.\d+)?\s*[\-–—:.]?\s*", "", s, flags=re.I)
    s = re.sub(r"^(title|title bar|h1|h2)\s*[:\-–—]?\s*", "", s, flags=re.I)
    return s.strip(" -–—:|")


def split_candidate(text):
    """(sep, a, b, maori_side) for the FIRST separator that yields two non-empty halves; maori_side in {a, b, both, none}."""
    for name, rx in SEPS:
        m = re.search(rx, text)
        if not m:
            continue
        a, b = text[:m.start()].strip(" -–—:|"), text[m.end():].strip(" -–—:|")
        if not a or not b:
            continue
        ma, mb = looks_maori(a), looks_maori(b)
        side = "both" if (ma and mb) else ("a" if ma else ("b" if mb else "none"))
        return name, a, b, side
    return None


rows = []
codes = sorted(c for c in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, c)))
for code in codes:
    gdir = _corpus.mdir(HUMAN, code); tmpl = os.path.basename(os.path.dirname(gdir))
    subject = (meta.get(code) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or re.search(r"acks|acknowledge|glossary", os.path.basename(cp), re.I):
            continue
        ptype = "overview" if n == 0 else "lesson"
        g = header_h1s(open(hp, encoding="utf-8", errors="replace").read())
        c = header_h1s(open(cp, encoding="utf-8", errors="replace").read())
        first = (g[0]["text"] if g else "") or (c[0]["text"] if c else "")
        line = find_title_line(code, first) if first else None
        if not line:
            continue
        text = clean_line(line, code)
        cand = split_candidate(text)
        if not cand:
            continue
        sep, a, b, side = cand
        ga = [unorm(x["text"]) for x in g]; ca = [unorm(x["text"]) for x in c]
        ua, ub = unorm(a), unorm(b)

        def verdict(arr):
            if len(arr) >= 2 and (ua in arr or ub in arr) and not any(ua in x and ub in x for x in arr):
                return "split"
            if any(ua in x and ub in x for x in arr):
                return "glued"
            if len(arr) >= 2:
                return "two-other"
            return "one-other"
        rows.append({"module": code, "page": os.path.basename(cp), "template": tmpl, "subject": subject, "ptype": ptype,
                     "sep": sep, "a": a[:80], "b": b[:80], "maori_side": side, "gold": verdict(ga), "claude": verdict(ca),
                     "gold_h1": [x["text"][:60] for x in g], "claude_h1": [x["text"][:60] for x in c], "line": text[:160]})


def tally(rs, label):
    out = [f"{label}: {len(rs)} candidate pages / {len({r['module'] for r in rs})} modules"]
    for key in ("sep", "maori_side"):
        cnt = collections.defaultdict(collections.Counter)
        for r in rs:
            cnt[r[key]]["pages"] += 1; cnt[r[key]]["gold:" + r["gold"]] += 1; cnt[r[key]]["claude:" + r["claude"]] += 1
        for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]["pages"]):
            out.append(f"   {key}={k!r:8} " + " ".join(f"{a}={b}" for a, b in sorted(v.items())))
    return out


L = [f"r358 separator probe — {len(rows)} candidate title lines with a non-pipe / pipe separator, over the gate's pairs"]
one = [r for r in rows if r["maori_side"] in ("a", "b")]
L += tally(rows, "ALL candidates (any Māori side)")
L += tally(one, "EXACTLY ONE Māori half (the rule's trigger)")
L.append("")
L.append("EXACTLY-ONE-MĀORI by template / page type / separator: gold split vs glued")
cnt = collections.defaultdict(collections.Counter); mods = collections.defaultdict(set)
for r in one:
    k = f"{r['template']}/{r['ptype']}/{r['sep'].strip() or 'pipe'}"
    cnt[k]["pages"] += 1; cnt[k]["gold:" + r["gold"]] += 1; cnt[k]["claude:" + r["claude"]] += 1; mods[k].add(r["module"])
for k, v in sorted(cnt.items()):
    L.append(f"   {k:34} mods={len(mods[k]):3} " + " ".join(f"{a}={b}" for a, b in sorted(v.items())))
L.append("")
L.append("NON-PIPE, exactly-one-Māori pages where the gold SPLIT and Claude did not (the derivable class):")
cls = [r for r in one if r["sep"] != " | " and r["gold"] == "split" and r["claude"] != "split"]
L.append(f"   {len(cls)} pages / {len({r['module'] for r in cls})} modules: " + ", ".join(sorted({r['module'] for r in cls})))
for r in cls[:40]:
    L.append(f"   {r['module']:9} {r['page']:20} {r['template'][:4]}/{r['ptype'][:3]} sep={r['sep']!r} side={r['maori_side']} gold={r['gold_h1']} claude={r['claude_h1']} line«{r['line'][:90]}»")
L.append("")
L.append("NON-PIPE, exactly-one-Māori pages where the gold GLUED (the counter-evidence):")
ce = [r for r in one if r["sep"] != " | " and r["gold"] == "glued"]
L.append(f"   {len(ce)} pages / {len({r['module'] for r in ce})} modules")
for r in ce[:20]:
    L.append(f"   {r['module']:9} {r['page']:20} {r['template'][:4]}/{r['ptype'][:3]} sep={r['sep']!r} gold={r['gold_h1']} line«{r['line'][:90]}»")
L.append("")
L.append("BOTH-or-NONE Māori with a non-pipe separator (what a bare-separator rule would wrongly split):")
bn = [r for r in rows if r["maori_side"] in ("both", "none") and r["sep"] != " | "]
L.append(f"   {len(bn)} pages; gold split {sum(1 for r in bn if r['gold'] == 'split')} / glued {sum(1 for r in bn if r['gold'] == 'glued')} / other {sum(1 for r in bn if r['gold'] not in ('split', 'glued'))}")
for r in bn[:12]:
    L.append(f"   {r['module']:9} {r['page']:20} sep={r['sep']!r} side={r['maori_side']} gold={r['gold']} line«{r['line'][:90]}»")
open(os.path.join(HERE, "_r358_seps.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
json.dump(rows, open(os.path.join(HERE, "_r358_seps.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("\n".join(L[:14])); print(f"wrote _r358_seps.json / .log ({len(L)} lines)")
