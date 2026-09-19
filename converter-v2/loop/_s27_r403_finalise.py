#!/usr/bin/env python3
"""ROUND 403 (loop session 27 Round 8 — an [embed] of an external web page is the KB's externalButton) — finalise:
changelog (entry text in _s27_r403_entry.md), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
(Config.js AppVersion 260619.74 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s27_r403_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s27_r403_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 403, build 260619.74" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r403 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.74"' in s, "Config.js not bumped"

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`EMBEDBTN_OFF` | 403" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 402 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 403 BASELINE (an `[embed]` of an external web page is the KB's externalButton — "
            "`elements.embeds.external_button`; 53 modules; SCOPED regeneration of the 53, the probe proving the other 363 byte-identical; scoped ship #7 since the r396 full — "
            "THE NEXT SHIP IS THE FULL BACKSTOP): SCAFFOLD mean 53.998% / >=50% 1175 / >=75% 200 / >=90% 18 / RAW 38.006% @ 1956 pairs, pairs skipped 0 — hold-or-improve; "
            "20 movers (18 up, 2 down — XDLS903_7_0 −8.7 the scorer's alignment artefact on a page whose gold ships this very site as the externalButton, MXDI202_8_0 −0.7 — named). "
            "compare_structure 11798 / 172 / 626 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 402 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `OWNERALIAS_OFF` | 402 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `EMBEDBTN_OFF` | 403 | **AN `[embed]` OF AN EXTERNAL WEB PAGE IS THE KB'S externalButton, NEVER A BARE IFRAME** (the autonomous loop's session 27 Round 8 — the "
             "position-free label census's Claude-only label `div.ratio.ratio-16x9`, the `[embed]` route's wrapper for a non-video URL: gold 0 / Claude 133). Measured on the paired "
             "pages (`_s27_r8_bareratio.py`, 129 sites / 77 pages / 58 modules): the gold iframes NONE — it drops the resource on 91 (worksheet / PDF / slide pages the developer "
             "re-sourced or omitted) and LINKS it on 38 (24 buttons, 14 anchors) — every kept URL a link (KB 05D + constraint 75). Data `elements.embeds.external_button {enabled, env}` "
             "— the route emits the r338 `buttons.external_destination` form (`<a href target=_blank><div class=externalButton>Go to website</div></a>`) for a host not on that rule's "
             "internal-host list (Google Docs / Drive / SharePoint keep the iframe); a video host never reaches the branch. OFF = the bare iframe (probe 2109 / 2109). 66 pages / 53 "
             "modules; skeleton +0.0091pp (18 up / 2 down, named), ≥50 +1; every other gate EXACT. Measured and DECLINED the same round: the r6 'synthetic box after a writer box' "
             "merge class (`_s27_r8_mergebox.py`: the gold ships the same-numbered box 0.62, merges 0.08). |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.73` (round 402"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.74` (round 403 — **an `[embed]` of an external web page is the KB's externalButton, never a bare iframe** (the `[embed link]` / `[link to PDF of: …]` "
             "route emits the r338 external-destination button for a non-internal host; `elements.embeds.external_button`, env `EMBEDBTN_OFF`; KB 05D + constraint 75); the "
             "autonomous loop's session 27 Round 8 — the label census's Claude-only wrapper (gold 0 / Claude 133; the gold links every kept URL, 38 / 38); 66 pages / 53 modules "
             "changed; SCOPED regeneration of the 53 (scoped ship #7 since the r396 full — the FULL backstop is due at the next ship); skeleton 53.989 → 53.998 % (+0.0091pp; "
             "20 movers 18 up / 2 down, named), ≥50 1174 → 1175, ≥75 200, ≥90 18, RAW 38.000 → 38.006 %; compare_structure / body_compare / every verifier EXACT). Previous: "
             "`260619.73` (round 402"
             + OLD14[len("- **Build:** `260619.73` (round 402"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r403" not in d["_meta"]:
    d["_meta"]["build"] = "260619.74"; d["_meta"]["round"] = 403; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r403"] = ("Round 403: an [embed] of an external web page is the KB's externalButton (66 pages / 53 modules; scoped ship #7 since the r396 full — the next "
                               "ship is the FULL backstop). Skeleton 53.989 -> 53.998 (+0.0091pp; 20 movers 18 up / 2 down, named), >=50 1174 -> 1175, >=75 200, >=90 18, "
                               "RAW 38.000 -> 38.006; compare_structure 11798 / 172 / 626 EXACT; every other gate EXACT; every verifier RESULT identical to r402.")
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.998; sk["raw_mean_pct"] = 38.006; sk["pages_ge_50"] = 1175
    if "pages_ge_75" in sk: sk["pages_ge_75"] = 200
    sk["_note_r403"] = ("Round 403: SCAFFOLD 53.9886 -> 53.9977 (+0.0091pp; 20 movers, 18 up / 2 down, pp-sum +17.9 — XDLS903_7_0 -8.7 the alignment artefact on a page whose gold "
                        "ships the site as the externalButton, MXDI202_8_0 -0.7), >=50 1174 -> 1175 (TEFUN08_0_0), >=75 200, >=90 18; RAW 38.000 -> 38.006; 1956 pairs / 0 skipped.")
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r403")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s27_r403_finalise.py" not in s:
    A = "| `_s27_r7_pick.md` + `_s27_r7_inprogress.py` / `_s27_r7_ownerscan.cjs`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s27_r8_mergebox.py` + `.out` (the synthetic box after a writer box — gold own-box 0.62 / merged 0.08, DECLINED) / `_s27_r8_bareratio.py` + `.out` (CLAUDE'S BARE "
           "`div.ratio.ratio-16x9` — the gold iframes none of the 129, links 38 — the round's instrument) / `_s27_r8_pick.md` + `_s27_r8_inprogress.py` / `_s27_r403_probe.cjs` + "
           "`_s27_r403_probe_run.sh` + their OFF / ON logs + `_s27_r403_on/` / `_s27_r403_pagescore.py` + `_s27_r403_onscore.json` / `_s27_r403_batches.sh` + `_s27_r403_regen_run.sh` "
           "+ the batch logs / `_s27_r403_regen_vs_probe.log` / `_s27_r403_gates.sh` + `.log` + `_s27_r403_sk_final.json` + `_s27_r403_sk_full.log` + `_s27_r403_skdelta.py` + "
           "`_s27_r403_sk_delta.log` / `_s27_r403_postship.sh` + the selftest / fast-loop / manifest / index logs / `_diff_miner_s27_r403.log` + `_diff_queue_pre_r403.md` + "
           "`_s27_r403_qdelta.py` + `_s27_r403_queue_delta.log` / `_s27_r403_entry.md` + `_s27_r403_finalise.py` + `_s27_r403_checksums.sh` + `_s27_r403_loopstate.py` | "
           + loc + " | Session 27 Round 8 (engine r403, build 260619.74) — an `[embed]` of an external web page is the KB's externalButton, never a bare iframe: the merge-box "
           "class measured and declined, the bare-ratio census (gold 0 / 129), the in-memory probe (OFF 2109 / 2109, ON 66 pages / 53 modules), the gate-scored ON pages "
           "(18 up / 2 down, +17.7), the scoped regeneration, the gates and the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r403 row")
print("finalise done")
