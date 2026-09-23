/** _measure_r271_variations.cjs — ROUND 271 measurement probe (Chris: "ALL of the
 *  various variations for ALL of the non-complex interactives should ALL be
 *  configured into the code").
 *
 *  THE QUESTION. For every captured bundle of a NON-COMPLEX widget type, what
 *  AUTHORING SHAPE did the writer use, and does the shipped builder build it?
 *  Round 245 measured only the headline coverage (8.3%); round 246 widened three
 *  dialects by hand. To close the class we need the shapes themselves clustered,
 *  so a round can take the biggest declining SHAPE, not the biggest type.
 *
 *  THE SHAPE SIGNATURE is the unit of analysis. For each bundle it compresses:
 *    - how many tables, their dimensions, and the KIND GRID of their cells
 *      (media / tagged-media / text / tagged-text / empty) — the discriminator
 *      that separates "media|caption table" from "media-only table" from "quiz
 *      matrix", which is exactly where the builders keep bailing;
 *    - the member kind/tag stream, run-length compressed;
 *    - the media inventory by host class (youtube / istock / other);
 *    - whether red writer-instruction text is embedded.
 *  Bundles with the SAME signature are the same authoring dialect, so a fix for
 *  one is a fix for all of them — which is what "train on all variations" means.
 *
 *  Diagnostic only — never imported by the engine.
 *
 *  Usage (FROM reference/tests/), sharded for the 45s wall:
 *    STUB_OEMBED=1 timeout 42 node --require ./_deflate_raw_polyfill.cjs \
 *      ../../outputs/_measure_r271_variations.cjs --shard K 16
 *  then:
 *    node ../../outputs/_measure_r271_variations.cjs --merge
 *    node ../../outputs/_measure_r271_variations.cjs --report [type]
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const OUT = __dirname;
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const SHARD = (k) => path.join(OUT, `_r271_var_shard${k}.json`);
const MERGED = path.join(OUT, "_r271_variations.json");

/** the NON-COMPLEX types: every type with a builder case, plus the display types
 *  a writer commonly tags that we could reasonably build. Task/quiz engines
 *  (crossword, memoryGame, typing, …) are Phase-1 placeholders by design. */
const WANT = new Set([
	"carousel", "accordion", "speechBubble", "flipCard", "tabs", "hintSlider", "hint",
	"shapeHover", "clickDrop", "glossary", "selfCheck", "dragAndDrop", "modal",
	"rotateBanner", "slider", "infoTrigger",
]);
/** SESSION 40 ROUND 10 (24 Sept 2026 — the r449 follow-up): the quiz engines are no longer placeholders by design — Chris's
 *  D13-4 builds them where the writer marked the answer (typing shape 1 shipped r449) — so the census counts them too, and the
 *  dashboard's §4 widget-round "still a box" test can be read for them. The list is the D13-4 answer-key type list
 *  (Emit_Templates interactive_placeholder.answer_key_d13_4.types). CENSUS_QUIZ_OFF=1 reproduces the pre-round census. */
const QUIZ_TYPES = ["multiChoiceQuiz", "typing", "dropDown", "dropQuiz", "radioQuiz", "reorder", "selectionBox"];
if (!process.env.CENSUS_QUIZ_OFF) for (const t of QUIZ_TYPES) WANT.add(t);

const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
const URLRE = /https?:\/\/[^\s\]"<>)]+/;

function hostClass(u) {
	const s = String(u ?? "");
	if (/youtu\.?be|youtube\.com/i.test(s)) return /\/shorts\//i.test(s) ? "ytshort" : "yt";
	if (/vimeo/i.test(s)) return "vimeo";
	if (/istockphoto\.com/i.test(s)) return "istock";
	if (/gettyimages/i.test(s)) return "getty";
	if (/\.(mp3|wav|m4a|ogg)(\?|$)/i.test(s)) return "audio";
	if (/\.(pdf|docx?|pptx?|xlsx?)(\?|$)/i.test(s)) return "doc";
	if (!s) return "";
	return "web";
}

