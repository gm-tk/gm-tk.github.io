#!/usr/bin/env python3
"""ROUND 359 (loop session 19, Round 3 — the INQUIRY OVERVIEW MENU is the KB 06 §3.4 two-column form: `col-md-6 paddingR`
+ `col-md-6 paddingL`, no banner, `<h4><span>Understand / Know / Do</span></h4>` on the left, `<h5>` titles on the right)
— the anchored engine + data splice. Idempotent; LF; node --check; duplicate-key JSON guard.

  (1) data/Emit_Templates.json — menu.two_col_li.inquiry_family {enabled, env INQMENU_OFF, template_type, source,
      exclude_subjects, left_heading, right_heading, none_becomes}; menu.shells.two_col_inquiry.
  (2) app/js/MenuBuilder.js — #inquiryFamilyFor(run, page); menuTypeFor: a "none" verdict for an Inquiry overview becomes
      "simplified" (the gold always carries the menu — 06 §3.4); buildMenu: the family forces the two_col_li archetype
      (TWHA's "flat"), disables the banner family (ConnectED|1-3's banner_h4_span), swaps the heading templates; out.inquiryFamily.
  (3) app/js/SkeletonBuilder.js — the two_col_inquiry shell when content.menu.inquiryFamily; no banner.
"""
import os, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
MB = os.path.join(PF, "app", "js", "MenuBuilder.js"); SB = os.path.join(PF, "app", "js", "SkeletonBuilder.js"); ET = os.path.join(PF, "data", "Emit_Templates.json")


def rd(p):
    s = open(p, encoding="utf-8", newline="").read(); assert "\r\n" not in s, p; return s


def wr(p, s):
    open(p, "w", encoding="utf-8", newline="").write(s)


def once(s, old, where):
    assert s.count(old) == 1, f"{where}: anchor count {s.count(old)} for {old[:70]!r}"


