// _verify_count.cjs — ROUND 501 (session 49 Round 1, 25 Sept 2026): THE VERIFIER COUNT TEST (LOOP §3 step 6, as amended by
// the third /loop-review). A verifier whose RESULT reads ✓ only because nothing was built passes VACUOUSLY — a builder that
// stops building reports defect 0. So every verifier with a count in gate_baseline.json prints that count against the
// baseline's and reads ✗ when it FELL: each recorded total, AND each module's own count (a module that stops building while
// another grows would otherwise cancel out in the total).
//
// The test applies only when the verifier runs on its RECORDED module set (gate_baseline.json.<key>.count_modules — the
// run_all_gates.sh set). An ad-hoc run (one module, a --selftest fixture) prints "n/a" and never fails on it.
//
// Recording: VERIFY_COUNT_RECORD=1 writes the live counts into gate_baseline.json — the totals, count_per_module and
// count_modules — by a section-aware LINE edit that keeps the file's own formatting (the file mixes 2- and 4-space indents, so
// it can never be re-serialised whole). A round that legitimately GREW a count (or shrank one, NAMED in its changelog entry)
// records it this way at its finalise — never by hand. Usage inside a verifier:
//   const C = require("./_verify_count.cjs").countTest("bingo", { grids: 52, cells: 624 }, { BLL110: 12, … }, mods);
//   … RESULT reads ✗ when C.fell.
"use strict";
const fs = require("fs"), path = require("path");
const GB = path.join(__dirname, "gate_baseline.json");

function load() { try { return JSON.parse(fs.readFileSync(GB, "utf8")); } catch { return {}; } }

// Replace (or insert) `"field": <json>` at the 4-space level inside the 2-space `"key": {` section.
function setFields(key, fields) {
	const src = fs.readFileSync(GB, "utf8");
	const eol = src.includes("\r\n") ? "\r\n" : "\n";
	const L = src.split(eol);
	const open = L.findIndex((l) => l === `  "${key}": {`);
	if (open < 0) throw new Error(`gate_baseline.json has no top-level "${key}" section`);
	let close = open + 1;
	while (close < L.length && !/^  \}/.test(L[close])) close++;
	if (close >= L.length) throw new Error(`gate_baseline.json "${key}" section is not closed`);
	for (const [f, v] of Object.entries(fields)) {
		const val = JSON.stringify(v);
		let hit = -1;
		for (let i = open + 1; i < close; i++) if (L[i].startsWith(`    "${f}": `)) { hit = i; break; }
		if (hit >= 0) {
			const comma = /,\s*$/.test(L[hit]) ? "," : "";
			L[hit] = `    "${f}": ${val}${comma}`;
		} else {
			L.splice(open + 1, 0, `    "${f}": ${val},`);
			close++;
		}
	}
	const out = L.join(eol);
	JSON.parse(out);                                   // must still parse before it replaces the file
	const tmp = GB + ".tmp";
	fs.writeFileSync(tmp, out);
	if (fs.statSync(tmp).size < 1000) throw new Error("refusing to write a truncated gate_baseline.json");
	fs.renameSync(tmp, GB);
}

function countTest(key, totals, perModule, modules, log) {
	const mods = [...new Set((modules || []).filter((m) => m && !m.startsWith("-")))].sort();
	const say = (s) => (log || console.log)(s);   // a verifier that mutes console.log (typing) passes its own logger
	if (process.env.VERIFY_COUNT_RECORD === "1" && !process.env.CV2_SELFTEST_INJECT) {
		const pm = {};
		for (const m of mods) pm[m] = +(perModule[m] || 0);
		setFields(key, { ...totals, count_per_module: pm, count_modules: mods });
		say(`COUNT (${key}): RECORDED into gate_baseline.json — ${Object.entries(totals).map(([k, v]) => `${k} ${v}`).join(", ")} over ${mods.length} module(s).`);
		return { fell: false, recorded: true };
	}
	const base = load()[key] || {};
	const setB = Array.isArray(base.count_modules) ? [...base.count_modules].sort() : null;
	if (!setB) {
		say(`COUNT (${key}): n/a — no recorded module set in gate_baseline.json.${key} (record it: VERIFY_COUNT_RECORD=1).`);
		return { fell: false, na: true };
	}
	if (setB.join(" ") !== mods.join(" ")) {
		say(`COUNT (${key}): n/a — an ad-hoc module set (the count test applies to the recorded ${setB.length}-module gate set only).`);
		return { fell: false, na: true };
	}
	const fellTot = [], grewTot = [], parts = [];
	for (const [k, v] of Object.entries(totals)) {
		const b = base[k];
		if (typeof b !== "number") { parts.push(`${k} ${v} (no baseline)`); continue; }
		parts.push(`${k} ${v} vs ${b}`);
		if (v < b) fellTot.push(`${k} ${v} < ${b}`); else if (v > b) grewTot.push(`${k} ${v} > ${b}`);
	}
	const bpm = base.count_per_module || {};
	const fellMod = [], grewMod = [];
	for (const m of mods) {
		const v = +(perModule[m] || 0), b = +(bpm[m] || 0);
		if (v < b) fellMod.push(`${m} ${v} < ${b}`); else if (v > b) grewMod.push(`${m} ${v} > ${b}`);
	}
	const fell = fellTot.length > 0 || fellMod.length > 0;
	if (fell) {
		say(`COUNT (${key}): ${parts.join(", ")} ✗ FELL — ${[...fellTot, ...fellMod].join("; ")} (a builder that stopped building passes the defect test vacuously; investigate, or NAME it and record: VERIFY_COUNT_RECORD=1).`);
	} else if (grewTot.length || grewMod.length) {
		say(`COUNT (${key}): ${parts.join(", ")} ✓ GREW — ${[...grewTot, ...grewMod].join("; ")} (record the new count at the finalise: VERIFY_COUNT_RECORD=1).`);
	} else {
		say(`COUNT (${key}): ${parts.join(", ")} ✓ held (per module too).`);
	}
	return { fell };
}

module.exports = { countTest, setFields };
