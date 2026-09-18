#!/usr/bin/env python3
"""ROUND 398 (loop session 27 Round 1 — the videoSection icon registry re-mined + the widget-embedded video) — finalise:
changelog (entry text in _s27_r398_entry.md), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
(Config.js AppVersion 260619.69 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s27_r398_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s27_r398_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 398, build 260619.69" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r398 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.69"' in s, "Config.js not bumped"

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`VIDEOICONWIDGET_OFF` | 398" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 397 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 398 BASELINE (the videoSection `icon` registry re-mined + the widget-embedded video follows it — `video.icon_rule` + `widget_embedded`; 74 modules; SCOPED regeneration of the 74, the probe proving the other 342 byte-identical; scoped ship #2 since the r396 full): SCAFFOLD mean 53.759% / >=50% 1166 / >=75% 195 / >=90% 18 / RAW 37.846% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 88 movers (84 up, 4 down — MXDI102 ×4, the MXDI10 series' plain minority: MXDI102_0_0 −2.3 = the ≥50 down-crosser accepted BY NAME). compare_structure 11723 / 172 / 626 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 397 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `THPLAIN_OFF` | 397 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `VIDEOICONWIDGET_OFF` | 398 | **THE videoSection `icon` REGISTRY RE-MINED + THE WIDGET-EMBEDDED VIDEO FOLLOWS IT** (the autonomous loop's session 27 Round 1 — the position-free label census `_s27_r1_labelcensus.py`: `div.icon.ratio.ratio-16x9.videoSection` the 20th-largest MISSING label, 978 lines / 503 pages; re-measured `_s27_r1_videoicon.py` / `_videoicon2.py` / `_videoicon3.py`). The r200 rule (a per-SERIES / SUBJECT|TEMPLATE house style, Chris-approved, mined on 392 modules) is brought up to the r397 corpus — ADDITIVE, every r200 entry stands: 18 series at n ≥ 2 / share ≥ 0.85 (each ≥ 8 gold videos, 14 at 1.00: ANZH20, CEDR20, CEDR30, ENGC20, ENGC30, ENGJ10, ENGJ20, ENGR10, ENGS20, MXDB20, MXDB30, MXDI10, MXEO20, MXEX20, MXEX30, MXFL30, MXFU30, XDLS91) + the NEW `plain_series` carve-out (a series at n ≥ 2 / share ≤ 0.40 stays plain even inside an icon subject group; consulted before the subject|template fallback) — and its recorded follow-up: in the registry's own modules the gold puts `icon` on the WIDGET-EMBEDDED videos at 0.95 (carousel 364 / 382, accordion 41 / 43, tabs 42 / 44, clickDrop 112 / 122, panel 111 / 120), so `MediaBuilder.videoIconPostpass(bodyHtml, run)` — the LAST step of `ContentConverter`'s final-body chain — adds the token to every `class=\"videoSection …\"` that lacks it in an icon-group module (`MediaBuilder.#videoIconGroup` is the one decision shared with the r200 per-embed replace; idempotent; data `video.icon_rule.widget_embedded {enabled, env_off}`). Scored with the gate's own `match()` on the probe's ON pages BEFORE regenerating — which removed `NCEA1|Standard` (0.81, n = 41: carried by HIS10 / PES10 already in; its reachable series AGH10 a per-module coin-flip whose icon modules' videos are un-built widgets — net −23.2 pp-sum). OFF = `VIDEOICONWIDGET_OFF` reverts the post-pass alone, `VIDEOICON_OFF` the whole rule; the pre-round registry is `outputs/_s27_r398_icon_rule_pre.json` (the probe's OFF leg: 2109 / 2109 byte-identical). 198 pages / 74 modules (704 tokens, nothing else); skeleton +0.064pp, ≥50 +3; every other gate EXACT, every verifier RESULT identical. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.68` (round 397"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.69` (round 398 — **the videoSection `icon` registry re-mined on the r397 corpus + the widget-embedded video follows it** (`video.icon_rule`: 18 series added at n ≥ 2 / share ≥ 0.85, the NEW `plain_series` carve-out; `video.icon_rule.widget_embedded` → `MediaBuilder.videoIconPostpass` at the end of `ContentConverter`'s final-body chain, env `VIDEOICONWIDGET_OFF`; the r200 recorded follow-up — the gold 0.95 on the registry modules' widget-embedded videos); the autonomous loop's session 27 Round 1 — found by the position-free label census; 198 pages / 74 modules changed (704 `icon` tokens, nothing else); SCOPED regeneration of the 74 (scoped ship #2 since the r396 full); skeleton 53.695 → 53.759 % (+0.064pp; 88 movers 84 up / 4 down — MXDI102 ×4 named), ≥50 1163 → 1166, ≥75 195, ≥90 18, RAW 37.782 → 37.846 %; every other gate EXACT, every verifier RESULT identical; `NCEA1|Standard` measured, added, scored on the gate and REMOVED (−23.2 pp-sum on AGH10)). Previous: `260619.68` (round 397"
             + OLD14[len("- **Build:** `260619.68` (round 397"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r398" not in d["_meta"]:
    d["_meta"]["build"] = "260619.69"; d["_meta"]["round"] = 398; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r398"] = "Round 398: the videoSection icon registry re-mined + the widget-embedded video follows it (198 pages / 74 modules; scoped ship #2 since the r396 full). Skeleton 53.695 -> 53.759 (+0.064pp; 88 movers 84 up / 4 down, pp-sum +124.8), >=50 1163 -> 1166, >=75 195, >=90 18, RAW 37.782 -> 37.846; compare_structure 11723 / 172 / 626 and every other gate EXACT; every verifier RESULT identical."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.759; sk["raw_mean_pct"] = 37.846; sk["pages_ge_50"] = 1166
    sk["_note_r398"] = "Round 398: SCAFFOLD 53.6953 -> 53.7589 (+0.064pp; 88 movers, 84 up / 4 down, pp-sum +124.8 - MXDI102 x4 the MXDI10 series' plain minority, MXDI102_0_0 50.0 -> 47.7 the >=50 down-crosser named), >=50 1166, >=75 195, >=90 18, median 54.3, RAW 37.846; SCOPED regeneration of the 74 affected modules. State outputs/_s27_r398_sk_final.json."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r398")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s27_r398_finalise.py" not in s:
    A = "| `_s26_r397_bubbles.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s27_condense.py` + `_s27_startnote.py` + `_s27_insert_section.py` (the session-27 §5d condense + state-file helpers) / `_s27_r1_labelcensus.py` + `.out` + `.json` + `.log` (THE POSITION-FREE LABEL CENSUS — every gate pair's scaffold skeleton as a label multiset, EXTRA / MISSING per label) / `_s27_r1_videoicon.py` + `.out` + `.json` (the gold's icon share per module and context, the r200 solidify test re-run) + `_s27_r1_videoicon2.py` + `.out` + `.json` (the gate-visible substitutions per group) + `_s27_r1_videoicon3.py` + `.out` (four registry designs simulated on the gate's lines) / `_s27_r398_pick.md` / `_s27_r398_icon_rule_pre.json` (the pre-round registry) / `_s27_r398_probe.cjs` + `_s27_r398_probe_run.sh` + their OFF / ON logs + `_s27_r398_on/` / `_s27_r398_why.py` / `_s27_r398_pagescore.py` + `_s27_r398_onscore.json` / `_s27_r398_batches.sh` + `_s27_r398_regen_run.sh` + the batch logs / `_s27_r398_regen_vs_probe.log` / `_s27_r398_gates.sh` + `.log` + `_s27_r398_sk_final.json` + `_s27_r398_sk_full.log` + `_s27_r398_skdelta.py` / `_s27_r398_postship.sh` + the selftest / fast-loop / manifest / index logs / `_diff_miner_s27_r398.log` + `_diff_queue_pre_r398.md` + `_s27_r398_qdelta.py` + `_s27_r398_queue_delta.log` / `_s27_r398_entry.md` + `_s27_r398_finalise.py` + `_s27_r398_checksums.sh` | "
           + loc + " | Session 27 Round 1 (engine r398, build 260619.69) — the videoSection `icon` registry re-mined + the widget-embedded video follows it: the position-free label census (the new instrument), the registry re-mine (18 series + the plain carve-out; NCEA1|Standard added, scored on the gate and removed), the probe (OFF 2109 / 2109 with the pre-round registry; ON 198 pages / 74 modules, 84 up / 4 down, +124.4), the scoped regen + gates (skeleton 53.695 → 53.759, ≥50 +3; every other gate EXACT), the miner re-mine, the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r398 row")
print("finalise done")
