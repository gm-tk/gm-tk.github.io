#!/usr/bin/env python3
"""ROUND 461 finalise — BUILD_CHANGELOG.md (prepend), Config.js AppVersion, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json,
KB_AMALGAMATION_STATUS.md (a KB 01E row note), LOOP_STATE.md (marker cleared, Position, round log, PICK → archive). Line edits
only; .bak kept. Run under WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
# ---------- asserts first (nothing written until every anchor is found) ----------
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 461," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.30";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 460 BASELINE"; a11 = "| `KPTABS_OFF` | 460 |"; a14 = "- **Build:** `260620.30` (round 460"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 9 (engine r461) IN FLIGHT — NOT PROVEN**", "- LAST SHIPPED: **r460**", "- Plateau window (§4): **1 of 3** — r460",
          "- Standing facts: AppVersion 260620.30", "## Session 41 — Round 9 PICK (engine r461)", "## Round log", "**Next session starts with:**"):
    find(p)

entry = """## 2026-09-24 (round 461, build 260620.31) — THE AUDIO-IMAGE UNIT (KB 01E / 04B): in a bilingual lesson the writer's `[Audio Image]` / `[Audio Image Hover]` tag and its image + audio lines now build the clickable picture that plays its sound (`div.audioImage > div#{audio}.audioImageOption > img`), side-by-side units sharing one grid row — where it used to ship an empty audio player, a picture and a second audio player — the loop's session 41 Round 9 (the loss ledger's lowest family, TRR)

### 1. WHAT CHANGED

**The find** (`outputs/_s41_r9_skdiff.py` on the TRR family — 76 pages, mean 40.4 %; `outputs/_s41_r9_audioimg.py`): the gold's `div.audioImage` grids (111 pages / 31 modules; Claude 0). The WT-tagged population: 141 `[Audio Image …]` tags / 18 modules, 100 in the tag → `[Item N] [Image]` → `[Item N] [Audio]` shape, almost all in the TRR bilingual cells. The lexicon's `audioimage` alias of `audio` turned each into three embeds. The r135 table-grid build (`audio_image`, parked) catches only 3 pages (a separate image-row / audio-row table) and stays parked.

**The fix** (`BilingualBuilder.bilingualSplit`; data `Emit_Templates.elements.dual_language.audio_image_tag` {tag_pattern, unit_template, group_cols}; env **`AUDIOIMGTAG_OFF`**, byte-identical OFF): the tag opens a RUN — each following image + audio pair is one unit (id = the writer's audio name; the img = the cell image the converter already builds) until other content breaks it; a run of 2+ units is one `div.row` (2 → `col-md-6 offset-md-0 col-12`, 3 → `col-md-4 col-12`, 4+ → `col-md-3 col-6`, the gold's forms); a broken shape emits exactly the old embeds. In-round repair: TRR113's `[AudioImage Hover]` introduces TWO pairs (u … e) — the run continuation. **Parked in the same round:** `dual_language.media_in_place` (`REOMEDIAPOS_OFF`, enabled:false) — putting each bilingual media embed back between the paragraphs where the writer typed it measured 27 up / 37 down (+8.0 pp-sum over the unit alone; 26 dips with no rising companion — TRR116 / TRR203 / TRR108's gold does not follow the writer's cell order); the code stays as the base.

### 2. PROOF

- In-memory A/B (`outputs/_r461_probe_run.sh`): OFF 3217 / 3217 identical; ON 22 pages / 7 modules (TRR103, TRR109, TRR110, TRR111, TRR112, TRR113, TRR116).
- Pre-score + companions (`_r461_prescore.py`, `_r461_companion.py` → `_r461_companion_ai.log`): **7 up / 15 down, pp-sum +25.6** — TRR112_2 22.6 → 38.5, TRR112_3 31.1 → 37.7, TRR113 2.0 39.1 → 42.7, TRR111 3 / 4 / 1 +2.7 / +2.6 / +1.6. **Named dips (all ≤ 0.9):** TRR109 1 / 2 / 3-4 and TRR110 1–4 are KB overrides (those golds render the tag as audioTrigger / `img.audioText`, not audioImage — KB 01E rank 1); TRR111_2, TRR113_1 have a rising position-free overlap (the alignment artefact); TRR112_1 / 4, TRR113_3 / 4.0, TRR103_3, TRR116_1 lose ≤ 0.9 because the bilingual cell's media still follows its paragraphs (the parked media_in_place) — the unit's three lines sit where the gold has text.
- Scoped regeneration of the 7 + the 12-module spot-check (`_r461_regen.sh`): 0 truly stale, 12 / 12 byte-identical; `scoped_ship.sh --toggle AUDIOIMGTAG_OFF --round 461`: **PASS** (exact, decomposition-proven), scoped #1 since the r460 FULL.

### 3. PROTECTED GATES

