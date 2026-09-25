/** _s46_r6_blackimg.cjs — session 46 Round 6: every page item that is BLACK text opening with an image bracket (`[Image …]`,
 *  `[image] …`, `[Insert image …]`) — the writer's image request typed in black, invisible to the red-tag detector. Records the
 *  text, whether it carries a URL, whether a scanned bundle consumed it, and the next item. Sharded; --merge N → _s46_r6_blackimg.json. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const NAME = process.env.BL_NAME || "_s46_r6_blackimg"; const SHARD = (k) => path.join(OUT, `${NAME}_shard${k}.json`);
if (process.argv.includes("--merge")) {
	const n = parseInt(arg("--merge", "8"), 10); const all = [];
	for (let k = 0; k < n; k++) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8")));
	fs.writeFileSync(path.join(OUT, `${NAME}.json`), JSON.stringify(all)); console.log(`${all.length} records`); process.exit(0);
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const RE = process.env.BL_RE === "head" ? /^\s*\[\s*(?:heading\s*)?h[1-6]\s*[\]}]/i : /^\s*\[\s*(?:insert\s+(?:an?\s+)?)?(?:image|photo|picture)\b/i;
function moduleDirs() {
	const out = [];
	for (const tmpl of fs.readdirSync(GOLD)) {
		const tp = path.join(GOLD, tmpl); if (!fs.statSync(tp).isDirectory()) continue;
		for (const code of fs.readdirSync(tp)) { const cp = path.join(tp, code); if (fs.statSync(cp).isDirectory()) out.push({ code, dir: cp }); }
	}
	return out.sort((a, b) => a.code.localeCompare(b.code));
}
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const recs = []; let curMod = "?"; const pend = [];
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) {
		const res = origScan(page, n, run);
		const label = String(page?.lessonLabel ?? page?.label ?? "?");
		(page.items ?? []).forEach((it, i) => {
			if (it?.type !== "black") return;
			for (const line of String(it.text ?? "").split("\n")) {
				if (!RE.test(line)) continue;
				const nx = page.items[i + 1];
				pend.push({ code: curMod, page: label, text: line.replace(/\s+/g, " ").slice(0, 140), url: /https?:\/\//.test(line),
					consumed: it.consumedBy !== undefined, lines: String(it.text).split("\n").length,
					next: nx ? `${nx.type}${nx.type === "tag" ? ":" + (nx.parse?.primary?.tag ?? nx.parse?.class) : ""}` : "(end)" });
			}
		});
		return res;
	};
	const dirs = moduleDirs(); const si = process.argv.indexOf("--shard");
	let list = dirs, k = 0;
	if (si > -1) { k = parseInt(process.argv[si + 1], 10); const n = parseInt(process.argv[si + 2], 10); list = dirs.filter((_, i) => i % n === k); }
	for (const d of list) {
		curMod = d.code;
		try {
			const run = new ConversionRun({ imageMode: "P" }); const docs = [];
			for (const name of fs.readdirSync(d.dir).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
				const buf = fs.readFileSync(path.join(d.dir, name));
				docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
			}
			const istockAcksFiles = fs.readdirSync(d.dir).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(d.dir, f), "utf8") }));
			const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
			if (!prep.ok) continue;
			await PageAssembler.AssembleModule(run, norm);
		} catch (e) { /* keep scanning */ }
		recs.push(...pend.splice(0));
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "records");
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
