#!/usr/bin/env bash
# SESSION 28 TASK 1 (round 408) — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt over their existing path lists (a .pre-s28t1.bak kept).
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_s27_s28t1_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-s28t1.bak" ] || cp "$f" "$f.pre-s28t1.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-s28t1.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-s28t1: $(diff "$f.pre-s28t1.bak" "$f" | grep -c '^>')"
done
