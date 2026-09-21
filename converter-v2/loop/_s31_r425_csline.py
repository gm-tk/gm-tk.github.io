"""_s31_r425_csline.py — round 425: a `CS:` / `To CS:` line in an activity row is a Writers Note (RED span), not prose.
Run under WSL from CONVERTER_V2/outputs: python3 _s31_r425_csline.py"""
import io, os
JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2", "app", "js")

def patch(name, old, new):
    p = os.path.join(JS, name)
    s = io.open(p, encoding="utf-8", newline="").read()
    assert s.count(old) == 1, (name, s.count(old))
    s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("patched", name)

patch("DocxExtractor.js",
"""		const isCs = (s) => /^(to\\s+)?cs\\s*:/i.test(plain(s));
""",
"""		const isCs = (s) => re(ad.cs_line_pattern ?? "^(to\\\\s+)?cs\\\\s*:").test(plain(s));
""")

patch("DocxExtractor.js",
"""				const s = stripInstruction(l);
				if (!s) continue;
				if (first && !isImage(s) && !isCs(s)) { push(TAG("Body") + s, links); first = false; }
				else push(s, links);
""",
"""				const s = stripInstruction(l);
				if (!s) continue;
				// a `CS:` / `To CS:` line is the writer's note to Creative Services — a RED span, so the
				// standard instruction path renders it as the Writers Note (data cs_lines_as_instruction)
				if (isCs(s) && ad.cs_lines_as_instruction !== false) { push(RED(plain(s)), links); continue; }
				if (first && !isImage(s) && !isCs(s)) { push(TAG("Body") + s, links); first = false; }
				else push(s, links);
""")
