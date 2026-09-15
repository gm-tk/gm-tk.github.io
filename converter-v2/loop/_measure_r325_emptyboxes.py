#!/usr/bin/env python3
"""ROUND 325 measure — the EMPTY hand-off boxes (body_compare's `empty_widgets`: a cv2-interactive placeholder
with < 40 chars of member text). For every Claude page: each un-built box, its widget type (from the banner),
its member text length, and the writer's own span text; classify the empties by type and by shape (a bare
tag with nothing after it / a tag whose members went elsewhere). Writes outputs/_r325_emptyboxes.json."""
import re, glob, collections, os, json
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
BANNER = re.compile(r'INTERACTIVE \(un-built\) #(\d+): ([A-Za-z]+)')
types = collections.Counter(); pages = set(); mods = set(); samples = collections.defaultdict(list); n = 0; per_tmpl = collections.Counter()
rows = []
for f in glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", "*", "*.html")):
    parts = f.replace("\\", "/").split("/"); code = parts[-2]; tmpl = parts[-3]
    s = open(f, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r'<div class="cv2-interactive" data-cv2-index="(\d+)"[^>]*>', s):
        i = m.end(); depth = 1; j = len(s)
        for mm in re.finditer(r'<div\b|</div>', s[i:]):
            depth += 1 if mm.group(0) == "<div" else -1
            if depth == 0: j = i + mm.start(); break
        inner = s[i:j]
        b = BANNER.search(inner); ty = b.group(2) if b else "?"
        body = re.sub(r'<p style="color: #d9480f[^>]*>.*?</p>', "", inner, count=1, flags=re.S)
        txt = re.sub(r"<[^>]+>", " ", body); txt = re.sub(r"\s+", " ", txt).strip()
        if len(txt) < 40:
            n += 1; types[ty] += 1; pages.add(f); mods.add(code); per_tmpl[tmpl] += 1
            rows.append({"tmpl": tmpl, "code": code, "page": os.path.basename(f), "type": ty, "text": txt[:80]})
            if len(samples[ty]) < 3: samples[ty].append((code, os.path.basename(f), txt[:50]))
json.dump({"empty_boxes": n, "pages": len(pages), "modules": len(mods), "by_type": dict(types), "by_template": dict(per_tmpl), "rows": rows},
          open(os.path.join(ROOT, "CONVERTER_V2", "outputs", "_r325_emptyboxes.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"empty hand-off boxes: {n} on {len(pages)} pages / {len(mods)} modules; by template {dict(per_tmpl)}")
for t, c in types.most_common(15): print(f"  {t:<18} {c:>4}  e.g. {samples[t][:3]}")
