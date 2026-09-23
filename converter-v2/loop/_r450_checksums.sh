#!/usr/bin/env bash
# ROUND 450 (session 40 Round 7 — the claude-audit Phase 3b) — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt
# over their existing path lists (a .pre-r450.bak kept). The r445 pattern.
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_r450_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-r450.bak" ] || cp "$f" "$f.pre-r450.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-r450.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-r450: $(diff "$f.pre-r450.bak" "$f" | grep -c '^>')"
  diff "$f.pre-r450.bak" "$f" | grep '^>' | cut -c36-
done
