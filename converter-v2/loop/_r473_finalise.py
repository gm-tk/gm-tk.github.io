#!/usr/bin/env python3
"""ROUND 473 finalise (session 43 Round 2 — the modal's single-link button never swallows the writer's words, MODALBTNTEXT_OFF) —
BUILD_CHANGELOG.md (prepend), Config.js AppVersion 260620.36 -> 260620.37, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json,
LOOP_STATE.md (marker cleared, Position, plateau, round log, next-session line; the PICK → archive). Line edits only; .bak kept;
nothing written until every anchor is found. Run under WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 473," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.36";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 472 BASELINE"; a11 = "| `FLIPTEXTGUARD_OFF` | 472 |"; a14 = "- **Build:** `260620.36` (round 472"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 473 IN FLIGHT — NOT PROVEN**", "- **Before r473: no round in flight**", "- LAST SHIPPED: **r472**", "- Before it: **r470**",
          "- Plateau window (§4): **2 of 3** — r472", "- Standing facts: AppVersion 260620.36", "## Round log", "**Next session starts with:**",
          "## Session 43 — Round 2 PICK (engine r473)", "- Before them: **r467**"):
    find(p)

entry = """## 2026-09-24 (round 473, build 260620.37) — THE MODAL'S SINGLE-LINK BUTTON NEVER SWALLOWS THE WRITER'S WORDS: a content-carrying modal is not a link button, whatever its content — 18 modals stop shipping as one bare button with their text gone

### 1. WHAT CHANGED

