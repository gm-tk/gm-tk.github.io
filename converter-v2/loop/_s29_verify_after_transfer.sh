#!/usr/bin/env bash
# Verify FINAL_MODULE_DATA arrived intact on the new computer.
#
# Run this FIRST, before doing any work. It checks the five things a transfer
# actually breaks: symlinks, engine bytes, gate-tool bytes, corpus counts, git state.
#
# Usage:  bash _MIGRATION/verify_after_transfer.sh
#
# Exit 0 = safe to start work.  Exit 1 = something did not survive the transfer.

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
M="$ROOT/_MIGRATION"
cd "$ROOT"

FAIL=0
pass() { printf "  \033[32mPASS\033[0m  %s\n" "$1"; }
fail() { printf "  \033[31mFAIL\033[0m  %s\n" "$1"; FAIL=1; }
warn() { printf "  \033[33mWARN\033[0m  %s\n" "$1"; }

echo
echo "==============================================================="
echo " PageForge transfer verification"
echo " Folder: $ROOT"
echo "==============================================================="

# ---------------------------------------------------------------- 1. symlinks
echo
echo "[1/6] Symlinks (the #1 transfer casualty)"
if bash "$M/restore_symlinks.sh" >/tmp/pf_sym.txt 2>&1; then
  pass "all 5 symlinks intact"
else
  fail "symlinks damaged — the engine may exist twice on disk"
  sed 's/^/        /' /tmp/pf_sym.txt
  echo "        REPAIR: bash _MIGRATION/restore_symlinks.sh --fix"
fi

# ------------------------------------------------------------------ 2. engine
echo
echo "[2/6] Engine + data file integrity (62 files)"
if [ -f "$M/CHECKSUMS__engine.txt" ]; then
  BAD=$(md5sum -c "$M/CHECKSUMS__engine.txt" 2>/dev/null | grep -c ': FAILED$' || true)
  MISS=$(md5sum -c "$M/CHECKSUMS__engine.txt" 2>&1 | grep -c 'No such file' || true)
  if [ "$BAD" = "0" ] && [ "$MISS" = "0" ]; then
    pass "all engine + data files byte-identical"
  else
    fail "$BAD changed, $MISS missing"
    md5sum -c "$M/CHECKSUMS__engine.txt" 2>&1 | grep -E 'FAILED|No such file' | sed 's/^/        /' | head -20
  fi
else
  warn "no engine checksum manifest found"
fi

# ------------------------------------------------------------------- 3. gates
echo
echo "[3/6] Gate tooling integrity (81 files)"
if [ -f "$M/CHECKSUMS__gates.txt" ]; then
  BAD=$(md5sum -c "$M/CHECKSUMS__gates.txt" 2>/dev/null | grep -c ': FAILED$' || true)
  MISS=$(md5sum -c "$M/CHECKSUMS__gates.txt" 2>&1 | grep -c 'No such file' || true)
  if [ "$BAD" = "0" ] && [ "$MISS" = "0" ]; then
    pass "all gate tools byte-identical"
  else
    fail "$BAD changed, $MISS missing"
    md5sum -c "$M/CHECKSUMS__gates.txt" 2>&1 | grep -E 'FAILED|No such file' | sed 's/^/        /' | head -20
  fi
else
  warn "no gate checksum manifest found"
fi

# ------------------------------------------------------------------ 4. corpus
echo
echo "[4/6] Corpus census"
expect() { # label  actual  expected
  if [ "$2" = "$3" ]; then pass "$1: $2"; else fail "$1: got $2, expected $3"; fi
}
expect "human gold module dirs" "$(find 01-Finalized_Modules_ -mindepth 2 -maxdepth 2 -type d 2>/dev/null | wc -l)" "552"   # 2026-09-19 intake: 454 -> 552 (98 modules; 20 are gold-only by design — see LOOP_INTAKE__2026-09-19_98_Modules.md §5)
expect "Claude module dirs"     "$(find 01-Claude_Modules_    -mindepth 2 -maxdepth 2 -type d 2>/dev/null | wc -l)" "494"   # 2026-09-19 intake: 416 -> 494 (78 of the 98 convert; 552 gold vs 494 Claude is CORRECT)
expect "Claude .html pages"     "$(find 01-Claude_Modules_ -name '*.html' -type f 2>/dev/null | wc -l)" "2555"   # r408 (2026-09-20): 2613 -> 2555 (the 21 WJFUN + JPFUN01 single-file page model); 19 Sept intake 2109 -> 2613; before that r370 (2026-09-18): MXEX101's phantom _7_0 page removed (the media-list section pasted mid-document); before that r341 (2026-09-16): 2102 -> 2110 after the full regeneration (near-red page boundaries +10 / -2)
expect "gold .html pages"       "$(find 01-Finalized_Modules_ -name '*.html' -type f 2>/dev/null | wc -l)" "2993"   # 2026-09-19 intake: 2385 -> 2993
expect "gold .docx sources"     "$(find 01-Finalized_Modules_ -name '*.docx' -type f 2>/dev/null | wc -l)" "762"   # 2026-09-19 intake: 619 -> 762
expect "engine js files"        "$(find pageforge-site/converter-v2/app/js -name '*.js' -type f 2>/dev/null | wc -l)" "33"
expect "data json files"        "$(find pageforge-site/converter-v2/data -name '*.json' -type f 2>/dev/null | wc -l)" "24"   # r408 (2026-09-20): + data/Subject_Prefix_Map.json

# --------------------------------------------------------------------- 5. git
echo
echo "[5/6] Git repositories"
for repo in pageforge-site 00-Other-TK-Resources/htmlconvertor-kb; do
  if [ -d "$ROOT/$repo/.git" ]; then
    cd "$ROOT/$repo"
    if git log -1 --format=%h >/dev/null 2>&1; then
      HEAD_SHA=$(git log -1 --format=%h)
      pass "$repo — history intact (HEAD $HEAD_SHA)"
    else
      fail "$repo — .git present but unreadable"
    fi
    if [ -f .git/index.lock ]; then
      warn "$repo — stale .git/index.lock present; delete it or commits will fail"
    fi
    cd "$ROOT"
  else
    fail "$repo — .git MISSING (history lost; re-clone and restore work from _MIGRATION/git-state/)"
  fi
done
if [ -f "$ROOT/pageforge-site/.git/config" ]; then
  cd "$ROOT/pageforge-site"
  EXPECT_HEAD="9fb3ebd"
  ACTUAL_HEAD=$(git log -1 --format=%h 2>/dev/null || echo none)
  if [ "$ACTUAL_HEAD" = "$EXPECT_HEAD" ]; then
    pass "pageforge-site HEAD matches pre-transfer snapshot ($EXPECT_HEAD)"
  else
    warn "pageforge-site HEAD is $ACTUAL_HEAD, snapshot was $EXPECT_HEAD (fine if you have since committed)"
  fi
  cd "$ROOT"
fi

# ------------------------------------------------------------------- 6. tools
echo
echo "[6/6] Toolchain present"
for t in node python3 git; do
  if command -v "$t" >/dev/null 2>&1; then
    pass "$t — $($t --version 2>&1 | head -1)"
  else
    fail "$t not found (needed to run the converter and the gates)"
  fi
done

echo
echo "==============================================================="
if [ "$FAIL" = "0" ]; then
  echo " RESULT: PASS — the folder arrived intact. Safe to start work."
else
  echo " RESULT: FAIL — see the lines above before doing any work."
  echo " Do NOT run a corpus regeneration until this passes."
fi
echo "==============================================================="
echo
exit $FAIL
