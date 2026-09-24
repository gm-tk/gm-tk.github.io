#!/usr/bin/env python3
"""ROUND 486 finalise (session 45 Round 1 — KB 01F the writer's quote is p.quoteText + p.quoteAck, QUOTEFORM_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 486," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.49";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 485 BASELINE"; a11 = "| `TITLELANGSPLIT_OFF` | 485 |"; a14 = "- **Build:** `260620.49` (round 485"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
kD = "| — | c92 language fonts (7 pages), c85 three-part title (5 modules)"; assert sk.count(kD) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 486 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈03:25, session 44 Round 11", "- LAST SHIPPED: **r485**",
          "- Before it: **r484**", "- Before them: **r483 → r467**", "- Plateau window (§4): **0 of 3** — r485", "- Standing facts: AppVersion **260620.49**",
          "## Round log", "**Next session starts with:**", "## Session 45 — Round 1 PICK (engine r486)",
          "- **(s44-r5 / r11 / r12) left after this session, each measured:**"):
    find(p)
entry = """## 2026-09-25 (round 486, build 260620.50) — KB 01F / 05D THE WRITER'S QUOTE IS `p.quoteText` + `p.quoteAck`: no wrapper div, the attribution its own paragraph, the quote box holding only the quote

### 1. WHAT CHANGED

