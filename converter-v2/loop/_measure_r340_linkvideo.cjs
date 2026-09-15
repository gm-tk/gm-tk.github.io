/** _measure_r340_linkvideo.cjs — ROUND 340 PICK measurement (session 7 Round 3).
 *
 *  THE CLASS: a paragraph tagged with the EXTERNAL-LINK family (`[link]`, `[url]`, `[website]`, `[external link]`, `[external link
 *  button]`) — NOT a button-family tag — whose URL is a VIDEO url (youtube watch / shorts / embed, youtu.be, vimeo id). The r339 rule
 *  excluded this family by design; the r339 residue verifier found 46 anchored buttons with a video href on those emitters. The
 *  question: does the gold EMBED such a link (videoSection) or keep it a button / inline anchor?
 *
 *  For every WT (live extractor → run.wtBlocks): every para block whose red spans resolve (by alias fold) to the external-link family
 *  and which carries a video url (own links or text); record (a) the block's own visible text minus the url (standalone vs prose),
 *  (b) the PRECEDING block's text — does it name a video / watch / play?, (c) whether the preceding block is an [embed]/[video]-family
 *  tag with NO own url (the HIS1006 shape), (d) the gold's form for that video id on the module's pages (EMBED / BUTTON / ANCHOR /
 *  ABSENT) and Claude's.
 *
 *  Run from reference/tests under WSL:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r340_linkvideo.cjs
 *  Writes outputs/_r340_linkvideo.json and prints the summary.
 */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const OUT = path.join(__dirname, "..", "..", "01-Claude_Modules_");
