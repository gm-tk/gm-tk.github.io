#!/usr/bin/env python3
"""Session 26 Round 10 (engine r396) — A CAROUSEL VIDEO SLIDE WITH A CAPTION IS `item video`: a slide whose parts hold a
videoSection AND a carousel-caption block carries the class `item video` (the gold 0.92); a video-only slide stays `item`
(the gold 0.55 — a tie, recorded). Data: `interactive.carousel.item_video_with_caption {enabled, env ITEMVIDEO_OFF, from, to}`.
Engine: `#carRenderSlides` (the rich / table slide renderer shared by rich_slides + table_slides) swaps the item's class when both
hold. Also writes the PICK. LF preserved. Idempotent. Run under WSL."""
import io, os, sys
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
PF = ROOT + "/pageforge-site/converter-v2"

LS = ROOT + "/LOOP_STATE.md"
s = io.open(LS, encoding="utf-8", newline="").read()
if "## Session 26 — Round 10 PICK (engine r396)" not in s:
    PICK = """## Session 26 — Round 10 PICK (engine r396): A CAROUSEL VIDEO SLIDE WITH A CAPTION IS `item video` — the class the gold gives a captioned video slide, which Claude's rich / table slide renderer never sets · THE FULL-REGENERATION BACKSTOP (scoped #8 → full)
- **The lead:** the widget-wrapper census generalised from r394 (`outputs/_s26_r396_widgetwrap.py` → `.out`, every built widget's two enclosing wrappers, gold vs Claude): under `videoSection` the gold's carousel items are `div.item.video` 660 (127 pages) against Claude's plain `div.item` 894 (173 pages). The item census (`_s26_r396_itemvideo.py` / `.out`): of the gold's 1393 video-carrying carousel items 813 = 0.58 carry `item video` (Claude 125 of 932 = 0.13) — a tie corpus-wide, so decomposed by the slide's OTHER content (`_s26_r396_itemvideo2.py` / `.out`): **a video slide WITH a `carousel-caption` block → `item video` 273 / 298 = 0.92** (Inquiry / BLL 51 / 51, Fundamentals 45 / 46, English 38 / 38, NCEA1 20 / 20, ANZH 18 / 18, Leaving to Learn 28 / 38 = 0.74); Claude's 193 such slides carry `item video` 22 (the media-caption-table builder's own `item_video_caption`) and plain `item` 171 (the rich / table slide renderer). **A video-ONLY slide → `item video` 496 / 907 = 0.55 — a TIE** (Inquiry / BLL 0.67, Maths 0.75, LtL 0.65, ConnectED 0.60, Standard / BLL 0.32, EXPlore 0.00) — recorded, not taken; a slide with a heading or a bare paragraph stays `item` (0.12 / 0.13 / 0.33).
- **KB-first check:** the carousel data's `item_video` / `item_video_caption` templates already name `item video` for the homogeneous-video and media-caption-table builds (r-era measurements); nothing in the KB on the class per slide content → §1b level 3 / 4, the gold's own consensus 0.92 on 298 gold slides. A class token, structure-only → derivable (the slide's own parts decide).
- **Fix (DATA OVER CODE):** `interactive.carousel.item_video_with_caption {enabled, env: ITEMVIDEO_OFF, from: "<div class=\\"item\\">", to: "<div class=\\"item video\\">"}` — in `#carRenderSlides` (the renderer both `rich_slides` and `table_slides` use): when the slide's chunks hold a `videoSection` AND the caption block was opened (`capOpen`), the item's opening tag is swapped. The media-caption-table builder keeps its own templates. OFF = the r395 output.
- **Regeneration: FULL** — the ledger stands at scoped #7 since the r388 full, so this ship is the backstop: every one of the 416 gated dirs regenerates (the r388 batch list, 36 batches, 4 in parallel), `_content_manifest.py fresh` over the whole corpus must report 0 truly stale, the manifest diff must equal the probe's ON set exactly (no residue from r389–r395), then the full gate suite; `_ship_ledger.py record-full --round 396`.

"""
    i = s.index("## Round log\n")
    s = s[:i] + PICK + s[i:]
    io.open(LS, "w", encoding="utf-8", newline="").write(s); print("PICK written")

