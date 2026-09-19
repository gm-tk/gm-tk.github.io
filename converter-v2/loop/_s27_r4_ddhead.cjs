/** _s27_r4_ddhead.cjs — Session 27 Round 4 probe: THE TITLE-LED dragAndDrop (the census's largest declining
 *  shape, "noTable || drag and drop" — 53 bundles / 35 modules on the r399 corpus).
 *
 *  For every dragAndDrop bundle the builder DECLINES with NO captured table, classify the page items AFTER the
 *  bundle's end: is the next item a heading (h2–h5 — the widget's title the walk treats as a terminator), then
 *  prose / [body], then a TABLE (the widget's data) before any other structural tag? Record the table's shape
 *  (rows × cols, kinds) and whether the gold page builds a div.dragAndDrop whose text carries the writer's
 *  table cells. Usage (from reference/tests/):
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s27_r4_ddhead.cjs --shard K 8
 *    node ../../outputs/_s27_r4_ddhead.cjs --merge
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const OUT = __dirname;
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const SHARD = (k) => path.join(OUT, `_s27_r4_ddhead_shard${k}.json`);
const MERGED = path.join(OUT, "_s27_r4_ddhead.json");
const clean = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
const fold = (s) => clean(s).toLowerCase().replace(/[^\p{L}\p{N} ]+/gu, " ").replace(/\s+/g, " ").trim();
const URLRE = /https?:\/\/[^\s\]"<>)]+/;

function goldPages(code) {
	for (const tmpl of fs.readdirSync(GOLD)) {
		const d = path.join(GOLD, tmpl, code);
		if (fs.existsSync(d) && fs.statSync(d).isDirectory())
			return fs.readdirSync(d).filter((f) => f.endsWith(".html")).map((f) => ({ f, html: fs.readFileSync(path.join(d, f), "utf8") }));
	}
	return [];
}
function goldDdBlocks(html) {
	const out = []; const re = /<div class="dragAndDrop[^"]*"[^>]*>/g; let m;
	while ((m = re.exec(html))) {
		let depth = 0, i = m.index, j = i; const tag = /<(\/?)div\b[^>]*>/g; tag.lastIndex = i;
		let t; while ((t = tag.exec(html))) { if (t[1]) depth--; else depth++; if (depth === 0) { j = t.index + t[0].length; break; } }
		out.push(html.slice(i, j));
	}
	return out;
}

if (process.argv.includes("--merge")) {
	let all = [];
	for (let k = 0; k < 32; k++) { const f = SHARD(k); if (fs.existsSync(f)) all = all.concat(JSON.parse(fs.readFileSync(f, "utf8"))); }
	fs.writeFileSync(MERGED, JSON.stringify(all, null, 1));
	const C = {}; const mods = {}; const pages = {}; const ex = {};
	for (const r of all) {
		const k = r.klass; C[k] = (C[k] || 0) + 1; (mods[k] ??= new Set()).add(r.code); (pages[k] ??= new Set()).add(r.code + "/" + r.page);
		if ((ex[k] ??= []).length < 6) ex[k].push(`${r.code}/${r.page} seq=${r.seq} tbl=${r.tbl} gold=${r.gold}`);
	}
	console.log("un-built table-less dragAndDrop bundles:", all.length);
	for (const [k, v] of Object.entries(C).sort((a, b) => b[1] - a[1])) {
		console.log(`  ${k.padEnd(28)} ${String(v).padStart(3)} bundles / ${mods[k].size} modules / ${pages[k].size} pages`);
		for (const e of ex[k]) console.log("        " + e);
	}
	// the title-led class with a following 2-col table: gold verdict split
	const G = {};
	for (const r of all) if (r.klass.startsWith("HEAD")) { G[r.gold] = (G[r.gold] || 0) + 1; }
	console.log("HEAD-led rows by gold verdict:", JSON.stringify(G));
	const T = {};
	for (const r of all) if (r.klass.startsWith("HEAD") && r.tbl) { T[r.tbl] = (T[r.tbl] || 0) + 1; }
	console.log("HEAD-led table shapes:", JSON.stringify(Object.entries(T).sort((a, b) => b[1] - a[1]).slice(0, 12)));
	process.exit(0);
}

const eng = require(path.join(TESTS, "_engine_load.cjs"));
function moduleDirs() {
	const out = [];
	for (const tmpl of fs.readdirSync(GOLD)) {
		const tp = path.join(GOLD, tmpl); if (!fs.statSync(tp).isDirectory()) continue;
		for (const code of fs.readdirSync(tp)) { const cp = path.join(tp, code); if (fs.statSync(cp).isDirectory()) out.push({ code, dir: cp }); }
	}
	return out.sort((a, b) => a.code.localeCompare(b.code));
}
function tagOf(it) { return String(it?.parse?.primary?.tag ?? "").toLowerCase(); }
function dirOf(it) { return String(it?.parse?.primary?.directive ?? ""); }
function cellText(c) { return clean(typeof c === "string" ? c : (c?.text ?? "")); }

async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
	eng.loadEngine(); console.log = _l;
	globalThis.norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const HEAD = new Set(["h2", "h3", "h4", "h5", "activity heading", "heading"]);
	const recs = []; let curMod = "?", curPage = "?"; const pending = new Map(); let gold = [];
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, normaliser, run) {
		curPage = String(page?.lessonLabel ?? page?.label ?? "?");
		const bundles = origScan(page, normaliser, run);
		const items = page.items || [];
		for (const b of (bundles || [])) {
			if (b.type !== "dragAndDrop") continue;
			if ((b.tables || []).length) continue;
			// walk forward from the bundle's end
			let i = b.endIndex, seq = [], tblIt = null, klass = "", nHead = 0, nProse = 0;
			for (; i < items.length && seq.length < 10; i++) {
				const it = items[i]; if (!it) continue;
				if (it.type === "black") { if (!clean(it.text)) continue; seq.push("blk"); nProse++; continue; }
				if (it.type === "table") { seq.push("TABLE"); tblIt = it; break; }
				const tg = tagOf(it), dr = dirOf(it);
				if (HEAD.has(tg)) { seq.push(tg + (clean(it.blackAfter) ? "+t" : "")); nHead++; continue; }
				if (tg === "body" || tg === "list") { seq.push("[" + tg + "]"); nProse++; continue; }
				if (it.parse?.class === "instruction" || it.parse?.class === "noise") { seq.push("INSTR"); continue; }
				if (tg === "activity" && dr === "CONTAINER_OPEN" && !seq.some((s) => s.startsWith("ACT"))) { seq.push("ACT" + (clean(it.blackAfter) ? "+t" : "")); continue; }
				if (dr === "INTERACTIVE" || dr === "CONTAINER_OPEN" || dr === "CONTAINER_CLOSE" || dr === "SECTION_MARKER" || dr === "PAGE_BOUNDARY") { seq.push("STOP:" + tg); break; }
				seq.push("[" + tg + "]");
			}
			const first0 = seq[0] || "END";
			const actLed = first0.startsWith("ACT");
			const first = actLed ? (seq[1] || "END") : first0;
			const pre = actLed ? "ACT/" : "";
			if (tblIt) klass = pre + (HEAD.has(first.replace(/\+t$/, "")) ? "HEAD" : (first === "blk" || first.startsWith("[body") ? "PROSE" : "OTHER")) + "→TABLE";
			else klass = pre + (HEAD.has(first.replace(/\+t$/, "")) ? "HEAD" : first === "END" ? "END" : first.startsWith("STOP") ? "STOP" : "PROSE") + "→noTable";
			let tbl = "", g = "n/a";
			if (tblIt) {
				const rows = tblIt.block?.rows ?? tblIt.rows ?? []; const nc = Math.max(0, ...rows.map((r) => (r || []).length));
				const kinds = rows.slice(0, 3).map((r) => (r || []).map((c) => { const t = cellText(c); if (!t) return "-"; if (URLRE.test(t)) return "M"; if (/\[/.test(t)) return "T"; return t.length > 60 ? "L" : "t"; }).join("|")).join(",");
				tbl = `${rows.length}x${nc}[${kinds}]`;
				// gold verdict: a dragAndDrop block on some gold page holding the writer's first two cells
				const c0 = fold(cellText((rows[0] || [])[0])), c1 = fold(cellText((rows[1] || [])[0] ?? (rows[0] || [])[1]));
				const key = (c0.split(" ").slice(0, 5).join(" ") || c1.split(" ").slice(0, 5).join(" "));
				g = "gold:none";
				for (const p of gold) {
					const blocks = goldDdBlocks(p.html);
					for (const bl of blocks) { const f = fold(bl.replace(/<[^>]+>/g, " ")); if (key && f.includes(key)) { g = "gold:DD"; break; } }
					if (g === "gold:DD") break;
					if (key && fold(p.html.replace(/<[^>]+>/g, " ")).includes(key)) g = "gold:other";
				}
			}
			const rec = { code: curMod, page: curPage, index: b.index, klass, seq: seq.join(","), tbl, gold: g, nHead, nProse, built: false,
				head: (() => { const it = items[b.endIndex]; return HEAD.has(tagOf(it)) ? clean(it.blackAfter).slice(0, 50) : ""; })() };
			pending.set(b, rec); recs.push(rec);
		}
		return bundles;
	};
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		let out = null; try { out = origBuild(args); } catch (e) { out = null; }
		const r = pending.get(args?.bundle); if (r) r.built = out != null;
		return out;
	};
	const dirs = moduleDirs(); const si = process.argv.indexOf("--shard"); let list = dirs, k = 0;
	if (si > -1) { k = parseInt(process.argv[si + 1], 10); const n = parseInt(process.argv[si + 2], 10); list = dirs.filter((_, i) => i % n === k); }
	for (const d of list) {
		curMod = d.code; gold = goldPages(d.code);
		try {
			const run = new ConversionRun({ imageMode: "P" }); const docs = [];
			for (const name of fs.readdirSync(d.dir).filter((f) => f.endsWith(".docx"))) {
				const buf = fs.readFileSync(path.join(d.dir, name));
				docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
			}
			const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm }); if (!prep.ok) continue;
			await PageAssembler.AssembleModule(run, norm);
		} catch (e) { /* keep scanning */ }
	}
	const outRecs = recs.filter((r) => !r.built);
	fs.writeFileSync(SHARD(k), JSON.stringify(outRecs));
	_l("shard", k, "->", list.length, "modules,", outRecs.length, "un-built table-less dragAndDrop records");
}
main().catch((e) => { console.error(e); process.exit(1); });
