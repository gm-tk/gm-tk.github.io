#!/usr/bin/env python3
"""r326 helper — write the exclude_label_match pattern with JSON-escaped \\b word boundaries."""
import io, json, os, re
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2", "data", "Emit_Templates.json")
s = io.open(P, encoding="utf-8", newline="").read()
i = s.index('"exclude_label_match": "')
j = s.index('",', i)
pattern = r"^(check(?!point)|reset|show(?! us)|reveal|hide|try again|clear|see (the )?answers?|click to)\b|\b(answers?|reveal)\b"
s = s[:i] + '"exclude_label_match": ' + json.dumps(pattern) + s[j + 1:]
io.open(P, "w", encoding="utf-8", newline="").write(s)
d = json.load(io.open(P, encoding="utf-8"))
pat = d["buttons"]["anchor_wrap"]["exclude_label_match"]
print(repr(pat))
r = re.compile(pat, re.I)
for t in ["Check answers", "Reset", "Checkpoint", "Show us", "Go to your journal", "Upload to dropbox", "Reveal answer", "Answers", "Go to quiz", "Submit answers"]:
    print("%-20s %s" % (t, bool(r.search(t))))