- Skeleton **54.9376 % → 54.9477 % @ 2524 (+0.0101pp)**; ≥50 1581, ≥75 275, ≥90 25; RAW 38.967 → 38.975; 0 movers outside the affected set.
- compare_structure 16719 / 208 / 896 / 24 EXACT; body_compare 61 / 5 / 176 / 239 EXACT; clean 2621 / 2667 EXACT; leak 75 / 46 EXACT; tags 9557; every verifier ✓; selftests 50 PASS; index GREEN; the miner 197 CANDIDATE @ 2524.
- Plateau (§4): the PICK predicted a skeleton move; +0.0101pp is under the 0.02pp line → counted as NOT moving: **2 of 3**.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 461 (260620.31): THE AUDIO-IMAGE UNIT (session 41 Round 9; KB 01E / 04B). In a bilingual cell the writer's [Audio Image] / [Audio Image Hover] tag + its [Image] + [Audio] lines build div.audioImage > div#{audio}.audioImageOption > img (a run of units = one grid row), where the lexicon's audioimage alias made an empty audio player + an image + a second player. Emit_Templates dual_language.audio_image_tag, env AUDIOIMGTAG_OFF; dual_language.media_in_place (REOMEDIAPOS_OFF) PARKED off (27 up / 37 down). 7 modules / 22 pages; skeleton +0.0101pp (7 up / 15 down named, TRR112_2 +15.9); every other gate exact.\n" + '\tstatic AppVersion = "260620.31";', 1)
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 461 BASELINE (the audio-image unit — KB 01E, `AUDIOIMGTAG_OFF`; SCOPED, scoped #1 since the r460 FULL): SCAFFOLD mean 54.9477% / >=50% 1581 / >=75% 275 / >=90% 25 / RAW 38.975% @ 2524 pairs — +0.0101pp (7 up / 15 down NAMED); cs 16719 / 208 / 896 / 24, body 61 / 5 / 176 / 239, clean 2621 / 2667, leak 75 / 46 — all EXACT.** Previous: **ROUND 460 BASELINE", 1)
so = so.replace(a11, "| `AUDIOIMGTAG_OFF` | 461 | **THE AUDIO-IMAGE UNIT** (session 41 Round 9; KB 01E / 04B). Reverts `elements.dual_language.audio_image_tag`: a bilingual cell's `[Audio Image]` tag + image + audio lines ship as an empty audio player, an image and a second player again; byte-identical to r460. 7 TRR modules / 22 pages; skeleton +0.0101pp. (`REOMEDIAPOS_OFF` — the same round's `media_in_place`, shipped PARKED `enabled:false`.) |\n" + a11, 1)
so = so.replace(a14, "- **Build:** `260620.31` (round 461 — **THE AUDIO-IMAGE UNIT** (KB 01E): the bilingual `[Audio Image]` tag builds `div.audioImage`; `AUDIOIMGTAG_OFF`; scoped #1 since the r460 FULL; 7 modules / 22 pages; skeleton 54.9477 %).\n" + a14, 1)
wr(PO, so); print("OG ok")
# ---------- gate_baseline.json ----------
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r461.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            G[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.30"', '"260620.31"'); setv("round", "460", "461")
insert_before("_note_r460", '    "_note_r461": "Round 461 (session 41 Round 9, 2026-09-24; KB 01E / 04B) — THE AUDIO-IMAGE UNIT (AUDIOIMGTAG_OFF): 7 TRR modules / 22 pages; SCAFFOLD 54.9376 -> 54.9477 (+0.0101pp; 7 up / 15 down named in BUILD_CHANGELOG round 461); every other gate EXACT; scoped #1 since the r460 FULL.",')
setv("mean_scaffold_pct", "54.94", "54.95"); setv("raw_mean_pct", "38.97", "38.98")
insert_before("_note_r460_state", '    "_note_r461_state": "r461 (the audio-image unit): SCAFFOLD 54.9376 -> 54.9477 @ 2524, RAW 38.967 -> 38.975; 22 movers, 0 outside the affected set.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
# ---------- KB status ----------
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
anchor = "| 67 | Canonical overview tab set"
assert sk.count(anchor) == 1
i = sk.index(anchor); j = sk.index("\n", i) + 1
sk = sk[:j] + "| 01E-AI | `[audio image]` → `div.audioImage > div#{audio}.audioImageOption > img` (01E Audio Image / 04B COMP_08) | 01E / 04B | bilingual cells (TRR) | **CAPTURED r461** for the tag + image + audio shape in bilingual cells (`dual_language.audio_image_tag`, AUDIOIMGTAG_OFF; 7 modules / 22 pages); the normal-path tag (ENGC401 / PWY, 1–3 per module) and the gold's untagged BLL grids NOT captured | BilingualBuilder |\n" + sk[j:]
wr(PK, sk); print("KB ok")
# ---------- LOOP_STATE ----------
shutil.copyfile(S, S + ".pre-r461-finalise.bak")
i = find("- **ROUND 9 (engine r461) IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈12:25, session 41 Round 9 — r461 SHIPPED and committed; the in-flight marker is "
        "cleared). LAST SHIPPED **r461** (260620.31); **LAST FULL = r460**; ledger **scoped #1** since it (7 of headroom).")
k = find("- LAST SHIPPED: **r460**")
L[k] = ("- Before it: **r460** (260620.30, the Knowledge / Practices overview tabs, KB c67 — THE FULL BACKSTOP; skeleton EXACT, "
        "RAW +0.033pp; 19 modules / 28 pages) — gate row in BUILD_CHANGELOG.md round 460.")
L.insert(k, "- LAST SHIPPED: **r461** (build 260620.31, 24 Sept ≈12:20, session 41 Round 9 — THE AUDIO-IMAGE UNIT, KB 01E / 04B, "
         "`AUDIOIMGTAG_OFF`; 7 TRR modules / 22 pages; SCOPED, **scoped #1 since the r460 FULL**, scoped_ship PASS; **skeleton "
         "54.9376 → 54.9477 % @ 2524 (+0.0101pp; 7 up / 15 down NAMED)**, ≥50 1581, ≥75 275, ≥90 25, RAW 38.975 %; cs / body / "
         "clean / leak EXACT; `media_in_place` PARKED off (27 up / 37 down); `gate_baseline.json` at r461; the miner 197 CANDIDATE).")
k = find("- Plateau window (§4): **1 of 3** — r460")
L[k] = L[k].replace("- Plateau window (§4): **1 of 3** — r460", "- Plateau window (§4): **2 of 3** — r461 predicted a skeleton "
                    "move and delivered +0.0101pp (under the 0.02pp line): counted as NOT moving; r460", 1)
k = find("- Standing facts: AppVersion 260620.30")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.30 (r460", "- Standing facts: AppVersion 260620.31 (r461 the audio-image "
                    "unit, KB 01E — session 41 Round 9, 24 Sept); before it 260620.30 (r460", 1)
p0 = find("## Session 41 — Round 9 PICK (engine r461)"); p1 = p0 + 1
while p1 < len(L) and not L[p1].startswith("## "): p1 += 1
pick = L[p0:p1]
L[p0:p1] = ["## Session 41 — Round 9 (engine r461, build 260620.31) — THE AUDIO-IMAGE UNIT (KB 01E) — SHIPPED; the PICK + "
            "what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 41 — Round 9 PICK (engine r461) + what shipped'; the one-line "
            "summary is the s41-r9 Round-log line below.", ""]
k = find("## Round log")
L.insert(k + 1, "- s41-r9 (engine r461, build 260620.31, 24 Sept ≈11:55 → ≈12:25) · THE AUDIO-IMAGE UNIT (KB 01E: the bilingual "
         "`[Audio Image]` tag + image + audio → `div.audioImage`, runs = one grid row) · SHIPPED scoped #1 · 7 TRR modules / 22 pages · "
         "skeleton 54.9376 → 54.9477 (+0.0101pp; 7 up / 15 down named: TRR109 / 110 KB overrides, the rest ≤ 0.9 position) · every "
         "other gate EXACT · `media_in_place` PARKED (27 up / 37 down) · plateau 2 of 3.")
k = find("**Next session starts with:**")
L[k] = L[k].replace("LAST SHIPPED **r460** (260620.30); LAST FULL = **r460**; ledger scoped #0; plateau **1 of 3**.",
                    "LAST SHIPPED **r461** (260620.31); LAST FULL = **r460**; ledger scoped #1; plateau **2 of 3**.", 1)
assert "LAST SHIPPED **r461**" in L[k]
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Session 41 — Round 9 PICK (engine r461) + what shipped\n\n" + "\n".join(pick).rstrip() + "\n" + marker + "\n"
    "- **What shipped (r461, 260620.31):** `BilingualBuilder.bilingualSplit` builds the audio-image unit from the `[Audio Image …]` "
    "tag run (data `dual_language.audio_image_tag`, env `AUDIOIMGTAG_OFF`); the media-position record + `bilingualRows` in-place "
    "interleave shipped PARKED (`dual_language.media_in_place`, `REOMEDIAPOS_OFF`, enabled:false — 27 up / 37 down, 26 dips with "
    "no rising companion). Evidence: `outputs/_s41_r9_audioimg.log` (141 tags / 18 modules), `_r461_prescore*.log`, "
    "`_r461_companion.log` (both mechanisms) / `_r461_companion_ai.log` (the unit alone). Follow-ups: (1) the skeleton keeps the "
    "`div#{id}` of an audioImageOption — the writer's audio name vs the developer's id (`short u` vs `u short`) decides the "
    "line; a measurement-tool question; (2) the normal-path `[Audio Image]` tag (ENGC401 / 301, PWY1001 / 1007 — the `xx` shapes) "
    "and the BLL gold's untagged audioImage grids (BLL27x ~60 each) are not captured.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
