#!/usr/bin/env python3
"""Session 44 Round 11 — write the PICK (engine r485) + the in-flight marker in LOOP_STATE.md (§3 step 1; written as the round's first state
write — the prototype probe ran before it, recorded here). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r485-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈03:00, session 44 Round 9")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 485 IN FLIGHT — NOT PROVEN** (session 44 Round 11, 25 Sept ≈03:30): THE TITLE BAR'S LANGUAGE-BOUNDARY SPLIT — an English "
         "run then a Māori run with no separator ships as the two header h1 spans. Files: `app/js/ContentConverter.js` (`#bilingualLangSplit`, the "
         "last fallback of the title-bar split chain), `data/Emit_Templates.json` `header.title_split.lang_boundary_split` {enabled, env "
         "`TITLELANGSPLIT_OFF`}. Affected: 9 modules (8 scored + CHI1005, D14-21 excluded).")
p = [i for i, l in enumerate(L) if l.startswith("## Session 44 — Round 9 PICK (engine r484)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 44 — Round 11 PICK (engine r485) — THE TITLE BAR'S LANGUAGE-BOUNDARY SPLIT (IN FLIGHT)",
 "- **Lane:** the miner's CHROME row #4 (`title MISSING h1>span`, 270 pages / 128 modules — its Online Safety overview group at 0.93) re-read "
 "by module: the OS overview headers (`h1 > span` per module, Claude vs gold) show three shapes — (a) the unfilled `MODULE TITLE TE REO` "
 "placeholder (OSBY101 / 201 — class C, the placeholder rule already drops it), (b) English-only title bars whose Te Reo title the gold "
 "takes from the series (OSAH501 / OSAI501 / OSBY501 / OSGM201 / OSGM501 / OSSC501 — not in the WT, class C), (c) **the pair typed with NO "
 "separator, the Te Reo run only highlighted** (`*Online Bullying* ✅*Whakaweti ā-ipurangi*`): Claude joins it into ONE span, the gold "
 "ships two. The title-bar chain splits on pipe / line break / 2+ spaces / punctuation / dash / character / ALL-CAPS case, never at the "
 "English → Māori word boundary.",
 "- **Measured (a prototype behind the flag, probed corpus-wide):** 9 modules / 18 pages — GEO1004 / MXEX101 / OSBY301 / OSSC301 / OSSM301 / "
 "TWHK901 / XDLS901 / XMES203 (+ CHI1005, outside the scored population by D14-21); the gold ships the pair as two spans on every "
 "measured overview (GEO1004 / TWHK901 / XDLS901 / XMES203 / MXEX101 / the three OS); two over-fires found and guarded (CHI1005's lower-case "
 "Māori-lettered 'routine'; ENGS101's 'Exploring Te Ika a Māui' — a place name, the gold one title). Pre-score +30.9 pp-sum with CHI1005's "
 "lesson fallbacks, every scored page up; ≥75 +2.",
 "- **Authority:** the KB's bilingual title pair (c79 — 'a second h1 only for the lesson's own bilingual pair'; the r316 / r358 title-split "
 "mechanism it already drives) + the gold on every affected overview. The derivable sub-shape of CANDIDATE row #4 (8 scored modules — "
 "under the chrome floor alone; a sub-shape of a candidate row, all movers up). Predicts a skeleton move; plateau: counts if < 0.02pp.",
 "",
]
io.open(S, "w", encoding="utf-8", newline="\n").write("\n".join(L)); print("ok", os.path.getsize(S))
