#!/usr/bin/env python3
"""_s53_stop.py — session 53 /loop-stop: LOOP_STATE.md at the stop (WSL). The r541 in-flight marker becomes a BUILT-TOGGLED-OFF line
(the four engine / data files uncommitted by design); the 'Before r541' line becomes the no-round line; the session-53 decisions
block, the STOPPED entry (s52's archived verbatim), the s53-r8 Round-log line and the new 'Next session starts with' line."""
import io, os, re, shutil, subprocess
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
T = subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()
s = io.open(S, encoding="utf-8", newline="").read(); L = s.split("\n")
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s53-stop.bak"))
def one(pfx):
    idx = [i for i, l in enumerate(L) if l.startswith(pfx)]; assert len(idx) == 1, (pfx, idx); return idx[0]
arch = []
# (1) the r541 marker → built / toggled OFF
fl = one("- **ROUND 541 IN FLIGHT — NOT PROVEN**")
arch.append(("Session 53 — r541 PICK (the in-flight marker, verbatim) — BUILT, TOGGLED OFF at the /loop-stop", L[fl]))
L[fl] = ("- **r541 BUILT, TOGGLED OFF, UNCOMMITTED (the s53 `/loop-stop`, 27 Sept " + T + ")** — THE ALERT WHOSE TITLE IS A HEADING (`_s53_r8_alertrun.py`; "
         "form A: an EMPTY `[Alert]` / `[Important]` then a `[Hn]` — the gold boxes the heading on 55 / 67 sites, Claude ships the empty box + the "
         "\"Empty [alert]\" flag and the heading free on 31; form B: the `[Alert] [H3] …` co-tag — gold 31 / 41, Claude 0). **The tree is DIRTY by design:** "
         "`app/js/ContentConverter.js` (`#emptyCalloutHeadingBox`, called first inside `#summaryHeadingAlert`; data `body_region.empty_callout_heading_box` "
         "**enabled: false**; env CALLOUTHEADBOX_OFF), `app/js/TagNormaliser.js` + `data/Tag_Lexicon.json` (the parked `_r524_declined.patch` applied — "
         "`activity_heading_cotag.callouts` **enabled: false**; env CALLOUTHDCOTAG_OFF), `data/Emit_Templates.json`. Both flags OFF ⇒ the in-memory probe reads "
         "6,432 / 6,432 pages identical to the shipped r539 corpus (`_r541_toggledoff_0?.log`); nothing was regenerated. A copy of the whole diff: "
         "`outputs/_r541_inflight_toggledoff.patch`. Probe readings (flags ON): form A with the full following run incl. notes **+0.0179pp** (75 pages / 26 "
         "modules, 41 up / 13 down); the r529 run rule +0.0109; the run stopping at a note +0.0160; + the r529-heading hand-off (drop only the empty row when "
         "r529 boxes the heading) +0.0148 (the current code: `run_rule` \"all\" incl. notes AND the hand-off); form B adds +0.0012 (XGF9001 / 9002 / 9003 down, "
         "XGF9006 / HPRE301 up). Dips: HIS1007_3_1 −8.2 (the writer asked for the right-hand column — gold `col-md-4 … alert top`), ENGC403_12_0 −6.0, "
         "TEDC402_8_0 −4.2, HPRE301_6_0 −3.1, HES1006_5_0 −2.9.")
# (2) the no-round line
bl = one("- **Before r541: no round in flight**")
L[bl] = L[bl].replace("- **Before r541: no round in flight** (", f"- **No round in flight** (27 Sept 2026 {T}, the s53 `/loop-stop` — r541 built and toggled OFF, above; before it: ", 1)
# (3) the plateau line: r541 neither
pl = one("- Plateau window (§4): **")
L[pl] = L[pl].replace(" — r539 +0.0038pp (< 0.02: counts);", " — r541 built, toggled OFF unproven (neither); s53-r7 a PICK pass (neither); r540 parked (neither); r539 +0.0038pp (< 0.02: counts);", 1)
# (4) decisions block
dh = [i for i, l in enumerate(L) if l.startswith("## Decisions from Chris (loop-run sessions 40 / 42–46 / 49–52")]; assert len(dh) == 1
L.insert(dh[0], "## Decisions from Chris (session 53 — 2026-09-26 22:40 → 2026-09-27 " + T + " NZST): the standing `/loop-start` kickoff (the default budget, "
         "16 rounds or 10 hours) and, at ≈01:24 NZST 27 Sept, the standard `/loop-stop` message — NO new numbered decision; no new Needs-Chris item.\n")
