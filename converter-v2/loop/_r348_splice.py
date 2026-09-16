#!/usr/bin/env python3
"""ROUND 348 (loop session 13 Round 1 — the 16 Sept review's two queued mechanical items) — the splice.

(a) `_verify_speechbubble.cjs` + `_verify_math.cjs`: the RESULT line reads ✓ AT the recorded PER-MODULE baseline
    (`gate_baseline.json` `speechbubble.per_module` / `math.per_module`) and ✗ ONLY above it (exit code 1 only then).
    The per-module `defect N` lines and the TOTAL line — the selftest's DETECTION signal — are untouched.
(b) `batch_convert.cjs`: the oembed cache read tolerates a torn file; the save is atomic (tmp + rename), merges the
    file's current entries, and is skipped when nothing changed (under STUB_OEMBED it never wrote anything useful).
(c) `gate_baseline.json`: the two per-module tables.

Idempotent. LF kept. §6 atomic writes: encode first, write a temp file, `node --check` it, then move it over the original.
"""
import io, os, json, subprocess, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "reference", "tests")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def atomic_js(p, s):
    b = s.encode("utf-8")                       # encode FIRST (the r347 lesson)
    assert len(b) > 1000, "refusing to write a near-empty engine/tool file"
    tmp = p[:-4] + ".r348tmp.cjs"           # node --check needs the .cjs extension
    with open(tmp, "wb") as f: f.write(b)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode != 0:
        os.remove(tmp); sys.exit(f"node --check FAILED for {p}:\n{r.stderr}")
    os.replace(tmp, p)                      # atomic on the same volume; replaces an existing target on Windows too

# ------------------------------------------------------------------ (a1) _verify_speechbubble.cjs
P = os.path.join(T, "_verify_speechbubble.cjs"); s = rd(P); n0 = s
if "ROUND 348" not in s:
    A = 'const j = (p) => JSON.parse(fs.readFileSync(p, "utf8"));\n'
    assert s.count(A) == 1, "sb anchor 1"
    s = s.replace(A, A +
        '// ROUND 348 (the 16 Sept 2026 loop review, LOOP §3 step 6): the RESULT line reads ✓ AT the recorded PER-MODULE\n'
        '// baseline (gate_baseline.json.speechbubble.per_module — the A/B-proven pre-existing defects: OSAI401 3, OSAH501 1 at\n'
        '// r313) and ✗ ONLY above it; a module absent from the table has baseline 0. The per-module `defect N` lines and the\n'
        '// TOTAL line are UNCHANGED — they are the selftest\'s DETECTION signal (_selftest_core.cjs sums every `defect N`).\n'
        'const BASE = (() => { try { return j(path.join(__dirname, "gate_baseline.json")).speechbubble?.per_module || {}; } catch { return {}; } })();\n', 1)
    B = ('\t\tconst verdict = builtBubbles.length === 0 ? "no builds"\n'
         '\t\t\t: (defect.length === 0 ? "OK ✓ (built⊆human, modulo copy-edits / dev-rewrites / gold-subst)" : "DEFECT ✗");\n')
    assert s.count(B) == 1, "sb anchor 2"
    s = s.replace(B,
        '\t\tconst base = +(BASE[mod] || 0);   // ROUND 348: this module\'s recorded baseline (0 when unrecorded)\n'
        '\t\tconst verdict = builtBubbles.length === 0 ? "no builds"\n'
        '\t\t\t: defect.length === 0 ? "OK ✓ (built⊆human, modulo copy-edits / dev-rewrites / gold-subst)"\n'
        '\t\t\t: defect.length <= base ? `OK ✓ (at the recorded baseline ${base}${defect.length < base ? " — IMPROVED, refresh gate_baseline.json" : ""})`\n'
        '\t\t\t: `DEFECT ✗ (above the recorded baseline ${base})`;\n'
        '\t\tif (defect.length > base) anyAbove = true;\n'
        '\t\tif (defect.length && defect.length < base) improved = true;\n', 1)
    C = '\tlet anyDefect = false, totBuilt = 0,'
    assert s.count(C) == 1, "sb anchor 3"
    s = s.replace(C, '\tlet anyDefect = false, anyAbove = false, improved = false, totBuilt = 0,', 1)
    D = ('\tconsole.log(anyDefect ? "RESULT: real defects present ✗ — fix before proceeding."\n'
         '\t\t: "RESULT: every built bubble is human-matched or writer-faithful (gold-subst) ✓");\n')
    assert s.count(D) == 1, "sb anchor 4"
    s = s.replace(D,
        '\t// ROUND 348: ✓ at the recorded baseline, ✗ only above it (LOOP §3 step 6). anyDefect still says whether ANY defect\n'
        '\t// exists at all (the pre-r348 wording is kept as a parenthetical so a reader sees the baseline is not zero).\n'
        '\tconsole.log(anyAbove ? "RESULT: defects ABOVE the recorded baseline ✗ — fix before proceeding (gate_baseline.json.speechbubble.per_module)."\n'
        '\t\t: anyDefect ? `RESULT: every built bubble is human-matched, writer-faithful (gold-subst) or at its recorded baseline ✓ (${totDefect} recorded in gate_baseline.json.speechbubble${improved ? " — IMPROVED below baseline: refresh it" : ""})`\n'
        '\t\t: "RESULT: every built bubble is human-matched or writer-faithful (gold-subst) ✓");\n'
        '\tprocess.exitCode = anyAbove ? 1 : 0;\n', 1)
    atomic_js(P, s); print("_verify_speechbubble.cjs spliced")
