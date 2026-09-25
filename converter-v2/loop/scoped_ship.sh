#!/usr/bin/env bash
# scoped_ship.sh — THE SCOPED SHIP CHECKPOINT (round 175): rebuild ONLY the affected modules, prove
# the rest is byte-identical, and read the EXACT protected gates off the fast-loop baseline — no
# full-corpus regen. The full ship (ship.sh) stays the periodic backstop (see _ship_ledger.py).
#
# WHY IT IS SAFE (a code-path-completeness argument, not a shortcut): every fix ships behind a
# faithful *_OFF toggle, so the LAST-SHIPPED corpus IS the toggle-OFF state. A guarded code path that
# only fires where the Writers Template matches pattern P is a PROVABLE no-op on every module P skips.
# The affected set is therefore the COMPLETE set of modules whose WT matches P — found by
# regen_affected.cjs (--from-list from the round's measurement probe, or --wt-regex). This checkpoint
# then PROVES that completeness three ways: containment (nothing outside the set changed), a sampled
# completeness spot-check (P is a no-op on random non-affected modules), and the exact decomposition
# gate proof.
#
# USAGE (from CONVERTER_V2/reference/tests/):
#   ./scoped_ship.sh --affected affected_modules.txt --toggle BRACKETFIX_OFF            # prints the regen plans
#   # ...regen the affected set AND the spot-check sample WITH THE FIX ON (chunk for the 45s wall)...
#   ./scoped_ship.sh --affected affected_modules.txt --toggle BRACKETFIX_OFF --no-regen --commit
#
# Options: --no-regen (run the proofs; assumes the regens are done) · --sample N (spot-check size,
#   default 12) · --commit (refresh the baseline + manifest on PASS) · --manifest M (last-shipped
#   content, default outputs/_content_manifest.txt) · --round R (for the cadence ledger; ROUND 501: also passed to
#   _fastloop_diff.py --commit, which writes every gate_baseline.json aggregate + _meta.round itself) ·
#   --accept-named M1,M2 (ROUND 501: passed through to _fastloop_diff.py for a mover NAMED in the round's changelog).
set -u
cd "$(dirname "$0")"

AFF=""; TOGGLE=""; NOREGEN=0; SAMPLE=12; COMMIT=0; MANIFEST="../../outputs/_content_manifest.txt"; ROUND=""; NAMED=""
while [ $# -gt 0 ]; do
  case "$1" in
    --affected) AFF="$2"; shift 2;;
    --toggle)   TOGGLE="$2"; shift 2;;
    --no-regen) NOREGEN=1; shift;;
    --sample)   SAMPLE="$2"; shift 2;;
    --commit)   COMMIT=1; shift;;
    --manifest) MANIFEST="$2"; shift 2;;
    --round)    ROUND="$2"; shift 2;;
    --accept-named) NAMED="$2"; shift 2;;
    *) echo "unknown arg: $1"; exit 2;;
  esac
done
[ -z "$AFF" ] && { echo "need --affected FILE"; exit 2; }
[ -z "$TOGGLE" ] && { echo "need --toggle NAME (the fix's *_OFF env toggle — the scoped-ship safety invariant)"; exit 2; }
[ -f "$AFF" ] || { echo "affected file not found: $AFF"; exit 2; }
NAFF=$(grep -c . "$AFF" || true)

echo "======================================================================"
echo " SCOPED SHIP — affected=$AFF ($NAFF modules), toggle=$TOGGLE"
echo "======================================================================"

# STEP 0 — the toggle MUST exist. A fix without a faithful *_OFF breaks the whole safety argument.
echo "[0] toggle-exists invariant ($TOGGLE)"
if grep -rqF "$TOGGLE" ../../app/js; then
  echo "    OK — $TOGGLE found in app/js (the last-shipped corpus == this toggle OFF)."
else
  echo "    !! $TOGGLE not found in app/js. A fix WITHOUT a faithful *_OFF cannot be scoped-shipped."
  echo "       Add the toggle (CLAUDE.md S11) or use the full ./ship.sh."
  exit 2
fi

