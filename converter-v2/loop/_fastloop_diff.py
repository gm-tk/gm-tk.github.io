#!/usr/bin/env python3
"""_fastloop_diff.py — the FAST INNER-LOOP gate proof (exact, not approximate).

Every protected gate metric is a per-page / per-module additive sum or mean. So if a
change only regenerates modules X, every OTHER module's output is byte-identical and
its gate contribution CANNOT move. This tool re-scores ONLY the affected modules X,
patches them into the stored full-corpus BASELINE (refreshed each SHIP by
_fastloop_snapshot.py), and recomputes every protected aggregate. The result is
MATHEMATICALLY IDENTICAL to a full-corpus gate run — it just skips re-parsing the
~190 untouched modules, turning an ~18-20 min A/B round into ~1 min.

  HELD-OR-IMPROVE here == HELD-OR-IMPROVE corpus-wide (proven by decomposition;
  empirically re-confirmed by _fastloop_validate.py against a true full run).

This is the INNER loop only. You still run the full-corpus regen + full gate suite at
the SHIP checkpoint (ship.sh) before finalising — that stays the backstop, so even an
under-scoped affected set cannot ship a regression; it is caught one step later.

USAGE (run from CONVERTER_V2/reference/tests/, AFTER regenerating the affected codes):
  python3 _fastloop_diff.py AGH1004 OSBY201        # diff these modules vs baseline
  python3 _fastloop_diff.py AGH1004 --commit --round 501 [--build 260620.64]
                                                   # PASS -> refresh the fast-loop baseline AND write every
                                                   # gate_baseline.json aggregate (ROUND 501)
  python3 _fastloop_diff.py --gate-baseline-check  # committed aggregates == the shipped state? (exit 1 on drift)

Env passthrough: set any A/B toggle (e.g. ACTHEAD_OFF=1) when you regen the codes to
isolate a single fix's effect, then run this to read it off the gates.
"""
import os, sys, json, copy, subprocess, time
import _corpus  # round128: nesting-aware corpus paths

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUTS = os.path.normpath(os.path.join(BASE, "..", "..", "outputs"))
BASELINE = os.path.join(OUTPUTS, "_fastloop_baseline")
CURRENT = os.path.join(OUTPUTS, "_fastloop_current")
PY = sys.executable

# ---- protected metrics: polarity (+1 higher better, -1 lower better) + labels --------
POLARITY = {"sk_mean": +1, "sk_ge50": +1, "sk_ge75": +1,
            "cs_exact": +1, "cs_extra": -1, "cs_missing": -1,
            "body_any": -1,
            "df_clean_pct": +1, "df_leak_occ": -1, "df_leak_pages": -1}
ORDER = ["sk_mean", "sk_ge50", "sk_ge75", "cs_exact", "cs_extra", "cs_missing",
         "body_any", "df_clean_pct", "df_leak_occ", "df_leak_pages"]
LABEL = {"sk_mean": "skeleton SCAFFOLD mean %", "sk_ge50": "skeleton pages >=50%",
         "sk_ge75": "skeleton pages >=75%", "cs_exact": "compare_structure exact chain",
         "cs_extra": "compare_structure EXTRA container",
         "cs_missing": "compare_structure missing container",
         "body_any": "body_compare ANY breakdown", "df_clean_pct": "defect structurally-clean %",
         "df_leak_occ": "literal-[tag] leak (occ)", "df_leak_pages": "literal-[tag] leak (pages)"}
# context-only metrics (page/element counts — printed, never a pass/fail)
CONTEXT = ["sk_pages", "cs_matched", "body_pages", "df_total", "df_clean"]


# ---- pure aggregate functions over the raw gate-json structures ----------------------
def cs_metrics(rows):
    ok = [r for r in rows if "error" not in r and "matched" in r]
    s = lambda k: sum(r.get(k, 0) for r in ok)
    return {"cs_matched": s("matched"), "cs_exact": s("exact_chain"),
            "cs_extra": s("claude_extra_container"), "cs_missing": s("claude_missing_container")}