**The find** (session 45 Round 1 — the loss ledger's HIS1 family, 77 pages at 49.8 %, re-read with the scoped miner view: `p.quoteText` / `p.quoteAck` MISSING 23 + 20 lines). KB-first: **KB 01F's normalised-tag table maps `quote` → `<p class="quoteText">"Quote"</p><p class="quoteAck">Attribution</p>`** and 05D "Quote Text" gives the same form — no wrapper. `KB_AMALGAMATION_STATUS.md` had no row for it. The gold agrees wherever it styles a tagged quote (290+ `p.quoteText` / 221 `p.quoteAck` on 125 pages, never a div). Claude shipped the flowing `<div class="quoteText">` box around the gathered `<p>`s, the attribution glued into the quote's own paragraph (`“Failure is success in progress.” Albert Einstein.` — EXBP901), and the strict gather's whole black run inside the box (SSCI104_4: the explanation and the question after the quote).

**The fix:** `ContentConverter.#quoteKbForm`, called at the end of `#calloutOpen`'s strict path when the callout def carries `kb_p_form`: no wrapper; every plain `<p>` of the box → `p.quoteText` (+ the tag's modifier classes); the attribution → its own `p.quoteAck` — the LAST paragraph's tail after the closing quote mark (`tail_after_quote_pattern`) or after a spaced en/em dash (`tail_after_dash_pattern`, head ≥ 3 words), ≤ 14 words, or a last paragraph that is itself an attribution line (a dash / `Source:` / `By Name` line, or a bare link). **The quote's own extent:** a box that opens with a self-contained quote (wholly quoted or wholly italic) ends at the first later paragraph that opens neither way — that paragraph is the `p.quoteAck` when it is an attribution line (PES1005_4's source link), and everything after it stays a plain `<p>` in the same column (SSCI104_4's explanation — the gold's own form); a box opening any other way (a poem's plain lines, ENGJ402; a quotation opened on one paragraph and closed on the next, ENGS101) keeps every paragraph. **Only a genuine quote tag takes the form** (`genuine_tag_pattern` on the tag's own bracket text: `quote` / `quotation` / `quotetext`, optionally `centered` / `highlighted` / `pull` / `block` before or `by <name>` after): the writer INSTRUCTIONS the lexicon matched on the word "quote" — ART1002's `[please create three tiles … match colours with quote above …]`, ENGC403's `[insert quote from …]` — and a box that opens with a bare link (the `[quote link] URL` instruction, HIS1005) keep the legacy box. Data `Emit_Templates.callouts.by_tag.quote.kb_p_form` {enabled, env, classes, the patterns, word caps, `quote_extent`, `ack_bare_link`}; env **`QUOTEFORM_OFF`**, byte-identical OFF.

**Not derivable, recorded:** the gold's UNTAGGED quotes (its larger `p.quoteText` population — 72 not in the WT at all, 52 on untagged lines …). A WT line that opens with a quotation mark is `p.quoteText` in the gold 41 / 399 = 0.10 corpus-wide (plain p 0.26, absent 0.21, li 0.11); only HIS reaches 0.68 (26 / 38) — a family-dialect candidate (`_s45_r1_quote2.py`).

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **19 pages / 16 modules** (ENGI102 ENGJ402 ENGJ403 ENGS101 ENGS301 EXBP901 OSAH401 OSAI301 OSAI401 OSAI501 PES1005 SSCI104 TEDC402 TWHA906 XDLS905 XDLS906). Regeneration + 12-module spot-check clean; content manifest 0 stale.
- `scoped_ship.sh`: every gate held or improved except **compare_structure missing container 872 → 878 (+6), committed NAMED** (`_fastloop_diff.py --accept-named`): decomposed BLOCK BY BLOCK against the OFF render (`_r486_csblocks.py`) — **no block left EXACT**; 6 EXTRA → exact, 4 newly matched → exact (the split attributions), and the +6 = 4 blocks ALREADY mismatched moving EXTRA → MISSING (SSCI104_4's quote + its two paragraphs, which the gold keeps inside the writer's preceding `[alert]` box; TWHA906's Mandela quote, which the gold sets in a whakatauki box) + 2 newly matched blocks inside that TWHA906 whakatauki box.

### 3. PROTECTED GATES

- Skeleton **55.3463 % → 55.3485 % @ 2491 (+0.0021pp)**, RAW 39.231 → 39.234 %; ≥50 1582 / ≥75 277 / ≥90 26 EXACT; 17 movers, **13 up / 4 down NAMED**, each with its position-free companion (`_r486_companion.py`): ENGJ402_3_0 58.9 → 56.4 (overlap +1 — the gold lays the sonnet out as plain lines in a carousel), SSCI104_4_0 54.2 → 52.0 (+1 — the gold's alert around the quote), OSAH401_2_0 63.4 → 62.0 (−1 — the gold's `<blockquote>`, a KB-over-gold override), XDLS905_7_0 62.9 → 61.7 (+1 — alignment); up: OSAI301 +2.8, ENGS301 +2.7, OSAI501 +2.1, OSAI401 +1.5, EXBP901 +1.0 …
- compare_structure exact **16691 → 16701 (+10)**, EXTRA **208 → 198 (−10)**, missing 872 → 878 (+6 NAMED, above), row-wrap 24; body 238 / clean 2587 / 2633 / leak 75 / 46 EXACT; tags 9557 / 9557; every verifier RESULT line ✓; selftests 50 green / 0 fail; the miner 195 CANDIDATE.
- Plateau (§4): a KB-rule round, +0.0021pp — neither counts nor resets; **0 of 3**.

**Ledger:** scoped #4 since the r482 FULL · data `callouts.by_tag.quote.kb_p_form` · env `QUOTEFORM_OFF` · code `ContentConverter.#quoteKbForm` · tools `_s45_r1_{quote,quote2,pick}.py`, `_r486_{companion,csblocks}.py`, `_r486_commit_named.sh`, `_s45_{regen,postship}.sh`, `_r486_finalise.py` · session 45 Round 1.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 486 (260620.50): KB 01F THE WRITER'S QUOTE IS p.quoteText + p.quoteAck (session 45 Round 1) — no wrapper div, the "
                "attribution its own paragraph, the box holding only the quote (ContentConverter.#quoteKbForm). Env QUOTEFORM_OFF.\n" + '\tstatic AppVersion = "260620.50";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 486 BASELINE (KB 01F the writer's quote is p.quoteText + "
                "p.quoteAck, `QUOTEFORM_OFF`; SCOPED, scoped #4 since the r482 FULL; committed NAMED — cs missing +6, a reclassification proven block "
                "by block): SCAFFOLD mean 55.3485% / >=50% 1582 / >=75% 277 / >=90% 26 / RAW 39.234% @ 2491 pairs — +0.0021pp (13 up / 4 down NAMED); "
                "cs exact 16701 / EXTRA 198 / missing 878; body / clean / leak EXACT.** Previous: **ROUND 485 BASELINE")
so = so.replace(a11, "| `QUOTEFORM_OFF` | 486 | **KB 01F THE WRITER'S QUOTE IS p.quoteText + p.quoteAck** (session 45 Round 1). Reverts "
                "`callouts.by_tag.quote.kb_p_form`: the tagged quote ships as the flowing `<div class=\"quoteText\">` box around plain `<p>`s again "
                "(the attribution glued into the quote's paragraph, the whole gathered run inside) — 16 modules / 19 pages; byte-identical to r485. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.50` (round 486 — **KB 01F the writer's quote is p.quoteText + p.quoteAck**; `QUOTEFORM_OFF`; scoped #4 since "
                "the r482 FULL; 16 modules; skeleton 55.3485 % @ 2491, +0.0021pp; cs exact +10 / EXTRA −10 / missing +6 NAMED).\n" + a14)
wr(PO, so); print("OG ok")
KL = sk.split("\n"); iD = [i for i, l in enumerate(KL) if l.startswith(kD)][0]
KL.insert(iD, "| ~~—~~ | 01F normalised-tag table + 05D \"Quote Text\" — the writer's `[quote]` → `<p class=\"quoteText\">` + `<p class=\"quoteAck\">`, "
          "no wrapper | **SHIPPED round 486 (2026-09-25, session 45 Round 1)** — `callouts.by_tag.quote.kb_p_form`, `QUOTEFORM_OFF`; 16 modules / 19 "
          "pages (Claude's 45 `div.quoteText` boxes on 25 pages → the KB form where the tag is a genuine quote; instruction-matched boxes left) | "
          "skeleton-visible (+0.0021pp, 13 up / 4 down NAMED); cs exact +10 / EXTRA −10 / missing +6 NAMED | the writer's quote tag + the "
          "attribution tail / line | the gold agrees (290+ p.quoteText, never a div); the UNTAGGED quote is not derivable (0.10; HIS 0.68 — a "
          "family-dialect candidate) |")
wr(PK, "\n".join(KL)); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r486.bak")
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
setv("build", '"260620.49"', '"260620.50"'); setv("round", "485", "486")
insert_before("_note_r485", '    "_note_r486": "Round 486 (session 45 Round 1, 2026-09-25) — KB 01F THE WRITER\'S QUOTE IS p.quoteText + p.quoteAck (QUOTEFORM_OFF): '
              '16 modules / 19 pages; SCAFFOLD 55.3463 -> 55.3485 @ 2491 (+0.0021pp, 13 up / 4 down NAMED); RAW 39.231 -> 39.234; buckets EXACT; cs '
              'exact 16691 -> 16701, EXTRA 208 -> 198, missing 872 -> 878 NAMED (a reclassification: 4 already-mismatched blocks EXTRA -> MISSING + 2 '
              'newly matched, 0 blocks left EXACT — outputs/_r486_csblocks.log); body / clean / leak EXACT; scoped #4 since the r482 FULL. Also: '
              'pages_ge_90 25 -> 26 corrects the r485 finalise, which left the >=90 bucket at its r484 value.",')
setv("pages_ge_90", "25", "26"); setv("exact_chain", "16691", "16701"); setv("claude_extra_container", "208", "198")
setv("claude_missing_container", "872", "878")
insert_before("_note_r485_state", '    "_note_r486_state": "r486 (the KB quote form): SCAFFOLD 55.3485 @ 2491, RAW 39.234; 17 movers (13 up / 4 down NAMED).",')
insert_before("_note_r453", '    "_note_r486": "r486: exact 16691 -> 16701 (+10), EXTRA 208 -> 198 (-10), missing 872 -> 878 (+6 NAMED), matched 19453 -> 19459 (+6) — '
              'block by block (outputs/_r486_csblocks.log): 6 EXTRA -> exact, 4 new -> exact, 4 EXTRA -> MISSING (SSCI104_4 x3 the gold\'s alert, '
              'TWHA906 x1 the gold\'s whakatauki), 2 new -> MISSING (TWHA906, whakatauki); 0 blocks left EXACT.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r486-finalise.bak")
i = find("- **ROUND 486 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈06:05, session 45 Round 1 — r486 (KB 01F the writer's quote is p.quoteText + p.quoteAck) SHIPPED "
        "and committed; the in-flight marker is cleared). LAST SHIPPED **r486** (260620.50); **LAST FULL = r482 (the s44 backstop)**; ledger **scoped "
        "#4** (4 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈03:25, session 44 Round 11"); prior = L[k]; del L[k]
k = find("- Before it: **r484**"); r484 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r485**"); L[k] = L[k].replace("- LAST SHIPPED: **r485**", "- Before it: **r485**", 1)
L.insert(k, "- LAST SHIPPED: **r486** (build 260620.50, 25 Sept ≈06:05, session 45 Round 1 — KB 01F THE WRITER'S QUOTE IS p.quoteText + p.quoteAck, "
         "`QUOTEFORM_OFF`; SCOPED, **scoped #4 since the r482 FULL backstop**, committed NAMED (cs missing +6 = a reclassification, 0 blocks left "
         "EXACT); **skeleton 55.3463 → 55.3485 % @ 2491 (+0.0021pp, 13 up / 4 down NAMED)**, ≥50 1582, ≥75 277, ≥90 26, RAW 39.234 %; cs exact "
         "16701 (+10) / EXTRA 198 (−10) / missing 878 (+6 NAMED); body / clean / leak EXACT; `gate_baseline.json` at r486; the miner 195 CANDIDATE).")
k = find("- Before them: **r483 → r467**")
L[k] = L[k].replace("- Before them: **r483 → r467** (260620.47 → 260620.34 — KB c38 autoCheck,",
                    "- Before them: **r484 → r467** (260620.48 → 260620.34 — KB c38 for the quiz types, KB c38 autoCheck,", 1)
k = find("- Plateau window (§4): **0 of 3** — r485")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r485", "- Plateau window (§4): **0 of 3** — r486 a KB-rule round (+0.0021pp; neither); r485", 1)
k = find("- Standing facts: AppVersion **260620.49**")
L[k] = L[k].replace("AppVersion **260620.49** (r485 the title-bar language split — session 44 Round 11, 25 Sept); the history 260620.48",
                    "AppVersion **260620.50** (r486 KB 01F the quote form — session 45 Round 1, 25 Sept); before it 260620.49 (r485 the title-bar "
                    "language split — session 44 Round 11, 25 Sept); the history 260620.48", 1)
assert "260620.50" in L[k]
k = find("- **(s44-r5 / r11 / r12) left after this session, each measured:**")
L.insert(k, "- **(s45-r1) the quote family after r486, each measured:** (a) **the HIS untagged quote** — a WT line opening with a quotation mark is "
         "`p.quoteText` in the HIS gold 26 / 38 = 0.68 (every other family ≤ 0.29; corpus 0.10) — a family-dialect candidate (§1d exception 1) with "
         "its `Source:` line as the `p.quoteAck` (HIS1002 / HIS1003 / HIS1004 — size the pages first, `_s45_r1_quote2.py`); (b) **the "
         "`[quote link] URL` instruction** (7 tags, HIS1005 / HIS1007): the gold links the preceding `Source:` line to the URL; Claude ships a "
         "`div.quoteText` holding the bare URL (HIS1005_1_0 ×2, _2_0 ×3 — the box also swallows the following journal task on _2_0); below floor; "
         "(c) SSCI104_4's quote the gold keeps inside the writer's preceding `[alert]` (the alert ends at the `[quote]` tag in Claude); (d) the "
         "lexicon matching the word \"quote\" inside writer INSTRUCTIONS (ART1002's tile request, ENGC403's `[insert quote from …]`, HIS1002's "
         "`[Kaitiakitanga]` in-text bracket) — each builds a stray quote box (r486 leaves them in the legacy form); 4 sites.")
k = find("## Round log")
L.insert(k + 1, "- s45-r1 (engine r486, build 260620.50, 25 Sept 05:20 → ≈06:05) · KB 01F THE WRITER'S QUOTE IS p.quoteText + p.quoteAck (found on "
         "the loss ledger's HIS1 lane; no wrapper, the attribution its own p, the box holding only the quote; instruction-matched boxes left) · "
         "SHIPPED scoped #4, committed NAMED (cs missing +6 = a reclassification) · 16 modules / 19 pages · skeleton +0.0021pp (13 up / 4 down "
         "NAMED) · cs exact +10 / EXTRA −10 · plateau 0 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r486** (260620.50, "
        "the KB quote form); LAST FULL = **r482** (the s44 backstop); ledger scoped #4; plateau **0 of 3**; 2,491 pairs; census 552 / 545 / 2,679. "
        "Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("## Session 45 — Round 1 PICK (engine r486)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 45 — Round 1 PICK (engine r486) — KB 01F THE WRITER'S QUOTE IS p.quoteText + p.quoteAck — SHIPPED; the PICK + what-shipped "
         "record is in LOOP_STATE_ARCHIVE.md 'Session 45 — Round 1 PICK (engine r486) + what shipped'; the one-line summary is the s45-r1 Round-log "
         "line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r484 (verbatim, s45 r486)\n\n" + r484 + "\n"
    "\n## Session 45 — Round 1 PICK (engine r486) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r486, 260620.50):** `callouts.by_tag.quote.kb_p_form` (env `QUOTEFORM_OFF`; genuine_tag_pattern, the two tail patterns, "
    "ack_line_pattern + ack_bare_link, quote_extent) — `ContentConverter.#quoteKbForm` at the end of `#calloutOpen`'s strict path. Probe OFF 0 "
    "changed; ON 19 pages / 16 modules; scoped_ship FAIL on cs missing +6 only → decomposed block by block (a reclassification, 0 blocks left "
    "EXACT) → committed NAMED (`_r486_commit_named.sh`); +0.0021pp, 13 up / 4 down NAMED; cs exact +10 / EXTRA −10.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
