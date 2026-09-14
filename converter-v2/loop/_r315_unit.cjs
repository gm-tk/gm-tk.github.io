/** _r315_unit.cjs — drives the REAL HtmlFormatter.Indent (round 315 void pass) on edge cases.
 *  Run from CONVERTER_V2/outputs/:  node _r315_unit.cjs        (ON)
 *                                   XHTMLVOID_OFF=1 node _r315_unit.cjs   (OFF: every line unchanged) */
"use strict";
const path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData() };
eng.loadEngine();
const off = !!process.env.XHTMLVOID_OFF;
const one = (line) => HtmlFormatter.Indent(line).trim();
const cases = [
	["<!DOCTYPE html>", "<!doctype html>"],
	["<br>", "<br />"], ["<br/>", "<br />"], ["<br />", "<br />"], ["<BR>", "<BR />"],
	['<img src="a/b.png" alt="">', '<img src="a/b.png" alt="" />'],
	['<img src="a/b.png" alt="x > y"/>', '<img src="a/b.png" alt="x > y" />'],
	["<img src=a/b.png>", "<img src=a/b.png />"],
	["<p>one<br>two<br />three</p>", "<p>one<br />two<br />three</p>"],
	['<meta charset="utf-8" />', '<meta charset="utf-8" />'],
	['<link rel="stylesheet" href="https://x/y.css">', '<link rel="stylesheet" href="https://x/y.css" />'],
	["<brand>", "<brand>"], ["<br-x>", "<br-x>"], ["<column>", "<column>"], ['<hr class="x">', '<hr class="x" />'],
	['<div class="brick">', '<div class="brick">'],
	["<img alt='it&#39;s'>", "<img alt='it&#39;s' />"],
	['<p><a href="x"><img src="y"></a></p>', '<p><a href="x"><img src="y" /></a></p>'],
];
let bad = 0;
for (const [i, want] of cases) {
	const exp = off ? i : want;
	const got = one(i);
	if (got !== exp) { bad++; console.log("FAIL", JSON.stringify(i), "->", JSON.stringify(got), "want", JSON.stringify(exp)); }
}
const idem = cases.every(([i, o]) => one(one(i)) === one(i));
console.log(`${off ? "OFF" : "ON "}: ${bad ? bad + " FAIL" : "all " + cases.length + " cases pass"}; idempotent: ${idem}`);
process.exit(bad ? 1 : 0);
