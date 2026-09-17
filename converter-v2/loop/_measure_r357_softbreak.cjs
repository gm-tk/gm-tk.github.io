/** _measure_r357_softbreak.cjs — session 17 PICK measurement: the r227 soft-break form question re-measured over EVERY module. For every
 *  Writers-Template paragraph block that carries a soft line break (the extractor's '\n' inside block.text — a writer's Shift+Enter), with
 *  ≥ 2 words on each side of the break: what does the GOLD ship at that boundary — the two sides in ONE element joined by <br> (br), in
 *  TWO sibling elements (split), or glued with a space in one element (glued), or not found? Per template folder / subject family / list-ness.
 *  Run from reference/tests under WSL, sharded (8): STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r357_softbreak.cjs --shard K 8 CODES…
 *  then --merge → _r357_softbreak.json. Diagnostic only. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const SHARD = (k) => path.join(OUT, `_r357_sb_shard${k}.json`);
if (process.argv.includes("--merge")) {
	const all = [];
	for (let k = 0; k < 64; k++) { if (fs.existsSync(SHARD(k))) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8"))); }
	fs.writeFileSync(path.join(OUT, "_r357_softbreak.json"), JSON.stringify(all));
	console.log("records ->", path.join(OUT, "_r357_softbreak.json"), all.length);
	return;
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const ENT = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", rsquo: "’", lsquo: "‘", rdquo: "”", ldquo: "“", hellip: "…", ndash: "–", mdash: "—" };
const unesc = (s) => String(s).replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n)).replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16))).replace(/&([a-z]+);/gi, (m, n) => ENT[n.toLowerCase()] ?? m);
const norm = (s) => unesc(String(s ?? "")).toLowerCase().replace(/[\u2018\u2019]/g, "'").replace(/[\u201c\u201d]/g, '"').replace(/[^\p{L}\p{N}]+/gu, " ").trim();
const words = (s) => norm(s).split(" ").filter(Boolean);
function goldStream(html) {
	// a token stream of the gold page: text words + boundary markers BR (a <br>) and EL (any other element boundary)
	let h = String(html).replace(/<!--[\s\S]*?-->/g, " ").replace(/<(script|style)\b[\s\S]*?<\/\1>/gi, " ");
	const b = h.indexOf('id="body"'); if (b > 0) h = h.slice(b);
	const out = [];
	for (const m of h.matchAll(/<br\s*\/?>|<\/?(p|li|h[1-6]|div|td|th|tr|table|ul|ol|blockquote|span|b|i|strong|em|a|u)\b[^>]*>|<[^>]+>|[^<]+/gi)) {
		const t = m[0];
		if (/^<br/i.test(t)) out.push("\u0001BR");
		else if (/^<\/?(span|b|i|strong|em|a|u)\b/i.test(t)) continue;           // inline formatting is not a boundary
		else if (t[0] === "<") out.push("\u0001EL");
		else { const w = words(t); if (w.length) out.push(...w); }
	}
	return out;
}
function classify(streams, left, right) {
	const L = left.slice(-4), R = right.slice(0, 4);
	if (!L.length || !R.length) return "short";
	let best = "missing";
	for (const s of streams) {
		for (let i = 0; i + L.length <= s.length; i++) {
			let ok = true; for (let j = 0; j < L.length; j++) if (s[i + j] !== L[j]) { ok = false; break; }
			if (!ok) continue;
			// after the left words: skip boundary markers and see what separates them from the right words
			let k = i + L.length, sawBR = false, sawEL = false;
			while (k < s.length && s[k].startsWith("\u0001")) { if (s[k] === "\u0001BR") sawBR = true; else sawEL = true; k++; }
			let okR = true; for (let j = 0; j < R.length; j++) if (s[k + j] !== R[j]) { okR = false; break; }
			if (!okR) { if (best === "missing") best = "left-only"; continue; }
			return sawBR ? "br" : (sawEL ? "split" : "glued");
		}
	}
	return best;
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
			const prep = ModuleResolver.PrepareRun({ docs, run, normaliser, istockAcksFiles: [] });
			if (!prep.ok) continue;
			const goldPages = fs.readdirSync(base).filter((f) => /\.html?$/i.test(f) && !/acks|acknowledge|glossary/i.test(f));
			const streams = goldPages.map((f) => goldStream(fs.readFileSync(path.join(base, f), "utf8")));
			const tmpl = path.basename(path.dirname(base));
			let inMedia = false;
			for (const b of run.wtBlocks ?? []) {
				if (b.kind !== "para") continue;
				const raw = String(b.text ?? "");
				const black = raw.replace(/\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}/gu, " ");
				if (/^\s*media\s+list\b/i.test(black)) inMedia = true;
				if (inMedia || !black.includes("\n")) continue;
				const lines = black.split("\n").map((s) => s.trim()).filter(Boolean);
				for (let i = 0; i + 1 < lines.length; i++) {
					const L = words(lines[i]), R = words(lines[i + 1]);
					if (L.length < 2 || R.length < 2) continue;
					recs.push({ code, tmpl, list: b.list ?? null, red: /\[RED TEXT\]/.test(raw), bold: /\*\*/.test(lines[i]), nLines: lines.length,
						cls: classify(streams, L, R), l: lines[i].slice(0, 50), r: lines[i + 1].slice(0, 50) });
				}
			}
		} catch (e) { errs++; lastErr = String(e && e.stack || e).slice(0, 300); }
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "soft breaks; errors", errs, lastErr);
}
main().catch((e) => { console.error(e); process.exit(1); });
