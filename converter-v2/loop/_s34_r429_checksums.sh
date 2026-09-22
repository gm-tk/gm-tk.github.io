#!/usr/bin/env bash
# ROUND 429 (session 34 Round 4) — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt over their existing path lists (a .pre-r429.bak kept).
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_s33_r429_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-r429.bak" ] || cp "$f" "$f.pre-r429.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-r429.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-r429: $(diff "$f.pre-r429.bak" "$f" | grep -c '^>')"
  diff "$f.pre-r429.bak" "$f" | grep '^>' | cut -c36-
done
