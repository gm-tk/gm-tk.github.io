// _verify_mtkquiz.cjs — ROUND 322 (KB constraint 65 / CL-0082): the [MTKquiz] SHELL.
//
// For each module: convert in memory (oEmbed stubbed, exactly the batch_convert path), find
// every MTK quiz SHELL the engine emitted — the "Designer/Developer To Do: create this quiz
// in MTK DEV …" note — and check the shell is the KB's shell and nothing more:
//
//   THE GATE (defect = a shell the KB forbids):
//   • the note is followed IMMEDIATELY by the one button
//       <a href="#" target="_blank"><div class="button">Go to quiz</div></a>
//     (the button is the box's LAST shell child; nothing sits between note and button);
//   • inside the enclosing activity box, BEFORE the button, only the shell's own pieces
//     exist: a title heading (h2–h5), instruction paragraphs / bullets, inline markup, the
//     note — no numbered list (<ol>), no table, no QUIZ-type widget placeholder, no media
//     (<img>/<audio>/<video>/<iframe>), no second button, no <hr>;
//   A NON-quiz un-built placeholder inside the shell (HPRE203 1C: the marker captured by an
//   "unclassified" container bundle — the round's named Path 2b residue) is counted as
//   RESIDUE, reported, and not a defect — the shell path does not own that bundle.
//   • no answer-mark residue before the button — a "Red Flag: Orphan sub-tag [correct]/
//     [answer]" note, a "[correct]"/"[answer]" bracket, or a "Writers Note: …answers…"
//     (the omission is SILENT: constraint 65 forbids any trace of the quiz's content);
//   • no leaked question line before the button (a paragraph that starts "1." / "Q1" /
//     "Question 1" is the quiz, not an instruction).
//   Content AFTER the button (a closing speech bubble the writer put in the same box —
//   HPRE203 2D, SSOG103 6A) is NOT the shell's business and is not inspected.
//
//   A BOX-LESS shell (the marker had no [Activity] box — EXBP901 1.0, SSOG301) is checked
//   for the note→button adjacency only; its missing box is a named residue of the round.
//
// It also reports, for information, the gold's own "Go to quiz" button count per module.
//
// Run: node --require ./_deflate_raw_polyfill.cjs _verify_mtkquiz.cjs <MOD> ...
//      node --require ./_deflate_raw_polyfill.cjs _verify_mtkquiz.cjs --selftest
"use strict";
const fs = require("fs"), path = require("path");
const corpus = require("./corpus.cjs");
if (process.argv.includes("--selftest")) { require("./_selftest_core.cjs").selftest(__filename); return; }
const MODS = process.env.CV2_MODS_ROOT || path.join(__dirname, "..", "..", "..", "01-Finalized_Modules_");
const eng = require("./_engine_load.cjs");
const Data = eng.loadData();
Data.AcksFormats.oembed.throttle_ms = 0;
globalThis.DataService = { Data, async FetchOembed() { return { ok: false, reason: "stubbed" }; } };
eng.loadEngine();
const norm = new TagNormaliser(Data.TagLexicon, Data.TagExceptions, Data.InstructionCues);

