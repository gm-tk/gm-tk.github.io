#!/usr/bin/env bash
# ROUND 439 (session 39 — finishing the claude-audit Phase 2 round the Cowork session left loose) — the toggle-OFF proof.
# (1) snapshot the 7 ON modules; (2) regen WRITEFONT_OFF=1; (3) OFF == ON with writeFont -> sassoonI-text, byte for byte,
# and OFF carries 0 writeFont; (4) regen ON again; (5) ON again == the snapshot byte for byte (determinism).
# under WSL: bash ../../outputs/_r439_offproof.sh   (from CONVERTER_V2/reference/tests)
set -u
cd "$(dirname "$0")/../reference/tests"
ROOT=../../..
CM=$ROOT/01-Claude_Modules_
SNAP=/tmp/r439_snap; rm -rf $SNAP; mkdir -p $SNAP/on $SNAP/off $SNAP/on2
CODES=$(cat ../../outputs/_affected_r439.txt | tr -d '\r' | tr '\n' ' ')
dir_of() { ls -d $CM/*/$1 2>/dev/null | head -1; }
for c in $CODES; do d=$(dir_of $c); cp -r "$d" $SNAP/on/$c; done
echo "[$(date +%T)] snapshot ON: $(ls $SNAP/on | wc -l) modules, writeFont occ $(cat $SNAP/on/*/*.html | grep -o 'writeFont' | wc -l), sassoon occ $(cat $SNAP/on/*/*.html | grep -o 'sassoon' | wc -l)"
echo "[$(date +%T)] regen OFF"
WRITEFONT_OFF=1 STUB_OEMBED=1 timeout 900 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs $CODES --force > ../../outputs/_r439_offproof_regen_off.log 2>&1; echo "  rc=$?"
for c in $CODES; do d=$(dir_of $c); cp -r "$d" $SNAP/off/$c; done
echo "  OFF writeFont occ $(cat $SNAP/off/*/*.html | grep -o 'writeFont' | wc -l), sassoonI-text occ $(cat $SNAP/off/*/*.html | grep -o 'sassoonI-text' | wc -l)"
bad=0
for c in $CODES; do
  for f in $SNAP/on/$c/*.html; do
    b=$(basename $f)
    if ! cmp -s <(sed 's/class="writeFont"/class="sassoonI-text"/g' $f) $SNAP/off/$c/$b; then echo "  DIFF beyond the class swap: $c/$b"; bad=$((bad+1)); fi
  done
  n_on=$(ls $SNAP/on/$c | wc -l); n_off=$(ls $SNAP/off/$c | wc -l); [ "$n_on" = "$n_off" ] || { echo "  file count differs $c $n_on/$n_off"; bad=$((bad+1)); }
done
echo "  OFF == ON-with-the-class-swapped: $([ $bad = 0 ] && echo YES || echo "NO ($bad)")"
echo "[$(date +%T)] regen ON again"
STUB_OEMBED=1 timeout 900 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs $CODES --force > ../../outputs/_r439_offproof_regen_on.log 2>&1; echo "  rc=$?"
bad2=0
for c in $CODES; do d=$(dir_of $c); for f in $SNAP/on/$c/*; do b=$(basename $f); [ "$b" = "_run.json" ] && continue; cmp -s $f "$d/$b" || { echo "  ON-again differs: $c/$b"; bad2=$((bad2+1)); }; done; done
echo "  ON-again == the shipped ON snapshot (every page): $([ $bad2 = 0 ] && echo YES || echo "NO ($bad2)")"
echo "[$(date +%T)] content manifest fresh over the 7"
python3 _content_manifest.py fresh --affected ../../outputs/_affected_r439.txt 2>&1 | tail -3
echo "[$(date +%T)] OFFPROOF_DONE"
