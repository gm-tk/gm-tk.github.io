#!/usr/bin/env python3
"""ROUND 348 (loop session 13 Round 1 — the 16 Sept review's two queued mechanical items) — finalise: changelog, AppVersion
(260619.18 → 260619.19), CLAUDE.md §9 / §14, gate_baseline.json _meta, loop/README.md rows, LOOP_STATE.md (what shipped +
position + round log). Idempotent; LF kept (the r343 pattern)."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

# ---------------------------------------------------------------- 1. BUILD_CHANGELOG.md
CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-16 (round 348, build 260619.19) — THE TWO VERIFIERS THAT PRINTED A RED RESULT AT THEIR OWN BASELINE NOW READ ✓ AT BASELINE AND ✗ ONLY ABOVE IT (speechBubble defect 4, math defect 1 — per-module baselines in `gate_baseline.json`), AND THE BATCH RUNNER'S OEMBED-CACHE WRITE RACE IS CLOSED (an atomic, merged, skip-when-clean save; a torn-tolerant read) — the 16 Sept `/loop-review`'s two queued mechanical items, pulled forward of D10-9 because the amended LOOP §3 step 6 ("a round may not ship while any RESULT line is red") would otherwise refuse the next ship; a TOOLING round — no engine or data change, no regeneration, gate-neutral by design

### 1. WHAT CHANGED, IN ONE LINE

**`_verify_speechbubble.cjs` and `_verify_math.cjs` read their recorded PER-MODULE baseline from `gate_baseline.json` (`speechbubble.per_module` = OSAI401 3 / OSAH501 1, the A/B-proven pre-existing defects of r313; `math.per_module` = PES1007 1, its pre-existing page-tail loss, identical with `MATHML_OFF`) and print `RESULT … ✓` when every module is at-or-under its baseline — naming the baseline, and "IMPROVED below baseline: refresh it" when under — and `RESULT: defects ABOVE the recorded baseline ✗` (exit code 1) ONLY when a module is above it; a module absent from the table has baseline 0.** For 34 rounds (speechBubble) and 2 rounds (math) the loop had read a red "fix before proceeding" as "at baseline" — the review named that as a state the loop must not learn to ignore. **And `batch_convert.cjs` no longer races itself:** the `oembed_cache.json` save was a plain `writeFileSync` (truncate + write) that EVERY worker ran at exit — even under `STUB_OEMBED=1`, when the cache is never consulted and nothing had changed — so under the 4-worker full-regeneration runners a worker starting up read a torn file and died in `JSON.parse` before converting anything (`_r347_batch_26.log`: "Unterminated string in JSON at position 114366"; ≈ 3 of 36 batches on every full regeneration r341 → r347, each re-run singly). Now the read tolerates a torn / corrupt file (warns, starts empty — it is only a cache), and the save is skipped when nothing changed, MERGES the file's current entries (a parallel worker's fetches are not lost) and is ATOMIC — a `.pid.tmp` renamed over the target, so a concurrent reader sees the old file or the new one, never a torn one.

### 2. THE SEAM (tooling only — `reference/tests/`, outside git, mirrored to `converter-v2/loop/`)

- `_verify_speechbubble.cjs`: `BASE = gate_baseline.json.speechbubble.per_module`; per module `base = BASE[mod] || 0`; the verdict is `OK ✓ (at the recorded baseline N)` when `0 < defect ≤ base`, `DEFECT ✗ (above the recorded baseline N)` above; `anyAbove` drives the RESULT line and `process.exitCode`. The per-module `defect N` lines, the per-defect `DEFECT (overlap …)` lines and the TOTAL line are UNCHANGED — they are the selftest's DETECTION signal (`_selftest_core.cjs` sums every `defect N`).
- `_verify_math.cjs`: the same shape (`BASE = gate_baseline.json.math.per_module`; `totAbove` = the sum of every module's excess over its baseline drives RESULT + `process.exit`).
- `batch_convert.cjs`: `readCache()` (try / catch → warn + `{}`), `saveCache()` (`if (!cacheDirty) return;` → merge `readCache()` under the in-memory map → write `${CACHE_FILE}.${pid}.tmp` → `renameSync` over the target → `cacheDirty = 0`).
- `gate_baseline.json`: `speechbubble.per_module {OSAI401: 3, OSAH501: 1}`, `math.per_module {PES1007: 1}` (+ `_note_r348` on each). Refresh a table when a defect is fixed (hold-or-improve, the verifier says "IMPROVED — refresh").
- The splice `outputs/_r348_splice.py` (idempotent; §6 atomic writes — encode first, temp file, `node --check`, `os.replace`).

### 3. THE PROOF (`outputs/_r348_verify_before.log` / `_r348_verify_after.log` / `_r348_cache_unit.log`)

- BEFORE: speechBubble gate set (OSAI501 OSAI401 OSAH501 ENGR101 OSGM501) `defect 4` → `RESULT: real defects present ✗` (rc 0 — it never set an exit code); math gate set (11 modules) `defect 1` → `✗` rc 1. AFTER, identical counts: speechBubble `TOTAL built 62 … defect 4` → **`RESULT: … or at its recorded baseline ✓ (4 recorded in gate_baseline.json.speechbubble)` rc 0**, OSAI401 `OK ✓ (at the recorded baseline 3)`, OSAH501 `OK ✓ (at the recorded baseline 1)`; math `TOTAL: 323 … <math> 322; defect 1` → **`RESULT: … or is at its recorded baseline ✓ (1 recorded in gate_baseline.json.math)` rc 0**, PES1007 `defect 1 ✓ (at the recorded baseline 1)`.
- DETECTION kept: both `--selftest` GREEN (speechBubble LIVENESS 8 on OSAH501, signal 2 → 4 injected; math LIVENESS 69 on MXDI301, signal 0 → 2). ABOVE-baseline proof: an injected malformed bubble on OSAH501 (baseline 1 → defect 2) prints `RESULT: defects ABOVE the recorded baseline ✗` rc 1; an injected lost `<math>` on PES1007 (baseline 1 → defect 2) the same, rc 1.
- The batch runner: a 2-module `--force` re-run (SCCH301 + MXDB202, `STUB_OEMBED=1`) against a pre-run copy — **byte-identical**, `oembed_cache.json` untouched (md5 e8655a8a…, no write when clean), no `.tmp` left. `_r348_cache_unit.cjs` runs the ACTUAL cache block (extracted from `batch_convert.cjs`, never a copy) against a scratch file: a torn file → empty map + one warning; clean → no write (bytes + mtime unchanged); dirty → the result parses, carries memory MERGED with the file's entries, no `.tmp` left, `cacheDirty` 0 — 5/5 PASS.
- **Gate-neutral by design:** no engine or data file changed; the corpus on disk is r347's byte-for-byte (nothing regenerated); every gate's numbers are the r347 baseline (`_check_index_sync.cjs` OK — 33 / 28). Outside the plateau window (LOOP §4: a gate-configuration round neither counts nor resets).

### 4. RECORDED

- The full gate suite's two RESULT lines are now honest at baseline; the next round that lowers either count must refresh the per-module table (the verifier says so). The next full regeneration should hit 0 race batches — record the count in that round's proof.

**Ledger:** no ship (no regeneration) · no data flag / env toggle (tooling) · gate tools (outside git, mirrored to `loop/`) `_verify_speechbubble.cjs`, `_verify_math.cjs`, `batch_convert.cjs`, `gate_baseline.json` · tools `outputs/_r348_splice.py`, `_r348_cache_unit.cjs` (+ `.log`), `_r348_verify_before.log`, `_r348_verify_after.log`, `_r348_finalise.py` · `_MIGRATION/CHECKSUMS__gates.txt` refreshed (backup `.pre-r348.bak`) · AppVersion 260619.19.

"""
if "round 348, build 260619.19" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

