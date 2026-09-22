/** _s36_r2_headpayload.cjs — session 36 Round 2 PICK measurement: THE HEAD-MATCHED TAG WHOSE PAYLOAD SPAWNS A HIGHER-RANKED TAG.
 *  Over every parsed Writers Template: each red span whose first bracket fragment has a colon; parse it with the live TagNormaliser;
 *  report the spans where the FIRST tag was matched on the HEAD (text before the colon) and a later pass found another alias INSIDE
 *  the payload, so the primary is NOT the head's tag. Group by (head tag → primary tag) and by module. reference/tests under WSL:
 *    node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s36_r2_headpayload.cjs > ../../outputs/_s36_r2_headpayload.log */
"use strict";
const fs = require("fs"), path = require("path");
const TESTS = path.join(__dirname, "..", "reference", "tests");
const eng = require(path.join(TESTS, "_engine_load.cjs"));
const GOLD = path.join(__dirname, "..", "..", "01-Finalized_Modules_");
globalThis.DataService = { Data: eng.loadData(), async FetchOembed() { return { ok: false }; } };
const _l = console.log.bind(console); console.log = () => {}; console.warn = () => {};
eng.loadEngine();
const norm = new TagNormaliser(DataService.Data.TagLexicon, DataService.Data.TagExceptions, DataService.Data.InstructionCues);
const RED = /\u{1f534}\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\u{1f534}/gu;
const byPair = new Map(), byMod = new Map(), ex = new Map();
let spans = 0, colonSpans = 0, hits = 0;
for (const tpl of fs.readdirSync(GOLD)) {
  const tdir = path.join(GOLD, tpl); if (!fs.statSync(tdir).isDirectory()) continue;
  for (const code of fs.readdirSync(tdir)) {
    const mdir = path.join(tdir, code); if (!fs.statSync(mdir).isDirectory()) continue;
    for (const f of fs.readdirSync(mdir).filter((x) => /Writers.*parsed\.txt$/i.test(x))) {
      const txt = fs.readFileSync(path.join(mdir, f), "utf8");
      for (const m of txt.matchAll(RED)) {
        const raw = m[1]; spans++;
        const br = /\[([^\]]*)\]/.exec(raw); if (!br || !br[1].includes(":")) continue;
        colonSpans++;
        let p; try { p = norm.Parse(raw); } catch { continue; }
        if (!p.tags || p.tags.length < 2 || !p.primary) continue;
        const first = p.tags[0];
        if (first.how !== "head") continue;
        if (p.primary.tag === first.tag) continue;
        hits++;
        const key = `${first.tag} -> ${p.primary.tag} (${p.primary.how})`;
        byPair.set(key, (byPair.get(key) ?? 0) + 1);
        byMod.set(code, (byMod.get(code) ?? 0) + 1);
        if (!ex.has(key)) ex.set(key, []);
        if (ex.get(key).length < 4) ex.get(key).push(`${code}: ${raw.replace(/\s+/g, " ").trim().slice(0, 90)}`);
      }
    }
  }
}
_l(`red spans ${spans}; with a colon in the first bracket ${colonSpans}; head-matched with a payload-spawned PRIMARY of another tag: ${hits} (modules ${byMod.size})`);
_l("by head tag -> primary:");
for (const [k, v] of [...byPair].sort((a, b) => b[1] - a[1])) { _l(`  ${v.toString().padStart(4)}  ${k}`); for (const e of ex.get(k)) _l(`          ${e}`); }
_l("by module (top 25):");
for (const [k, v] of [...byMod].sort((a, b) => b[1] - a[1]).slice(0, 25)) _l(`  ${v.toString().padStart(4)}  ${k}`);
