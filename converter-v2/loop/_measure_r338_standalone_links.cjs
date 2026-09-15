/** _measure_r338_standalone_links.cjs — ROUND 338 measurement (the autonomous loop, session 7 Round 1 PICK).
 *
 *  THE CLASS: an UNTAGGED hyperlink the writer gave its own paragraph (the paragraph's visible text IS the
 *  hyperlink phrase — nothing else, no red tag) — KB constraint 75's "position decides, not the tag": a link
 *  on its own line is a call to action and renders <a href target=_blank><div class="externalButton">…</div></a>;
 *  a link inside prose / a list item / a table cell stays an inline <a>. Claude today ships every untagged
 *  hyperlink as the round-74 weave (<p><a href>phrase</a></p>), tagged ones through r76/r88/r326.
 *
 *  THE INSTRUMENT: the LIVE extractor (DocxExtractor.Extract → ModuleResolver.PrepareRun → run.wtBlocks), never
 *  the _parsed.txt dumps (they do not carry block.links). For every para block that carries a hyperlink:
 *    standalone = the paragraph's visible text (red spans removed, markdown markers stripped, trailing
 *                 punctuation dropped) equals the concatenated link text(s)
 *    tagged     = the paragraph carries any red span ([external link], [button], [video], [H3] …)
 *    list       = the paragraph is a Word list item (bullet / number)
 *    bareUrl    = the link text is itself a URL
 *  and for each instance the GOLD's form on that module's pages (matched by href OR by label text):
 *    BUTTON      <a href…><div class="…externalButton…">LABEL</div></a>   (the KB form)
 *    BUTTON_PLAIN <a href…><div class="button…">LABEL</div></a>           (the r326 call-to-action form)
 *    STANDALONE_A <p><a href…>text</a></p>                                (the anchor alone in its paragraph)
 *    INLINE_A     <a href…>text</a> inside other text
 *    PLAIN        the label text is on the page but not linked
 *    ABSENT       neither the href nor the label is on any gold page
 *  plus Claude's current form on the same key. Reported per template family and subject family (LOOP §1b),
 *  standalone vs inline vs list vs tagged, so the discriminator is validated on BOTH halves.
 *
 *  Run from reference/tests under WSL:
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r338_standalone_links.cjs [CODES…]
 *  Writes outputs/_r338_standalone_links.json (every instance) and prints the summary.
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
const normText = (s) => String(s ?? "").replace(/&amp;/g, "&").replace(/&#(\d+);/g, (m, n) => String.fromCharCode(+n))
	.replace(/&nbsp;/g, " ").toLowerCase().replace(/[‘’]/g, "'").replace(/[“”]/g, '"')
	.replace(/[^\p{L}\p{N}]+/gu, " ").trim();
const normHref = (h) => String(h ?? "").replace(/&amp;/g, "&").trim().toLowerCase()
	.replace(/^https?:\/\//, "").replace(/^www\./, "").replace(/#.*$/, "").replace(/\/+$/, "");
const visibleText = (raw) => String(raw ?? "").replace(RED, " ").replace(/\*\*|__|(?<!\*)\*(?!\*)/g, "")
	.replace(/\s+/g, " ").trim();
const stripTrailPunct = (s) => s.replace(/[\s.:;,!?)\]]+$/u, "").replace(/^[(\[]+/u, "").trim();
const isUrl = (t) => /^(?:https?:\/\/|www\.)/i.test(String(t ?? "").trim());
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/** Classify how a page renders a link: by href first (the sharper key), then by label text. */
function classifyOnPages(pages, href, label) {
	const hN = normHref(href), lN = normText(label);
	let best = null;   // rank: BUTTON > BUTTON_PLAIN > STANDALONE_A > INLINE_A > PLAIN > ABSENT
	const rank = { BUTTON: 6, BUTTON_PLAIN: 5, STANDALONE_A: 4, INLINE_A: 3, PLAIN: 2, ABSENT: 1 };
	const take = (form, extra) => { if (!best || rank[form] > rank[best.form]) best = { form, ...extra }; };
	for (const [file, html] of pages) {
		// every anchor on the page
		const re = /<a\b([^>]*)>([\s\S]*?)<\/a>/gi; let m;
		while ((m = re.exec(html))) {
			const attrs = m[1], inner = m[2];
			const ah = normHref(attrs.match(/href="([^"]*)"/i)?.[1] ?? "");
			const innerText = normText(inner.replace(/<[^>]+>/g, " "));
			const hrefHit = hN && ah && (ah === hN);
			const textHit = lN && innerText && (innerText === lN);
			if (!hrefHit && !textHit) continue;
			const divClass = inner.match(/<div class="([^"]*)"/i)?.[1] ?? "";
			const label = inner.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
			if (/\bexternalButton\b/.test(divClass)) { take("BUTTON", { file, cls: divClass, goldLabel: label, by: hrefHit ? "href" : "text" }); continue; }
			if (/\bbutton\b/.test(divClass)) { take("BUTTON_PLAIN", { file, cls: divClass, goldLabel: label, by: hrefHit ? "href" : "text" }); continue; }
			// standalone: the anchor is the whole content of its <p> (or <h*>/<li>)
			const before = html.slice(Math.max(0, m.index - 200), m.index), after = html.slice(re.lastIndex, re.lastIndex + 200);
			const openTag = before.match(/<(p|li|h[1-6]|div)\b[^>]*>\s*(?:<b>|<strong>|<i>)?\s*$/i);
			const closeTag = after.match(/^\s*(?:<\/b>|<\/strong>|<\/i>)?\s*[.]?\s*<\/(p|li|h[1-6]|div)>/i);
			if (openTag && closeTag && openTag[1].toLowerCase() === closeTag[1].toLowerCase()) take("STANDALONE_A", { file, wrap: openTag[1].toLowerCase(), goldLabel: label, by: hrefHit ? "href" : "text" });
			else take("INLINE_A", { file, goldLabel: label, by: hrefHit ? "href" : "text" });
		}
		if ((!best || rank[best.form] < rank.PLAIN) && lN && lN.length >= 4) {
			const bodyText = normText(html.replace(/<script[\s\S]*?<\/script>/gi, " ").replace(/<[^>]+>/g, " "));
			if (bodyText.includes(" " + lN + " ") || bodyText.startsWith(lN + " ") || bodyText.endsWith(" " + lN)) take("PLAIN", { file });
		}
	}
	return best ?? { form: "ABSENT" };
}