const NOTE_RE = /<p class="cv2-note"[^>]*>Designer\/Developer To Do: create this quiz in MTK DEV[^<]*<\/p>/g;
const BUTTON = '<a href="#" target="_blank"><div class="button">Go to quiz</div></a>';
const FORBIDDEN_TAG = /^(ol|table|thead|tbody|tr|td|th|img|audio|video|iframe|hr|pre|blockquote)$/i;
// a <ul> BEFORE the marker is the writer's own instruction bullets (TEFUN02 4A "tell the audience…");
// the leaked-option <ul> always follows a question line, which QLINE_RE catches
const ALLOWED_TAG = /^(h[1-6]|p|ul|li|b|i|u|strong|em|span|br|sup|sub|small|a|div)$/i;
const QUIZ_TYPES = new Set(Data.EmitTemplates?.interactive_builders?.mtk_quiz?.omit_quiz_content?.quiz_bundle_types ?? []);
const ANSWER_RE = /Red Flag: Orphan sub-tag \[(?:correct|answer|incorrect)|\[\s*(?:correct|incorrect|answer)\b|Writers Note:[^<]*\banswers?\b/i;
const QLINE_RE = /<p>\s*(?:\(?\d{1,2}[.)]\s|q\d\b|question\s*\d)/i;

async function convertModule(mod) {
	const base = corpus.mdir(MODS, mod);
	const run = new ConversionRun({ imageMode: "P" });
	const docs = [];
	for (const name of fs.readdirSync(base).filter((f) => f.endsWith(".docx"))) {
		const buf = fs.readFileSync(path.join(base, name));
		const zip = new ZipReader(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
		docs.push({ name, doc: await DocxExtractor.Extract(zip) });
	}
	const istockAcksFiles = fs.readdirSync(base).filter((f) => /\.txt$/i.test(f))
		.map((f) => ({ name: f, text: fs.readFileSync(path.join(base, f), "utf8") }));
	const log = console.log, warn = console.warn, err = console.error;
	console.log = () => {}; console.warn = () => {}; console.error = () => {};
	try {
		const prep = ModuleResolver.PrepareRun({ docs, run, normaliser: norm, istockAcksFiles });
		if (!prep.ok) throw new Error(`prep refused (${prep.reason})`);
		await PageAssembler.AssembleModule(run, norm);
	} finally { console.log = log; console.warn = warn; console.error = err; }
	return run.outputs.filter((o) => /\.html$/.test(o.filename)).map((o) => ({ name: o.filename, html: String(o.content ?? "") }));
}

/** The enclosing `<div class="activity…" number="…">` still open at `at`, or null. */
function enclosingBox(html, at) {
	const pre = html.slice(0, at);
	const opens = [...pre.matchAll(/<div class="(activity[^"]*)"(?: number="([^"]*)")?[^>]*>/g)];
	for (let k = opens.length - 1; k >= 0; k--) {
		const o = opens[k];
		const seg = pre.slice(o.index + o[0].length);
		const depth = (seg.match(/<div\b/g) || []).length - (seg.match(/<\/div>/g) || []).length;
		if (depth >= 0) return { start: o.index + o[0].length, cls: o[1], number: o[2] ?? null };
	}
	return null;
}

/** Every shell on a page: { number, cls, boxed, before (html from box open to the note), afterNote (html right after the note) }. */
function shellsOf(html) {
	const out = [];
	for (const m of html.matchAll(NOTE_RE)) {
		const box = enclosingBox(html, m.index);
		const before = box ? html.slice(box.start, m.index) : "";
		const afterNote = html.slice(m.index + m[0].length, m.index + m[0].length + 400);
		out.push({ number: box?.number ?? null, cls: box?.cls ?? null, boxed: !!box, before, afterNote, note: m[0] });
	}
	return out;
}

function checkShell(s, residue) {
	const bad = [];
	// 1. the button follows the note at once (whitespace only)
	if (!afterIsButton(s.afterNote)) bad.push(`the note is not followed by the one "Go to quiz" button (next: ${s.afterNote.replace(/\s+/g, " ").trim().slice(0, 70)})`);
	if (!s.boxed) return bad;                      // box-less: adjacency is all there is to check
	// 2. only shell pieces before the note
	const tags = [...s.before.matchAll(/<(\/?)([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>/g)];
	let buttons = 0;
	for (const t of tags) {
		const name = t[2], attrs = t[3] || "";
		if (t[1]) continue;
		if (FORBIDDEN_TAG.test(name)) { bad.push(`<${name}> inside the shell before the button (quiz content leaked)`); break; }
		if (name.toLowerCase() === "div") {
			if (/class="button/.test(attrs)) buttons++;
			else if (/cv2-interactive/.test(attrs)) {
				const ty = (s.before.slice(t.index).match(/INTERACTIVE \(un-built\) #\d+: ([A-Za-z]+)/) || [])[1] || "?";
				if (QUIZ_TYPES.has(ty)) bad.push(`a ${ty} widget placeholder inside the shell (the shell path missed its own bundle)`);
				else residue.push(`Path 2b: the marker rides a non-quiz "${ty}" bundle whose placeholder sits in the box`);
				break;
			}
			else if (!/class="(row|col-[^"]*|activity[^"]*)"/.test(attrs) && !/^\s*$/.test(attrs)) { bad.push(`an unexpected <div${attrs.slice(0, 40)}> inside the shell`); break; }
		} else if (!ALLOWED_TAG.test(name)) { bad.push(`<${name}> inside the shell`); break; }
	}
	if (buttons) bad.push(`${buttons} extra button(s) before the "Go to quiz" button`);
	// 3. silent omission — no answer-mark residue, no leaked question line
	if (ANSWER_RE.test(s.before)) bad.push("an answer-mark residue before the button (the omission must be silent)");
	if (QLINE_RE.test(s.before)) bad.push("a question line before the button (quiz content leaked)");
	return bad;
}
function afterIsButton(after) { return after.replace(/^\s+/, "").startsWith(BUTTON); }

function goldButtons(mod) {
	let n = 0;
	try {
		const dir = corpus.mdir(MODS, mod);
		for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".html"))) n += (fs.readFileSync(path.join(dir, f), "utf8").match(/Go to quiz/g) || []).length;
	} catch { /* no gold */ }
	return n;
}

(async () => {
	let total = 0, boxed = 0, defect = 0, modsBuilt = 0, residueN = 0;
	for (const mod of process.argv.slice(2)) {
		let pages;
		try { pages = await convertModule(mod); } catch (e) { console.log(`${mod}: ERROR ${e.message}`); continue; }
		const shells = [];
		for (const p of pages) for (const s of shellsOf(p.html)) shells.push({ page: p.name, ...s });
		// T1 null-test: an internally WRONG shell the gate MUST flag — a question list sits
		// between the note and the button, and an answer mark survived inside the box.
		if (process.env.CV2_SELFTEST_INJECT) {
			shells.push({ page: "INJECTED", number: "9Z", cls: "activity", boxed: true,
				before: '<div class="row"><div class="col-12"><h3>Quiz</h3><p>Answer the questions.</p><ol><li>What is 2 + 2?</li></ol><p class="cv2-note">Red Flag: Orphan sub-tag [correct] outside an interactive</p>',
				afterNote: '<ol><li>1. Which is a mammal?</li></ol>' + BUTTON, note: "" });
		}
		if (!shells.length) { console.log(`${mod}: 0 shells (no [MTKquiz] marker reached the shell path) — gold "Go to quiz" ${goldButtons(mod)}`); continue; }
		modsBuilt++;
		let mD = 0, mR = 0; const reasons = [];
		for (const s of shells) {
			total++; if (s.boxed) boxed++;
			const res = [];
			const bad = checkShell(s, res);
			if (bad.length) { mD++; reasons.push(`${s.page} ${s.number ?? "(box-less)"}: ${bad.join("; ")}`); }
			if (res.length) { mR++; reasons.push(`${s.page} ${s.number ?? "(box-less)"}: ${res.join("; ")} (residue, not counted)`); }
		}
		defect += mD; residueN += mR;
		console.log(`${mod}: ${shells.length} shell(s) [boxed ${shells.filter((s) => s.boxed).length}, box-less ${shells.filter((s) => !s.boxed).length}, defect ${mD}${mR ? `, residue ${mR}` : ""}]  gold "Go to quiz" ${goldButtons(mod)}  ${mD ? `✗ ${mD} defect` : "✓ every shell is the KB shell"}`);
		for (const r of reasons.slice(0, 8)) console.log(`    ! ${r}`);
	}
	console.log(`\nTOTAL: ${total} shell(s) across ${modsBuilt} module(s); boxed ${boxed}, box-less ${total - boxed}, residue ${residueN}, defect ${defect}.`);
	console.log(defect ? "RESULT: real defects present ✗" : "RESULT: every MTK quiz shell is the KB shell ✓");
	process.exit(defect ? 1 : 0);
})();
