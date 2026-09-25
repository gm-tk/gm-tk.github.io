/** _s51_r1_dropbox.cjs — session 51 Round 1 PICK: every bundle whose opener names a DROPBOX; for every bundle InteractiveScanner.ScanPage returns on the given
 *  modules, print the page items from startIndex-2 to startIndex+4 (type / block / text / blackAfter) and mark which
 *  ones are inside [startIndex, endIndex). DUMP_TYPE filters by bundle type (default all); DUMP_IDX filters by the
 *  bundle's page-local order. In memory, no disk writes. Run from reference/tests/ under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s51_r1_itemdump.cjs BLL247
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const TYPE = process.env.DUMP_TYPE || "";
const W = +(process.env.DUMP_AFTER || 4);
const clip = (s, n = 110) => JSON.stringify(String(s ?? "").replace(/\s+/g, " ").slice(0, n));
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	let code = "";
	const orig = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) {
		const out = orig(page, normaliser, run);
		const items = page.items ?? [];
		for (const b of out ?? []) {
			const op = (b.memberItems ?? [])[0] ?? items[b.startIndex]; const opt = String(op?.text ?? "");
			if (!/dropbox/i.test(opt)) continue;
			_l(`DBX	${code}	${b.type}	${b.endIndex - b.startIndex}	${clip(opt, 70)}	${JSON.stringify(op?.parse?.tags?.map?.((t) => t.tag ?? t) ?? [])}`);
			if (!process.env.DUMP_FULL) continue;
			_l(`--- ${code} ${b.type} [${b.startIndex},${b.endIndex}) act=${b.activityId ?? "-"} head=${clip(b.headingText, 60)} owner=${b.activityOwner ? clip(b.activityOwner.text, 40) : "-"}`);
			_l(`  openers: ${(b.openerItems ?? []).map((m) => m.type + ":" + clip(m.text, 40)).join(" | ")}`);
			_l(`  members0-3: ${(b.memberItems ?? []).slice(0, 4).map((m) => m.type + ":" + clip(m.text, 40)).join(" | ")}`);
			for (let k = Math.max(0, b.startIndex - 2); k < Math.min(items.length, b.startIndex + W); k++) {
				const it = items[k]; const inB = k >= b.startIndex && k < b.endIndex ? "IN " : "   ";
				_l(`  ${inB}${k} ${it.type} blk=${it.block?.id ?? it.blockIndex ?? (it.block ? "obj" : "-")} tags=${JSON.stringify(it.parse?.tags?.map?.((t) => t.tag ?? t) ?? [])} cls=${it.parse?.class ?? "-"} text=${clip(it.text)} after=${clip(it.blackAfter, 60)}`);
			}
		}
		return out;
	};
	for (code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
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
		if (!prep.ok) { _l(`${code}\tPREP FAIL`); continue; }
		try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}\tASSEMBLE ERROR ${e.message}`); }
	}
}
main();
