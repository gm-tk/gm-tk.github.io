# _r342_patch_membertext.py — ROUND 342: a tag member whose words ride its own bracket line
# ("[audio] while, whale, whirl, whole, whine") is CONTENT for the hand-off box: the empty-box
# guards count it and the member dump renders it. Data interactive_placeholder.embedded_member_text
# (env MEMBERTEXT_OFF). Tabs/LF preserved (io.open newline="").
import io, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2")
CC = os.path.join(ROOT, "app", "js", "ContentConverter.js")
ET = os.path.join(ROOT, "data", "Emit_Templates.json")

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)

cc = rd(CC)
old_guard = '\t\tconst hasText = (it) => String(it.type === "black" ? it.text : (it.blackAfter ?? "")).trim().length > 0;\n'
new_guard = (
    '\t\t// ROUND 342 — a TAG member whose words ride its OWN bracket line ("[audio] while,\n'
    '\t\t// whale, whirl, whole, whine" — an ELEMENT with embedded text and an empty tail) is\n'
    '\t\t// member CONTENT: the guards below count it and the dump renders it. Before this the\n'
    '\t\t// two guards read blackAfter alone, so a bundle whose only member was such an element\n'
    '\t\t// rendered as notes-only (or the "no content captured" flag) and the writer\'s words\n'
    '\t\t// vanished from the page (BLL240 1.1 wordDrag, BLL150/BLL166 dragAndDrop audio lists,\n'
    '\t\t// ENGC101 4.0\'s five [image] faces). Data interactive_placeholder.embedded_member_text\n'
    '\t\t// (directives listed there; an instruction-class member never counts — it already\n'
    '\t\t// surfaces as the note before the box); env MEMBERTEXT_OFF.\n'
    '\t\tconst embCfg = DataService.Data.EmitTemplates.interactive_placeholder?.embedded_member_text;\n'
    '\t\tconst embOn = embCfg && embCfg.enabled !== false\n'
    '\t\t\t&& !(typeof process !== "undefined" && process.env && process.env.MEMBERTEXT_OFF);\n'
    '\t\tconst embeddedText = (it) => {\n'
    '\t\t\tif (!embOn || !it || it.type !== "tag" || String(it.blackAfter ?? "").trim()) return "";\n'
    '\t\t\tconst p = it.parse; const prim = p?.primary;\n'
    '\t\t\tif (!prim || p.class !== "tag" || p.instructionFragment) return "";\n'
    '\t\t\tif (!(embCfg.directives ?? ["ELEMENT", "INLINE"]).includes(prim.directive)) return "";\n'
    '\t\t\tlet words = ""; try { words = this.#norm.RenderText(it.text) || ""; } catch { words = ""; }\n'
    '\t\t\treturn words.trim() ? String(it.text ?? "").replace(/\\s+/g, " ").trim() : "";\n'
    '\t\t};\n'
    '\t\tconst hasText = (it) => String(it.type === "black" ? it.text : (it.blackAfter ?? "")).trim().length > 0\n'
    '\t\t\t|| embeddedText(it).length > 0;\n'
)
assert cc.count(old_guard) == 1, cc.count(old_guard)
cc = cc.replace(old_guard, new_guard)

old_dump = '\t\t\tconst text = m.type === "black" ? m.text : (m.blackAfter ?? "");\n\t\t\t// don\'t repeat the line already shown as the bundle heading\n'
new_dump = '\t\t\tconst text = m.type === "black" ? m.text : (String(m.blackAfter ?? "").trim() ? m.blackAfter : embeddedText(m));   // ROUND 342 — the bracket-line words of an element member\n\t\t\t// don\'t repeat the line already shown as the bundle heading\n'
assert cc.count(old_dump) == 1, cc.count(old_dump)
cc = cc.replace(old_dump, new_dump)
wr(CC, cc)

et = rd(ET)
old_et = '\t"interactive_placeholder": {\n\t\t"instructions_before": true,\n'
new_et = (
    '\t"interactive_placeholder": {\n'
    '\t\t"embedded_member_text": {\n'
    '\t\t\t"enabled": true,\n'
    '\t\t\t"env": "MEMBERTEXT_OFF",\n'
    '\t\t\t"directives": ["ELEMENT", "INLINE"],\n'
    '\t\t\t"_note": "ROUND 342 — a tag member whose words ride its OWN bracket line (\'[audio] while, whale, whirl, whole, whine\', \'[image] angry person\', \'[button] Go to journal\') is CONTENT for the un-built hand-off box: the empty-bundle / empty-box guards count it and the member dump renders the raw bracket line. Only members whose primary directive is listed here (content ELEMENTs and INLINE links — never an INTERACTIVE invocation, whose bracket text is its own spec and lives in the .txt) and whose span is a TAG (an instruction-class member already surfaces as the note before the box). Measured over the r341 corpus: 255 un-built bundles / 124 modules carry such a member (button 112, image 94, embed 56, audio button 12, external link 12, body 10, audio 9, video 9 …); 7 boxes were suppressed outright with the words lost from the page (BLL150 / BLL166 audio word lists, ENGC101 4.0 five [image] faces, MXEO201 4.0 [h3], XWHA02, EXPFUN04, HIS1001). Env MEMBERTEXT_OFF reverts both guards and the dump."\n'
    '\t\t},\n'
    '\t\t"instructions_before": true,\n'
)
assert et.count(old_et) == 1, et.count(old_et)
et = et.replace(old_et, new_et)
wr(ET, et)
print("patched", CC, ET)
