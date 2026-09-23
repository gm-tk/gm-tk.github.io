// one-off: switch the recorder's hook from the defaulting line to the final green-button emission (records only defaulted labels that SHIP)
const fs = require("fs"); const p = process.argv[2]; let s = fs.readFileSync(p, "utf8");
s = s.replace('const LINE = "if (!label) { label = keyDefaultOn ? btn.label_default : tpl.buttons.journal_label_default; labelDefaulted = true; }";',
  'const LINE = "label = this.#buttonCanonicalLabel(label, key, run, tpl);";');
s = s.replace('const rec = "if (!label && !(keyDefaultOn)) { (globalThis.__jd', 'const rec = "if (labelDefaulted) { (globalThis.__jd');
s = s.replace('nextType: bodyItems?.[i + 1]?.type ?? \\"\\", page:', 'nextType: bodyItems?.[i + 1]?.type ?? \\"\\", label, url, form: String(form).slice(0, 40), page:');
s = s.replace("const patched = src.replace(LINE, rec + LINE);", "const patched = src.replace(LINE, LINE + \" \" + rec);");
s = s.replace("_l(`JDEF\t${code}\t${r.page}\t${r.key}\t${clip(r.text)}", "_l(`JDEF\t${code}\t${r.page}\t${clip(r.label)}|${r.url ? \"URL\" : \"-\"}|${clip(r.form)}\t${clip(r.text)}");
fs.writeFileSync(p, s);
