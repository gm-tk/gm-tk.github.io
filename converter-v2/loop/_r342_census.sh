#!/bin/bash
# session-9 PICK: refresh the 16-shard interactive census, then the coverage dashboard (--refresh re-runs the defect audit)
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs || exit 1
for k in $(seq 0 15); do node _measure_r271_variations.cjs --shard $k 16 > _r342_census_shard$k.log 2>&1 & done
wait
echo "shards done $(date +%H:%M:%S)"
python3 _coverage_dashboard.py --refresh > _r342_dashboard.log 2>&1
echo "dashboard rc=$? $(date +%H:%M:%S)"
