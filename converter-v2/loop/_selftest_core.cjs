// _selftest_core.cjs — T1 verifier NULL-TESTS (round 149, ENGINE SPLIT phase 0c).
//
// WHY: rounds 97-104 every widget verifier silently reported a vacuous "defect 0" —
// the engine load threw under a suppressed console, nothing was BUILT, and an empty
// built set reads as success. A verifier must PROVE it can still detect a defect
// before its green is trusted.
//
// WHAT: each _verify_*.cjs now accepts --selftest, which routes here. Two assertions:
//   1. LIVENESS  — run the verifier on a fixture module KNOWN to build the widget;
//                  the built TOTAL must be > 0 (an empty built set = the r97-104 hole).
//   2. DETECTION — copy the fixture module to /tmp, MANGLE every human *.html
//                  (every [A-Za-z0-9] -> 'x'; the .docx WT is untouched so the build
//                  still happens), re-run with CV2_MODS_ROOT pointing at the mangled
//                  copy: the verifier's defect signal MUST strictly INCREASE. A
//                  verifier that still reports its baseline against garbage is blind.
//
// Usage:  node _verify_flipcard.cjs --selftest      (any migrated verifier)
//         node _selftest_core.cjs                   (run ALL selftests, sequential)
//         node _selftest_core.cjs flipcard tabs     (subset)
// Run at every ENGINE SPLIT phase boundary + whenever a verifier or the loader changes.
// NOTE: /tmp wipes between sandbox calls — fixtures are rebuilt per invocation (cheap).
// The fixture dir is PER-PROCESS (round 246): a shared "/tmp/cv2_selftest" survived one
// sandbox session owned by another uid, and every later selftest then died with
// "EACCES: permission denied, rmdir" before its DETECTION half could run. A pid-suffixed
// dir cannot collide, so a stale fixture can never block a gate run again.
"use strict";
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const corpus = require("./corpus.cjs");

const MODS = path.join(__dirname, "..", "..", "..", "01-Finalized_Modules_");
const OUT = path.join(__dirname, "..", "..", "..", "01-Claude_Modules_");
// ROUND 282 — PER-RUN, not per-PID. The round-246 per-process dir still collided:
// sandbox pids recycle low numbers, so a fixture left by an EARLIER SESSION (owned by
// another uid, undeletable) sat at the same path and every selftest died with EACCES
// on rmSync — the failure the kickoffs kept telling the next session to "just re-run".
// A random suffix makes a collision impossible.
const FIX = `/tmp/cv2_selftest_${process.pid}_${Math.random().toString(36).slice(2, 10)}`;