P = PF + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"item_video_with_caption"' not in s:
    old = '\t\t\t"item_video": "<div class=\\"item video\\">\\n{embed}\\n</div>",\n'
    assert s.count(old) == 1, s.count(old)
    new = (old +
           '\t\t\t"item_video_with_caption": {\n'
           '\t\t\t\t"_doc": "ROUND 396 (the autonomous loop\'s session 26 Round 10 — the censuses outputs/_s26_r396_itemvideo.py / _itemvideo2.py). A CAROUSEL VIDEO SLIDE WITH A CAPTION IS `item video`: of the gold\'s video-carrying carousel slides that also hold a carousel-caption block, 273 / 298 = 0.92 carry the class `item video` (Inquiry / BLL 51 / 51, Fundamentals 45 / 46, English 38 / 38, NCEA1 20 / 20, ANZH 18 / 18, LtL 28 / 38); Claude\'s rich / table slide renderer shipped 171 of them as plain `item`. A video-ONLY slide is a tie (496 / 907 = 0.55) and stays `item`; a slide with a heading or a bare paragraph stays `item` (0.12–0.33). In #carRenderSlides, when the slide\'s chunks hold a videoSection AND the caption block was opened, `from` is swapped for `to` in the finished item. The media-caption-table builder keeps its own item_video_caption template. OFF = the r395 output.",\n'
           '\t\t\t\t"enabled": true,\n'
           '\t\t\t\t"env": "ITEMVIDEO_OFF",\n'
           '\t\t\t\t"from": "<div class=\\"item\\">",\n'
           '\t\t\t\t"to": "<div class=\\"item video\\">"\n'
           '\t\t\t},\n')
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: carousel.item_video_with_caption added")
else:
    print("data: already")

P2 = PF + "/app/js/InteractiveBuilder.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "item_video_with_caption" not in s:
    old = ("\t\t\tif (capOpen) chunks.push(cfg.caption_close);\n"
           "\t\t\titems.push(Utils.FillTemplate(cfg.item, { parts: chunks.join(\"\\n\") }));\n")
    assert s.count(old) == 1, s.count(old)
    new = ("\t\t\tif (capOpen) chunks.push(cfg.caption_close);\n"
           "\t\t\tlet _slide = Utils.FillTemplate(cfg.item, { parts: chunks.join(\"\\n\") });\n"
           "\t\t\t// ROUND 396 — A CAROUSEL VIDEO SLIDE WITH A CAPTION IS `item video`: the gold gives a\n"
           "\t\t\t// captioned video slide that class 273 / 298 = 0.92 (a video-only slide is a tie and stays\n"
           "\t\t\t// `item`). Data carousel.item_video_with_caption; env ITEMVIDEO_OFF (= the r395 output).\n"
           "\t\t\tconst _ivc = tpl?.item_video_with_caption;\n"
           "\t\t\tif (_ivc && _ivc.enabled !== false && capOpen && /\\bvideoSection\\b/.test(_slide)\n"
           "\t\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[_ivc.env ?? \"ITEMVIDEO_OFF\"])) {\n"
           "\t\t\t\tconst _from = _ivc.from ?? \"<div class=\\\"item\\\">\", _to = _ivc.to ?? \"<div class=\\\"item video\\\">\";\n"
           "\t\t\t\tif (_slide.startsWith(_from)) _slide = _to + _slide.slice(_from.length);\n"
           "\t\t\t}\n"
           "\t\t\titems.push(_slide);\n")
    s = s.replace(old, new, 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: #carRenderSlides item video with caption")
else:
    print("engine: already")
