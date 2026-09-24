#!/usr/bin/env python3
"""ROUND 474 finalise (session 43 Round 5 — KB c52: every iStock image carries its title as alt, WIDGETALT_OFF; THE FULL BACKSTOP) —
BUILD_CHANGELOG.md (prepend), Config.js AppVersion 260620.37 -> 260620.38, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (build /
round / note), KB_AMALGAMATION_STATUS.md row 52, LOOP_STATE.md (marker cleared, Position — LAST FULL = r474, ledger 0 — plateau, round
log, next-session line; the PICK → archive). Line edits only; .bak kept; nothing written until every anchor is found. WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 474," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.37";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 473 BASELINE"; a11 = "| `MODALBTNTEXT_OFF` | 473 |"; a14 = "- **Build:** `260620.37` (round 473"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
k52 = '| 52 | Alt text: concise, never "stock photo"; iStock API name preferred | CL-0001 | every image | **LIVE** (r240 `img_alt_lazy`; 0 Claude alts contain "stock photo", gold 52 pages do) |'
assert sk.count(k52) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 474 IN FLIGHT — NOT PROVEN**", "- **Before r474: no round in flight**", "- LAST SHIPPED: **r473**", "- Before it: **r472**",
          "- Plateau window (§4): **2 of 3** — r473", "- Standing facts: AppVersion 260620.37", "## Round log", "**Next session starts with:**",
          "## Session 43 — Round 5 PICK (engine r474)", "- Before them: **r470**"):
    find(p)

entry = """## 2026-09-24 (round 474, build 260620.38) — KB CONSTRAINT 52: EVERY iSTOCK IMAGE CARRIES ITS TITLE AS ALT TEXT — the widget-internal images round 242 left corpus-inert (flip cards, carousels, speech bubbles, accordions, activity boxes) now take the same title as the content images; recoverable iStock images with an empty alt 1,642 → 13 — with THE FULL-REGENERATION BACKSTOP (ledger scoped #6 → 0)

### 1. WHAT CHANGED