else: print("_verify_speechbubble.cjs already spliced")

# ------------------------------------------------------------------ (a2) _verify_math.cjs
P = os.path.join(T, "_verify_math.cjs"); s = rd(P)
if "ROUND 348" not in s:
    A = 'const SENT = /[\\uE010\\uE011]/;\n'
    assert s.count(A) == 1, "math anchor 1"
    s = s.replace(A, A +
        '// ROUND 348 (the 16 Sept 2026 loop review, LOOP §3 step 6): ✓ AT the recorded PER-MODULE baseline\n'
        '// (gate_baseline.json.math.per_module — PES1007 1 = its pre-existing page-tail loss, identical with MATHML_OFF) and ✗\n'
        '// ONLY above it. The per-module `defect N` lines and the TOTAL line are unchanged (the selftest\'s DETECTION signal).\n'
        'const BASE = (() => { try { return JSON.parse(fs.readFileSync(path.join(__dirname, "gate_baseline.json"), "utf8")).math?.per_module || {}; } catch { return {}; } })();\n', 1)
    B = '\tlet totEq = 0, totMath = 0, totDefect = 0, mods = 0;\n'
    assert s.count(B) == 1, "math anchor 2"
    s = s.replace(B, '\tlet totEq = 0, totMath = 0, totDefect = 0, mods = 0, totAbove = 0, improved = false;\n', 1)
    C = ('\t\ttotEq += r.omath; totMath += math; totDefect += defect;\n'
         '\t\tconsole.log(`${mod}: equations ${r.omath} (registered ${r.registered}) / <math> ${math} on ${mathPages} page(s); ${TOKEN} missing ${noJax}; sentinel leaks ${leaks}; malformed ${bad}; defect ${defect}${defect ? " ✗" : " ✓"}`);\n')
    assert s.count(C) == 1, "math anchor 3"
    s = s.replace(C,
        '\t\tconst base = +(BASE[mod] || 0);   // ROUND 348: this module\'s recorded baseline (0 when unrecorded)\n'
        '\t\tif (defect > base) totAbove += defect - base;\n'
        '\t\tif (defect && defect < base) improved = true;\n'
        '\t\ttotEq += r.omath; totMath += math; totDefect += defect;\n'
        '\t\tconsole.log(`${mod}: equations ${r.omath} (registered ${r.registered}) / <math> ${math} on ${mathPages} page(s); ${TOKEN} missing ${noJax}; sentinel leaks ${leaks}; malformed ${bad}; defect ${defect}${defect > base ? ` ✗ (above the recorded baseline ${base})` : defect ? ` ✓ (at the recorded baseline ${base}${defect < base ? " — IMPROVED, refresh gate_baseline.json" : ""})` : " ✓"}`);\n', 1)
    D = ('\tconsole.log(totDefect ? "RESULT: real defects present ✗ — fix before proceeding." : "RESULT: every Word equation ships as MathML ✓");\n'
         '\tprocess.exit(totDefect ? 1 : 0);\n')
    assert s.count(D) == 1, "math anchor 4"
    s = s.replace(D,
        '\t// ROUND 348: ✓ at the recorded baseline, ✗ only above it (LOOP §3 step 6).\n'
        '\tconsole.log(totAbove ? "RESULT: defects ABOVE the recorded baseline ✗ — fix before proceeding (gate_baseline.json.math.per_module)."\n'
        '\t\t: totDefect ? `RESULT: every Word equation ships as MathML or is at its recorded baseline ✓ (${totDefect} recorded in gate_baseline.json.math${improved ? " — IMPROVED below baseline: refresh it" : ""})`\n'
        '\t\t: "RESULT: every Word equation ships as MathML ✓");\n'
        '\tprocess.exit(totAbove ? 1 : 0);\n', 1)
    atomic_js(P, s); print("_verify_math.cjs spliced")
