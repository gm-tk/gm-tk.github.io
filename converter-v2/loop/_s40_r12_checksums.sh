#!/usr/bin/env bash
# SESSION 40 ROUND 12 (the FULL backstop — no engine change) — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt
# over their existing path lists (a .pre-s40-r12.bak kept). The r445 pattern.
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_s40_r12_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-s40-r12.bak" ] || cp "$f" "$f.pre-s40-r12.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-s40-r12.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-s40-r12: $(diff "$f.pre-s40-r12.bak" "$f" | grep -c '^>')"
  diff "$f.pre-s40-r12.bak" "$f" | grep '^>' | cut -c36-
done