**The find** (session 43 Round 2 — r472's widget text-loss census made media-aware, `outputs/_s43_widgetloss2.cjs`: every lost PART tagged media label vs learner text): after r472 the largest learner-text loss by widget type is the carousel (79 bundles, mostly video TITLES on a tag line whose URL is on the next line — a media-label follow-up) and then **modal — 41 bundles / 30 pages / 19 modules, 124 parts**. Triangulated: ONE mechanism. The round-73 single-document button (`#modalDocButton`: exactly one URL in the bundle → `<a href=URL><div class="button">LABEL</div></a>`) fired on CONTENT-CARRYING modals whose one URL was a stock photo, a source link or a website and dropped every other member — and the r356 members rule counts a member consumed once the builder READ it, so nothing came back: **PWY1009-2.2** (modal 6 "Get independent advice" → a button to the handshake photo; its body, its list and all of modal 7 lost), **TEFUN03-0.0** ("AI is a tool" → a button to the stock photo; sixteen paragraphs lost), **HIS1005-3.0** (Vincent O'Malley's source text + two questions → a "Go to journal" button to the source URL), **MXFL401-4.0** (the KiwiSaver modal → a "What's the catch?" button to IRD), **BLL240-0.0** (×3 — five activity modals → one button to a memory-game site), CEDR203 (18 parts), CEDK102, ENGJ101 ×2, CEDT102 (9 parts), HPRE301, MXEO301, OSSM401, OSOH101, BLL210. Round 311 had fenced this path for a HEADING member only ("a content-carrying bundle is not a link button").

**The fix** (`InteractiveBuilder.#modalDocButton`; data `interactive_builders.modal.doc_button_text_fence` {enabled, env, min_words 3, media_tag_pattern}; env **`MODALBTNTEXT_OFF`**, byte-identical OFF): the bundle's LEARNER text is every black / tag-line part that is not a `[image]` / `[video]` / `[audio]` / `[embed]` / `[button]` / `[link]` label, not a writer instruction and not the invocation tag's own line (the round-354 tag-words note already surfaces that as the red Writers Note — OSOH201-3.0). A bundle carrying any learner part of ≥ 3 words beyond the button's own label falls through to the round-280 trigger + TKmodal set composer, which builds the content modal or keeps the honest hand-off box. A genuine document button is untouched (BLLR201-5.0 "Narrative organiser modelled example" + its `[button] Go to journal`).

### 2. PROOF

- In-memory A/B over all 545 modules (`outputs/_s42_probe_run.sh r473`): **OFF 3222 / 3222 identical; ON 25 pages / 14 modules changed**, all inside the modal family.
- The media-aware loss census, r472 → r473 (`_r473_wl_compare_m2.log`): **4 lossy modals → full builds** (TEFUN03-0.0 #19 — 17 parts, PWY1009-2.2 #12 — 8, CEDT102-0.0 #8 — 9, OSOH101-2.0 #8), **14 lossy modals → the honest hand-off box** (every word kept for the developer: BLL240 ×3, CEDR203 ×2, ENGJ101 ×2, CEDK102, HIS1005, HPRE301, MXEO301, MXFL401, OSSM401, BLL210 — mixed-widget bundles and long free sections the set composer rightly refuses); **0 loss-free builds changed**; every other widget type byte-identical.
- **OPERATING_GUIDE §0a whole-type rule:** the modal family = every module carrying a modal bundle (367 bundles / **110 modules**, `outputs/_r473_family.txt`) regenerated (`_r473_regen.sh`) + the 12-module spot-check: 0 truly stale, spot-check 12 / 12 byte-identical; `scoped_ship.sh` **PASS** (14 changed ⊆ 110 affected).
- The modal verifier over the WHOLE family, OFF → ON (`_r473_vm_{OFF,ON}_0*.log`): **defect 0 → 0** on every shard, every RESULT ✓; triggers 17 / 168 / 95 / 57 → 21 / 174 / 95 / 57 (the four new content sets).

### 3. PROTECTED GATES

- Skeleton **55.2277 % → 55.2315 % @ 2491 (+0.0039pp)**, **≥50 1576 → 1577**, ≥75 276, ≥90 25, RAW 39.200 → 39.194 %; 15 movers, **12 up / 3 down**: OSSM401_3_0 +4.5, ENGJ101_2_0 +1.8, ENGJ101_1_0 +1.4, CEDT102_0_0 +1.3, MXEO301_7_0 +1.0, MXFL401_4_0 +0.7, OSOH101_2_0 +0.6, CEDR203_0_0 +0.4, HPRE301_10_0 +0.4, HIS1005_3_0 +0.2, CEDK102 / BLL210 +0.0; **NAMED (KB constraint 1 — the writer's words restored):** PWY1009_2_2_0 −2.4 (modals 6 / 7 now carry their text; the gold omits both modals), BLL240_0_0 −0.3, TEFUN03_0_0 −0.1; movers outside the affected set 0.
- compare_structure **exact 16757 → 16758**, EXTRA 208, missing 903, row-wrap 24; body 61 / 5 / 175 / 238; clean 2587 / 2633; leak 75 / 46 — held or improved; every verifier RESULT line identical to r472; 17 selftests + the skeleton selftest green; the feature index green; the miner 197 CANDIDATE @ 2491.
- Plateau (§4): a widget-correctness round, skeleton-blind by design — neither counts nor resets: **2 of 3** stands.

**Ledger:** scoped #6 since the r460 FULL · data `interactive_builders.modal.doc_button_text_fence` · env `MODALBTNTEXT_OFF` · code `InteractiveBuilder.#modalDocButton` · tools `outputs/_s43_widgetloss2.cjs`, `_s43_wl2_{run.sh,report.py,compare.py}`, `_s43_wdump.cjs`, `_r473_{measure,regen,postship,checksums}.sh`, `_r473_finalise.py`. **Follow-ups (recorded):** the carousel's video titles on the tag line (79 bundles — media labels unless the gold shows them); accordion 23 / clickDrop 13 / speechBubble 13 learner-part losses, each its own measure.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 473 (260620.37): THE MODAL'S SINGLE-LINK BUTTON NEVER SWALLOWS THE WRITER'S WORDS (session 43 Round 2). "
                "interactive_builders.modal.doc_button_text_fence — a content-carrying modal falls through to the round-280 set composer "
                "(or its box) instead of shipping as one bare button. Env MODALBTNTEXT_OFF.\n"
                '\tstatic AppVersion = "260620.37";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 473 BASELINE (the modal's single-link button never "
                "swallows the writer's words, `MODALBTNTEXT_OFF`; SCOPED, scoped #6 since the r460 FULL — the 110-module modal family "
                "regenerated): SCAFFOLD mean 55.2315% / >=50% 1577 / >=75% 276 / >=90% 25 / RAW 39.194% @ 2491 pairs — +0.0039pp, 12 up / 3 "
                "down (PWY1009_2_2_0 −2.4, BLL240_0_0 −0.3, TEFUN03_0_0 −0.1 NAMED: the writer's words restored); cs exact 16758 (+1); body / "
                "clean / leak EXACT; modal verifier defect 0.** Previous: **ROUND 472 BASELINE")
so = so.replace(a11, "| `MODALBTNTEXT_OFF` | 473 | **THE MODAL'S SINGLE-LINK BUTTON NEVER SWALLOWS THE WRITER'S WORDS** (session 43 Round 2). "
                "Reverts `interactive_builders.modal.doc_button_text_fence`: a content-carrying modal whose one URL is a picture, a source or "
                "a website ships as one bare button again (18 modals / 14 modules — PWY1009-2.2, TEFUN03-0.0, HIS1005-3.0, MXFL401-4.0, "
                "BLL240-0.0 …); byte-identical to r472. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.37` (round 473 — **THE MODAL'S SINGLE-LINK BUTTON NEVER SWALLOWS THE WRITER'S WORDS** (a "
                "content-carrying modal is not a link button); `MODALBTNTEXT_OFF`; scoped #6 since the r460 FULL; the 110-module modal family "
                "regenerated, 25 pages / 14 modules changed; skeleton 55.2315 % @ 2491).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r473.bak")
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
setv("build", '"260620.36"', '"260620.37"'); setv("round", "472", "473")
insert_before("_note_r472", '    "_note_r473": "Round 473 (session 43 Round 2, 2026-09-24) — THE MODAL\'S SINGLE-LINK BUTTON NEVER SWALLOWS THE WRITER\'S WORDS '
              '(MODALBTNTEXT_OFF): the 110-module modal family regenerated, 25 pages / 14 modules changed; SCAFFOLD 55.2277 -> 55.2315 @ 2491 '
              '(+0.0039pp, 12 up / 3 down NAMED: PWY1009_2_2_0 -2.4, BLL240_0_0 -0.3, TEFUN03_0_0 -0.1 — the writer\'s words restored), >=50 '
              '1576 -> 1577, RAW 39.200 -> 39.194; cs exact 16757 -> 16758; body / clean / leak EXACT; modal verifier defect 0; scoped #6 since '
              'the r460 FULL.",')
setv("pages_ge_50", "1576", "1577"); setv("raw_mean_pct", "39.2", "39.19")
insert_before("_note_r472_state", '    "_note_r473_state": "r473 (the modal text fence): SCAFFOLD 55.2315 @ 2491, RAW 39.194; 15 movers (12 up / 3 down).",')
setv("exact_chain", "16757", "16758")
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r473-finalise.bak")
i = find("- **ROUND 473 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈19:58, session 43 Round 2 — r473 (the modal text fence) SHIPPED and committed; the "
        "in-flight marker is cleared). LAST SHIPPED **r473** (260620.37); **LAST FULL = r460**; ledger **scoped #6** since it (2 of headroom). "
        "Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **Before r473: no round in flight**"); prior = L[k]; del L[k]
k = find("- Before it: **r470**"); r470 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r472**"); L[k] = L[k].replace("- LAST SHIPPED: **r472**", "- Before it: **r472**", 1)
L.insert(k, "- LAST SHIPPED: **r473** (build 260620.37, 24 Sept ≈19:58, session 43 Round 2 — THE MODAL'S SINGLE-LINK BUTTON NEVER SWALLOWS "
         "THE WRITER'S WORDS, `MODALBTNTEXT_OFF`: a content-carrying modal falls through to the round-280 set composer or its box; SCOPED, "
         "**scoped #6 since the r460 FULL** (the 110-module modal family regenerated), scoped_ship PASS; **skeleton 55.2277 → 55.2315 % @ "
         "2491 (+0.0039pp, 12 up / 3 down NAMED)**, ≥50 1577, ≥75 276, ≥90 25, RAW 39.194 %; cs exact 16758; body / clean / leak EXACT; "
         "4 lossy modals → full builds, 14 → the box, 0 loss-free changed; modal verifier defect 0; `gate_baseline.json` at r473; the "
         "miner 197 CANDIDATE).")
k = find("- Before them: **r467**")
L[k] = L[k].replace("- Before them: **r467**", "- Before them: **r470** (260620.35, TRR115 converts — verbatim → LOOP_STATE_ARCHIVE.md "
                    "'Position — LAST SHIPPED r470 (verbatim, s43 r473)'), **r467**", 1)
k = find("- Plateau window (§4): **2 of 3** — r472")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r472", "- Plateau window (§4): **2 of 3** — r473 a widget-correctness round "
                    "(skeleton-blind by design, +0.0039pp; neither counts nor resets); r472", 1)
k = find("- Standing facts: AppVersion 260620.36")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.36 (r472", "- Standing facts: AppVersion 260620.37 (r473 the modal text fence — "
                    "session 43 Round 2, 24 Sept); before it 260620.36 (r472", 1)
k = find("## Round log")
L.insert(k + 1, "- s43-r2 (engine r473, build 260620.37, 24 Sept 19:25 → ≈19:58) · THE MODAL'S SINGLE-LINK BUTTON NEVER SWALLOWS THE WRITER'S "
         "WORDS (the media-aware loss census: modal 41 lossy bundles, one mechanism — the r73 single-URL button) · SHIPPED scoped #6 (the "
         "110-module modal family regenerated; 25 pages / 14 modules changed) · 4 lossy → full, 14 → box · skeleton +0.0039pp (12 up / 3 "
         "down NAMED) · plateau 2 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r473** (260620.37, "
        "the modal text fence); LAST FULL = **r460**; ledger scoped #6 (a FULL backstop due within 2 more scoped ships); plateau **2 of 3**; "
        "2,491 pairs; census 552 / 545 / 2,679. Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / "
        "`_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("## Session 43 — Round 2 PICK (engine r473)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 43 — Round 2 PICK (engine r473) — THE MODAL'S SINGLE-LINK BUTTON NEVER SWALLOWS THE WRITER'S WORDS — SHIPPED; the PICK + "
         "what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 43 — Round 2 PICK (engine r473) + what shipped'; the one-line summary is "
         "the s43-r2 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r470 (verbatim, s43 r473)\n\n" + r470 + "\n"
    "\n## Session 43 — Round 2 PICK (engine r473) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r473, 260620.37):** `interactive_builders.modal.doc_button_text_fence` (env `MODALBTNTEXT_OFF`) — learner text beyond "
    "the label (not a media / button / link label, not an instruction, not the invocation line) sends the bundle to the round-280 set "
    "composer. Probe OFF 3222 identical / ON 25 pages / 14 modules; the 110-module family regenerated; scoped_ship PASS; 4 lossy → full, "
    "14 → box, 0 loss-free changed; skeleton +0.0039pp (12 up / 3 down NAMED: PWY1009_2_2_0 −2.4 — the gold omits modals 6 / 7); cs "
    "exact +1; modal verifier defect 0.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
