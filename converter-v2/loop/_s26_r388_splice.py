#!/usr/bin/env python3
"""Session 26 Round 2 (engine r388) — the alert box does not close its column either.
Splices ContentConverter.js: #flowsAfter reads callouts.flow_after_tags.rules (each with its own tags / templates /
exclude_subjects / exclude_class_match) and takes the box's open tag; the strict site passes the emitted open tag,
the span push records `boxOpen` and the CONTAINER_CLOSE site passes it. LF preserved. Idempotent."""
import io, sys, re
P = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/app/js/ContentConverter.js"
s = io.open(P, encoding="utf-8", newline="").read()
if "flow_after_tags.rules" in s:
    print("already applied"); sys.exit(0)

# (1) the helper body: rules + boxOpen
old_h = s[s.index("\tstatic #flowsAfter(tag, run) {\n"):]
old_h = old_h[:old_h.index("\t}\n\n") + len("\t}\n\n")]
new_h = (
"\tstatic #flowsAfter(tag, run, boxOpen = \"\") {\n"
"\t\t// ROUND 388: `rules` — each rule its own tags / templates / exclude_subjects / exclude_class_match (the\n"
"\t\t// class test runs on the box's own emitted open tag, e.g. the `top` modifier); one env for the family.\n"
"\t\tconst cfg = DataService.Data.EmitTemplates?.callouts?.flow_after_tags;\n"
"\t\tif (!cfg || cfg.enabled === false) return false;\n"
"\t\tif (typeof process !== \"undefined\" && process.env && process.env[cfg.env ?? \"WHFLOW_OFF\"]) return false;\n"
"\t\tconst meta = DataService.Data.ModuleStructureIndex?.module_meta?.[String(run?.moduleCode || \"\")];\n"
"\t\tif (!meta) return false;\n"
"\t\tconst rules = Array.isArray(cfg.rules) ? cfg.rules : [cfg];   // r387 shape = one rule at the top level\n"
"\t\tfor (const rule of rules) {\n"
"\t\t\tif (!(rule.tags ?? []).some((t) => String(t) === String(tag))) continue;\n"
"\t\t\tif ((rule.templates ?? []).length && !(rule.templates ?? []).some((t) => String(t) === String(meta.template_type ?? \"\"))) continue;\n"
"\t\t\tif ((rule.exclude_subjects ?? []).some((sub) => String(sub) === String(meta.subject ?? \"\"))) continue;\n"
"\t\t\tif (rule.exclude_class_match) {\n"
"\t\t\t\tconst m = String(boxOpen || \"\").match(/^\\s*<div class=\"([^\"]*)\"/);\n"
"\t\t\t\tif (m && new RegExp(rule.exclude_class_match).test(m[1])) continue;\n"
"\t\t\t}\n"
"\t\t\treturn true;\n"
"\t\t}\n"
"\t\treturn false;\n"
"\t}\n\n"
)
assert s.count(old_h) == 1
s = s.replace(old_h, new_h, 1)

# (2a) the strict site: pass the emitted open tag (the first part that opens a div)
old_a = ("\t\t\t\t\temit(...this.#calloutOpen(it, bodyItems, i, stack, run, spans, wrapStructured));\n"
         "\t\t\t\t\tif (!spans) {\n")
new_a = ("\t\t\t\t\tconst _r387Parts = this.#calloutOpen(it, bodyItems, i, stack, run, spans, wrapStructured);\n"
         "\t\t\t\t\tconst _r388BoxOpen = _r387Parts.find((p) => typeof p === \"string\" && /^\\s*<div class=\"/.test(p)) ?? \"\";\n"
         "\t\t\t\t\temit(..._r387Parts);\n"
         "\t\t\t\t\tif (!spans) {\n")
assert s.count(old_a) == 1, s.count(old_a)
s = s.replace(old_a, new_a, 1)
old_a2 = "\t\t\t\t\t\tif (!flowingCallout && !stack.length && !this.#flowsAfter(primary.tag, run)) breakRow();\n"
new_a2 = "\t\t\t\t\t\tif (!flowingCallout && !stack.length && !this.#flowsAfter(primary.tag, run, _r388BoxOpen)) breakRow();\n"
assert s.count(old_a2) == 1
s = s.replace(old_a2, new_a2, 1)

# (2b) the span push records the box's open tag; the CONTAINER_CLOSE site passes it
old_p = ("\t\t\tstack.push({ tag, close: closeHtml,\n"
         "\t\t\t\tmode: wrapStructured ? \"span-wrap\" : \"span\", hasContent: out.length > 1,\n"
         "\t\t\t\twrapOpen: wrap ? wrap.open : null, wrapClose: wrap ? wrap.close : null });\n")
new_p = ("\t\t\tstack.push({ tag, close: closeHtml,\n"
         "\t\t\t\tmode: wrapStructured ? \"span-wrap\" : \"span\", hasContent: out.length > 1,\n"
         "\t\t\t\twrapOpen: wrap ? wrap.open : null, wrapClose: wrap ? wrap.close : null,\n"
         "\t\t\t\tboxOpen: out.find((p) => typeof p === \"string\" && /^\\s*<div class=\"/.test(p)) ?? \"\" });   // ROUND 388: for #flowsAfter's class test\n")
assert s.count(old_p) == 1, s.count(old_p)
s = s.replace(old_p, new_p, 1)
old_c = "\t\t\t\t\t\tif (!stack.length && !this.#flowsAfter(top.tag, run) && rowCfg.after.includes(\n"
new_c = "\t\t\t\t\t\tif (!stack.length && !this.#flowsAfter(top.tag, run, top.boxOpen) && rowCfg.after.includes(\n"
assert s.count(old_c) == 1
s = s.replace(old_c, new_c, 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("applied")
