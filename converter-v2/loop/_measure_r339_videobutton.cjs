/** _measure_r339_videobutton.cjs — ROUND 339 PICK measurement (session 7 Round 2).
 *
 *  THE CLASS: a `[button]`-family tag that ends up carrying a VIDEO-HOST URL (youtube / youtu.be / vimeo) — the writer's
 *  "[Button] Play video" + "[video link] URL", "[Button: youtube-url]", or an instruction line containing the word
 *  "button" ("[Please embed this video with a play button …]") followed by the video link. Claude ships an anchored
 *  button (r88 absorb / r326 anchor; r338 → externalButton "Go to video"); the gold EMBEDS the video (videoSection).
 *
 *  For every WT (live extractor → run.wtBlocks → PageSplitter item stream would be ideal, but the block level is enough
 *  here): every para block whose red spans include a button-family tag; record (a) a video URL inside the block itself,
 *  (b) the NEXT block being a [video]-family tagged block with a video URL, (c) the next block a bare video URL; and the
 *  gold's form for that video id on the module's pages (EMBED = iframe/videoSection carrying the id; BUTTON = an anchored
 *  button with the id; ABSENT). Also the tag's own bracket text (to see the instruction-as-button mis-read).
 *
 *  Run from reference/tests under WSL:  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_measure_r339_videobutton.cjs
 *  Writes outputs/_r339_videobutton.json and prints the summary.
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
const VID = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube-nocookie\.com\/embed\/|vimeo\.com\/(?:video\/)?)([A-Za-z0-9_-]{6,})/i;
const URL = /https?:\/\/[^\s\]]+/;
const vidOf = (s) => (String(s ?? "").match(VID) || [])[1] || null;
const isVideoHost = (u) => /youtu\.?be|youtube|vimeo/i.test(String(u ?? ""));
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
	const buttonAliases = new Set(); const videoAliases = new Set();
	for (const [canon, def] of Object.entries(lex)) { if (/button/.test(canon)) for (const a of (def.aliases ?? [canon])) buttonAliases.add(a.toLowerCase()); if (canon === "video") for (const a of (def.aliases ?? [canon])) videoAliases.add(a.toLowerCase()); }
	const fold = (s) => String(s ?? "").toLowerCase().replace(/[\[\]]/g, " ").replace(/\s+/g, " ").trim();
	const isButtonTag = (t) => { const f = fold(t); return [...buttonAliases].some((a) => f === a || f.startsWith(a + " ") || f.startsWith(a + ":") || f.startsWith(a + "–") || f.startsWith(a + "-") || f.endsWith(" " + a)) || /\bbutton\b/.test(f); };
	const isVideoTag = (t) => { const f = fold(t); return [...videoAliases].some((a) => f === a || f.startsWith(a + " ") || f.startsWith(a + ":")) || /\bvideo\b/.test(f); };
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
			const bt = tags.find(isButtonTag); if (!bt) continue;
			if (tags.some((t) => /external link/i.test(t))) continue;   // the [external link button] family is its own rule
			const own = urlsOf(b).find(isVideoHost);
			let shape = null, url = own, nextTags = null;
			if (own) shape = "A:own-url";
			else {
				// next non-empty para block
				let n = k + 1; while (n < blocks.length && blocks[n] && blocks[n].kind === "para" && !String(blocks[n].text ?? "").trim()) n++;
				const nb = blocks[n]; if (nb && nb.kind === "para") {
					const nt = tagsOf(nb); const nu = urlsOf(nb).find(isVideoHost); const nvis = String(nb.text ?? "").replace(RED, " ").trim();
					if (nu && nt.some(isVideoTag)) { shape = "B:next-[video]-block"; url = nu; nextTags = nt.slice(0, 2); }
					else if (nu && URL.test(nvis) && nvis.replace(URL, "").trim() === "") { shape = "C:next-bare-url"; url = nu; }
					else if (nu) { shape = "D:next-prose-with-video-url"; url = nu; nextTags = nt.slice(0, 2); }
				}
			}
			if (!shape) continue;
			const id = vidOf(url);
			const label = String(b.text ?? "").replace(RED, " ").replace(URL, " ").replace(/\*/g, "").replace(/\s+/g, " ").trim();
			rows.push({ code, template: meta.template_type ?? "?", subject: meta.subject ?? "?", wtPage: b.wtPage, shape, buttonTag: bt.slice(0, 80), nextTags, label: label.slice(0, 80),
				instructionLike: /\b(please|embed|insert|add|put|place)\b/i.test(bt) && bt.split(/\s+/).length > 4, url: url.slice(0, 120), id, gold: goldForm(goldPages, id), claude: goldForm(claudePages, id) });
		}
	}
	fs.writeFileSync(path.join(__dirname, "_r339_videobutton.json"), JSON.stringify({ generated: new Date().toISOString(), rows }, null, 1));
	const tally = (label, rs) => { const c = {}; for (const r of rs) c[r.gold] = (c[r.gold] ?? 0) + 1; const cc = {}; for (const r of rs) cc[r.claude] = (cc[r.claude] ?? 0) + 1; const found = (c.EMBED ?? 0) + (c.BUTTON ?? 0) + (c.OTHER ?? 0); _l(`${label.padEnd(40)} n=${String(rs.length).padStart(3)} mods=${String(new Set(rs.map((r) => r.code)).size).padStart(3)} | gold ${JSON.stringify(c)} embed/found ${found ? ((c.EMBED ?? 0) / found).toFixed(2) : "-"} | claude ${JSON.stringify(cc)}`); };
	_l(`button-family blocks carrying a video-host URL: ${rows.length} in ${new Set(rows.map((r) => r.code)).size} modules`);
	for (const s of ["A:own-url", "B:next-[video]-block", "C:next-bare-url", "D:next-prose-with-video-url"]) tally(s, rows.filter((r) => r.shape === s));
	_l("\nby instruction-like bracket (a sentence containing 'button') vs a real [button] tag:");
	tally("  instruction-like", rows.filter((r) => r.instructionLike)); tally("  real button tag", rows.filter((r) => !r.instructionLike));
	_l("\nby template:"); for (const t of ["Standard", "Inquiry", "Fundamentals", "Bilingual"]) { const rs = rows.filter((r) => r.template === t); if (rs.length) tally("  " + t, rs); }
	_l("\nby label (top 12):"); const bl = {}; for (const r of rows) (bl[r.label.toLowerCase() || "(none)"] ??= []).push(r); for (const [l, rs] of Object.entries(bl).sort((a, b) => b[1].length - a[1].length).slice(0, 12)) tally("  " + JSON.stringify(l).slice(0, 36), rs);
	_l("\nbutton tag spellings (top 12):"); const bt = {}; for (const r of rows) (bt[r.buttonTag.toLowerCase().replace(/\d+/g, "N")] ??= []).push(r); for (const [l, rs] of Object.entries(bt).sort((a, b) => b[1].length - a[1].length).slice(0, 12)) tally("  " + JSON.stringify(l).slice(0, 38), rs);
}
main().catch((e) => { process.stderr.write(String(e && e.stack || e) + "\n"); process.exit(1); });
