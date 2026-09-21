#!/usr/bin/env bash
# run_all_gates.sh — the full PROTECTED gate suite, timed, READ-ONLY.
#
# A convenience for an end-of-round / pre-ship sanity check on the CURRENT on-disk
# corpus. Does NOT touch the fast-loop baseline (use _fastloop_snapshot.py / ship.sh for
# that). Full suite is ~45s; on the 45s sandbox wall, run the two halves in separate
# calls (skeleton+defect, then the rest).
set -u
cd "$(dirname "$0")"

run() { local name="$1"; shift; local s=$SECONDS; echo "=== $name ==="; "$@"; echo "  [$((SECONDS - s))s] $name"; echo; }

# round 149 (phase 0b): loader-manifest sync FIRST — a drifted _modules.json/index.html/app/js
# set invalidates every downstream number (the r97-104 vacuous-verifier hole, now guarded).
run "index/manifest sync"    node _check_index_sync.cjs
# round 185 (D0 parity): the browser app and the node harness MUST share the one prep
# sequence (ModuleResolver.PrepareRun) — they had drifted and produced different output
# for the same module (HPFUN903). Runs right after sync: a broken entry contract makes
# every downstream gate a statement about the harness only, not the product.
run "entry parity (app↔harness)" env STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_entry_parity.cjs --selftest
run "skeleton (PRIMARY)"     python3 _skeleton_compare.py
run "structural defect audit" python3 _structural_defect_audit.py
run "compare_structure"      python3 compare_structure.py
run "body_compare"           python3 body_compare.py
run "JS regression (tags)"   node --require ./_deflate_raw_polyfill.cjs run_regression_js.cjs
run "flipCard verifier"      node --require ./_deflate_raw_polyfill.cjs _verify_flipcard.cjs CEDO102 MXDB302 TRR114 XMES201
# speechBubble verifier MUST be run on modules that actually BUILD bubbles, else it reports a
# vacuous "defect 0" (the flipCard module set above builds ZERO speechBubbles). This set builds
# ~39 bubbles across conversation + static forms; the protected criterion is defect 0.
run "speechBubble verifier"  node --require ./_deflate_raw_polyfill.cjs _verify_speechbubble.cjs OSAI501 OSAI401 OSAH501 ENGR101 OSGM501
# modal verifier (round 292 — the modal was the only widget in the coverage chain with no
# verifier at all). Run on modules that actually BUILD pop-outs; the protected criterion is
# defect 0 (an unpaired trigger, an empty pop-out, a wordless pictureless trigger, a raw
# [tag] on either side). A picture trigger and a media-only pop-out are NOT defects.
run "modal verifier"         node --require ./_deflate_raw_polyfill.cjs _verify_modal.cjs OSOH501 MXFU301 ENGR302 MXDB201 EXPFUN04
# MTK quiz SHELL verifier (round 322 — KB constraint 65 / CL-0082: the [MTKquiz] box holds ONLY
# title + instructions + To Do note + "Go to quiz", the quiz content omitted silently). Run on
# modules whose markers reach the shell; the protected criterion is defect 0 (a leaked numbered
# list / table / quiz-type placeholder / answer-mark residue / question line before the button,
# anything between note and button, a second button). A Path 2b placeholder (the marker riding a
# non-quiz container bundle — HPRE203 1C, MXFU402 5C) is reported as residue, not a defect.
run "mtkQuiz shell verifier" env STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_mtkquiz.cjs TEFUN06 TEFUN03 ARFUN04 SCCH301 BLLR201 HPRE203
run "math verifier (equations → MathML)" env STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_math.cjs MXDI102 MXDI301 PES1008 MXEX301 PES1007 MXFU302 MXFU401 MXDB301 MXDI201 MXDB202 SCCH301
# lesson-menu label verifier (round 349 — Chris's D10-9, KB constraint 23 / 01B): every learning / success label in
# #module-menu-content is the KB's <h5> colon form, no section title above a label on a lesson page, no <p> between a
# label and its list. The set covers every authoring shape: the combined "about/to" label (AGH1002), the "to" family
# (ENGC401), titles + bold Māori labels + the lesson-repeat (MXFL201), the c70 OSSC sentence (OSSC401), the two-column
# banner (ANZH101), the banner-family overview (BLL110), Fundamentals (XFUN02), Inquiry (CEDT501). Protected: defect 0.
run "menu-label verifier (c23 / 01B)" env STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_menulabels.cjs AGH1002 ENGC401 MXFL201 OSSC401 ANZH101 BLL110 XFUN02 CEDT501 CEDO502
# dragAndDrop verifier (round 350 — Chris's D10-3, the dragAndDrop build kickoff; KB 03B): every BUILT dragAndDrop is the 03B standard
# form — a questionContainer / ddContainer pair, drop + drag containers, questions = drops = drags, every drag option matched by a
# drop and vice-versa, the activityButton row, no raw [tag], NO loading="lazy" (c83), an images widget's drags each one <img>. The
# set covers both forms: the image-pair table (BLL146 gold-exact, BLL112 with its asset note, ENFUN04, CHFUN05, BLL266, MXFUN03 x2,
# BLL244 sentences) and the r69 text form (ENGJ102, ARFUN03, ENFUN01). Protected: defect 0.
run "dragAndDrop verifier (03B)" env STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_dragdrop.cjs BLL146 BLL112 ENFUN04 CHFUN05 BLL266 MXFUN03 BLL244 ENGJ102 ARFUN03 ENFUN01 ENGI203 BLL220 ENFUN08 ENGR201
# bingo verifier (round 420 — Chris's D10-3, the selfCheck type's LETTER-GRID form → the KB 03E bingo): every BUILT grid is the
# 03E form — a `div.bingo` wrapper, a `bingoContainer` with a positive integer grid, ≥ 4 cells each a <p> with text, at least one
# value="correct" cell, the Reset / Check row, no raw [tag] / red marker in a cell. The set = the nine BLL modules whose WTs carry
# the letter grid (BLL113 / BLL154 build none by design — word grids and a tile shape). Protected: defect 0.
run "bingo verifier (03E)" env STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_bingo.cjs BLL110 BLL120 BLL130 BLL140 BLL150 BLL160 BLL170 BLL113 BLL154
echo "=== gate suite complete ==="
