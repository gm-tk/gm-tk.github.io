"""SESSION 40 ROUND 11 — the LOOP_STATE.md record of the DECLINED image-caption class (written with the Write tool; run under WSL from
FINAL_MODULE_DATA). Each prefix must match exactly once or nothing is written."""
import io, sys

S = "LOOP_STATE.md"
src = io.open(S, encoding="utf-8", newline="").read()
lines = src.split("\n")


def find(prefix):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        sys.exit(f"prefix {prefix[:60]!r} matched {len(hits)} lines")
    return hits[0]


i = find("- **Session 40 Round 6 (24 Sept")
lines.insert(i, "- **Session 40 Round 11 (24 Sept 04:55 → 05:00) — THE STOCK IMAGE'S OWN WORDS AS A CAPTION (`[Image] avatar Tina` + an iStock "
                "link) — DECLINED on measurement; never re-open without a new discriminator.** Mechanism (`outputs/_s40_r11_trace.cjs`): an "
                "`[Image]` item whose picture is identified by the paragraph's STOCK hyperlink (the anchor = the iStock title → filename + alt) "
                "keeps its own `blackAfter` words as a caption `<p>` in `MediaBuilder.image`. Census over all 545 (`_s40_r11_stockcap.cjs`): "
                "**869** stock-image captions; own words: the gold ships them **533**, lacks them **309** — by length 1–2 words 81 / 61, 3–4 "
                "42 / 39, 5–8 115 / 44, 9–15 131 / 47, 16+ 164 / 118 (has / lacks): **no bucket reaches 0.60 lacking** — the gold keeps most "
                "stock captions, so a drop rule would delete real captions. TEDC402's 'avatar Tina' (11 captions + 8 inside built bubbles, "
                "`_s40_r10_bubbledesc.py`) is a one-module dialect, below floor (a `Style_Anchor_Registry`-style family row only if the TEDC "
                "family grows). The instruction-cue descriptions ('please recreate', 'creative services, please source …') are ≈ 20 sites / "
                "9 modules — below floor.")

i = find("- s40-r10 ")
lines.insert(i, "- s40-r11 (no engine change — DECLINED on measurement, 24 Sept 04:53 → 05:00) · THE STOCK IMAGE'S OWN WORDS AS A CAPTION: "
                "869 stock-image captions, gold has 533 / lacks 309, no length bucket ≥ 0.60 lacking (`_s40_r11_stockcap.cjs`); the TEDC "
                "'avatar Tina' dialect one module · see Declined classes.")

i = find("- **(s40-r10) The writer's `[Image] <description>` line ships as a visible `<p>`.**")
lines[i] = ("- ~~**(s40-r10) The writer's `[Image] <description>` line ships as a visible `<p>`.**~~ → **DECLINED s40-r11** (the mechanism "
            "found — the stock-link image's own words; the gold keeps 533 of 842 such captions; see Declined classes).")

out = "\n".join(lines)
io.open(S + ".new", "w", encoding="utf-8", newline="").write(out)
print("state", len(src.encode()), "->", len(out.encode()))
