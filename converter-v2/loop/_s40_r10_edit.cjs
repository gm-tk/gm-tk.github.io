// one-off (session 40 Round 10): turn the r9 journal-default recorder copy into the image own-text recorder — patch MediaBuilder.image
// to record, per image with a r240 drop, the own-text lines and which were dropped; print IMGOWN lines. Never touches the corpus.
const fs = require("fs"); const p = process.argv[2]; let s = fs.readFileSync(p, "utf8");
s = s.replace(/const LINE = [^\n]*\n/, 'const LINE = "keep = ownKept + following;";\n');
s = s.replace(/const rec = [^\n]*\n/, 'const rec = " (globalThis.__jd = globalThis.__jd || []).push({ code: run.moduleCode, own: own.split(\\"\\n\\").map((line) => ({ t: line, drop: !!fold(line) && (anchors.includes(fold(line)) || refRe.test(fold(line))) })) });";\n');
s = s.replace('fs.readFileSync(path.join(eng.APP, "ContentConverter.js"), "utf8")', 'fs.readFileSync(path.join(eng.APP, "MediaBuilder.js"), "utf8")');
s = s.replace(/for \(const r of globalThis\.__jd\) _l\([^\n]*\n/, 'for (const r of globalThis.__jd) { const L = r.own; for (let k = 0; k + 1 < L.length; k++) if (!L[k].drop && L[k + 1].drop && L[k].t.trim()) _l(`IMGOWN\t${code}\t${clip(L[k].t)}\t${clip(L[k + 1].t)}`); }\n');
fs.writeFileSync(p, s);
