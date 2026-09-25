#!/usr/bin/env bash
# Session 49 — mirror the loop artefacts, prove the mirror (cmp), refresh the checksum manifests, commit pageforge-site.
# Usage (Git Bash, from anywhere): bash _s49_ship.sh <N> <commit-message-file> [extra outputs/ files to mirror…]
set -u
cd "$(dirname "$0")/../.." || exit 1          # FINAL_MODULE_DATA
N="$1"; MSG="$2"; shift 2
T=CONVERTER_V2/reference/tests; L=pageforge-site/converter-v2/loop; O=CONVERTER_V2/outputs; FAIL=0
for f in gate_baseline.json run_all_gates.sh _corpus.py _fastloop_diff.py _gatecheck.py scoped_ship.sh _selftest_core.cjs _verify_count.cjs \
         _verify_bingo.cjs _verify_typing.cjs _verify_dragdrop.cjs _verify_flipcard.cjs _verify_math.cjs _verify_menulabels.cjs compare_gold_pages.txt compare_exclusions.txt; do
  cp -p "$T/$f" "$L/$f" && cmp -s "$T/$f" "$L/$f" || { echo "MIRROR FAIL $f"; FAIL=1; }
done
for f in COVERAGE_DASHBOARD.md _coverage_dashboard.json _placement_census.md _placement_census.json _s49_fin.py _s49_ship.sh "$@"; do
  [ -e "$O/$f" ] || continue
  cp -p "$O/$f" "$L/$f" && cmp -s "$O/$f" "$L/$f" || { echo "MIRROR FAIL $f"; FAIL=1; }
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DIFF_QUEUE.md; do
  cp -p "$f" "$L/$f" && cmp -s "$f" "$L/$f" || { echo "MIRROR FAIL $f"; FAIL=1; }
done
for s in .claude/skills/*/SKILL.md; do n=$(basename "$(dirname "$s")"); cmp -s "$s" "$L/_skills/$n.SKILL.md" || cp -p "$s" "$L/_skills/$n.SKILL.md"; done
[ "$(grep -c '^\*\*Amended:\*\*' LOOP__Autonomous_Rounds.md)" = "1" ] || { echo "AMENDED LINE COUNT != 1"; FAIL=1; }
for m in engine gates; do
  F=_MIGRATION/CHECKSUMS__$m.txt; cp -p "$F" "$F.pre-r$N.bak"
  sed 's/^[0-9a-f]* \*//' "$F" > /tmp/paths_$m.txt; : > /tmp/new_$m.txt
  while IFS= read -r p; do md5sum -b "$p" >> /tmp/new_$m.txt; done < /tmp/paths_$m.txt
  mv /tmp/new_$m.txt "$F"; B=$(md5sum -c "$F" 2>&1 | grep -vc ': OK$'); [ "$B" = "0" ] || { echo "CHECKSUM FAIL $m"; FAIL=1; }
done
[ "$FAIL" = "0" ] || { echo "SHIP ABORTED — nothing committed"; exit 1; }
cd pageforge-site && git add -A converter-v2 && git commit -q -F "$MSG" && git --no-pager log --oneline -1
