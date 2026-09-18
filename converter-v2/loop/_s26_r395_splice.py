#!/usr/bin/env python3
"""Session 26 Round 9 (engine r395) — THE FLIP-CARD COLUMN WIDTH FOLLOWS THE CARD COUNT: a 2-card or 4-card flipCard group
renders its cards in `col-md-6 col-12 paddingLR` (the gold 0.86 / 0.76), the rest keep the template's `col-md-4`.
Data: `interactive.flipCard.card_col_by_count {enabled, env FLIPCOL_OFF, default, by_count}`. Engine: `#flipCardsByCount(tpl, cards)`
applied at the four `tpl.card` join sites (the image-front card_image_front family untouched). Also writes the PICK. LF preserved.
Idempotent. Run under WSL."""
import io, os, sys
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
PF = ROOT + "/pageforge-site/converter-v2"

LS = ROOT + "/LOOP_STATE.md"
s = io.open(LS, encoding="utf-8", newline="").read()
if "## Session 26 — Round 9 PICK (engine r395)" not in s:
    PICK = """## Session 26 — Round 9 PICK (engine r395): THE FLIP-CARD COLUMN WIDTH FOLLOWS THE CARD COUNT — a 2-card or 4-card group is `col-md-6`, not the template's `col-md-4`
- **The lead:** the r394 column census (`_s26_r394_colrow.out`) listed the gold's flip-card columns as `col-md-6 paddingLR` 72 (59 pages) against `col-md-4` 45 — Claude's 176 all `col-md-4`. The paired widget census (`outputs/_s26_r395_flipcols.py` → `.out`, every `flipCardsContainer`'s card count and column class, gold vs Claude, per subject): **4 cards — gold `col-md-6` 48 (39 pages) + `col-md-6 col-sm-6` 9 + `col-md-3` 16 + `col-md-4` 2 → `col-md-6` 0.76; Claude `col-md-4` 57 on 49 pages / 43 modules. 2 cards — gold `col-md-6` 39 (28 pages) + `col-6 col-md-6` 11 + `col-md-4` 8 → 0.86; Claude `col-md-4` 19 on 18 pages / 14 modules.** 3 cards `col-md-4` 100 / 5–12 cards `col-md-4` (Claude already matches). 1 card: the gold `col-md-12` 17 (16 pages) = 0.63 but Claude's 1-card groups sit on 8 pages — UNDER the floor, recorded, not taken. By subject the 4-card `col-md-6` holds in Mathematics 13, English 9, Online Safety 8, LtL 5, TEDC 3 (English's `col-md-3` 7 is the minority); the 2-card `col-md-6` in LtL 15, TEDC 4 (Te ara Whakapuawa's `col-6 col-md-6` 11 is its own form).
- **KB-first check:** 02C names `flipCardsContainer` on the wrapper row and nothing on the column width; 07C's `col-md-6 col-12 paddingLR` is the word / image grid — nothing on a flip card's width by count → §1b level 3 / 4 (the gold's own consensus 0.86 / 0.76 on 28 / 39 gold pages, 18 / 49 Claude pages). A wrapper class token, structure-only → derivable (the card count is the writer's own table).
- **Fix (DATA OVER CODE):** `interactive.flipCard.card_col_by_count {enabled, env: FLIPCOL_OFF, default: "col-md-4 col-12 paddingLR", by_count: {"2": "col-md-6 col-12 paddingLR", "4": "col-md-6 col-12 paddingLR"}}` — `#flipCardsByCount(tpl, cards)` swaps the template's default column class for the by-count class in each finished card (first occurrence = the wrapper) at the four `tpl.card` join sites (the table builder, the r2xx composer, the alternating and transposed readers); the image-front `card_image_front` family (`col-md-6 col-sm-6`, the gold's own form for it) is untouched. OFF = the r394 output. Regeneration: SCOPED (the probe's ON list) = scoped ship #7 since the r388 full (the NEXT ship is the FULL backstop).

"""
    i = s.index("## Round log\n")
    s = s[:i] + PICK + s[i:]
    io.open(LS, "w", encoding="utf-8", newline="").write(s); print("PICK written")

