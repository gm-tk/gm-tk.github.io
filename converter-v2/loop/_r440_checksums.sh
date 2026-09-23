#!/usr/bin/env bash
# ROUND 440 (session 39 Round 2 — D13-6, the dual-build golds; compare_gold_pages.txt joins the gate manifest) — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt
# over their existing path lists (a .pre-r440.bak kept). The r436 pattern.
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_r439_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-r440.bak" ] || cp "$f" "$f.pre-r440.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-r440.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-r440: $(diff "$f.pre-r440.bak" "$f" | grep -c '^>')"
  diff "$f.pre-r440.bak" "$f" | grep '^>' | cut -c36-
done
