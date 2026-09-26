/** _s54_r3_btnblock.cjs — session 54 Round 3: THE BUTTON BLOCKER, SIMULATED (diagnostic only). Hooks InteractiveBuilder.Build; for
 *  every bundle that does NOT build and holds ≥ 1 `[button]` member, re-runs the builder on a shallow copy with the button members
 *  removed and records whether it would then build, with each button's label (its black text) and its position (last member?).
 *  → outputs/_s54_btn_shardK.json; --merge prints, per widget type, refused-with-button / would-build, and the labels.
 *  FROM reference/tests/:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s54_r3_btnblock.cjs --shard K 8
 *                          node ../../outputs/_s54_r3_btnblock.cjs --merge */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const SHARD = (k) => path.join(__dirname, `_s54_btn_shard${k}.json`);
const unRed = (s) => String(s ?? "").replace(/\u{1f534}\[\/?RED TEXT\]\u{1f534}/gu, " ");
const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();

if (process.argv.includes("--merge")) {
	let all = [];
	for (let k = 0; k < 64; k++) if (fs.existsSync(SHARD(k))) all = all.concat(JSON.parse(fs.readFileSync(SHARD(k), "utf8")));
	fs.writeFileSync(path.join(__dirname, "_s54_btnblock.json"), JSON.stringify(all));
	const by = {};
	for (const r of all) { const t = (by[r.type] ??= { n: 0, would: 0, pages: new Set(), wpages: new Set(), wmods: new Set(), labels: {}, wlabels: {}, last: 0 });
		t.n++; t.pages.add(r.code + " " + r.page);
		for (const l of r.labels) { const k = l.toLowerCase().replace(/[.!]+$/, "").slice(0, 40); t.labels[k] = (t.labels[k] ?? 0) + 1; }
		if (r.would) { t.would++; t.wpages.add(r.code + " " + r.page); t.wmods.add(r.code); if (r.lastIsButton) t.last++;
			for (const l of r.labels) { const k = l.toLowerCase().replace(/[.!]+$/, "").slice(0, 40); t.wlabels[k] = (t.wlabels[k] ?? 0) + 1; } } }
	console.log(`refused bundles holding a [button] member: ${all.length}`);
	for (const [ty, t] of Object.entries(by).sort((a, b) => b[1].would - a[1].would)) {
		console.log(`\n${ty}: refused-with-button ${t.n} (${t.pages.size} pages) — WOULD BUILD without the button(s): ${t.would} bundles / ${t.wpages.size} pages / ${t.wmods.size} modules (button last member ${t.last})`);
		console.log(`   would-build labels: ${JSON.stringify(Object.fromEntries(Object.entries(t.wlabels).sort((a, b) => b[1] - a[1]).slice(0, 14)))}`);
		console.log(`   all labels:         ${JSON.stringify(Object.fromEntries(Object.entries(t.labels).sort((a, b) => b[1] - a[1]).slice(0, 14)))}`);
		console.log(`   e.g. ${all.filter((r) => r.type === ty && r.would).slice(0, 6).map((r) => `${r.code} ${r.page} #${r.index} [${r.labels.join(" | ")}]`).join(" ; ")}`);
	}
	process.exit(0);
}

async function main() {
	const eng = require(path.join(TESTS, "_engine_load.cjs"));
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
	eng.loadEngine(); console.log = _l;
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const recs = []; let curMod = "?", curPage = "?", inner = false;
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) { curPage = String(page?.lessonLabel ?? page?.label ?? "?"); return origScan(page, normaliser, run); };
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		let out = null;
		try { out = origBuild(args); } catch (e) { out = null; }
		if (inner) return out;
		try {
			const b = args?.bundle;
			const mem = b?.memberItems ?? [];
			const isBtn = (m) => m && m.type === "tag" && m.parse?.primary?.tag === "button";
			if (out == null && b && mem.some(isBtn)) {
				const labels = mem.filter(isBtn).map((m) => clean(m.blackAfter ?? "") || clean(unRed(m.text)));
				const kept = mem.filter((m) => !isBtn(m));
				const lastIdx = mem.map((m, i) => (m ? i : -1)).filter((i) => i >= 0).pop();
				let would = false;
				inner = true;
				try { would = origBuild({ ...args, bundle: { ...b, memberItems: kept, instructions: [...(b.instructions ?? [])] } }) != null; } catch (e) { would = false; }
				inner = false;
				recs.push({ code: curMod, page: curPage, index: b.index, type: b.type, labels, would, lastIsButton: isBtn(mem[lastIdx]) });
			}
		} catch (e) { inner = false; }
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
