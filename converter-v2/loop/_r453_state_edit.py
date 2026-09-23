#!/usr/bin/env python3
"""ROUND 453 finalise — LOOP_STATE.md edits (the r452 _state_edit pattern): clear the in-flight marker, the LAST SHIPPED row,
the plateau reset, the AppVersion history, Needs Chris #20, the stale r370 follow-up struck + the r453 residue follow-ups,
the round-log line, and MOVE the round's PICK section to LOOP_STATE_ARCHIVE.md (append-only) with a pointer line.
Writes LF UTF-8 via a temp file; a .pre-r453-finalise.bak is kept. Run under WSL."""
import io, os, shutil, re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(P, P + ".pre-r453-finalise.bak")
s = io.open(P, encoding="utf-8").read()
L = s.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx)
    return idx[0]

# 1. the in-flight bullet + the "Before r453" bullet -> one no-round-in-flight bullet
i = find("- **ROUND 453 IN FLIGHT — NOT PROVEN**")
j = find("- Before r453: **no round in flight**")
assert j == i + 1
L[i:j + 1] = ["- **No round in flight** (24 Sept 2026 ≈09:00, session 41 Round 1 — r453 SHIPPED and committed; the in-flight marker raised at the PICK is cleared). LAST SHIPPED **r453** (260620.24); **LAST FULL = the r452 state** (s40-r12, the ledger's backstop); ledger **scoped #1** since it (7 of headroom)."]

# 2. LAST SHIPPED r453; the r452 row becomes "Before it"
k = find("- LAST SHIPPED: **r452**")
L[k] = L[k].replace("- LAST SHIPPED: **r452**", "- Before it: **r452**", 1)
L.insert(k, "- LAST SHIPPED: **r453** (build 260620.24, 24 Sept ≈08:50, session 41 Round 1 — THE TABLE-CELL TITLE BAR OPENS THE DOCUMENT + THE MTK OVERVIEW-TABLE TABS, KB 07A §4 / 07D §19.1, `TABLETB_OFF` / `REOOVTABS_OFF`; 13 TRR modules, 59 files; SCOPED, **scoped #1 since the r452 FULL**; a POPULATION change **2477 → 2487 pairs** (+10 restored pages at a 39.4 % mean): **the pre-existing 2477 pairs 54.7484 → 54.7695 % (+0.0211pp; 12 up / 2 down — TRR107_1.0 / 2.0 NAMED, empty gold shells)**, the whole population **54.7079 %** (−0.0405pp), **≥50 1549** (+5), **≥75 265** (+5), ≥90 23, RAW 38.676 %; cs 15855 / 199 / 840 / 24 (matched 18463; missing +44 NAMED — all on +285 newly compared restored elements); body 59 / 5 / 176 / 238 (+1 NAMED — TRR108_0_0, the writer's own [Tabs: …] request); clean 2623 / 2668; leak 75 / 45; `gate_baseline.json` at r453; `outputs/_r453_sk_final.json`; the miner 195 CANDIDATE on 2487 pairs).")

# 3. plateau reset
k = find("- Plateau window (§4): **2 of 3**")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — ", "- Plateau window (§4): **0 of 3 — RESET by r453** (the PICK predicted a move; the pre-existing 2477 pairs +0.0211pp, above the 0.02pp line, with ≥50 +5 / ≥75 +5; the whole-population −0.0405pp is the +10 restored pages entering below the mean, §1e). Before it (the s40 window, 2 of 3): ", 1)

