#!/usr/bin/env bash
# s52 — refresh BOTH checksum manifests from their own file lists (a .txt.pre-<TAG>.bak kept), print what changed, then
# run verify_after_transfer.sh. Usage (Git Bash, from anywhere): bash _s52_checksums.sh r528
set -u
TAG="${1:?tag}"
cd "$(dirname "$0")/../.." || exit 1
M=_MIGRATION
for k in engine gates; do
  f=$M/CHECKSUMS__$k.txt
  cp "$f" "$f.pre-$TAG.bak"
  sed 's/^[0-9a-f]* \*//' "$f.pre-$TAG.bak" > /tmp/_s52_$k.lst
  md5sum -b $(cat /tmp/_s52_$k.lst) > /tmp/_s52_$k.new || { echo "md5sum failed for $k"; exit 1; }
  [ -s /tmp/_s52_$k.new ] || { echo "empty $k"; exit 1; }
  echo "$k: $(diff "$f.pre-$TAG.bak" /tmp/_s52_$k.new | grep -c '^>') line(s) changed: $(diff "$f.pre-$TAG.bak" /tmp/_s52_$k.new | grep '^>' | cut -c37- | tr '\n' ' ')"
  mv /tmp/_s52_$k.new "$f"
done
timeout 150 bash $M/verify_after_transfer.sh 2>&1 | grep -E 'FAIL|RESULT|census|PASS  (human|Claude|gold)' | head -12
