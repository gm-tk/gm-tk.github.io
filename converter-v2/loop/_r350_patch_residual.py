import io, subprocess, os
p = r'C:\Users\Gavin\TeKura\FINAL_MODULE_DATA\pageforge-site\converter-v2\app\js\InteractiveBuilder.js'
s = io.open(p, encoding='utf-8', newline='').read()
old = ('\t\t\tconst residual = this.#cellText(imgCell).replace(/\\[[^\\]]*\\]/g, "").replace(/https?:\\/\\/\\S+/g, "")\n')
new = ('\t\t\tconst residual = imgCell.replace(/\\u{1f534}\\[RED TEXT\\][\\s\\S]*?\\[\\/RED TEXT\\]\\u{1f534}/gu, "")   // the red runs are notes / the tag, not residue\n'
       '\t\t\t\t.replace(/\\[[^\\]]*\\]/g, "").replace(/https?:\\/\\/\\S+/g, "")\n')
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new, 1)
tmp = p[:-3] + '.r350tmp.js'
io.open(tmp, 'w', encoding='utf-8', newline='').write(s)
r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True); assert r.returncode == 0, r.stderr
os.replace(tmp, p); print('ok')
