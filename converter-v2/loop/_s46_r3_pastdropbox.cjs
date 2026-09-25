/** _s46_r3_pastdropbox.cjs — session 46 Round 3: corpus-wide, every scanned bundle that holds a writer's "Upload to dropbox" [Button]
 *  member and captured MORE members after it — the capture running past the activity's own closing button. Records the bundle type,
 *  whether it built, and the members after the button. Sharded (through _s46_shardrun.sh); --merge N → _s46_r3_pastdropbox.json. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const NAME = "_s46_r3_pastdropbox"; const SHARD = (k) => path.join(OUT, `${NAME}_shard${k}.json`);
if (process.argv.includes("--merge")) {
	const n = parseInt(arg("--merge", "8"), 10); const all = [];
	for (let k = 0; k < n; k++) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8")));
	fs.writeFileSync(path.join(OUT, `${NAME}.json`), JSON.stringify(all)); console.log(`${all.length} records`); process.exit(0);
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const tagOf = (it) => it?.type === "tag" ? (it.parse?.primary?.tag ?? `(${it.parse?.class ?? "?"})`) : it?.type ?? "(end)";
const DROP = /upload\s+(?:it\s+|this\s+|your\s+\w+\s+)?to\s+(?:the\s+|your\s+)?drop\s*-?\s*box/i;
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
	const recs = []; let curMod = "?"; const built = new Map(); const pending = [];
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) { const out = origBuild(args); if (args?.bundle) built.set(args.bundle, out != null); return out; };
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) {
		const res = origScan(page, n, run);
		const label = String(page?.lessonLabel ?? page?.label ?? "?");
		for (const b of (Array.isArray(res) ? res : (res?.bundles ?? []))) {
			const mem = b?.memberItems ?? [];
			const bi = mem.findIndex((m) => tagOf(m) === "button" && DROP.test(`${m.text ?? ""} ${m.blackAfter ?? ""}`));
			if (bi < 0 || bi === mem.length - 1) continue;
			const after = mem.slice(bi + 1);
			pending.push({ b, rec: { code: curMod, page: label, type: b.type, after: after.length,
				afterTags: after.map(tagOf).slice(0, 8), afterText: after.map((m) => String(m.blackAfter ?? m.text ?? "").replace(/\s+/g, " ").slice(0, 60)).slice(0, 3),
				term: tagOf(page.items[b.endIndex]) } });
		}
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
		for (const p of pending.splice(0)) recs.push({ ...p.rec, built: built.get(p.b) ?? null });
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "records");
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e)); process.exit(1); });
