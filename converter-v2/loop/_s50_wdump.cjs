/** _s50_wdump.cjs — session 50: dump every bundle of DUMP_TYPE (default reorder) in the given modules — its member stream
 *  (tag / black lines / table rows, clipped) — plus the module's GOLD widgets of that class (their item texts in order).
 *  In memory, no writes. Run from reference/tests/ under WSL:  DUMP_TYPE=reorder node ../../outputs/_s50_wdump.cjs CODES… */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const TYPE = process.env.DUMP_TYPE || "reorder";
const GOLDCLS = process.env.GOLD_CLASS || TYPE;
const ITEMCLS = process.env.GOLD_ITEM || "reorderItem";
const clip = (s, n) => String(s ?? "").replace(/\u{1f534}\[\/?RED TEXT\]\u{1f534}/gu, "").replace(/\s+/g, " ").trim().slice(0, n);
const strip = (s) => String(s).replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	let code = "";
	const orig = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle; const out = orig(args);
		if (b?.type === TYPE) {
			_l(`--- ${code} #${b.index} ${out ? "BUILT" : "box"} modifier=${JSON.stringify(b.modifier ?? "")}`);
			for (const m of [...(b.openerItems ?? []), ...(b.memberItems ?? [])].slice(0, 16)) {
				if (m?.type === "table") _l(`    TABLE ${(m.block?.rows ?? []).length}x${Math.max(0, ...(m.block?.rows ?? []).map((r) => (r ?? []).length))}: ${(m.block?.rows ?? []).slice(0, 4).map((r) => (r ?? []).map((c) => clip(typeof c === "string" ? c : c?.text, 30)).join(" ‖ ")).join(" // ")}`);
				else _l(`    ${m?.type}: ${clip(m?.text, 110)}${m?.blackAfter ? " ⟶ " + clip(m.blackAfter, 60) : ""}`);
			}
		}
		return out;
	};
	for (code of process.argv.slice(2).filter((a) => !a.startsWith("--")).map((a) => a.trim()).filter(Boolean)) {
		let base; try { base = corpus.mdir(MODS, code); fs.readdirSync(base); } catch { continue; }
		const run = new ConversionRun({ imageMode: "P" });
		const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
		const docs = [];
		for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
			const buf = fs.readFileSync(path.join(base, name));
			docs.push({ name, doc: await DocxExtractor.Extract(new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength))) });
		}
		const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f)).map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
		const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
		if (!prep.ok) continue;
		try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}: ASSEMBLE ERROR`); }
		for (const f of fs.readdirSync(base).filter((x) => x.endsWith(".html"))) {
			const h = fs.readFileSync(path.join(base, f), "utf8").replace(/<!--[\s\S]*?-->/g, "");
			const re = new RegExp(`<div class="${GOLDCLS}[ "][^>]*>`, "g");
			for (const m of h.matchAll(re)) {
				const seg = h.slice(m.index, m.index + 12000);
				const items = [...seg.matchAll(new RegExp(`class="${ITEMCLS}"[^>]*>([\\s\\S]*?)</(?:div|span)>`, "g"))].map((x) => strip(x[1]).slice(0, 40)).slice(0, 12);
				_l(`    GOLD ${f}: ${m[0].slice(0, 70)} items ${items.length}: ${items.join(" | ")}`);
			}
		}
	}
}
main();
