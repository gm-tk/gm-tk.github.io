#!/usr/bin/env python3
"""s52 stop (§4 BUDGET, 16 of 16 rounds): the s51 STOPPED entry archived verbatim and pointed at; the s52 STOPPED entry; the
session-52 Decisions block; the round-16 Round-log line; the 'Next session starts with' line replaced. Asserts every anchor. WSL."""
import io, os, subprocess
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"; S = os.path.join(R, "LOOP_STATE.md"); A = os.path.join(R, "LOOP_STATE_ARCHIVE.md")
T = subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()
L = io.open(S, encoding="utf-8", newline="").read().split("\n")
def one(pred, what):
    idx = [i for i, l in enumerate(L) if pred(l)]; assert len(idx) == 1, (what, idx); return idx[0]
st51 = one(lambda l: l.startswith("## >>> STOPPED 2026-09-26 14:58 NZST (session 51)"), "s51 stop")
old = L[st51]
stop52 = (f"## >>> STOPPED 2026-09-26 {T} NZST (session 52) on §4 BUDGET — all 16 rounds used (≈ 4 h 40 m of the 10 h). **SEVEN ENGINE ROUNDS "
          "SHIPPED + ONE FULL BACKSTOP, every one committed:** r528 the untagged whakataukī (s51's toggled-OFF build, refined), r529 the summary "
          "heading's alert box, r530 the whakataukī's other writer forms, r531 the bracket fragment in a button label (text-only), r532 the bare "
          "stock-photo URL (→ the To Do note), r533 the bare video URL (→ the embed), r534 the bare link line (→ the To Do note); FULL s52-r11 "
          "(0 pages differ). Eight PICK passes found no other class at the floor (the lanes: the miner + four scoped miners, the placement "
          "census, the loss ledger, the KB queue, the recognition census, the hand-off text census, cs wrapper_set / MISSING splits). Skeleton "
          "**56.1010 → 56.3343 % @ 2486** (+0.2333pp), ≥50 1627 → 1638, ≥75 292 → 305, ≥90 28 → 29, RAW 39.844 → 39.971; cs exact 16830 → "
          "17024 (EXTRA 204 → 198, missing 879 → 661); body ANY 234 → 233; leak 52; **61.4 % of achievable** (ceiling 91.7 %). Plateau 0 of 3. "
          "Needs Chris: #1 / #10 only (human actions). <<<")
assert len(stop52) <= 1500, len(stop52)
L[st51] = stop52 + "\n## STOPPED entry, session 51 (26 Sept 14:58, `/loop-stop`; r522–r526 shipped + the s51-r12 FULL, r528 toggled OFF — finished by s52 Round 1) -> LOOP_STATE_ARCHIVE.md 'STOPPED entry, session 51 (verbatim, s52 stop)'. Superseded by the session-52 entry above; every verdict stands."
d51 = one(lambda l: l.startswith("## Decisions from Chris (session 51 "), "s51 decisions")
L.insert(d51, "## Decisions from Chris (session 52 — 2026-09-26 15:01 → " + T + " NZST): the standing `/loop-start` kickoff only (the default budget, 16 "
              "rounds or 10 hours — the 16 rounds reached first) — NO new numbered decision; no new Needs-Chris item.\n")
rl = one(lambda l: l == "## Round log", "round log")
L.insert(rl + 1, f"- s52-r16 (no engine change, 26 Sept 19:38 → 19:40) · the HAND-OFF lane fresh (`_s43_wl2_run.sh s52` → "
                 "`_s43_widgetloss2_s52.json`, `_s51_r11_wl2sum.py s52`): carousel 133 tag-source parts / 43 modules (video titles and stock "
                 "credits), dropDown 71 (rebuilt questions), clickDrop 36, modal 28 — identical to s51-r11's (no builder changed this session) · "
                 "nothing new at the floor · the §4 BUDGET stop (16 of 16).")
nx = one(lambda l: l.startswith("**Next session starts with:**"), "next line")
L[nx] = ("**Next session starts with:** `/loop-start` (16 rounds or 10 hours). The tree is CLEAN at the s52 stop commit; `verify_after_transfer.sh` "
         "should PASS (census 552 / 545 / 2673 / 2993 / 762). LAST SHIPPED r534 (260620.93); LAST FULL s52-r11 (at 260620.93); ledger scoped #0. "
         "No round in flight. Round 1 = a PICK pass led by the s52 follow-ups (Follow-up candidates s52-r2 / r3 / r8: the `[Alert]` + heading "
         "lane at 13 runs, the whakataukī glued one-line form 7 pages, the video / D2L / other bare-URL leftovers), then the lanes s52 found "
         "empty re-read with a NEW instrument (the s52 lesson: box-level and residue censuses found classes the miner's rows did not).")
assert len(L[nx]) <= 800, len(L[nx])
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## STOPPED entry, session 51 (verbatim, s52 stop)\n\n" + old + "\n")
out = "\n".join(L); tmp = S + ".tmp"
io.open(tmp, "w", encoding="utf-8", newline="").write(out); assert os.path.getsize(tmp) > 60000; os.replace(tmp, S)
print("LOOP_STATE", os.path.getsize(S), "stop entry chars", len(stop52), "next chars", len(L[nx]))
