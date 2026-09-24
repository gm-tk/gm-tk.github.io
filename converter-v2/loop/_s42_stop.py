#!/usr/bin/env python3
"""Session 42 STOP (§4 BUDGET — 12 rounds) — LOOP_STATE.md: the Round 12 record, the clock correction, the STOPPED entry at the top (the
s41 entry → a pointer, verbatim to the archive), the session-42 Decisions block (the standing kickoff only), the Position rows r465 /
r466 → archive, and the final 'Next session starts with:' line. .bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
shutil.copyfile(S, S + ".pre-s42-stop.bak")
ss = rd(S); L = ss.split("\n"); arch = []
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
# 1. Round 12 record
k = find("## Declined classes")
L.insert(k + 1, "- **Session 42 Round 12 (24 Sept 16:30 → 16:40) — THE MTK BILINGUAL PAIR ORDER (a PICK pass, no engine change).** The order "
         "census's TRR / PMT reo-before-English rows sized over every Bilingual pair (`outputs/_s42_r12_reoorder.py` → `.log`): Claude's "
         "`<p>` / heading pairs are Māori first (activity 822 + body 1,438 reo-first `<p>` pairs); its ≈ 117 \"English-first\" adjacencies "
         "on ≈ 25 TRR / PMT pages are the probe pairing across uneven paragraph runs (PMT101_1_0 read by eye: reo first throughout) — no "
         "order class; KB c79 / 07D rule 7 already holds.")
k = find("## Round log")
L.insert(k + 1, "- s42-r12 (no engine change, 24 Sept 16:30 → 16:40) · a PICK pass: the MTK bilingual pair order — Māori first throughout, "
         "no class · plateau 2 of 3 (neither) · **the 12-round budget reached → §4 BUDGET stop.**")
# 2. clock correction on the session start line
k = find("**Session 42 started:**")
L[k] += (" **Clock note 2 (16:40):** the ≈ times written on s42-r10 / r11 (17:00 → 17:45) also ran ≈ 45 min ahead — the commits: R9 16:26, "
         "R10 16:32, R11 16:38; the session ran 14:14 → 16:45 (≈ 2 h 30 min).")
# 3. Position rows r466 / r465 → archive
b = [find("- Before it: **r466**"), find("- Before it: **r465**")]
arch.append(("Position — LAST SHIPPED tail r466 / r465 (verbatim, s42 stop)", [L[i] for i in b]))
for i in sorted(b, reverse=True): del L[i]
k = find("- Before it: **r467**")
L.insert(k + 1, "- Before it: **r466** (260620.33, D14-20 the course-code heading, +0.0137pp) and **r465** (260620.32, D14-21 the exclusion, a "
         "population re-base) — the verbatim gate rows → LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED tail r466 / r465 (verbatim, s42 stop)'.")
k = find("- **No round in flight** (24 Sept 2026 17:25 real clock, session 42 Round 10")
L[k] = ("- **No round in flight** (24 Sept 2026 16:45, after the session-42 stop — §4 BUDGET, 12 rounds). LAST SHIPPED **r470** (260620.35); "
        "**LAST FULL = r460**; ledger **scoped #4** (4 of headroom); `git status` clean. Ride-along patches `outputs/_r469_declined.patch` "
        "(alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
# 4. STOPPED entry: the s41 one → archive + pointer; the s42 one on top
k = find("## >>> STOPPED 2026-09-24 12:50 NZST (session 41)")
arch.append(("STOPPED entry, session 41 (verbatim, s42 stop)", [L[k]]))
L[k] = ("## STOPPED entry, session 41 (24 Sept 12:50, `/loop-stop`; r453–r461 shipped) -> LOOP_STATE_ARCHIVE.md 'STOPPED entry, session 41 "
        "(verbatim, s42 stop)'. Superseded by the session-42 entry above; every verdict stands.")
L.insert(k, "## >>> STOPPED 2026-09-24 16:45 NZST (session 42) on §4 BUDGET — the 12-round default reached (≈ 2 h 30 min; the 10 h cap not "
         "reached). **FOUR ENGINE ROUNDS SHIPPED + ONE GATE-CONFIGURATION ROUND, every one committed:** r465 D14-21 (four no-source modules "
         "out of the scored population); r466 D14-20 (the MTK course-code heading dropped, 22 pages); r467 KB c67 the canonical Standards "
         "tab (42 modules — the placement census's first find); r470 TRR115 converts (the table-cell title bar recognises its Writers "
         "Template). **Two instrument rounds:** the §1g PLACEMENT CENSUS built (`outputs/_placement_census.py`, + an ORDER census). "
         "**Declined:** r468, r469 / r469b (ride-along patches kept), r471; three PICK passes. Skeleton **54.9477 % @ 2524 → 55.2245 % @ "
         "2491** (population re-bases: −37 pairs r465, +4 r470; the fixed-population move +0.0137pp r466), ≥50 1581 → 1576, ≥75 275 → "
         "276, RAW 38.975 → 39.194; cs exact 16719 → 16757; body ANY 239 → 238; 60.2 % of achievable (ceiling 91.7 %). Plateau 2 of 3. "
         "Needs Chris: #17–#19 + NEW #22. <<<")
# 5. Decisions block for session 42
k = find("## Decisions from Chris (session 41, AFTER the stop")
L.insert(k, "## Decisions from Chris (session 42 — 2026-09-24 14:14 → 16:45 NZST): the standing `/loop-start` kickoff only (default budget, 12 "
         "rounds or 10 hours) — NO new numbered decision. The D14 queue it carried was actioned: D14-21 → r465, D14-20 → r466, D14-S1 → "
         "the §1g placement census (built, run, its first find shipped as r467). One new Needs-Chris item raised (#22, the BLL2xx Knowledge / "
         "Practices tabs).")
L.insert(k + 1, "")
# 6. next-session line
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** the standing `/loop-start`. Health check: census 552 / 545 / **2,679** pages / **2,491** pairs; "
        "`git status` CLEAN. LAST SHIPPED **r470** (260620.35); LAST FULL = **r460**; ledger scoped #4; plateau **2 of 3**. First: re-run "
        "the miner + the placement census (`outputs/_placement_census.py`, now with its ORDER section) and take the PICK; the lanes this "
        "session exhausted are listed in its Declined entries (s42-r5 → r12). Ride-along patches `_r469_declined.patch` (alerts) / "
        "`_r469b_declined.patch` (buttons) / `_r468_declined.patch` (lesson menu). Needs Chris #17–#19, #22 (`/loop-decisions`).")
with io.open(A, "a", encoding="utf-8", newline="\n") as f:
    for title, lines in arch: f.write("\n## " + title + "\n\n" + "\n".join(lines).rstrip() + "\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
