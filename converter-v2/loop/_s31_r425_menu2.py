"""_s31_r425_menu2.py — round 425: the trailing-prose rule fires only after the LAST left label (Do) — a label's own paragraph stays left."""
import io, os
JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2", "app", "js")
p = os.path.join(JS, "MenuBuilder.js"); s = io.open(p, encoding="utf-8", newline="").read()
old = """							const left = famHit || (famLeft ?? cfg.left_match).some((m) => folded.startsWith(m));
							const right = (cfg.right_match ?? []).some((m) => folded.includes(m));
"""
new = """							const left = famHit || (famLeft ?? cfg.left_match).some((m) => folded.startsWith(m));
							const right = (cfg.right_match ?? []).some((m) => folded.includes(m));
							if (famLeft && left) famLastLabel = folded.startsWith(String(famLeft[famLeft.length - 1]));   // r425: past the last left label?
"""
assert s.count(old) == 1; s = s.replace(old, new)
old = """						if (inqFamily && inqCfg.trailing_prose_right && bucket === "left" && line.trim()
							&& !/^\*\*/.test(line.trim())
"""
new = """						if (inqFamily && inqCfg.trailing_prose_right && bucket === "left" && famLastLabel && line.trim()
							&& !/^\*\*/.test(line.trim())
"""
assert s.count(old) == 1; s = s.replace(old, new)
# declare the latch beside `bucket`
old = """		let bucket = archetype === "tabs" ? "tab1\""""
new = """		let famLastLabel = false;   // r425: the item family — set once the LAST left label (Do) has opened; trailing prose then goes right
		let bucket = archetype === "tabs" ? "tab1\""""
assert s.count(old) == 1, s.count(old); s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="").write(s); print("patched")
