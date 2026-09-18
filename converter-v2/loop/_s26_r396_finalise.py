#!/usr/bin/env python3
"""ROUND 396 (loop session 26 Round 10 — the captioned carousel video slide is item video; the FULL backstop) — finalise:
changelog (entry text in _s26_r396_entry.md), AppVersion (260619.66 -> 260619.67), CLAUDE.md §9 / §11 / §14, gate_baseline.json,
loop/README.md. Idempotent; LF preserved. Run under WSL: python3 _s26_r396_finalise.py"""
import io, os, json
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
HERE = os.path.dirname(os.path.abspath(__file__))


def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f:
        return f.read()


def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = rd(os.path.join(HERE, "_s26_r396_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 396, build 260619.67" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r396 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.67"' not in s:
    old = '\tstatic AppVersion = "260619.66";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 396 (260619.67): a carousel video slide with a caption is `item video` (interactive.carousel.item_video_with_caption, InteractiveBuilder.#carRenderSlides, env ITEMVIDEO_OFF; the gold 273 / 298 = 0.92; a video-only slide is a tie and stays `item`). 52 pages / 44 modules; THE FULL-REGENERATION BACKSTOP — all 416 regenerated, 0 stale, the manifest diff = the probe's 52 pages (no residue from r389–r395); the ledger's scoped-since counter reset to 0.\n\tstatic AppVersion = \"260619.67\";")
    wr(P, s); print("Config.js: 260619.67")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`ITEMVIDEO_OFF` | 396" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 395 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 396 BASELINE (the captioned carousel video slide is `item video` — `interactive.carousel.item_video_with_caption`; a FULL regeneration of all 416 (the ledger's backstop), 0 stale, the manifest diff = the probe's 52 pages exactly): SCAFFOLD mean 53.684% / >=50% 1163 / >=75% 195 / >=90% 18 / RAW 37.780% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 0 movers (the class is a widget-internal token, invisible to the scaffold). compare_structure 11723 / 172 / 626 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 395 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `FLIPCOL_OFF` | 395 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `ITEMVIDEO_OFF` | 396 | **A CAROUSEL VIDEO SLIDE WITH A CAPTION IS `item video`** (the autonomous loop's session 26 Round 10 — the widget-wrapper census `_s26_r396_widgetwrap.py` generalised from r394, then `_s26_r396_itemvideo.py` / `_itemvideo2.py`: of the gold's video-carrying carousel slides that also hold a carousel-caption block 273 / 298 = 0.92 carry `item video` (Inquiry / BLL 51 / 51, Fundamentals 45 / 46, English 38 / 38, NCEA1 20 / 20, ANZH 18 / 18, LtL 28 / 38); Claude's rich / table slide renderer shipped 171 of them as plain `item`. A video-ONLY slide is a tie (496 / 907 = 0.55) and stays `item`; a slide with a heading or a bare paragraph stays `item` (0.12–0.33). Data `interactive.carousel.item_video_with_caption {enabled, env, from, to}` — in `#carRenderSlides` (shared by `rich_slides` + `table_slides`), when the slide's chunks hold a videoSection AND the caption block was opened, the item's opening tag is swapped; the media-caption-table builder keeps its own `item_video_caption`. OFF = the r395 output (probe 2109 / 2109). 52 pages / 44 modules; gate-invisible (a widget-internal token): skeleton / compare_structure / body_compare EXACT, every verifier RESULT identical. Shipped as THE FULL-REGENERATION BACKSTOP (scoped #7 since r388 → full): all 416 regenerated, 0 stale, the manifest diff = the probe's 52 pages — no residue from r389–r395. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.66` (round 395"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.67` (round 396 — **a carousel video slide with a caption is `item video`** (`interactive.carousel.item_video_with_caption`, `InteractiveBuilder.#carRenderSlides`, env `ITEMVIDEO_OFF`); the autonomous loop's session 26 Round 10 — the gold 273 / 298 = 0.92 (a video-only slide a tie, untouched); 52 pages / 44 modules changed; **the FULL-regeneration backstop** — all 416 regenerated (36 batches rc 0), `_stalecheck.sh` 0 stale, the manifest diff = the probe's 52 pages exactly (no residue from the seven scoped ships r389–r395), the ledger's scoped-since counter reset to 0; skeleton 53.684 % / ≥50 1163 / ≥75 195 / ≥90 18 EXACT (gate-invisible), RAW 37.784 → 37.780 %; every other gate EXACT, every verifier RESULT identical; the miner re-mined 173 CANDIDATE rows (nothing gone, nothing new)). Previous: `260619.66` (round 395"
             + OLD14[len("- **Build:** `260619.66` (round 395"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r396" not in d["_meta"]:
    d["_meta"]["build"] = "260619.67"; d["_meta"]["round"] = 396; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r396"] = "Round 396: a carousel video slide with a caption is item video (52 pages / 44 modules; THE FULL-REGENERATION BACKSTOP — all 416 regenerated, 0 stale, the manifest diff = the probe's 52 pages; the ledger reset to 0 scoped since). Skeleton 53.684 / >=50 1163 / >=75 195 / >=90 18 EXACT (gate-invisible), RAW 37.784 -> 37.780; compare_structure 11723 / 172 / 626 and every other gate EXACT; every verifier RESULT identical."
    sk = d["skeleton"]; sk["raw_mean_pct"] = 37.780
    sk["_note_r396"] = "Round 396: SCAFFOLD 53.6835 EXACT (0 movers - the carousel item class is a widget-internal token), >=50 1163, >=75 195, >=90 18, median 54.3, RAW 37.780; FULL regeneration of all 416 (the ledger's backstop). State outputs/_s26_r396_sk_final.json."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r396")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r396_finalise.py" not in s:
    A = "| `_s26_r395_flipcols.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_r396_widgetwrap.py` + `.out` (every built widget's two enclosing wrappers, gold vs Claude — the r394 instrument generalised) / `_s26_r396_itemvideo.py` + `.out` + `_s26_r396_itemvideo2.py` + `.out` (the carousel video item's class by carousel kind, then by the slide's other content) / `_s26_r396_splice.py` (the PICK + the data + engine splice) / `_s26_r396_probe.cjs` + `_s26_r396_probe_run.sh` + their OFF / ON logs + `_s26_r396_on/` / `_s26_r396_pagescore.py` + `_s26_r396_onscore.json` / `_s26_r396_fullship_run.sh` + `_s26_r396_fullship_par.sh` + `_s26_r396_fullship_regen.log` + the 36 batch logs (THE FULL REGENERATION) / `_s26_r396_stalecheck.log` + `_s26_r396_fresh.log` + `_s26_r396_manifest_diff.log` + `_s26_r396_regen_vs_probe.log` / `_s26_r396_gates.sh` + `.log` + `_s26_r396_sk_final.json` + `_s26_r396_sk_full.log` + `_s26_r396_skdelta.py` + `_s26_r396_sk_delta.log` / `_s26_r396_postship.sh` + the selftest / fast-loop / manifest / index logs / `_s26_r396_ledger.log` (record-full) / `_diff_miner_s26_r396.log` + `_diff_queue_pre_r396.md` + `_s26_r396_qdelta.py` + `_s26_r396_queue_delta.log` / `_s26_r396_entry.md` + `_s26_r396_finalise.py` + `_s26_r396_checksums.sh` | "
           + loc + " | Session 26 Round 10 (engine r396, build 260619.67) — a carousel video slide with a caption is `item video` (the gold 0.92; the video-only slide a tie, recorded), the probe (OFF 2109 / 2109; ON 52 pages / 44 modules, gate-invisible), THE FULL-REGENERATION BACKSTOP (all 416, 0 stale, the manifest diff = the probe's 52 pages — no residue from r389–r395), the gates (every one EXACT), the miner re-mine (173 rows, unchanged), the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r396 row")
print("finalise done")
