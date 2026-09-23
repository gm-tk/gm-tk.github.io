"""ROUND 451 (session 40 Round 8) — the LOOP_STATE.md finalise edits, applied by exact line prefix (written with the Write tool;
run under WSL from FINAL_MODULE_DATA). Each edit must match exactly once or nothing is written."""
import io, sys

P = "LOOP_STATE.md"
src = io.open(P, encoding="utf-8", newline="").read()
lines = src.split("\n")


def find(prefix):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        sys.exit(f"prefix {prefix[:50]!r} matched {len(hits)} lines")
    return hits[0]


# 1. the in-flight marker -> no round in flight
i = find("- **ROUND 451 IN FLIGHT — NOT PROVEN**")
lines[i] = ("- **No round in flight** (24 Sept 2026 04:10, session 40 Round 8 SHIPPED r451; the corpus on disk IS the r451 state, "
            "LAST SHIPPED r451, LAST FULL r444, ledger scoped #6 — 2 of headroom). The §3 step-1 rule stands: the next PICK raises "
            "`ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited (r451 raised it at 03:45, before its first edit).")

# 2. LAST SHIPPED r451, r450 becomes "Before it"
i = find("- LAST SHIPPED: **r450**")
old = lines[i]
lines[i] = ("- LAST SHIPPED: **r451** (build 260620.22, 24 Sept 04:10, session 40 Round 8 — THE BILINGUAL SECTION'S WIDGET BUNDLE TAKES "
            "THE STANDARD HAND-OFF BOX, `BILHANDOFF_OFF`; 95 boxes / 50 files / 15 Bilingual modules, 61 empty `<table>` boxes → 0; "
            "SCOPED (the 23 Bilingual modules), **scoped #6 since the r444 FULL (2 of headroom)**; **skeleton 54.7407 % @ 2477 "
            "+0.0000pp, 0 movers**, ≥50 1542, ≥75 260, ≥90 23, RAW 38.644 % (−0.051pp NAMED, the hand-off internals); cs 15657 / 199 / "
            "796 / 24; **body 58 / 5 / 176 / 237** (ANY −23, EMPTY −24; over-capture +1 NAMED TRR301_3_0, EMPTY → visible); clean "
            "2613 / 2658; leak 75 / 45; `gate_baseline.json` at r451 (its `_meta` build / round refreshed — they had stood at r446); "
            "`outputs/_r451_sk_final.json`; 60.1 % of achievable; the miner 195 CANDIDATE).")
lines.insert(i + 1, "- Before it " + old[len("- LAST SHIPPED: "):].replace("24 Sept ≈04:45", "24 Sept ≈03:30"))

# 3. plateau reading
i = find("- Plateau window (§4): **1 of 3** — r449")
lines[i] = lines[i].replace("- Plateau window (§4): **1 of 3** — r449",
                            "- Plateau window (§4): **1 of 3** — r451 declared skeleton-neutral by design (a hand-off box is one WIDGET line) "
                            "and moved the body gate (improved): neither counts nor resets; r450 output-inert (neither); r449", 1)

# 4. standing facts
i = find("- Standing facts: AppVersion 260620.21")
lines[i] = lines[i].replace("- Standing facts: AppVersion 260620.21 (",
                            "- Standing facts: AppVersion 260620.22 (r451 the bilingual section bundle hand-off box — session 40 Round 8, "
                            "24 Sept); before it 260620.21 (", 1)

# 5. round-log line
i = find("- s40-r7 ")
lines.insert(i, "- s40-r8 (engine r451, build 260620.22, 24 Sept 03:34 → 04:10) · THE BILINGUAL SECTION'S WIDGET BUNDLE TAKES THE "
                "STANDARD HAND-OFF BOX (the dashboard lane — the body gate's empty-widget row split: 61 empty `<table>` boxes / 23 TRR "
                "pages were `contentTable(<first member>)` of an `[Activity: Embedded]` tag line) · `BILHANDOFF_OFF`, 95 boxes / 15 "
                "modules · SHIPPED · scaffold 54.7407 → 54.7407 (0 movers) · body ANY 260 → 237 · over-capture +1 NAMED · scoped #6.")

# 6. follow-up
i = find("- **(r449) The coverage dashboard has no quiz-engine rows.**")
lines.insert(i, "- **(r451) TRR301_3_0's unclassified bundle captures the page.** Its hand-off box (empty until r451) holds 4,327 characters "
                "= 62 % of the page, and the gold keeps 32 free blocks where Claude keeps 2 (lost 30) — the scanner's capture never finds "
                "the bundle's end inside the keystone section. ONE page (below floor); check the other Bilingual over-capture pages "
                "(TRR110_0_0 0.96, PMT101_0_0 1.0) for the same terminator before calling it a class. **The rest of the empty-box row** "
                "(`outputs/_s40_r8_empty.json`, 266 placeholders after r451): real short widgets (word lists — not a defect), banner-only "
                "boxes with < 10 member characters (≈ 76: clickDrop 22, unclassified 16, dragAndDrop 15 — members that are images or "
                "references only), and the WJFUN `[correct answer …]` tables (11) — each its own measure before any round.")

out = "\n".join(lines)
io.open(P + ".new", "w", encoding="utf-8", newline="").write(out)
print("ok", len(src), "->", len(out))
