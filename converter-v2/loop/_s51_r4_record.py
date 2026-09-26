#!/usr/bin/env python3
"""_s51_r4_record.py — session 51 Round 4: r524 DECLINED on measurement. Clears the in-flight marker (the prior no-round line
restored), archives the marker verbatim, adds the Declined entry, the ride-along note and the Round-log line. WSL."""
import io, os, re, shutil, subprocess
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
T = subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s51-r4-record.bak"))
L = io.open(S, encoding="utf-8", newline="").read().split("\n")
mk = [i for i, l in enumerate(L) if l.startswith("- **ROUND 524 IN FLIGHT — NOT PROVEN")]; assert len(mk) == 1
bf = [i for i, l in enumerate(L) if l.startswith("- **Before r524: no round in flight**")]; assert len(bf) == 1
marker = L[mk[0]]
L[bf[0]] = L[bf[0]].replace("- **Before r524: no round in flight**", "- **No round in flight**", 1)
L[bf[0]] = L[bf[0]].replace("Checked at r523: none rides", "`_r524_declined.patch` (the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list that follows its title) is parked. Checked at r523: none rides", 1)
del L[mk[0]]
dc = [i for i, l in enumerate(L) if l.startswith("## Declined classes")]; assert len(dc) == 1
L.insert(dc[0] + 1, "- **Session 51 Round 4 (26 Sept 12:31 → " + T + ") — a PICK pass, then engine r524 BUILT, PROBED and DECLINED on measurement.** "
         "(1) **r524 — a callout governs a heading co-tag** (`[Alert] [H2] Key questions`, XGF9001–9006; `[Important] [H3] Step 1 …`, CEDT501 — "
         "76 spans / 18 modules; the gold boxes the heading in an alert on 38 of 48 matched; r523's `activity_heading_cotag` + a `callouts` sub-rule, "
         "env `CALLOUTHDCOTAG_OFF`): probe OFF 0 / ON **17 modules**, pre-score **+0.0006pp, 17 up / 21 down** — the alert opens but its STRICT run "
         "holds only the title line (`div.alert > p`), so the list the gold keeps inside it stays free, and a callout closes an open activity "
         "(XGF9001_4_0: 4C cut, −2.8). Backed out (`git apply -R`), parked as `outputs/_r524_declined.patch`; corpus 0 pages differ; no ledger record. "
         "Re-open with the alert's run extended over the list after its title. (2) The unboxed gold boxes' writer forms (`_s51_r4_unboxform.py`, "
         "1,065 boxes): 194 plain `[body]` + 163 plain `[Hn]` sections the developer boxed with no writer tag — diffuse (class C); "
         "(3) activity spans another tag wins (`_s51_r4_actlost.cjs`, 1,737): the widget co-tags are the round-92 form; the ELEMENT winners "
         "(image 78 = `[Interactive image]` requests, video 54, the single-bracket `[H3 Activity 1C]` ≈ 5 modules) — below the floor.")
rl = [i for i, l in enumerate(L) if l.startswith("## Round log")]; assert len(rl) == 1
L.insert(rl[0] + 1, f"- s51-r4 (engine r524, 26 Sept 12:31 → {T}) · a PICK pass (the unboxed forms — class C; the activity spans lost to another "
         "tag; the containers lost to a heading) then A CALLOUT GOVERNS A HEADING CO-TAG · DECLINED on measurement (+0.0006pp, 17 up / 21 down — "
         "the alert's strict run holds only its title) · backed out, patch `_r524_declined.patch`, corpus 0 pages differ · plateau 0 of 3 (neither).")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 51 — r524 PICK (the in-flight marker, verbatim) — DECLINED\n\n" + marker + "\n")
io.open(S, "w", encoding="utf-8", newline="").write("\n".join(L))
print("LOOP_STATE", os.path.getsize(S))
