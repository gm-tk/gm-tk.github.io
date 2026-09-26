/** _s54_r3_ddtable.cjs — session 54 Round 3: THE DRAG-AND-DROP FIB TABLE (diagnostic only). Hooks InteractiveBuilder.Build (the
 *  r286 recorder's pattern); for every dragAndDrop bundle that does NOT build and holds exactly ONE table member, classifies the
 *  table: per body row, cell 0 = a sentence with ≥ 1 red run and black words around it (a FIB sentence); the other cells empty,
 *  or an answer echo (their unred text = the row's red runs), or other. Writes one record per bundle with its rows (≤ 6) to
 *  outputs/_s54_ddtable_shardK.json; --merge prints the census by shape + family.
 *  FROM reference/tests/:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s54_r3_ddtable.cjs --shard K 8
 *                          node ../../outputs/_s54_r3_ddtable.cjs --merge */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const SHARD = (k) => path.join(__dirname, `_s54_ddtable_shard${k}.json`);
const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
const unRed = (s) => String(s ?? "").replace(/\u{1f534}\[\/?RED TEXT\]\u{1f534}/gu, " ");
const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
const fold = (s) => clean(s).toLowerCase().replace(/[^\p{L}\p{N}]+/gu, "");

if (process.argv.includes("--merge")) {
	let all = [];
	for (let k = 0; k < 64; k++) if (fs.existsSync(SHARD(k))) all = all.concat(JSON.parse(fs.readFileSync(SHARD(k), "utf8")));
	fs.writeFileSync(path.join(__dirname, "_s54_ddtable.json"), JSON.stringify(all));
	const by = {};
	for (const r of all) { const k = r.cls; (by[k] ??= { n: 0, mods: new Set(), pages: new Set(), fam: {}, ex: [] }); by[k].n++; by[k].mods.add(r.code); by[k].pages.add(r.code + " " + r.page);
		const f = r.code.replace(/\d.*$/, ""); by[k].fam[f] = (by[k].fam[f] ?? 0) + 1; if (by[k].ex.length < 4) by[k].ex.push(r); }
	console.log(`refused single-table dragAndDrop bundles: ${all.length}`);
	for (const [k, v] of Object.entries(by).sort((a, b) => b[1].n - a[1].n)) {
		console.log(`\n${String(v.n).padStart(4)}  ${k}  — ${v.pages.size} pages / ${v.mods.size} modules  ${JSON.stringify(Object.fromEntries(Object.entries(v.fam).sort((a, b) => b[1] - a[1]).slice(0, 8)))}`);
		for (const e of v.ex) { console.log(`      e.g. ${e.code} ${e.page} #${e.index} ${e.w}-col ${e.nrows} rows  others=${JSON.stringify(e.others)}`); for (const row of e.rows.slice(0, 3)) console.log(`           | ${row.map((c) => c.slice(0, 70)).join(" ║ ")}`); }
	}
	process.exit(0);
}

function classify(rows) {
	const body = rows.filter((r) => r.some((c) => clean(unRed(c))));
	if (!body.length) return { cls: "empty" };
	const w = Math.max(...body.map((r) => r.length));
	let fib = 0, echo = 0, emptyRest = 0, other = 0, header = 0, redOnly = 0;
	body.forEach((r, i) => {
		const c0 = String(r[0] ?? "");
		RED.lastIndex = 0; const reds = [...c0.matchAll(RED)].map((m) => clean(m[1])).filter(Boolean);
		const black = clean(c0.replace(RED, " "));
		const rest = r.slice(1).map((c) => clean(unRed(c))).filter(Boolean);
		if (!reds.length) { if (i === 0) header++; else other++; return; }
		if (!/[\p{L}\p{N}]/u.test(black)) { redOnly++; return; }
		fib++;
		if (!rest.length) emptyRest++;
		else if (fold(rest.join(" ")) === fold(reds.join(" ")) || rest.every((t) => reds.some((a) => fold(a) === fold(t)))) echo++;
		else other++;
	});
	const n = body.length - header;
	let cls;
	if (fib === n && n >= 2) cls = `FIB table (${w}-col): rest ${emptyRest === n ? "empty" : echo + emptyRest === n ? "echo/empty" : "mixed"}`;
	else if (fib >= 2 && fib >= n * 0.6) cls = `mostly FIB (${w}-col)`;
	else if (redOnly >= n * 0.6) cls = `red-only cell 0 (${w}-col)`;
	else cls = `other (${w}-col)`;
	return { cls, w, nrows: body.length, fib, echo, emptyRest, other, header };
}

async function main() {
	const eng = require(path.join(TESTS, "_engine_load.cjs"));
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
	eng.loadEngine(); console.log = _l;
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const recs = []; let curMod = "?", curPage = "?";
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) { curPage = String(page?.lessonLabel ?? page?.label ?? "?"); return origScan(page, normaliser, run); };
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle; let out = null;
		try { out = origBuild(args); } catch (e) { out = null; }
		try {
			if (b?.type === "dragAndDrop" && out == null) {
				const mem = b.memberItems ?? [];
				const tables = mem.filter((m) => m?.type === "table");
				if (tables.length === 1) {
					const rows = (tables[0].block?.rows ?? []).map((r) => (r ?? []).map((c) => String(typeof c === "string" ? c : c?.text ?? "")));
					const others = mem.filter((m) => m && m.type !== "table").map((m) => m.type === "black" ? "black" : (m.parse?.primary?.tag ?? m.parse?.class ?? m.type));
					const c = classify(rows);
					recs.push({ code: curMod, page: curPage, index: b.index, ...c, others, extra: b.extraTypes ?? [], media: (b.media ?? []).length,
						rows: rows.slice(0, 6).map((r) => r.map((x) => clean(x).replace(/\u{1f534}\[RED TEXT\]/gu, "«").replace(/\[\/RED TEXT\]\u{1f534}/gu, "»"))) });
				}
			}
		} catch (e) { /* keep scanning */ }
		return out;
	};
	const dirs = [];
	for (const t of fs.readdirSync(GOLD)) { const tp = path.join(GOLD, t); if (!fs.statSync(tp).isDirectory()) continue;
		for (const code of fs.readdirSync(tp)) { const cp = path.join(tp, code); if (fs.statSync(cp).isDirectory()) dirs.push({ code, dir: cp }); } }
	dirs.sort((a, b) => a.code.localeCompare(b.code));
	const si = process.argv.indexOf("--shard"); let list = dirs, k = 0;
	if (si > -1) { k = parseInt(process.argv[si + 1], 10); const n = parseInt(process.argv[si + 2], 10); list = dirs.filter((_, i) => i % n === k); }
	for (const d of list) {
		curMod = d.code;
		try {
			const run = new ConversionRun({ imageMode: "P" }); const docs = [];
			for (const name of fs.readdirSync(d.dir).filter((f) => f.endsWith(".docx"))) {
				const buf = fs.readFileSync(path.join(d.dir, name));
				docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
			}
			const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm });
			if (!prep.ok) continue;
			await PageAssembler.AssembleModule(run, norm);
		} catch (e) { /* keep scanning */ }
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "records");
}
main().catch((e) => { console.error(e); process.exit(1); });
