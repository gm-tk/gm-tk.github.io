import io, subprocess, os, json
PF = r'C:\Users\Gavin\TeKura\FINAL_MODULE_DATA\pageforge-site\converter-v2'
# (1) JS: the residual strip also drops a stray bracket (the r174 malformed-bracket class — BLL266's `[🔴image]🔴`) and a list bullet
p = os.path.join(PF, 'app', 'js', 'InteractiveBuilder.js')
s = io.open(p, encoding='utf-8', newline='').read()
old = ('\t\t\t\t.replace(/\\[[^\\]]*\\]/g, "").replace(/https?:\\/\\/\\S+/g, "")\n'
       '\t\t\t\t.replace(/[/|\\u2013\\u2014-]/g, " ").trim();\n')
new = ('\t\t\t\t.replace(/\\[[^\\]]*\\]/g, "").replace(/https?:\\/\\/\\S+/g, "")\n'
       '\t\t\t\t.replace(/[/|\\u2013\\u2014\\-\\[\\]\\u2022\\u00b7]/g, " ").trim();   // a stray bracket (r174\'s class — BLL266) / a list bullet are not residue\n')
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new, 1)
old2 = '\t\tconst tagRe = new RegExp(cfg.image_tag_pattern ?? "^\\\\[\\\\s*(?:insert\\\\s+)?image[^\\\\]]*\\\\]$", "i");\n'
new2 = '\t\tconst tagRe = new RegExp(cfg.image_tag_pattern ?? "^\\\\[?\\\\s*(?:insert\\\\s+)?(?:image|photo)[^\\\\]]*\\\\]?$", "i");\n'
assert s.count(old2) == 1, s.count(old2)
s = s.replace(old2, new2, 1)
tmp = p[:-3] + '.r350tmp.js'
io.open(tmp, 'w', encoding='utf-8', newline='').write(s)
r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True); assert r.returncode == 0, r.stderr
os.replace(tmp, p); print('js ok')
# (2) data: the tag pattern tolerates a missing bracket + [photo]
p = os.path.join(PF, 'data', 'Emit_Templates.json')
s = io.open(p, encoding='utf-8', newline='').read()
old3 = '\t\t\t\t"image_tag_pattern": "^\\\\[\\\\s*(?:insert\\\\s+)?image[^\\\\]]*\\\\]$",\n'
new3 = '\t\t\t\t"image_tag_pattern": "^\\\\[?\\\\s*(?:insert\\\\s+)?(?:image|photo)[^\\\\]]*\\\\]?$",\n'
assert s.count(old3) == 1, s.count(old3)
s = s.replace(old3, new3, 1)
def nodup(pairs):
    d = {}
    for k, v in pairs:
        if k in d: raise ValueError(k)
        d[k] = v
    return d
json.loads(s, object_pairs_hook=nodup)
tmp = p[:-5] + '.r350tmp.json'
io.open(tmp, 'w', encoding='utf-8', newline='').write(s)
os.replace(tmp, p); print('json ok')
