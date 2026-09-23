#!/usr/bin/env bash
# ROUND 450 (session 40 Round 7 — the claude-audit Phase 3b, the inert Subject_Global_Parameters.json refresh) — the loop mirror.
# Written with the Write tool. Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s40_r7_probe_run.sh` / `_s40_r7_probe_ON_0*.log` / `_s40_r7_{codes,ON_pages,ON_modules}.txt` / `_r450_mirror.sh` / `_r450_checksums.sh` | `CONVERTER_V2/outputs/` | **Round 450 (session 40 Round 7, 2026-09-24) — the claude-audit Phase 3b, the inert SGP refresh** (KB 910a9cb: CL-0111 / CL-0112 / CL-0113) — the full-corpus inertness probe (3208 / 3208 identical), the checksums and this mirror. |'
ANCHOR='| `_s40_r6_ddwhy.cjs`'
if grep -qF '_s40_r7_probe_run.sh' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _s40_r7_* _r450_mirror.sh _r450_checksums.sh 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md; do cp "$f" "$L/$f"; n=$((n+1)); done
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
