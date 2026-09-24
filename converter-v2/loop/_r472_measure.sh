#!/usr/bin/env bash
# ROUND 472 — one pass of every pre-ship measurement: the flipCard family census (ON), the widget text-loss census vs the
# r470 base, the in-memory A/B probe (OFF null test + ON changed set) and the flipCard verifier over the whole family.
# WSL: bash _r472_measure.sh <TAG>
cd "$(dirname "$0")" || exit 1
TAG="${1:-final}"
bash _s43_fam_run.sh on > /dev/null 2>&1; python3 _s43_fam_report.py flipCard /dev/null | head -2
bash _s43_wl_run.sh $TAG > /dev/null 2>&1
python3 _s43_wl_compare.py _s43_widgetloss_base.json _s43_widgetloss_$TAG.json flipCard > _r472_wl_compare_$TAG.log
grep -E '^[a-z]' _r472_wl_compare_$TAG.log
python3 _s43_wl_compare.py _s43_widgetloss_base.json _s43_widgetloss_$TAG.json | grep -E '^[a-z]' | sed 's/^/  all types: /'
bash _s42_probe_run.sh r472 OFF FLIPTEXTGUARD_OFF 2>&1 | tail -1
bash _s42_probe_run.sh r472 ON 2>&1 | tail -1
bash _r472_verify_family.sh > /dev/null 2>&1
for m in OFF ON; do printf "verifier %s: " $m; grep -h "^TOTAL" _r472_vf_${m}_0*.log | sed "s/[:,.]//g" | awk '{t+=$2; e+=$4; c+=$6; g+=$8; d+=$10; v+=$12} END{print "cards",t,"exact",e,"copy-edit",c,"gold-subst",g,"defect",d,"divergence",v}'; done
echo "[$(date +%T)] MEASURE_DONE"
