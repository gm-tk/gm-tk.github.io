#!/usr/bin/env python3
"""Session 45 — §5d condense #1 (LOOP_STATE.md 95.6 KB at the start, target <= 100 KB with a session's headroom) + the
session-45 start note. Moves verbatim to LOOP_STATE_ARCHIVE.md: the session-44 start note, the Position 'Before them' list,
the Standing-facts AppVersion history, the session-43 Rounds 3-6 declined entries. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s45-condense1.bak")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
TAG = "(verbatim, s45 §5d condense #1)"
arch = []
# 1. session-44 start note
i = find("**Session 44 started:**")
arch += ["## Session start note 44 " + TAG, "", L[i], ""]
L[i] = ("**Session 44 started:** 24 Sept 23:33 (Opus 5.5) — started DIRTY with s43's toggled-OFF r478 (named in Position, not a crash), "
        "finished it as Round 1; r478–r485 shipped + the FULL backstop (Round 7), three PICK passes; §4 BUDGET stop at 03:25. "
        "Verbatim → LOOP_STATE_ARCHIVE.md 'Session start note 44 " + TAG + "'.")
# 2. Position 'Before them' list
i = find("- Before them: **r483**")
arch += ["## Position — Before-them list r483 → r451 " + TAG, "", L[i], ""]
L[i] = ("- Before them: **r483 → r467** (260620.47 → 260620.34 — KB c38 autoCheck, KB 07D lesson-title h2, the MTK data-row hand-off, KB 07B "
        "one-box activity / whakatauki box, KB c75 ×4, KB c52 iStock alt, the modal / flip-card guards, TRR115, KB c67 Standards tab) and "
        "**r461 → r451** — each round's LAST SHIPPED block is verbatim in LOOP_STATE_ARCHIVE.md under 'Position — LAST SHIPPED rNNN' (grep the "
        "round); the full pointer list → 'Position — Before-them list r483 → r451 " + TAG + "'.")
# 3. Standing facts AppVersion history
i = find("- Standing facts: AppVersion 260620.49")
arch += ["## Position — Standing facts AppVersion history 260620.49 → 260620.30 " + TAG, "", L[i], ""]
L[i] = ("- Standing facts: AppVersion **260620.49** (r485 the title-bar language split — session 44 Round 11, 25 Sept); the history "
        "260620.48 → 260620.30 (r484 → r460, one build per shipped round) → LOOP_STATE_ARCHIVE.md 'Position — Standing facts AppVersion "
        "history 260620.49 → 260620.30 " + TAG + "', and 260620.29 and older → 'Position — Standing facts AppVersion history 260620.29 → "
        "260620.18 (verbatim, s42 §5d condense #2)'; every toggle is listed in OPERATING_GUIDE.md §11; the engine + gate checksum manifests "
        "(`_MIGRATION/CHECKSUMS__engine.txt` / `CHECKSUMS__gates.txt`) are refreshed at every ship (a `.pre-rNNN.bak` copy kept).")
# 4. session-43 Rounds 6 / 5 / 4 / 3 declined entries (consecutive)
i6 = find("- **Session 43 Round 6 (24 Sept"); i5 = find("- **Session 43 Round 5 PICK pass"); i4 = find("- **Session 43 Round 4 (24 Sept")
i3 = find("- **Session 43 Round 3 (24 Sept"); assert [i5, i4, i3] == [i6 + 1, i6 + 2, i6 + 3]
arch += ["## Declined classes — session 43 Rounds 3 / 4 / 5 / 6 " + TAG, ""] + L[i6:i3 + 1] + [""]
L[i6:i3 + 1] = [
    "- **Session 43 declined classes, Rounds 3 / 4 / 5 / 6 (PICK passes, no engine change: R6 the KB audit's PARTIAL rows — c41 `captionText` "
    "not derivable by position (≈ 2–3 %), the pasted-picture generic src (class C), Phase 3b recorded; R5 the PES1 / XDLS9 scoped miners, "
    "miner #568 the AGH journal-instruction box (no single target), #828 the XDLS `activity dropbox` (mixed forms); R4 the whole-unit "
    "content-loss census `_s43_r4_lostunits.py` (664 of 87,905 units lost, scattered — no class), the unbracketed supervisor note (≈ 17 notes, "
    "below floor), `body:panel:activity → free` (class C); R3 the widget text-loss residue (media labels / single modules) and census row "
    "`menu:Information → menu:Overview` — KB 01B: Claude correct for 13 non-MTK modules (NAMED), the 8 MTK LI-tab modules below floor)** → "
    "LOOP_STATE_ARCHIVE.md 'Declined classes — session 43 Rounds 3 / 4 / 5 / 6 " + TAG + "'; every verdict stands."]
# 5. session-45 start note, after the session-44 one
i = find("**Session 44 started:**")
L.insert(i + 1, "**Session 45 started:** 2026-09-25 05:14 NZST (Claude Code, Opus 5.5). Budget: **12 rounds or 10 hours** (the `/loop-start` "
         "default → ends ≈ 15:14). **Health check CLEAN:** `git status` clean at f517770; `verify_after_transfer.sh` PASS (census 552 / 545 / "
         "2679 / 2993 / 762 / 33 / 24 EXACT — no intake trigger (a)); §0 (b) the 7 gold-only dirs = the no-source list, (c) 0 docx newer than "
         "its `_run.json`, (d) no staging folder newer than `_INTAKE_AUDIT_2026-09-19.md`; no git locks; the Amended line present (1); KB HEAD "
         "`910a9cb` = the status file's (unchanged). LOOP_STATE 95.6 KB → §5d condense #1 at once. `DIFF_QUEUE.md` 03:20 = the r485 corpus "
         "(195 CANDIDATE; no page newer) — current, no Round 0c. No round in flight; nothing SHIPPED INERT.")
ns = "\n".join(L)
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write(ns); os.replace(S + ".tmp", S)
sa = rd(A)
io.open(A, "a", encoding="utf-8", newline="").write(("" if sa.endswith("\n") else "\n") + "\n" + "\n".join(arch) + "\n")
print("LOOP_STATE", len(ss.encode()), "->", len(ns.encode()), "bytes; archive +", len("\n".join(arch).encode()))
