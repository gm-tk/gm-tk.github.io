"""SESSION 40 — §5d condense #5: the three bullet lines under '## Loop review 2026-09-22' MOVE verbatim to LOOP_STATE_ARCHIVE.md; a
one-line pointer stays; the heading and the 'Next session starts with' line stay where they are. Run under WSL from FINAL_MODULE_DATA."""
import io, sys
S, A = "LOOP_STATE.md", "LOOP_STATE_ARCHIVE.md"
lines = io.open(S, encoding="utf-8", newline="").read().split("\n")
h = [i for i, l in enumerate(lines) if l.startswith("## Loop review 2026-09-22")]
n = [i for i, l in enumerate(lines) if l.startswith("**Next session starts with:**")]
if len(h) != 1 or len(n) != 1 or n[0] < h[0]: sys.exit("anchors")
body = [l for l in lines[h[0] + 1:n[0]] if l.strip()]
lines[h[0] + 1:n[0]] = ["", "- The review's three standing bullets (D12-1…3 applied; the Changed / Assessed pointers; the adversarial check) → LOOP_STATE_ARCHIVE.md 'Loop review 2026-09-22 — the hot bullets (verbatim, s40 §5d condense #5)'.", ""]
arch = io.open(A, encoding="utf-8", newline="").read().rstrip("\n") + "\n\n## Loop review 2026-09-22 — the hot bullets (verbatim, s40 §5d condense #5)\n" + "\n".join(body) + "\n"
io.open(A + ".new", "w", encoding="utf-8", newline="").write(arch)
io.open(S + ".new", "w", encoding="utf-8", newline="").write("\n".join(lines))
print("moved", len(body), "lines")
