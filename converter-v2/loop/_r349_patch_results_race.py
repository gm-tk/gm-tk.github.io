#!/usr/bin/env python3
"""ROUND 349 — patch 3 (found by this round's full regeneration, the first with the r348 oembed-cache fix in place): the SECOND
torn-read race in batch_convert.cjs — `batch_results.json` (4.5 MB) is read whole at startup and rewritten whole after EVERY
module by every worker (`writeFileSync` = truncate + write), so under 4 workers a starting worker reads a torn file and dies
("Unterminated string in JSON at position 4320808") — 4 of 36 batches at r349 (12 / 22 / 27 / 33); the r341–r347 "≈ 3 of 36"
were a mix of both files. Fix, the r348 shape: a torn-tolerant read (warn, start empty — it is a diagnostic ledger) and an
ATOMIC MERGED write (re-read the file, overlay this worker's entries, write `.pid.tmp`, `renameSync`). Idempotent; LF kept;
node --check before the move (§6)."""
import io, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.normpath(os.path.join(HERE, "..", "reference", "tests", "batch_convert.cjs"))
s = io.open(P, encoding="utf-8", newline="").read()
if "saveResults" in s: print("already patched"); raise SystemExit
A = "\tconst results = fs.existsSync(RESULTS) ? j(RESULTS) : {};\n"
B = "\t\tfs.writeFileSync(RESULTS, JSON.stringify(results, null, 1));\n"
assert s.count(A) == 1 and s.count(B) == 1
s = s.replace(A,
    "\t// ROUND 349: batch_results.json is the SECOND file the parallel workers race on (the r348 fix covered the oembed cache):\n"
    "\t// a torn-tolerant read (it is a diagnostic ledger — warn and start empty) and, below, an atomic MERGED write.\n"
    "\tconst readResults = () => { if (!fs.existsSync(RESULTS)) return {}; try { return j(RESULTS); } catch (e) { console.error(`batch_results.json unreadable (${e.message}) — starting empty`); return {}; } };\n"
    "\tconst results = readResults();\n"
    "\tconst saveResults = () => {\n"
    "\t\tconst merged = { ...readResults(), ...results };   // another worker's rows are kept; this worker's rows win\n"
    "\t\tconst tmp = `${RESULTS}.${process.pid}.tmp`;\n"
    "\t\tfs.writeFileSync(tmp, JSON.stringify(merged, null, 1));\n"
    "\t\tfs.renameSync(tmp, RESULTS);\n"
    "\t};\n", 1)
s = s.replace(B, "\t\tsaveResults();\n", 1)
b = s.encode("utf-8"); tmp = P[:-4] + ".r349tmp.cjs"
with open(tmp, "wb") as f: f.write(b)
r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True); assert r.returncode == 0, r.stderr
os.replace(tmp, P); print("batch_convert.cjs: results ledger read torn-tolerant, write atomic + merged")