# ---------------------------------------------------------------- 2. Config.js
CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.18";' + chr(10)
NEW = ('\t// ROUND 348 (2026-09-16, build 260619.19): a TOOLING round, no engine change — _verify_speechbubble.cjs and' + chr(10) +
       '\t// _verify_math.cjs read their per-module baseline from gate_baseline.json (✓ at baseline, ✗ only above it; LOOP §3' + chr(10) +
       '\t// step 6); batch_convert.cjs\'s oembed-cache save is atomic + merged + skipped when clean (the 4-worker race closed).' + chr(10) +
       '\tstatic AppVersion = "260619.19";' + chr(10))
if '"260619.19"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

# ---------------------------------------------------------------- 3. CLAUDE.md §9 / §14
CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "Adjunct verifiers (run when you touch a widget): `_verify_math.cjs` (round 346"
NEW9 = ("**Round 348 — a verifier's RESULT line is ✓ AT its recorded baseline and ✗ ONLY above it (LOOP §3 step 6).** `_verify_speechbubble.cjs` and `_verify_math.cjs` read `gate_baseline.json` `speechbubble.per_module` (OSAI401 3, OSAH501 1) / `math.per_module` (PES1007 1); a module absent from the table has baseline 0; the per-module `defect N` lines and the TOTAL line are the selftest's DETECTION signal and never change meaning. When a round lowers a count the verifier prints \"IMPROVED — refresh gate_baseline.json\": do so in the finalise. A red RESULT is now always a real regression — no round ships on one. Also round 348: `batch_convert.cjs`'s `oembed_cache.json` save is atomic (tmp + rename), merged, and skipped when nothing changed; the read tolerates a torn file — the 4-worker full-regeneration race (≈ 3 of 36 batches, r341–r347) is closed.\n\n"
        + OLD9)