def _bc_broken(r):
    """Replicates body_compare.main().flags() — kept in sync; _fastloop_validate.py
    asserts bc_metrics(full)==the gate's printed ANY count, so any drift is caught."""
    if r["over_capture"] >= 0.40 and r["biggest_widget_chars"] > 400 and r["lost_blocks"] >= 3:
        return True
    if r["multi_type"] >= 4:
        return True
    if r["empty_widgets"]:
        return True
    return False


def bc_metrics(pages):
    return {"body_any": sum(1 for r in pages if _bc_broken(r)), "body_pages": len(pages)}


def sk_metrics(per_page):
    vals = [p["scaffold"] for p in per_page]
    n = len(vals)
    return {"sk_mean": (sum(vals) / n if n else 0.0), "sk_pages": n,
            "sk_ge50": sum(1 for v in vals if v >= 0.50),
            "sk_ge75": sum(1 for v in vals if v >= 0.75)}


def df_metrics(dj):
    pmp, pmc = dj["per_module_pages"], dj["per_module_clean"]
    pm, pmw = dj.get("per_module", {}), dj.get("per_module_pages_with_class", {})
    total = sum(pmp.values())
    clean = sum(pmc.values())
    leak_occ = sum(pm.get(m, {}).get("A_literal_tag_leak", 0) for m in pmp)
    leak_pages = sum(pmw.get(m, {}).get("A_literal_tag_leak", 0) for m in pmp)
    return {"df_total": total, "df_clean": clean,
            "df_clean_pct": (100 * clean / total if total else 0.0),
            "df_leak_occ": leak_occ, "df_leak_pages": leak_pages}


# ---- patching: baseline with the affected modules' fresh scoped results --------------
def patch_cs(base_rows, scoped_rows, affected):
    by = {r["module"]: r for r in base_rows if "module" in r}
    sc = {r["module"]: r for r in scoped_rows if "module" in r}
    for m in affected:
        if m in sc:
            by[m] = sc[m]
        else:
            by.pop(m, None)
    return list(by.values())


def patch_pages(base_pages, scoped_pages, affected):
    """bc and skeleton per_page rows both carry 'module'; replace affected wholesale."""
    kept = [p for p in base_pages if p["module"] not in affected]
    add = [p for p in scoped_pages if p["module"] in affected]
    return kept + add


def patch_df(base_dj, scoped_dj, affected):
    d = copy.deepcopy(base_dj)
    for key in ("per_module_pages", "per_module_clean", "per_module", "per_module_pages_with_class"):
        d.setdefault(key, {})
        sc = scoped_dj.get(key, {})
        for m in affected:
            d[key].pop(m, None)
            if m in sc:
                d[key][m] = sc[m]
    return d


# ---- baseline load + aggregate (also used by _fastloop_snapshot.py) ------------------
def _load(p):
    return json.load(open(p))


def _baseline_paths():
    return {"cs": os.path.join(BASELINE, "structural_comparison.json"),
            "bc": os.path.join(BASELINE, "body_compare.json"),
            "sk": os.path.join(BASELINE, "skeleton.json"),
            "df": os.path.join(BASELINE, "defect.json")}


def baseline_loaded():
    return all(os.path.exists(p) for p in _baseline_paths().values())


def baseline_structs():
    p = _baseline_paths()
    return (_load(p["cs"]), _load(p["bc"]), _load(p["sk"])["per_page"], _load(p["df"]))


def baseline_aggregates():
    cs, bc, sk, df = baseline_structs()
    return {**cs_metrics(cs), **bc_metrics(bc), **sk_metrics(sk), **df_metrics(df)}