# 4. AppVersion history
k = find("- Standing facts: AppVersion 260620.23")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.23 (r452", "- Standing facts: AppVersion 260620.24 (r453 the table-cell title bar + the MTK overview-table tabs — session 41 Round 1, 24 Sept); before it 260620.23 (r452", 1)

# 5. Needs Chris #20
k = find("19. **24 Sept (session 40 Rounds 3 / 4 / 6)**")
L.insert(k + 1, "20. **24 Sept (session 41 Round 1, r453)** — **the MTK overview introduction's course-code heading: keep or drop?** The writer types `[H1] TRR900` (the course code) at the top of every TRR Module Introduction table; r453 renders it (the writer's own heading, the neutral default) as a reo/eng heading pair. The KB 07D §19.1 skeleton comment reads \"Typically: course code h1, Module Introduction h2, …\"; the gold DROPS it on 17 of 18 TRR overviews (TRR108 keeps it). A KB component-doc example the gold contradicts at 0.94 = §2 block (c) — so asked, not decided. Drop it = +2 skeleton lines matched on ≈ 13 overview pages. Holds up ≈ 13 pages.")

# 6. follow-ups: strike the stale r370 bold-header entry; add the r453 residue
k = find("- **(r370) The bold-header media table.**")
L[k] = "- ~~**(r370) The bold-header media table.**~~ → **ALREADY SHIPPED at r372** (`media_table.strip_markers`, `MLMARKERS_OFF` — `MediaListParser.#cleanCell` strips the `*` markers; noticed stale in s41-r1)."
k = find("## Follow-up candidates surfaced by Round 1")
L.insert(k + 1, "- **(r453) The TRR family's LESSON pages are the family's remaining loss.** With the overview restored, TRR1 lesson pages still score 15–35 % (TRR116 1.0–9.0 11–25 %, TRR103 1.0–3.0 26–29 %, TRR304 2.0 / 3.0 17 / 9.5): the bilingual activity tables render through the r135 keystone sections / `bilingualRows`, and the restored TRR304 lesson alone matched 148 elements with 28 missing containers. Measure the gold's TRR lesson skeleton per activity (the `Activity NX:` table → `div.activity` + h3 + reo/eng pairs + hand-off) against Claude's before any round; 55 pages / 12 modules. **(r453) TRR107's gold lesson pages 1.0–4.0 are EMPTY shells** (header + empty `col-md-8`) — a human outlier, never chase. **(r453) TRR112 / TRR113's gold overviews carry Strand / Dispositions panes their WTs lack** (no source) and TRR103 / TRR106 golds put Critical Point in a 5th pane after Information — both below floor, KB-over-gold.")

# 7. round-log line (top of the Round log)
k = find("## Round log")
L.insert(k + 1, "- s41-r1 (engine r453, build 260620.24, 24 Sept 07:40 → ≈09:00) · THE TABLE-CELL TITLE BAR OPENS THE DOCUMENT + THE MTK OVERVIEW-TABLE TABS (KB 07A §4; the loss ledger's lowest large family TRR1 38.3 % + the recognition lane — TRR116's WT 138 blocks, 63 reached the converter) · `TABLETB_OFF` / `REOOVTABS_OFF`, 13 modules · SHIPPED · pairs 2477 → 2487; pre-existing +0.0211pp, whole −0.0405pp (population), ≥50 +5, ≥75 +5, cs exact +198 · scoped #1 · plateau RESET.")

# 8. move the PICK section to the archive
k = find("## Session 41 — Round 1 PICK (engine r453)")
e = k + 1
while e < len(L) and not L[e].startswith("## "): e += 1
block = L[k:e]
title = "Session 41 — Round 1 PICK (engine r453) + what shipped"
L[k:e] = ["## Session 41 — Round 1 (engine r453, build 260620.24) — THE TABLE-CELL TITLE BAR OPENS THE DOCUMENT + THE MTK OVERVIEW-TABLE TABS — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md '" + title + "'; the one-line summary is the s41-r1 Round-log line below.", ""]
shipped = ["", "- **What shipped (r453, 260620.24):** the opener (`DocxExtractor.TrimFrontMatter`, `Input_Doc_Rules.content_start.table_title_bar_opener`, `TABLETB_OFF`) + the menu (`ContentConverter.#partitionItems` capture, `MenuBuilder.reoOverviewTableRole` / `#reoOverviewTabs` on the r212 `reo_tabs` shell, `Emit_Templates.elements.dual_language.overview_table_tabs`, `REOOVTABS_OFF`) + the course-code introduction's header-less unfold (`intro_match` → `_reoModuleContent`). In-round repairs: (1) the opener alone put the overview tables in `#body` (pre-score −0.179pp) → the KB 07A §4 tabs composer; (2) TRR304's untagged 'Ngā Whenu … / Strands Dispositions' label row → `untagged_roles`; (3) the introduction shipped as a raw `bilingual-unbuilt` dump with literal [H1] / [Body] tags → the header-less unfold, scanning past TRR103 / 106's paragraph [H1]. Proof: OFF 3208 / 3208; ON = the 13; scoped regen of the 20 Bilingual + 12 spot-check; disk = probe 81 / 81; containment 13 ⊆ 20; §1e split `outputs/_r453_popsplit.log`; committed `_fastloop_diff --accept-named` (three movers). Gates: see the changelog entry and the Position row."]
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## " + title + "\n\n" + "\n".join(block[1:]) + "\n".join(shipped) + "\n")
out = "\n".join(L)
tmp = P + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, P)
print("LOOP_STATE.md", len(s.encode("utf-8")), "->", os.path.getsize(P))
