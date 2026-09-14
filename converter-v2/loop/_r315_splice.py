"""ROUND 315 splice (loop Round 2) — KB constraint 28: lowercase doctype + XHTML self-closing voids.
Anchored, unique-match edits in bytes mode (LF files, tabs preserved). Idempotent: re-running is a no-op."""
ROOT = r"C:/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/"
HF = ROOT + "app/js/HtmlFormatter.js"
ET = ROOT + "data/Emit_Templates.json"

def edit(path, pairs):
    b = open(path, "rb").read()
    for old, new in pairs:
        o = old.encode("utf-8"); n = new.encode("utf-8")
        ins = n[:-len(o)] if n.endswith(o) else n   # the inserted block (a new that ends with its anchor)
        if b.count(ins) == 1 and (n.endswith(o) or b.count(o) == 0):
            print("already applied:", path, old[:50].strip()); continue
        cnt = b.count(o)
        assert cnt == 1, f"{path}: anchor count {cnt} != 1 for anchor starting {old[:60]!r}"
        b = b.replace(o, n)
    open(path, "wb").write(b)
    print("edited", path, len(pairs), "edit(s)")

# ---------------------------------------------------------------- data block (inside "formatter")
DATA_OLD = '\t\t"block_line_breaks": {\n\t\t\t"enabled": true,\n\t\t\t"tags": [\n\t\t\t\t"div",\n'
DATA_NEW = ('\t\t"xhtml_voids": {\n'
 '\t\t\t"enabled": true,\n'
 '\t\t\t"env": "XHTMLVOID_OFF",\n'
 '\t\t\t"doctype": "<!doctype html>",\n'
 '\t\t\t"void_tags": [\n'
 '\t\t\t\t"img",\n\t\t\t\t"br",\n\t\t\t\t"meta",\n\t\t\t\t"link",\n\t\t\t\t"hr",\n\t\t\t\t"input",\n\t\t\t\t"source",\n'
 '\t\t\t\t"wbr",\n\t\t\t\t"area",\n\t\t\t\t"base",\n\t\t\t\t"col",\n\t\t\t\t"embed",\n\t\t\t\t"track"\n'
 '\t\t\t],\n'
 '\t\t\t"close": " />",\n'
 '\t\t\t"_round315_note": "ROUND 315 (the autonomous loop\'s Round 2, 2026-09-15 \\u2014 KB constraint 28 + 01A_TEMPLATE_LEVELS_CORE \'Void element self-closing syntax\' / \'DOCTYPE casing\' + the 02C checklist). The KB\'s output spec is a lowercase <!doctype html> and XHTML-style self-closing void elements (<meta charset=\\"utf-8\\" />, <img ... />, <br />). Claude shipped <!DOCTYPE html> on 2102/2102 pages and 0 self-closing body voids (11992 <img>, 2930 <br>); the head\'s <meta> tags were already in the KB form. MEASURED (gold, every page): the two halves are ONE style \\u2014 the 572 lowercase-doctype gold pages self-close \' />\' 10371 : \'/>\' 552 : \'>\' 2519 (77%; img 80%, meta 99%, br 53%), the 1810 uppercase-doctype pages self-close 1% \\u2014 so the gold MAJORITY does NOT follow the rule; under the loop\'s order of authority (LOOP__Autonomous_Rounds.md \\u00a71b) the KB outranks the gold because the gold predates the rule: an INTENTIONAL OVERRIDE, gate-neutral (every protected gate parses through html.parser, where <img ... /> and <img ...> are the same node; the doctype and <html> are outside the skeleton). THE RULE: HtmlFormatter.Indent\'s final pass rewrites the doctype line to `doctype` and normalises every void open tag\'s tail to `close` (attribute-aware: quoted attribute values may hold \'>\' or \'/\'); idempotent on tags already in the form. Env toggle XHTMLVOID_OFF reverts to the round-314 form byte-for-byte. Full corpus regeneration (a shell change is corpus-wide by construction)."\n'
 '\t\t},\n'
 + DATA_OLD)
edit(ET, [(DATA_OLD, DATA_NEW)])

