#!/usr/bin/env bash
# ROUND 473 — one pass of every pre-ship measurement: the modal family census (ON; the family list from the r472-state OFF json),
# the media-aware widget text-loss census vs the r472 state, the in-memory A/B probe (OFF null test + ON changed set) and the
# modal verifier over the whole modal family (OFF / ON). WSL: bash _r473_measure.sh <TAG>
cd "$(dirname "$0")" || exit 1
TAG="${1:-final}"
bash _s43_fam_run.sh on > /dev/null 2>&1; python3 _s43_fam_report.py modal _r473_family.txt | tail -2
bash _s43_wl2_run.sh $TAG > /dev/null 2>&1
python3 _s43_wl2_compare.py _s43_widgetloss2_r472.json _s43_widgetloss2_$TAG.json modal > _r473_wl_compare_$TAG.log
grep -E '^[a-z]' _r473_wl_compare_$TAG.log
python3 _s43_wl2_compare.py _s43_widgetloss2_r472.json _s43_widgetloss2_$TAG.json | grep -E '^[a-z]' | sed 's/^/  all types: /'
bash _s42_probe_run.sh r473 OFF MODALBTNTEXT_OFF 2>&1 | tail -1
bash _s42_probe_run.sh r473 ON 2>&1 | tail -1
cd ../reference/tests
rm -f ../../outputs/_r473_vm_*
split -n l/4 -d ../../outputs/_r473_family.txt ../../outputs/_r473_vm_codes_
for i in 00 01 02 03; do
  ( MODALBTNTEXT_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_modal.cjs $(cat ../../outputs/_r473_vm_codes_$i) > ../../outputs/_r473_vm_OFF_$i.log 2>&1 ) &
  ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_modal.cjs $(cat ../../outputs/_r473_vm_codes_$i) > ../../outputs/_r473_vm_ON_$i.log 2>&1 ) &
done; wait
for m in OFF ON; do echo "modal verifier $m:"; grep -h -E "^TOTAL|RESULT" ../../outputs/_r473_vm_${m}_0*.log | sort | uniq -c | head -8; done
echo "[$(date +%T)] MEASURE_DONE"
