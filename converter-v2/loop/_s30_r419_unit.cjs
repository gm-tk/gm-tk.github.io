/** _s30_r419_unit.cjs — unit check of ListsAndRuns.LanguageFontWrap on synthetic HTML (run from reference/tests/ under WSL):
 *    STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s30_r419_unit.cjs
 */
"use strict";
const path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {}; console.error = () => {};
eng.loadEngine();
console.log = _l;
const W = (html, code) => ListsAndRuns.LanguageFontWrap(html, { moduleCode: code });
const cases = [
  ["CHFUN05", `<p>paragraph 奶奶 and more</p>`, `<p>paragraph <span class="ch-text">奶奶</span> and more</p>`],
  ["CHFUN05", `<p><b>奶奶</b></p>`, `<p><b><span class="ch-text">奶奶</span></b></p>`],
  ["CHFUN05", `<h1><span>第一课</span></h1>`, `<h1><span><span class="ch-text">第一课</span></span></h1>`],
  ["CHFUN05", `<td>他(她)是我的(哥哥/弟弟/姐姐/妹妹</td>`, `<td><span class="ch-text">他(她)是我的(哥哥/弟弟/姐姐/妹妹</span></td>`],
  ["CHFUN05", `<p>你好 (hello) 再见。</p>`, `<p><span class="ch-text">你好</span> (hello) <span class="ch-text">再见。</span></p>`],
  ["CHFUN05", `<p>。</p>`, `<p>。</p>`],
  ["CHFUN05", `<p><span class="ch-text">奶奶</span> 再见</p>`, `<p><span class="ch-text">奶奶</span> <span class="ch-text">再见</span></p>`],
  ["CHFUN05", `<p>小明：你好 吗？</p>`, `<p><span class="ch-text">小明：你好 吗？</span></p>`],
  ["JPN1004", `<li>list しちがつ</li>`, `<li>list <span class="jp-text">しちがつ</span></li>`],
  ["JPN1004", `<p>日本語</p>`, `<p><span class="jp-text">日本語</span></p>`],
  ["MXFL202", `<p>Origami 動物折り紙 x</p>`, `<p>Origami <span class="jp-text">動物折り紙</span> x</p>`],
  ["ENGS202", `<p>Osaka (大阪)</p>`, `<p>Osaka (大阪)</p>`],
  ["CHFUN05", `<img alt="奶奶" src="x.png" /><p>奶奶</p>`, `<img alt="奶奶" src="x.png" /><p><span class="ch-text">奶奶</span></p>`],
  ["CHFUN05", `<title>奶奶</title><script>var a="奶奶";</script><p class="cv2-note" style="color:red">奶奶</p><p>奶奶</p>`, `<title>奶奶</title><script>var a="奶奶";</script><p class="cv2-note" style="color:red">奶奶</p><p><span class="ch-text">奶奶</span></p>`],
  ["CHFUN05", `<p>Māori ākonga kaiako nǎinai</p>`, `<p>Māori ākonga kaiako nǎinai</p>`],
  ["CHFUN05", `<p>你好<br />再见</p>`, `<p><span class="ch-text">你好</span><br /><span class="ch-text">再见</span></p>`],
  ["CHFUN05", `<p>Ｗ１２３</p>`, `<p>Ｗ１２３</p>`],
  ["CHFUN05", `<p>a 你好\n\t再见 b</p>`, `<p>a <span class="ch-text">你好\n\t再见</span> b</p>`],
  ["JPN1004", `<p>Sachiko： かず！　もう　時間です。</p>`, `<p>Sachiko： <span class="jp-text">かず！　もう　時間です。</span></p>`],
  ["JPN1004", `<p>「ありがとう」と言う</p>`, `<p><span class="jp-text">「ありがとう」と言う</span></p>`],
  ["CHFUN05", `<p>x 。你好</p>`, `<p>x 。<span class="ch-text">你好</span></p>`],
  ["CHFUN05", `<p>。。。</p>`, `<p>。。。</p>`],
];
let ok = 0, bad = 0;
for (const [code, inp, exp] of cases) {
  const got = W(inp, code);
  if (got === exp) ok++; else { bad++; _l(`FAIL [${code}]\n  in : ${inp}\n  exp: ${exp}\n  got: ${got}`); }
}
// idempotence
for (const [code, inp] of cases) { const a = W(inp, code); if (W(a, code) !== a) { bad++; _l(`NOT IDEMPOTENT [${code}] ${inp}`); } }
// OFF toggle
process.env.LANGFONT_OFF = "1";
if (W(`<p>奶奶</p>`, "CHFUN05") !== `<p>奶奶</p>`) { bad++; _l("OFF toggle failed"); }
delete process.env.LANGFONT_OFF;
_l(`unit: ${ok} ok / ${bad} bad`);
process.exit(bad ? 1 : 0);
