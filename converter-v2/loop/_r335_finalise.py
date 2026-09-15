#!/usr/bin/env python3
"""ROUND 335 (loop session 6, finishing session 5's Round 6) — finalise: changelog, AppVersion (260619.05 → 260619.06),
CLAUDE.md §9/§11/§14, gate_baseline.json, KB status D-row, LOOP_STATE.md (what shipped + position + round log + header).
Idempotent. Every repo write goes through wr() with newline="" so LF stays LF (the r333 CRLF gotcha)."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

# ---- the numbers (filled from outputs/_r335_gates_s6.log / _r335_sk_full.log / _r335_fastloop_s6.log) ----
SK_B, SK_A, RAW_B, RAW_A = "51.060", "51.078", "35.243", "35.256"
GE50_B, GE50_A, GE75, GE90 = 1066, 1066, 200, 15
DELTA = "+0.018"          # e.g. "+0.02"
MOVED = "28 moved — 19 up / 9 down, every mover in the affected set, pp-sum +35.31; the 9 dips ≤ 0.33pp NAMED = the scorer's alignment artefact on pages whose gold box has no inner row > col-12 (OSBY501_5, OSSC501_5, OSSC301_3, OSAI201_3, OSOH501_5, OSSC401_4, ARFUN01_0, HPFUN401_0, ARFUN02_0 — the element sequence h3 → p → a → div.button is now the gold's)"          # e.g. "28 moved — 26 up / 2 down (dips named)"
PCT = "55.8"              # % of achievable, e.g. "55.8"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 335, build 260619.06) — THE `[Engagement quiz button]` IS THE KB'S EXTERNAL QUIZ LINK BUTTON (KB 01F `engagement_quiz_button` + constraint 65 / CL-0038; the autonomous loop's session-5 Round 6, BUILT + probe-proven there and SHIPPED OFF at Chris's stop, flipped ON and FINALISED in session 6; **SCOPED regeneration of the 28 affected modules; skeleton {DELTA}pp, every other gate EXACT; scoped ship #1 since the round-334 full-ship backstop**)

### 1. WHAT CHANGED, IN ONE LINE

**The writer's `[Engagement quiz button] <sharepoint quiz doc URL>` shipped `<div class="button engagementTrigger">…</div>` — a bare div carrying a class the gold has on 0 of 2,385 pages, no anchor, and a label that fell to the journal default (`Go to your journal` on 13 of 28) or to the quiz DOCUMENT'S FILENAME; it now ships the KB's external quiz link button `<a href="#" target="_blank"><div class="button">Go to quiz</div></a>` with ONE Designer/Developer To Do note carrying the writer's link, which is what the gold ships at every paired site (30/30).**

### 2. THE EVIDENCE (docx → human → Claude)

- **OSAI301 lesson 3** — WT `[Engagement quiz button] https://mytekuraschool.sharepoint.com/…` → gold `<a href="/d2l/common/dialogs/quickLink/quickLink.d2l?ou={{orgUnitId}}&type=quiz&rcode=TCS_Dev-74927" target="_blank"><div class="button">Go to quiz</div></a>` → Claude before: `<div class="button engagementTrigger">Go to your journal</div>` (the sharepoint link lost); after: the anchored `Go to quiz` button + the To Do note quoting the writer's link.
- **OSGM301** — the same shape; **OSSC301 / OSAH501** — the label had fallen to the quiz document's filename (`Online Safety Scams OSSC301 Quiz - Copy`, `Writers Template -OSAH501 …docx`); after: `Go to quiz`, the filename preserved in the note.
- **The KB:** 01F `engagement_quiz_button` → "External quiz link button" (the `button` form); constraint 65 / CL-0038 (round 232) fixed the quiz button's label `Go to quiz` and its blank publish-time href — the gold's D2L `rcode` is publish-time wiring (the r232 / CL-0044 class), never in a Writers Template.

### 3. THE MEASUREMENT (session 5, `outputs/_r335_probe.cjs` in four shards — `_r335_probe_off_0*.log` / `_r335_probe_on_0*.log`; `_r335_carriers.txt`)

- The tag lives in the OS family + ARFUN01/02 + HPFUN401: **28 pages / 28 modules, 28 buttons**. The gold ships `engagementTrigger` on **0** of 2,385 pages and the anchored `Go to quiz` form at every paired site: **25 in the OS golds, ARFUN01 4, HPFUN401 1**.
- In-memory over ALL 416 modules: **OFF (`ENGQUIZ_OFF=1`) = disk 2102/2102**; ON names **exactly 28 pages / 28 modules** and every differing line is the one button swap (28 legacy divs → 28 anchored buttons + 28 To Do notes, cv2-note, gate-neutral).

### 4. THE FIX — one data block `buttons["engagement quiz button"].kb_form` `{{ enabled, env: "ENGQUIZ_OFF", form: "<a href=\\"{{href}}\\" target=\\"_blank\\"><div class=\\"button\\">{{label}}</div></a>", href: "#", label: "Go to quiz", todo_note }}` (built in session 5, `enabled:false` at Chris's stop, `enabled:true` this round)

- At the `ContentConverter` button seam, right after the r329 trigger-marker test, an `engagement quiz button` item ships `kb_form.form` with the canonical `href` + `label` and ONE Designer/Developer To Do note (`todo_note`: "Wire this engagement quiz's D2L quicklink (the href is intentionally blank). Writer's quiz source: {{url}}{{text}}") carrying the writer's link and any other words of the bracket's tail; the legacy `engagementTrigger` div is the OFF form. Nothing else at the seam moves — `[trigger engagement]` markers (r329) and every other `[button]` route are untouched.

### 5. THE PROOF AND THE GATES

- Session 6 flipped the flag, regenerated the 28 modules (`outputs/_r335_batches_run.sh`, 5 batches, all rc 0; `_r335_regen_s6.log`), `_content_manifest.py fresh --affected` → **0 truly stale**, `diff` = **exactly the 28 pages, 0 added/removed** (the 385 untouched modules byte-identical to the r334 full-ship manifest).
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% ({DELTA}pp) / ≥50% {GE50_B} → {GE50_A} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%** (state `outputs/_r335_sk_final.json`, FRESH). {MOVED}.
- Every other gate EXACT (`_fastloop_diff.py` on the 28 PASS; full suite `_r335_gates_s6.log` line-for-line identical to r334 outside the skeleton block): cs exact 11375 / EXTRA 171 / missing 593 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · mtkQuiz shells defect 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN** (`_r335_selftests_s6.log`). **Ceiling:** SCAFFOLD {SK_A}% = **{PCT}% of achievable** (ceiling 91.6%).
- **Verifier:** `button engagementTrigger` divs corpus-wide 28 → 0; anchored `Go to quiz` buttons at the engagement sites 0 → 28, notes 28 (1:1).
- **A gotcha caught this round:** `outputs/_r335_affected.txt` was written on Windows with CRLF, so `xargs < file` handed `_fastloop_diff.py` codes ending in `\\r` — every module read as "not regenerated" and the baseline as "stale". The file is LF now; a code list a WSL tool consumes must be LF (`_content_manifest.py` strips whitespace and was never fooled).

### 6. NAMED, NOT CHASED

- The gold's populated D2L `rcode` quicklinks (publish-time wiring — the r232 / CL-0044 class); the 28 residual compound `[… engagement trigger]` brackets (r329 named); the `[engagement quiz button]` sites whose gold carries no button at all (none in the paired set).

**Ledger:** scoped ship #1 since the r334 full-ship backstop · data `buttons["engagement quiz button"].kb_form` · env `ENGQUIZ_OFF` · tools (session 5) `outputs/_r335_probe.cjs`, `_r335_affected.txt`, `_r335_carriers.txt`, `_r335_batches_plan.txt` / `_r335_batches_run.sh`; (session 6) `_r335_proof_s6.sh`, `_r335_finalise.py` · state `outputs/_r335_sk_final.json` (FRESH) · logs `_r335_regen_s6.log`, `_r335_fresh.log`, `_r335_fastloop_s6.log`, `_r335_gates_s6.log`, `_r335_sk_full.log`, `_r335_selftests_s6.log`, `_r335_fastloop_commit_s6.log`.

"""
if "round 335, build 260619.06" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.05";\n'
NEW = ('\t// ROUND 335 (2026-09-15, build 260619.06): the [Engagement quiz button] is the KB\'s external quiz link button\n'
       '\t// (01F engagement_quiz_button + constraint 65): the anchored "Go to quiz" form + one To Do note carrying the\n'
       '\t// writer\'s link replaces the bare engagementTrigger div; scoped regeneration of 28 modules; env ENGQUIZ_OFF.\n'
       '\tstatic AppVersion = "260619.06";\n')
