/** _s50_r12_fib.cjs — session 50 Round 12 PICK: every UN-BUILT dragAndDrop bundle whose writer typed the answers as short RED
 *  words inside black sentences (the FIB shape: red 'noise' items on the same block as black text), no table, no media.
 *  In memory. Run from reference/tests/ under WSL. */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const MODS = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
const unRed = (s) => String(s ?? "").replace(/\u{1f534}\[\/?RED TEXT\]\u{1f534}/gu, " ").replace(/\s+/g, " ").trim();
async function main() {
	globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
	DataService.Data.AcksFormats.oembed.throttle_ms = 0;
	const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
	eng.loadEngine();
	let code = "";
	const orig = InteractiveBuilder.Build.bind(InteractiveBuilder);
	InteractiveBuilder.Build = function (args) {
		const b = args?.bundle; const out = orig(args);
		// session 50 Round 15 PICK: a bundle that ABSORBED a different-type follower (extraTypes) whose own bracket names a
		// DIFFERENT activity id than the bundle's ('[Activity 3B – type the answer]' inside Activity 3A's bundle)
		if (b && (b.extraTypes ?? []).length) {
			const mem = [...(b.openerItems ?? []), ...(b.memberItems ?? [])];
			const own = String(b.activityId ?? "").trim().toUpperCase();
			const other = [];
			for (const m of b.memberItems ?? []) {
				if (m?.type !== "tag") continue;
				const mm = /\[\s*Activity\s+([0-9]+[A-Za-z]?)\b/i.exec(unRed(m.text));
				if (mm && mm[1].toUpperCase() !== own) other.push(mm[1].toUpperCase());
			}
			const opener = mem.filter((m) => m?.type === "tag").map((m) => unRed(m.text)).join(" ").slice(0, 100);
			_l(`${code}\t#${b.index}\t${b.type}+${b.extraTypes.join(",")}\tact ${own || "-"}\tother ${other.join(",") || "-"}\tbuilt ${out ? 1 : 0}\t${opener}`);
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
		try { await PageAssembler.AssembleModule(run, norm); } catch (e) { _l(`${code}\tASSEMBLE ERROR`); }
	}
}
main();
