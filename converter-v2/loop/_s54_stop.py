#!/usr/bin/env python3
"""_s54_stop.py — session 54's §4 EXHAUSTION stop: the s54-r9 Round-log line, the (s54-r3…r9) follow-up entry, the STOPPED entry (s53's moved
verbatim to the archive, a pointer left), the 'Next session starts with' line. WSL."""
import io, os, re, shutil, subprocess
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
T = subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()
s = io.open(S, encoding="utf-8", newline="").read(); L = s.split("\n")
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s54-stop.bak"))
def idx(pfx):
    j = [i for i, l in enumerate(L) if l.startswith(pfx)]; assert len(j) == 1, (pfx, j); return j[0]
# 1. the s53 STOPPED entry → archive, pointer
i53 = idx("## >>> STOPPED 2026-09-27 01:26 NZST (session 53)")
s53 = L[i53]
L[i53] = ("## STOPPED entry, session 53 (27 Sept 01:26, `/loop-stop`; r535–r539 shipped, r540 parked, r541 toggled OFF — finished by s54 Round 1) -> "
          "LOOP_STATE_ARCHIVE.md 'STOPPED entry, session 53 (verbatim, s54 stop)'. Superseded by the session-54 entry above; every verdict stands.")
stop = (f"## >>> STOPPED 2026-09-27 {T} NZDT (session 54) on §4 EXHAUSTION (9 of 16 rounds, ≈ 3 h 30 m of the 10 h). **FOUR ENGINE ROUNDS SHIPPED + the FULL "
        "backstop, every one committed:** r541 the alert whose title is a heading (s53's toggled-OFF round finished: +0.0183pp, cs exact +38 / missing −80), "
        "r542 the drag-and-drop label row (17 widgets), r543 the marked category sort (21), r544 the red answer column (21); s54-r5 the FULL backstop "
        "(0 pages differ). Skeleton **56.3799 → 56.3998 % @ 2486**, ≥50 1645 → 1648, ≥75 305 → 309, RAW 40.028 → 40.152; cs exact 17024 → 17062 / "
        "EXTRA 198 → 206 / missing 661 → 581; body ANY 233; **61.5 % of achievable** (ceiling 91.7 %); interactive coverage 45.6 → 46.4 % (drag-and-drop "
        "built 146 → 205). **The seven §4 lanes, each run fresh:** miner 198 CANDIDATE (each a recorded verdict / decided lane); KB queue — no NOT CAPTURED "
        "≥ 20; hand-off text = s52's; recognition 3,245 (templates; PWY's one-cell tables 20); the 4 parked flags (< +0.01pp); loss ledger (TRR = KB c93); "
        "placement census (class C). Widget rows: every type measured (Follow-up s54-r3…r9) — answer-less, image-bound or < 20 pages. Needs Chris: #1 / #10. <<<")
L.insert(i53, stop)
# 2. the Round-log line
rl = idx("## Round log")
L.insert(rl + 1, f"- s54-r9 (no engine change, 27 Sept ≈06:00 → {T} NZDT) · the last PICK pass + the §4 exhaustion test: a NEW instrument, the image's fate "
                 "by stock id (`_s54_r9_imgfate.py`: of Claude's main-column pictures the gold also shows, main 410 / side 304 / widget 235 — side ≥ 0.60 only "
                 "ARFUN 0.64, BLL 0.76 (one scaffold picture, the closing party popper, in per-module wrappers — `_s54_r9_popper.py`, no variant > 0.30), ENFUN "
                 "0.76, BLLR 0.62; each < 20 pages in its own form); every remaining widget type's refusals (Follow-up s54-r3…r9) · §4 EXHAUSTION declared · "
                 "plateau 0 of 3.")
# 3. the follow-up entry
fu = idx("## Follow-up candidates surfaced by Round 1")
L.insert(fu + 1, "- **(s54-r3…r9) the widget lane after r542–r544 + the image-fate census — what a later session starts from** (`outputs/_s54_r3_ddtable.cjs` "
                 "(a Build hook: every refused single-table drag-and-drop with its rows) + `_s54_r4_ddlayout.py` (a new widget's layout vs the gold's by shared "
                 "drags) + `_s54_r3_btnblock.cjs` (the button blocker simulated) + `_s54_r9_imgfate.py`): drag-and-drop 557 single-table refusals left — plain "
                 "black 2-column 56 (member / media / empty-cell mix), the `[Qn]` / `[correct]` answer-key marker tables 53 / 45 pages in FIVE conventions (one "
                 "marker-aware reader could take them together), the image column sort 17 / 12 pages (BLL phonics, stock links), the no-table prose 374 (157 "
                 "carry < 2 red answers — no key); flip card 356 (image fronts from non-stock page links; bold-lead faces mixed); carousel 350 (BLL video "
                 "carousels BUILT but uncaptioned — the gold's caption 373 / 1,114 video items, no consensus; the prose carousels carry no slide markers); "
                 "click-and-drop 582 (XDLS choice-board residue 185 / 30 pages, image tiles); accordion 363 / modal 245 / tabs 142 (foreign-tag mixes; modal "
                 "= A1 substitutions — BLL activity boxes, XGF MCQs); dropDown 411 / typing 253 / MCQ 543 (answer-unmarked — D13-4 / D15-19); self-check 255 "
                 "(BLL picture phonics 81); speech bubble 115. Side-column pictures by family (ARFUN `col-md-3 offset-md-0` right; BLL popper left, per-module "
                 "widths; ENFUN 0.76) and the family dialects ANZH `[Important]` → activity 12 pages, PES `[H2]` 13 — each under the floor alone.")
# 4. the next-session line
ns = idx("**Next session starts with:**")
L[ns] = ("**Next session starts with:** `/loop-start` (16 rounds or 10 hours). The tree is CLEAN (the s54 stop commit); LAST SHIPPED r544 (260621.02); "
         "LAST FULL r542 (the s54-r5 backstop); ledger scoped #2. Session 54 stopped on §4 EXHAUSTION — it holds only until a NEW instrument finds a "
         "class, the pattern every earlier exhaustion followed: open with a PICK pass that builds one (e.g. a marker-aware reader over the 53 `[Qn]` / "
         "`[correct]` answer-key drag-and-drop tables; a per-family side-column picture rule — ARFUN / ENFUN / BLL; a heading-level census per family "
         "after r536–r539), then the widget-build lane's next type by D10-3's order. Needs Chris: #1 / #10 only (human actions).")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(out); assert os.path.getsize(tmp) > 50000; os.replace(tmp, S)
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## STOPPED entry, session 53 (verbatim, s54 stop)\n\n" + s53 + "\n")
print("LOOP_STATE", len(s.encode("utf-8")), "->", os.path.getsize(S), "| STOPPED entry chars:", len(stop))
