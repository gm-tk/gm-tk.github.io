#!/usr/bin/env python3
"""r462 DECLINED record (marker → the r463 marker, Declined classes entry, round-log line, PICK → archive) + the r463 PICK.
Line edits only; .pre-r462-decline.bak kept. Run under WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-r462-decline.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8"))
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
i = find("- **ROUND 10 (engine r462) IN FLIGHT — NOT PROVEN**"); marker10 = L[i]
L[i] = ("- **ROUND 11 (engine r463) IN FLIGHT — NOT PROVEN** (24 Sept 2026 ≈13:40, session 41): THE TILE'S \"Year N\" LEARNING "
        "LEADS — the WJFUN tile dialect's `[Lesson Overview]` LI / SC run (r410 `splitLiSc`) is refused when its lead reads "
        "\"Year 3 Learning Intention\" / \"Year 3 Success Criteria\", so the tile's LI / SC ship as body paragraphs and its menu "
        "pane is an empty heading. Files: `app/js/ContentConverter.js`, `data/Emit_Templates.json` "
        "(`tile_pages.year_lead`), `app/js/Config.js`. Data flag `year_lead.enabled`; env **`TILEYEAR_OFF`**. Before it: r462 "
        "DECLINED (reverted, tree clean at dd4abba). LAST SHIPPED **r461** (260620.31); LAST FULL = r460; ledger scoped #1; "
        "plateau 2 of 3.")
p0 = find("## Session 41 — Round 10 PICK (engine r462)"); p1 = p0 + 1
while p1 < len(L) and not L[p1].startswith("## "): p1 += 1
pick10 = L[p0:p1]
L[p0:p1] = ["## Session 41 — Round 11 PICK (engine r463) — THE TILE'S \"Year N\" LEARNING LEADS (WJFUN)",
            "- **Lane:** per-family registry rows (§1d exception 1) — the r460 follow-up (WJFUN's menu) + the lost-content census "
            "(`_s41_r8_lost.py`: WJFUN116 701 / WJFUN115 386 / WJFUN112 166 lost shingles) + `_s41_r8_kptabs.py` (11 WJFUN "
            "modules / 18 menu panes are an EMPTY 'Learning Intentions' heading). **Triangulated:** WJFUN116 WT tile 1 `[Lesson "
            "Overview]` → \"Year 3 Learning Intention\" / \"We are learning:\" / • … / \"Year 3 Success Criteria\" / \"I can:\" / • …; "
            "the gold's \"Language choices\" pane holds them as `h4 Learning Intentions` + `h5 We are learning:` + ul …; Claude's "
            "pane is `<h5>Learning Intentions</h5>` alone and the run ships in the tile's body as `p` / `ul`. Cause: `splitLiSc` "
            "requires the run to OPEN with `li_lead_pattern` (`^(we are learning|learning intentions?)`), and \"Year 3 …\" does "
            "not. `[Lesson Overview]` is the WJFUN tile form in 14 of 21 modules. **Authority:** the gold (the family's own "
            "convention) + KB c67's canonical LI / SC titles. **Prediction:** a skeleton move on the WJFUN tile pages (the body "
            "loses the misplaced LI / SC `p` / `ul` lines).",
            ""]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 41 Round 10 (24 Sept ≈13:10 → 13:30) — THE AUDIO-IMAGE UNIT IN PLACE (engine r462 — BUILT, PROBED, "
         "DECLINED, REVERTED; `outputs/_r462_declined.patch` keeps the code).** `media_in_place.units_only`: only an audio-image "
         "unit goes back where the writer typed it. Companion scoring (`_r462_companion.log`): 11 up / 8 down, **pp-sum −5.1** — "
         "TRR109_4_0 (paired with gold 3.0 by the gate's pairing) −18.9 with its position-free overlap unchanged (matched lines "
         "58 → 29: a whole-page alignment flip); without it +13.8. The full interleave (r461's parked `media_in_place`) measured "
         "27 up / 37 down. Never re-open without first fixing TRR109's page pairing (its gold 3.0 / 4.0 pair with Claude 4_0 / "
         "3_0).")
k = find("## Round log")
L.insert(k + 1, "- s41-r10 (engine r462, 24 Sept ≈13:10 → ≈13:30) · THE AUDIO-IMAGE UNIT IN PLACE (the r461 follow-up: the unit placed "
         "where the writer typed it, other media unchanged) · DECLINED on measurement (11 up / 8 down, pp-sum −5.1; TRR109_4_0 −18.9 "
         "alignment flip) · reverted, tree clean · also measured and recorded this round: the activity box's missing title "
         "(`_s41_r10_boxtitle2.py` / `_s41_r10_outh.py` — heterogeneous, no sub-form at the floor) · plateau unchanged 2 of 3.")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 41 — Round 10 PICK (engine r462, DECLINED) + what it found\n\n"
    + "\n".join(pick10).rstrip() + "\n" + marker10 + "\n- **Verdict:** DECLINED — see Declined classes (s41-r10). The pre-experiment files "
    "were restored from `outputs/_r462_BB_pre.js` / `_r462_ET_pre.json` (= the committed r461 state; `git status` clean).\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", n0, "->", os.path.getsize(S))
