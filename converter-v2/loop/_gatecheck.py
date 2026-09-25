#!/usr/bin/env python3
"""_gatecheck.py — FULL-REGEN hold-or-improve verdict in ONE command (the round-92 gap).

_fastloop_diff.py is the INNER loop (re-score a few modules vs the fast-loop baseline); it
correctly REFUSES after a full regen — every module is newer than that baseline. So after a
full 0-stale SHIP regen there was no one-command verdict: round-92 hand-diffed the gate JSONs,
which is slow AND is exactly where the stale-read trap bit. This runs the 4 decomposable gates
FULL (fresh — it can never read a stale json) and diffs vs the COMMITTED, drift-proof
gate_baseline.json, printing the same HELD / IMPROVED / REGRESSED table _fastloop_diff prints.

Run AFTER a full 0-stale regen (it ASSERTS 0-stale and refuses otherwise). On the 45s sandbox,
split the gate run across calls; the verdict prints once all 4 are written:
  python3 _gatecheck.py skeleton defect      # call 1
  python3 _gatecheck.py cs bc                 # call 2 (+ verdict, since all 4 now exist)
  python3 _gatecheck.py                       # all 4 + verdict in one call (if it fits the wall)
  python3 _gatecheck.py verdict              # just diff the 4 already-written jsons (no re-run)
  python3 _gatecheck.py … --commit --round N [--build X]
                                              # ROUND 501: on PASS, write EVERY gate_baseline.json aggregate from
                                              # the live full run (the FULL-backstop re-base — never typed by hand)
The 3 VERIFIER gates (tags / flipCard / speechBubble) are NOT decomposable — run run_all_gates.sh.
"""
import os, sys, json, shutil, subprocess
import _fastloop_diff as D

BASE = D.BASE
CUR = D.CURRENT
os.makedirs(CUR, exist_ok=True)
PY = D.PY
PATHS = {"cs": os.path.join(CUR, "structural_comparison.json"),
         "bc": os.path.join(CUR, "body_compare.json"),
         "sk": os.path.join(CUR, "skeleton.json"),
         "df": os.path.join(CUR, "defect.json")}


def _stale_line():
    r = subprocess.run(["bash", "_stalecheck.sh"], cwd=BASE, capture_output=True, text=True)
    last = (r.stdout.strip().splitlines() or [""])[-1] if r.returncode == 0 else \
        (r.stdout.strip().splitlines() or ["stale"])[0]
    return r.returncode != 0, last


def run_cs():
    subprocess.run([PY, "compare_structure.py"], cwd=BASE, check=True, stdout=subprocess.DEVNULL)
    shutil.copyfile(os.path.join(BASE, "structural_comparison.json"), PATHS["cs"])


def run_bc():
    subprocess.run([PY, "body_compare.py"], cwd=BASE, check=True, stdout=subprocess.DEVNULL)
    shutil.copyfile(os.path.join(BASE, "body_compare.json"), PATHS["bc"])


def run_sk():
    subprocess.run([PY, "_skeleton_compare.py", "--json", PATHS["sk"]], cwd=BASE, check=True, stdout=subprocess.DEVNULL)


def run_df():
    subprocess.run([PY, "_structural_defect_audit.py", "--json", PATHS["df"]], cwd=BASE, check=True, stdout=subprocess.DEVNULL)


RUN = {"cs": run_cs, "bc": run_bc, "skeleton": run_sk, "defect": run_df}


def live_aggregates():
    cs = D._load(PATHS["cs"]); bc = D._load(PATHS["bc"])
    sk = D._load(PATHS["sk"])["per_page"]; df = D._load(PATHS["df"])
    return {**D.cs_metrics(cs), **D.bc_metrics(bc), **D.sk_metrics(sk), **D.df_metrics(df)}


def committed_baseline():
    gb = D._load(os.path.join(BASE, "gate_baseline.json"))
    sk, cs, bc, df = gb["skeleton"], gb["compare_structure"], gb["body_compare"], gb["structural_defect"]
    agg = {"sk_mean": sk["mean_scaffold_pct"] / 100.0, "sk_ge50": sk["pages_ge_50"], "sk_ge75": sk["pages_ge_75"],
           "cs_exact": cs["exact_chain"], "cs_extra": cs["claude_extra_container"], "cs_missing": cs["claude_missing_container"],
           "body_any": bc["any_breakdown"], "df_clean_pct": df["clean_pct"],
           "df_leak_occ": df["literal_tag_leak_occ"], "df_leak_pages": df["leak_pages"]}
    return agg, gb.get("_meta", {})