if '"260619.06"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 334 BASELINE (the activity box's title heading is h3 — KB 01F; scoped 73 modules)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 335 BASELINE (the [Engagement quiz button] is the KB's external quiz link button — KB 01F + constraint 65; scoped 28 modules): SCAFFOLD mean {SK_A}% / >=50% {GE50_A} / >=75% {GE75} / >=90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r335_sk_final.json`, FRESH). r335 {DELTA} ({MOVED}); every other gate EXACT. Older r334 text: **ROUND 334 BASELINE (the activity box's title heading is h3 — KB 01F; scoped 73 modules)")
if "ROUND 335 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
# §11: replace the SHIPPED-OFF row written at Chris's stop with the shipped form
i = m.find("| `ENGQUIZ_OFF` | 335 |"); assert i > 0, "§11 row"
j = m.find("\n", i)
ROW = ("| `ENGQUIZ_OFF` | 335 | **THE `[Engagement quiz button]` IS THE KB'S EXTERNAL QUIZ LINK BUTTON** (KB 01F `engagement_quiz_button` + constraint 65 / CL-0038; built + probe-proven in the autonomous loop's session-5 Round 6, shipped OFF at Chris's stop, flipped ON + finalised in session 6; **SCOPED regeneration of the 28 affected modules; scoped ship #1 since the r334 full-ship backstop**). Reverts byte-for-byte to the legacy `<div class=\"button engagementTrigger\">` div. ON (default), `buttons[\"engagement quiz button\"].kb_form`: at the `ContentConverter` button seam, right after the r329 trigger-marker test, an `engagement quiz button` item ships `<a href=\"#\" target=\"_blank\"><div class=\"button\">Go to quiz</div></a>` + ONE Designer/Developer To Do note (cv2-note, gate-neutral) carrying the writer's link and any other words of the bracket's tail. MEASURED: the tag lives in the OS family + ARFUN01/02 + HPFUN401 — 28 pages / 28 modules; the gold ships `engagementTrigger` on 0 of 2,385 pages and the anchored `Go to quiz` at 30/30 paired sites (the D2L rcode is publish-time wiring). Legacy divs 28 → 0. " + f"Skeleton {DELTA}pp ({MOVED}); every other gate EXACT; 13 selftests GREEN. |")
if "SHIPPED OFF" in m[i:j]:
    m = m[:i] + ROW + m[j:]; print("§11 row rewritten")
