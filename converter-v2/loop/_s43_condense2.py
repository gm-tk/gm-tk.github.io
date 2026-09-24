#!/usr/bin/env python3
"""Session 43 §5d condense #2 (after Round 3, 99.2 KB): MOVE verbatim to LOOP_STATE_ARCHIVE.md (1) the session-38 D13 decisions
block (every decision SUMMARISED in place, one line each — nothing deleted), (2) the three remaining session-42 Declined-classes
entries (Rounds 9 / 10 / 12), (3) the s42-r5…r12 round-log lines. Pointer lines left. .bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s43-condense2.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8")); arch = []
# (1) the D13 block: from its heading to the line before the session-32 heading
k0 = [i for i, l in enumerate(L) if l.startswith("## Decisions from Chris (session 38 — 2026-09-23")]; assert len(k0) == 1
k1 = [i for i, l in enumerate(L) if l.startswith("## Decisions from Chris (session 32")]; assert len(k1) == 1
blk = L[k0[0]:k1[0]]
arch.append(("Decisions from Chris session 38 — D13-1…D13-15 (verbatim, s43 §5d condense #2)", blk))
summary = [
    "## Decisions from Chris (session 38 — 2026-09-23, the `/loop-decisions` session; ALL FOURTEEN open items answered, D13-N = Needs Chris #N; "
    "report `DECISIONS__Pending_2026-09-23.md`) — the VERBATIM block (each answer in Chris's words, every qualifier spelled out) → "
    "LOOP_STATE_ARCHIVE.md 'Decisions from Chris session 38 — D13-1…D13-15 (verbatim, s43 §5d condense #2)'; grep `D13-N` there before acting "
    "on any. One line each (every one stands):",
    "- **D13-1** the stale KB wording + the 12G status lines: Chris runs the Admin-Mode KB session himself (Option A) — the loop does NOT touch "
    "the KB; still open as a human action (Needs Chris #1; carries the 05D l.239 edit D13-2 needs and the 01B l.246 edit D13-3 implies).",
    "- **D13-2** `tableFixed`: Option C — `table table-bordered tableFixed` on TRUE two-column comparison tables (opposite-pair headers) — DONE r445.",
    "- **D13-3** the success-label wording: Option A — keep the writer's wording (CLOSED, no round).",
    "- **D13-4** the quiz engines: Option A + the answer-key carry-through — build multiChoiceQuiz / typing / dropDown / reorder / radioQuiz / "
    "selectionBox ONLY where the writer marked the answer (r309's announced-answer guard; never invent an answer); one type per kickoff, largest "
    "first; the hand-off box keeps the answer marks — typing shape 1 SHIPPED r449, the rest declined on measurement (Needs Chris #19).",
    "- **D13-5** the journal button: Option B — every journal-label variant on a writer's `[Button]` renders the house `<h4 class=\"goJournal\">Go "
    "to your journal</h4>` (a sentence on the button stays a `<p>`); never invent one (constraint 3) — DONE (r447 / r452).",
    "- **D13-6** the dual-build golds: Option A for MXFUN01 / BLL240 / CEDT207 / CEDT301 (single-file tabbed build + pairing), CEDK501 stays "
    "split, `BLL240 claude.html` out of pairing — DONE r440 (CEDT301's caveat → Needs Chris #17).",
    "- **D13-7** activity numbers: Option C — fully consecutive everywhere (r369 `page_number_normalise` ON, a NAMED override) — DONE r444.",
    "- **D13-8** empty lesson menus: Option A for the TWELVE s24 modules only (the round-110 repeat list) — DONE r442; the other 18 stay declined.",
    "- **D13-9** the speech-bubble character: Option C — the writer's picture where given + the grey placeholder in Online Safety / TEDC — DONE r446.",
    "- **D13-10** seven modules with no Writers Template: Option A — collect them (a human action; Round 0d converts them when they land).",
    "- **D13-11** XOTPB08's pasted picture: Option B — accept the flagged gap (CLOSED; r443).",
    "- **D13-12** the `Subject_Prefix_Map.json` language labels: Option A — CONFIRMED (CHI / GER / JPN / SAM / SPA → NCEA1; CHFUN / FRFUN / JPFUN "
    "/ FRNO / GENO / CHWHA / GEWHA → 1-10 Languages) — DONE r441; every other row stays PROPOSED.",
    "- **D13-14** the XOTP reader book: Option B — flagged placeholders + a visible acks flag — DONE r443.",
    "- **D13-15** the XOTPB Overview text: Option B — a red To Do placeholder (not the XOTPG wording) — DONE r443.",
    "",
]
L[k0[0]:k1[0]] = summary
# (2) the s42 declined entries
d = [i for i, l in enumerate(L) if l.startswith("- **Session 42 Round 12 ") or l.startswith("- **Session 42 Round 10 ")
     or l.startswith("- **Session 42 Round 9 ")]
assert len(d) == 3, d
arch.append(("Declined classes — session 42 Rounds 9 / 10 / 12 (verbatim, s43 §5d condense #2)", [L[i] for i in d]))
for i in sorted(d, reverse=True): del L[i]
L.insert(min(d), "- **Session 42 declined classes, Rounds 9 / 10 / 12 (the BLL2 / BLL1 family lanes KB-correct + the widget decline census; "
         "engine r471 the two-column dragAndDrop table — 2 pages / 1 module build, not one authoring shape; the MTK bilingual pair order — "
         "Māori first throughout, no class)** → LOOP_STATE_ARCHIVE.md 'Declined classes — session 42 Rounds 9 / 10 / 12 (verbatim, s43 §5d "
         "condense #2)'; every verdict stands.")
# (3) the s42-r5…r12 round-log lines
r = [i for i, l in enumerate(L) if any(l.startswith(f"- s42-r{n} ") for n in range(5, 13))]
assert len(r) == 8, r
arch.append(("Round log s42-r5…r12 (verbatim, s43 §5d condense #2)", [L[i] for i in sorted(r)]))
for i in sorted(r, reverse=True): del L[i]
k = [i for i, l in enumerate(L) if l.startswith("- s42-r1…r4 round-log lines")][0]
L.insert(k, "- s42-r5…r12 round-log lines (8 lines, session 42: r468 / r469 / r471 declined, r470 TRR115 converts, the placement-census "
         "PICK passes and its ORDER census) → LOOP_STATE_ARCHIVE.md 'Round log s42-r5…r12 (verbatim, s43 §5d condense #2)'.")
k = [i for i, l in enumerate(L) if l.startswith("**Session 43 started:**")][0]
L[k] += (" **§5d condense #2 at 20:15** (after Round 3, 99.2 KB): the D13 decisions block (summarised in place, one line each), the s42 "
         "Rounds 9 / 10 / 12 declined entries and the s42-r5…r12 round-log lines moved verbatim (`outputs/_s43_condense2.py`).")
with io.open(A, "a", encoding="utf-8", newline="\n") as f:
    for title, lines in arch: f.write("\n## " + title + "\n\n" + "\n".join(lines).rstrip() + "\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", n0, "->", os.path.getsize(S))