# ---------------------------------------------------------------- HtmlFormatter: the pass + the hook
HF_A_OLD = ('\t/**\n'
 '\t * Round 243 (E4): splits glued block-tag boundaries in one emitter line.\n')
HF_A_NEW = ('\t/**\n'
 '\t * ROUND 315 (loop Round 2 \u2014 KB constraint 28): the XHTML void pass, or null\n'
 '\t * when off (data flag disabled, env XHTMLVOID_OFF, or no data). Returns\n'
 '\t * { doctype, re, close }: `re` matches one void open tag attribute-aware (a\n'
 '\t * quoted value may hold \'>\' or \'/\'), capturing the name and the attribute\n'
 '\t * run WITHOUT any trailing whitespace or slash, so the tail can be rewritten\n'
 '\t * to `close` (" />") whatever form it arrived in \u2014 `<img a="b">`, `<img a="b"/>`\n'
 '\t * and `<img a="b" />` all become `<img a="b" />` (idempotent).\n'
 '\t */\n'
 '\tstatic #voidPass() {\n'
 '\t\tif (typeof process !== "undefined" && process.env && process.env.XHTMLVOID_OFF) return null;\n'
 '\t\ttry {\n'
 '\t\t\tconst cfg = DataService.Data.EmitTemplates.formatter?.xhtml_voids;\n'
 '\t\t\tif (!cfg || !cfg.enabled || !Array.isArray(cfg.void_tags) || !cfg.void_tags.length) return null;\n'
 '\t\t\tif (cfg.env && typeof process !== "undefined" && process.env && process.env[cfg.env]) return null;\n'
 '\t\t\tconst names = cfg.void_tags.map((t) => String(t).toLowerCase()).join("|");\n'
 '\t\t\t// name, then the attribute run: quoted values or any non-quote non-\'>\'\n'
 '\t\t\t// character, ending BEFORE optional whitespace + optional \'/\' + \'>\'\n'
 '\t\t\tconst re = new RegExp("<(" + names + ")(?=[\\\\s/>])((?:\\"[^\\"]*\\"|\'[^\']*\'|[^>\\"\'/]|/(?!\\\\s*>))*?)\\\\s*/?>", "gi");\n'
 '\t\t\treturn { doctype: cfg.doctype ?? null, re, close: cfg.close ?? " />" };\n'
 '\t\t} catch (e) { return null; }\n'
 '\t};\n'
 '\n'
 '\t/**\n'
 '\t * Round 315: applies the void pass to one line \u2014 the doctype line is\n'
 '\t * rewritten whole (case-insensitive match on `<!doctype html>`), every\n'
 '\t * void open tag gets the `close` tail.\n'
 '\t */\n'
 '\tstatic #xhtmlVoids(line, vp) {\n'
 '\t\tif (vp.doctype && /^<!doctype\\s+html\\s*>$/i.test(line)) return vp.doctype;\n'
 '\t\treturn line.replace(vp.re, (whole, name, attrs) => "<" + name + attrs.replace(/\\s+$/, "") + vp.close);\n'
 '\t};\n'
 '\n'
 '\t/**\n'
 '\t * Round 243 (E4): splits glued block-tag boundaries in one emitter line.\n')
HF_B_OLD = ('\t\tfor (const raw of html.split("\\n")) {\n'
 '\t\t\tconst line = raw.trim();\n'
 '\t\t\tif (!line) continue;   // emitter blank lines carry no meaning\n'
 '\n')
HF_B_NEW = ('\t\t// ROUND 315 (KB constraint 28): lowercase doctype + XHTML self-closing voids,\n'
 '\t\t// applied per line after the block breaking so every void tag is seen once.\n'
 '\t\tconst vp = HtmlFormatter.#voidPass();\n'
 '\n'
 '\t\tfor (const raw of html.split("\\n")) {\n'
 '\t\t\tlet line = raw.trim();\n'
 '\t\t\tif (!line) continue;   // emitter blank lines carry no meaning\n'
 '\t\t\tif (vp) line = HtmlFormatter.#xhtmlVoids(line, vp);\n'
 '\n')
edit(HF, [(HF_A_OLD, HF_A_NEW), (HF_B_OLD, HF_B_NEW)])
print("done")
