#!/bin/bash
# s52 health check: the §1f intake triggers (b)-(d), one line each.
R=/c/Users/Gavin/TeKura/FINAL_MODULE_DATA
[ -d "$R" ] || R=/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA
cd "$R" || exit 1
ls -d 01-Finalized_Modules_/*/*/ | awk -F/ '{print $3}' | sort -u > /tmp/_s52_gold.txt
ls -d 01-Claude_Modules_/*/*/ | awk -F/ '{print $3}' | sort -u > /tmp/_s52_claude.txt
echo "(b) gold dirs with no Claude dir:"; comm -23 /tmp/_s52_gold.txt /tmp/_s52_claude.txt | tr '\n' ' '; echo
n=0
for d in 01-Finalized_Modules_/*/*/; do
  code=$(basename "$d")
  run=$(ls 01-Claude_Modules_/*/"$code"/_run.json 2>/dev/null | head -1)
  [ -n "$run" ] || continue
  c=$(find "$d" -name '*.docx' -newer "$run" </dev/null 2>/dev/null | wc -l)
  if [ "$c" -gt 0 ]; then echo "  newer docx: $code ($c)"; n=$((n+c)); fi
done
echo "(c) docx newer than its _run.json: $n"
echo "(d) staging areas:"
for s in 04-Newly-Developed-Modules-Raw-Info new-html-files-and-wt; do
  echo "  $s: $(ls "$s" 2>/dev/null | wc -l) entries, newest $(ls -t "$s" 2>/dev/null | head -1) $(stat -c %y "$s/$(ls -t "$s" | head -1)" 2>/dev/null | cut -c1-16)"
done
