"""SESSION 40 stop — §5d condense #6: the Declined entry 'Session 25 … the MINOR-HEADING ROW BREAK' MOVES verbatim to the archive;
a one-line pointer (with its verdict) stays under Declined classes. Run under WSL from FINAL_MODULE_DATA."""
import io, sys
S, A = "LOOP_STATE.md", "LOOP_STATE_ARCHIVE.md"
lines = io.open(S, encoding="utf-8", newline="").read().split("\n")
h = [i for i, l in enumerate(lines) if l.startswith("- **Session 25 (18 Sept 2026, 19:30 →) — the MINOR-HEADING ROW BREAK")]
if len(h) != 1: sys.exit("entry")
moved = lines[h[0]]
lines[h[0]] = "- **Session 25 — the MINOR-HEADING ROW BREAK — DECLINED** (verbatim → LOOP_STATE_ARCHIVE.md 'Declined — session 25 minor-heading row break (verbatim, s40 §5d condense #6)'); the verdict stands."
arch = io.open(A, encoding="utf-8", newline="").read().rstrip("\n") + "\n\n## Declined — session 25 minor-heading row break (verbatim, s40 §5d condense #6)\n" + moved + "\n"
io.open(A + ".new", "w", encoding="utf-8", newline="").write(arch)
io.open(S + ".new", "w", encoding="utf-8", newline="").write("\n".join(lines))
print("ok", len(moved.encode()))
