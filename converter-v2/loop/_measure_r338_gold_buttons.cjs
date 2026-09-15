/** _measure_r338_gold_buttons.cjs — ROUND 338 measurement, the REVERSE direction (session 7 Round 1 PICK).
 *
 *  For every gold `externalButton` (<a href…><div class="…externalButton…">LABEL</div></a>) on every gold page of
 *  every module the LIVE extractor can prepare, find its SOURCE in the Writers Template (run.wtBlocks):
 *    HREF   — a block whose hyperlink target equals the button's href (the sharp key)
 *    TEXT   — no href match, but a block whose visible text contains the button's label (the writer typed the
 *             label but the link was not a Word hyperlink, or the human re-hosted the URL)
 *    NONE   — neither (the human's own resource — class C, editorial)
 *  and record that source block's SIGNATURE: kind (para / table), the red tags on the paragraph, whether the
 *  hyperlink is the whole paragraph (STANDALONE) or sits in prose (INLINE), a list item, a bare URL, and what
 *  Claude ships today for the same key. The point: which WT signature PREDICTS a gold button, at what precision,
 *  so the class can be sized honestly per template / subject family (LOOP §1b, §3 step 3).
 *
 *  Run from reference/tests under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r338_gold_buttons.cjs [CODES…]
 *  Writes outputs/_r338_gold_buttons.json and prints the summary.
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const OUT = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const META = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "pageforge-site", "converter-v2", "data", "Module_Structure_Index.json"), "utf8")).module_meta || {};
const argCodes = process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.replace(/\r/g, "").trim()).filter(Boolean);

const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
const unent = (s) => String(s ?? "").replace(/&amp;/g, "&").replace(/&#(\d+);/g, (m, n) => String.fromCharCode(+n)).replace(/&nbsp;/g, " ").replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">");
const normText = (s) => unent(s).toLowerCase().replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/[^\p{L}\p{N}]+/gu, " ").trim();
const normHref = (h) => unent(h).trim().toLowerCase().replace(/^https?:\/\//, "").replace(/^www\./, "").replace(/#.*$/, "").replace(/\/+$/, "");
const visibleText = (raw) => String(raw ?? "").replace(RED, " ").replace(/\*\*|__|(?<!\*)\*(?!\*)/g, "").replace(/\s+/g, " ").trim();
const stripTrailPunct = (s) => s.replace(/[\s.:;,!?)\]]+$/u, "").replace(/^[(\[]+/u, "").trim();
const isUrl = (t) => /^(?:https?:\/\/|www\.)/i.test(String(t ?? "").trim());

function readPages(dir) {
	const out = [];
	if (!dir || !fs.existsSync(dir)) return out;
	for (const f of fs.readdirSync(dir).sort()) if (/\.html?$/i.test(f)) out.push([f, fs.readFileSync(path.join(dir, f), "utf8")]);
	return out;
}

/** The WT-side signature of a para block for one of its links. */
function paraSig(b, target) {
	const raw = String(b.text ?? "");
	const tags = [...raw.matchAll(RED)].map((m) => m[1].trim()).filter(Boolean);
	const vis = stripTrailPunct(visibleText(raw));
	const linkText = b.links.map((l) => String(l.text ?? "")).join("");
	const standalone = vis.length > 0 && normText(vis) === normText(stripTrailPunct(visibleText(linkText)));
	const label = b.links.filter((l) => normHref(l.target) === normHref(target)).map((l) => l.text).join("");
	return { kind: "para", tags: tags.length ? tags.slice(0, 4) : null, tag0: tags.length ? tags[0].toLowerCase().replace(/[^a-z ]/g, "").trim().split(" ").slice(0, 3).join(" ") : "",
		position: standalone ? "STANDALONE" : "INLINE", list: b.list ?? null, bareUrl: isUrl(label), linkText: String(label).trim().slice(0, 120), para: vis.slice(0, 160), wtPage: b.wtPage };
}

