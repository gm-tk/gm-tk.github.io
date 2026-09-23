"""ROUND 451 (session 40 Round 8) — the finalise-step §5d move (written with the Write tool; run under WSL from FINAL_MODULE_DATA).
(1) the '## Session 40 — Round 8 PICK (engine r451)' section MOVES to LOOP_STATE_ARCHIVE.md with a what-shipped line, leaving the
one-line pointer heading the other rounds use; (2) the Position bullets 'Before it **r448**' and 'Before it **r447**' MOVE verbatim to
an archive section 'Position — LAST SHIPPED tail r448 / r447 (verbatim, s40 §5d condense #2)', named from the 'Before it: **r446**'
bullet. Every text moved is appended verbatim; nothing is deleted. Writes .new files; the caller moves them over."""
import io, sys

S, A = "LOOP_STATE.md", "LOOP_STATE_ARCHIVE.md"
src = io.open(S, encoding="utf-8", newline="").read()
lines = src.split("\n")

# (1) the PICK section
start = [i for i, l in enumerate(lines) if l.startswith("## Session 40 — Round 8 PICK (engine r451)")]
if len(start) != 1:
    sys.exit("PICK heading not unique")
s = start[0]
e = next(i for i in range(s + 1, len(lines)) if lines[i].startswith("## "))
pick = lines[s:e]
while pick and pick[-1].strip() == "":
    pick.pop()
pointer = ("## Session 40 — Round 8 (engine r451, build 260620.22) — THE BILINGUAL SECTION'S WIDGET BUNDLE TAKES THE STANDARD HAND-OFF BOX "
           "— SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 40 — Round 8 PICK (engine r451) + what shipped'; "
           "the one-line summary is the s40-r8 Round-log line below.")
lines[s:e] = [pointer, ""]

# (2) the Position tail
tail_idx = [i for i, l in enumerate(lines) if l.startswith("- Before it **r448**") or l.startswith("- Before it **r447**")]
if len(tail_idx) != 2:
    sys.exit(f"Position tail bullets found {len(tail_idx)}")
tail = [lines[i] for i in tail_idx]
for i in sorted(tail_idx, reverse=True):
    del lines[i]
b = [i for i, l in enumerate(lines) if l.startswith("- Before it: **r446**")]
if len(b) != 1:
    sys.exit("r446 bullet not unique")
lines[b[0]] = lines[b[0]].replace("- Before it: **r446**",
                                  "- Before it: **r448** (260620.19, the answer-key carry-through, D13-4, gate-neutral) and **r447** (260620.18, "
                                  "the journal button, D13-5, −0.0317pp named) — the verbatim gate rows → LOOP_STATE_ARCHIVE.md 'Position — LAST "
                                  "SHIPPED tail r448 / r447 (verbatim, s40 §5d condense #2)'; **r446**", 1)

arch = io.open(A, encoding="utf-8", newline="").read()
add = ["", "## Session 40 — Round 8 PICK (engine r451) + what shipped (moved from LOOP_STATE.md at the r451 finalise, 24 Sept 2026)"]
add += pick[1:]
add += ["- **What shipped (r451, build 260620.22, 24 Sept 04:10):** `elements.dual_language.section_grouping.bundle_handoff` "
        "{enabled: true}, env `BILHANDOFF_OFF`; `BilingualBuilder.bilingualSection(…, handoff)` + `ContentConverter.#interactivePlaceholder("
        "bundle, run, { handoffOnly: true })`. Probe OFF 3208 / 3208 identical; ON 50 files / 15 modules (95 `bilingual-unbuilt` → 95 "
        "`cv2-int-ref`, empty tables 61 → 0); scoped regeneration of the 23 Bilingual modules + 12 spot-check (12 / 12 identical), 0 truly "
        "stale, disk = ON 75 / 75; scoped ship PASS (#6 since r444): SCAFFOLD 54.7407 +0.0000pp (0 movers), RAW −0.051pp NAMED, cs EXACT, "
        "body ANY 260 → 237 / EMPTY 200 → 176 / over-capture 57 → 58 NAMED (TRR301_3_0 EMPTY → visible), clean / leak EXACT, every verifier ✓, "
        "selftests 50 / 0 FAIL, the miner 195 CANDIDATE. Logs `outputs/_r451_*`."]
add += ["", "## Position — LAST SHIPPED tail r448 / r447 (verbatim, s40 §5d condense #2)"] + tail
arch = arch.rstrip("\n") + "\n" + "\n".join(add) + "\n"
io.open(A + ".new", "w", encoding="utf-8", newline="").write(arch)
out = "\n".join(lines)
io.open(S + ".new", "w", encoding="utf-8", newline="").write(out)
print("state", len(src.encode()), "->", len(out.encode()), "| archive +", len("\n".join(add).encode()))
