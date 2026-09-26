#!/usr/bin/env bash
# Session 54 — the post-ship chores of ONE shipped scoped round (LOOP §3 step 7), in order: the feature index (--rehtml / --merge /
# --selftest), the DIFF MINER (§1d — after every regeneration), the engine + gate checksum manifests (AFTER the index;
# .pre-rN.bak kept), then the mirror (_s51_mirror.sh: the loop artefacts + outputs/_rN_* + the extras) with its README row.
# Under WSL:  bash _s54_post.sh N ROWFILE [EXTRA outputs/ files …]
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests || exit 1
O=../../outputs; N="$1"; ROWF="$2"; shift 2
case "$ROWF" in /*) ;; *) ROWF="/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs/$ROWF";; esac   # the row file is named relative to outputs/
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_r${N}_index.log 2>&1; echo "  rc=$?  $(tail -1 $O/_r${N}_index.log)"
echo "[$(date +%T)] DIFF MINER"
python3 _diff_miner.py > $O/_diff_miner_r${N}.log 2>&1; echo "  miner rc=$?"; tail -2 $O/_diff_miner_r${N}.log | cut -c1-200
echo "[$(date +%T)] checksum manifests"
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA || exit 1
for m in engine gates; do
  f=_MIGRATION/CHECKSUMS__$m.txt; cp $f $f.pre-r$N.bak
  awk '{ p = $0; sub(/^[0-9a-f]+ \*/, "", p); print p }' $f.pre-r$N.bak | while IFS= read -r p; do md5sum -b "$p"; done > $f.tmp
  [ "$(wc -l < $f.tmp)" = "$(wc -l < $f.pre-r$N.bak)" ] && mv $f.tmp $f || { echo "  !! $m manifest line count changed — kept the old one"; rm -f $f.tmp; }
  echo "  $m: $(md5sum -c $f 2>/dev/null | grep -c ': OK$') OK / $(wc -l < $f) — changed vs pre: $(diff $f.pre-r$N.bak $f | grep -c '^>')"
done
echo "[$(date +%T)] mirror"
bash CONVERTER_V2/outputs/_s51_mirror.sh r$N "$ROWF" "$@" | tail -3
for f in .claude/skills/*/SKILL.md; do n=$(basename $(dirname $f)); cmp -s $f pageforge-site/converter-v2/loop/_skills/$n.SKILL.md || echo "  skill copy differs: $n"; done
echo "[$(date +%T)] POST_DONE"
