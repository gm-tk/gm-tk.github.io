#!/usr/bin/env python3
"""ROUND 359 — the refinements after the first in-memory probe.
  (a) ContentConverter #partitionItems, the content-based overview fallback: a menu-section label followed by a COLON
      ("Understand:", "Know:", "Do:") is a label (CEDT101 / CEDT104 / CEDT207 … keep their curriculum block in the menu
      instead of the body). Data menu.overview_section_labels_colon {enabled, env INQFAMILY_OFF}.
  (b) MenuBuilder.buildMenu: an Inquiry overview with NO menu items ships no menu at all (ENGFUN02 — no empty shell).
  (c) SkeletonBuilder: an Inquiry family menu whose LEFT column is empty carries a Writers Note (the curriculum statements
      are the developer's — TWHA's gold writes them from the curriculum, the WT has none). Data inquiry_family.empty_left_note.
Idempotent; LF; node --check; duplicate-key JSON guard.
"""
import os, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
CC = os.path.join(PF, "app", "js", "ContentConverter.js"); MB = os.path.join(PF, "app", "js", "MenuBuilder.js")
SB = os.path.join(PF, "app", "js", "SkeletonBuilder.js"); ET = os.path.join(PF, "data", "Emit_Templates.json")


def rd(p):
    s = open(p, encoding="utf-8", newline="").read(); assert "\r\n" not in s, p; return s


def wr(p, s):
    open(p, "w", encoding="utf-8", newline="").write(s)


def once(s, old, where):
    assert s.count(old) == 1, f"{where}: anchor count {s.count(old)} for {old[:70]!r}"


# (a) the colon label match
s = rd(CC)
if "overview_section_labels_colon" not in s:
    old = ("\t\t\tconst matchesLabel = (f) => labels.some((l) =>\n"
           "\t\t\t\tf === l || f.startsWith(l + \" \") || f.endsWith(\" \" + l) || f.includes(\" \" + l + \" \"));\n")
    once(s, old, "matchesLabel")
    new = ("\t\t\t// ROUND 359 (the Inquiry overview menu): a section label the writer typed WITH A COLON — \"Understand:\", \"Know:\",\n"
           "\t\t\t// \"Do:\" (CEDT101 / CEDT104 / CEDT207 …) — is that label; the plain test needed a following SPACE, so the curriculum\n"
           "\t\t\t// block fell to the body while the gold's menu carries it. Data menu.overview_section_labels_colon; env INQFAMILY_OFF.\n"
           "\t\t\tconst colonCfg = DataService.Data.EmitTemplates.menu.overview_section_labels_colon;\n"
           "\t\t\tconst colonOn = !!colonCfg && colonCfg.enabled !== false\n"
           "\t\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[colonCfg.env ?? \"INQFAMILY_OFF\"]);\n"
           "\t\t\tconst matchesLabel = (f) => labels.some((l) =>\n"
           "\t\t\t\tf === l || f.startsWith(l + \" \") || f.endsWith(\" \" + l) || f.includes(\" \" + l + \" \")\n"
           "\t\t\t\t|| (colonOn && (f === l + \":\" || f.startsWith(l + \": \") || f.startsWith(l + \":\"))));\n")
    s = s.replace(old, new, 1)
    wr(CC, s); print("ContentConverter.js: colon label match")
else:
    print("ContentConverter.js: already")

# (b) no empty shell
s = rd(MB)
if "an Inquiry overview with nothing to put in the menu" not in s:
    old = ("\tstatic buildMenu(menuItems, menuType, run, page, norm) {\n"
           "\t\tif (menuType === \"none\" || !menuItems.length) {\n"
           "\t\t\treturn { kind: menuType, tab1: \"\", tab2: \"\", content: \"\", left: \"\", right: \"\" };\n"
           "\t\t}\n")
    once(s, old, "buildMenu early return")
    new = ("\tstatic buildMenu(menuItems, menuType, run, page, norm) {\n"
           "\t\tif (menuType === \"none\" || !menuItems.length) {\n"
           "\t\t\t// ROUND 359: an Inquiry overview with nothing to put in the menu ships NO menu (ENGFUN02) — menuTypeFor's\n"
           "\t\t\t// none_becomes only serves a page that has menu content; an empty shell is never emitted.\n"
           "\t\t\tconst kind = (!menuItems.length && this.#inquiryFamilyFor(run, page)) ? \"none\" : menuType;\n"
           "\t\t\treturn { kind, tab1: \"\", tab2: \"\", content: \"\", left: \"\", right: \"\" };\n"
           "\t\t}\n")
    s = s.replace(old, new, 1)
    wr(MB, s); print("MenuBuilder.js: no empty Inquiry shell")
else:
    print("MenuBuilder.js: already")

# (c) the empty-left note
s = rd(SB)
if "empty_left_note" not in s:
    old = "\t\t\t\t\tleftContent: content.menu.left ?? \"\",\n"
    once(s, old, "leftContent")
    new = ("\t\t\t\t\t// ROUND 359: an Inquiry family menu with NO curriculum (Understand / Know / Do) block leaves the left column\n"
           "\t\t\t\t\t// to the developer with a Writers Note (TWHA's gold writes the statements from the curriculum; the WT has none).\n"
           "\t\t\t\t\tleftContent: (content.menu.left || ((content.menu.inquiryFamily && tpl.menu.two_col_li?.inquiry_family?.empty_left_note) || \"\")),\n")
    s = s.replace(old, new, 1)
    wr(SB, s); print("SkeletonBuilder.js: empty-left note")
else:
    print("SkeletonBuilder.js: already")

# data
s = rd(ET)
if '"overview_section_labels_colon"' not in s:
    old = '\t\t\t"none_becomes": "simplified",\n'
    once(s, old, "none_becomes")
    s = s.replace(old, old + '\t\t\t\t"empty_left_note": "<p class=\\"cv2-note\\" style=\\"color: red; font-weight: bold;\\">Writers Note: the curriculum Understand / Know / Do statements for this module go in this column — they are not in the Writers Template (the human developer writes them from the curriculum).</p>",\n', 1)
    old = '\t\t"overview_section_labels": [\n'
    once(s, old, "overview_section_labels")
    s = s.replace(old, '\t\t"overview_section_labels_colon": {\n\t\t\t"enabled": true,\n\t\t\t"env": "INQFAMILY_OFF",\n\t\t\t"_doc": "ROUND 359: in the content-based overview fallback (no [MODULE INTRODUCTION], no mid-document title-bar alias) a section label the writer typed with a trailing colon (\'Understand:\', \'Know:\', \'Do:\' — CEDT101 / 104 / 207 / 208 / 301 / 404, the ConnectED Inquiry form) matches overview_section_labels; the plain test needed a following space and left the curriculum block in the body while the gold\'s menu carries it. Shares the round\'s toggle."\n\t\t},\n' + old, 1)

    def no_dupes(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise SystemExit(f"duplicate key: {[k for k in keys if keys.count(k) > 1]}")
        return dict(pairs)
    json.loads(s, object_pairs_hook=no_dupes)
    wr(ET, s); print("Emit_Templates.json: labels_colon + empty_left_note")
else:
    print("Emit_Templates.json: already")
for p in (CC, MB, SB):
    r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
    print(os.path.basename(p), "node --check:", "OK" if r.returncode == 0 else r.stderr[:300])