# ---- ROUND 501 (session 49 Round 1, 25 Sept 2026): THE COMMITTED BASELINE'S AGGREGATES ARE WRITTEN BY THE TOOL ----------
# LOOP §3 step 7 (the third /loop-review): the r494–r498 finalise scripts typed gate_baseline.json fields by hand, updated
# pages_ge_50 / raw_mean_pct but not mean_scaffold_pct / median_scaffold_pct / body_compare.any_breakdown, and eight rounds were
# judged against a stale baseline. From r501 on, `--commit` (and `_gatecheck.py --commit` after a FULL run) writes EVERY
# aggregate below itself, computed exactly as each gate prints it; a finalise script edits notes only.
# `--gate-baseline-check` compares the committed file with the fast-loop baseline and exits 1 on any drift.
GATE_BASELINE = os.path.join(BASE, "gate_baseline.json")


def gate_fields(cs_rows, bc_pages, sk_per_page, df, sk_skipped=0):
    """Every aggregate gate_baseline.json carries, from the four raw gate structures (the same
    formulas and roundings as _skeleton_compare.py / compare_structure.py / body_compare.py /
    _structural_defect_audit.py print: the median is the gate's upper median, sorted[n // 2])."""
    ok = [r for r in cs_rows if "error" not in r and "matched" in r]
    s = lambda k: sum(r.get(k, 0) for r in ok)
    sca = [p["scaffold"] for p in sk_per_page]
    raw = [p.get("raw", 0.0) for p in sk_per_page]
    n = len(sca)
    srt = sorted(sca)
    dm = df_metrics(df)
    over = sum(1 for r in bc_pages if r["over_capture"] >= 0.40 and r["biggest_widget_chars"] > 400 and r["lost_blocks"] >= 3)
    return {
        "skeleton": {"mean_scaffold_pct": round(100 * sum(sca) / n, 2) if n else 0.0,
                     "median_scaffold_pct": round(100 * srt[n // 2], 1) if n else 0.0,
                     "pages_ge_50": sum(1 for v in sca if v >= 0.50), "pages_ge_75": sum(1 for v in sca if v >= 0.75),
                     "pages_ge_90": sum(1 for v in sca if v >= 0.90),
                     "raw_mean_pct": round(100 * sum(raw) / n, 2) if n else 0.0,
                     "pairs": n, "pairs_skipped": int(sk_skipped)},
        "compare_structure": {"exact_chain": s("exact_chain"), "claude_extra_container": s("claude_extra_container"),
                              "claude_missing_container": s("claude_missing_container"),
                              "row_wrap_missing": s("row_wrap_missing")},
        "body_compare": {"any_breakdown": bc_metrics(bc_pages)["body_any"], "over_capture": over,
                         "runaway": sum(1 for r in bc_pages if r["multi_type"] >= 4),
                         "empty_container": sum(1 for r in bc_pages if r["empty_widgets"])},
        "structural_defect": {"clean_pages": dm["df_clean"], "total_pages": dm["df_total"],
                              "clean_pct": round(dm["df_clean_pct"], 1),
                              "literal_tag_leak_occ": dm["df_leak_occ"], "leak_pages": dm["df_leak_pages"]},
    }


def _gb_lines():
    src = open(GATE_BASELINE, encoding="utf-8", newline="").read()
    eol = "\r\n" if "\r\n" in src else "\n"
    return src.split(eol), eol


def _gb_section(L, key):
    """(open, close) line indices of the top-level 2-space `"key": {` section."""
    op = [i for i, l in enumerate(L) if l == f'  "{key}": {{']
    assert len(op) == 1, f"gate_baseline.json: section {key} found {len(op)}x"
    cl = op[0] + 1
    while cl < len(L) and not L[cl].startswith("  }"):
        cl += 1
    assert cl < len(L), f"gate_baseline.json: section {key} not closed"
    return op[0], cl


def write_gate_baseline(fields, rnd=None, build=None):
    """Section-aware LINE edit of gate_baseline.json (the file mixes 2- and 4-space indents, so it is never
    re-serialised whole): each `    "field": value` line inside its section is replaced in place, its comma kept.
    Returns the list of (section.field, old, new) that changed. Validates the JSON before replacing the file."""
    import shutil, time as _t
    L, eol = _gb_lines()
    changed = []
    for sec, kv in fields.items():
        op, cl = _gb_section(L, sec)
        for k, v in kv.items():
            hit = [i for i in range(op + 1, cl) if L[i].startswith(f'    "{k}": ')]
            assert len(hit) == 1, f"gate_baseline.json: {sec}.{k} found {len(hit)}x"
            i = hit[0]
            comma = "," if L[i].rstrip().endswith(",") else ""
            old = L[i].split(": ", 1)[1].rstrip().rstrip(",")
            new = json.dumps(v)
            if old != new:
                changed.append((f"{sec}.{k}", old, new))
                L[i] = f'    "{k}": {new}{comma}'
    meta = {"date": _t.strftime("%Y-%m-%d")}
    if rnd is not None:
        meta["round"] = int(rnd)
    if build:
        meta["build"] = str(build)
    op, cl = _gb_section(L, "_meta")
    for k, v in meta.items():
        hit = [i for i in range(op + 1, cl) if L[i].startswith(f'    "{k}": ')]
        assert len(hit) == 1, f"gate_baseline.json: _meta.{k} found {len(hit)}x"
        i = hit[0]
        comma = "," if L[i].rstrip().endswith(",") else ""
        old = L[i].split(": ", 1)[1].rstrip().rstrip(",")
        new = json.dumps(v, ensure_ascii=False)
        if old != new:
            changed.append((f"_meta.{k}", old, new))
            L[i] = f'    "{k}": {new}{comma}'
    out = eol.join(L)
    json.loads(out)                                             # must parse before it replaces the file
    bak = GATE_BASELINE + (f".pre-r{int(rnd)}.bak" if rnd is not None else ".pre-commit.bak")
    if not os.path.exists(bak):
        shutil.copyfile(GATE_BASELINE, bak)
    tmp = GATE_BASELINE + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)
    assert os.path.getsize(tmp) > 1000, "refusing to write a truncated gate_baseline.json"
    os.replace(tmp, GATE_BASELINE)
    return changed


def report_gate_write(changed):
    agg = [c for c in changed if not c[0].startswith("_meta.")]
    print(f"[commit] gate_baseline.json: every aggregate written by the tool — {len(agg)} changed"
          + (": " + "; ".join(f"{k} {o} -> {n}" for k, o, n in agg) if agg else " (all already equal)")
          + ("  | " + "; ".join(f"{k} {n}" for k, o, n in changed if k.startswith("_meta.")) if len(agg) < len(changed) else ""))


def _arg_value(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv and sys.argv.index(flag) + 1 < len(sys.argv) else None


def gate_baseline_check():
    """--gate-baseline-check: the committed aggregates must equal the fast-loop baseline's (the shipped state)."""
    cs, bc, sk, df = baseline_structs()
    wrap = _load(_baseline_paths()["sk"])
    want = gate_fields(cs, bc, sk, df, wrap.get("skipped_parse_errors", 0))
    gb = _load(GATE_BASELINE)
    bad = []
    for sec, kv in want.items():
        for k, v in kv.items():
            have = gb.get(sec, {}).get(k)
            print(f"  {sec + '.' + k:42} committed {str(have):>10}   shipped-state {str(v):>10}  {'OK' if have == v else 'DRIFT'}")
            if have != v:
                bad.append(f"{sec}.{k}")
    print(f"\nGATE-BASELINE CHECK: {'PASS — every committed aggregate equals the shipped state' if not bad else 'DRIFT — ' + ', '.join(bad)}")
    return 0 if not bad else 1


def commit_baseline(new_cs, new_bc, new_sk, new_df, sk_skipped=0):
    """Scoped baseline refresh (round 175, step 5): overwrite the fast-loop baseline with the
    ALREADY-PATCHED full structs (affected modules re-scored, every other module unchanged) and
    refresh the content manifest to the new shipped state. Exact by construction — no full-corpus
    re-score. Called by `_fastloop_diff.py … --commit` only after a PASS verdict.
    ROUND 501: it also writes every gate_baseline.json aggregate (write_gate_baseline) and keeps the
    skeleton wrapper's summary fields in step with its per_page rows."""
    import time as _t
    p = _baseline_paths()
    json.dump(new_cs, open(p["cs"], "w"), indent=1, ensure_ascii=False)
    json.dump(new_bc, open(p["bc"], "w"), indent=1)
    sk_wrap = _load(p["sk"]) if os.path.exists(p["sk"]) else {}
    sk_wrap["per_page"] = new_sk
    if new_sk:
        sk_wrap["pages"] = len(new_sk)
        sk_wrap["scaffold_mean"] = sum(x["scaffold"] for x in new_sk) / len(new_sk)
        sk_wrap["raw_mean"] = sum(x.get("raw", 0.0) for x in new_sk) / len(new_sk)
        sk_wrap["skipped_parse_errors"] = int(sk_skipped)
    json.dump(sk_wrap, open(p["sk"], "w"))
    report_gate_write(write_gate_baseline(gate_fields(new_cs, new_bc, new_sk, new_df, sk_skipped),
                                          rnd=_arg_value("--round"), build=_arg_value("--build")))
    json.dump(new_df, open(p["df"], "w"))
    agg = {**cs_metrics(new_cs), **bc_metrics(new_bc), **sk_metrics(new_sk), **df_metrics(new_df)}
    man = {"utc": _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime()), "scoped_commit": True, "aggregates": agg}
    json.dump(man, open(os.path.join(BASELINE, "manifest.json"), "w"), indent=1)
    try:
        import _content_manifest as CM
        CM.write_manifest(CM.DEFAULT_MANIFEST, CM.corpus_manifest())
        print(f"[commit] fast-loop baseline PATCHED ({len(new_sk)} pages) + content manifest refreshed "
              f"— this is now the shipped state the next inner loop measures against.")
    except Exception as e:
        print(f"[commit] baseline patched; content-manifest refresh FAILED: {e}")


def _fmt(metric, v):
    if metric == "sk_mean":
        return f"{v * 100:.2f}"
    if metric == "df_clean_pct":
        return f"{v:.2f}"
    return f"{v:.0f}"


def print_aggregates(title, agg):
    print(f"\n{title}")
    for m in ORDER:
        print(f"  {LABEL[m]:36} {_fmt(m, agg[m]):>10}")
    ctx = "  ".join(f"{m}={agg[m]:.0f}" for m in CONTEXT if m in agg)
    print(f"  (context: {ctx})")


# ---- the scoped re-score of the affected modules -------------------------------------
def run_scoped(codes):
    # ROUND 428 (session 34, 2026-09-22): the scoped re-score honours compare_exclusions.txt (D10-6 / r343 — one
    # list, every gate) — a spot-check sample that draws an excluded module (CEDW303) must not enter the
    # decomposition as a NEW PAIR the corpus gates never score.
    _excl = set(_corpus.excluded())
    codes = [c for c in codes if c not in _excl]
    os.makedirs(CURRENT, exist_ok=True)
    devnull = subprocess.DEVNULL
    subprocess.run([PY, "compare_structure.py", *codes], cwd=BASE, check=True, stdout=devnull)
    scoped_cs = _load(os.path.join(BASE, "structural_comparison.json"))
    subprocess.run([PY, "body_compare.py", *codes], cwd=BASE, check=True, stdout=devnull)
    scoped_bc = _load(os.path.join(BASE, "body_compare.json"))
    skout = os.path.join(CURRENT, "skeleton_scoped.json")
    subprocess.run([PY, "_skeleton_compare.py", *codes, "--json", skout], cwd=BASE, check=True, stdout=devnull)
    scoped_sk = _load(skout)["per_page"]
    global SCOPED_SK_SKIPPED                     # ROUND 501: carried into gate_baseline.json skeleton.pairs_skipped
    SCOPED_SK_SKIPPED = int(_load(skout).get("skipped_parse_errors", 0))
    dfout = os.path.join(CURRENT, "defect_scoped.json")
    subprocess.run([PY, "_structural_defect_audit.py", *codes, "--json", dfout], cwd=BASE, check=True, stdout=devnull)
    scoped_df = _load(dfout)
    return scoped_cs, scoped_bc, scoped_sk, scoped_df


# ---- freshness guard: the inner loop is only EXACT if (a) the affected modules were actually
# regenerated after your last edit, and (b) the baseline still reflects every UNAFFECTED module's
# current on-disk output. Both have silently produced wrong deltas before (round 89 ran on a
# round-85 baseline) — so the tool now checks instead of trusting memory. -----------------------
SCOPED_SK_SKIPPED = 0
CLAUDE_DIR = os.path.normpath(os.path.join(BASE, "..", "..", "..", "01-Claude_Modules_"))
SRC_DIRS = (os.path.join(BASE, "..", "..", "app", "js"), os.path.join(BASE, "..", "..", "data"))


def _newest_source_mtime():
    newest = 0.0
    for root in SRC_DIRS:
        for dp, _dn, fns in os.walk(root):
            for fn in fns:
                if fn == "Config.js":            # UI-only AppVersion, never stamped in output
                    continue
                if fn.endswith((".js", ".json")):
                    newest = max(newest, os.path.getmtime(os.path.join(dp, fn)))
    return newest


def _module_newest_output(code):
    d = _corpus.mdir(CLAUDE_DIR, code)
    best = 0.0
    if os.path.isdir(d):
        for fn in os.listdir(d):
            if fn.endswith(".html"):
                best = max(best, os.path.getmtime(os.path.join(d, fn)))
    return best


def freshness_guard(affected):
    """Refuse to print deltas off a stale baseline / un-regenerated affected set, unless
    --allow-stale-baseline is passed. Cheap (mtimes only)."""
    problems, src = [], _newest_source_mtime()
    not_regen = [c for c in sorted(affected) if _module_newest_output(c) + 1 < src]
    if not_regen:
        problems.append(
            "AFFECTED modules NOT regenerated since your last source edit — their scored delta is "
            f"STALE: {' '.join(not_regen)}\n"
            f"      fix:  ./iterate.sh {' '.join(not_regen)}   (regens + scores; or batch_convert.cjs <codes> --force)")
    base_t = os.path.getmtime(os.path.join(BASELINE, "skeleton.json"))
    drifted = [c for c in (_corpus.mods(CLAUDE_DIR) if os.path.isdir(CLAUDE_DIR) else [])
               if c not in affected and _module_newest_output(c) > base_t + 1]
    # ROUND 428 (session 34, 2026-09-22): a module regenerated after the snapshot whose pages are BYTE-IDENTICAL to
    # the last-shipped content manifest has not drifted — its baseline contribution is exactly right (the scoped
    # ship's spot-check sample is regenerated WITH the fix ON and proven identical; a second sample after a re-plan
    # left the first one "newer" by mtime alone). The same content-hash rule _content_manifest.py fresh applies.
    if drifted:
        try:
            import _content_manifest as _CM
            _ref = _CM.load_manifest(_CM.DEFAULT_MANIFEST) if os.path.exists(_CM.DEFAULT_MANIFEST) else None
        except Exception:
            _ref = None
        if _ref:
            def _identical(c):
                d = _corpus.mdir(CLAUDE_DIR, c)
                if not os.path.isdir(d): return False
                for dp, _dn, fns in os.walk(d):
                    for fn in fns:
                        if not fn.endswith(".html"): continue
                        full = os.path.join(dp, fn)
                        rel = os.path.relpath(full, CLAUDE_DIR).replace(os.sep, "/")
                        if _ref.get(rel) != _CM._md5(full): return False
                return True
            drifted = [c for c in drifted if not _identical(c)]
    if drifted:
        ex = " ".join(sorted(drifted)[:6]) + (" …" if len(drifted) > 6 else "")
        problems.append(
            f"BASELINE is STALE — {len(drifted)} UNAFFECTED module(s) were regenerated AFTER the "
            f"baseline snapshot, so their baseline contribution is wrong (e.g. {ex}).\n"
            "      fix:  ./ship.sh   (full 0-stale regen + refresh), or python3 _fastloop_snapshot.py if already fresh")
    if problems:
        print("\n".join("!! " + p for p in problems))
        if "--allow-stale-baseline" in sys.argv:
            print(">> --allow-stale-baseline set: proceeding anyway — DELTAS MAY BE WRONG.\n")
        else:
            print(">> Refusing to report deltas off a stale baseline. Override: --allow-stale-baseline\n")
            sys.exit(2)


def _sk_skipped():
    """ROUND 501: pairs skipped (parse error) in the patched state — the baseline's own plus the scoped re-score's
    (the protected criterion is 0, so any double count errs towards reporting)."""
    try:
        base = int(_load(_baseline_paths()["sk"]).get("skipped_parse_errors", 0))
    except Exception:
        base = 0
    return base + SCOPED_SK_SKIPPED


def main():
    # ROUND 289 — --accept-named takes ONE comma-separated value; strip it (and its
    # value) before the positional module codes are read, or the named metric would be
    # mistaken for a module code.
    _argv = list(sys.argv[1:])
    # ROUND 501: --round N / --build X (the gate_baseline.json _meta the --commit writes) take a value too.
    for _flag in ("--accept-named", "--round", "--build"):
        if _flag in _argv:
            _i = _argv.index(_flag)
            del _argv[_i:_i + 2]
    if "--gate-baseline-check" in _argv:
        if not baseline_loaded():
            sys.exit("no fast-loop baseline — nothing to check against.")
        sys.exit(gate_baseline_check())
    codes = [a for a in _argv if not a.startswith("-")]
    if not codes:
        sys.exit("usage: python3 _fastloop_diff.py CODE1 [CODE2 ...]   (the regenerated modules)")
    if not baseline_loaded():
        sys.exit("no baseline yet — run `python3 _fastloop_snapshot.py` after a full 0-stale regen first.")
    affected = set(codes)
    freshness_guard(affected)

    man = {}
    mp = os.path.join(BASELINE, "manifest.json")
    if os.path.exists(mp):
        man = _load(mp)

    base_cs, base_bc, base_sk, base_df = baseline_structs()
    base_agg = {**cs_metrics(base_cs), **bc_metrics(base_bc), **sk_metrics(base_sk), **df_metrics(base_df)}

    print(f"re-scoring {len(affected)} affected module(s): {' '.join(sorted(affected))}")
    sc_cs, sc_bc, sc_sk, sc_df = run_scoped(codes)

    new_cs = patch_cs(base_cs, sc_cs, affected)
    new_bc = patch_pages(base_bc, sc_bc, affected)
    new_sk = patch_pages(base_sk, sc_sk, affected)
    new_df = patch_df(base_df, sc_df, affected)
    new_agg = {**cs_metrics(new_cs), **bc_metrics(new_bc), **sk_metrics(new_sk), **df_metrics(new_df)}

    # leave the live cs/bc jsons in a coherent FULL state (not the scoped fragment)
    json.dump(new_cs, open(os.path.join(BASE, "structural_comparison.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(new_bc, open(os.path.join(BASE, "body_compare.json"), "w"), indent=1)

    print(f"baseline taken: {man.get('utc', '(unknown — manifest missing)')}")
    print("(unaffected modules unchanged by construction — corpus aggregate moves by exactly the affected-set delta)\n")
    hdr = f"  {'metric':36} {'baseline':>10} {'new':>10} {'delta':>9}  verdict"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    regressed = []
    for m in ORDER:
        o, n = base_agg[m], new_agg[m]
        d = n - o
        if abs(d) < 1e-9:
            verdict = "HELD"
        elif d * POLARITY[m] > 0:
            verdict = "IMPROVED"
        else:
            verdict = "REGRESSED"
            regressed.append(LABEL[m])
        dstr = ("+" if d > 0 else "") + (_fmt(m, d) if m in ("sk_mean", "df_clean_pct") else f"{d:.0f}")
        print(f"  {LABEL[m]:36} {_fmt(m, o):>10} {_fmt(m, n):>10} {dstr:>9}  {verdict}")

    # context line (did page/element universe shift?)
    ctx = "  ".join(f"{m}: {base_agg.get(m, 0):.0f}->{new_agg.get(m, 0):.0f}" for m in CONTEXT)
    print(f"\n  context (no pass/fail): {ctx}")

    print()
    if regressed:
        # ROUND 289 — THE NAMED-MOVEMENT OVERRIDE. A metric may move the "wrong" way for a
        # reason the round has decomposed page by page and named in its changelog — the
        # documented net-positive class (r176/r194/r220/r235/r284): the SCAFFOLD view
        # collapses a widget to one marker, so a page that matched the gold's built widget
        # only by coincidence through a placeholder marker scores lower once real content
        # ships, while the RAW view rises. Rather than let an operator edit the baseline by
        # hand (silent, unreviewable), this requires the mover to be NAMED on the command
        # line; the name is recorded in the baseline manifest so the next round can see why
        # the line moved. It refuses any metric the operator did NOT name, so it can never
        # wave through an unexamined regression.
        accepted = []
        ai = sys.argv.index("--accept-named") if "--accept-named" in sys.argv else -1
        if ai > -1 and ai + 1 < len(sys.argv):
            accepted = [a.strip() for a in sys.argv[ai + 1].split(",") if a.strip()]
        unnamed = [r for r in regressed if not any(a.lower() in r.lower() for a in accepted)]
        if ai > -1 and not unnamed:
            print(f"RESULT: MOVED, ACCEPTED AS NAMED — {', '.join(regressed)}")
            print("        Every mover was named on the command line and must be decomposed in the")
            print("        round's changelog entry (which page, which mechanism). Recorded in the manifest.")
            if "--commit" in sys.argv:
                commit_baseline(new_cs, new_bc, new_sk, new_df, _sk_skipped())
                try:
                    mp = os.path.join(BASELINE, "manifest.json")
                    mm = json.load(open(mp))
                    mm["accepted_named_movement"] = regressed
                    json.dump(mm, open(mp, "w"), indent=1)
                    print(f"[commit] recorded accepted named movement: {', '.join(regressed)}")
                except Exception as e:                                   # pragma: no cover
                    print(f"[commit] could not record the named movement: {e}")
            return
        print(f"RESULT: FAIL — REGRESSED: {', '.join(regressed)}")
        if ai > -1:
            print(f"        NOT NAMED (so not accepted): {', '.join(unnamed)}")
        print("        (inner-loop only — investigate before the ship checkpoint; toggle the fix OFF and re-run to isolate.)")
        sys.exit(1)
    print("RESULT: PASS — every protected gate held-or-improved corpus-wide (exact, decomposition-proven).")
    if "--commit" in sys.argv:
        commit_baseline(new_cs, new_bc, new_sk, new_df, _sk_skipped())
    else:
        print("        Still run ship.sh (full regen + full suite + 0-stale + baseline refresh) before finalising,")
        print("        or scoped_ship.sh (which calls this with --commit to refresh the baseline in place).")


if __name__ == "__main__":
    main()
