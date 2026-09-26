#!/usr/bin/env python3
"""_s51_stop.py — session 51 `/loop-stop` (26 Sept 2026): r528 toggled OFF + uncommitted; the Position bullet, the Round-log line,
the Follow-up entry, the Decisions block, the STOPPED entry (the s50 one archived verbatim), the Next-session line. WSL, from outputs/:
python3 _s51_stop.py HH:MM"""
import io, os, sys, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
T = sys.argv[1]
src = io.open(S, encoding="utf-8", newline="").read(); L = src.split("\n")
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s51-stop.bak"))
def one(pre):
    h = [i for i, l in enumerate(L) if l.startswith(pre)]
    assert len(h) == 1, (pre, h); return h[0]

# 1. the in-flight marker → the toggled-off bullet
i = one("- **ROUND 528 IN FLIGHT — NOT PROVEN**")
L[i] = (f"- **ROUND 528 BUILT, TOGGLED OFF, UNCOMMITTED — finishing (or declining) it is Round 1 of the next session** (session 51 Round 13, "
        f"picked 26 Sept 14:52, stopped {T} by Chris's `/loop-stop`): **THE UNTAGGED WHAKATAUKĪ** — a free black paragraph of ≥ 4 words, every "
        f"word Māori-phonotactic, followed by a black English paragraph is re-typed as the `[Whakatauki]` tag (the existing proverb-only box). "
        f"Gold 49 / 77 untagged pairs boxed (0.77 of the 64 whose text is in the gold; 69 pages, no family > 6); KB 07B §7. **Uncommitted:** "
        f"`app/js/PageAssembler.js` (`#untaggedProverb` + its call after `#boldIdWidgetActivity`) and `data/Emit_Templates.json` "
        f"`callouts.untagged_proverb` — **`enabled: false`** (env `UNTAGPROVERB_OFF`); a copy in `outputs/_r528_wip.patch`. **Proven inert:** "
        f"406 / 406 pages identical over its 54 modules with the flag off; the env-OFF probe 0 changed corpus-wide. **ON** (the "
        f"`_s51_flagon.cjs` preload): 82 pages / 54 modules (`outputs/_affected_r528.txt`; ANZH301 / 302 change on ALL 12 pages each — check "
        f"why first; both have no gold dir). **Pre-score (`_r528_prescore.log`): +0.0030pp, 25 up / 34 down** — the downs are the -00 pages "
        f"(CEDR203 −9.51, PHE1005 −6.98, ENGC204 −5.17, PHE1007 −4.49, HES1003 −4.29): the gold puts the box elsewhere on the overview "
        f"(BLLR201: before the intro prose) or the swallowed English line. Nothing regenerated; the corpus on disk is the r526 state.")

# 2. the Round-log line (newest first: above s51-r12)
j = one("- s51-r12 (no engine change")
L.insert(j, f"- s51-r13 (engine r528, 26 Sept 14:25 → {T}) · a PICK pass — the registry rows' in-memory probe (the five parked flags ON via "
            f"`_s51_flagon.cjs`: all below the floor, stay parked) + a NEW instrument (`_s51_r13_csmiss.py`, cs MISSING 879 by wrapper: alert "
            f"768 el / 298 pages, whakatauki 111 / 59) → r528 THE UNTAGGED WHAKATAUKĪ built (gold 0.77) · pre-score +0.0030pp (25 up / 34 "
            f"down) · TOGGLED OFF at Chris's `/loop-stop`, uncommitted, proven inert.")

# 3. the Follow-up entry
k = one("## Follow-up candidates surfaced by Round 1")
L.insert(k + 1, "- **(s51-r13) the registry rows' lane + the cs MISSING census:** the five parked data flags re-probed ON against the "
                "r526 engine (`_s51_probe_par.sh` + `FLAGON=`; `_s51_r13_{cb,mip,aimg,rba,inh}_pre.log`) — `table.cell_bullets` +0.0053pp "
                "(19 up / 53 down), `dual_language.media_in_place` +0.0044 (30 / 35, as at r461), `dual_language.audio_image` −0.0049 (0 / 3), "
                "`reo_bundle_activity` +0.0073 (8 / 8 — TRR102 carries every gain: one module), `engine_inherit` 0 (92 pages change, "
                "skeleton-blind) — every one stays parked. `_s51_r13_csmiss.py` (compare_structure's MISSING 879 split by wrapper): "
                "**`div.alert` 768 elements / 298 pages / 149 modules** (TRR 105, HIS 81, HPRE 51, PES 49, ENFUN 41; Claude leaves `p` / `h3` / "
                "`ul` bare in the col) — **not yet cue-censused: the next PICK's lead** (is there a writer cue — a heading word, a bold lead, a "
                "`[Body]` run — at ≥ 0.60?); `div.whakatauki` 111 / 59 / 55 → r528.")

