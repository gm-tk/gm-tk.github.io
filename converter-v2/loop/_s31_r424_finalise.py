#!/usr/bin/env python3
"""r424 finalise (CLAUDE.md §12, an output-inert recognition round): changelog entry, Config.js bump, CLAUDE.md §11 / §14,
gate_baseline.json build / round + note. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-21 (round 424, build 260619.95) — THE ACTIVITY-TABLE WRITERS TEMPLATE IS RECOGNISED: the twelve XOTP reader modules stop being "unrecognised documents" and are refused BY NAME until their adapter ships (the spec's Round 1 — recognition, output-inert; the autonomous loop's session 31 Round 2; no regeneration, the corpus byte-identical 2559 / 2559)

### 1. WHAT CHANGED

**The gap.** The 12 XOTP documents (XOTPB08–13, XOTPG01, XOTPG03–06, XOTPO01 — the 19 Sept intake's largest no-build group) carry NO square-bracket red tags: their structure lives in one two-column table whose header row reads `Section heading | Text/Activity` (`00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md` — "a Writers Template in a different dialect"). `LooksLikeWritersTemplate` (a content-start red span) said no, so `ModuleResolver.PrepareRun` returned `no-wt` and the batch harness reported the misleading *"no Writers Template (no content opener found)"* — the same words a random non-template docx gets. Session 28 Task 2 (r409) had already corrected the parsed-text tab's message; the converter side was untouched.

**The fix (DATA OVER CODE; the spec's §3.1 / §6 round 1).** `Input_Doc_Rules.input_shapes.activity_table {enabled, env ACTTABLE_OFF, header [section heading, text/activity], scan_rows 3, label, action, adapter {enabled false, env ACTTABLEADAPT_OFF}}` + `DocxExtractor.IsActivityTableDoc(blocks)` (any table whose first `scan_rows` rows hold a row whose first two non-empty cells fold to the header pair — the table opens with a merged title row, so the header is the second row; the same test as `OutputFormatter.ACTIVITY_TABLE_NOTICE`). In `PrepareRun`, when the standard chain found no WT, such a document IS the WT: the module code resolves from its filename as usual, and — with `adapter.enabled` false — the run returns the data-driven `unsupported` refusal (`{label, action}`, the route the MTK / TRR pathway already uses), which `batch_convert.cjs` reports as *"refused by design: Activity-table Writers Template …"* and the App renders in the conversion summary, with a run note naming the module. Nothing is converted until the adapter round flips `adapter.enabled`.

### 2. PROOF

- MEASURED (`outputs/_s31_r424_attable.cjs` over all 762 corpus docx): the header pair exists in EXACTLY the 12 XOTP Writers Templates and in no other document — the detector is exact. `PrepareRun` on the 12: `ok=false reason=unsupported`, module code resolved (XOTPB08 … XOTPO01), the label set; PMT101 (r423) still `ok=true`; TRR115 unchanged (`no-wt`, pre-existing).
- The detector is consulted only when no upload is a Writers Template by the standard chain, which never happens on a built module, so the change is output-inert by construction: `_s31_r424_probe_run.sh ON` = **2559 / 2559 identical, changed 0** over all 495 Claude-dir modules; no regeneration (none needed — no page changed); `_verify_entry_parity.cjs --selftest` PASS (the refusal lives inside the one shared prep choke point); 17 selftests GREEN (50 / 0); `_check_index_sync.cjs` OK.

### 3. PROTECTED GATES — every gate as at r423 (the corpus byte-identical; `_s31_r423_gates.log` stands)

- Skeleton (PRIMARY) SCAFFOLD **54.1703 % @ 2353 pairs**, ≥50 1442 / ≥75 238 / ≥90 20, RAW 38.193 %; compare_structure 14255 / 186 / 689 / 23; body 55 / 5 / 190 / 248; clean 2508 / 2552; leak 73 / 44; tags 9557 / 9557; every verifier EXACT — unchanged.
- Plateau (§4): no engine round moved a metric (output-inert by design); the window stays at 0 of 3 (r423 a recognition round behind it).
- Recorded: the spec's Round 2 (the adapter, text only — the section-heading lexicon in data, the synthetic tag stream, the per-variant page boundary, the `CS:` build-vs-note split; the 7 modules whose payload is fully in the text first) is the next round; Round 3 (the reader book — the carousel images and the picture / sentence matching) NEEDS CHRIS: all twelve have no Media List, and XOTPB08's matching sentences exist only as a pasted picture.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-21 (round 423")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.94";'; assert s.count(old) == 1
note = ("\t// ROUND 424 (260619.95): THE ACTIVITY-TABLE WRITERS TEMPLATE IS RECOGNISED — the 12 XOTP reader documents (no red tags; the structure in a "
        "'Section heading | Text/Activity' table) are detected by DocxExtractor.IsActivityTableDoc (Input_Doc_Rules.input_shapes.activity_table, env "
        "ACTTABLE_OFF); ModuleResolver.PrepareRun takes such a document as the WT, resolves its module code and — until input_shapes.activity_table.adapter "
        "is enabled — returns the data-driven 'unsupported' refusal by name ('refused by design: Activity-table Writers Template …') instead of the "
        "misleading 'no Writers Template'. The loop's session 31 Round 2 (the spec's Round 1: recognition, output-inert). Measured over all 762 docx: "
        "exactly the 12; the built corpus byte-identical 2559 / 2559; no regeneration; every gate as at r423.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.95";'))

p = PF + "CLAUDE.md"; s = rd(p)
old11 = "| `ROWMARKER_OFF` | 423 | **A PAGE-BOUNDARY MARKER TYPED AS A TABLE ROW IS A PARAGRAPH"; assert s.count(old11) == 1
row11 = ("| `ACTTABLE_OFF` | 424 | **THE ACTIVITY-TABLE WRITERS TEMPLATE IS RECOGNISED — the twelve XOTP reader documents are refused BY NAME until their "
         "adapter ships** (the autonomous loop's session 31 Round 2; the spec `00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md` §6 round 1: "
         "recognition, output-inert). XOTPB08–13 / XOTPG01 / XOTPG03–06 / XOTPO01 carry no square-bracket red tags — the structure is one two-column "
         "table whose header row is `Section heading | Text/Activity` (the table opens with a merged title row, so the header is the second row). "
         "`Input_Doc_Rules.input_shapes.activity_table {enabled, env, header, scan_rows, label, action, adapter {enabled false, env ACTTABLEADAPT_OFF}}` + "
         "`DocxExtractor.IsActivityTableDoc`; in `ModuleResolver.PrepareRun`, when the standard chain finds no WT, such a document IS the WT: the module "
         "code resolves from the filename and the run returns the data-driven `unsupported` refusal (`{label, action}` — the MTK / TRR route) that "
         "`batch_convert.cjs` reports as *refused by design* and the App renders in the summary. Measured over all 762 docx: exactly the 12; consulted "
         "only when no upload is a WT, so the built corpus is byte-identical (2559 / 2559). OFF = the pre-424 `no-wt` path. NEXT: the adapter round "
         "(`adapter.enabled: true` — the section-heading lexicon, the synthetic tag stream, the per-variant page boundary, the `CS:` build-vs-note "
         "split); the reader book (carousel images, picture / sentence matching, acks credits) NEEDS CHRIS — no XOTP module has a Media List. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.94` (round 423 — **a page-boundary marker typed as a table row"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.95` (round 424 — **the activity-table Writers Template is recognised: the twelve XOTP reader documents are refused BY NAME "
       "until their adapter ships** — `Input_Doc_Rules.input_shapes.activity_table`, env `ACTTABLE_OFF`; `DocxExtractor.IsActivityTableDoc` + the "
       "`PrepareRun` named refusal; the autonomous loop's session 31 Round 2, the spec's Round 1 (recognition, output-inert); measured over all 762 docx: "
       "exactly the 12; the built corpus byte-identical 2559 / 2559; no regeneration; **every gate as at r423** — SCAFFOLD 54.1703% / >=50% 1442 / "
       ">=75% 238 / >=90% 20 / RAW 38.193% @ 2353 pairs; 17 selftests GREEN). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.94"', '"260619.95"'); setv("round", 423, 424)
a = '    "_note_r423": "Round 423 (session 31 Round 1)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r424": "Round 424 (session 31 Round 2): the activity-table Writers Template recognised — the 12 XOTP documents refused BY NAME (Input_Doc_Rules.input_shapes.activity_table, env ACTTABLE_OFF) until the adapter ships. Output-inert: no regeneration, the corpus byte-identical 2559 / 2559; every r423 number stands.",\n' + a)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r424 finalise: changelog + Config.js 260619.95 + CLAUDE.md §11/§14 + gate_baseline.json done")
