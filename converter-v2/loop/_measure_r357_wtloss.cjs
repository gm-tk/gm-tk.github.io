/** _measure_r357_wtloss.cjs — session 17 PICK measurement: the FREE-BODY text-loss census. For every module, every Writers-Template
 *  paragraph block from the content start to the MEDIA LIST heading whose BLACK text has ≥ 5 words: is it on any assembled page of the
 *  module (visible text — the free body, the hand-off boxes, the Writers Notes, alt/title attributes)? A paragraph is LOST when neither
 *  its first 6 words nor its last 6 words (normalised) are on any page. The r352 census asked this of built-widget MEMBERS; this asks it of
 *  the WHOLE document. Records every lost paragraph with the nearest preceding red tag (the writer's context) for offline classification.
 *  Run from reference/tests under WSL, sharded:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r357_wtloss.cjs --shard K 8 CODES…
 *  then --merge → _r357_wtloss.json. Diagnostic only — never imported by the engine, never writes to the corpus. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const SHARD = (k) => path.join(OUT, `_r357_wl_shard${k}.json`);
if (process.argv.includes("--merge")) {
	const all = [];
	for (let k = 0; k < 64; k++) { if (fs.existsSync(SHARD(k))) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8"))); }
	fs.writeFileSync(path.join(OUT, "_r357_wtloss.json"), JSON.stringify(all));
	console.log("records ->", path.join(OUT, "_r357_wtloss.json"), all.length);
	return;
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const ENT = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", rsquo: "’", lsquo: "‘", rdquo: "”", ldquo: "“", hellip: "…", ndash: "–", mdash: "—" };
const unesc = (s) => String(s).replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n)).replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16))).replace(/&([a-z]+);/gi, (m, n) => ENT[n.toLowerCase()] ?? m);
const norm = (s) => unesc(String(s ?? "")).toLowerCase().replace(/[\u2018\u2019]/g, "'").replace(/[\u201c\u201d]/g, '"').replace(/[^\p{L}\p{N}]+/gu, " ").trim();
const words = (s) => norm(s).split(" ").filter(Boolean);
function pageText(html) {
	let h = String(html).replace(/<!--[\s\S]*?-->/g, " ").replace(/<(script|style)\b[\s\S]*?<\/\1>/gi, " ");
	const attrs = [...h.matchAll(/\s(?:alt|title|data-text|placeholder)="([^"]*)"/g)].map((m) => m[1]).join(" ");
	return norm(h.replace(/<[^>]+>/g, " ") + " " + attrs);
}
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const normaliser = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const recs = []; let errs = 0, lastErr = "";
	const codes = process.argv.slice(2).filter((a, i, arr) => !a.startsWith("--") && !/^\d+$/.test(a) && arr[i - 1] !== "--shard");
	const si = process.argv.indexOf("--shard"); let k = 0, list = codes;
	if (si > -1) { k = parseInt(process.argv[si + 1], 10); const n = parseInt(process.argv[si + 2], 10); list = codes.filter((_, i) => i % n === k); }
	for (const code of list) {
		let base; try { base = corpus.mdir(GOLD, code); fs.readdirSync(base); } catch { continue; }
		try {
			const run = new ConversionRun({ imageMode: "P" }); const docs = [];
			for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx") && !f.startsWith("~"))) {
				const buf = fs.readFileSync(path.join(base, name));
				const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
				docs.push({ name, doc: await DocxExtractor.Extract(zip) });
			}
			const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
			const prep = ModuleResolver.PrepareRun({ docs, run, normaliser, istockAcksFiles });
			if (!prep.ok) continue;
			await PageAssembler.AssembleModule(run, normaliser);
			const pages = (run.outputs ?? []).filter((o) => /\.html?$/i.test(o.filename));
			const big = " " + pages.map((o) => pageText(o.content)).join(" ") + " ";
			let total = 0, lost = 0, lastTag = "", lastTagDist = 99, inMedia = false;
			const blocks = run.wtBlocks ?? [];
			for (let i = 0; i < blocks.length; i++) {
				const b = blocks[i];
				if (b.kind !== "para") { lastTagDist++; continue; }
				const raw = String(b.text ?? "");
				const reds = [...raw.matchAll(/\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu)].map((m) => m[1].trim());
				const black = raw.replace(/\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}/gu, " ").replace(/\s+/g, " ").trim();
				if (/^media\s+list\b/i.test(black) || reds.some((r) => /^\[?media list/i.test(r))) inMedia = true;
				if (inMedia) continue;
				if (reds.length) { lastTag = reds[0].slice(0, 60); lastTagDist = 0; } else lastTagDist++;
				const w = words(black);
				if (w.length < 5) continue;
				total++;
				const head = w.slice(0, 6).join(" "), tail = w.slice(-6).join(" ");
				if (big.includes(" " + head + " ") || big.includes(" " + tail + " ")) continue;
				lost++;
				recs.push({ code, wtPage: b.wtPage ?? null, i, list: b.list ?? null, sameTag: reds.length ? reds[0].slice(0, 50) : null,
					prevTag: lastTag, prevDist: lastTagDist, bold: /\*\*/.test(black), text: black.slice(0, 140), nWords: w.length });
			}
			recs.push({ code, summary: true, total, lost, pages: pages.length });
		} catch (e) { errs++; lastErr = String(e && e.stack || e).slice(0, 300); }
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "records; errors", errs, lastErr);
}
main().catch((e) => { console.error(e); process.exit(1); });