function claudeForm(pages, href, label) {
	const hN = normHref(href), lN = normText(label);
	let best = "ABSENT"; const rank = { BUTTON: 6, BUTTON_PLAIN: 5, A: 3, PLAIN: 2, ABSENT: 1 };
	for (const [, html] of pages) {
		const re = /<a\b([^>]*)>([\s\S]*?)<\/a>/gi; let m;
		while ((m = re.exec(html))) {
			const ah = normHref(m[1].match(/href="([^"]*)"/i)?.[1] ?? ""), it = normText(m[2].replace(/<[^>]+>/g, " "));
			if (!((hN && ah === hN) || (lN && it === lN))) continue;
			const dc = m[2].match(/<div class="([^"]*)"/i)?.[1] ?? "";
			const f = /\bexternalButton\b/.test(dc) ? "BUTTON" : /\bbutton\b/.test(dc) ? "BUTTON_PLAIN" : "A";
			if (rank[f] > rank[best]) best = f;
		}
		if (rank[best] < rank.PLAIN && lN.length >= 4 && normText(html.replace(/<[^>]+>/g, " ")).includes(" " + lN + " ")) best = "PLAIN";
	}
	return best;
}

async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const codes = argCodes.length ? argCodes : corpus.mods(MODS);
	const rows = []; let nMods = 0, nPrepFail = 0;
	for (const code of codes) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		const goldPages = readPages(base);
		const buttons = [];
		for (const [file, html] of goldPages) {
			// skip the acks block
			const body = html.split(/<div[^>]*class="[^"]*acks[^"]*"/i)[0];
			const re = /<a\b([^>]*)>\s*<div class="([^"]*externalButton[^"]*)">([\s\S]*?)<\/div>\s*<\/a>/gi; let m;
			while ((m = re.exec(body))) buttons.push({ file, href: unent(m[1].match(/href="([^"]*)"/i)?.[1] ?? ""), cls: m[2], label: m[3].replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim() });
		}
		if (!buttons.length) continue;
		const run = new ConversionRun({ imageMode: "P" });
		const docs = [];
		for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(base, name));
			const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
			try { docs.push({ name, doc: await DocxExtractor.Extract(zip) }); } catch (e) { /* noted below via prep */ }
		}
		const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f) && !/_parsed\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
		let prep; try { prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles }); } catch (e) { prep = { ok: false, reason: e && e.message }; }
		const meta = META[code] || {};
		if (!prep || !prep.ok) { nPrepFail++; for (const b of buttons) rows.push({ code, template: meta.template_type ?? "?", subject: meta.subject ?? "?", prefix: meta.prefix ?? code.replace(/\d.*$/, ""), ...b, source: "NOPREP" }); continue; }
		nMods++;
		let claudeDir = null; try { claudeDir = corpus.mdir(OUT, code); if (!fs.existsSync(claudeDir)) claudeDir = null; } catch { claudeDir = null; }
		const claudePages = readPages(claudeDir);
		for (const b of buttons) {
			const hN = normHref(b.href), lN = normText(b.label);
			let src = null;
			// HREF match first
			for (const blk of run.wtBlocks) {
				if (!blk || !Array.isArray(blk.links) || !blk.links.length) continue;
				const lk = blk.links.find((l) => normHref(l.target) === hN && hN);
				if (!lk) continue;
				src = blk.kind === "table" ? { kind: "table", wtPage: blk.wtPage, linkText: String(lk.text ?? "").slice(0, 120) } : paraSig(blk, lk.target);
				src.match = "HREF"; break;
			}
			if (!src && lN.length >= 3) {
				for (const blk of run.wtBlocks) {
					const vis = blk.kind === "table" ? normText(String(blk.text ?? "").replace(RED, " ")) : normText(visibleText(String(blk.text ?? "")));
					if (!vis || !(" " + vis + " ").includes(" " + lN + " ")) continue;
					src = blk.kind === "table" ? { kind: "table", wtPage: blk.wtPage } : paraSig(blk, "");
					src.match = "TEXT"; src.hasLinks = !!(blk.links && blk.links.length); break;
				}
			}
			if (!src) src = { match: "NONE" };
			rows.push({ code, template: meta.template_type ?? "?", subject: meta.subject ?? "?", prefix: meta.prefix ?? code.replace(/\d.*$/, ""), ...b, source: src.match, sig: src, claude: claudeForm(claudePages, b.href, b.label) });
		}
	}
	fs.writeFileSync(path.join(__dirname, "_r338_gold_buttons.json"), JSON.stringify({ generated: new Date().toISOString(), modules: nMods, prepFail: nPrepFail, buttons: rows }, null, 1));
	// ---- summary
	const cnt = (rs, f) => rs.filter(f).length;
	_l(`gold externalButtons ${rows.length} on ${new Set(rows.map((r) => r.code + "/" + r.file)).size} pages / ${new Set(rows.map((r) => r.code)).size} modules (prepared ${nMods}, prep refused ${nPrepFail})`);
	_l(`  source: HREF ${cnt(rows, (r) => r.source === "HREF")} · TEXT-only ${cnt(rows, (r) => r.source === "TEXT")} · NONE ${cnt(rows, (r) => r.source === "NONE")} · NOPREP ${cnt(rows, (r) => r.source === "NOPREP")}`);
	const sigKey = (r) => !r.sig || r.source === "NONE" || r.source === "NOPREP" ? r.source : r.sig.kind === "table" ? `${r.source}/table` : `${r.source}/para/${r.sig.tags ? "[" + r.sig.tag0 + "]" : "untagged"}/${r.sig.position}${r.sig.list ? "/list" : ""}${r.sig.bareUrl ? "/URL" : ""}`;
	const bySig = {}; for (const r of rows) (bySig[sigKey(r)] ??= []).push(r);
	_l("\n== gold buttons by WT source signature (count · pages · modules · Claude today) ==");
	for (const [k, rs] of Object.entries(bySig).sort((a, b) => b[1].length - a[1].length)) {
		const c = {}; for (const r of rs) c[r.claude ?? "?"] = (c[r.claude ?? "?"] ?? 0) + 1;
		_l(`  ${k.padEnd(58)} ${String(rs.length).padStart(4)} · ${String(new Set(rs.map((r) => r.code + "/" + r.file)).size).padStart(3)} pages · ${String(new Set(rs.map((r) => r.code)).size).padStart(3)} mods · claude ${JSON.stringify(c)}`);
	}
	_l("\n== label vs the writer's link text (HREF-sourced para buttons) ==");
	const hp = rows.filter((r) => r.source === "HREF" && r.sig && r.sig.kind === "para");
	let same = 0, goto = 0, other = 0, url = 0; const ex = [];
	for (const r of hp) { const g = normText(r.label), w = normText(r.sig.linkText); if (r.sig.bareUrl) url++; else if (g === w) same++; else if (/^go to /.test(g)) goto++; else { other++; if (ex.length < 15) ex.push(`${r.code} ${r.file}: "${r.sig.linkText.slice(0, 60)}" → "${r.label}"  [${r.sig.tags ? r.sig.tags.join(" | ").slice(0, 50) : "untagged"}] ${r.sig.position}`); } }
	_l(`  same ${same} · "Go to …" ${goto} · other ${other} · writer link is a bare URL ${url}`);
	for (const e of ex) _l("    " + e);
	_l("\n== by template (all gold buttons: HREF / TEXT / NONE) ==");
	for (const t of ["Standard", "Inquiry", "Fundamentals", "Bilingual", "?"]) { const rs = rows.filter((r) => r.template === t); if (rs.length) _l(`  ${t.padEnd(14)} ${rs.length} · HREF ${cnt(rs, (r) => r.source === "HREF")} · TEXT ${cnt(rs, (r) => r.source === "TEXT")} · NONE ${cnt(rs, (r) => r.source === "NONE")}`); }
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e) + "\n"); process.exit(1); });
