#!/usr/bin/env python3
"""Session 46 Round 6 — record the PICK pass (no engine change): clear the r496 in-flight marker, archive the PICK section, add the
Round-log line, the declined entry and the follow-up. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
rd = lambda p: io.open(p, encoding="utf-8", newline="").read()
ss = rd(S); L = ss.split("\n"); shutil.copyfile(S, S + ".pre-s46-r6-record.bak")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
i = find("- **ROUND 496 IN FLIGHT — NOT PROVEN**"); marker = L[i]; del L[i]
k = find("## Session 46 — Round 6 PICK (engine r496)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 46 — Round 6 (no engine change) — a PICK pass: the leak mechanisms, the clickDrop refusals, the XDLS choice board "
         "— the record is in LOOP_STATE_ARCHIVE.md 'Session 46 — Round 6 PICK pass (no engine change) + what it found'.\n")
k = find("## Round log")
L.insert(k + 1, "- s46-r6 (no engine change, 25 Sept ≈13:05 → 14:45) · a PICK pass: the leak lane's black `[Image …]` (21 lines) and black "
         "`[Hn]` (17) need a page-item promotion before scanning — recorded; clickDrop's 346 refusals traced (`_s46_r6_cdwhy.sh`); the XDLS "
         "Learning-Support choice board is ALREADY built by r307 / r418 on 30 of 35 pages — the five it refuses each fail differently "
         "(`_s46_trace_cc.cjs`) — recorded · plateau 0 of 3 (neither).")
k = find("## Declined classes")
L.insert(k + 1, "- **Session 46 Round 6 (25 Sept ≈13:05 → 14:45) — a PICK pass, no engine change.** (1) **The literal-tag leak's other "
         "mechanisms** (`_s46_r6_blackimg.cjs`, `BL_RE=head`): black image-request lines 21 / 10 modules (DTC1005 9; 14 with a URL), black `[Hn]` "
         "lines 17 / 12 modules (the gold a heading 6 / p 2 / absent 8) — a black bracket at a paragraph's head would have to be promoted to a "
         "tag item in `PageSplitter.BuildItemStream` before scanning, and a promoted heading inside a widget capture would start splitting "
         "captures: recorded, under the floor. (2) **clickDrop** (`_s46_r6_cdwhy.sh` — every refusal traced, 346 declined / 126 modules): no "
         "delimiter at all 137 (mostly bundles that captured only their opener — the gathering class), the role-word path 55 (the BLL choice "
         "board — `[Clickdrop N Image] same image from BLL110` / `[Clickdrop N text]` + videos + a nested `[carousel]` + the dropbox button, "
         "BLL220 …; a heavy family dialect), items resolved but the render refused 60 (36 XDLS9). (3) **The XDLS Learning-Support choice board** "
         "(`[Click Drop Activity N with embedded image] Label [image … icon from LS global edits]`, XDLS903–906, gold 6 / 6 on all 28 lesson "
         "pages): ALREADY built by r307 / r418 on 30 of 35 XDLS902–906 lesson pages; the prepass declines exactly five (`_s46_trace_cc.cjs`), "
         "each differently — XDLS906 3.0 a `[hover definition] fake light?` member inside a tile scrap, XDLS906 5.0 a `[body] Explain where one "
         "or more of your ancestors came from.` member, XDLS903 1.0 a nameless numbered marker, XDLS904 5.0 / XDLS905 4.0 five free activity "
         "anchors for six tiles (4A / 5E consumed elsewhere) — five pages, four mechanisms: recorded. (4) The XDLS per-activity upload buttons "
         "the gold consolidates into one closing \"Share your learning!\" box — a developer edit (class C).")
k = find("- **(s46-r5) the literal-tag leak after r495")
L.insert(k + 1, "- **(s46-r6) the XDLS choice board's five declined pages (r307 / r418 build the other 30):** XDLS906_3_0 (a `[hover "
         "definition]` member in a tile scrap), XDLS906_5_0 (a `[body]` member), XDLS903_1_0 (a nameless numbered marker), XDLS904_5_0 / "
         "XDLS905_4_0 (5 anchors for 6 tiles) — the family's five lowest-scoring lesson pages (38–49 %); each a small prepass extension "
         "(`ContentConverter.#cdTilePrepass`, lines 7145–7218).")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Session 46 — Round 6 PICK pass (no engine change) + what it found\n\n" + marker.replace("IN FLIGHT — NOT PROVEN", "PICKED, THEN "
    "WITHDRAWN BEFORE ANY CODE (r307 / r418 already build it)") + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **Outcome:** no engine change; r496 unused. The XDLS choice board turned out to be r307 / r418's (30 of 35 pages built); its five "
    "declined pages each fail differently (recorded in Follow-up candidates).\n")
io.open(S, "w", encoding="utf-8", newline="").write("\n".join(L))
print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