# (5) STOPPED entry: archive s52's, insert s53's
st = one("## >>> STOPPED 2026-09-26 19:41 NZST (session 52)")
arch.append(("STOPPED entry, session 52 (verbatim, s53 stop)", L[st]))
L[st] = ("## >>> STOPPED 2026-09-27 " + T + " NZST (session 53) on Chris's `/loop-stop` (8 of 16 rounds, ≈ 2 h 45 m of the 10 h). **FIVE ENGINE ROUNDS SHIPPED, "
         "every one committed:** r535 the writer's `[close alert box]` is not an opener, r536 the family keeps the writer's heading digit (FRFUN / WJFUN / ENGC), "
         "r537 the accordion panel's bullets are a list (skeleton-blind, RAW +0.043), r538 the same digit rule for COM / GEO / TWHK / TWHR / EXPFUN / CEDK / "
         "CEDO / OSOH, r539 the one-level shift under a body `[H1]` (ARFUN / TWHT); r540 (the writer's side / beside word) PARKED under the floor; s53-r7 a "
         "PICK pass; **r541 (the alert whose title is a heading) BUILT and TOGGLED OFF — the tree is dirty by design (Position).** NEW instruments: the "
         "writer-cue FATE census + its chrome and family-dialect sections (`_s53_tagfate.py`), the skeleton BALANCE, the row-break and body-class censuses. "
         "Skeleton **56.3343 → 56.3799 % @ 2486** (+0.0456pp), ≥50 1638 → 1645, ≥75 305, ≥90 29, RAW 39.971 → 40.028; cs exact 17024 / EXTRA 198 / missing "
         "661 held; body ANY 233; leak 52; **61.5 % of achievable** (ceiling 91.7 %). Plateau 2 of 3. Needs Chris: #1 / #10 only (human actions). <<<")
L.insert(st + 1, "## STOPPED entry, session 52 (26 Sept 19:41, §4 BUDGET; r528–r534 shipped + the s52-r11 FULL) -> LOOP_STATE_ARCHIVE.md 'STOPPED entry, session 52 (verbatim, s53 stop)'. Superseded by the session-53 entry above; every verdict stands.")
# (6) Round log
rl = one("## Round log")
L.insert(rl + 1, "- s53-r8 (engine r541, 27 Sept 01:11 → " + T + ") · THE ALERT WHOSE TITLE IS A HEADING (`_s53_r8_alertrun.py`: form A 67 sites / 31 pages — gold "
         "boxes 55; form B 41 / 16 — gold 31) · BUILT (`#emptyCalloutHeadingBox` + the r524 co-tag patch), four probe readings +0.0109 … +0.0191pp · the "
         "`/loop-stop` arrived mid-design: TOGGLED OFF (both flags enabled:false, 6,432 / 6,432 identical), UNCOMMITTED by design · plateau 2 of 3 (neither).")
# (7) Next session line
ns = one("**Next session starts with:**")
L[ns] = ("**Next session starts with:** `/loop-start` (16 rounds or 10 hours). **The tree is DIRTY BY DESIGN** — `ContentConverter.js`, `TagNormaliser.js`, "
         "`Emit_Templates.json`, `Tag_Lexicon.json` = r541, toggled OFF (both flags enabled:false; the probe read 6,432 / 6,432 identical), named by the s53 "
         "`/loop-stop` — not a crash, not a parallel session; `verify_after_transfer.sh` will FAIL on exactly those engine checksums (census PASS 552 / 545 / "
         "2673 / 2993 / 762). LAST SHIPPED r539 (260620.98); LAST FULL s52-r11 (r534); ledger scoped #5. Round 1 = FINISH OR DECLINE r541 (Position): decide "
         "the run rule and the r529 hand-off from the four readings, keep or drop form B (+0.0012 — XGF down), enable, probe, ship if ≥ +0.02pp or park it; "
         "the plateau is 2 of 3, so a sub-0.02 ship makes 3 of 3. Then a PICK pass led by the `_s53_tagfate.py` rows in Follow-up candidates (s53-r2).")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(out); assert os.path.getsize(tmp) > 50000; os.replace(tmp, S)
io.open(A, "a", encoding="utf-8", newline="\n").write("".join(f"\n## {h}\n\n{b}\n" for h, b in arch))
print("LOOP_STATE", len(s.encode("utf-8")), "->", os.path.getsize(S))
