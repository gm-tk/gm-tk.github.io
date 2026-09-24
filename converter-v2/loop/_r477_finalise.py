#!/usr/bin/env python3
"""ROUND 477 finalise (session 43 Round 9 — KB c75: the gathered body text keeps its links, GATHERLINKS_OFF) —
BUILD_CHANGELOG.md (prepend), Config.js AppVersion 260620.40 -> 260620.41, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (build / round /
notes / skeleton / cs), KB_AMALGAMATION_STATUS.md row 75, LOOP_STATE.md (marker cleared, Position, plateau, round log, next-session line;
the PICK → archive). Line edits only; .bak kept; nothing written until every anchor is found. WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 477," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.40";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 476 BASELINE"; a11 = "| `WIDGETLINKS_OFF` | 476 |"; a14 = "- **Build:** `260620.40` (round 476"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
k75 = "triggers excluded by measurement — `outputs/_s43_r8_linkprec.py`).** |"
assert sk.count(k75) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 477 IN FLIGHT — NOT PROVEN**", "- **Before r477: no round in flight**", "- LAST SHIPPED: **r476**", "- Before it: **r475**",
          "- Plateau window (§4): **2 of 3** — r476", "- Standing facts: AppVersion 260620.40", "## Round log", "**Next session starts with:**",
          "## Session 43 — Round 9 PICK (engine r477)", "- Before them: **r474**"):
    find(p)

entry = """## 2026-09-24 (round 477, build 260620.41) — KB CONSTRAINT 75 FOR GATHERED BODY TEXT: a tag line's paragraph and the black paragraphs gathered after it (an activity's body, an alert's content) keep the writer's inline links — public web targets, whole-phrase anchors

### 1. WHAT CHANGED

