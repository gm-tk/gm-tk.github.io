#!/usr/bin/env bash
# Session 29 Round 5 (engine r414) — the two un-nesting forms scored against each other on the 65 changed modules:
#   variant ALLCLOSE  = keep_inside_subjects []            (every subject closes the outer box first)
#   variant ALLKEEP   = keep_inside_subjects = every subject present (the synthetic box is suppressed everywhere)
# The data file is patched in place (tab-preserving), the probe's ON leg saved per variant, scored, then the data restored.
# Usage (WSL): bash _s29_r414_variants.sh
set -e
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
D=../../data/Emit_Templates.json
cp $D $O/_s29_r414_emit_backup.json
CODES=$(cat $O/_s29_r414_ON_modules.txt | tr '\n' ' ')
run_variant () {
  V=$1
  rm -rf $O/_s29_r414_var_$V; mkdir -p $O/_s29_r414_var_$V
  for i in 0 1 2 3; do
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s28_t3_probe.cjs --save $O/_s29_r414_var_$V $(awk -v i=$i 'NR%4==i' $O/_s29_r414_ON_modules.txt | tr '\n' ' ') > $O/_s29_r414_var_${V}_$i.log 2>&1 ) &
  done
  wait
  grep -h "^TOTAL" $O/_s29_r414_var_${V}_*.log
  sed "s#_s29_r414_on#_s29_r414_var_$V#; s#_s29_r414_onscore.json#_s29_r414_var_${V}_score.json#" $O/_s29_r414_pagescore.py > $O/_s29_r414_var_pagescore.py
  python3 $O/_s29_r414_var_pagescore.py $O/_s29_r414_ON_modules.txt > $O/_s29_r414_var_${V}_score.log 2>&1
  head -1 $O/_s29_r414_var_${V}_score.log
}
echo "[$(date +%T)] ALLCLOSE"
python3 - <<'EOF'
import io,re
p='../../data/Emit_Templates.json'; s=io.open(p,encoding='utf-8').read()
s2=re.sub(r'("keep_inside_subjects": \[)[^\]]*(\])', r'\1\2', s, count=1)
assert s2!=s; io.open(p,'w',encoding='utf-8',newline='').write(s2)
EOF
run_variant ALLCLOSE
echo "[$(date +%T)] ALLKEEP"
cp $O/_s29_r414_emit_backup.json $D
python3 - <<'EOF'
import io,re,json
subs=sorted(set(m.get('subject','') for m in json.load(open('../../data/Module_Structure_Index.json'))['module_meta'].values() if m.get('subject')))
p='../../data/Emit_Templates.json'; s=io.open(p,encoding='utf-8').read()
lst=',\n\t\t\t\t\t'.join(json.dumps(x) for x in subs)
s2=re.sub(r'("keep_inside_subjects": \[)[^\]]*(\])', lambda m: m.group(1)+'\n\t\t\t\t\t'+lst+'\n\t\t\t\t'+m.group(2), s, count=1)
assert s2!=s; io.open(p,'w',encoding='utf-8',newline='').write(s2)
EOF
run_variant ALLKEEP
cp $O/_s29_r414_emit_backup.json $D
echo "[$(date +%T)] data restored: $(cmp $O/_s29_r414_emit_backup.json $D && echo identical)"
