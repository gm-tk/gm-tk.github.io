"""SESSION 40 ROUND 10 — §5d: the 'Before it **r451**' Position bullet MOVES verbatim to LOOP_STATE_ARCHIVE.md; the 'Next session
starts with' line is refreshed. Run under WSL from FINAL_MODULE_DATA. Deletes nothing."""
import io, sys
S, A = "LOOP_STATE.md", "LOOP_STATE_ARCHIVE.md"
lines = io.open(S, encoding="utf-8", newline="").read().split("\n")
hits = [i for i, l in enumerate(lines) if l.startswith("- Before it **r451**")]
if len(hits) != 1: sys.exit("r451 bullet")
moved = lines.pop(hits[0])
b = [i for i, l in enumerate(lines) if l.startswith("- Before it: **r450**")]
if len(b) != 1: sys.exit("r450 pointer")
lines[b[0]] = lines[b[0]].replace("- Before it: **r450**", "- Before it: **r451** (260620.22, the bilingual section bundle hand-off box, body ANY 260 → 237) — its verbatim gate row → LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED tail r451 (verbatim, s40 §5d condense #4)'; **r450**", 1)
n = [i for i, l in enumerate(lines) if l.startswith("**Next session starts with:**")]
if len(n) != 1: sys.exit("next line")
L = lines[n[0]]
L = L.replace("Open lanes: the follow-ups (the dashboard's missing quiz rows; the iStock-href buttons;", "Open lanes: the follow-ups (the `[Image] <description>` captions — find the mechanism first, see Follow-up candidates; the iStock-href buttons;", 1)
lines[n[0]] = L
arch = io.open(A, encoding="utf-8", newline="").read().rstrip("\n") + "\n\n## Position — LAST SHIPPED tail r451 (verbatim, s40 §5d condense #4)\n" + moved + "\n"
io.open(A + ".new", "w", encoding="utf-8", newline="").write(arch)
io.open(S + ".new", "w", encoding="utf-8", newline="").write("\n".join(lines))
print("ok")