function readPages(dir) {
	const out = [];
	if (!dir || !fs.existsSync(dir)) return out;
	for (const f of fs.readdirSync(dir)) if (/\.html?$/i.test(f)) out.push([f, fs.readFileSync(path.join(dir, f), "utf8")]);
	return out;
}

async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const codes = argCodes.length ? argCodes : corpus.mods(MODS);
	const inst = [];
	let nMods = 0, nNoGold = 0, nPrepFail = 0;
	for (const code of codes) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { nNoGold++; continue; }
		const run = new ConversionRun({ imageMode: "P" });
		const docs = [];
		for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(base, name));
			const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
			try { docs.push({ name, doc: await DocxExtractor.Extract(zip) }); } catch (e) { _l(`${code}: extract error ${name}: ${e && e.message}`); }
		}
		const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f) && !/_parsed\.txt$/i.test(f))
			.map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
		let prep; try { prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles }); } catch (e) { prep = { ok: false, reason: e && e.message }; }
		if (!prep || !prep.ok) { nPrepFail++; _l(`${code}: prep refused (${prep && prep.reason})`); continue; }
		nMods++;
		const goldPages = readPages(base);
		let claudeDir = null; try { claudeDir = corpus.mdir(OUT, code); if (!fs.existsSync(claudeDir)) claudeDir = null; } catch { claudeDir = null; }
		const claudePages = readPages(claudeDir);
		const meta = META[code] || {};
		for (const b of run.wtBlocks) {
			if (!b || !Array.isArray(b.links) || !b.links.length) continue;
			if (b.kind === "table") {
				for (const lk of b.links) {
					const g = classifyOnPages(goldPages, lk.target, lk.text);
					inst.push({ code, template: meta.template_type ?? "?", subject: meta.subject ?? "?", prefix: meta.prefix ?? code.replace(/\d.*$/, ""),
						wtPage: b.wtPage, position: "TABLE", tagged: null, list: null, bareUrl: isUrl(lk.text), text: String(lk.text ?? "").trim().slice(0, 120),
						target: String(lk.target ?? "").slice(0, 200), gold: g, claude: classifyOnPages(claudePages, lk.target, lk.text) });
				}
				continue;
			}
			const raw = String(b.text ?? "");
			const tags = [...raw.matchAll(RED)].map((m) => m[1].trim()).filter(Boolean);
			const vis = stripTrailPunct(visibleText(raw));
			const linkText = b.links.map((l) => String(l.text ?? "")).join("");
			const linkVis = stripTrailPunct(visibleText(linkText));
			const standalone = vis.length > 0 && normText(vis) === normText(linkVis);
			// one instance per DISTINCT target in the paragraph (a phrase split across runs shares one target)
			const seen = new Set();
			for (const lk of b.links) {
				const key = normHref(lk.target); if (!key || seen.has(key)) continue; seen.add(key);
				const label = b.links.filter((l) => normHref(l.target) === key).map((l) => l.text).join("");
				const position = standalone ? "STANDALONE" : "INLINE";
				const g = classifyOnPages(goldPages, lk.target, label);
				const c = classifyOnPages(claudePages, lk.target, label);
				inst.push({ code, template: meta.template_type ?? "?", subject: meta.subject ?? "?", prefix: meta.prefix ?? code.replace(/\d.*$/, ""),
					wtPage: b.wtPage, position, tagged: tags.length ? tags.slice(0, 4) : null, list: b.list ?? null, bareUrl: isUrl(label),
					text: String(label ?? "").trim().slice(0, 120), para: vis.slice(0, 160), target: String(lk.target ?? "").slice(0, 200), gold: g, claude: c });
			}
		}
	}
	fs.writeFileSync(path.join(__dirname, "_r338_standalone_links.json"), JSON.stringify({ generated: new Date().toISOString(), modules: nMods, noGold: nNoGold, prepFail: nPrepFail, instances: inst }, null, 1));

	// ---- summary --------------------------------------------------------------------------------------------
	const forms = ["BUTTON", "BUTTON_PLAIN", "STANDALONE_A", "INLINE_A", "PLAIN", "ABSENT"];
	const tally = (rows, label) => {
		const c = Object.fromEntries(forms.map((f) => [f, 0]));
		for (const r of rows) c[r.gold.form]++;
		const found = rows.length - c.ABSENT;
		const pages = new Set(rows.filter((r) => r.gold.file).map((r) => r.code + "/" + r.gold.file)).size;
		const mods = new Set(rows.map((r) => r.code)).size;
		const btn = c.BUTTON + c.BUTTON_PLAIN;
		_l(`${label.padEnd(44)} n=${String(rows.length).padStart(4)} mods=${String(mods).padStart(3)} goldpages=${String(pages).padStart(3)} | BTN ${c.BUTTON} +plain ${c.BUTTON_PLAIN} | stdA ${c.STANDALONE_A} inlA ${c.INLINE_A} plain ${c.PLAIN} absent ${c.ABSENT} | button share (of found) ${found ? (btn / found).toFixed(3) : "-"} (of all) ${rows.length ? (btn / rows.length).toFixed(3) : "-"}`);
	};
	const para = inst.filter((r) => r.position !== "TABLE");
	const untagged = para.filter((r) => !r.tagged);
	_l(`\nmodules prepared ${nMods} (no gold dir ${nNoGold}, prep refused ${nPrepFail}); hyperlink instances ${inst.length} (para ${para.length}, table ${inst.length - para.length})\n`);
	_l("== THE CLASS: UNTAGGED hyperlink paragraphs, by position ==");
	tally(untagged.filter((r) => r.position === "STANDALONE" && !r.list && !r.bareUrl), "STANDALONE phrase (not list, not URL)");
	tally(untagged.filter((r) => r.position === "STANDALONE" && !r.list && r.bareUrl), "STANDALONE bare URL (not list)");
	tally(untagged.filter((r) => r.position === "STANDALONE" && r.list), "STANDALONE inside a list item");
	tally(untagged.filter((r) => r.position === "INLINE" && !r.list), "INLINE in prose (not list)");
	tally(untagged.filter((r) => r.position === "INLINE" && r.list), "INLINE in a list item");
	tally(inst.filter((r) => r.position === "TABLE"), "TABLE cell");
	_l("\n== TAGGED hyperlink paragraphs (other rounds own these), by first tag ==");
	const byTag = {};
	for (const r of para.filter((r) => r.tagged)) { const t = r.tagged[0].toLowerCase().replace(/[^a-z ]/g, "").trim().split(" ").slice(0, 3).join(" "); (byTag[t] ??= []).push(r); }
	for (const [t, rows] of Object.entries(byTag).sort((a, b) => b[1].length - a[1].length).slice(0, 14)) tally(rows, `  [${t}] ${rows.filter((r) => r.position === "STANDALONE").length} standalone`);
	_l("\n== THE CLASS by TEMPLATE family (standalone phrase, untagged, not list) ==");
	const cls = untagged.filter((r) => r.position === "STANDALONE" && !r.list && !r.bareUrl);
	for (const t of ["Standard", "Inquiry", "Fundamentals", "Bilingual", "?"]) { const rows = cls.filter((r) => r.template === t); if (rows.length) tally(rows, `  ${t}`); }
	_l("\n== THE CLASS by SUBJECT family (≥ 8 instances) ==");
	const bySub = {}; for (const r of cls) (bySub[r.subject] ??= []).push(r);
	for (const [s, rows] of Object.entries(bySub).sort((a, b) => b[1].length - a[1].length)) if (rows.length >= 8) tally(rows, `  ${s}`);
	_l("\n== THE CLASS by PREFIX (≥ 6 instances) ==");
	const byPre = {}; for (const r of cls) (byPre[r.prefix] ??= []).push(r);
	for (const [s, rows] of Object.entries(byPre).sort((a, b) => b[1].length - a[1].length)) if (rows.length >= 6) tally(rows, `  ${s}`);
	_l("\n== Gold BUTTON label vs the writer's phrase (the class, gold BUTTON) ==");
	const btnRows = cls.filter((r) => r.gold.form === "BUTTON" || r.gold.form === "BUTTON_PLAIN");
	let same = 0, goto = 0, other = 0; const others = [];
	for (const r of btnRows) { const gl = normText(r.gold.goldLabel), wl = normText(r.text); if (gl === wl) same++; else if (/^go to /.test(gl)) goto++; else { other++; if (others.length < 12) others.push(`${r.code}: "${r.text}" → "${r.gold.goldLabel}"`); } }
	_l(`  same as writer ${same} / "Go to …" ${goto} / other ${other}`); for (const o of others) _l("    " + o);
	_l("\n== Claude's CURRENT form on the class ==");
	const cc = Object.fromEntries(forms.map((f) => [f, 0])); for (const r of cls) cc[r.claude.form]++; _l("  " + JSON.stringify(cc));
	_l("\n== Class matched by HREF vs by TEXT only (gold BUTTON) ==");
	_l(`  by href ${btnRows.filter((r) => r.gold.by === "href").length} / by text ${btnRows.filter((r) => r.gold.by === "text").length}`);
	const byMod = {}; for (const r of cls) (byMod[r.code] ??= []).push(r);
	_l(`\nclass modules ${Object.keys(byMod).length}; class pages (gold, found) ${new Set(cls.filter((r) => r.gold.file).map((r) => r.code + "/" + r.gold.file)).size}`);
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e) + "\n"); process.exit(1); });
