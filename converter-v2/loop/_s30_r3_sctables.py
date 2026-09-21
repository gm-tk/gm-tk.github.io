#!/usr/bin/env python3
"""Session 30 Round 3 PICK — the OTHER `[Self check]` + table shapes (the 58 non-letter tables): per site the table's dims,
whether it has red cells (an answer table → the gold's `typing` engine?) or none (Question | Model answer → the KB selfCheck),
the header row's text, and the module's gold widget classes on the same page family (typing / selfCheck / dropQuiz …).
Output: _s30_r3_sctables.out"""
import os, sys, re, glob
from collections import Counter, defaultdict
T = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests"
sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import HUMAN
RED = r"🔴\[RED TEXT\]|\[/RED TEXT\]🔴"
def main():
    rows = []; permod = defaultdict(Counter)
    for code in _corpus.mods(HUMAN):
        d = _corpus.mdir(HUMAN, code)
        gold_cls = Counter()
        for f in glob.glob(os.path.join(d, "*.html")):
            s = open(f, encoding="utf-8", errors="replace").read()
            for m in re.finditer(r'class="(typing|selfCheck|dropQuiz|radioQuiz|multiChoiceQuiz|bingo|wordSelect|dropDown|reorder|memoryGame)\b', s):
                gold_cls[m.group(1)] += 1
        for f in glob.glob(os.path.join(d, "*_parsed.txt")):
            lines = open(f, encoding="utf-8", errors="replace").read().split("\n")
            for i, ln in enumerate(lines):
                if not re.search(r"\[\s*self[\s-]?check", ln, re.I): continue
                j = next((k for k in range(i + 1, min(i + 5, len(lines))) if "TABLE" in lines[k] and "┌" in lines[k]), None)
                if j is None: continue
                cells = []; k = j + 1; nrows = 0
                while k < len(lines) and "END TABLE" not in lines[k]:
                    if lines[k].startswith("│"):
                        cells.append([c.strip() for c in lines[k][1:].split("║")]); nrows += 1
                    k += 1
                flat = [c for r in cells for c in r]
                plain = [re.sub(RED, "", c).strip() for c in flat]
                letters = all(len(c) <= 2 for c in plain if c)
                if letters: continue
                red = sum(1 for c in flat if "[RED TEXT]" in c)
                width = max(len(r) for r in cells) if cells else 0
                header = " | ".join(re.sub(RED, "", c).strip()[:18] for c in cells[0]) if cells else ""
                lead = re.sub(r"🔴\[RED TEXT\]\s*\[[^\]]*\]\s*", "", ln).replace("[/RED TEXT]🔴", "").strip()[:60]
                kind = "answer-table(red)" if red else "no-red"
                rows.append((code, nrows, width, red, kind, header, lead, dict(gold_cls)))
                permod[code][kind] += 1
    L = [f"non-letter [Self check] tables: {len(rows)} in {len(permod)} modules"]
    L.append("by kind: " + str(Counter(r[4] for r in rows)))
    L.append("by width: " + str(Counter(r[2] for r in rows).most_common()))
    L.append("per module: " + ", ".join(f"{c} {dict(v)}" for c, v in sorted(permod.items(), key=lambda kv: -sum(kv[1].values()))))
    for r in rows:
        L.append(f"  {r[0]:8s} {r[1]}x{r[2]} red={r[3]:2d} {r[4]:18s} hdr«{r[5][:60]}» lead«{r[6]}» gold={r[7]}")
    txt = "\n".join(L)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s30_r3_sctables.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt[:8000])
main()
