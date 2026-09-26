#!/usr/bin/env bash
# s52 Round 4 — scoped miners per family group (4 in parallel; `wait`, never pgrep). WSL.
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests || exit 1
O=../../outputs
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > /tmp/_s52_codes.txt
for g in XDLS "ENGC ENGS ENGJ ENGR" AGH XGF; do
  tag=$(echo $g | tr ' ' '_' | tr 'A-Z' 'a-z')
  re=$(echo $g | sed 's/ /|/g')
  codes=$(grep -E "^($re)[0-9]" /tmp/_s52_codes.txt | tr '\n' ' ')
  ( python3 _diff_miner.py $codes --json $O/_s52_${tag}_miner.json --md $O/_s52_${tag}_miner.md > $O/_s52_${tag}_miner.log 2>&1 ) &
done
wait
for f in $O/_s52_*_miner.log; do echo "$(basename $f): $(tail -3 $f | head -1 | cut -c1-160)"; done
