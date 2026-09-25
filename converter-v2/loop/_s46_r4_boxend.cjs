/** _s46_r4_boxend.cjs — session 46 Round 4: for every gold-FREE text block Claude ships inside a hand-off box (_s46_r3_swallow.json),
 *  find the scanned bundle member that carries it and report WHAT the capture ran past: the member's own tag, the members before it
 *  (the widget's real content end), the bundle type and whether it built. Sharded (through _s46_shardrun.sh) over the modules in the
 *  list; --merge N → _s46_r4_boxend.json. Diagnostic only. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const NAME = "_s46_r4_boxend"; const SHARD = (k) => path.join(OUT, `${NAME}_shard${k}.json`);
if (process.argv.includes("--merge")) {
	const n = parseInt(arg("--merge", "8"), 10); const all = [];
	for (let k = 0; k < n; k++) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8")));
	fs.writeFileSync(path.join(OUT, `${NAME}.json`), JSON.stringify(all)); console.log(`${all.length} records`); process.exit(0);
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const fold = (s) => String(s ?? "").normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase()
	.replace(/[‘’“”'"*]/g, "").replace(/[^\p{L}\p{N}\s]/gu, " ").replace(/\s+/g, " ").trim();
const tagOf = (it) => it?.type === "tag" ? (it.parse?.primary?.tag ?? `(${it.parse?.class ?? "?"})`) : it?.type ?? "(end)";
const memText = (m) => m?.type === "table" ? (m.block?.rows ?? []).flat().map((c) => typeof c === "string" ? c : c?.text ?? "").join(" ")
	: `${m?.text ?? ""} ${m?.blackAfter ?? ""}`;
async function main() {
	const SW = JSON.parse(fs.readFileSync(path.join(OUT, "_s46_r3_swallow.json"), "utf8"));
	const byMod = {};
	for (const s of SW) (byMod[s.code] ??= []).push(fold(s.text).slice(0, 60));
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
		const wants = byMod[curMod] ?? [];
		for (const b of (Array.isArray(res) ? res : (res?.bundles ?? []))) {
			const mem = b?.memberItems ?? [];
			let first = -1;
			for (let q = 0; q < mem.length && first < 0; q++) {
				const f = fold(memText(mem[q]));
				if (f.length >= 20 && wants.some((w) => w.length >= 20 && f.includes(w.slice(0, 40)))) first = q;
			}
			if (first < 0) continue;
			const hits = mem.filter((m) => { const f = fold(memText(m)); return f.length >= 20 && wants.some((w) => f.includes(w.slice(0, 40))); }).length;
			pending.push({ b, rec: { code: curMod, page: label, type: b.type, members: mem.length, first, hits,
				opener: (b.openerItems ?? []).map(tagOf).slice(0, 3).join("+"),
				before: mem.slice(Math.max(0, first - 3), first).map((m) => `${tagOf(m)}:${String(m.blackAfter ?? m.text ?? "").replace(/\s+/g, " ").slice(0, 40)}`),
				at: `${tagOf(mem[first])}:${String(mem[first].blackAfter ?? mem[first].text ?? "").replace(/\s+/g, " ").slice(0, 50)}`,
				term: tagOf(page.items[b.endIndex]) } });
		}
		return res;
	};
	const codes = Object.keys(byMod).sort(); const si = process.argv.indexOf("--shard");
	let list = codes, k = 0;
	if (si > -1) { k = parseInt(process.argv[si + 1], 10); const n = parseInt(process.argv[si + 2], 10); list = codes.filter((_, i) => i % n === k); }
	for (const code of list) {
		curMod = code;
		try {
			const dir = corpus.mdir(GOLD, code);
			const run = new ConversionRun({ imageMode: "P" }); const docs = [];
			for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
				const buf = fs.readFileSync(path.join(dir, name));
				docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
			}
			const istockAcksFiles = fs.readdirSync(dir).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(dir, f), "utf8") }));
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