else: print("_verify_math.cjs already spliced")

# ------------------------------------------------------------------ (b) batch_convert.cjs
P = os.path.join(T, "batch_convert.cjs"); s = rd(P)
if "ROUND 348" not in s:
    A = ('const oembedCache = new Map(fs.existsSync(CACHE_FILE) ? Object.entries(j(CACHE_FILE)) : []);\n'
         'let cacheDirty = 0;\n'
         'const saveCache = () => fs.writeFileSync(CACHE_FILE, JSON.stringify(Object.fromEntries(oembedCache)));\n')
    assert s.count(A) == 1, "batch anchor 1"
    s = s.replace(A,
        '// ROUND 348: parallel workers (the _r341+ full-regeneration runners, 4 at a time) SHARE this file. The old save was a\n'
        '// plain writeFileSync (truncate + write) that EVERY worker ran at exit — even under STUB_OEMBED, when the cache is never\n'
        '// consulted and nothing had changed — so a worker starting up read a torn file and died in JSON.parse before converting\n'
        '// anything (≈ 3 of 36 batches on every full regeneration r341–r347, each re-run singly). Now: the read tolerates a\n'
        '// torn / corrupt file (warn, start empty — it is only a cache); the save is skipped when nothing changed, merges the\n'
        '// file\'s current entries (a parallel worker\'s fetches are not lost), and is ATOMIC — a .pid.tmp renamed over the target,\n'
        '// so a concurrent reader sees the old file or the new one, never a torn one.\n'
        'const readCache = () => { if (!fs.existsSync(CACHE_FILE)) return {}; try { return j(CACHE_FILE); } catch (e) { console.error(`oembed cache unreadable (${e.message}) — starting empty`); return {}; } };\n'
        'const oembedCache = new Map(Object.entries(readCache()));\n'
        'let cacheDirty = 0;\n'
        'const saveCache = () => {\n'
        '\tif (!cacheDirty) return;\n'
        '\tconst merged = { ...readCache(), ...Object.fromEntries(oembedCache) };\n'
        '\tconst tmp = `${CACHE_FILE}.${process.pid}.tmp`;\n'
        '\tfs.writeFileSync(tmp, JSON.stringify(merged));\n'
        '\tfs.renameSync(tmp, CACHE_FILE);\n'
        '\tcacheDirty = 0;\n'
        '};\n', 1)
    atomic_js(P, s); print("batch_convert.cjs spliced")
else: print("batch_convert.cjs already spliced")

# ------------------------------------------------------------------ (c) gate_baseline.json
P = os.path.join(T, "gate_baseline.json"); raw = rd(P); d = json.loads(raw); changed = False
if "per_module" not in d["speechbubble"]:
    d["speechbubble"]["per_module"] = {"OSAI401": 3, "OSAH501": 1}
    d["speechbubble"]["_note_r348"] = ("Round 348: the verifier reads per_module and prints ✓ at-or-under it, ✗ only above (LOOP §3 step 6); "
                                       "a module absent here has baseline 0. Refresh when a defect is fixed (hold-or-improve).")
    changed = True
if "per_module" not in d["math"]:
    d["math"]["per_module"] = {"PES1007": 1}
    d["math"]["_note_r348"] = "Round 348: same rule as speechbubble.per_module — ✓ at-or-under, ✗ only above; refresh when PES1007's page-tail class ships."
    changed = True
if changed:
    with io.open(P, "w", encoding="utf-8", newline="") as f: f.write(json.dumps(d, ensure_ascii=False) + (chr(10) if raw.endswith(chr(10)) else ""))
    json.loads(rd(P)); print("gate_baseline.json per_module tables added")
else: print("gate_baseline.json already has per_module")
