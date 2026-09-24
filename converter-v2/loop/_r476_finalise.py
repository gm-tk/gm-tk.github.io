#!/usr/bin/env python3
"""ROUND 476 finalise (session 43 Round 8 — KB c75 for built widgets: the writer's links in a widget's prose, WIDGETLINKS_OFF) —
BUILD_CHANGELOG.md (prepend), Config.js AppVersion 260620.39 -> 260620.40, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (build / round /
note / skeleton), KB_AMALGAMATION_STATUS.md row 75, LOOP_STATE.md (marker cleared, Position, plateau, round log, next-session line; the
PICK → archive). Line edits only; .bak kept; nothing written until every anchor is found. WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 476," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.39";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 475 BASELINE"; a11 = "| `MENULINKS_OFF` | 475 |"; a14 = "- **Build:** `260620.39` (round 475"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
k75 = "table cells (54 / 13) — `outputs/_s43_r7_inlinelinks.py`.** |"
assert sk.count(k75) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 476 IN FLIGHT — NOT PROVEN**", "- **Before r476: no round in flight**", "- LAST SHIPPED: **r475**", "- Before it: **r474**",
          "- Plateau window (§4): **2 of 3** — r475", "- Standing facts: AppVersion 260620.39", "## Round log", "**Next session starts with:**",
          "## Session 43 — Round 8 PICK (engine r476)", "- Before them: **r473**"):
    find(p)

entry = """## 2026-09-24 (round 476, build 260620.40) — KB CONSTRAINT 75 FOR BUILT WIDGETS: the writer's inline links in a widget's PROSE (panel bodies, the members' prose around it) keep their href — public web pages only; labels, faces and triggers stay link-free

### 1. WHAT CHANGED

