#!/usr/bin/env python3
"""_scoped_spotcheck.py — the COMPLETENESS spot-check for scoped ship (round 175, step 3).

A scoped ship regenerates ONLY the detector's affected set A and trusts the fix's guarded code
path is a no-op everywhere else. That trust is a COMPLETENESS claim about the detector pattern P:
"every module P skipped is truly unaffected." This cheaply STRESS-TESTS that claim — regenerate a
random sample S of NON-affected modules WITH THE FIX ON and assert each stays byte-identical to the
last-shipped content manifest. If any sample module CHANGES, P under-specified the trigger (a
truly-affected module sat outside A) => the scoped ship is unsafe => fall back to the full ship.

This is the round-148 byte-identity proof, formalised and sampled so it costs one small batch, not
a full regen. (A sample can only DISPROVE completeness; a corpus-wide change must still route to
--all up front — regen_affected.cjs's 60% guard + the operator's judgement do that.)

  plan   --affected FILE [--n N] [--seed S] [--manifest M]
         pick S deterministically from the non-affected modules, write the sample file, print the
         regen command (run it WITH THE FIX ON — no *_OFF — then `verify`).
  verify [--manifest M]
         read S; assert every sample module was REGENERATED (newer than the newest source) AND is
         byte-identical to the manifest. exit 0 = P holds on S; 1 = UNDER-SCOPED; 2 = not regenerated.
"""
import os, sys, random
import _content_manifest as CM
import _corpus

SAMPLE = os.path.join(CM.OUTPUTS, "_scoped_spotcheck_sample.txt")


def _opt(args, name, default=None):
    return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default


def _all_modules(ref):
    return sorted({CM.module_of(k) for k in ref})


def _module_pages(code):
    d = _corpus.mdir(CM.CLAUDE, code)
    out = {}
    if os.path.isdir(d):
        for dp, _dn, fns in os.walk(d):
            for fn in fns:
                if fn.endswith(".html"):
                    full = os.path.join(dp, fn)
                    out[os.path.relpath(full, CM.CLAUDE).replace(os.sep, "/")] = full
    return out


def plan(args):
    aff_spec = _opt(args, "--affected")
    if aff_spec is None:
        print("plan needs --affected FILE|CODES", file=sys.stderr); return 2
    n = int(_opt(args, "--n", "12"))
    seed = int(_opt(args, "--seed", "1750"))
    mpath = _opt(args, "--manifest", CM.DEFAULT_MANIFEST)
    if not os.path.exists(mpath):
        print(f"no manifest at {mpath} — a full ship must snapshot one first.", file=sys.stderr); return 2
    ref = CM.load_manifest(mpath)
    affected = set(CM.load_affected(aff_spec))
    # ROUND 428 (session 34, 2026-09-22): never sample a compare_exclusions.txt module (D10-6) — the scoped
    # re-score takes its codes verbatim, so an excluded module in the sample (CEDW303, seed 428) enters the
    # decomposition as a NEW PAIR with its own +1 missing container and reads as a regression the corpus gates
    # never see; the sample is drawn from the SCORED population, the same list every gate honours.
    pool = [m for m in _all_modules(ref) if m not in affected and m not in set(_corpus.excluded())]
    random.Random(seed).shuffle(pool)
    sample = sorted(pool[:n])
    open(SAMPLE, "w").write("\n".join(sample) + "\n")
    print(f"[spotcheck] sample of {len(sample)} NON-affected modules (seed {seed}) -> {os.path.basename(SAMPLE)}")
    print("  " + " ".join(sample))
    print("\nRegenerate them WITH THE FIX ON (default env, NO *_OFF), then run `verify`:")
    print("  python3 _batch_plan.py --codes " + " ".join(sample))
    return 0


def verify(args):
    mpath = _opt(args, "--manifest", CM.DEFAULT_MANIFEST)
    if not os.path.exists(SAMPLE):
        print("no sample file — run `plan` first.", file=sys.stderr); return 2
    sample = [c.strip() for c in open(SAMPLE).read().split() if c.strip()]
    ref = CM.load_manifest(mpath)
    src = CM._newest_source_mtime()
    changed, not_regen = [], []
    for code in sample:
        pages = _module_pages(code)
        newest = max((os.path.getmtime(p) for p in pages.values()), default=0.0)
        if newest + 1 < src:
            not_regen.append(code); continue
        for rel, full in pages.items():
            if ref.get(rel) != CM._md5(full):
                changed.append(code); break
    print(f"[spotcheck] verifying {len(sample)} non-affected modules regenerated WITH the fix ON")
    if not_regen:
        print(f"  !! NOT REGENERATED (inconclusive): {' '.join(not_regen)}")
        print("     regen them:  python3 _batch_plan.py --codes " + " ".join(not_regen))
    if changed:
        chg = sorted(set(changed))
        print(f"  !! DETECTOR UNDER-SCOPED — {len(chg)} NON-affected module(s) CHANGED under the fix: {' '.join(chg)}")
        print("     => the pattern P missed a truly-affected module. DO NOT scoped-ship — run ./ship.sh (full --all).")
        return 1
    if not_regen:
        return 2
    print(f"  OK — all {len(sample)} sampled non-affected modules are BYTE-IDENTICAL under the fix "
          f"(P's no-op claim holds on the sample).")
    return 0


CMDS = {"plan": plan, "verify": verify}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__); return 2
    return CMDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
