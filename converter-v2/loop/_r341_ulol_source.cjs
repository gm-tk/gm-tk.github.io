/** _r341_ulol_source.cjs — for each `ul ⇐ ol` site (from _r341_ulol_sites.py output on stdin: "CODE claudePage goldPage nth"), find the
 *  Claude <ol>'s first item text in the module's WT blocks and report the block's Word list kind (bullet / number / none = typed). */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const OUT = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const norm = (s) => String(s ?? "").replace(/<[^>]+>/g, "").replace(/&[a-z#0-9]+;/g, " ").replace(/[*_]/g, "").replace(/\s+/g, " ").trim().toLowerCase();
async function main() {
  globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
  const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
  eng.loadEngine();
  const lines = fs.readFileSync(0, "utf8").split(/\r?\n/).filter((l) => /^[A-Z]+\d+ /.test(l));
  const byCode = new Map();
  for (const l of lines) { const [code, cp, hp, nth] = l.trim().split(/\s+/); if (!byCode.has(code)) byCode.set(code, []); byCode.get(code).push({ cp, hp, nth: +nth }); }
  const tally = {};
  for (const [code, sites] of byCode) {
    const base = corpus.mdir(MODS, code); const blocks = [];
    for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
      const buf = fs.readFileSync(path.join(base, name));
      const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
      const doc = await DocxExtractor.Extract(zip); for (const b of (doc.blocks ?? [])) blocks.push(b);
    }
    for (const s of sites) {
      const html = fs.readFileSync(path.join(corpus.mdir(OUT, code), s.cp), "utf8");
      const ols = [...html.matchAll(/<ol[^>]*>([\s\S]*?)<\/ol>/g)];
      const ol = ols[s.nth]; if (!ol) { _l(`${code} ${s.cp} ol#${s.nth}: NOT FOUND (${ols.length} ols)`); continue; }
      const lis = [...ol[1].matchAll(/<li>([\s\S]*?)<\/li>/g)].map((m) => norm(m[1]));
      const first = lis[0] ?? ""; const key = first.slice(0, 40);
      const hit = blocks.find((b) => norm(b.text).replace(/^\d+[.)]\s*/, "").startsWith(key.slice(0, 30)) || norm(b.text).includes(key.slice(0, 30)));
      const typed = hit ? /^\s*\d+[.)]\s/.test(String(hit.text)) : false;
      const kind = hit ? (hit.list ?? "none") : "??";
      const cls = hit ? (kind === "number" ? "WORD-NUMBERED" : typed ? "TYPED-DIGITS" : kind === "bullet" ? "WORD-BULLET" : "PLAIN") : "NO-WT-MATCH";
      tally[cls] = (tally[cls] ?? 0) + 1;
      // the gold's form for the same text
      const gold = fs.readFileSync(path.join(base, s.hp), "utf8");
      const gk = key.slice(0, 25); let gform = "absent";
      for (const m of gold.matchAll(/<(ul|ol)[^>]*>([\s\S]*?)<\/\1>/g)) if (norm(m[2]).includes(gk)) { gform = m[1]; break; }
      if (gform === "absent" && norm(gold).includes(gk)) gform = "not-a-list";
      _l(`${code} ${s.cp} ol#${s.nth} n=${lis.length} ${cls} bold=${hit ? /^\*\*/.test(String(hit.text).trim()) : "?"} gold=${gform} | ${first.slice(0, 60)}`);
    }
  }
  _l("TALLY", JSON.stringify(tally));
}
main().catch((e) => { process.stdout.write("ERR " + (e && e.stack || e) + "\n"); });
