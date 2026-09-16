import io, subprocess, os
PF = r'C:\Users\Gavin\TeKura\FINAL_MODULE_DATA\pageforge-site\converter-v2'
p = os.path.join(PF, 'app', 'js', 'InteractiveBuilder.js')
s = io.open(p, encoding='utf-8', newline='').read()
# header row: a short all-red column LABEL ("Image | words", the r63 label-row class) or a pure bracket token ("[correct answers]") is markup, not a note
old = ('\t\t\tfor (const c of rows[0]) if (this.#hasRedText(c)) { const t = this.#cellText(c); if (t) notes.push(t); }\n')
new = ('\t\t\tfor (const c of rows[0]) if (this.#hasRedText(c)) { const t = this.#cellText(c); if (this.#ddIsNote(t, cfg)) notes.push(t); }\n')
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new, 1)
old2 = ('\t\t\tfor (const x of reds) if (!tagRe.test(x)) notes.push(x);\n')
new2 = ('\t\t\tfor (const x of reds) if (!tagRe.test(x) && this.#ddIsNote(x, cfg)) notes.push(x);\n')
assert s.count(old2) == 1, s.count(old2)
s = s.replace(old2, new2, 1)
# the helper, before #ddImage's doc comment
old3 = ('\t/**\n'
        '\t * ROUND 350 — a drag item\'s image in the run\'s image mode')
new3 = ('\t/**\n'
        '\t * ROUND 350 — is a red run in the image-pair table a developer NOTE (ride along as a Writers Note) or MARKUP (drop\n'
        '\t * silently)? Markup = a run made entirely of bracketed tokens ("[correct answers]", "[image] [media item 39]" — the r282\n'
        '\t * rule) or a short bare column LABEL ("Image", "words" — the r63 all-red label-row class, at most label_max_words words);\n'
        '\t * anything longer with real words ("Correct answer - can we jumble them up though please.", "Arrow added to image") is a note.\n'
        '\t */\n'
        '\tstatic #ddIsNote(text, cfg) {\n'
        '\t\tconst t = String(text ?? "").trim();\n'
        '\t\tif (!t) return false;\n'
        '\t\tconst bare = t.replace(/\\[[^\\]]*\\]/g, " ").replace(/[\\[\\]]/g, " ").trim();\n'
        '\t\tif (!/[\\p{L}\\p{N}]/u.test(bare)) return false;                       // bracket tokens only → markup\n'
        '\t\tconst words = bare.split(/\\s+/).filter(Boolean).length;\n'
        '\t\tif (words <= (cfg.label_max_words ?? 3) && !/[.:;!?,]/.test(bare)) return false;   // a bare column label\n'
        '\t\treturn true;\n'
        '\t}\n'
        '\n'
        '\t/**\n'
        '\t * ROUND 350 — a drag item\'s image in the run\'s image mode')
assert s.count(old3) == 1, s.count(old3)
s = s.replace(old3, new3, 1)
tmp = p[:-3] + '.r350tmp.js'
io.open(tmp, 'w', encoding='utf-8', newline='').write(s)
r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True); assert r.returncode == 0, r.stderr
os.replace(tmp, p); print('js ok')