**The find** (session 43 Round 5 — `outputs/_s43_r5_alt.py`: every `<img>` on every Claude page by container, iStock id, whether that id's URL — with its slug — is in the module's Writers Template, alt filled / empty): **1,642 iStock images whose title is RECOVERABLE shipped `alt=""`** — flipCard 493 / 74 modules, carousel 427 / 70, activity 243 / 28, speechBubble 236 / 45, accordion 101 / 29, body 85 / 21, tab-pane 26, clickDrop 21, TKmodal 8 — while the standalone content images already carried it (round 240's `MediaBuilder.FinishImg`, which only the content-image path calls; round 242 took the widget-internal images under the rule but recorded them corpus-INERT, the `#assetImage` seam seeing only the filename). The gold fills 0.88 of its iStock alts (14,056 / 15,919). **KB constraint 52 (universal):** "For an iStock image, the preferred alt value is the iStock/Getty API image name — the descriptive title carried in the supplied iStock acknowledgements file or recoverable from the iStock link"; `KB_AMALGAMATION_STATUS.md` row 52 read LIVE on its negative half only.

**The fix** (`MediaBuilder.FillWidgetAlts` + `#istockAltMap`, called LAST in `PageAssembler` after the MathML pass; data `Emit_Templates.elements.image_attrs.widget_alt_postpass` {enabled, env}; env **`WIDGETALT_OFF`**, byte-identical OFF): every `<img … alt="">` whose tag names `iStock-<id>` — the Mode-P placeholder, the commented-out reference, a Mode-D image — takes round 240's title for that id: the VERIFIED `*_istock-acks.txt` title, else the Title-Cased slug of the id's URL anywhere in the module (the Media List items, the Writers Template blocks). No URL and no verified title → the alt stays empty (never invent a description); a non-iStock image is never touched; "stock photo" is stripped (c52's negative half — 0 alts carry it). `FinishImg` itself is unchanged.

### 2. PROOF

- In-memory A/B over all 545 modules (`outputs/_s42_probe_run.sh r474`): **OFF 3222 / 3222 identical; ON 324 pages / 170 modules changed.**
- **THE FULL REGENERATION** (the ledger backstop, due within two scoped ships — `_r474_fullship_par.sh`, 4 workers, 6 min 45 s): `_stalecheck.sh` 0 stale; `_content_manifest.py fresh --affected` (the 170) → **the 373 other modules byte-identical to the manifest**; the changed set = exactly the probe's 170.
- **Attribute-only, proven page by page:** the 170 modules' pages snapshotted before the regeneration; of 886 pages, 562 identical and **324 changed — every one identical once alt values are blanked** (0 non-alt differences).
- The alt census after (`_r474_alt_after.log`): recoverable iStock images **filled 1,963 → 3,592, empty 1,642 → 13** (links whose slug the `istock_slug_from_url` pattern does not parse); 3 more filled from a Media-List-only link; `stock photo` in any alt: 0.

### 3. PROTECTED GATES — EXACT (attributes are invisible to every structural gate)

- Skeleton **55.2315 % @ 2491 EXACT** (0 movers), ≥50 1577, ≥75 276, ≥90 25, RAW 39.194 %; compare_structure 16758 / 208 / 903; body 238; clean 2587 / 2633; leak 75 / 46 — `_gatecheck.py cs bc` then `skeleton defect` on the full 0-stale corpus: **every row HELD** (its first run printed a CACHED skeleton row, 54.94 — the §6 trap; the fresh run is 55.23 HELD); every verifier RESULT line identical to r473; 17 selftests + the skeleton selftest green; the feature index green; the miner 197 CANDIDATE @ 2491.
- **Ledger:** `_ship_ledger.py record-full --round 474` — **LAST FULL = r474, scoped #0** (8 of headroom); the fast-loop baseline re-snapshotted; the content manifest snapshotted (2679 pages / 543 modules).
- Plateau (§4): a KB-rule round that is skeleton-blind by design (an attribute) — neither counts nor resets: **2 of 3** stands.

**Ledger:** FULL (backstop) · data `elements.image_attrs.widget_alt_postpass` · env `WIDGETALT_OFF` · code `MediaBuilder.FillWidgetAlts` / `#istockAltMap`, `PageAssembler` (the call) · tools `outputs/_s43_r5_alt.py`, `_r474_{fullship_par,postship,checksums}.sh`, `_r474_finalise.py`. **Follow-ups (recorded):** a picture cell whose link the engine lifted out of the cell keeps no iStock id at all (XMES201 / XMES202's `flipCard-image` placeholders — the id would have to be read from the cell's link record); non-iStock images (2,442 body / 1,129 activity …) have no title source by design.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 474 (260620.38): KB c52 — EVERY iSTOCK IMAGE CARRIES ITS TITLE AS ALT TEXT (session 43 Round 5; the FULL backstop). "
                "MediaBuilder.FillWidgetAlts, last in PageAssembler: an <img alt=\"\"> naming iStock-<id> takes the verified acks title, else the "
                "module's URL-slug title. Env WIDGETALT_OFF.\n"
                '\tstatic AppVersion = "260620.38";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 474 BASELINE (KB c52 — every iStock image carries its "
                "title as alt text, `WIDGETALT_OFF`; THE FULL BACKSTOP — ledger scoped #6 → 0): SCAFFOLD mean 55.2315% / >=50% 1577 / >=75% "
                "276 / >=90% 25 / RAW 39.194% @ 2491 pairs — EXACT (324 pages / 170 modules changed, alt attributes only, proven page by "
                "page); cs / body / clean / leak EXACT; recoverable iStock alts empty 1,642 → 13.** Previous: **ROUND 473 BASELINE")
so = so.replace(a11, "| `WIDGETALT_OFF` | 474 | **KB c52 — EVERY iSTOCK IMAGE CARRIES ITS TITLE AS ALT TEXT** (session 43 Round 5; shipped with "
                "the FULL backstop). Reverts `elements.image_attrs.widget_alt_postpass`: the widget-internal iStock images (flip cards, "
                "carousels, speech bubbles, accordions, activity boxes …) ship `alt=\"\"` again — 1,629 images / 170 modules; byte-identical to "
                "r473. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.38` (round 474 — **KB c52: EVERY iSTOCK IMAGE CARRIES ITS TITLE AS ALT TEXT**; `WIDGETALT_OFF`; "
                "**LAST FULL** — the ledger backstop regenerated all 545, 373 modules byte-identical, 324 pages / 170 modules changed in alt "
                "attributes only; skeleton 55.2315 % @ 2491 EXACT; ledger scoped #0).\n" + a14)
wr(PO, so); print("OG ok")
sk = sk.replace(k52, '| 52 | Alt text: concise, never "stock photo"; iStock API name preferred | CL-0001 | every image | **LIVE — both halves '
                'since r474 (24 Sept 2026, session 43 Round 5)**: the widget-internal images round 242 left corpus-inert now take the verified '
                'acks / URL-slug title too (`MediaBuilder.FillWidgetAlts`, `WIDGETALT_OFF`) — recoverable iStock images with an empty alt '
                '1,642 → 13, filled 1,963 → 3,592; was LIVE on the negative half only (r240 `img_alt_lazy`; 0 Claude alts contain "stock '
                'photo", gold 52 pages do) |')
wr(PK, sk); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r474.bak")
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
setv("build", '"260620.37"', '"260620.38"'); setv("round", "473", "474")
insert_before("_note_r473", '    "_note_r474": "Round 474 (session 43 Round 5, 2026-09-24) — KB c52: EVERY iSTOCK IMAGE CARRIES ITS TITLE AS ALT TEXT (WIDGETALT_OFF) '
              '+ THE FULL BACKSTOP (ledger scoped #6 -> 0): all 545 regenerated, 373 modules byte-identical, 324 pages / 170 modules changed in alt '
              'attributes only (proven page by page); every gate EXACT — SCAFFOLD 55.2315 @ 2491, cs 16758 / 208 / 903, body 238, clean 2587 / '
              '2633, leak 75 / 46; recoverable iStock alts empty 1,642 -> 13.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r474-finalise.bak")
i = find("- **ROUND 474 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈20:50 real clock, session 43 Round 5 — r474 (KB c52, every iStock alt) SHIPPED with the FULL "
        "backstop and committed; the in-flight marker is cleared). LAST SHIPPED **r474** (260620.38); **LAST FULL = r474**; ledger **scoped #0** "
        "(8 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **Before r474: no round in flight**"); prior = L[k]; del L[k]
k = find("- Before it: **r472**"); r472 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r473**"); L[k] = L[k].replace("- LAST SHIPPED: **r473**", "- Before it: **r473**", 1)
L.insert(k, "- LAST SHIPPED: **r474** (build 260620.38, 24 Sept ≈20:50 real clock, session 43 Round 5 — KB c52: EVERY iSTOCK IMAGE CARRIES ITS "
         "TITLE AS ALT TEXT, `WIDGETALT_OFF`; **THE FULL BACKSTOP** — all 545 regenerated, 373 modules byte-identical, 324 pages / 170 "
         "modules changed in alt attributes only (proven page by page); **every gate EXACT: skeleton 55.2315 % @ 2491**, ≥50 1577, ≥75 276, "
         "≥90 25, RAW 39.194 %; cs 16758 / 208 / 903; body 238; clean 2587 / 2633; leak 75 / 46; recoverable iStock alts empty 1,642 → 13; "
         "ledger record-full, scoped #0; `gate_baseline.json` at r474; the miner 197 CANDIDATE @ 2491).")
k = find("- Before them: **r470**")
L[k] = L[k].replace("- Before them: **r470**", "- Before them: **r472** (260620.36, the flip-card text guard — verbatim → LOOP_STATE_ARCHIVE.md "
                    "'Position — LAST SHIPPED r472 (verbatim, s43 r474)'), **r470**", 1)
k = find("- Plateau window (§4): **2 of 3** — r473")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r473", "- Plateau window (§4): **2 of 3** — r474 a KB-rule round, skeleton-blind "
                    "by design (an attribute; EXACT): neither counts nor resets; r473", 1)
k = find("- Standing facts: AppVersion 260620.37")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.37 (r473", "- Standing facts: AppVersion 260620.38 (r474 KB c52 every iStock alt + "
                    "the FULL backstop — session 43 Round 5, 24 Sept); before it 260620.37 (r473", 1)
k = find("## Round log")
L.insert(k + 1, "- s43-r5 (engine r474, build 260620.38, 24 Sept ≈20:10 → 20:50 real clock) · KB c52: EVERY iSTOCK IMAGE CARRIES ITS TITLE AS "
         "ALT TEXT (the widget-internal images r242 left corpus-inert) · SHIPPED with the FULL backstop (LAST FULL = r474, scoped #0) · 324 "
         "pages / 170 modules, alt only; recoverable empty 1,642 → 13 · every gate EXACT · plateau 2 of 3 (neither). The PICK pass before it: "
         "PES1 / XDLS9 scoped miners, the AGH red journal-instruction box and the XDLS dropbox dialect — recorded below floor.")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r474** (260620.38, "
        "KB c52 every iStock alt); LAST FULL = **r474**; ledger scoped #0; plateau **2 of 3**; 2,491 pairs; census 552 / 545 / 2,679. Ride-along "
        "patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("## Session 43 — Round 5 PICK (engine r474)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 43 — Round 5 PICK (engine r474) — KB c52: EVERY iSTOCK IMAGE CARRIES ITS TITLE AS ALT TEXT — SHIPPED (the FULL backstop); "
         "the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 43 — Round 5 PICK (engine r474) + what shipped'; the one-line "
         "summary is the s43-r5 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r472 (verbatim, s43 r474)\n\n" + r472 + "\n"
    "\n## Session 43 — Round 5 PICK (engine r474) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r474, 260620.38):** `MediaBuilder.FillWidgetAlts` (data `elements.image_attrs.widget_alt_postpass`, env "
    "`WIDGETALT_OFF`), last in PageAssembler. Probe OFF 3222 identical / ON 324 pages / 170 modules; the FULL regeneration (6 min 45 s): "
    "373 modules byte-identical, the 324 pages differ in alt values only (snapshot proof); every gate EXACT; recoverable iStock alts empty "
    "1,642 → 13; ledger record-full (scoped #0).\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
