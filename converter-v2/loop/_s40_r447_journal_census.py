#!/usr/bin/env python3
"""Session 40 Round 1 (engine r447) — D13-5 THE JOURNAL BUTTON: the WIDENED census the decision asked for.

For every module with a gold dir AND a Claude dir, walk each parsed Writers Template line and find every
writer [Button]-family tag (the lexicon's button head, plus the alias spans [go to journal] / [journal button] /
[link to journal]). For each, take the label the engine would read — the in-bracket tail after the button head
(`[Button – go to learning journal]`) or the black text after the tag on the same line (`[Button] Learning journal.`)
— and classify it:
  journal-pure      the whole label names the journal ("Go to learning journal.", "Learning Journal", "Journal")
  journal-sentence  the label mentions the journal inside a longer instruction ("Complete activity 3A in your
                    learning journal", "Journal. Complete Activity 4E Reflection")
  excluded          download / upload / dropbox / a .docx or module-code document name (another button's job)
  r239              already caught by the r239 rule (label folds to "go to (your|the) journal")
  not-journal       no journal word at all (ignored)
Also counts per module the gold's h4.goJournal and green "…journal" buttons and Claude's, so the round can
name its override pages. Writes outputs/_s40_r447_journal_census.{json,log}.
"""
import os, io, re, sys, json, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reference", "tests"))
import _corpus
import _diff_miner as dm

RED = re.compile(r"\U0001F534\[RED TEXT\]|\[/RED TEXT\]\U0001F534")
SPAN = re.compile(r"\[([^\[\]\n]{0,200})\]")
BTN_HEAD = re.compile(r"^\s*(?:add\s+(?:a\s+)?)?(?:green\s+)?button\b\s*[:–—\-]?\s*(.*)$", re.I)
ALIAS = re.compile(r"^\s*(?:go to (?:your |the )?journals?|journal button|link to (?:your |the )?journal)\s*$", re.I)
R239 = re.compile(r"^go\s*to\s*(?:your\s+|the\s+)?journals?\s*[.!]*$", re.I)
JOURNAL = re.compile(r"\bjournals?\b", re.I)
EXCL = re.compile(r"\bdownload|\bupload|\bdropbox|\.docx\b|\bsubmit|\b[A-Z]{2,6}\d{2,4}\b|\bplease\b|\bcreate a link\b", re.I)
PURE = re.compile(r"^(?:go\s+to\s+)?(?:(?:your|the|my)\s+)?(?:(?:learning|reflection|reflective|online)\s+)?journals?\s*[.!:]*$", re.I)
H4 = re.compile(r'<h4 class="goJournal">', re.I)
GBTN = re.compile(r'<div class="button">[^<]*journal[^<]*</div>', re.I)

def labels_in_line(line):
    s = RED.sub("", line)
    out = []
    ms = list(SPAN.finditer(s))
    for k, m in enumerate(ms):
        inner = m.group(1)
        end = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        after = re.sub(r"\s+", " ", s[m.end():end].replace("*", "")).strip()
        if ALIAS.match(inner):
            out.append(("alias", inner.strip(), after))
            continue
        h = BTN_HEAD.match(inner)
        if not h:
            continue
        tail = h.group(1).strip()
        if re.match(r"^(?:–|—|-|:)", tail):
            tail = tail[1:].strip()
        out.append(("button", tail, after))
    return out

def classify(kind, tail, after):
    lbl = (tail or after or "").replace("*", "").strip()
    if kind == "alias":
        return "r239", lbl or tail
    if not lbl:
        return "bare", ""
    if not JOURNAL.search(lbl):
        return "not-journal", lbl
    if EXCL.search(lbl):
        return "excluded", lbl
    if R239.match(lbl) and not tail:
        return "r239", lbl
    if PURE.match(lbl):
        return "journal-pure", lbl
    return "journal-sentence", lbl