**The find** (session 43 Round 9 — the r475 link census's remaining free-body paths, traced with `outputs/_s43_r8_linkdbg.cjs`): ANZH104-6.0's "use an app like __Google Lens__ or __Seek by iNaturalist__" (inside activity 6B) is rendered by `ContentConverter.#element`'s body default — `renderBlackText(MediaBuilder.gatherFollowing(…), run)` with NO links; OSBY401's "Complete an online contact form" (a Netsafe alert) by `#calloutOpen` with only the alert TAG's own `block.links`, while its content was gathered from the following items. `gatherFollowing` returned the joined text, never the gathered items' links.

**The fix** (`MediaBuilder.gatherFollowing` records the gathered items' `block.links` — the tag's own included — on `it._gatheredLinks`; `ContentConverter.#gatheredLinks` hands them to the `#element` body default and the callout content; data `Emit_Templates.body_region.gathered_links` {enabled, env, exclude_targets, min_text_chars 3}; env **`GATHERLINKS_OFF`**, byte-identical OFF): the free-body weave (exact phrase, first occurrence per line, never inside an `<a>`) on the gathered text, with r476's target exclusion (ONE pattern, `interactive_builders._widget_links.exclude_target_pattern`: the first ON run added 73 Drive / Slides / picture pointers the gold never links) and a 3-character minimum link text (Word split PES1005's "Te Rā" link run so only "ā" carried it — the first build linked the macron alone, "Te R<a>ā</a>").

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 3222 / 3222 identical**; ON (final) 38 modules changed; every added `<a>` inside a `<p>` / `<li>` / an inline `<i>` / `<b>` (`_r477_on/`, the parent census). Precision against the gold BODY (`_s43_r8_linkprec.py`): 37 of the added URLs the gold body carries (ANZH104's Google Lens / Seek / AutoDraw, ANZH404's Te Ara Kotahitanga, AGH1009's news articles …), the rest public pages the writer linked the gold drops — NAMED overrides of **KB constraint 75** ("inline → anchor").
- Regeneration of the 39-module detector set + the 12-module spot-check (`_r477_regen.sh`, re-run with the final code): 0 truly stale, 12 / 12 byte-identical; `scoped_ship.sh` containment OK (38 ⊆ 39), its decomposition flagged ≥75 −1 → committed NAMED (`_fastloop_diff.py --accept-named "skeleton pages >=75%"`, the r470 / r475 precedent).

### 3. PROTECTED GATES

- Skeleton **55.2317 % → 55.2360 % @ 2491 (+0.0042pp)**, RAW 39.191 → 39.195 %; ≥50 1577; **≥75 276 → 275 — NAMED: HIS1008_5_0 75.9 → 74.9** (the writer's citation link "Garrow, David," → Wikipedia, which the gold drops); ≥90 25; 44 movers, 13 up (FRFUN06_6_0 +15.1, ANZH404_3_0 +13.0, OSBY401_1_0 +4.0, ANZH104_6_0 +2.2 …) / 31 down (the largest: HES1002_5_0 −5.8 — its list of health-resource links the gold leaves out; MXDI202_8_0 −4.1 — "Merino" / "fleece" → Wikipedia; PHE1007_10_0 −3.8) — every down page a writer link the gold drops; movers outside the affected set 0.
- compare_structure **exact 16758 → 16759** (matched 19531 → 19532), EXTRA 208, missing 903; body / clean / leak EXACT; every verifier RESULT line identical to r476; 17 selftests + the skeleton selftest green; the feature index green; the miner 197 CANDIDATE @ 2491.
- Plateau (§4): a KB-rule round; neither counts nor resets: **2 of 3** stands.

**Ledger:** scoped #3 since the r474 FULL · data `body_region.gathered_links` · env `GATHERLINKS_OFF` · code `MediaBuilder.gatherFollowing`, `ContentConverter.#gatheredLinks` / `#element` / `#calloutOpen` · tools `_r477_{regen,postship,commit_named,checksums}.sh`, `_r477_finalise.py`. **Follow-ups (recorded):** the shared weave matches a phrase anywhere in the line (no word boundary) — the 3-character floor contains it here; table-cell links (a precision question); the Bilingual audio players' missing `src` / `title`.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 477 (260620.41): KB c75 FOR GATHERED BODY TEXT (session 43 Round 9). MediaBuilder.gatherFollowing records the gathered "
                "items' links; #element's body default and the callout content weave them (public web targets, >= 3-character phrases). "
                "Env GATHERLINKS_OFF.\n"
                '\tstatic AppVersion = "260620.41";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 477 BASELINE (KB c75 for gathered body text — the "
                "writer's links in an activity's / alert's gathered paragraphs, `GATHERLINKS_OFF`; SCOPED, scoped #3 since the r474 FULL): "
                "SCAFFOLD mean 55.2360% / >=50% 1577 / >=75% 275 / >=90% 25 / RAW 39.195% @ 2491 pairs — +0.0042pp; ≥75 −1 NAMED "
                "(HIS1008_5_0 75.9 → 74.9, a citation link the gold drops); cs exact 16759 (+1); body / clean / leak EXACT.** Previous: "
                "**ROUND 476 BASELINE")
so = so.replace(a11, "| `GATHERLINKS_OFF` | 477 | **KB c75 FOR GATHERED BODY TEXT** (session 43 Round 9). Reverts `body_region.gathered_links`: "
                "the paragraphs gathered after a tag line (an activity's body, an alert's content) lose the writer's inline links again — 38 "
                "modules; byte-identical to r476. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.41` (round 477 — **KB c75 FOR GATHERED BODY TEXT**; `GATHERLINKS_OFF`; scoped #3 since the r474 FULL; "
                "38 modules; skeleton 55.2360 % @ 2491, ≥75 −1 NAMED; cs exact 16759).\n" + a14)
wr(PO, so); print("OG ok")
sk = sk.replace(k75, "triggers excluded by measurement — `outputs/_s43_r8_linkprec.py`). **r477 (session 43 Round 9): the GATHERED BODY half — "
                "an activity's / alert's gathered paragraphs weave the writer's public-web links (`body_region.gathered_links`, "
                "`GATHERLINKS_OFF`; 38 modules; ≥ 3-character phrases).** Remaining: table cells (a precision question). |")
wr(PK, sk); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r477.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            G[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.40"', '"260620.41"'); setv("round", "476", "477")
insert_before("_note_r476", '    "_note_r477": "Round 477 (session 43 Round 9, 2026-09-24) — KB c75 FOR GATHERED BODY TEXT (GATHERLINKS_OFF): 38 modules; SCAFFOLD '
              '55.2317 -> 55.2360 @ 2491 (+0.0042pp), RAW 39.191 -> 39.195; >=75 276 -> 275 NAMED (HIS1008_5_0 75.9 -> 74.9, the writer\'s '
              'citation link the gold drops); cs exact 16758 -> 16759; body / clean / leak EXACT; scoped #3 since the r474 FULL; committed NAMED.",')
setv("mean_scaffold_pct", "55.23", "55.24"); setv("pages_ge_75", "276", "275"); setv("raw_mean_pct", "39.19", "39.2")
insert_before("_note_r476_state", '    "_note_r477_state": "r477 (the gathered-text links): SCAFFOLD 55.2360 @ 2491, RAW 39.195; 44 movers (13 up / 31 down).",')
setv("exact_chain", "16758", "16759")
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r477-finalise.bak")
i = find("- **ROUND 477 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈22:50 real clock, session 43 Round 9 — r477 (KB c75 for gathered body text) SHIPPED and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r477** (260620.41); **LAST FULL = r474**; ledger **scoped #3** (5 of "
        "headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **Before r477: no round in flight**"); prior = L[k]; del L[k]
k = find("- Before it: **r475**"); r475 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r476**"); L[k] = L[k].replace("- LAST SHIPPED: **r476**", "- Before it: **r476**", 1)
L.insert(k, "- LAST SHIPPED: **r477** (build 260620.41, 24 Sept ≈22:50 real clock, session 43 Round 9 — KB c75 FOR GATHERED BODY TEXT, "
         "`GATHERLINKS_OFF`; SCOPED, **scoped #3 since the r474 FULL**, committed NAMED; **skeleton 55.2317 → 55.2360 % @ 2491 (+0.0042pp)**, "
         "≥50 1577, **≥75 275 (−1 NAMED: HIS1008_5_0)**, ≥90 25, RAW 39.195 %; cs exact 16759; body / clean / leak EXACT; "
         "`gate_baseline.json` at r477; the miner 197 CANDIDATE).")
k = find("- Before them: **r474**")
L[k] = L[k].replace("- Before them: **r474**", "- Before them: **r475** (260620.39, KB c75 the menu's inline links — verbatim → "
                    "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r475 (verbatim, s43 r477)'), **r474**", 1)
k = find("- Plateau window (§4): **2 of 3** — r476")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r476", "- Plateau window (§4): **2 of 3** — r477 a KB-rule round (+0.0042pp; "
                    "neither counts nor resets); r476", 1)
k = find("- Standing facts: AppVersion 260620.40")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.40 (r476", "- Standing facts: AppVersion 260620.41 (r477 KB c75 for gathered body text "
                    "— session 43 Round 9, 24 Sept); before it 260620.40 (r476", 1)
k = find("## Round log")
L.insert(k + 1, "- s43-r9 (engine r477, build 260620.41, 24 Sept 22:10 → ≈22:50 real clock) · KB c75 FOR GATHERED BODY TEXT: an activity's / "
         "alert's gathered paragraphs keep the writer's links (target exclusion + a 3-character floor after a mid-word 'ā' anchor) · SHIPPED "
         "scoped #3, committed NAMED · 38 modules · skeleton +0.0042pp, ≥75 −1 NAMED, cs exact +1 · plateau 2 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r477** (260620.41, "
        "KB c75 for gathered body text); LAST FULL = **r474**; ledger scoped #3; plateau **2 of 3**; 2,491 pairs; census 552 / 545 / 2,679. "
        "Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("## Session 43 — Round 9 PICK (engine r477)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 43 — Round 9 PICK (engine r477) — KB c75 FOR GATHERED BODY TEXT — SHIPPED; the PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md 'Session 43 — Round 9 PICK (engine r477) + what shipped'; the one-line summary is the s43-r9 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r475 (verbatim, s43 r477)\n\n" + r475 + "\n"
    "\n## Session 43 — Round 9 PICK (engine r477) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r477, 260620.41):** `body_region.gathered_links` (env `GATHERLINKS_OFF`; exclude_targets, min_text_chars 3) — "
    "gatherFollowing records the gathered links; #element's body default and the callout content weave them. Probe OFF 3222 identical; "
    "38 modules; scoped_ship containment OK, ≥75 −1 → committed NAMED; skeleton +0.0042pp; cs exact +1.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
