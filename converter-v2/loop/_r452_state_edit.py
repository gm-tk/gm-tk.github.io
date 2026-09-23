"""ROUND 452 (session 40 Round 9) — the LOOP_STATE.md finalise edits + the §5d archive move (written with the Write tool; run under
WSL from FINAL_MODULE_DATA). Each prefix must match exactly once or nothing is written. Moves verbatim, deletes nothing."""
import io, sys

S, A = "LOOP_STATE.md", "LOOP_STATE_ARCHIVE.md"
src = io.open(S, encoding="utf-8", newline="").read()
lines = src.split("\n")


def find(prefix):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        sys.exit(f"prefix {prefix[:60]!r} matched {len(hits)} lines")
    return hits[0]


# 1. in-flight marker -> no round in flight
i = find("- **ROUND 452 IN FLIGHT — NOT PROVEN**")
lines[i] = ("- **No round in flight** (24 Sept 2026 04:45, session 40 Round 9 SHIPPED r452; the corpus on disk IS the r452 state, "
            "LAST SHIPPED r452, LAST FULL r444, ledger scoped #7 — 1 of headroom: **the next engine ship should be the FULL backstop**). "
            "The §3 step-1 rule stands (r452 raised its marker at ≈04:15 real time, before its first edit — the '04:38' written in it "
            "was a clock slip).")

# 2. LAST SHIPPED r452; r451 becomes "Before it"; the r450 / r449 "Before it" bullets move to the archive
i = find("- LAST SHIPPED: **r451**")
old451 = lines[i]
lines[i] = ("- LAST SHIPPED: **r452** (build 260620.23, 24 Sept 04:45, session 40 Round 9 — A WRITER INSTRUCTION THAT MENTIONS A BUTTON "
            "IS NOT A JOURNAL BUTTON, Chris's D13-5, `JDEFGUARD_OFF`; 43 files / 29 modules; SCOPED, **scoped #7 since the r444 FULL "
            "(1 of headroom)**; **skeleton 54.7484 % @ 2477 (+0.0077pp; 35 up / 5 down — the five HIS dips NAMED)**, **≥50 1544** "
            "(+2), ≥75 260, ≥90 23, RAW 38.649 %; cs 15657 / 199 / 796 / 24; body 58 / 5 / 176 / 237; clean 2613 / 2658; leak 75 / 45; "
            "`gate_baseline.json` at r452; `outputs/_r452_sk_final.json`; 60.1 % of achievable; the miner 195 CANDIDATE).")
lines.insert(i + 1, "- Before it " + old451[len("- LAST SHIPPED: "):])
tail = []
for pre in ("- Before it **r450**", "- Before it **r449**"):
    j = find(pre)
    tail.append(lines[j])
    del lines[j]
b = find("- Before it: **r448**")
lines[b] = lines[b].replace("- Before it: **r448**",
                            "- Before it: **r450** (260620.21, the inert SGP refresh) and **r449** (260620.20, the typing quiz shape 1, "
                            "−0.0002pp named) — the verbatim gate rows → LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED tail r450 / r449 "
                            "(verbatim, s40 §5d condense #3)'; **r448**", 1)

# 3. plateau
i = find("- Plateau window (§4): **1 of 3** — r451")
lines[i] = lines[i].replace("- Plateau window (§4): **1 of 3** — r451",
                            "- Plateau window (§4): **2 of 3** — r452 predicted a skeleton move and delivered +0.0077pp (≥50 +2), under "
                            "the 0.02pp line: counted as NOT moving (conservative); r451", 1)

# 4. standing facts
i = find("- Standing facts: AppVersion 260620.22 (")
lines[i] = lines[i].replace("- Standing facts: AppVersion 260620.22 (",
                            "- Standing facts: AppVersion 260620.23 (r452 the invented journal button — D13-5, session 40 Round 9, "
                            "24 Sept); before it 260620.22 (", 1)