// Per-verifier spec: fixture codes (must BUILD the widget), liveness TOTAL regex,
// defect-signal extractor (number that must strictly increase under the mangle).
// signal "xmark" = count of ✗ marks; "built-only" = count of built-only: lines.
const SPEC = {
	"_verify_flipcard.cjs": { codes: ["CEDO102"], total: /TOTAL (\d+):/, signal: /divergence (\d+)/, mangle: "full" },
	// speechBubble joined the A1 faithful-to-source family at round 247 (text-only builds:
	// a zero-overlap writer-faithful bubble = tolerated gold-subst, not a defect) — so, like
	// accordion/clickdrop, mangled gold is the WRONG probe: its null-test INJECTS a
	// malformed (letterless) built bubble the malformation rule MUST flag.
	"_verify_speechbubble.cjs": { codes: ["OSAH501"], total: /TOTAL built (\d+):/, signal: /defect (\d+)/, inject: true },
	// accordion + clickdrop define DEFECT as an internally MALFORMED build (A1 faithful-to-
	// source: human mismatch is tolerated by design) — mangled gold is the WRONG probe for
	// them. Their null-test INJECTS a malformed built sample (CV2_SELFTEST_INJECT) instead,
	// which their defect rule MUST flag.
	"_verify_accordion.cjs": { codes: ["OSAH501", "CEDW501"], total: /TOTAL: (\d+) panels/, signal: "xmark", inject: true },
	"_verify_tabs.cjs": { codes: ["HES1003"], total: /TOTAL (\d+):/, signal: /defect (\d+)/ },
	"_verify_clickdrop.cjs": { codes: ["BLL237"], total: /TOTAL: (\d+) clickDrop/, signal: /defect (\d+)/, inject: true },
	// dropDown (round 287) is A1 faithful-to-source like accordion/clickdrop — a human
	// mismatch is tolerated BY DESIGN, so mangled gold is the wrong probe. Its null-test
	// INJECTS an internally malformed unit (one empty option, an out-of-range answer, an
	// empty placeholder) which the defect rule MUST flag.
	"_verify_dropdown.cjs": { codes: ["BLL273", "MXFU301"], total: /TOTAL: (\d+) dropDown group/, signal: /defect (\d+)/, inject: true },
	// modal (round 292) is A1 faithful-to-source too — and more so than any other widget
	// here, since the whole BLL phonics family's gold contains no pop-out markup at all.
	// Mangled gold is therefore the wrong probe; its null-test INJECTS a malformed build
	// (a wordless, pictureless trigger over an empty pop-out, plus an unpaired trigger)
	// which the defect rule MUST flag.
	"_verify_modal.cjs": { codes: ["OSOH501", "MXFU301"], total: /TOTAL: (\d+) pop-out group/, signal: /defect (\d+)/, inject: true },
	// mtkquiz (round 322 — KB constraint 65, the [MTKquiz] shell without the quiz content). The
	// gate is the KB shell itself (note followed at once by the one button; no numbered list /
	// table / quiz-type placeholder / answer-mark residue / question line inside the box before
	// the button), so mangled gold is the wrong probe: its null-test INJECTS a wrong shell (a
	// question list between note and button, a [correct] residue in the box) the gate MUST flag.
	"_verify_mtkquiz.cjs": { codes: ["TEFUN06", "SCCH301"], total: /TOTAL: (\d+) shell/, signal: /defect (\d+)/, inject: true },
	// math (round 346): the INJECT probe strips one built <math> from the first math page — the docx-vs-page
	// count mismatch must register as a defect; MXDI301 (69 equations) is the fixture.
	"_verify_math.cjs": { codes: ["MXDI301"], total: /TOTAL: (\d+) equation/, signal: /defect (\d+)/, inject: true },
	"_verify_hintslider.cjs": { codes: ["OSBY201"], total: /built (\d+) rows/, signal: "built-only", mangle: "full" },
	// image_carousel fixture must have a CLEAN baseline (OSGM501: 5 slides exact, defect 0) —
	// CEDO105 is saturated (12/12 baseline defects), a saturated signal cannot increase.
	"_verify_image_carousel.cjs": { codes: ["OSGM501"], total: /TOTAL: (\d+) image carousel/, signal: /defect (\d+)/ },
	// carousel: the defect channel is BUILT video-slide ids vs human ids — DORMANT until
	// round 247 (the media-series fixes make BLL210 build 16 video slides), so the r149
	// detect_skip is DROPPED as its own note instructed: mangled gold ("full" — the iframe
	// src ids live in attributes) must raise the mismatched-slide-id signal.
	"_verify_carousel.cjs": { codes: ["BLL117", "BLL210"], total: /TOTAL: (\d+) carousels/, signal: /(\d+) mismatched slide ids/, mangle: "full" },
	// intextract byte-compares its in-memory conversion against 01-Claude_Modules_ on disk:
	// mangle a copy of the CLAUDE output instead (CV2_OUT_ROOT) and expect BYTE-DIFF + rc 1.
	"_verify_intextract.cjs": { codes: ["OSBY201"], total: /DEFAULT: (\d+) files/, out_mode: true },
};

// Two mangle modes — each verifier's spec pins the probe its PROTECTED signal needs:
//   "text": [A-Za-z0-9] -> 'x' in TEXT NODES ONLY. The human page keeps its widget
//           STRUCTURE, so structure-dependent tolerance branches (tabs' "human has no
//           tabs -> divergence, not defect") stay on their normal path while every text
//           match is destroyed.
//   "full": every [A-Za-z0-9] -> 'x' incl. tags. Structure vanishes — probes signals
//           that fire on STRUCTURAL absence (flipCard's protected divergence).
function mangleHtmlDir(dir, mode) {
	for (const e of fs.readdirSync(dir)) {
		const p = path.join(dir, e);
		if (fs.statSync(p).isDirectory()) mangleHtmlDir(p, mode);
		else if (e.endsWith(".html")) {
			const raw = fs.readFileSync(p, "utf8");
			const mangled = mode === "full"
				? raw.replace(/[A-Za-z0-9]/g, "x")
				: raw.split(/(<[^>]*>)/).map((seg) => (seg.startsWith("<") ? seg : seg.replace(/[A-Za-z0-9]/g, "x"))).join("");
			fs.writeFileSync(p, mangled);
		}
	}
}