# 4. the Decisions block (above session 50's)
d = one("## Decisions from Chris (session 50 ")
L.insert(d, f"## Decisions from Chris (session 51 — 2026-09-26 09:36 → {T} NZST): the standing `/loop-start` kickoff (the default budget, "
            f"16 rounds or 10 hours) and, at ≈ 14:55, the standing `/loop-stop` (finish-and-commit if provable in under 10 minutes, else toggle "
            f"OFF and leave it uncommitted-but-described; record decisions; \"Next session starts with:\"; commit what is finished; the §5 "
            f"report; a safe-to-close sentence) — NO new numbered decision; no new Needs-Chris item. Applied stop: r528 needed its downs "
            f"triangulated, a 54-module regeneration, the scoped ship and the gates (≈ 45 min) → its data flag set `enabled: false`, engine "
            f"+ data left uncommitted and described in Position (proven inert: 406 / 406 pages identical over its 54 modules).")
L.insert(d + 1, "")

# 5. the STOPPED entry; the s50 one archived verbatim
s = one("## >>> STOPPED 2026-09-26 06:40 NZST (session 50)")
old = L[s]
L[s] = (f"## >>> STOPPED 2026-09-26 {T} NZST (session 51) on Chris's `/loop-stop` — 13 of 16 rounds (≈ 5 h 20 m of the 10 h). **FOUR "
        f"ENGINE ROUNDS SHIPPED + ONE FULL BACKSTOP, every one committed:** r522 the journal instruction's own activity box (+ the AGH "
        f"[Summary] alert + the r468 ride-along), r523 the activity governs a heading co-tag, r525 the FRNO bold activity id, r526 the BLL "
        f"introduction's full-width row; FULL s51-r12 (0 pages differ). Declined: r524, r527, r527 v2. **r528 (the untagged whakataukī) "
        f"built and TOGGLED OFF, uncommitted** (pre-score +0.0030pp). Skeleton **55.7889 → 56.1010 % @ 2486** (+0.3121pp), ≥50 1616 → "
        f"1627, ≥75 286 → 292, ≥90 26 → 28, RAW 39.630 → 39.844; cs exact 16772 → 16830 (EXTRA 204, missing 886 → 879); body ANY 236 → "
        f"234; leak 52; **61.2 % of achievable** (ceiling 91.7 %). Plateau 0 of 3. Needs Chris: #1 / #10 only (human actions). <<<")
L.insert(s + 1, "## STOPPED entry, session 50 (26 Sept 06:40, §4 BUDGET; r510–r521 shipped + the r513 / r520 FULL backstops) -> "
                "LOOP_STATE_ARCHIVE.md 'STOPPED entry, session 50 (verbatim, s51 stop)'. Superseded by the session-51 entry above; every verdict stands.")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## STOPPED entry, session 50 (verbatim, s51 stop)\n\n" + old + "\n")

# 6. the plateau window
p = one("- Plateau window (§4): **0 of 3** — ")
L[p] = L[p].replace("- Plateau window (§4): **0 of 3** — ", "- Plateau window (§4): **0 of 3** — s51-r13 r528 built, toggled OFF unproven (neither); ", 1)

# 7. the Next-session line
n = one("**Next session starts with:**")
L[n] = ("**Next session starts with:** `/loop-start` (16 rounds or 10 hours). The tree is DIRTY BY DESIGN: r528 (the untagged "
        "whakataukī) is built and toggled OFF (`callouts.untagged_proverb.enabled: false`), `app/js/PageAssembler.js` + `data/Emit_Templates.json` "
        "uncommitted and proven inert — NOT a crashed round (Position names it). **Round 1 = finish or decline r528:** triangulate its -00 "
        "downs (CEDR203 / PHE1005 / ENGC204 — where the gold puts the box) and ANZH301 / 302's all-page change; ship only above the floor, "
        "else decline and park `outputs/_r528_wip.patch`. Then the `div.alert` 768-element MISSING class (Follow-up s51-r13). LAST SHIPPED "
        "r526 (260620.86); LAST FULL r526 (s51-r12); ledger scoped #0.")
out = "\n".join(L)
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write(out)
assert os.path.getsize(S + ".tmp") > 90000
os.replace(S + ".tmp", S)
print("LOOP_STATE", len(src.encode()), "->", os.path.getsize(S))