# 5. round log
i = find("- s40-r8 ")
lines.insert(i, "- s40-r9 (engine r452, build 260620.23, 24 Sept 04:10 → 04:45) · A WRITER INSTRUCTION THAT MENTIONS A BUTTON IS NOT A "
                "JOURNAL BUTTON (D13-5; the r447 follow-up re-measured — 0 journal buttons inside bundles, but 178 buttons ship a label "
                "the writer never typed, 117 'Go to your journal') · `JDEFGUARD_OFF`, 43 files / 29 modules · SHIPPED · scaffold "
                "54.7407 → 54.7484 (+0.0077pp, 35 up / 5 down named), ≥50 +2 · scoped #7.")

# 6. the PICK section -> archive, pointer left
s = find("## Session 40 — Round 9 PICK (engine r452)")
e = next(k for k in range(s + 1, len(lines)) if lines[k].startswith("## "))
pick = lines[s:e]
while pick and pick[-1].strip() == "":
    pick.pop()
lines[s:e] = ["## Session 40 — Round 9 (engine r452, build 260620.23) — A WRITER INSTRUCTION THAT MENTIONS A BUTTON IS NOT A JOURNAL "
              "BUTTON — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 40 — Round 9 PICK (engine r452) + "
              "what shipped'; the one-line summary is the s40-r9 Round-log line below.", ""]

# 7. the follow-up list: the r447 journal-button item is dispositioned
i = find("- **(r447) Journal buttons INSIDE a widget bundle keep the green button.**")
lines[i] = ("- ~~**(r447) Journal buttons INSIDE a widget bundle keep the green button.**~~ → **DISPOSITIONED s40-r9:** 0 sit inside a "
            "bundle (`_s40_r9_journalbtn.py`); the real class was the invented journal default — SHIPPED r452. **Left (below floor / "
            "a button the writer asked for):** 24 bare `[Button]` + ~13 bracket-led requests ('[Insert button to website]', '[Create "
            "check button]', '[Button - click here - link to come]') still read 'Go to your journal' — the gold's label for a bare "
            "`[Button]` is mixed (AGH1003 'Go to journal'); and 23 URL-bearing defaults on internal hosts (`_s40_r9_jd_journal.tsv`).")

arch = io.open(A, encoding="utf-8", newline="").read()
add = ["", "## Session 40 — Round 9 PICK (engine r452) + what shipped (moved from LOOP_STATE.md at the r452 finalise, 24 Sept 2026)"]
add += pick[1:]
add += ["- **What shipped (r452, build 260620.23, 24 Sept 04:45):** `Emit_Templates.buttons.journal_default_guard` {enabled, "
        "bare_match (a PREFIX — the first draft's whole-bracket form took PHE1003's '[Button - click here - link to come]', −1.8 on its "
        "page), keep_match 'journal'}, env `JDEFGUARD_OFF`; the guard sits at the button seam before the r338 external step. Probe OFF "
        "3208 / 3208; ON 43 files / 29 modules; pre-score 40 movers 35 up / 5 down pp-sum +19.1; scoped regeneration of the 29 + 12 "
        "spot-check (12 / 12), 0 truly stale, disk = ON 227 / 227; scoped ship PASS (#7): SCAFFOLD 54.7407 → 54.7484 (+0.0077pp), ≥50 "
        "1542 → 1544, cs / body / clean / leak EXACT; every verifier ✓; selftests 50 / 0; the miner 195 (differing lines 278,074 → "
        "277,989). Logs `outputs/_r452_*`, `outputs/_s40_r9_*`."]
add += ["", "## Position — LAST SHIPPED tail r450 / r449 (verbatim, s40 §5d condense #3)"] + tail
arch = arch.rstrip("\n") + "\n" + "\n".join(add) + "\n"
io.open(A + ".new", "w", encoding="utf-8", newline="").write(arch)
out = "\n".join(lines)
io.open(S + ".new", "w", encoding="utf-8", newline="").write(out)
print("state", len(src.encode()), "->", len(out.encode()))