function makeFixture(root, codes, mangle) {
	fs.rmSync(FIX, { recursive: true, force: true });
	fs.mkdirSync(FIX, { recursive: true });
	for (const c of codes) {
		const src = corpus.mdir(root, c);
		fs.cpSync(src, path.join(FIX, c), { recursive: true });
	}
	if (mangle) mangleHtmlDir(FIX, mangle);
	return FIX;
}

function runVerifier(file, codes, env) {
	const r = spawnSync("node", ["--require", "./_deflate_raw_polyfill.cjs", file, ...codes],
		{ cwd: __dirname, encoding: "utf8", env: { ...process.env, STUB_OEMBED: "1", ...env }, timeout: 120000 });
	return { rc: r.status, out: (r.stdout || "") + (r.stderr || "") };
}

function signalCount(spec, out) {
	if (spec.signal === "xmark") return (out.match(/✗/g) || []).length;
	if (spec.signal === "built-only") return (out.match(/built-only:/g) || []).length;
	let n = 0;
	for (const m of out.matchAll(new RegExp(spec.signal.source, "g"))) n += +m[1];
	return n;
}

function selftest(verifierFile) {
	const base = path.basename(verifierFile);
	const spec = SPEC[base];
	if (!spec) { console.error(`SELFTEST ${base}: no spec — add one to _selftest_core.cjs SPEC`); process.exit(1); }

	// 1. LIVENESS — normal run must BUILD.
	const norm = runVerifier(base, spec.codes, {});
	const tm = norm.out.match(spec.total);
	const totals = spec.total.global ? 0 : (tm ? +tm[1] : NaN);
	const liveTotal = Number.isNaN(totals) ? 0 : totals;
	const liveOk = liveTotal > 0 && (spec.out_mode ? norm.rc === 0 : true);
	console.log(`SELFTEST ${base} LIVENESS: built TOTAL ${Number.isNaN(totals) ? "«no TOTAL line»" : liveTotal} on ${spec.codes.join(" ")} ${liveOk ? "PASS" : "FAIL"}`);

	// 2. DETECTION — mangled gold must raise the defect signal.
	let detOk = true, detMsg = "";
	if (spec.detect_skip) {
		detMsg = `SKIP (${spec.detect_skip})`;
	} else if (spec.inject) {
		const before = signalCount(spec, norm.out);
		const mang = runVerifier(base, spec.codes, { CV2_SELFTEST_INJECT: "1" });
		const after = signalCount(spec, mang.out);
		detOk = after > before;
		detMsg = `defect signal ${before} -> ${after} with an INJECTED malformed build ${detOk ? "— PASS" : "— FAIL (verifier is BLIND)"}`;
	} else if (spec.out_mode) {
		makeFixture(OUT, spec.codes, "full");
		const mang = runVerifier(base, spec.codes, { CV2_OUT_ROOT: FIX });
		detOk = mang.rc !== 0 && /BYTE-DIFF/.test(mang.out);
		detMsg = `mangled corpus -> rc ${mang.rc}, BYTE-DIFF ${detOk ? "reported — PASS" : "NOT reported — FAIL"}`;
	} else {
		const before = signalCount(spec, norm.out);
		makeFixture(MODS, spec.codes, spec.mangle || "text");
		const mang = runVerifier(base, spec.codes, { CV2_MODS_ROOT: FIX });
		const after = signalCount(spec, mang.out);
		detOk = after > before;
		detMsg = `defect signal ${before} -> ${after} under mangled gold ${detOk ? "— PASS" : "— FAIL (verifier is BLIND)"}`;
	}
	console.log(`SELFTEST ${base} DETECTION: ${detMsg}`);

	const ok = liveOk && detOk;
	console.log(`SELFTEST ${base}: ${ok ? "GREEN" : "RED"}`);
	process.exit(ok ? 0 : 1);
}

module.exports = { selftest, SPEC };

// standalone: run all (or named subset) sequentially in-process via subshells
if (require.main === module) {
	const want = process.argv.slice(2);
	const files = Object.keys(SPEC).filter((f) => !want.length || want.some((w) => f.includes(w)));
	let allOk = true;
	for (const f of files) {
		const r = spawnSync("node", [f, "--selftest"], { cwd: __dirname, encoding: "utf8", timeout: 300000 });
		process.stdout.write(r.stdout || "");
		if (r.status !== 0) allOk = false;
	}
	console.log(allOk ? "== ALL SELFTESTS GREEN ==" : "== SELFTEST FAILURE(S) — a verifier cannot be trusted ==");
	process.exit(allOk ? 0 : 1);
}
