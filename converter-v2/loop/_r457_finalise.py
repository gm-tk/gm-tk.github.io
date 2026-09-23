#!/usr/bin/env python3
"""ROUND 457 finalise — gate_baseline.json (line edits, the r453 pattern) + LOOP_STATE.md (the r456 pattern) in one script.
.pre-r457.bak / .pre-r457-finalise.bak kept. Run under WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
# ---- gate_baseline.json ----
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json")
shutil.copyfile(P, P + ".pre-r457.bak")
L = io.open(P, encoding="utf-8").read().split("\n")
def setv(key, old, new):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            L[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            L.insert(i, line); return
    raise SystemExit(f"anchor not found {key}")
setv("build", '"260620.26"', '"260620.27"'); setv("round", "456", "457")
insert_before("_note_r456", '    "_note_r457": "Round 457 (session 41 Round 5, 2026-09-24; the page-model lane — the over-split census) — THE SECTION-LABEL MARKER IS NOT A PAGE BOUNDARY: the inline \'[lesson title]\' label (PES1008 ×8) and the red \'[Lesson Summary]\' label before a short summary (HIS1002 ×9 of 10, MXFU402 ×2) no longer open a page (r245\'s lesson_boundary_guard deny_marker_pattern / deny_short_marker_pattern, LABELMARK_OFF); HIS1002\'s FIRST summary stays a boundary (lesson 2 has no marker of its own). SCOPED ship #4 since the r452 FULL: 3 modules, pages 2717 -> 2700, pairs 2520 -> 2519. SCAFFOLD 54.8705 -> 54.8967 (+0.0263pp; 9 up / 5 down ≤ 2.6), >=50 1575 -> 1577; cs exact 16024 -> 16045. NAMED: cs missing 840 -> 847 (+7 on +28 newly matched summary / menu elements), body ANY 239 -> 240 (PES1008_7_0: a pre-existing widget over-capture now visible because gold 7.0 pairs with its true page), clean 2663/2709 -> 2646/2692 (98.30 -> 98.29 — the 17 removed pages were all clean; the unclean count held at 46). _fastloop_diff --accept-named, outputs/_r457_fastloop_named.log.",')
setv("mean_scaffold_pct", "54.87", "54.9"); setv("median_scaffold_pct", "55.92", "55.96")
setv("pages_ge_50", "1575", "1577"); setv("raw_mean_pct", "38.88", "38.9"); setv("pairs", "2520", "2519")
insert_before("_note_r456_state", '    "_note_r457_state": "r457 (the section-label marker): SCAFFOLD 54.8705 @ 2520 -> 54.8967 @ 2519 (+0.0263pp), RAW 38.878 -> 38.896; movers 14 (9 up / 5 down), pp-sum +16.5, 6 new-only / 7 gone Claude pages, 0 outside the affected set; the one lost pair PES1008_3.0 (the human splits lesson 3 into 3.0 / 3.1). outputs/_r457_sk_final.json, _r457_skdelta.log, _r457_prescore2.log.",')
setv("exact_chain", "16024", "16045"); setv("claude_missing_container", "840", "847")
setv("any_breakdown", "239", "240"); setv("over_capture", "61", "62")
setv("clean_pages", "2663", "2646"); setv("total_pages", "2709", "2692"); setv("clean_pct", "98.3", "98.29")
out = "\n".join(L); json.loads(out)
tmp = P + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, P)
print("gate_baseline.json -> r457")
# ---- LOOP_STATE.md ----
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-r457-finalise.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
i = find("- **ROUND 457 IN FLIGHT — NOT PROVEN**"); j = find("- Before r457: **no round in flight**"); assert j == i + 1
marker = L[i]
L[i:j + 1] = ["- **No round in flight** (24 Sept 2026 ≈10:25, session 41 Round 5 — r457 SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r457** (260620.27); **LAST FULL = the r452 state**; ledger **scoped #4** since it (4 of headroom)."]
k = find("- LAST SHIPPED: **r456**")
L[k] = "- Before it: **r456** (260620.26, the mid-page lesson heading opens its page, +0.1025pp, ≥50 +26; 22 modules, pairs 2487 → 2520; three movers named) — gate row in BUILD_CHANGELOG.md round 456."
L.insert(k, "- LAST SHIPPED: **r457** (build 260620.27, 24 Sept ≈10:20, session 41 Round 5 — THE SECTION-LABEL MARKER IS NOT A PAGE BOUNDARY, `LABELMARK_OFF`; 3 modules (HIS1002 / MXFU402 / PES1008), Claude pages 2717 → 2700; SCOPED, **scoped #4 since the r452 FULL**; **skeleton 54.8705 % @ 2520 → 54.8967 % @ 2519 (+0.0263pp)**, ≥50 1577 (+2), ≥75 270, ≥90 24, RAW 38.896 %; cs 16045 / 199 / 847 / 24 (missing +7 NAMED); body 62 / 5 / 176 / 240 (+1 NAMED); clean 2646 / 2692 (NAMED); leak 75 / 46; `gate_baseline.json` at r457; the miner 196 CANDIDATE @ 2519).")
k = find("- Plateau window (§4): **0 of 3** — r456")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r456", "- Plateau window (§4): **0 of 3** — r457 predicted a move and delivered +0.0263pp (above the 0.02pp line); r456", 1)
k = find("- Standing facts: AppVersion 260620.26")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.26 (r456", "- Standing facts: AppVersion 260620.27 (r457 the section-label marker — session 41 Round 5, 24 Sept); before it 260620.26 (r456", 1)
k = find("## Round log")
L.insert(k + 1, "- s41-r5 (engine r457, build 260620.27, 24 Sept ≈10:05 → ≈10:25) · THE SECTION-LABEL MARKER IS NOT A PAGE BOUNDARY (the over-split census: `[lesson title]` PES1008 ×8, `[Lesson Summary]` HIS1002 / MXFU402 — r245 had kept both as 'genuine' boundaries) · `LABELMARK_OFF`, 3 modules, −17 pages · SHIPPED · scaffold 54.8705 → 54.8967 (+0.0263pp), ≥50 +2, cs exact +21 · in-round repair: the unconditional summary deny merged HIS1002 lessons 1 + 2 (gold 1.0 −33.6) → the short-run lookahead · three movers NAMED · scoped #4.")
k = find("**Next session starts with:**")
L[k] = L[k].replace("census 552 / 545 / **2,717** pages / **2,520** pairs", "census 552 / 545 / **2,700** pages / **2,519** pairs", 1).replace("LAST SHIPPED **r456** (260620.26); LAST FULL = the **r452 state**; ledger scoped #3;", "LAST SHIPPED **r457** (260620.27); LAST FULL = the **r452 state**; ledger scoped #4;", 1)
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 41 — Round 5 PICK (engine r457) + what shipped\n\n" + marker + "\n- **What shipped (r457, 260620.27):** the r245 guard's `deny_marker_pattern` (`[lesson title]`, unconditional) + `deny_short_marker_pattern` (`[Lesson Summary]` when the next page boundary follows within 12 items); OFF 3218 / 3218 (the probe's disk state); ON 24 pages / 3 modules; first probe (summary denied unconditionally) HIS1002 −33.6 on gold 1.0 → the lookahead; pre-existing pairs +51.6 pp-sum; scoped regen 3 + 12; disk = probe 34 / 34; decomposition: skeleton +0.03 / ≥50 +2 / cs exact +21, missing +7 / body +1 / clean −0.01 NAMED; post-ship green.\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", len(s.encode("utf-8")), "->", os.path.getsize(S))
