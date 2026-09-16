// _r348_cache_unit.cjs — ROUND 348: a unit test of batch_convert.cjs's oembed-cache block (the race fix), run on the
// ACTUAL source text (extracted from batch_convert.cjs, never a copy) against a scratch cache file.
//   1. a torn / corrupt cache file → readCache warns and starts EMPTY (no throw — the r347 batch-26 failure mode);
//   2. saveCache with nothing dirty → NO write (the file's bytes and mtime unchanged);
//   3. saveCache when dirty → an atomic tmp + rename: the result parses, carries the in-memory entries MERGED with the
//      file's current entries (a parallel worker's fetches are kept), no .tmp is left behind, cacheDirty resets to 0.
// Usage: node _r348_cache_unit.cjs   (from anywhere; writes only under os.tmpdir())
"use strict";
const fs = require("fs"), path = require("path"), os = require("os"), vm = require("vm");
const SRC = path.join(__dirname, "..", "reference", "tests", "batch_convert.cjs");
const src = fs.readFileSync(SRC, "utf8");
const i0 = src.indexOf("const readCache = "), i1 = src.indexOf("globalThis.DataService = {");
if (i0 < 0 || i1 < 0 || i1 < i0) { console.log("FAIL: cache block not found in batch_convert.cjs"); process.exit(1); }
const block = src.slice(i0, i1);
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "r348cache-"));
const CACHE_FILE = path.join(dir, "oembed_cache.json");
const warnings = [];
function load(fileText) {
	if (fileText === null) { if (fs.existsSync(CACHE_FILE)) fs.unlinkSync(CACHE_FILE); }
	else fs.writeFileSync(CACHE_FILE, fileText);
	const ctx = { fs, CACHE_FILE, process, console: { error: (m) => warnings.push(m), log: () => {} },
		j: (p) => JSON.parse(fs.readFileSync(p, "utf8")) };
	vm.createContext(ctx);
	vm.runInContext(block + "\nthis.oembedCache = oembedCache; this.saveCache = saveCache; this.dirty = () => cacheDirty; this.touch = () => { cacheDirty++; };", ctx);
	return ctx;
}
let fails = 0;
const check = (ok, msg) => { console.log(`${ok ? "PASS" : "FAIL"}: ${msg}`); if (!ok) fails++; };

// 1. torn file
let c = load('{"abc": {"ok": true, "title": "T');
check(c.oembedCache.size === 0 && warnings.length === 1 && /unreadable/.test(warnings[0]), `torn cache → empty map + one warning (${warnings[0] || "none"})`);

// 2. clean → no write
c = load('{"v1":{"ok":true,"title":"one","channel":"c"}}');
const st0 = fs.statSync(CACHE_FILE); const b0 = fs.readFileSync(CACHE_FILE, "utf8");
c.saveCache();
check(fs.readFileSync(CACHE_FILE, "utf8") === b0 && fs.statSync(CACHE_FILE).mtimeMs === st0.mtimeMs, "saveCache with nothing dirty writes nothing");

// 3. dirty → atomic merged write
c.oembedCache.set("v2", { ok: false, reason: "error" }); c.touch();
fs.writeFileSync(CACHE_FILE, '{"v1":{"ok":true,"title":"one","channel":"c"},"v3":{"ok":true,"title":"from a parallel worker","channel":"w"}}');
c.saveCache();
const after = JSON.parse(fs.readFileSync(CACHE_FILE, "utf8"));
check(after.v1 && after.v2 && after.v3 && after.v2.reason === "error", `saveCache merges the file's entries with memory (${Object.keys(after).join(",")})`);
check(!fs.readdirSync(dir).some((f) => f.endsWith(".tmp")), "no .tmp left behind (renamed over the target)");
check(c.dirty() === 0, "cacheDirty resets to 0 after a save");
fs.rmSync(dir, { recursive: true, force: true });
console.log(fails ? `RESULT: ${fails} FAIL ✗` : "RESULT: the oembed-cache block is torn-tolerant, no-op when clean, atomic + merged when dirty ✓");
process.exit(fails ? 1 : 0);