const META = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "pageforge-site", "converter-v2", "data", "Module_Structure_Index.json"), "utf8")).module_meta || {};
const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
const VID = /(?:youtube\.com\/(?:watch\?(?:[^ ]*&)?v=|shorts\/|embed\/)|youtu\.be\/|youtube-nocookie\.com\/embed\/|vimeo\.com\/(?:video\/)?)([A-Za-z0-9_-]{6,})/i;
const URL = /https?:\/\/[^\s\]]+/;
const vidOf = (s) => (String(s ?? "").match(VID) || [])[1] || null;
function tagsOf(b) { return [...String(b.text ?? "").matchAll(RED)].map((m) => m[1].trim()).filter(Boolean); }
function urlsOf(b) {
	const out = [];
	for (const l of (b.links ?? [])) if (l?.target) out.push(l.target);
	const m = String(b.text ?? "").replace(RED, " ").match(URL); if (m) out.push(m[0]);
	return out;
}
function readPages(dir) { const out = []; if (!dir || !fs.existsSync(dir)) return out; for (const f of fs.readdirSync(dir)) if (/\.html?$/i.test(f)) out.push([f, fs.readFileSync(path.join(dir, f), "utf8")]); return out; }
function goldForm(pages, id) {
	if (!id) return "NOID";
	let best = "ABSENT";
	for (const [f, h] of pages) {
		let i = -1;
		while ((i = h.indexOf(id, i + 1)) >= 0) {
			const seg = h.slice(Math.max(0, i - 700), i + 200);
			if (/<iframe|videoSection/i.test(seg)) return "EMBED";
			if (/externalButton|class="button/i.test(seg)) best = "BUTTON";
			else if (/<a [^>]*href="[^"]*$/i.test(h.slice(Math.max(0, i - 300), i)) || /<a\s/i.test(seg)) { if (best === "ABSENT") best = "ANCHOR"; }
			else if (best === "ABSENT") best = "OTHER";
		}
	}
	return best;
}
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
	const lex = DataService.Data.TagLexicon.tags || {};
	const linkAliases = new Set(), buttonAliases = new Set(), mediaAliases = new Set();
	for (const [canon, def] of Object.entries(lex)) {
		const al = (def.aliases ?? [canon]).map((a) => a.toLowerCase());
		if (canon === "external link" || canon === "external link button") for (const a of al) linkAliases.add(a);
		if (/button/.test(canon)) for (const a of al) buttonAliases.add(a);
		if (canon === "video" || canon === "embed" || canon === "audio") for (const a of al) mediaAliases.add(a);
	}
	const fold = (s) => String(s ?? "").toLowerCase().replace(/[\[\]]/g, " ").replace(/[:\-–—]+/g, " ").replace(/\s+/g, " ").trim();
	const head = (t) => { const f = fold(t); return f.split(" ").slice(0, 3).join(" "); };
	const isLinkTag = (t) => { const f = fold(t); return [...linkAliases].some((a) => f === a || f.startsWith(a + " ")) ; };
	const isButtonTag = (t) => { const f = fold(t); return /\bbutton\b/.test(f) && ![...linkAliases].some((a) => f === a); };
	const isMediaTag = (t) => { const f = fold(t); return [...mediaAliases].some((a) => f === a || f.startsWith(a + " ")) || /\b(video|embed)\b/.test(f); };
	const rows = [];
	for (const code of corpus.mods(MODS)) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		const run = new ConversionRun({ imageMode: "P" }); const docs = [];
		for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(base, name)); const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
			try { docs.push({ name, doc: await DocxExtractor.Extract(zip) }); } catch { }
		}
		let prep; try { prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles: [] }); } catch (e) { prep = { ok: false }; }
		if (!prep || !prep.ok) continue;
		const goldPages = readPages(base); const meta = META[code] || {};
		let claudeDir = null; try { claudeDir = corpus.mdir(OUT, code); if (!fs.existsSync(claudeDir)) claudeDir = null; } catch { }
		const claudePages = readPages(claudeDir);
		const blocks = run.wtBlocks;
		for (let k = 0; k < blocks.length; k++) {
			const b = blocks[k]; if (!b || b.kind !== "para") continue;
			const tags = tagsOf(b); if (!tags.length) continue;
			const lt = tags.find(isLinkTag); if (!lt) continue;
			if (tags.some(isButtonTag) && !/external link button|link button|external button/.test(fold(lt))) continue;   // the r339 class
			const url = urlsOf(b).find((u) => vidOf(u)); if (!url) continue;
			const id = vidOf(url);
			const vis = String(b.text ?? "").replace(RED, " ").replace(URL, " ").replace(/\*/g, "").replace(/\s+/g, " ").trim();
			const words = vis ? vis.split(" ").length : 0;
			// preceding non-empty block
			let p = k - 1; while (p >= 0 && blocks[p] && blocks[p].kind === "para" && !String(blocks[p].text ?? "").trim()) p--;
			const pb = p >= 0 ? blocks[p] : null; const ptags = pb && pb.kind === "para" ? tagsOf(pb) : [];
			const ptext = pb && pb.kind === "para" ? String(pb.text ?? "").replace(RED, " ").replace(/\s+/g, " ").trim() : "";
			const prevMediaTagNoUrl = ptags.some(isMediaTag) && !urlsOf(pb).length;
			const prevWatch = /\b(watch|play|video|clip|film|listen)\b/i.test(ptext) || ptags.some((t) => /\b(watch|play|video|clip|film|embed)\b/i.test(t));
			const linkKind = /external link button|link button|external button/.test(fold(lt)) ? "link-button" : "link";
			rows.push({ code, template: meta.template_type ?? "?", subject: meta.subject ?? "?", wtPage: b.wtPage, linkKind, tag: lt.slice(0, 60), words, vis: vis.slice(0, 80),
				standalone: words <= 8, prevMediaTagNoUrl, prevWatch, prevTag: ptags[0] ? ptags[0].slice(0, 40) : null, prevText: ptext.slice(0, 80),
				url: url.slice(0, 100), id, gold: goldForm(goldPages, id), claude: goldForm(claudePages, id) });
		}
	}
	fs.writeFileSync(path.join(__dirname, "_r340_linkvideo.json"), JSON.stringify({ generated: new Date().toISOString(), rows }, null, 1));
	const tally = (label, rs) => { const c = {}; for (const r of rs) c[r.gold] = (c[r.gold] ?? 0) + 1; const cc = {}; for (const r of rs) cc[r.claude] = (cc[r.claude] ?? 0) + 1; const found = rs.length - (c.ABSENT ?? 0) - (c.NOID ?? 0); _l(`${label.padEnd(44)} n=${String(rs.length).padStart(3)} mods=${String(new Set(rs.map((r) => r.code)).size).padStart(3)} | gold ${JSON.stringify(c)} embed/found ${found ? ((c.EMBED ?? 0) / found).toFixed(2) : "-"} | claude ${JSON.stringify(cc)}`); };
	_l(`external-link-family blocks carrying a VIDEO url: ${rows.length} in ${new Set(rows.map((r) => r.code)).size} modules`);
	tally("ALL", rows);
	tally("  link tag (INLINE family)", rows.filter((r) => r.linkKind === "link")); tally("  link-button tag (ELEMENT family)", rows.filter((r) => r.linkKind === "link-button"));
	_l("\nby standalone-ness (visible words minus url):"); tally("  standalone (<= 8 words)", rows.filter((r) => r.standalone)); tally("  prose (> 8 words)", rows.filter((r) => !r.standalone));
	_l("\nstandalone, by what PRECEDES the link:");
	tally("  prev = media tag with NO own url", rows.filter((r) => r.standalone && r.prevMediaTagNoUrl));
	tally("  prev names watch/play/video/clip", rows.filter((r) => r.standalone && !r.prevMediaTagNoUrl && r.prevWatch));
	tally("  prev neither", rows.filter((r) => r.standalone && !r.prevMediaTagNoUrl && !r.prevWatch));
	_l("\nstandalone, by template:"); for (const t of ["Standard", "Inquiry", "Fundamentals", "Bilingual"]) { const rs = rows.filter((r) => r.standalone && r.template === t); if (rs.length) tally("  " + t, rs); }
	_l("\nstandalone, by subject (n >= 4):"); const bs = {}; for (const r of rows.filter((r) => r.standalone)) (bs[r.subject] ??= []).push(r); for (const [s, rs] of Object.entries(bs).sort((a, b) => b[1].length - a[1].length)) if (rs.length >= 4) tally("  " + s.slice(0, 40), rs);
	_l("\nstandalone, by visible-word count:"); for (const w of [0, 1, 2, 3, 4]) { const rs = rows.filter((r) => r.standalone && (w < 4 ? r.words === w : r.words >= 4)); if (rs.length) tally("  words " + (w < 4 ? w : ">=4"), rs); }
	_l("\ntag spellings (top 10):"); const bt = {}; for (const r of rows) (bt[fold(r.tag).replace(/\d+/g, "N")] ??= []).push(r); for (const [l, rs] of Object.entries(bt).sort((a, b) => b[1].length - a[1].length).slice(0, 10)) tally("  " + JSON.stringify(l).slice(0, 42), rs);
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e) + "\n"); process.exit(1); });