B14 = (f"- **Build:** `260619.06` (round 335 — **the [Engagement quiz button] is the KB's external quiz link button** (KB 01F + constraint 65; the autonomous loop's session-5 Round 6, finalised in session 6; **SCOPED regeneration of 28 modules; scoped ship #1 since the r334 full-ship backstop**). **ROUND 335 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50_A} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r335_sk_final.json`, FRESH) = **{PCT}% of achievable** (ceiling 91.6%). Every other gate EXACT: cs exact **11375** / EXTRA **171** / missing **593** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **28 pages / 28 modules changed, 0 added/removed**; toggle `ENGQUIZ_OFF`; data `buttons[\"engagement quiz button\"].kb_form`. Legacy `engagementTrigger` divs 28 → 0. **Plateau window: r333 +0.066 · r334 +0.167 · r335 {DELTA}.**)\n")
if "- **Build:** `260619.06` (round 335" not in m:
    A = "- **Build:** `260619.05` (round 334 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.06"; d["_meta"]["round"] = 335; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50_A, "pages_ge_75": GE75})
d["_meta"]["_round335_note"] = f"Round 335 (the [Engagement quiz button] is the KB's external quiz link button — KB 01F + c65; scoped 28-module regeneration, scoped ship #1 since the r334 full backstop). Skeleton {SK_B}->{SK_A} ({DELTA}pp; {MOVED}; >=50 {GE50_B}->{GE50_A}, >=75 {GE75}, >=90 {GE90}); every other gate EXACT; 13 selftests GREEN."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
anchor = "| ~~—~~ | 01F \"Activities\" — `activity_heading`"
row = (f"| ~~—~~ | 01F \"Activities\" — `engagement_quiz_button` → the external quiz link button (`<a href target=_blank><div class=button>Go to quiz</div></a>`, constraint 65's blank publish-time href + label) | **SHIPPED round 335** (28 legacy `engagementTrigger` divs → 28 anchored `Go to quiz` buttons + 28 To Do notes; 28 pages / 28 modules) | 28 pages | {DELTA}pp | `ENGQUIZ_OFF` | CAPTURED-LIVE |\n")
if "`engagement_quiz_button` → the external quiz link button" not in k:
    assert k.count(anchor) == 1; k = k.replace(anchor, row + anchor, 1); wr(KB, k); print("KB status D-row")

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 6 · Round 1 = Session 5 · Round 6 (engine r335) — what shipped (the [Engagement quiz button] is the KB's external quiz link button)
- **Fix (built in session 5, flipped ON here):** `buttons["engagement quiz button"].kb_form` {{enabled, env ENGQUIZ_OFF, form `<a href="{{href}}"
  target="_blank"><div class="button">{{label}}</div></a>`, href "#", label "Go to quiz", todo_note}} at the ContentConverter button seam right
  after the r329 marker test: an `engagement quiz button` item ships the KB form + ONE Designer/Developer To Do note (cv2-note) carrying the
  writer's link and any tail words; the legacy `engagementTrigger` div is the OFF form.
- **Regeneration:** scoped — session 5's in-memory probe over ALL 416 modules: OFF = disk 2102/2102; ON = exactly 28 pages / 28 modules, every
  diff line the one button swap. Session 6: the 5 batches (`_r335_batches_run.sh`) all rc 0; `_content_manifest.py fresh` → 0 truly stale;
  `diff` = exactly the 28, 0 added/removed. Gotcha: `_r335_affected.txt` was CRLF (written on Windows) — `xargs` fed `_fastloop_diff.py`
  codes ending in `\\r` and every guard fired; converted to LF, re-run clean.
- **Gates:** skeleton {SK_B} → {SK_A} ({DELTA}pp; {MOVED}); ≥50 {GE50_B} → {GE50_A}; ≥75 {GE75}; ≥90 {GE90}; every other gate line-for-line
  EXACT with r334 (fastloop PASS, nothing to name; full suite `_r335_gates_s6.log`); 13 selftests GREEN. **{PCT}% of achievable.**
- **Verifier:** `button engagementTrigger` divs 28 → 0; anchored `Go to quiz` at the engagement sites 0 → 28 (+28 notes, 1:1).
  Ship ledger: scoped #1 since the r334 full-ship backstop. **Plateau window: r333 +0.066 · r334 +0.167 · r335 {DELTA}.**

""")
ANCHOR = "## Session 5 · Round 6 PICK (engine r335)"
if "(engine r335) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Session 5 Round 6 (engine r335 — the `[Engagement quiz button]` KB form, 01F + c65): BUILT + PROBE-PROVEN, **SHIPPED OFF** at Chris's stop ≈20:03 (data `kb_form.enabled: false`, 28 modules regenerated OFF, manifest IDENTICAL). To finish: flip `enabled: true`, regenerate `_r335_affected.txt` (28), gates, finalise (AppVersion 260619.06, changelog, §9/§11/§14, KB D-row, ledger scoped #1)."
NEW_P = f"- Session 5 Round 6 = Session 6 Round 1 (engine r335 — the `[Engagement quiz button]` KB form, 01F + c65): BUILT + PROBE-PROVEN in session 5, SHIPPED OFF at Chris's stop, **flipped ON + SHIPPED 2026-09-15 ≈21:2x (session 6)**. AppVersion 260619.06, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #1 since the r334 full backstop. Skeleton {DELTA}pp; every other gate EXACT."
if OLD_P in s: s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s5-r6 (engine r335) · the `[Engagement quiz button]` is the KB's external quiz link button"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i)
NEW_R = f"- s5-r6 / s6-r1 (engine r335) · the `[Engagement quiz button]` is the KB's external quiz link button (01F; c65 label `Go to quiz`, blank publish-time href, ONE To Do note with the writer's link) · BUILT + PROBE-PROVEN in session 5 (OFF = disk 2102/2102; ON = 28 pages / 28 modules), SHIPPED OFF at Chris's stop, **flipped ON + SHIPPED 2026-09-15 (session 6)** · scoped regeneration, 28 pages / 28 modules · scaffold {SK_B}→{SK_A} ({DELTA}; {MOVED}), ≥50 {GE50_B}→{GE50_A}, every other gate EXACT · engagementTrigger divs 28→0 · {PCT}% of achievable · scoped ship #1 since the r334 full · commit (see git log)"
s = s[:i] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
