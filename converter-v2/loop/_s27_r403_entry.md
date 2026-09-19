## 2026-09-19 (round 403, build 260619.74) — AN `[embed]` OF AN EXTERNAL WEB PAGE IS THE KB'S externalButton, NEVER A BARE IFRAME: the `[embed link]` / `[link to PDF of: …]` / `[Embed audio]` route emits the r338 external-destination button for a non-internal host (the autonomous loop's session 27 Round 8; a SCOPED regeneration of the 53 changed modules, the probe proving the other 363 byte-identical — scoped ship #7 since the r396 full; THE FULL BACKSTOP IS DUE AT THE NEXT SHIP)

### 1. WHAT CHANGED

**The class.** The session's position-free label census (`_s27_r3_labelcensus.out`) lists `div.ratio.ratio-16x9` — the `[embed]` route's wrapper for a non-video URL (`elements.embeds.iframe`) — as a label the gold ships **0** times against Claude's 133 (77 pages / 58 modules). Measured on the paired pages (`outputs/_s27_r8_bareratio.py`, 129 sites): the gold iframes **none** of them — it drops the resource on 91 (kindergartenworksheets 18, twinkl 11, tahurangi 10, SharePoint / Google 20 — worksheet, PDF and slide pages the developer re-sourced as a downloaded PDF or omitted) and LINKS it on 38 (24 `div.button` / `externalButton` — csfieldguide, scratch, padlet, tuigarden, codeavengers, natlib, nzhistory; 14 plain `<a>`, the BLL parents' worksheet links); Fundamentals / Technology button 0.77, Leaving to Learn button 0.67. Every URL the gold keeps is a link; a third-party page in an iframe is also the form most sites refuse to render (the r126 note).

**The fix (DATA OVER CODE, one env `EMBEDBTN_OFF`).** `Emit_Templates.elements.embeds.external_button {enabled, env, _doc}`: in `ContentConverter`'s `[embed]` route, after the video-host and story-carousel branches, a URL whose host is not on the r338 `buttons.external_destination.internal_hosts` list (Google Docs / Drive / SharePoint — an embed that genuinely frames; the gold drops those 20 unknowably) emits that rule's form `<a href="{url}" target="_blank"><div class="externalButton">Go to website</div></a>` (KB 05D + constraint 75's default label) instead of the bare iframe. OFF = the iframe.

### 2. HOW IT WAS FOUND — and what was measured and declined first

Round 8 opened on the r6 census's largest remaining Claude-side class — "211 synthetic boxes around a hand-off widget on Claude-more pages" — and measured it to a decline: `_s27_r8_mergebox.py` over every heading-less single-widget Claude box on the paired lesson pages (387) finds the gold shipping a box with the SAME number on 241 = 0.62 (the r217 rule is right), merging the widget into the preceding box on 31 = 0.08, and no box for the previous number on 61 — no merge class. The label census's Claude-only wrapper was the next derivable line.

### 3. AUTHORITY (LOOP §1b)

KB 05D "Buttons" Internal / External + constraint 75 (the external destination is `externalButton`, default label "Go to website") — the r338 rule, extended from the `[button]` seam to the `[embed]` seam; the gold's own kept form 38 / 38.

### 4. PROOF

- `_s27_r403_probe.cjs` + `_s27_r403_probe_run.sh`: **OFF (`EMBEDBTN_OFF=1`) = disk 2109 / 2109**; ON = **66 pages / 53 modules changed, 2043 identical**; every changed site swaps the 3-line wrapper for the 1-line anchored button.
- `_s27_r403_pagescore.py` (the gate's own `match()` on the probe's ON pages BEFORE regenerating): 64 changed paired pages — **up 18 / down 2 / same 44; pp-sum +17.7**.
- Regeneration: `_s27_r403_batches.sh` (6 batches from `_batch_plan.py`, two at a time, all rc 0); `_content_manifest.py fresh --affected` → 0 truly stale, the 360 unaffected byte-identical; **probe ON == regenerated disk 344 / 344 pages**.
- `_s27_r403_skdelta.py`: 20 movers, 18 up / 2 down, **0 outside the affected set**.

### 5. PROTECTED GATES (all HELD-or-IMPROVED)

- **Skeleton (PRIMARY)**: SCAFFOLD **53.989 → 53.998 % (+0.0091pp)**; ≥50 **1174 → 1175** (TEFUN08_0_0 48.1 → 50.6); ≥75 **200**; ≥90 **18**; RAW **38.000 → 38.006 %**; 1956 pairs / 0 skipped (state `outputs/_s27_r403_sk_final.json`). The 2 dips, named: **XDLS903_7_0 −8.7** — the gold ships this very site as `<a href="pdf/…kindness-bingo…pdf" target="_blank"><div class="externalButton">Kindness bingo</div></a>` (the new form is the gold's own; the page's four YouTube `iframe` lines had been coincidentally aligned with the removed bare iframe — the scorer's alignment artefact, position-free overlap up), **MXDI202_8_0 −0.7** (the same class). The gains: MXFU201_2_0 +5.5, ANZH303_1_0 +3.3, TEFUN08_0_0 +2.5, XDLS902_5_0 +2.1, MXDI201_2_0 +1.9, ENGI202_4_0 +1.5, XDLS908_3_0 +1.5, MXDB302_4_0 +1.4 …
- **compare_structure** exact 11798 / EXTRA 172 / MISSING 626 — **EXACT**; **body_compare** 42 / 4 / 173 / 218 EXACT; structural-defect **clean 2079 / 2102, leak 26 / 23** EXACT; tags 9557 / 9557; every widget verifier RESULT identical to r402; 15 selftests + the feature-index selftest GREEN (46 PASS / GREEN lines).
- Ship ledger: **scoped #7 since the r396 full (1 of headroom) — the next ship is the FULL regeneration backstop**; content manifest + fast-loop baselines re-snapshotted; feature index GREEN.
- Plateau: ≥50 +1 moved a protected bucket — the window RESETS (0 of 3), the r346 precedent.
- DIFF MINER re-mined on the r403 corpus: 169 CANDIDATE rows — one gone (`activity EXTRA div.col-12 › div.TKmodal`, 20 pages / 17 modules — an alignment-shadow row), one new at the floor (`body SUBSTITUTED div.col-12.col-md-8: div.alert → div.activity.clickDropContent.dropbox[number=*]`, 20 pages / 4 modules — the XDLS tile-panel alignment, an artefact to measure before taking).

### 6. RECORDED, NOT TAKEN

- The 91 dropped sites: the gold re-sources a worksheet / PDF page as an attached PDF (`pdf/…`) or omits it — the asset is outside the WT (the r292 Media-List class); the button is the honest form until the resource exists.
- The 20 Google / SharePoint embeds keep the iframe (the internal-host list); the gold drops them too — a designer decision, unknowable from the WT.
- The r6 merge-box class (0.08) is DECLINED; the 61 "no box for the previous number" pages are the pagination / letter-offset classes recorded at r400.