# REGEN PHASE — print the plans (inline multi-batch regen does not fit the 45s wall; chunk by hand).
if [ "$NOREGEN" = "0" ]; then
  echo
  echo "[regen] Regenerate the AFFECTED set WITH THE FIX ON (default env — do NOT set $TOGGLE):"
  python3 _batch_plan.py --codes $(cat "$AFF")
  echo
  echo "[regen] Completeness spot-check sample (regen these too, WITH THE FIX ON):"
  python3 _scoped_spotcheck.py plan --affected "$AFF" --n "$SAMPLE" --manifest "$MANIFEST"
  echo
  echo ">> Run both plans above (each ./_regen_safe.sh line in its OWN call), verify 0-stale, then:"
  echo "   ./scoped_ship.sh --affected $AFF --toggle $TOGGLE --no-regen --commit"
  exit 0
fi

FAIL=0

# STEP 1 — content-hash freshness (deliverable C): affected regenerated; everything else byte-identical.
echo
echo "[1] content-hash 0-stale (mtime false-alarm defeated)"
python3 _content_manifest.py fresh --affected "$AFF" --manifest "$MANIFEST" || FAIL=1

# STEP 2 — containment: the set that ACTUALLY changed must be a subset of the detector's affected set.
echo
echo "[2] containment — actually-changed modules must be a subset of the affected set"
CHANGED=$(python3 _content_manifest.py changed --manifest "$MANIFEST" || true)
NCHANGED=$(printf '%s\n' "$CHANGED" | grep -c . || true)
EXTRA=$(comm -23 <(printf '%s\n' "$CHANGED" | sort -u | grep . || true) <(sort -u "$AFF" | grep . || true) || true)
if [ -n "$EXTRA" ]; then
  echo "    !! UNDER-SCOPED — these CHANGED modules are NOT in the affected set:"
  echo "       $(echo $EXTRA)"
  echo "       => the detector missed a truly-affected module. Fall back to ./ship.sh (full --all)."
  FAIL=1
else
  echo "    OK — $NCHANGED changed module(s) are a subset of $NAFF affected (the true set ⊆ the detector set)."
fi

# STEP 3 — completeness spot-check: a random sample of NON-affected modules must be byte-identical under the fix.
echo
echo "[3] completeness spot-check (a mis-specified P is caught here)"
python3 _scoped_spotcheck.py verify --manifest "$MANIFEST" || FAIL=1

if [ "$FAIL" != "0" ]; then
  echo
  echo "SCOPED SHIP: BLOCKED — a freshness/containment/completeness check failed above. Do not finalise;"
  echo "fix the detector (or run ./ship.sh) then retry."
  exit 1
fi

# STEP 4 — exact protected-gate proof off the fast-loop baseline (decomposition; no full regen).
# Re-score the affected set PLUS the spot-check sample: the sample was regenerated too, so including it
# keeps the fast-loop mtime drift-guard satisfied; being byte-identical, it moves no aggregate.
echo
echo "[4] exact gate proof (decomposition vs the last-ship baseline)"
SAMPLEF="../../outputs/_scoped_spotcheck_sample.txt"
UNION=$(cat "$AFF" "$SAMPLEF" 2>/dev/null | sort -u | grep . || true)
if [ "$COMMIT" = "1" ]; then
  python3 _fastloop_diff.py $UNION --commit ${ROUND:+--round "$ROUND"} ${NAMED:+--accept-named "$NAMED"} || FAIL=1
else
  python3 _fastloop_diff.py $UNION ${NAMED:+--accept-named "$NAMED"} || FAIL=1
fi

# STEP 5 — baseline refresh happens inside step 4 with --commit. Remind if omitted.
if [ "$COMMIT" != "1" ]; then
  echo
  echo "[5] baseline NOT refreshed (no --commit). To make this the new shipped state, re-run with --commit."
fi

# STEP 6 — periodic full-ship backstop cadence (deliverable D).
echo
echo "[6] periodic full-ship backstop cadence"
python3 _ship_ledger.py record-scoped ${ROUND:+--round "$ROUND"} >/dev/null || true
python3 _ship_ledger.py check || true

echo
if [ "$FAIL" = "0" ]; then
  echo "SCOPED SHIP: PASS — only the affected set changed, the rest is byte-identical, and every protected"
  echo "gate held-or-improved (exact, decomposition-proven). Finalise (changelog + AppVersion + CLAUDE.md)."
else
  echo "SCOPED SHIP: FAILED — see the log above."
  exit 1
fi