**The find** (session 43 Round 8 — the r475 link census's next path; debug harness `outputs/_s43_r8_linkdbg.cjs`, which hooks `inlineMarkup` / `renderBlackText` on a phrase): AGH1009-7.0's "One example of precision agriculture is the Yara N-Sensor (__Yara N-Sensor – to variably apply nitrogen | Yara New Zealand__ [LINK: yara.co.nz/…])" is rendered by the carousel builder (`#carouselTableSlides` → the widget `renderBlock` callback) with NO links: `ContentConverter.#interactivePlaceholder` handed every widget builder `renderInline` / `renderBlock` callbacks that pass `[]` / `undefined` — the hover-definition stitch is deliberately off inside widgets, and the link weave had been switched off with it. So every writer inline link inside a built widget, or in the prose the round-353 members rule renders around it, lost its href.

**Measured three ways before shipping** (`_s42_probe_run.sh r476 ON / SAVE` + `outputs/_s43_r8_linkprec.py`: every href the ON pages add, by target kind × whether the gold BODY carries the URL): (1) all links, both callbacks — 715 added, **515 on picture / stock / developer-asset hosts the gold never links** (iStock picture labels, Drive audio folders): wrong; (2) those targets excluded (+ YouTube / Vimeo — the gold's YouTube hrefs are acknowledgement credits, its video titles unlinked) — 77 added, but `renderInline` put a link on ENGS101's modal TRIGGER BUTTON and on TEFUN03's flip-card FRONTS (a click would navigate instead of open / flip): wrong; (3) **`renderBlock` only — 49 links on 16 pages / 14 modules, every one inside a `<p>` / `<li>`**: the gold body carries 16 of the URLs (AGH1009's Yara, ANZH205's Te Papa activity book, TWHK902's Count Us In / #ActNow, OSAH501 / OSGM501's Netsafe mailto …); the other 33 are public resources the writer linked (ENGI201's School Journal list in its accordion panels) — NAMED overrides of **KB constraint 75** ("inline → anchor").

**The fix** (`ContentConverter.#widgetLinks` + the `renderBlock` callback in `#interactivePlaceholder`; data `Emit_Templates.interactive_builders._widget_links` {enabled, env, exclude_target_pattern}; env **`WIDGETLINKS_OFF`**, byte-identical OFF): the widget's block prose weaves the bundle's own hyperlinks (every opener / member item's and captured table's `block.links`) except picture / stock / Google-image / Drive / Docs / SharePoint / D2L / media-file / YouTube / Vimeo targets; `renderInline` (labels, faces, triggers) stays link-free; the hover stitch stays off.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 3222 / 3222 identical; ON 16 pages / 14 modules**; regeneration + the 12-module spot-check (`_r476_regen.sh`): 0 truly stale, 12 / 12 byte-identical; `scoped_ship.sh` **PASS** (14 ⊆ 14).

### 3. PROTECTED GATES

- Skeleton **55.2309 % → 55.2317 % @ 2491 (+0.0008pp)**, RAW 39.192 → 39.191 %; ≥50 1577, ≥75 276, ≥90 25; 1 mover: **AGH1009_7_0 +2.0** (the gold links the same sentence); movers outside the affected set 0; compare_structure / body / clean / leak and every verifier RESULT line IDENTICAL to r475; 17 selftests + the skeleton selftest green; the feature index green; the miner 197 CANDIDATE @ 2491.
- Plateau (§4): a KB-rule round predicted skeleton-neutral (inside a widget) — +0.0008pp; neither counts nor resets: **2 of 3** stands.

**Ledger:** scoped #2 since the r474 FULL · data `interactive_builders._widget_links` · env `WIDGETLINKS_OFF` · code `ContentConverter.#widgetLinks` / `#interactivePlaceholder` · tools `outputs/_s43_r8_{linkdbg.cjs,linkprec.py}`, `_r476_{regen,postship,checksums}.sh`, `_r476_finalise.py`. **Follow-ups (recorded):** the remaining link paths — activity boxes (ANZH104's Google Lens / Seek), alerts (OSBY401's Netsafe form), table cells (a precision question: 54 gold-kept vs 388 picture-source pointers), flat body sentences not in a widget bundle.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 476 (260620.40): KB c75 FOR BUILT WIDGETS (session 43 Round 8). ContentConverter.#interactivePlaceholder's renderBlock "
                "weaves the bundle's own public-web links into the widget's prose; renderInline (labels / faces / triggers) stays link-free. "
                "Env WIDGETLINKS_OFF.\n"
                '\tstatic AppVersion = "260620.40";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 476 BASELINE (KB c75 for built widgets — the writer's "
                "links in a widget's prose, `WIDGETLINKS_OFF`; SCOPED, scoped #2 since the r474 FULL): SCAFFOLD mean 55.2317% / >=50% 1577 / "
                ">=75% 276 / >=90% 25 / RAW 39.191% @ 2491 pairs — +0.0008pp (AGH1009_7_0 +2.0); cs / body / clean / leak EXACT; 49 links on "
                "16 pages / 14 modules, public web only.** Previous: **ROUND 475 BASELINE")
so = so.replace(a11, "| `WIDGETLINKS_OFF` | 476 | **KB c75 FOR BUILT WIDGETS** (session 43 Round 8). Reverts `interactive_builders._widget_links`: "
                "the prose a built widget renders (panel bodies, the members' prose around it) loses the writer's public-web links again — 49 "
                "links / 16 pages / 14 modules; byte-identical to r475. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.40` (round 476 — **KB c75 FOR BUILT WIDGETS: the writer's links in a widget's prose**; "
                "`WIDGETLINKS_OFF`; scoped #2 since the r474 FULL; 16 pages / 14 modules; skeleton 55.2317 % @ 2491).\n" + a14)
wr(PO, so); print("OG ok")
sk = sk.replace(k75, "table cells (54 / 13) — `outputs/_s43_r7_inlinelinks.py`. **r476 (session 43 Round 8): the WIDGET PROSE half — a built "
                "widget's panel bodies and the members' prose around it weave the bundle's public-web links (`interactive_builders._widget_links`, "
                "`WIDGETLINKS_OFF`; 49 links / 14 modules; picture / stock / developer-asset / video targets and the widget's labels / faces / "
                "triggers excluded by measurement — `outputs/_s43_r8_linkprec.py`).** |")
wr(PK, sk); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r476.bak")
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
setv("build", '"260620.39"', '"260620.40"'); setv("round", "475", "476")
insert_before("_note_r475", '    "_note_r476": "Round 476 (session 43 Round 8, 2026-09-24) — KB c75 FOR BUILT WIDGETS (WIDGETLINKS_OFF): 49 public-web links on 16 '
              'pages / 14 modules; SCAFFOLD 55.2309 -> 55.2317 @ 2491 (+0.0008pp, AGH1009_7_0 +2.0), RAW 39.192 -> 39.191; cs / body / clean / leak '
              'EXACT; scoped #2 since the r474 FULL.",')
insert_before("_note_r475_state", '    "_note_r476_state": "r476 (the widget-prose links): SCAFFOLD 55.2317 @ 2491, RAW 39.191; 1 mover (up).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r476-finalise.bak")
i = find("- **ROUND 476 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈22:10 real clock, session 43 Round 8 — r476 (KB c75 for built widgets) SHIPPED and committed; "
        "the in-flight marker is cleared). LAST SHIPPED **r476** (260620.40); **LAST FULL = r474**; ledger **scoped #2** (6 of headroom). "
        "Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **Before r476: no round in flight**"); prior = L[k]; del L[k]
k = find("- Before it: **r474**"); r474 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r475**"); L[k] = L[k].replace("- LAST SHIPPED: **r475**", "- Before it: **r475**", 1)
L.insert(k, "- LAST SHIPPED: **r476** (build 260620.40, 24 Sept ≈22:10 real clock, session 43 Round 8 — KB c75 FOR BUILT WIDGETS: the writer's "
         "links in a widget's prose, `WIDGETLINKS_OFF`; SCOPED, **scoped #2 since the r474 FULL**, scoped_ship PASS; **skeleton 55.2309 → "
         "55.2317 % @ 2491 (+0.0008pp, AGH1009_7_0 +2.0)**, ≥50 1577, ≥75 276, ≥90 25, RAW 39.191 %; cs / body / clean / leak EXACT; 49 "
         "links / 16 pages / 14 modules; `gate_baseline.json` at r476; the miner 197 CANDIDATE).")
k = find("- Before them: **r473**")
L[k] = L[k].replace("- Before them: **r473**", "- Before them: **r474** (260620.38, KB c52 every iStock alt + the FULL backstop — verbatim → "
                    "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r474 (verbatim, s43 r476)'), **r473**", 1)
k = find("- Plateau window (§4): **2 of 3** — r475")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r475", "- Plateau window (§4): **2 of 3** — r476 a KB-rule round (+0.0008pp; "
                    "neither counts nor resets); r475", 1)
k = find("- Standing facts: AppVersion 260620.39")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.39 (r475", "- Standing facts: AppVersion 260620.40 (r476 KB c75 for built widgets — "
                    "session 43 Round 8, 24 Sept); before it 260620.39 (r475", 1)
k = find("## Round log")
L.insert(k + 1, "- s43-r8 (engine r476, build 260620.40, 24 Sept ≈21:40 → 22:10 real clock) · KB c75 FOR BUILT WIDGETS: the writer's links in a "
         "widget's prose (measured three ways: all links → 515 asset pointers wrong; +labels → trigger buttons / card faces wrong; prose only "
         "→ 49 in <p> / <li>) · SHIPPED scoped #2 · 16 pages / 14 modules · skeleton +0.0008pp · plateau 2 of 3 (neither). The in-flight "
         "marker was raised late (after the first probe) — a §3 step-1 slip, recorded.")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r476** (260620.40, "
        "KB c75 for built widgets); LAST FULL = **r474**; ledger scoped #2; plateau **2 of 3**; 2,491 pairs; census 552 / 545 / 2,679. Ride-along "
        "patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("## Session 43 — Round 8 PICK (engine r476)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 43 — Round 8 PICK (engine r476) — KB c75 FOR BUILT WIDGETS — SHIPPED; the PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md 'Session 43 — Round 8 PICK (engine r476) + what shipped'; the one-line summary is the s43-r8 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r474 (verbatim, s43 r476)\n\n" + r474 + "\n"
    "\n## Session 43 — Round 8 PICK (engine r476) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r476, 260620.40):** `interactive_builders._widget_links` (env `WIDGETLINKS_OFF`) — the widget `renderBlock` weaves "
    "the bundle's public-web links; `renderInline` link-free. Probe OFF 3222 identical / ON 16 pages / 14 modules; scoped_ship PASS; skeleton "
    "+0.0008pp (AGH1009_7_0 +2.0); gates identical to r475.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
