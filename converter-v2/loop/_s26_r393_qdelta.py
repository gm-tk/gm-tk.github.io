#!/usr/bin/env python3
"""r392 queue delta: CANDIDATE rows of the pre-r392 DIFF_QUEUE vs the re-mined one, keyed (region, dir, parent, gold, claude)."""
import re, sys
def rows(p):
    out = {}
    for l in open(p, encoding="utf-8"):
        if not l.startswith("| #") and re.match(r"\| \d+ \|", l) and "CANDIDATE" in l:
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) >= 13:
                out[(c[1], c[2], c[3], c[4], c[5])] = (c[0], c[6], c[7])
    return out
a = rows("_diff_queue_pre_r393.md"); b = rows("../../DIFF_QUEUE.md")
new = sorted(set(b) - set(a)); gone = sorted(set(a) - set(b))
print(f"CANDIDATE rows pre {len(a)} / post {len(b)}; new {[(k, b[k]) for k in new]} / gone {[(k, a[k]) for k in gone]}")