rows, examples = [], collections.defaultdict(list)
tot = collections.Counter()
for code in _corpus.mods(dm.CLAUDE):
    gdir = _corpus.mdir(dm.HUMAN, code); cdir = _corpus.mdir(dm.CLAUDE, code)
    if not os.path.isdir(gdir):
        continue
    c = collections.Counter()
    for f in sorted(glob.glob(os.path.join(gdir, "*_parsed.txt"))):
        for ln in io.open(f, encoding="utf-8", errors="replace"):
            for kind, tail, after in labels_in_line(ln):
                cat, lbl = classify(kind, tail, after)
                c[cat] += 1; tot[cat] += 1
                if cat not in ("not-journal", "bare") and len(examples[cat]) < 400:
                    examples[cat].append(f"{code}\t{'IN' if tail else 'AFTER'}\t{lbl[:140]}")
    def cnt(d, p):
        return sum(len(p.findall(io.open(x, encoding="utf-8", errors="replace").read())) for x in glob.glob(os.path.join(d, "*.html")))
    g_h4, g_btn = cnt(gdir, H4), cnt(gdir, GBTN)
    c_h4, c_btn = cnt(cdir, H4), cnt(cdir, GBTN)
    tdir = os.path.basename(os.path.dirname(gdir))
    rows.append(dict(module=code, template=tdir, gold_h4=g_h4, gold_btn=g_btn, claude_h4=c_h4, claude_btn=c_btn, **dict(c)))

log = []
log.append("D13-5 journal-button census (session 40, r447) — writer [Button]-family tags over every paired module's parsed WT")
log.append("totals by class: " + ", ".join(f"{k} {v}" for k, v in tot.most_common()))
tgt = [r for r in rows if r.get("journal-pure", 0) + r.get("journal-sentence", 0) > 0]
log.append(f"modules with a NEW target (journal-pure or journal-sentence): {len(tgt)}; target tags: "
           f"{sum(r.get('journal-pure', 0) for r in tgt)} pure + {sum(r.get('journal-sentence', 0) for r in tgt)} sentence")
bt = collections.Counter(); bm = collections.Counter()
for r in tgt:
    bt[r["template"]] += r.get("journal-pure", 0) + r.get("journal-sentence", 0); bm[r["template"]] += 1
log.append("by template (tags / modules): " + ", ".join(f"{k} {bt[k]} / {bm[k]}" for k in sorted(bt)))
gh = sum(1 for r in tgt if r["gold_h4"] and not r["gold_btn"]); gb = sum(1 for r in tgt if r["gold_btn"] and not r["gold_h4"])
gboth = sum(1 for r in tgt if r["gold_btn"] and r["gold_h4"]); gnone = sum(1 for r in tgt if not r["gold_btn"] and not r["gold_h4"])
log.append(f"gold form on the target modules: h4-only {gh}, green-button-only {gb}, both {gboth}, neither {gnone} "
           "(the green-button golds are the D13-5 NAMED OVERRIDE — Chris chose r239's h4 form)")
log.append("")
log.append("module        template      pure sent excl r239 | gold h4 btn | claude h4 btn")
for r in sorted(tgt, key=lambda r: -(r.get("journal-pure", 0) + r.get("journal-sentence", 0))):
    log.append(f"{r['module']:<13} {r['template']:<13} {r.get('journal-pure',0):>4} {r.get('journal-sentence',0):>4} "
               f"{r.get('excluded',0):>4} {r.get('r239',0):>4} | {r['gold_h4']:>7} {r['gold_btn']:>3} | {r['claude_h4']:>9} {r['claude_btn']:>3}")
for cat in ("journal-pure", "journal-sentence", "excluded", "r239"):
    log.append("")
    log.append(f"== {cat}: label forms (count, label)")
    lc = collections.Counter(e.split("\t", 2)[1] + " " + e.split("\t", 2)[2] for e in examples[cat])
    for k, v in lc.most_common(60):
        log.append(f"  {v:>3}  {k}")
io.open(os.path.join(HERE, "_s40_r447_journal_census.log"), "w", encoding="utf-8", newline="").write("\n".join(log) + "\n")
json.dump(dict(totals=tot, rows=rows, examples=examples), io.open(os.path.join(HERE, "_s40_r447_journal_census.json"), "w", encoding="utf-8", newline=""), indent=1)
print("\n".join(log[:6]))
