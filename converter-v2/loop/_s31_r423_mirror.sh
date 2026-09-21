#!/usr/bin/env bash
# SESSION 31 ROUND 1 (engine r423) — the loop mirror: README row + copy the round's artefacts + the loop md files into
# pageforge-site/converter-v2/loop/, then refresh the engine / gate checksum manifests (a .pre-r423.bak kept).
# Run from anywhere (Git Bash or WSL): bash CONVERTER_V2/outputs/_s31_r423_mirror.sh
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
# --- README row (inserted above the newest row — the r422 one) ---
python_row() { :; }
ROW='| `_s31_r1_rowmarkers.{cjs,out}` / `_s31_r423_{unit,split}.cjs` / `_s31_r423_{probe_run,regen,postship,mirror}.sh` / `_s31_r423_finalise.py` / `_s31_r423_{gates,gatecheck,spotcheck_plan,batch_plan,regen_batch_1..3,scoped_ship,fastloop,fastloop_named,selftests,index,postship,sk_full,skdelta,pmt101_build}.log` / `_s31_r423_probe_{OFF,ON}_0*.log` / `_s31_r423_{codes,ON_modules,OFF_modules}.txt` / `_s31_r423_sk_final.json` / `_affected_r423.txt` / `_diff_miner_s31_r423.log` / `_diff_queue_pre_r423.md` | `CONVERTER_V2/outputs/` | **Round 423 (session 31 Round 1, 2026-09-21) — A PAGE-BOUNDARY MARKER TYPED AS A TABLE ROW IS A PARAGRAPH (PMT101, the one-table MTK template, now converts)**: the corpus-wide marker-row census over all 762 docx (PMT101 alone, 9 rows), the unit + splitter traces, the A/B probe (OFF = disk 2555 / 2555 with PMT101 refused; ON = 2559 / 2559), the SCOPED regeneration of the 1 + 12 spot-checks, the exact decomposition (0 movers, 4 new-only pages) and the named population change, the gates / 17 selftests / index / miner (182 → 184) logs and the r423 skeleton state (2353 pairs). |'
ANCHOR='| `_s30_r5_items.cjs` / `_s30_r5_items_frfun06.log` / `_s30_r422_{probe_run,checksums}.sh`'
if grep -qF '_s31_r423_finalise.py' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
# --- artefacts ---
n=0
for f in _s31_r1_rowmarkers.cjs _s31_r1_rowmarkers.out _s31_r423_unit.cjs _s31_r423_split.cjs _s31_r423_probe_run.sh _s31_r423_regen.sh _s31_r423_postship.sh _s31_r423_mirror.sh _s31_r423_finalise.py \
         _s31_r423_gates.log _s31_r423_gatecheck.log _s31_r423_spotcheck_plan.log _s31_r423_batch_plan.log _s31_r423_regen_batch_1.log _s31_r423_regen_batch_2.log _s31_r423_regen_batch_3.log \
         _s31_r423_scoped_ship.log _s31_r423_fastloop.log _s31_r423_fastloop_named.log _s31_r423_selftests.log _s31_r423_index.log _s31_r423_postship.log _s31_r423_sk_full.log _s31_r423_skdelta.log _s31_r423_pmt101_build.log \
         _s31_r423_probe_OFF_00.log _s31_r423_probe_OFF_01.log _s31_r423_probe_OFF_02.log _s31_r423_probe_OFF_03.log _s31_r423_probe_ON_00.log _s31_r423_probe_ON_01.log _s31_r423_probe_ON_02.log _s31_r423_probe_ON_03.log \
         _s31_r423_codes.txt _s31_r423_ON_modules.txt _s31_r423_OFF_modules.txt _s31_r423_sk_final.json _affected_r423.txt _diff_miner_s31_r423.log _diff_queue_pre_r423.md; do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1)) || echo "  (missing $f)"
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md; do cp "$f" "$L/$f"; n=$((n+1)); done
echo "mirrored $n files"
# --- checksums ---
for name in engine gates; do
  f=_MIGRATION/CHECKSUMS__$name.txt
  [ -f "$f.pre-r423.bak" ] || cp "$f" "$f.pre-r423.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-r423.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$name: $(wc -l < "$f") entries; changed vs pre-r423: $(diff "$f.pre-r423.bak" "$f" | grep -c '^>')"
done
