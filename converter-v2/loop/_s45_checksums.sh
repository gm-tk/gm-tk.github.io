#!/usr/bin/env bash
# SESSION 45 — refresh _MIGRATION/CHECKSUMS__{engine,gates}.txt over their existing path lists (a .pre-r<R>.bak kept) — the r445 /
# r485 pattern, parametrised. Run from anywhere (Git Bash or WSL): bash CONVERTER_V2/outputs/_s45_checksums.sh <R e.g. 486>
R="$1"; [ -n "$R" ] || { echo "need the round number"; exit 2; }
cd "$(dirname "$0")/../.." || exit 1
for n in engine gates; do
  f=_MIGRATION/CHECKSUMS__$n.txt
  [ -f "$f.pre-r$R.bak" ] || cp "$f" "$f.pre-r$R.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-r$R.bak" | while IFS= read -r p; do [ -f "$p" ] && md5sum "$p" | sed 's/  / */'; done > "$f.new"
  mv "$f.new" "$f"
  echo "$n: $(wc -l < "$f") entries; changed vs pre-r$R: $(diff "$f.pre-r$R.bak" "$f" | grep -c '^>')"
  diff "$f.pre-r$R.bak" "$f" | grep '^>' | cut -c36-
done
