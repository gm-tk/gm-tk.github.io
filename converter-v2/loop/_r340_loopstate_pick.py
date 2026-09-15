import io
p='LOOP_STATE.md'; s=io.open(p,encoding='utf-8',newline='').read(); nl='\r\n' if '\r\n' in s[:3000] else '\n'
PICK = """## Session 7 · Round 3 PICK (engine r340) — written before any code, 2026-09-16 01:25 NZST
- **The queue after r339 (the r336 substitution instrument re-run on the current corpus, `_r340_subst.log`, + two re-sizings):** nothing
  new reaches 20 derivable pages in the Standard / Inquiry rankings — the rows left are the declined / blocked / KB-correct classes
  (col widths c17/c56, `iframe.embed-responsive-item`, `videoSection.icon`, the heading ladder, `paddingR`, `p⇐h5`, `mathJax`,
  `table-bordered`, the `interactive` modifier, acks, the BLL footer, the super-content order); `div#body.container-fluid` (23 pages /
  9 modules) is the gold's own minority — 31 pages carry it against 2,347 bare `id="body"` (the BLL17x series), not a class;
  `div.row.supervisor ⇐ div.row` 16 pages / 15 modules and `div.alert.solid ⇐ div.alert` 19 pages / 9 modules sit under the floor
  (recorded). **c79 (KB queue rank 3) re-sized on the current corpus** (`_measure_r324_lessontitles.py` re-run → `_r340_lessontitles_now.
  json`/`.log`; the pair-count residue `_r340_paircount.py`): exact 567 / case-only 71 / punct 8; `claude = module title, gold = own` 44
  pages whose gold title is in the WT as `[H2]` 13, `[LESSON]` 6, `[PAGE]` 4, a plain line 10, NOT in the WT 10 — four small mechanisms,
  text-only (gate-neutral), none ≥ 20 pages; the pair-count residue (51 pages, all gold-more) is the gold's own second `<h1>` = "Lorem
  Ipsum" / "Maori title not provided" junk (23, ENGJ/MXDB), the module Te Reo repeated on lessons (12 — TRR203/301 MTK, ANZH401's three
  h1s), the module English (2), a lesson's own reo not in the WT (14) — not chased. c79 stays PARTIAL with the residue named.
- **Class: A STANDALONE `[link]`-FAMILY PARAGRAPH WHOSE TEXT IS NOTHING BUT A VIDEO URL IS THE EMBEDDED VIDEO** — the r339 verifier's
  residue class (46 video-href anchored buttons on the `[external link]` emitter). The writer types "[Link] https://www.youtube.com/
  watch?v=…" on its own line (often under "[embed video with image and play button]" or after "Watch the following video…"); today the
  r76 standalone rule ships `<a href target=_blank><div class="externalButton">Go to video</div></a>`, or the `[video]` element with no
  own url prints "[video] with no URL found" and the link becomes the button; the gold EMBEDS (videoSection + iframe). Authority: §1b
  level 4 — the KB is silent on the link form (01E `[video]` → videoSection is the nearest rule; r339's sibling); the gold's consensus
  decides.
- **Measured (`outputs/_measure_r340_linkvideo.cjs` → `_r340_linkvideo.json` / `.log`, the LIVE extractor over all 454 WTs; every
  external-link-family para block carrying a video-id url, paired to the gold by the id):** 71 blocks / 22 modules, gold EMBED 0.74 of
  found — but the shape decides: **url-only (0 visible words) 37 blocks / 13 modules, gold EMBED 26 / 29 found = 0.90** (Standard 0.89
  n=36 / Fundamentals 1.00 n=1; NCEA1 0.86 n=29 / Mathematics 1.00 n=4 / English, ANZH, EXPlore, Leaving-to-Learn 1.00 n=1 each; by
  context: after a media tag with no own url 0.94 n=24 (HIS1006 / HIS1008 / HIS1005 / HIS1007 / XWHA02), after a watch / play sentence
  0.75 n=9, neither 1.00 n=4); a link with ≥ 4 visible words 0.47 (the gold anchors the phrase inline — `[Link for video] Title` ×13 in
  one English module) → the titled form is NOT in the class. Gold BUTTON only 2 (HIS1005 / HIS1007 "If you want to learn more…" +
  `[Link]` — an optional extra), gold ANCHOR 1. **Fix population: 30 blocks / 12 modules** (HIS1006 13, HIS1008 6, HIS1005 2, +9 singles
  — ANZH303, ENFUN01, EXBP901, HIS1003, HIS1007, MXDI202, MXFL203, MXFU202, XWHA02); Claude today BUTTON 25 / ANCHOR 4 / OTHER 1.
- **Mechanism (two seams, one data block `elements.external_link_video_embed` `{ enabled, env "LINKVID_OFF", host_match (the r339
  video-id regex), media_follow }`):** (A) in the `[external link]` inline branch, before the r76 standalone-button rule: a url-only
  external-link item whose url is a VIDEO url → `MediaBuilder.media(it, …, "video", run)` (the standard `[video]` embed, host / icon
  / title-drop conventions included); (B) in `MediaBuilder.media`'s r247 following-link source: a `[video]` / `[embed]` element with no
  own url whose next unconsumed item is such a url-only external-link TAG item takes that url and consumes the item (the r247 rule
  extended from a black line to the tagged line) — so the media tag embeds and no phantom "no URL" note + button ships. Gate:
  skeleton-visible (`a > div.externalButton` → `div.videoSection > iframe`); est. +0.005pp over ~15 pages. Regeneration scope (§0b):
  the OFF/ON probe over all 416 modules gives the changed half; the working half (every `[external link]` with a non-video url, every
  `[video]` with its own url) proven byte-identical by the same probe. Scoped ship #6 since the r334 full backstop (2 of headroom).
- **Triangulation:** HIS1008 (WT `[link] https://www.youtube.com/watch?v=…` under `[embed video with image and play button]` → gold
  `<div class="videoSection icon ratio ratio-16x9"><iframe …>` → Claude a "[video] with no URL found" note + `externalButton` "Go to
  video"); HIS1005 lesson 2 (WT "Click on the play button to watch the short video below." + `[Link:] https://www.youtube.com/
  watch?v=NJ9LJfM4PjM` → gold embed → Claude `externalButton` "Go to video"); ENFUN01 (WT "Ricky Baker 'Happy Birthday song'…" +
  `[Link] https://www.youtube.com/watch?v=us6ZcvCcYoo` → gold embed → Claude `externalButton`).

"""
ANCHOR = "## Session 7 · Round 2 (engine r339) — what shipped"
assert s.count(ANCHOR) == 1 and "Round 3 PICK (engine r340)" not in s
s = s.replace(ANCHOR, PICK.replace("\n", nl) + ANCHOR, 1)
io.open(p,'w',encoding='utf-8',newline='').write(s); print("PICK written")
