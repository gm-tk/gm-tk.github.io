// Session 45 Round 3 — how does the engine's own TagNormaliser resolve each hover / rollover marker span in the given modules' WTs?
// Prints, per distinct marker HEAD (the text before the first ':'), the primary tag / directive / class / widget types and a count.
// WSL, from reference/tests: node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s45_r3_hoverparse.cjs CODE ...
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = process.cwd();
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const corpus = require(path.join(TESTS, "corpus.cjs"));
const Data = eng.loadData();
globalThis.DataService = { Data, async FetchOembed() { return { ok: false }; } };
eng.loadEngine();
const norm = new TagNormaliser(Data.TagLexicon, Data.TagExceptions, Data.InstructionCues);
const MODS = path.join(TESTS, "..", "..", "..", "01-Finalized_Modules_");
const HEAD = /\[\s*(?:hover(?:\s*info(?:rmation)?)?|roll\s*-?\s*over|rollover|mouse\s*-?\s*over|mouseover)\b[^\]]*/i;
const agg = new Map();
for (const code of process.argv.slice(2)) {
	const dir = corpus.mdir(MODS, code);
	for (const f of fs.readdirSync(dir).filter((x) => /writers template/i.test(x) && x.endsWith("_parsed.txt"))) {
		const txt = fs.readFileSync(path.join(dir, f), "utf8");
		// every red span
		for (const m of txt.matchAll(/🔴\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]🔴/gu)) {
			const span = m[1];
			const h = HEAD.exec(span);
			if (!h) continue;
			const p = norm.Parse(span);
			const prim = p.primary;
			const wt = prim ? (norm.GetWidgetTypes(prim.tag) ?? []) : [];
			const head = span.slice(h.index).split(":")[0].replace(/\s+/g, " ").trim().toLowerCase().slice(0, 30);
			const closed = /\]/.test(span.slice(h.index));
			const k = `${head} | ${prim ? prim.tag + "/" + prim.directive : "-"} | class=${p.class} | instrFrag=${!!p.instructionFragment} | wt=${wt.join(",")} | closedInSpan=${closed}`;
			const e = agg.get(k) ?? { n: 0, mods: new Set(), ex: [] };
			e.n++; e.mods.add(code); if (e.ex.length < 2) e.ex.push(span.replace(/\s+/g, " ").slice(0, 90));
			agg.set(k, e);
		}
	}
}
for (const [k, e] of [...agg.entries()].sort((a, b) => b[1].n - a[1].n))
	console.log(`${String(e.n).padStart(4)} ${String(e.mods.size).padStart(3)}m  ${k}\n        e.g. ${e.ex.join(" || ")}`);
