/** _measure_r356_consumed.cjs — ROUND 356 PICK measurement (the r353 class under an EXACT design). Which members of a
 *  BUILT bundle did the builder never even READ? The r353 members rule guessed consumption from text presence and could
 *  not know what a builder consumed (475 false reverts / 18 duplications). This probe wraps InteractiveBuilder.Build and,
 *  for the duration of the build only, replaces every memberItem with a Proxy that records a read of its CONTENT
 *  (`text`, `blackAfter`, `block`) and every `bundle.tables` read; the originals are restored before the caller sees
 *  the bundle again. A member the builder never read cannot be in the build — an EXACT "un-consumed" set, no guessing.
 *  For every built bundle it records the untouched members by kind (prose / heading / media / tag / table / nested) and,
 *  once the module's pages are assembled, whether each untouched prose run is LOST on the page (the census test) or
 *  PRESENT (reached the page by another route — the read test's false-consumption check). Run from reference/tests
 *  under WSL, sharded exactly like _measure_r354_tagwords.cjs:
 *      STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r356_consumed.cjs --shard K N CODES…
 *      node ../../outputs/_measure_r356_consumed.cjs --merge      → _r356_consumed.json + the summary
 *  Diagnostic only — never imported by the engine, never writes to the corpus. */
"use strict";
const fs = require("fs"), path = require("path");
const OUT = __dirname, TESTS = path.join(OUT, "..", "reference", "tests"), GOLD = path.join(OUT, "..", "..", "01-Finalized_Modules_");
const SHARD = (k) => path.join(OUT, `_r356_cm_shard${k}.json`);
const RED = /\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}/gu;
const norm = (s) => String(s ?? "").replace(/&[a-z#0-9]+;/gi, " ").replace(/[^\p{L}\p{N}]+/gu, " ").trim().toLowerCase();
const words = (t) => norm(String(t ?? "").replace(RED, " ").replace(/\[[^\]]*\]/g, " ").replace(/https?:\/\/\S+/g, " "));
const nw = (t) => t.split(" ").filter(Boolean).length;

if (process.argv.includes("--merge")) {
	const all = [];
	for (let k = 0; k < 64; k++) { if (fs.existsSync(SHARD(k))) all.push(...JSON.parse(fs.readFileSync(SHARD(k), "utf8"))); }
	fs.writeFileSync(path.join(OUT, "_r356_consumed.json"), JSON.stringify(all));
	// ---- summary: per type, the bundles with an untouched LOST prose member (the population), pages, modules
	const by = {};
	const pagesAll = new Set(), modsAll = new Set();
	for (const r of all) {
		const t = by[r.type] ??= { built: 0, lossy: 0, sites: 0, pages: new Set(), mods: new Set(), present: 0, kinds: {}, ex: [] };
		t.built++;
		const lostProse = r.untouched.filter((u) => u.kind === "prose" && u.lost);
		const presProse = r.untouched.filter((u) => u.kind === "prose" && !u.lost);
		t.present += presProse.length;
		for (const u of r.untouched) t.kinds[u.kind] = (t.kinds[u.kind] ?? 0) + 1;
		if (lostProse.length) {
			t.lossy++; t.sites += lostProse.length; t.pages.add(r.code + " " + r.page); t.mods.add(r.code);
			pagesAll.add(r.code + " " + r.page); modsAll.add(r.code);
			if (t.ex.length < 3) t.ex.push(`${r.code} p${r.page} #${r.index} [${lostProse[0].pos}] {${r.map}}: ${lostProse[0].text}`);
		}
	}
	const lines = ["type           built lossy sites pages mods present | untouched kinds"];
	for (const [k, v] of Object.entries(by).sort((a, b) => b[1].lossy - a[1].lossy)) {
		lines.push(`${k.padEnd(14)} ${String(v.built).padStart(5)} ${String(v.lossy).padStart(5)} ${String(v.sites).padStart(5)} ${String(v.pages.size).padStart(5)} ${String(v.mods.size).padStart(4)} ${String(v.present).padStart(7)} | ${Object.entries(v.kinds).map(([a, b]) => a + " " + b).join(", ")}`);
		for (const e of v.ex) lines.push("    " + e);
	}
	lines.push(`TOTAL lossy-prose bundles ${all.filter((r) => r.untouched.some((u) => u.kind === "prose" && u.lost)).length} on ${pagesAll.size} pages / ${modsAll.size} modules`);
	// the strict-mode decline forecast: bundles with an untouched NON-prose member (would revert to the box)
	const dec = all.filter((r) => r.untouched.some((u) => u.kind !== "prose" && u.kind !== "skip"));
	const decBy = {}; for (const r of dec) decBy[r.type] = (decBy[r.type] ?? 0) + 1;
	lines.push(`STRICT-mode declines (an untouched non-prose member): ${dec.length} bundles — ${Object.entries(decBy).map(([a, b]) => a + " " + b).join(", ")}`);
	const decKinds = {}; for (const r of dec) for (const u of r.untouched) if (u.kind !== "prose" && u.kind !== "skip") decKinds[u.kind] = (decKinds[u.kind] ?? 0) + 1;
	lines.push(`  by kind: ${Object.entries(decKinds).sort((a, b) => b[1] - a[1]).map(([a, b]) => a + " " + b).join(", ")}`);
	fs.writeFileSync(path.join(OUT, "_r356_consumed.log"), lines.join("\n") + "\n");
	console.log(lines.join("\n"));
	console.log("records ->", path.join(OUT, "_r356_consumed.json"), all.length);
	return;
}
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const CONTENT = new Set(["text", "blackAfter", "block", "nestedBundle"]);
const urlsOf = (t) => [...String(t ?? "").matchAll(/https?:\/\/[^\s"'<>)\]]+/g)].map((m) => m[0]);
const vidId = (u) => /(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([\w-]{11})/.exec(u)?.[1] ?? null;
const imgKeys = (u) => { const out = []; const gm = /gm(\d{6,})/.exec(u) ?? /\/id\/(\d{6,})/.exec(u) ?? /istock[^\d]*(\d{6,})/i.exec(u); if (gm) out.push("istock-" + gm[1]);
	const seg = String(u).replace(/[?#].*$/, "").split("/").filter(Boolean).pop() ?? ""; const slug = seg.replace(/\.[a-z0-9]{2,5}$/i, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); if (slug.length >= 6) out.push(slug.slice(0, 24)); return out; };
const mediaInHtml = (t, html) => { const us = urlsOf(t); if (!us.length) return null; const low = String(html).toLowerCase(); return us.every((u) => { const id = vidId(u); return low.includes(u.toLowerCase()) || (id && low.includes(id.toLowerCase())) || imgKeys(u).some((k) => low.includes(k)); }); };
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const normaliser = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const mediaTags = new Set(["image", "video", "audio", "embed", "data marker"]);
	const headings = new Set(["h2", "h3", "h4", "h5"]);
	const recs = []; let curMod = "?", curPage = "?", errs = 0, lastErr = "";
	let pending = [];
	const origScan = InteractiveScanner.ScanPage.bind(InteractiveScanner);
	InteractiveScanner.ScanPage = function (page, n, run) { curPage = String(page?.lessonLabel ?? page?.label ?? "?"); return origScan(page, n, run); };
	const origBuild = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle;
		if (!b || !Array.isArray(b.memberItems) || !b.memberItems.length) return origBuild(args);
		const orig = b.memberItems, touched = new Array(orig.length).fill(false);
		let tablesRead = false;
		const proxies = orig.map((m, k) => (m && typeof m === "object")
			? new Proxy(m, { get(t, p, r) { if (CONTENT.has(p)) touched[k] = true; return Reflect.get(t, p, r); } })
			: m);
		const origTables = b.tables;
		b.memberItems = proxies;
		Object.defineProperty(b, "tables", { configurable: true, enumerable: true, get() { tablesRead = true; return origTables; }, set(v) { Object.defineProperty(b, "tables", { configurable: true, enumerable: true, writable: true, value: v }); } });
		let out = null;
		try { out = origBuild(args); } catch (e) { out = null; }
		finally {
			b.memberItems = orig;
			Object.defineProperty(b, "tables", { configurable: true, enumerable: true, writable: true, value: b.tables });
		}
		try {
			if (out != null && b.type) {
				const untouched = [];
				let firstT = -1, lastT = -1;
				const map = orig.map((m, k) => (m ? (m.type === "tag" ? "[" + String(m.parse?.primary?.tag ?? m.tag ?? "?") + "]" : m.type === "black" ? "b" : m.type === "table" ? "T" : m.type) : "-") + (touched[k] || (m?.type === "table" && tablesRead && origTables?.includes(m.block)) ? "*" : "")).join(" ");
				for (let k = 0; k < orig.length; k++) if (touched[k] || (orig[k]?.type === "table" && tablesRead && origTables?.includes(orig[k].block))) { if (firstT < 0) firstT = k; lastT = k; }
				for (let k = 0; k < orig.length; k++) {
					const m = orig[k]; if (!m) continue;
					const isT = touched[k] || (m.type === "table" && tablesRead && origTables?.includes(m.block));
					if (isT) continue;
					let kind = "skip", text = "", w = 0;
					if (m.type === "black") { text = String(m.text ?? "").replace(RED, " ").trim(); w = nw(words(text)); const mh = mediaInHtml(text, out); kind = mh === true ? "skip" : (mh === false && w < 3 ? "media-dropped" : (w >= 3 ? "prose" : "skip")); }
					else if (m.type === "table") { kind = "table"; }
					else if (m.type === "nested") { kind = "nested"; }
					else if (m.type === "tag") {
						const parse = m.parse, prim = parse?.primary;
						if (k === 0 && prim?.directive === "INTERACTIVE") continue;                      // the invocation tag (r354's note)
						if (parse && (parse.class === "instruction" || parse.instructionFragment)) continue;   // already the red note
						const tag = String(prim?.tag ?? m.tag ?? "").toLowerCase();
						const after = String(m.blackAfter ?? "").replace(RED, " ").trim(), line = String(m.text ?? "");
						text = after || line.replace(/\[[^\]]*\]/g, " ").trim(); w = nw(words(line) + " " + words(after));
						if (mediaTags.has(tag)) { const mh = mediaInHtml(line + " " + after + " " + (m.block?.links ?? []).map((l) => l?.target ?? "").join(" "), out); kind = mh === true ? "skip" : (mh === false ? "media-dropped" : "media-nourl"); }
						else if (headings.has(tag)) kind = "heading";
						else if (tag === "button") kind = "button";
						else if (tag === "body" || !prim || parse?.class === "noise") kind = w >= 3 ? "prose" : "skip";
						else kind = w >= 3 ? "tag:" + tag : "skip";
					}
					if (kind === "skip") continue;
					const pos = firstT < 0 ? "only" : (k < firstT ? "before" : (k > lastT ? "after" : "between"));
					untouched.push({ k, kind, pos, w, text: text.slice(0, 90), key: words(text) });
				}
				pending.push({ type: b.type, code: curMod, page: curPage, index: b.index, members: orig.length, touched: touched.filter(Boolean).length, tablesRead, map, untouched });
			}
		} catch (e) { errs++; lastErr = String(e && e.stack || e).slice(0, 300); }
		return out;
	};
	const codes = process.argv.slice(2).filter((a, i, arr) => !a.startsWith("--") && !/^\d+$/.test(a) && arr[i - 1] !== "--shard");
	const si = process.argv.indexOf("--shard"); let k = 0, list = codes;
	if (si > -1) { k = parseInt(process.argv[si + 1], 10); const n = parseInt(process.argv[si + 2], 10); list = codes.filter((_, i) => i % n === k); }
	for (const code of list) {
		curMod = code; pending = [];
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
			const pageText = {};
			for (const o of run.outputs.filter((o) => /\.html$/.test(o.filename))) {
				const html = String(o.content ?? "").replace(/<!--[\s\S]*?-->/g, " ").replace(/<script[\s\S]*?<\/script>/gi, " ");
				const attrs = [...html.matchAll(/(?:alt|title|aria-label|placeholder|data-caption)="([^"]*)"/g)].map((m) => m[1]).join(" ");
				pageText[o.filename] = norm(html.replace(/<[^>]+>/g, " ") + " " + attrs);
			}
			const allText = Object.values(pageText).join(" | ");
			for (const p of pending) {
				for (const u of p.untouched) {
					if (u.kind === "prose" || u.kind.startsWith("tag:") || u.kind === "heading" || u.kind === "button") {
						const key = u.key.replace(/^(?:\d+|[a-z]|[ivx]+)\s+/, "");
						u.lost = key ? !allText.includes(key) : false;
					}
					delete u.key;
				}
				recs.push(p);
			}
		} catch (e) { errs++; lastErr = String(e && e.stack || e).slice(0, 300); }
	}
	fs.writeFileSync(SHARD(k), JSON.stringify(recs));
	_l("shard", k, "->", list.length, "modules,", recs.length, "built bundles; errors", errs, lastErr);
}
main().catch((e) => { console.error(e); process.exit(1); });
