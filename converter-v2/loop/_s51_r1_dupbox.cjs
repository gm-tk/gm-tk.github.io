/** _s51_r1_dupbox.cjs — session 51 Round 1 PICK: with the r369 de-dupe OFF (run with NUMNORM_OFF=1), every pair of
 *  activity boxes on a page that carry the SAME writer id — the writer's one activity rendered as two boxes (the
 *  de-dupe then shifts every later id on the page). Prints, per pair: the classes of the containers BETWEEN the first
 *  box's end and the second box's start (a side column, an alert, a heading …) and the second box's opening text.
 *  In memory, no disk writes. Run from reference/tests/ under WSL:
 *    NUMNORM_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s51_r1_dupbox.cjs CODES…
 *  Output: DUP \t code \t file \t id \t between-classes \t second-box text \t the first box's last text */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const strip = (h, n) => String(h).replace(/<script[\s\S]*?<\/script>/g, " ").replace(/<[^>]+>/g, " ").replace(/&[a-z#0-9]+;/gi, " ").replace(/\s+/g, " ").trim().slice(0, n);
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	for (const code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		const run = new ConversionRun({ imageMode: "P" });
		const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
		const docs = [];
		for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(base, name));
			docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
		}
		const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
		const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
		if (!prep.ok) continue;
		try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}\tASSEMBLE ERROR`); continue; }
		for (const o of run.outputs ?? []) {
			if (!/\.html$/.test(o.filename)) continue;
			const html = String(o.content);
			const re = /<div class="((?:[^"]*\s)?activity(?:\s[^"]*)?)"[^>]*? number="([^"]*)"/g;
			const hits = []; let m;
			while ((m = re.exec(html)) !== null) hits.push({ at: m.index, cls: m[1], id: m[2] });
			for (let i = 1; i < hits.length; i++) {
				if (hits[i].id !== hits[i - 1].id) continue;
				// the gap: from the first box's LAST text to the second box's start — list the container classes opened in it
				const seg = html.slice(hits[i - 1].at, hits[i].at);
				const tailText = strip(seg, 100000).slice(-90);
				// the containers opened after the first box closed: take the last 2500 chars before box 2 for class tokens
				const gap = seg.slice(-2500);
				const cls = [...gap.matchAll(/<(div|h[1-6]|p|ul|ol|img|table|audio|iframe)\b[^>]*?(?:class="([^"]*)")?[^>]*>/g)]
					.map((x) => x[1] + (x[2] ? "." + x[2].split(/\s+/).filter((c) => !/^col-|^row$|^offset/.test(c)).join(".") : ""))
					.filter((x) => !/^div$/.test(x)).slice(-8).join(" ");
				const second = strip(html.slice(hits[i].at, hits[i].at + 1500), 110);
				const first = strip(html.slice(hits[i - 1].at, hits[i - 1].at + 1500), 110);
				_l(`DUP\t${code}\t${o.filename}\t${hits[i].id}\t${hits[i - 1].cls}|${hits[i].cls}\t${cls}\t${second}\t${first}\t${tailText}`);
			}
		}
	}
}
main();
