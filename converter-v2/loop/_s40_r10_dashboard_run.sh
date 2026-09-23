#!/usr/bin/env bash
# SESSION 40 ROUND 10 (24 Sept 2026) — the measurement-tool round: the r271 census gains the D13-4 quiz types.
# (1) the census with CENSUS_QUIZ_OFF=1 (the pre-round census) and (2) without it, 16 shards each, 4 at a time, each merged and kept;
# (3) the proof — ON minus the quiz types == OFF, record for record; (4) the r286 decline recorder + the dashboard --refresh (ON).
# Run under WSL: bash _s40_r10_dashboard_run.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
for MODE in OFF ON; do
  echo "[$(date +%T)] r271 census $MODE — 16 shards"
  if [ $MODE = OFF ]; then export CENSUS_QUIZ_OFF=1; else unset CENSUS_QUIZ_OFF; fi
  seq 0 15 | xargs -P 4 -I{} bash -c 'STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs '"$O"'/_measure_r271_variations.cjs --shard {} 16 > '"$O"'/_s40_r10_var_'"$MODE"'_shard{}.log 2>&1 || echo "shard {} rc=$?"'
  node --require ./_deflate_raw_polyfill.cjs $O/_measure_r271_variations.cjs --merge > $O/_s40_r10_var_${MODE}_merge.log 2>&1; echo "  merge rc=$?"
  cp $O/_r271_variations.json $O/_s40_r10_var_${MODE}.json
done
unset CENSUS_QUIZ_OFF
echo "[$(date +%T)] proof: ON minus the quiz types == OFF"
node -e '
const fs = require("fs"); const Q = new Set(["multiChoiceQuiz","typing","dropDown","dropQuiz","radioQuiz","reorder","selectionBox"]);
const load = (f) => { const j = JSON.parse(fs.readFileSync(f, "utf8")); return Array.isArray(j) ? j : (j.records ?? j.recs ?? Object.values(j).find(Array.isArray) ?? []); };
const off = load(process.argv[1]), on = load(process.argv[2]);
const key = (r) => JSON.stringify([r.code, r.page, r.type, r.index, r.built, r.sig]);
const a = off.map(key).sort(), b = on.filter((r) => !Q.has(r.type)).map(key).sort();
const same = a.length === b.length && a.every((x, i) => x === b[i]);
const byT = {}; for (const r of on) if (Q.has(r.type)) { const t = (byT[r.type] ??= { n: 0, built: 0, mods: new Set() }); t.n++; if (r.built) t.built++; t.mods.add(r.code); }
console.log(`OFF ${off.length} records; ON ${on.length} (${on.length - b.length} quiz); non-quiz identical: ${same}`);
for (const [t, v] of Object.entries(byT)) console.log(`  ${t}: ${v.n} Build calls, ${v.built} built, ${v.mods.size} modules`);
' $O/_s40_r10_var_OFF.json $O/_s40_r10_var_ON.json
echo "[$(date +%T)] r286 decline recorder — 16 shards"
seq 0 15 | xargs -P 4 -I{} bash -c 'STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs '"$O"'/_measure_r286_declines.cjs --shard {} 16 > '"$O"'/_s40_r10_dec_shard{}.log 2>&1 || echo "dec shard {} rc=$?"'
node --require ./_deflate_raw_polyfill.cjs $O/_measure_r286_declines.cjs --merge > $O/_s40_r10_dec_merge.log 2>&1; echo "  merge rc=$?"
echo "[$(date +%T)] dashboard --refresh"
python3 $O/_coverage_dashboard.py --refresh > $O/_s40_r10_dashboard.log 2>&1; echo "  rc=$?"; tail -3 $O/_s40_r10_dashboard.log
echo "[$(date +%T)] DASH_DONE"