P = PF + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"card_col_by_count"' not in s:
    old = '\t\t\t"card": "<div class=\\"col-md-4 col-12 paddingLR\\"><div class=\\"flipCard\\">'
    assert s.count(old) == 1, s.count(old)
    new = ('\t\t\t"card_col_by_count": {\n'
           '\t\t\t\t"_doc": "ROUND 395 (the autonomous loop\'s session 26 Round 9 — the census outputs/_s26_r395_flipcols.py). THE FLIP-CARD COLUMN WIDTH FOLLOWS THE CARD COUNT: over the gold\'s flipCardsContainer groups a 4-card group\'s cards are `col-md-6 col-12 paddingLR` 0.76 (48 + 9 col-sm-6 of 75; col-md-3 16, col-md-4 2) and a 2-card group\'s 0.86 (39 + 11 col-6 of 58; col-md-4 8); 3 cards and 5+ cards are col-md-4 (the template default). Claude shipped every card col-md-4 (4-card groups 57 on 49 pages / 43 modules, 2-card 19 on 18 pages / 14 modules). A 1-card group is col-md-12 in the gold (17 of 27 = 0.63) but on 8 Claude pages — under the floor, not listed. `#flipCardsByCount` swaps `default` for the by_count class in each finished card at the four tpl.card join sites; the image-front card_image_front family is untouched. OFF = the r394 output.",\n'
           '\t\t\t\t"enabled": true,\n'
           '\t\t\t\t"env": "FLIPCOL_OFF",\n'
           '\t\t\t\t"default": "col-md-4 col-12 paddingLR",\n'
           '\t\t\t\t"by_count": {\n'
           '\t\t\t\t\t"2": "col-md-6 col-12 paddingLR",\n'
           '\t\t\t\t\t"4": "col-md-6 col-12 paddingLR"\n'
           '\t\t\t\t}\n'
           '\t\t\t},\n' + old)
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: flipCard.card_col_by_count added")
else:
    print("data: already")

P2 = PF + "/app/js/InteractiveBuilder.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "#flipCardsByCount" not in s:
    sites = [
        "\t\treturn [tpl.container_open, ...cards, tpl.container_close].join(\"\\n\");\n\t}\n",
        "\t\treturn [tpl.container_open, ...built, tpl.container_close].join(\"\\n\");\n\t}\n",
        "\t\treturn cards.length ? [tpl.container_open, ...cards, tpl.container_close].join(\"\\n\") : null;\n",
    ]
    # site 1: the table builder (one occurrence); site 2: the r2xx composer — two occurrences of this exact text (the image-front
    # member builder at 4810 and the composer at 4898) — only the composer uses tpl.card, so patch the SECOND; site 3: the
    # alternating + transposed readers (tpl.card) and the multi-row reader (card_image_front) — patch the FIRST TWO only.
    assert s.count(sites[0]) == 1, s.count(sites[0])
    s = s.replace(sites[0], "\t\treturn [tpl.container_open, ...this.#flipCardsByCount(tpl, cards), tpl.container_close].join(\"\\n\");\n\t}\n", 1)
    assert s.count(sites[1]) == 2, s.count(sites[1])
    first = s.index(sites[1]); second = s.index(sites[1], first + 1)
    s = s[:second] + "\t\treturn [tpl.container_open, ...this.#flipCardsByCount(tpl, built), tpl.container_close].join(\"\\n\");\n\t}\n" + s[second + len(sites[1]):]
    assert s.count(sites[2]) == 3, s.count(sites[2])
    rep = "\t\treturn cards.length ? [tpl.container_open, ...this.#flipCardsByCount(tpl, cards), tpl.container_close].join(\"\\n\") : null;\n"
    a = s.index(sites[2]); s = s[:a] + rep + s[a + len(sites[2]):]
    b = s.index(sites[2], a + len(rep)); s = s[:b] + rep + s[b + len(sites[2]):]
    # the helper, placed before the table builder's docblock anchor `static #flipCardTransposed` is far away; anchor on the
    # member-image builder's JSDoc start instead
    anchor = "\t/**\n\t * MEMBER-CAPTURED image-front flipCards (verified against OSAI501-03)."
    assert s.count(anchor) == 1, s.count(anchor)
    helper = ("\t/**\n"
              "\t * ROUND 395 — THE FLIP-CARD COLUMN WIDTH FOLLOWS THE CARD COUNT. Over the gold's\n"
              "\t * flipCardsContainer groups a 4-card group's cards are col-md-6 (0.76) and a 2-card\n"
              "\t * group's col-md-6 (0.86); 3 and 5+ cards keep col-md-4 (the template default). Claude\n"
              "\t * shipped every card col-md-4. Swaps the data default for the by-count class in each\n"
              "\t * finished card (the first occurrence = the wrapper column). Data\n"
              "\t * flipCard.card_col_by_count; env FLIPCOL_OFF (= the r394 output).\n"
              "\t * @param {Object} tpl - the flipCard template block\n"
              "\t * @param {string[]} cards - the finished card html strings\n"
              "\t * @returns {string[]}\n"
              "\t */\n"
              "\tstatic #flipCardsByCount(tpl, cards) {\n"
              "\t\tconst cfg = tpl?.card_col_by_count;\n"
              "\t\tif (!cfg || cfg.enabled === false || !Array.isArray(cards)) return cards;\n"
              "\t\tif (typeof process !== \"undefined\" && process.env && process.env[cfg.env ?? \"FLIPCOL_OFF\"]) return cards;\n"
              "\t\tconst to = (cfg.by_count ?? {})[String(cards.length)];\n"
              "\t\tconst from = cfg.default ?? \"col-md-4 col-12 paddingLR\";\n"
              "\t\tif (!to || to === from) return cards;\n"
              "\t\treturn cards.map((c) => String(c).replace(`class=\"${from}\"`, `class=\"${to}\"`));\n"
              "\t}\n\n")
    s = s.replace(anchor, helper + anchor, 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: #flipCardsByCount + 4 sites")
else:
    print("engine: already")
