/** _r318_unit.cjs — drives the REAL HtmlFormatter.Indent (round 318 lazy-free hosts) on containment cases.
 *  Run from CONVERTER_V2/outputs/:  node --require ../reference/tests/_deflate_raw_polyfill.cjs _r318_unit.cjs
 *                                   LAZYHOST_OFF=1 node ... (OFF: every image keeps the attribute) */
"use strict";
const path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData() };
eng.loadEngine();
const off = !!process.env.LAZYHOST_OFF;
const L = 'loading="lazy"';
const IMG = (n) => `<img class="img-fluid" ${L} src="images/${n}.png" alt="" />`;
const run = (html) => HtmlFormatter.Indent(html);
const count = (s) => (s.match(/loading="lazy"/g) || []).length;
// [html, expected lazy count ON, description]
const cases = [
	[`<div class="row">\n<div class="col-12">\n${IMG(1)}\n</div>\n</div>`, 1, "outside any host keeps it"],
	[`<div class="row carousel">\n<div class="col-md-12 col-12 viewer">\n<div class="item">\n${IMG(1)}\n</div>\n</div>\n</div>\n${IMG(2)}`, 1, "inside a carousel loses it; the next sibling image keeps it"],
	[`<div class="flipCard">\n<div class="front">\n${IMG(1)}\n</div>\n<div class="back">\n<p>text</p>\n${IMG(2)}\n</div>\n</div>`, 0, "flip card front + back both lose it"],
	[`<div class="row">\n<div class="button clickDrop">Need help?</div>\n<div class="clickDropContent">\n<p>x</p>\n${IMG(1)}\n</div>\n${IMG(2)}\n</div>`, 1, "clickDropContent (a sibling panel) loses it; the row's other image keeps it"],
	[`<div class="accordion">\n<div class="accContent">\n${IMG(1)}\n</div>\n</div>`, 1, "an accordion is not a moving host"],
	[`<div class="dragAndDrop row" layout="area">\n<div class="dragContainer col-12">\n<div class="drag" option="1"><img class="dragImage" ${L} src="a.png" alt="x" /></div>\n</div>\n</div>`, 0, "a dragImage inside dragAndDrop loses it (any img class)"],
	[`<div class="bannerContainer">\n<!-- <img class="img-fluid" ${L} src="images/real.jpg" alt=""> -->\n${IMG(1)}\n</div>`, 0, "the Mode-P commented real reference inside a banner loses it too"],
	[`<div class="carousel">\n<p>unbalanced\n</div>\n${IMG(1)}`, 1, "after the host closes, an image is outside again"],
	[`<div class="memoryGame">\n<div class="memCard cardHidden">\n${IMG(1)}\n</div>\n</div>\n<div class="canvasContainer">\n${IMG(2)}\n</div>`, 0, "memory game + sketcher"],
];
let bad = 0;
for (const [html, wantOn, desc] of cases) {
	const got = count(run(html)); const want = off ? count(html) : wantOn;
	if (got !== want) { bad++; console.log("FAIL", desc, "->", got, "want", want); }
}
console.log(`${off ? "OFF" : "ON "}: ${bad ? bad + " FAIL" : "all " + cases.length + " cases pass"}`);
process.exit(bad ? 1 : 0);
