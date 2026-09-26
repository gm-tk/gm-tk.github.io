/** _s51_flagon.cjs — session 51 Round 13 (the registry rows' in-memory probe lane): a --require PRELOAD that flips ONE parked
 *  data flag ON in memory, so any in-memory probe (e.g. _r448_probe.cjs) scores the parked row against the CURRENT engine without
 *  touching data/*.json. FLAGON="EmitTemplates:elements.table.cell_bullets" (the data-map key, then the dotted path to the object
 *  whose `enabled` becomes true). Several: separate with ";".
 *    FLAGON=... node --require ./_deflate_raw_polyfill.cjs --require ../../outputs/_s51_flagon.cjs ../../outputs/_r448_probe.cjs …
 */
"use strict";
const path = require("path");
const eng = require(path.join(__dirname, "..", "reference", "tests", "_engine_load.cjs"));
const orig = eng.loadData;
eng.loadData = function () {
	const D = orig.apply(this, arguments);
	for (const spec of String(process.env.FLAGON || "").split(";").filter(Boolean)) {
		const [key, dotted] = spec.split(":");
		let o = D[key];
		for (const k of dotted.split(".")) { if (!o || typeof o !== "object") throw new Error("FLAGON: no " + spec); o = o[k]; }
		if (!o || o.enabled !== false) throw new Error("FLAGON: not a parked flag: " + spec);
		o.enabled = true;
		process.stderr.write("[flagon] " + spec + " → enabled\n");
	}
	return D;
};
