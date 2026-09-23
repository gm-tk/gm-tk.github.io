#!/usr/bin/env bash
# ROUND 442 (session 39 Round 4 — D13-8, the twelve lesson-menu repeaters) — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt
# over their existing path lists (a .pre-r442.bak kept). The r436 pattern.
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_r439_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-r442.bak" ] || cp "$f" "$f.pre-r442.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-r442.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-r442: $(diff "$f.pre-r442.bak" "$f" | grep -c '^>')"
  diff "$f.pre-r442.bak" "$f" | grep '^>' | cut -c36-
done
