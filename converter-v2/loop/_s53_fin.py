#!/usr/bin/env python3
"""_s53_fin.py — session 53 (a copy of _s52_fin.py)'s shared (a copy of _s49_fin.py; the in-flight and no-round anchors widened) FINALISE helper (WSL). One call per shipped engine round:
changelog prepend, Config.js AppVersion bump, OPERATING_GUIDE §9 / §11 / §14, the gate_baseline.json NOTE + _meta.build
(the aggregates are written by _fastloop_diff.py --commit since r501 — this never touches them), and the LOOP_STATE.md
Position roll (in-flight marker -> no-round line; LAST SHIPPED / Before it / Before them; plateau; standing facts; Round log;
the displaced lines archived verbatim). Every anchor is asserted unique before anything is written."""
import io, os, json, re, shutil, subprocess

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")


def now():
    return subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()


def rd(p):
    return io.open(p, encoding="utf-8", newline="").read()


def wr(p, s):
    tmp = p + ".tmp"
    io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000
    os.replace(tmp, p)


def one(hay, needle, what):
    n = hay.count(needle)
    assert n == 1, f"{what}: anchor found {n}x: {needle[:90]!r}"


def finalise(*, N, old_build, new_build, entry, config_comment, og9=None, og11=None, og14, gb_note,
             no_round, last_shipped, before_them_add, plateau, standing, roundlog, archive_extra="",
             before_them_prev_first=None):
    """N: this round's number. og9: the new §9 skeleton line prefix (replaces '**ROUND <prev> BASELINE' with it + 'Previous: ');
    og11: the new §11 toggle row (inserted above the newest row); og14: the new §14 build bullet (inserted above the newest).
    before_them_add: text inserted after 'the ' in the Before-them list for the round that leaves 'Before it'."""
    PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
    assert sc.startswith(head) and f"(round {N}," not in sc[:6000]
    PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = f'\tstatic AppVersion = "{old_build}";'; one(sj, oldj, "Config")
    PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
    m9 = re.search(r"^\| \*\*Skeleton \(PRIMARY\)\*\* \| `python3 _skeleton_compare\.py` \| \*\*ROUND (\d+) BASELINE", so, re.M)
    assert m9, "OG §9 skeleton line"
    m11 = re.search(r"^\| `[A-Z0-9_]+_OFF` \| (\d+) \|", so, re.M)
    assert m11, "OG §11 newest toggle row"
    a14 = f"- **Build:** `{old_build}`"; one(so, a14, "OG §14")
    S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")

    def find(prefix, start=False):
        idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
        assert len(idx) == 1, (prefix, idx)
        return idx[0]
    fl = find(f"- **ROUND {N} IN FLIGHT — NOT PROVEN")
    others = [i for i, l in enumerate(L) if l.startswith("- **No round in flight**") or re.match(r"- \*\*Before r\d+: no round in flight\*\*", l)]
    assert len(others) == 1, others
    ls = find("- LAST SHIPPED: **r")
    prev = re.match(r"- LAST SHIPPED: \*\*r(\d+)\*\*", L[ls]).group(1)
    bi = [i for i, l in enumerate(L) if re.match(r"- Before it: \*\*r\d+\*\* \(build ", l)]
    assert len(bi) == 1, ("Before it (build", bi)
    bi = bi[0]
    bt = find("- Before them: **r")
    pl = find("- Plateau window (§4): **")
    sf = find("- Standing facts: AppVersion **")
    rl = find("## Round log")
    assert re.match(r"^- Plateau window \(§4\): \*\*\d of 3\*\* — ", L[pl]) and re.match(r"^- Standing facts: AppVersion \*\*[\d.]+\*\* \(", L[sf])
    assert re.match(r"- Before them: \*\*r(\d+) → r(\d+)\*\* \((\d+\.\d+) → (\d+\.\d+) — ", L[bt]), "Before-them shape"
    assert re.match(r"- Before it: \*\*r(\d+)\*\* \(build (\d+\.\d+)", L[bi]), "Before-it shape"
    # ---- writes
    wr(PC, head + entry.strip() + "\n\n" + sc[len(head):]); print("changelog ok")
    wr(PJ, sj.replace(oldj, f"\t// ROUND {N} ({new_build}): {config_comment}\n" + f'\tstatic AppVersion = "{new_build}";')); print("config ok")
    if og9:
        so = so.replace(m9.group(0), og9 + " Previous: **ROUND " + m9.group(1) + " BASELINE", 1)
    if og11:
        so = so.replace(m11.group(0), og11 + "\n" + m11.group(0), 1)
    so = so.replace(a14, og14 + "\n" + a14, 1)
    wr(PO, so); print("OG ok")
    P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json")
    shutil.copyfile(P, P + f".pre-r{N}-note.bak")
    G = rd(P).split("\n")
    hits = [i for i, l in enumerate(G) if re.match(r'^    "_note_r\d+": ', l)]
    assert hits, "gate_baseline _note anchor"
    G.insert(hits[0], f'    "_note_r{N}": ' + json.dumps(gb_note, ensure_ascii=False) + ",")
    bl = [i for i, l in enumerate(G) if l.startswith('    "build": ')]
    assert len(bl) == 1
    G[bl[0]] = f'    "build": "{new_build}",'
    out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline note + build ok")
    os.makedirs(os.path.join(ROOT, "_Backups", "loop_state"), exist_ok=True)
    shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", f"LOOP_STATE.md.pre-r{N}-finalise.bak"))
    marker, prior_nr, before_it = L[fl], L[others[0]], L[bi]
    L[fl] = no_round
    L[ls] = L[ls].replace(f"- LAST SHIPPED: **r{prev}**", f"- Before it: **r{prev}**", 1)
    L[ls] = last_shipped + "\n" + L[ls]
    m = re.match(r"- Before them: \*\*r(\d+) → r(\d+)\*\* \((\d+\.\d+) → (\d+\.\d+) — ", L[bt])
    assert m, "Before-them shape"
    bprev = re.match(r"- Before it: \*\*r(\d+)\*\* \(build (\d+\.\d+)", before_it)
    assert bprev, "Before-it shape"
    L[bt] = L[bt].replace(m.group(0), f"- Before them: **r{bprev.group(1)} → r{m.group(2)}** ({bprev.group(2)} → {m.group(4)} — {before_them_add}, ", 1)
    L[pl], npl = re.subn(r"^- Plateau window \(§4\): \*\*\d of 3\*\* — ", lambda _m: plateau, L[pl], count=1)
    L[sf], nsf = re.subn(r"^- Standing facts: AppVersion \*\*[\d.]+\*\* \(", lambda _m: standing, L[sf], count=1)
    assert npl == 1 and nsf == 1, ("plateau / standing anchors", npl, nsf)
    L.insert(rl + 1, roundlog)
    for i in sorted([others[0], bi], reverse=True):
        del L[i]
    io.open(A, "a", encoding="utf-8", newline="\n").write(
        f"\n## Position — Before it r{bprev.group(1)} + the prior no-round line (verbatim, s53 r{N})\n\n" + before_it + "\n" + prior_nr + "\n"
        f"\n## Session 53 — r{N} PICK (the in-flight marker, verbatim) + what shipped\n\n" + marker + "\n" + archive_extra + "\n")
    wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