if "Round 348 — a verifier's RESULT line is ✓ AT its recorded baseline" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
B14 = ("- **Build:** `260619.19` (round 348 — **the two red-at-baseline verifiers read ✓ at baseline / ✗ only above it, and the batch runner's oembed-cache race is closed** (the 16 Sept `/loop-review`'s two queued mechanical items; a TOOLING round — no engine / data change, no regeneration, gate-neutral by design). `_verify_speechbubble.cjs` / `_verify_math.cjs` read `gate_baseline.json` `speechbubble.per_module` {OSAI401 3, OSAH501 1} / `math.per_module` {PES1007 1}: gate set counts unchanged (defect 4 / defect 1), RESULT ✓ rc 0; an injected above-baseline defect prints ✗ rc 1; both selftests GREEN. `batch_convert.cjs`: atomic + merged + skip-when-clean cache save, torn-tolerant read (`_r348_cache_unit.cjs` 5/5; a 2-module `--force` re-run byte-identical). **Every baseline = the r347 state** (SCAFFOLD 51.283% / ≥50 1074 / ≥75 198 / ≥90 15 @ 1955; RAW 35.409%; cs 11464/175/607; clean 2080/2103; leak 26/23; body 180; 14 selftests GREEN) = 55.8% of achievable. Corpus on disk unchanged: 2110 pages / 416 modules.\n")
if "- **Build:** `260619.19` (round 348" not in m:
    A = "- **Build:** `260619.18` (round 347 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

# ---------------------------------------------------------------- 4. gate_baseline.json _meta
GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
if "_round348_note" not in d["_meta"]:
    d["_meta"]["build"] = "260619.19"; d["_meta"]["round"] = 348; d["_meta"]["date"] = "2026-09-16"
    d["_meta"]["_round348_note"] = ("Round 348 (tooling: _verify_speechbubble.cjs / _verify_math.cjs read speechbubble.per_module / math.per_module and print ✓ at-or-under "
        "the baseline, ✗ only above it — LOOP §3 step 6; batch_convert.cjs oembed-cache save atomic + merged + skip-when-clean). No engine change, no regeneration: "
        "every number here is the r347 state. Refresh a per_module table when a round lowers a count (the verifier prints IMPROVED).")
    wr(GB, json.dumps(d, ensure_ascii=False) + (chr(10) if raw.endswith(chr(10)) else "")); print("gate_baseline.json _meta")

# ---------------------------------------------------------------- 5. loop/README.md rows
RM = os.path.join(PF, "loop", "README.md"); r = rd(RM)
ROW_ANCHOR = "| `_verify_math.cjs` / `run_all_gates.sh` / `_selftest_core.cjs` | `CONVERTER_V2/reference/tests/` | Session 12 Round 3"
NEWROWS = ("| `_verify_speechbubble.cjs` / `_verify_math.cjs` / `batch_convert.cjs` / `gate_baseline.json` | `CONVERTER_V2/reference/tests/` | Session 13 Round 1 (tooling round r348) — the two verifiers read their per-module baseline from `gate_baseline.json` (✓ at baseline, ✗ only above it — LOOP §3 step 6); the batch runner's oembed-cache save is atomic + merged + skip-when-clean and its read torn-tolerant (the 4-worker race closed); the gate tools are outside git, so these are the durable copies |\n"
           "| `_r348_splice.py` / `_r348_cache_unit.cjs` / `_r348_cache_unit.log` / `_r348_verify_before.log` / `_r348_verify_after.log` / `_r348_finalise.py` | `CONVERTER_V2/outputs/` | Session 13 Round 1 (r348) — the idempotent splice (§6 atomic writes), the cache-block unit test on the actual source text (5/5), the before / after verifier runs, the finalise |\n")
