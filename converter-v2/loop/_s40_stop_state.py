"""SESSION 40 STOP (§4 BUDGET, after Round 12 — the FULL backstop) — the LOOP_STATE.md finalise + STOPPED record (written with the Write
tool; run under WSL from FINAL_MODULE_DATA). Each prefix must match exactly once or nothing is written. The s39 STOPPED entry MOVES
verbatim to the archive (a pointer stays). Deletes nothing."""
import io, sys

S, A = "LOOP_STATE.md", "LOOP_STATE_ARCHIVE.md"
src = io.open(S, encoding="utf-8", newline="").read()
lines = src.split("\n")


def find(prefix):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        sys.exit(f"prefix {prefix[:60]!r} matched {len(hits)} lines")
    return hits[0]


# 1. the in-flight marker -> no round in flight (the stop)
i = find("- **ROUND 12 IN FLIGHT — NOT PROVEN**")
lines[i] = ("- **No round in flight** (24 Sept 2026 05:30, session 40 STOPPED on §4 BUDGET after Round 12). LAST SHIPPED **r452** "
            "(260620.23); **LAST FULL = the r452 state** — s40-r12, the ledger's backstop: all 545 regenerated with the r452 engine, "
            "byte-identical to the scoped-shipped corpus, every gate EXACT; `_ship_ledger.py record-full --round 452`, **scoped #0 "
            "(8 of headroom)**. The §3 step-1 rule stands (s40-r11, a decline with no code, raised no marker — recorded).")

# 2. plateau
i = find("- Plateau window (§4): **2 of 3** — s40-r10")
lines[i] = lines[i].replace("- Plateau window (§4): **2 of 3** — s40-r10",
                            "- Plateau window (§4): **2 of 3** — s40-r12 the FULL backstop (no engine change: neither counts nor resets); "
                            "s40-r11 declined (neither); s40-r10", 1)

# 3. round log
i = find("- s40-r11 ")
lines.insert(i, "- s40-r12 (no engine change — THE LEDGER'S FULL-SHIP BACKSTOP, 24 Sept 04:58 → 05:26) · all 545 regenerated with the r452 "
                "engine (42 batches, 4 workers, 6.5 min, all rc 0): 0 stale, 542 / 542 modules byte-identical to the manifest; every gate "
                "EXACT (skeleton 54.7484 % @ 2477, 0 movers; cs / body / clean / leak held; 10 ✓; selftests 50 / 0; the miner 195) · "
                "ledger record-full (round 452) → scoped #0.")

# 4. the STOPPED entry at the top; the s39 one moves to the archive
i = find("## >>> STOPPED 2026-09-23 18:25 NZST (session 39)")
s39 = lines[i]
lines[i] = ("## >>> STOPPED 2026-09-24 05:30 NZST (session 40) on §4 BUDGET — 12 of 12 rounds in ≈ 5 h (the 10 h cap not reached). "
            "**SIX ENGINE ROUNDS SHIPPED, r447–r452, every one committed:** r447 D13-5 the journal button; r448 D13-4 the answer-key "
            "carry-through; r449 D13-4 the typing quiz shape 1; r450 the claude-audit Phase 3b (inert SGP); r451 the bilingual section "
            "bundle's hand-off box (body ANY 260 → 237); r452 D13-5 the invented journal button (+0.0077pp, ≥50 +2). **Four DECLINED on "
            "measurement** (the mcq kickoff, the `[RHS alert]` family, the remaining quiz types, the stock-image caption); **one "
            "measurement-tool round** (the dashboard's quiz rows — coverage RE-BASED 50.8 → 44.9 %); **Round 12 the FULL backstop** (all "
            "545 byte-identical; ledger reset). Skeleton **54.7726 % @ 2476 → 54.7484 % @ 2477** (−0.024pp on a changed population — "
            "r447's decided D13-5 override −0.0317pp, every dip named), ≥50 1542 → 1544; body 260 → 237; every other gate held; 60.1 % "
            "of achievable. Plateau 2 of 3. Needs Chris: #17, #18 (new), #19 (new). Tree clean at the stop commit. <<<")
lines.insert(i + 1, "## STOPPED entry, session 39 (23 Sept 18:25, `/loop-stop`; eight rounds r439–r446 shipped) -> LOOP_STATE_ARCHIVE.md "
                    "'STOPPED entry, session 39 (verbatim, s40 stop)'. Superseded by the session-40 entry above; every verdict stands.")

# 5. Decisions from Chris (session 40)
i = find("## Decisions from Chris (session 39")
lines.insert(i, "## Decisions from Chris (session 40 — 2026-09-24 00:27 → 05:30 NZST): the standing `/loop-start` kickoff only (default "
                "budget, 12 rounds or 10 hours) — NO new numbered decision. Two new Needs-Chris items were raised (#18 the `[RHS alert]` "
                "family, #19 the unannounced highlights — `DECISIONS__Pending_2026-09-24.md`).")
lines.insert(i + 1, "")

# 6. the Next-session line
i = find("**Next session starts with:**")
lines[i] = ("**Next session starts with:** the standing `/loop-start` (health check: census 552 / 545 / **2,666** pages / **2,477** pairs; "
            "`git status` CLEAN at the last commit). No round in flight; LAST SHIPPED **r452** (260620.23); LAST FULL = the **r452 state** "
            "(the s40-r12 backstop; ledger scoped #0, 8 of headroom); plateau **2 of 3**. D13-4 and the claude-audit kickoff are "
            "dispositioned. Open lanes: the follow-ups (the iStock-href buttons; the r451 empty-box residue + TRR301_3_0's capture; the "
            "r452 residue — bare / bracket-led `[Button]` still 'Go to your journal'); Needs Chris #17 / #18 / #19 (a `/loop-decisions` "
            "session would unlock #19's ≈ 190 highlight boxes).")

arch = io.open(A, encoding="utf-8", newline="").read().rstrip("\n") + "\n\n## STOPPED entry, session 39 (verbatim, s40 stop)\n" + s39 + "\n"
io.open(A + ".new", "w", encoding="utf-8", newline="").write(arch)
out = "\n".join(lines)
io.open(S + ".new", "w", encoding="utf-8", newline="").write(out)
print("state", len(src.encode()), "->", len(out.encode()), "| next line", len(lines[i]), "chars")
