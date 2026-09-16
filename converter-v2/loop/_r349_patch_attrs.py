#!/usr/bin/env python3
"""ROUND 349 — patch 2 (found by the §0b whole-family probe): the label element's ATTRIBUTES are kept when it is re-emitted
(the MTK menus carry `<h5 eng>` / `<h5 reo>`; the first draft re-emitted a bare `<h5>`). Applied to the live engine AND to
the durable splice record `_r349_splice.py` (so the record still reproduces the engine from the HEAD blob). Idempotent."""
import io, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2", "app", "js", "ContentConverter.js"))
EDITS = [
    (r'''		const re = /<(p|h[1-6])\b[^>]*>([\s\S]*?)<\/\1>|<(ul|ol)\b[^>]*>[\s\S]*?<\/\3>/gi;
		let m;
		while ((m = re.exec(html)) !== null) {
			if (m[3]) { els.push({ kind: "list", start: m.index, end: m.index + m[0].length, raw: m[0] }); continue; }
			const inner = m[2], f = fold(inner), words = f ? f.split(" ").length : 0;''',
     r'''		const re = /<(p|h[1-6])\b([^>]*)>([\s\S]*?)<\/\1>|<(ul|ol)\b[^>]*>[\s\S]*?<\/\4>/gi;
		let m;
		while ((m = re.exec(html)) !== null) {
			if (m[4]) { els.push({ kind: "list", start: m.index, end: m.index + m[0].length, raw: m[0] }); continue; }
			const inner = m[3], attrs = m[2] || "", f = fold(inner), words = f ? f.split(" ").length : 0;'''),
    (r'''			els.push({ kind: "blk", tag: m[1].toLowerCase(), start: m.index, end: m.index + m[0].length, raw: m[0], inner, f, words, role, punct,''',
     r'''			els.push({ kind: "blk", tag: m[1].toLowerCase(), attrs, start: m.index, end: m.index + m[0].length, raw: m[0], inner, f, words, role, punct,'''),
    (r'''			out.push(`<h${level}>${label}</h${level}>`);''',
     r'''			out.push(`<h${level}${e.attrs}>${label}</h${level}>`);   // the element's own attributes are kept (the MTK menus' <h5 eng> / <h5 reo>)'''),
]
for path in (ENGINE, os.path.join(HERE, "_r349_splice.py")):
    s = io.open(path, encoding="utf-8", newline="").read()
    if "<h${level}${e.attrs}>" in s: print("already patched", os.path.basename(path)); continue
    for old, new in EDITS:
        assert s.count(old) == 1, (os.path.basename(path), old[:60]); s = s.replace(old, new, 1)
    if path.endswith(".js"):
        b = s.encode("utf-8"); tmp = path[:-3] + ".r349tmp.js"
        with open(tmp, "wb") as f: f.write(b)
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True); assert r.returncode == 0, r.stderr
        os.replace(tmp, path)
    else:
        with io.open(path, "w", encoding="utf-8", newline="") as f: f.write(s)
    print("patched", os.path.basename(path))