def verdict():
    missing = [g for g, p in PATHS.items() if not os.path.exists(p)]
    if missing:
        names = {"sk": "skeleton", "df": "defect"}
        sys.exit("gates not all run yet — run: python3 _gatecheck.py "
                 + " ".join(names.get(m, m) for m in missing))
    new = live_aggregates()
    base, meta = committed_baseline()
    print(f"\nFULL-REGEN GATE VERDICT — live full corpus vs committed gate_baseline.json "
          f"(round {meta.get('round')}, build {meta.get('build')})")
    hdr = f"  {'metric':36} {'baseline':>10} {'live':>10} {'delta':>9}  verdict"
    print(hdr); print("  " + "-" * (len(hdr) - 2))
    regressed, body_only = [], None
    for m in D.ORDER:
        o, n = base[m], new[m]
        of, nf = D._fmt(m, o), D._fmt(m, n)
        if of == nf:
            verd = "HELD"
        elif (n - o) * D.POLARITY[m] > 0:
            verd = "IMPROVED"
        else:
            verd = "REGRESSED"; regressed.append(m)
        d = n - o
        ds = ("+" if d > 0 else "") + (D._fmt(m, d) if m in ("sk_mean", "df_clean_pct") else f"{d:.0f}")
        print(f"  {D.LABEL[m]:36} {of:>10} {nf:>10} {ds:>9}  {verd}")
    print("\n  (Run the 3 verifier gates separately — tags / flipCard / speechBubble via run_all_gates.sh.)")
    if regressed:
        labels = ", ".join(D.LABEL[m] for m in regressed)
        print(f"\nRESULT: REGRESSED — {labels}")
        if regressed == ["body_any"] and (new["sk_ge50"] - base["sk_ge50"]) > 0:
            print("  NOTE: body_compare is the ONLY regression and the PRIMARY skeleton IMPROVED — this MAY be a")
            print("  documented net-positive (the MEASUREMENT MANDATE judges a structural change on the skeleton).")
            print("  CONFIRM THE CAUSE before shipping:  ./_ab.py <TOGGLE>=1 <the regressed pages' modules>")
        sys.exit(1)
    print("\nRESULT: PASS — every decomposable protected gate held-or-improved vs the committed baseline.")
    if "--commit" in sys.argv:
        # ROUND 501 (LOOP §3 step 7): the full run's own aggregates become the committed baseline — every field.
        sk_wrap = D._load(PATHS["sk"])
        fields = D.gate_fields(D._load(PATHS["cs"]), D._load(PATHS["bc"]), sk_wrap["per_page"], D._load(PATHS["df"]),
                               sk_wrap.get("skipped_parse_errors", 0))
        D.report_gate_write(D.write_gate_baseline(fields, rnd=D._arg_value("--round"), build=D._arg_value("--build")))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    for _flag in ("--round", "--build"):                     # ROUND 501: their values are not gate names
        if _flag in sys.argv and sys.argv.index(_flag) + 1 < len(sys.argv):
            _v = sys.argv[sys.argv.index(_flag) + 1]
            if _v in args:
                args.remove(_v)
    if args == ["verdict"]:
        verdict(); return
    which = [a for a in args if a in RUN] or list(RUN)
    stale, line = _stale_line()
    if stale:
        print("!! " + line)
        print(">> Corpus is NOT 0-stale — a full-regen verdict off a stale corpus is meaningless.")
        print("   Regen the named stale modules (./_stalecheck.sh lists them; python3 _batch_plan.py --codes …), then retry.")
        sys.exit(2)
    for g in which:
        print(f"[gatecheck] running {g} (full corpus)…"); RUN[g]()
    if all(os.path.exists(p) for p in PATHS.values()):
        verdict()
    else:
        have = [g for g, p in PATHS.items() if os.path.exists(p)]
        print(f"[gatecheck] ran {which}; have {have}. Run the rest, then `python3 _gatecheck.py verdict`.")


if __name__ == "__main__":
    main()
