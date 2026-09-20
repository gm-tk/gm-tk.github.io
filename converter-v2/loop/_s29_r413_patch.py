import io
p = "app/js/InteractiveScanner.js"
s = io.open(p, encoding="utf-8", newline="").read()
old = """		const owned = bundle.activityOwner !== undefined;
		if (owned) {
			const oc = cfg.owned_bundles;
			if (!oc || oc.enabled === false) return;
			if (typeof process !== "undefined" && process.env && process.env[oc.env || "HEADTABLEOWNED_OFF"]) return;
"""
new = """		const owned = bundle.activityOwner !== undefined;
		const oc = cfg.owned_bundles;
		const ocOn = !!oc && oc.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[oc.env || "HEADTABLEOWNED_OFF"]);
		if (owned) {
			if (!ocOn) return;
"""
assert s.count(old) == 1; s = s.replace(old, new)
old2 = """		const betweenMedia = new Set((cfg.between_media_tags ?? []).map((t) => String(t).toLowerCase()));"""
new2 = """		const betweenMedia = new Set(((ocOn && oc.between_media_tags) || []).map((t) => String(t).toLowerCase()));"""
assert s.count(old2) == 1; s = s.replace(old2, new2)
io.open(p, "w", encoding="utf-8", newline="").write(s)
d = "data/Interactive_Boundary_ChildTag_Bank.json"
t = io.open(d, encoding="utf-8", newline="").read()
o3 = '\t\t\t\t"between_media_tags": ["image", "video", "audio"],\n\t\t\t\t"max_between": 6,\n'
assert t.count(o3) == 1; t = t.replace(o3, '\t\t\t\t"max_between": 6,\n')
o4 = '\t\t\t\t\t"enabled": true,\n\t\t\t\t\t"env": "HEADTABLEOWNED_OFF"\n'
assert t.count(o4) == 1; t = t.replace(o4, '\t\t\t\t\t"enabled": true,\n\t\t\t\t\t"env": "HEADTABLEOWNED_OFF",\n\t\t\t\t\t"between_media_tags": ["image", "video", "audio"]\n')
io.open(d, "w", encoding="utf-8", newline="").write(t)
print("patched")
