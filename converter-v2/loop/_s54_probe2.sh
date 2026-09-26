#!/usr/bin/env bash
# Session 54 — one ON probe (_s52_on.sh TAG ENV...) + compare_structure's per-page delta on the changed modules (_s54_csdelta.py,
# the saved ON pages against the disk). Under WSL:  bash _s54_probe2.sh TAG [ENV=VAL ...]
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs || exit 1
T="$1"
bash _s52_on.sh "$@" 2>&1 | grep -E 'ASSEMBLE|changed:|pages moved'
cd ../reference/tests && python3 ../../outputs/_s54_csdelta.py ../../outputs/_affected_$T.txt /tmp/${T}_on --saved-is-on > ../../outputs/_${T}_csdelta.log 2>&1
tail -1 ../../outputs/_${T}_csdelta.log
