#!/usr/bin/env bash
# ROUND 0d intake 2026-09-22 (session 33 Round 3) — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt over their existing path lists (a .pre-intake20260922.bak kept).
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_s27_intake20260922_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-intake20260922.bak" ] || cp "$f" "$f.pre-intake20260922.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-intake20260922.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-intake20260922: $(diff "$f.pre-intake20260922.bak" "$f" | grep -c '^>')"
done
