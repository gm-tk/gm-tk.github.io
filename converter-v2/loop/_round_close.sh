#!/usr/bin/env bash
# _round_close.sh — the loop's round-close housekeeping (session 15): mirror the gate tools + loop artefacts + this round's
# outputs into pageforge-site/converter-v2/loop (byte-identical, proven with cmp), refresh BOTH checksum manifests from
# their own file lists (backups kept; AFTER build_feature_index.cjs — the r351 lesson), re-run verify_after_transfer.sh.
#   bash _round_close.sh r352            (run from anywhere; Git Bash or WSL)
set -u
R="${1:?round tag, e.g. r352}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
L="$ROOT/pageforge-site/converter-v2/loop"; T="$ROOT/CONVERTER_V2/reference/tests"; O="$ROOT/CONVERTER_V2/outputs"; M="$ROOT/_MIGRATION"
cd "$ROOT"
# 1. mirror
for f in _verify_dragdrop.cjs _selftest_core.cjs run_all_gates.sh gate_baseline.json _corpus.py batch_convert.cjs; do cp "$T/$f" "$L/$f"; done
cp LOOP_STATE.md KB_AMALGAMATION_STATUS.md LOOP__Autonomous_Rounds.md "$L/"
cp "$O/COVERAGE_DASHBOARD.md" "$L/"; [ -f "$O/_coverage_dashboard.json" ] && cp "$O/_coverage_dashboard.json" "$L/"
n=0; for f in $(cd "$O" && ls --indicator-style=none | grep -E "^(_${R}[_a-z0-9]*|_measure_${R}_.*)" | grep -v "^_${R}_on$\|^_${R}_off_sample$"); do [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1)); done
echo "mirrored $n ${R} artefacts"
bad=0; cnt=0
for f in $(cd "$L" && ls --indicator-style=none _${R}* _measure_${R}* _verify_dragdrop.cjs _selftest_core.cjs run_all_gates.sh gate_baseline.json _corpus.py batch_convert.cjs LOOP_STATE.md KB_AMALGAMATION_STATUS.md LOOP__Autonomous_Rounds.md COVERAGE_DASHBOARD.md 2>/dev/null); do
  src=""; for d in "$T" "$O" "$ROOT"; do [ -f "$d/$f" ] && src="$d/$f" && break; done
  cnt=$((cnt+1)); cmp -s "$src" "$L/$f" || { echo "MIRROR DIFF $f"; bad=1; }
done
echo "mirror cmp: $cnt files, bad=$bad"
# 2. checksum manifests
cp "$M/CHECKSUMS__engine.txt" "$M/CHECKSUMS__engine.pre-${R}.bak"; cp "$M/CHECKSUMS__gates.txt" "$M/CHECKSUMS__gates.pre-${R}.bak"
sed 's/^[0-9a-f]* \*//' "$M/CHECKSUMS__engine.pre-${R}.bak" > /tmp/eng_list.txt; sed 's/^[0-9a-f]* \*//' "$M/CHECKSUMS__gates.pre-${R}.bak" > /tmp/gate_list.txt
md5sum -b $(cat /tmp/eng_list.txt) > /tmp/eng_new.txt && md5sum -b $(cat /tmp/gate_list.txt) > /tmp/gate_new.txt
echo "engine lines changed: $(diff "$M/CHECKSUMS__engine.pre-${R}.bak" /tmp/eng_new.txt | grep -c '^>')  gates lines changed: $(diff "$M/CHECKSUMS__gates.pre-${R}.bak" /tmp/gate_new.txt | grep -c '^>')"
diff "$M/CHECKSUMS__engine.pre-${R}.bak" /tmp/eng_new.txt | grep '^>' | cut -c36-; diff "$M/CHECKSUMS__gates.pre-${R}.bak" /tmp/gate_new.txt | grep '^>' | cut -c36-
mv /tmp/eng_new.txt "$M/CHECKSUMS__engine.txt"; mv /tmp/gate_new.txt "$M/CHECKSUMS__gates.txt"
# 3. verify
bash "$M/verify_after_transfer.sh" 2>&1 | grep -E "FAIL|RESULT"
