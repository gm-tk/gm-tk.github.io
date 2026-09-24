#!/usr/bin/env python3
"""Session 45 Round 5 — write the PICK (engine r488) + the in-flight marker in LOOP_STATE.md (§3 step 1, BEFORE any code). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r488-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈06:35, session 45 Round 2")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 488 IN FLIGHT — NOT PROVEN** (session 45 Round 5, 25 Sept ≈08:15): THE STORY-REFERENCE CAROUSEL SHELL — a carousel "
         "bundle whose members are a story reference (`[embed book N]` / `[embed story]`, + its title / set / link lines) builds the r126 "
         "embed-story shell (one placeholder slide) + a Designer/Developer To Do naming the story, set and source; trailing `[body]` / question "
         "lines render after it. Files: `app/js/InteractiveBuilder.js` (`#carouselStoryShell`, dispatched after `#carouselRich`), "
         "`data/Emit_Templates.json` `interactive_builders.carousel.story_shell` {enabled, env `CARSTORY_OFF`}. Affected: ≈ 50 BLL modules.")
p = [i for i, l in enumerate(L) if l.startswith("## Session 45 — Round 2 PICK (engine r487)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 45 — Round 5 PICK (engine r488) — THE STORY-REFERENCE CAROUSEL SHELL (IN FLIGHT)",
 "- **Lane:** the hand-off boxes on disk (a §4 lane this session had not used) — the coverage dashboard's un-built carousels (320) and "
 "`WHY_UNBUILT__carousel.md` reason 1: the writer asks for a decodable / School Journal story to be paged through as a carousel "
 "(`[carousel]` + `[embed book 1] Are we able to embed just the story … into a carousel …` + `The story ‘Zac hid from Dad’ can be found - "
 "(in Set 5)` + the PDF link); the human builds `div.row.carousel > viewer > item.image > img` × the story's pages (BLL152-2.0), cut from "
 "the PDF by hand — the page count is nowhere in the WT, so the slides are not derivable but the SHELL is: since r126 the ordinary-text "
 "path emits exactly that shell for an `[embed story]` line, and a member captured inside a carousel bundle never reaches it.",
 "- **Measured (`_s43_wdump.cjs` DUMP_TYPE=carousel over the 82 modules whose WT carries an `[embed … story|book]` tag → "
 "`_s45_r5_cardump.log`, `_s45_r5_carshape.py`):** 60 story-carrying carousel bundles, **59 ship as the hand-off box** (1 built — "
 "BLL262 3.0), ≈ 50 modules (BLL1 / BLL2 phonics families); shapes: the reference alone (± a `……` / set / link line) ≈ 33, the reference "
 "+ `[body]` + the discussion questions (± an instruction to put them in an accordion) ≈ 20, a few with two or three story references.",
 "- **Authority:** A1 (Decision Framework) — the writer tagged a carousel and the human built one on its page; D10-3 (build the writer's "
 "interactives, judged on the widget's own verifier — `_verify_carousel.cjs` checks built video slides only, so an image-placeholder shell "
 "cannot register as a defect) + the dashboard's Still-a-box count (≥ 20 converted = progress, §4 widget-build bullet). The widget itself "
 "is skeleton-blind (the hand-off box and the carousel both collapse to one WIDGET line); the discussion prose that leaves the box is "
 "visible (the gold keeps it as page text or an accordion) — a widget-build round: neither counts toward nor resets the plateau.",
]
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(L)); os.replace(S + ".tmp", S)
print("ok", os.path.getsize(S))
