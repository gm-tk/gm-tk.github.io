#!/usr/bin/env python3
"""_ship_ledger.py — the periodic FULL-ship backstop cadence (round 175, deliverable D).

Scoped ship proves held-or-improve by DECOMPOSITION (exact) + a sampled completeness check, but a
mis-specified pattern P can still, in principle, slip a truly-affected module past an unlucky
sample. The full ship (ship.sh: regen EVERY module + the whole gate suite) has no such blind spot.
So we keep it as a periodic backstop: run it every N scoped ships (or whenever a change is
genuinely corpus-wide), which bounds any accumulated under-scoping to at most N rounds.

This ledger just tracks the gap. `ship.sh` records a full ship (resets the counter); `scoped_ship.sh`
records a scoped ship (increments it) and calls `check`, which WARNS (or, past a hard limit, refuses)
when a full ship is overdue.

  python3 _ship_ledger.py check        [--cadence N] [--hard H]   # exit 0 ok / 1 overdue / 2 hard-overdue
  python3 _ship_ledger.py record-scoped [--round R]
  python3 _ship_ledger.py record-full   [--round R] [--build B]
"""
import os, sys, json, time

LEDGER = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "..", "..", "outputs", "_ship_ledger.json"))
CADENCE_DEFAULT = 8      # a full ship at least every 8 scoped ships
HARD_DEFAULT = 16        # past this, scoped_ship refuses until a full ship runs


def _load():
    if os.path.exists(LEDGER):
        try:
            return json.load(open(LEDGER))
        except Exception:
            pass
    return {"last_full": None, "scoped_since": 0, "history": []}


def _save(d):
    json.dump(d, open(LEDGER, "w"), indent=1)


def _opt(args, name, default=None):
    return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default


def _utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def record_full(args):
    d = _load()
    d["last_full"] = {"round": _opt(args, "--round"), "build": _opt(args, "--build"), "utc": _utc()}
    d["scoped_since"] = 0
    _save(d)
    print(f"[ledger] recorded FULL ship (round {d['last_full']['round']}); scoped-since counter reset to 0.")
    return 0


def record_scoped(args):
    d = _load()
    rnd = _opt(args, "--round")
    hist = d.setdefault("history", [])
    # ROUND 428 (session 34, 2026-09-22): one ship per ROUND — a scoped_ship.sh re-run for the same round (a
    # failed decomposition repaired and run again: r425 twice, r428 three times) refreshes the entry's time
    # instead of counting another scoped ship toward the full-regeneration cadence.
    if rnd and hist and hist[-1].get("kind") == "scoped" and str(hist[-1].get("round")) == str(rnd):
        hist[-1]["utc"] = _utc()
        _save(d)
        print(f"[ledger] scoped ship for round {rnd} re-recorded (same round) — {d.get('scoped_since', 0)} scoped ship(s) since the last full ship.")
        return 0
    d["scoped_since"] = d.get("scoped_since", 0) + 1
    hist.append({"round": rnd, "utc": _utc(), "kind": "scoped"})
    d["history"] = d["history"][-40:]
    _save(d)
    print(f"[ledger] recorded scoped ship — {d['scoped_since']} scoped ship(s) since the last full ship.")
    return 0


def check(args):
    cadence = int(_opt(args, "--cadence", str(CADENCE_DEFAULT)))
    hard = int(_opt(args, "--hard", str(HARD_DEFAULT)))
    d = _load()
    lf = d.get("last_full")
    since = d.get("scoped_since", 0)
    lf_str = f"round {lf['round']} ({lf['utc']})" if lf else "NEVER (no full ship on record)"
    print(f"[ledger] last full ship: {lf_str}; scoped ships since: {since} (cadence {cadence}, hard {hard})")
    if lf is None:
        print("  !! NO FULL SHIP ON RECORD — run ./ship.sh once to establish the baseline + ledger.")
        return 2
    if since >= hard:
        print(f"  !! FULL SHIP REQUIRED — {since} scoped ships since the last full ship (>= hard limit {hard}).")
        print("     Run ./ship.sh (full regen + full suite) THIS round before finalising.")
        return 2
    if since >= cadence:
        print(f"  !! FULL SHIP DUE — {since} scoped ships since the last full ship (>= cadence {cadence}).")
        print("     Prefer ./ship.sh (full backstop) this round; it bounds any accumulated under-scoping.")
        return 1
    print(f"  OK — a full-ship backstop is not yet due ({cadence - since} scoped ship(s) of headroom).")
    return 0


CMDS = {"check": check, "record-scoped": record_scoped, "record-full": record_full}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__); return 2
    return CMDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
