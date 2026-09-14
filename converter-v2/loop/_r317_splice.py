"""ROUND 317 splice (loop Round 4) — KB constraints 45 + 90: the acknowledgements block's template form.
Anchored, unique-match edits in bytes mode (LF files; Acks_Formats.json is SPACE-indented, AcksBuilder.js tab-indented).
Idempotent (prefix test for inserts that end/start with their anchor)."""
ROOT = r"C:/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/"
AB = ROOT + "app/js/AcksBuilder.js"
AF = ROOT + "data/Acks_Formats.json"

def edit(path, pairs):
    b = open(path, "rb").read()
    for old, new in pairs:
        o = old.encode("utf-8"); n = new.encode("utf-8")
        ins = n[:-len(o)] if n.endswith(o) else (n[len(o):] if n.startswith(o) else n)
        if b.count(ins) == 1 and (n.endswith(o) or n.startswith(o) or b.count(o) == 0):
            print("already applied:", path.split("/")[-1], old[:40].strip()); continue
        cnt = b.count(o)
        assert cnt == 1, f"{path}: anchor count {cnt} != 1 for anchor starting {old[:60]!r}"
        b = b.replace(o, n)
    open(path, "wb").write(b)
    print("edited", path.split("/")[-1], len(pairs), "edit(s)")

# ---------------------------------------------------------------- data block (standing_items, before template_variant_omit)
DATA_OLD = '  "template_variant_omit": {\n   "enabled": true,\n'
DATA_NEW = ('  "kb_template_form": {\n'
 '   "enabled": true,\n'
 '   "env": "ACKSTEMPLATE_OFF",\n'
 '   "acks_class_standard": "acks acksTemplate",\n'
 '   "omit_always": true,\n'
 '   "rule": "ROUND 317 (the autonomous loop\'s Round 4, 2026-09-15 \\u2014 KB constraints 45 + 90; CL-0090 is a LOCKED admin decision, reported by the Design Team Lead 27 Aug 2026 with WJFUN105_0.0 as the example). The acknowledgements wrapper is `acks acksTemplate` on EVERY module (plus `acksAI` where the module has AI media \\u2014 the round-241 variant, unchanged), and the template classes GENERATE the apology, the Copyright \\u00a9 <span class=currentYear> line and the AI statement \\u2014 typing them as well produces a visible double-up on the published page. Only the catch-all line (All other images \\u00a9 \\u2026) is still typed, as an unlabelled acksLesson div after the media entries. THE CHANGE: the standard container class comes from acks_class_standard here (the legacy `acks` in container.acks_class_standard is kept for the OFF state), and the round-241 template_variant_omit list applies ALWAYS (omit_always), not only on the AI variant. MEASURED (outputs/_measure_r317_acks.py, the KB form simulated on every paired acks page and scored with the skeleton gate\'s own scorer): Claude shipped the pre-rule form on 394 overview pages (bare `acks`, apology + copyright typed) vs the KB form on the 19 AI-variant pages; the gold is the OLD convention (bare `acks` typed on 421 blocks, template-class 74) \\u2014 under the loop\'s order of authority (\\u00a71b) the KB outranks the gold because the gold predates the rule: a NAMED KB-over-gold override. Expected skeleton delta pp-sum \\u221246.05 = corpus mean \\u22120.024pp (88 pages down \\u2248 0.5pp each where the gold overview carries the old bare block, 12 up where it carries `acks acksTemplate`, 287 zero \\u2014 249 gold overviews have no acks block at all, the gold\'s old LAST-PAGE placement that constraint 33 rejects), judged net of the named pages per Subject_Global_Parameters._meta.gold_override_policy (b). Env toggle ACKSTEMPLATE_OFF reverts both the class and the always-omit to the round-316 form byte-for-byte; ACKSBOILER_OFF still reverts the omit list alone."\n'
 '  },\n'
 + DATA_OLD)

# ---------------------------------------------------------------- AcksBuilder (a) the container class
AB_A_OLD = ('\t\thtml.push(Utils.FillTemplate(fmt.container.wrapper_open, {\n'
 '\t\t\tacksClass: hasAi ? fmt.container.acks_class_ai_variant : fmt.container.acks_class_standard,\n'
 '\t\t}));\n')
AB_A_NEW = ('\t\t// ROUND 317 (loop Round 4 \u2014 KB constraints 45 + 90, CL-0090 locked). The wrapper is\n'
 '\t\t// `acks acksTemplate` on EVERY module and the template classes generate the\n'
 '\t\t// apology / copyright / AI statements, so the round-241 omit applies always \u2014\n'
 '\t\t// the gold\'s bare `acks` + typed statements is the pre-rule form the KB outranks\n'
 '\t\t// (a named override, measured -0.024pp). Data standing_items.kb_template_form;\n'
 '\t\t// env ACKSTEMPLATE_OFF (the AI variant and ACKSBOILER_OFF are unchanged).\n'
 '\t\tconst ktf = fmt.standing_items.kb_template_form;\n'
 '\t\tconst ktfOn = !!ktf && ktf.enabled !== false\n'
 '\t\t\t&& !(typeof process !== "undefined" && process.env && process.env[ktf.env ?? "ACKSTEMPLATE_OFF"]);\n'
 '\t\thtml.push(Utils.FillTemplate(fmt.container.wrapper_open, {\n'
 '\t\t\tacksClass: hasAi ? fmt.container.acks_class_ai_variant\n'
 '\t\t\t\t: (ktfOn && ktf.acks_class_standard) ? ktf.acks_class_standard : fmt.container.acks_class_standard,\n'
 '\t\t}));\n')

# ---------------------------------------------------------------- AcksBuilder (b) the omit condition
AB_B_OLD = ('\t\tconst omitList = (hasAi && tvo && tvo.enabled !== false\n')
AB_B_NEW = ('\t\tconst omitList = ((hasAi || (ktfOn && ktf.omit_always !== false)) && tvo && tvo.enabled !== false\n')

edit(AF, [(DATA_OLD, DATA_NEW)])
edit(AB, [(AB_A_OLD, AB_A_NEW), (AB_B_OLD, AB_B_NEW)])
print("done")
