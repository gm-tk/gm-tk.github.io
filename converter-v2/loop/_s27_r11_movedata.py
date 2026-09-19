# _s27_r11_movedata.py — relocate opener_rule.id_heading_opener.bare_red_opener -> opener_rule.bare_red_opener
# (the engine reads _meta.opener_rule.bare_red_opener; the block had been inserted one level too deep). LF-preserving.
import io, os, re, json
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2", "data", "Interactive_Boundary_ChildTag_Bank.json")
p = os.path.abspath(p)
s = io.open(p, "r", encoding="utf-8", newline="").read()
assert "\r\n" not in s, "CRLF found"
lines = s.split("\n")
# locate the nested block: 4-tab indent "bare_red_opener": { ... "},"
start = next(i for i, l in enumerate(lines) if l == '\t\t\t\t"bare_red_opener": {')
end = next(i for i in range(start + 1, len(lines)) if lines[i] == "\t\t\t\t},")
block = lines[start:end + 1]
del lines[start:end + 1]
# re-indent by one tab less
block = [l[1:] if l.startswith("\t") else l for l in block]
# insert after the owner_alias_exclude block close (3-tab "},") that precedes "opener_tags"
ot = next(i for i, l in enumerate(lines) if l == '\t\t\t"opener_tags": [')
assert lines[ot - 1] == "\t\t\t},", lines[ot - 1]
lines[ot:ot] = block
out = "\n".join(lines)
json.loads(out)
io.open(p, "w", encoding="utf-8", newline="").write(out)
d = json.loads(out)
print("top-level keys:", list(d["_meta"]["opener_rule"].keys()))
print("nested still present:", "bare_red_opener" in d["_meta"]["opener_rule"]["id_heading_opener"])
print("moved block enabled:", d["_meta"]["opener_rule"]["bare_red_opener"]["enabled"])