/** the KIND of one table cell — the heart of the signature. */
function cellKind(cell, normaliser) {
	const raw = typeof cell === "string" ? cell : (cell?.text ?? "");
	const txt = String(raw);
	if (!clean(txt)) return "-";                       // empty
	const url = txt.match(URLRE)?.[0] ?? "";
	// a red [tag] present in the cell?
	let tag = "";
	try {
		const p = normaliser.Parse(txt);
		tag = p?.primary?.tag ?? "";
	} catch (e) { /* unparsed cell */ }
	const hc = hostClass(url);
	// strip tags + url; is there real prose left?
	const prose = clean(txt.replace(/\[[^\]]*\]/g, " ").replace(new RegExp(URLRE.source, "g"), " "));
	if (hc && prose.length > 25) return `M${hc}+txt`;   // media cell that ALSO carries caption prose
	if (hc) return `M${hc}`;                            // pure media cell
	if (tag && !prose) return `T:${tag}`;               // bare marker cell (front/back/drop/hint…)
	if (tag) return `T:${tag}+txt`;                     // marker + prose
	return prose.length > 60 ? "txtL" : "txt";          // long / short prose
}

/** compress a repeated sequence: [a,a,a,b,b] -> "a*3,b*2" */
function rle(arr) {
	const out = [];
	for (const v of arr) {
		const last = out[out.length - 1];
		if (last && last.v === v) last.n++;
		else out.push({ v, n: 1 });
	}
	return out.map((o) => (o.n > 1 ? `${o.v}*${o.n}` : o.v)).join(",");
}

function tableSig(t, normaliser) {
	const rows = t?.rows ?? [];
	if (!rows.length) return "table0x0";
	const nCol = Math.max(...rows.map((r) => (r ?? []).length));
	// the kind grid, row by row; identical consecutive rows collapse
	const rowSigs = rows.map((r) => (r ?? []).map((c) => cellKind(c, normaliser)).join("|"));
	return `T${rows.length}x${nCol}[${rle(rowSigs)}]`;
}

function bundleSig(b, normaliser) {
	const members = b.memberItems ?? [];
	const kinds = [];
	let instr = 0;
	for (const m of members) {
		if (!m) continue;
		if (m.type === "table") { kinds.push("TABLE"); continue; }
		if (m.type === "black") {
			const t = clean(m.text);
			if (!t) continue;
			const hc = hostClass(t.match(URLRE)?.[0] ?? "");
			kinds.push(hc ? `blk:${hc}` : (t.length > 60 ? "blkL" : "blk"));
			continue;
		}
		const p = m.parse?.primary;
		const cls = m.parse?.class;
		if (cls === "instruction" || cls === "noise") { instr++; kinds.push("INSTR"); continue; }
		const after = clean(m.blackAfter);
		const hc = hostClass(after.match(URLRE)?.[0] ?? "");
		kinds.push(`${p?.tag ?? "?"}${hc ? ":" + hc : (after ? "+txt" : "")}`);
	}
	const tables = (b.tables ?? []).map((t) => tableSig(t, normaliser));
	const extra = [...new Set(b.extraTypes ?? [])].sort();
	return {
		sig: [
			tables.length ? tables.join(";") : "noTable",
			rle(kinds) || "noMembers",
			extra.length ? `extra:${extra.join("+")}` : "",
			b.variant ? `var:${b.variant}` : "",
			instr ? "hasInstr" : "",
		].filter(Boolean).join(" || "),
		nTables: tables.length,
		instr,
	};
}