if "Session 13 Round 1 (tooling round r348)" not in r:
    assert r.count(ROW_ANCHOR) == 1, "README anchor"; r = r.replace(ROW_ANCHOR, NEWROWS + ROW_ANCHOR, 1); wr(RM, r); print("README rows")

# ---------------------------------------------------------------- 6. LOOP_STATE.md
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = chr(13) + chr(10) if chr(13) + chr(10) in s[:3000] else chr(10)
def L(t): return t.replace(chr(10), nl)
SEC = L("""## Session 13 · Round 1 (tooling round r348) — what shipped (the two red-at-baseline verifiers read ✓ at baseline; the batch runner's oembed-cache race closed)
- **Fix:** `_verify_speechbubble.cjs` / `_verify_math.cjs` read `gate_baseline.json` `speechbubble.per_module` {OSAI401 3, OSAH501 1} / `math.per_module`
  {PES1007 1} and print ✓ when every module is at-or-under its baseline (naming it; "IMPROVED — refresh" when under), ✗ + exit 1 ONLY above it; the
  per-module `defect N` / TOTAL lines (the selftest's DETECTION signal) unchanged. `batch_convert.cjs`: `readCache()` tolerates a torn file; `saveCache()`
  skips when clean, merges the file's entries, writes `.pid.tmp` + `renameSync` (atomic). Splice `outputs/_r348_splice.py` (idempotent, §6 atomic writes).
- **Proof:** gate-set counts unchanged (speechBubble defect 4, math defect 1) → RESULT ✓ rc 0 on both (`_r348_verify_after.log`); both `--selftest` GREEN
  (signals 2→4, 0→2); an injected above-baseline defect → ✗ rc 1 on both; 2-module `--force` re-run (SCCH301 + MXDB202) byte-identical, cache untouched;
  `_r348_cache_unit.cjs` 5/5 on the actual cache block. `_check_index_sync.cjs` OK.
- **No regeneration, no engine change** (AppVersion 260619.19 for the round ↔ build mapping). Every gate number = the r347 state (SCAFFOLD 51.283% = 55.8%
  of achievable, 1955 pairs). Gate tools mirrored to `converter-v2/loop/` (byte-identical), `_MIGRATION/CHECKSUMS__gates.txt` refreshed (backup
  `.pre-r348.bak`), `verify_after_transfer.sh` PASS.
- **The plateau window** ignores this round (gate-configuration, no PICK-predicted move); it stands at 1 of 3 (r347).

""")
ANCHOR = "## Session 13 · Round 1 PICK (gate-config / tooling round r348"
if "## Session 13 · Round 1 (tooling round r348) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = ("- Session 13 Round 1 (tooling round r348 — the two red-at-baseline verifiers read ✓ at their recorded per-module baseline / ✗ only above it; the batch runner's oembed-cache race closed; no engine change, no regeneration): **SHIPPED 2026-09-16 ≈21:50 (session 13)**. AppVersion 260619.19, CLAUDE.md §9/§14, `gate_baseline.json` per_module tables; every gate number = the r347 state." + nl)
if "- Session 13 Round 1 (tooling round r348" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P + OLD_P, 1); print("position")
OLD_R = "- review · `/loop-review` 2026-09-16 (no engine round)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = ("- s13-r1 (tooling r348) · `_verify_speechbubble.cjs` + `_verify_math.cjs` read their per-module baseline from `gate_baseline.json` (✓ at baseline / ✗ only above it — LOOP §3 step 6); `batch_convert.cjs` oembed-cache save atomic + merged + skip-when-clean, read torn-tolerant (the 4-worker race, ≈ 3 of 36 batches r341–r347, closed) · SHIPPED 2026-09-16 · no regeneration, no engine change · gate-neutral by design: every gate = the r347 state (scaffold 51.283%, 55.8% of achievable) · pages moved 0 · commit (see git log) · plateau window unchanged (1 of 3)" + nl)
if "- s13-r1 (tooling r348)" not in s:
    s = s[:i] + NEW_R + s[i:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
