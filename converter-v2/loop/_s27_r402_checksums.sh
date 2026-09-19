#!/usr/bin/env bash
# ROUND 402 — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt over their existing path lists (a .pre-r402.bak kept).
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_s27_r402_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-r402.bak" ] || cp "$f" "$f.pre-r402.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-r402.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-r402: $(diff "$f.pre-r402.bak" "$f" | grep -c '^>')"
done
