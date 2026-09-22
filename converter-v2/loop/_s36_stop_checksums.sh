#!/usr/bin/env bash
# SESSION 36 STOP (after the r437 decline record) — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt over their existing path lists (a .pre-s36stop.bak kept).
# Run from FINAL_MODULE_DATA (Git Bash or WSL): bash CONVERTER_V2/outputs/_s36_stop_checksums.sh
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-s36stop.bak" ] || cp "$f" "$f.pre-s36stop.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-s36stop.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-s36stop: $(diff "$f.pre-s36stop.bak" "$f" | grep -c '^>')"
  diff "$f.pre-s36stop.bak" "$f" | grep '^>' | cut -c36-
done