# ---- (1) data
s = rd(ET)
if '"inquiry_family": {' not in s:
    anchor = '\t\t\t"eng_family": {\n'
    once(s, anchor, "Emit_Templates eng_family")
    block = "\n".join([
        '\t\t\t"inquiry_family": {',
        '\t\t\t\t"enabled": true,',
        '\t\t\t\t"env": "INQMENU_OFF",',
        '\t\t\t\t"template_type": "Inquiry",',
        '\t\t\t\t"source": "Module_Structure_Index.module_meta.<code>.template_type",',
        '\t\t\t\t"exclude_subjects": ["BLL"],',
        '\t\t\t\t"shell": "two_col_inquiry",',
        '\t\t\t\t"left_heading": "<h4><span>{heading}</span></h4>",',
        '\t\t\t\t"right_heading": "<h5>{heading}</h5>",',
        '\t\t\t\t"none_becomes": "simplified",',
        '\t\t\t\t"_doc": "ROUND 359 (the autonomous loop\'s session-19 Round 3, 2026-09-17 — the diff miner\'s MODULE-MENU classes #36 / #46 / #28 / #54, Chris\'s BLL110 finding generalised). KB 06 §3.4 (level 1): an INQUIRY module\'s overview menu is a two-column layout — left column `<h4><span>Understand / Know / Do</span></h4>` headings, right column `<h5>Learning intentions</h5>` + `<h5>How will I know if I\'ve learned it?</h5>`. Measured over the gate\'s 42 paired Inquiry overviews (outputs/_measure_r359_inqmenu.py): the NON-BLL Inquiry families ship exactly that — TWHA / TWHK 8 / 8 `col-md-6 paddingR | col-md-6 paddingL` with `h4>span` left + `h5` right, ConnectED 11 / 14 paddingR | paddingL with `h4>span` left (4 of them with a banner row above), EXPlore 4 / 5 paddingR | paddingL with `h4>span` both sides — while Claude shipped the BLL banner shell (`col-md-12 paddingR` banner + two `paddingR` columns + `h5>span`) for ConnectED 4-6 / 7-8, a single `col-md-8` column for TWHA (no overview convention in Html_Convention_Registry → \'flat\') and NO menu for CEDW101 / CEDW201 / CEDR204 (a no-evidence menu value). The BLL Inquiry PARENTS are excluded (exclude_subjects): their own gold IS the banner form on 7 of 11 (BLL110 / BLL120 are the family\'s outliers — the r178 rule). The family: (a) an Inquiry-template overview (the module index\'s template_type — a module the index does not know keeps today\'s path) outside the excluded subjects forces the two_col_li archetype (TWHA\'s flat → two columns), disables the banner family and the banner, and renders through the two_col_inquiry shell with these heading templates; (b) menuTypeFor\'s \'none\' verdict for such a page becomes none_becomes (\'simplified\') so the button and the menu emit. D10-9\'s `<h5>` labels (\'We are learning:\') in the right column stay (the gold\'s `<p>` lead-in is the recorded named override). OFF (INQMENU_OFF) = the r358 output on every page."',
        '\t\t\t},',
        '',
    ])
    s = s.replace(anchor, block + anchor, 1)
    anchor2 = '\t\t\t"_two_col_offset_note":'
    once(s, anchor2, "Emit_Templates _two_col_offset_note")
    shell = ('\t\t\t"two_col_inquiry": "<div id=\\"module-menu-content\\" class=\\"moduleMenu\\">\\n<div class=\\"row\\">\\n<div class=\\"col-md-6 col-12 paddingR\\">\\n{leftContent}\\n</div>\\n<div class=\\"col-md-6 col-12 paddingL\\">\\n{rightContent}\\n</div>\\n</div>\\n</div>",\n'
             '\t\t\t"_two_col_inquiry_note": "ROUND 359 — the INQUIRY two-column overview menu (KB 06 §3.4): NO banner, `col-md-6 col-12 paddingR` left + `col-md-6 col-12 paddingL` right. Selected by SkeletonBuilder when content.menu.inquiryFamily is true (menu.two_col_li.inquiry_family). The BLL `two_col_li` shell (banner + paddingR ×2) and the ENG `two_col_offset` shell are untouched.",\n')
    s = s.replace(anchor2, shell + anchor2, 1)

    def no_dupes(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise SystemExit(f"duplicate key: {[k for k in keys if keys.count(k) > 1]}")
        return dict(pairs)
    json.loads(s, object_pairs_hook=no_dupes)
    wr(ET, s); print("Emit_Templates.json: inquiry_family + two_col_inquiry shell")
else:
    print("Emit_Templates.json: already")

# ---- (2) MenuBuilder
s = rd(MB)
if "static #inquiryFamilyFor(" not in s:
    # (2a) menuTypeFor wrapper + the helper
    old = "\tstatic menuTypeFor(page, run) {\n"
    once(s, old, "menuTypeFor")
    new = "\n".join([
        "\t/**",
        "\t * ROUND 359 (the autonomous loop's session-19 Round 3 — the diff miner's MODULE-MENU classes; KB 06 §3.4). The INQUIRY",
        "\t * overview-menu family: this page is an OVERVIEW of an Inquiry-template module (the module index's template_type — a",
        "\t * module the index does not know keeps today's path) whose subject is not excluded (the BLL parents' own gold is the",
        "\t * banner form). Returns the family config or null. Data menu.two_col_li.inquiry_family; env INQMENU_OFF.",
        "\t */",
        "\tstatic #inquiryFamilyFor(run, page) {",
        "\t\tconst cfg = DataService.Data.EmitTemplates?.menu?.two_col_li?.inquiry_family;",
        "\t\tif (!cfg || cfg.enabled === false || !page?.isOverview) return null;",
        "\t\tif (typeof process !== \"undefined\" && process.env && process.env[cfg.env ?? \"INQMENU_OFF\"]) return null;",
        "\t\tconst code = String(run?.moduleCode || \"\");",
        "\t\tconst tt = DataService.Data.ModuleStructureIndex?.module_meta?.[code]?.template_type;",
        "\t\tif (!tt || tt !== (cfg.template_type ?? \"Inquiry\")) return null;",
        "\t\tconst subj = code.match(/^[A-Za-z]+/)?.[0] ?? \"\";",
        "\t\tif ((cfg.exclude_subjects ?? []).some((p) => subj.toUpperCase().startsWith(String(p).toUpperCase()))) return null;",
        "\t\treturn cfg;",
        "\t}",
        "",
        "\tstatic menuTypeFor(page, run) {",
        "\t\tconst base = this.#menuTypeForBase(page, run);",
        "\t\t// ROUND 359: an Inquiry overview always carries its menu (KB 06 §3.4) — a registry 'none' verdict (CEDW101 / CEDW201 /",
        "\t\t// CEDR204's no-evidence value) becomes the family's none_becomes ('simplified'); tabs and simplified pass through.",
        "\t\tconst inq = this.#inquiryFamilyFor(run, page);",
        "\t\tif (inq && base === \"none\") return inq.none_becomes ?? \"simplified\";",
        "\t\treturn base;",
        "\t}",
        "",
        "\tstatic #menuTypeForBase(page, run) {",
        "",
    ])
    s = s.replace(old, new, 1)
    # (2b) the archetype / family decision
    old = ("\t\tconst archetype = menuType === \"tabs\" ? \"tabs\"\n"
           "\t\t\t: (convention?.archetype === \"two_col_li\" ? \"two_col_li\" : \"flat\");\n")
    once(s, old, "archetype")
    s = s.replace(old, "\t\tlet archetype = menuType === \"tabs\" ? \"tabs\"\n\t\t\t: (convention?.archetype === \"two_col_li\" ? \"two_col_li\" : \"flat\");\n", 1)
    old = ("\t\tconst bannerFamily = archetype === \"two_col_li\"\n"
           "\t\t\t&& !engFamily\n"
           "\t\t\t&& bannerCfg && bannerCfg.enabled !== false\n"
           "\t\t\t&& convention?.banner_h4_span === true\n"
           "\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env.BANNERMENU_OFF);\n")
    once(s, old, "bannerFamily")
    new = ("\t\tlet bannerFamily = archetype === \"two_col_li\"\n"
           "\t\t\t&& !engFamily\n"
           "\t\t\t&& bannerCfg && bannerCfg.enabled !== false\n"
           "\t\t\t&& convention?.banner_h4_span === true\n"
           "\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env.BANNERMENU_OFF);\n"
           "\t\t// THE INQUIRY FAMILY (ROUND 359 — KB 06 §3.4; menu.two_col_li.inquiry_family; env INQMENU_OFF): an Inquiry-template\n"
           "\t\t// OVERVIEW outside the excluded subjects renders the two-column form — the archetype is FORCED to two_col_li (TWHA's\n"
           "\t\t// 'flat' convention gave it one col-md-8 column), the banner family is off (ConnectED|1-3's mined banner_h4_span),\n"
           "\t\t// the left headings are h4>span and the shell is two_col_inquiry (paddingR | paddingL, no banner). The ENG offset\n"
           "\t\t// family and a tabs menu are untouched. See #inquiryFamilyFor.\n"
           "\t\tconst inqCfg = this.#inquiryFamilyFor(run, page);\n"
           "\t\tconst inqFamily = !!inqCfg && !engFamily && archetype !== \"tabs\";\n"
           "\t\tif (inqFamily) { archetype = \"two_col_li\"; bannerFamily = false; }\n")
    s = s.replace(old, new, 1)
    old = "\t\tconst out = { kind: menuType, archetype, engFamily, bannerFamily, bannerLabel: \"\","
    once(s, old, "out")
    s = s.replace(old, "\t\tconst out = { kind: menuType, archetype, engFamily, bannerFamily, inquiryFamily: inqFamily, bannerLabel: \"\",", 1)
    # (2c) the heading templates at the three generic-path push sites
    old = "\t\t\t\t\t\t\tpush(Utils.FillTemplate(cfg.left_heading, { heading: Utils.EscapeHtml(label) }));\n"
    once(s, old, "curricSplit left_heading")
    s = s.replace(old, "\t\t\t\t\t\t\tpush(Utils.FillTemplate((inqFamily ? inqCfg.left_heading : cfg.left_heading), { heading: Utils.EscapeHtml(label) }));   // r359: the Inquiry family's h4>span\n", 1)
    old = "\t\t\t\t\t\t\t\tbucket === \"left\" ? cfg.left_heading : cfg.right_heading,\n"
    once(s, old, "plain heading push")
    s = s.replace(old, "\t\t\t\t\t\t\t\tbucket === \"left\" ? (inqFamily ? inqCfg.left_heading : cfg.left_heading) : (inqFamily ? inqCfg.right_heading : cfg.right_heading),   // r359\n", 1)
    old = "\t\t\t\t\t\t\t\t\tleft ? cfg.left_heading : cfg.right_heading,\n"
    once(s, old, "bold-label heading push")
    s = s.replace(old, "\t\t\t\t\t\t\t\t\tleft ? (inqFamily ? inqCfg.left_heading : cfg.left_heading) : (inqFamily ? inqCfg.right_heading : cfg.right_heading),   // r359\n", 1)
    wr(MB, s); print("MenuBuilder.js: #inquiryFamilyFor, menuTypeFor wrapper, the family decision, 3 heading sites")
else:
    print("MenuBuilder.js: already")

# ---- (3) SkeletonBuilder
s = rd(SB)
if "two_col_inquiry" not in s:
    old = "\t\t\t\t\t\t? (content.menu.engFamily ? \"two_col_offset\" : \"two_col_li\")\n"
    once(s, old, "shellKey")
    s = s.replace(old, "\t\t\t\t\t\t? (content.menu.engFamily ? \"two_col_offset\" : (content.menu.inquiryFamily ? \"two_col_inquiry\" : \"two_col_li\"))   // r359: the Inquiry two-column shell\n", 1)
    old = "\t\t\t\t\tbanner: content.menu.engFamily ? \"\"\n"
    once(s, old, "banner fill")
    s = s.replace(old, "\t\t\t\t\tbanner: (content.menu.engFamily || content.menu.inquiryFamily) ? \"\"\n", 1)
    wr(SB, s); print("SkeletonBuilder.js: two_col_inquiry shell + no banner")
else:
    print("SkeletonBuilder.js: already")

for p in (MB, SB):
    r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
    print(os.path.basename(p), "node --check:", "OK" if r.returncode == 0 else r.stderr[:300])
