#!/usr/bin/env bash
# ROUND 472 (session 43 Round 1 — the flip-card text guard) — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt
# over their existing path lists (a .pre-s44full.bak kept). The r445 pattern.
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_s44full_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-s44full.bak" ] || cp "$f" "$f.pre-s44full.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-s44full.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-s44full: $(diff "$f.pre-s44full.bak" "$f" | grep -c '^>')"
  diff "$f.pre-s44full.bak" "$f" | grep '^>' | cut -c36-
done
