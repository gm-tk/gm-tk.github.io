#!/usr/bin/env bash
# ROUND 501 — the six count-tested verifiers on their run_all_gates.sh module sets (pass VERIFY_COUNT_RECORD=1 to record).
cd "$(dirname "$0")/../reference/tests"
export STUB_OEMBED=1
R="node --require ./_deflate_raw_polyfill.cjs"
echo "=== flipCard";   $R _verify_flipcard.cjs CEDO102 MXDB302 TRR114 XMES201 | grep -E 'TOTAL|COUNT|RESULT'; echo "rc ${PIPESTATUS[0]}"
echo "=== math";       $R _verify_math.cjs MXDI102 MXDI301 PES1008 MXEX301 PES1007 MXFU302 MXFU401 MXDB301 MXDI201 MXDB202 SCCH301 | grep -E 'TOTAL|COUNT|RESULT'; echo "rc ${PIPESTATUS[0]}"
echo "=== menulabels"; $R _verify_menulabels.cjs AGH1002 ENGC401 MXFL201 OSSC401 ANZH101 BLL110 XFUN02 CEDT501 CEDO502 | grep -E 'TOTAL|COUNT|RESULT'; echo "rc ${PIPESTATUS[0]}"
echo "=== dragdrop";   $R _verify_dragdrop.cjs BLL146 BLL112 ENFUN04 CHFUN05 BLL266 MXFUN03 BLL244 ENGJ102 ARFUN03 ENFUN01 ENGI203 BLL220 ENFUN08 ENGR201 | grep -E 'TOTAL|COUNT|RESULT'; echo "rc ${PIPESTATUS[0]}"
echo "=== bingo";      $R _verify_bingo.cjs BLL110 BLL120 BLL130 BLL140 BLL150 BLL160 BLL170 BLL113 BLL154 | grep -E 'TOTAL|COUNT|RESULT'; echo "rc ${PIPESTATUS[0]}"
echo "=== typing";     $R _verify_typing.cjs BLL244 FRFUN08 MXDB302 MXEO301 MXFL301 MXFL302 PHE1007 | grep -E 'TOTAL|COUNT|RESULT'; echo "rc ${PIPESTATUS[0]}"
