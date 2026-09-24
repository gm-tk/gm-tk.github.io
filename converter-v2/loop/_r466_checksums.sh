#!/usr/bin/env bash
# ROUND 465 (session 42 Round 2 — D14-20, the course-code heading) — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt
# over their existing path lists (a .pre-r466.bak kept). The r445 pattern.
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_r466_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-r466.bak" ] || cp "$f" "$f.pre-r466.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-r466.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-r466: $(diff "$f.pre-r466.bak" "$f" | grep -c '^>')"
  diff "$f.pre-r466.bak" "$f" | grep '^>' | cut -c36-
done