// ---------------------------------------------------------------- merge/report
if (process.argv.includes("--merge")) {
	let all = [];
	for (let k = 0; k < 64; k++) {
		const f = SHARD(k);
		if (fs.existsSync(f)) all = all.concat(JSON.parse(fs.readFileSync(f, "utf8")));
	}
	all.sort((a, b) => (a.code + a.type + a.index).localeCompare(b.code + b.type + b.index));
	fs.writeFileSync(MERGED, JSON.stringify(all));
	const by = {};
	for (const r of all) {
		by[r.type] ??= { built: 0, fell: 0, mods: new Set() };
		if (r.built) by[r.type].built++; else { by[r.type].fell++; by[r.type].mods.add(r.code); }
	}
	const rows = Object.entries(by).sort((a, b) => b[1].fell - a[1].fell);
	console.log("TYPE            BUILT  DECLINED  MODULES  COVERAGE");
	let tb = 0, tf = 0;
	for (const [t, s] of rows) {
		tb += s.built; tf += s.fell;
		const cov = (100 * s.built / (s.built + s.fell)).toFixed(1);
		console.log(`${t.padEnd(15)} ${String(s.built).padStart(5)} ${String(s.fell).padStart(9)} ${String(s.mods.size).padStart(8)}   ${cov}%`);
	}
	console.log(`${"TOTAL".padEnd(15)} ${String(tb).padStart(5)} ${String(tf).padStart(9)}          ${(100 * tb / (tb + tf)).toFixed(1)}%`);
	console.log("records ->", MERGED, all.length);
	process.exit(0);
}

if (process.argv.includes("--report")) {
	const only = process.argv[process.argv.indexOf("--report") + 1];
	const all = JSON.parse(fs.readFileSync(MERGED, "utf8"));
	const groups = {};
	for (const r of all) {
		if (r.built) continue;
		if (only && only !== "all" && r.type !== only) continue;
		const key = `${r.type} :: ${r.sig}`;
		groups[key] ??= { n: 0, mods: new Set(), ex: [] };
		groups[key].n++;
		groups[key].mods.add(r.code);
		if (groups[key].ex.length < 4) groups[key].ex.push(`${r.code}/${r.page}`);
	}
	const rows = Object.entries(groups).sort((a, b) => b[1].n - a[1].n);
	console.log(`DECLINING SHAPES${only && only !== "all" ? " for " + only : ""} — ${rows.length} distinct signatures\n`);
	for (const [k, v] of rows.slice(0, Number(process.env.TOP || 45))) {
		console.log(`[${String(v.n).padStart(4)} bundles / ${String(v.mods.size).padStart(3)} modules]  ${k}`);
		console.log(`        e.g. ${v.ex.join(", ")}`);
	}
	const tot = rows.reduce((a, b) => a + b[1].n, 0);
	console.log(`\nTOTAL declining bundles: ${tot} across ${rows.length} shapes`);
	process.exit(0);
}

// ---------------------------------------------------------------------- scan
const eng = require(path.join(TESTS, "_engine_load.cjs"));

function moduleDirs() {
	const out = [];
	for (const tmpl of fs.readdirSync(GOLD)) {
		const tp = path.join(GOLD, tmpl);
		if (!fs.statSync(tp).isDirectory()) continue;
		for (const code of fs.readdirSync(tp)) {
			const cp = path.join(tp, code);
			if (fs.statSync(cp).isDirectory()) out.push({ code, dir: cp });
		}
	}
	return out.sort((a, b) => a.code.localeCompare(b.code));
}

async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
	eng.loadEngine(); console.log = _l;
	globalThis.norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);

	const recs = [];
	let curMod = "?", curPage = "?";
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) {
		curPage = String(page?.lessonLabel ?? page?.label ?? "?");
		return origScan(page, normaliser, run);
	};

	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle;
		let out = null;
		try { out = origBuild(args); } catch (e) { out = null; }
		if (b && WANT.has(b.type)) {
			try {
				const s = bundleSig(b, norm);
				recs.push({
					code: curMod, page: curPage, type: b.type, index: b.index,
					built: out != null, sig: s.sig, nTables: s.nTables, instr: s.instr,
					modifier: clean(b.modifier).slice(0, 60),
				});
			} catch (e) { /* keep scanning */ }
		}
		return out;
	};

	const dirs = moduleDirs();
	const si = process.argv.indexOf("--shard");
	let list = dirs, k = 0;
	if (si > -1) {
		k = parseInt(process.argv[si + 1], 10);
		const n = parseInt(process.argv[si + 2], 10);
		list = dirs.filter((_, i) => i % n === k);
	}
	for (const d of list) {
		curMod = d.code;
		try {
			const run = new ConversionRun({ imageMode: "P" });
			const docs = [];
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
