#!/usr/bin/env python3
"""Session 26 Round 1 (engine r387) — the whakatauki does not close its column.
Splices ContentConverter.js: (1) a private static helper #flowsAfter(tag, run) reading
callouts.flow_after_tags (data + env WHFLOW_OFF + template / subject scope); (2) the two after-box
breakRow() sites consult it. LF preserved (io.open newline=""). Idempotent: refuses to re-apply."""
import io, sys
P = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/app/js/ContentConverter.js"
s = io.open(P, encoding="utf-8", newline="").read()
if "#flowsAfter(" in s:
    print("already applied"); sys.exit(0)

# (1) the helper, inserted directly above #calloutOpen
anchor = "\tstatic #calloutOpen(it, bodyItems, i, stack, run, spans, wrapStructured = false) {\n"
assert s.count(anchor) == 1, s.count(anchor)
helper = (
"\t// ROUND 387 (the autonomous loop's session 26 Round 1) — a callout that does NOT close its\n"
"\t// column. The r51 `row_breaks.after` rule closes the section row after every boxed callout;\n"
"\t// measured on today's corpus (outputs/_s26_after2.py) that is the gold's own form for every\n"
"\t// box but the whakataukī, whose commentary paragraph flows on INSIDE the same col-md-8 (gold\n"
"\t// 0.70 over 81 Standard boxes; paired to the very next text 0.81 on 35 pages / 35 modules).\n"
"\t// The break BEFORE the box stands (gold FIRST-in-column 0.78). Data\n"
"\t// callouts.flow_after_tags {enabled, env, tags, templates, exclude_subjects}: a listed tag\n"
"\t// skips the after-box breakRow when the module's Module_Structure_Index template_type is\n"
"\t// listed (an unknown module keeps the r51 break) and its subject is not excluded (NCEA1 —\n"
"\t// the HIS 'The whakataukī chosen for this module…' paragraph opens a gold row). Env\n"
"\t// WHFLOW_OFF = the r386 output.\n"
"\tstatic #flowsAfter(tag, run) {\n"
"\t\tconst cfg = DataService.Data.EmitTemplates?.callouts?.flow_after_tags;\n"
"\t\tif (!cfg || cfg.enabled === false) return false;\n"
"\t\tif (typeof process !== \"undefined\" && process.env && process.env[cfg.env ?? \"WHFLOW_OFF\"]) return false;\n"
"\t\tif (!(cfg.tags ?? []).some((t) => String(t) === String(tag))) return false;\n"
"\t\tconst meta = DataService.Data.ModuleStructureIndex?.module_meta?.[String(run?.moduleCode || \"\")];\n"
"\t\tif (!meta) return false;\n"
"\t\tif ((cfg.templates ?? []).length && !(cfg.templates ?? []).some((t) => String(t) === String(meta.template_type ?? \"\"))) return false;\n"
"\t\tif ((cfg.exclude_subjects ?? []).some((sub) => String(sub) === String(meta.subject ?? \"\"))) return false;\n"
"\t\treturn true;\n"
"\t}\n\n"
)
s = s.replace(anchor, helper + anchor, 1)

# (2a) the strict (non-spanning) box: fresh row next — unless the tag flows after
old_a = "\t\t\t\t\t\tif (!flowingCallout && !stack.length) breakRow();\n"
new_a = ("\t\t\t\t\t\t// ROUND 387: a flow_after_tags box (the whakataukī) keeps its column open — #flowsAfter\n"
         "\t\t\t\t\t\tif (!flowingCallout && !stack.length && !this.#flowsAfter(primary.tag, run)) breakRow();\n")
assert s.count(old_a) == 1, s.count(old_a)
s = s.replace(old_a, new_a, 1)

# (2b) the CONTAINER_CLOSE of a spanning box
old_b = ("\t\t\t\t\t\tif (!stack.length && rowCfg.after.includes(\n"
         "\t\t\t\t\t\t\ttop.tag === \"activity\" ? \"activity_close\" : \"callout_close\")) breakRow();\n")
new_b = ("\t\t\t\t\t\t// ROUND 387: a flow_after_tags box (the whakataukī) keeps its column open — #flowsAfter\n"
         "\t\t\t\t\t\tif (!stack.length && !this.#flowsAfter(top.tag, run) && rowCfg.after.includes(\n"
         "\t\t\t\t\t\t\ttop.tag === \"activity\" ? \"activity_close\" : \"callout_close\")) breakRow();\n")
assert s.count(old_b) == 1, s.count(old_b)
s = s.replace(old_b, new_b, 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("applied")
