"""ROUND 320 splice (loop Round 7) — the upload box releases the writer's text in the writer's order around the button.
Anchored, unique-match edits in bytes mode (LF files, tabs preserved). Idempotent (prefix test).
History: the first draft split at the OPENER; the in-memory probe showed a same-type merge (two dropbox brackets, one
button — the r242/r279 rule) carries its text BETWEEN the brackets, so the split moved to the LAST bracket member."""
ROOT = r"C:/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/"
IB = ROOT + "app/js/InteractiveBuilder.js"
ET = ROOT + "data/Emit_Templates.json"

def edit(path, pairs):
    b = open(path, "rb").read()
    for old, new in pairs:
        o = old.encode("utf-8"); n = new.encode("utf-8")
        ins = n[:-len(o)] if n.endswith(o) else (n[len(o):] if n.startswith(o) else n)
        if b.count(ins) == 1 and (n.endswith(o) or n.startswith(o) or b.count(o) == 0):
            print("already applied:", path.split("/")[-1], old[:40].strip()); continue
        cnt = b.count(o)
        assert cnt == 1, f"{path}: anchor count {cnt} != 1 for anchor starting {old[:60]!r}"
        b = b.replace(o, n)
    open(path, "wb").write(b)
    print("edited", path.split("/")[-1], len(pairs), "edit(s)")

# ---------------------------------------------------------------- data block (upload_box, after "enabled": true)
DATA_OLD = ('\t\t\t"upload_box": {\n'
 '\t\t\t\t"_doc": "ROUND 308 (Chris, 2026-08-11 \u2014 \'Build it\'; the round-306 follow-t')
b = open(ET, "rb").read()
i = b.find(DATA_OLD.encode("utf-8")); assert i > 0
j = b.find(b'\t\t\t\t"enabled": true,\n', i); assert 0 < j < i + 4000
ANCH = b[i:j + len(b'\t\t\t\t"enabled": true,\n')].decode("utf-8")
DATA_NEW = (ANCH +
 '\t\t\t\t"release_split": {\n'
 '\t\t\t\t\t"enabled": true,\n'
 '\t\t\t\t\t"env": "DBXORDER_OFF",\n'
 '\t\t\t\t\t"_round320_note": "ROUND 320 (the autonomous loop\'s Round 7, 2026-09-15). Round 308 released the bundle\'s captured learner text AFTER the button (button, To Do note, text) whatever the writer\'s order \\u2014 XTAS101 1G\'s \'3. Upload some pictures \\u2026 here.[insert dropbox link]\' shipped the button above its own list item. The gold keeps the dropbox button as the activity box\'s LAST content child in 629/720 non-BLL (87%) and 463/475 BLL (97%) boxes (KB constraint 43: an activity that ENDS in the button), and puts text the writer typed AFTER the marker after the button (XDLS901 \'Ka pai! You can now arrange\\u2026\'). THE RULE: the scanner keeps memberItems in document order (backward absorptions unshift), so the scan splits the released text at the LAST dropbox bracket member (a same-type merge holds two brackets and ONE button) \\u2014 text captured before it renders before the button, the bracket\'s own trailing text and later members after it. MEASURED: 49 upload boxes on 46 pages / 35 modules shipped released text directly after the button; 37 activity boxes on 35 pages carried content after their dropbox button. Env toggle DBXORDER_OFF reverts to the round-308 order (button first) byte-for-byte."\n'
 '\t\t\t\t},\n')

# ---------------------------------------------------------------- InteractiveBuilder (a) the scan: the split counter
IB_A_OLD = ('\t\tconst raw = [];        // captured learner text, in the writer\'s own order (unrendered)\n'
 '\t\tconst push = (t) => { const s = String(t ?? "").trim(); if (s) raw.push(s); };\n'
 '\t\tfor (const m of bundle.memberItems ?? []) {\n'
 '\t\t\tif (!m) continue;\n'
 '\t\t\tif (m.type === "black") { push(m.text); continue; }\n')
IB_A_NEW = ('\t\tconst raw = [];        // captured learner text, in the writer\'s own order (unrendered)\n'
 '\t\t// ROUND 320: the split point \u2014 the button stands where the writer\'s LAST dropbox\n'
 '\t\t// marker stood (a same-type merge holds two brackets and ONE button, the r242/r279\n'
 '\t\t// rule), so text captured before that marker (memberItems is document order \u2014\n'
 '\t\t// the scanner\'s backward absorptions unshift) renders before the button and the\n'
 '\t\t// marker\'s own trailing text and later members after it.\n'
 '\t\tlet nBefore = 0;\n'
 '\t\tconst push = (t) => { const s = String(t ?? "").trim(); if (s) raw.push(s); };\n'
 '\t\tfor (const m of bundle.memberItems ?? []) {\n'
 '\t\t\tif (!m) continue;\n'
 '\t\t\tif (m.type === "black") { push(m.text); continue; }\n')
IB_D_OLD = ('\t\t\t\tif (w) spec.push(w);                              // every bracket\'s words reach the note\n')
IB_D_NEW = ('\t\t\t\tif (w) spec.push(w);                              // every bracket\'s words reach the note\n'
 '\t\t\t\tnBefore = raw.length;                             // ROUND 320: text so far precedes this marker\n')
IB_B_OLD = ('\t\treturn { opener, spec, raw };\n')
IB_B_NEW = ('\t\treturn { opener, spec, raw, nBefore };\n')
# ---------------------------------------------------------------- InteractiveBuilder (b) the builder: emit around the button
IB_C_OLD = ('\t\treturn [btn, note, ...content].join("\\n");\n')
IB_C_NEW = ('\t\t// ROUND 320 \u2014 the writer\'s order around the button: text captured before the\n'
 '\t\t// marker renders before it, text after the marker after it (gold: the button is\n'
 '\t\t// the box\'s last child 87% / 97%). Data upload_box.release_split; env DBXORDER_OFF.\n'
 '\t\tconst rs = cfg.release_split;\n'
 '\t\tconst rsOn = !!rs && rs.enabled !== false\n'
 '\t\t\t&& !(typeof process !== "undefined" && process.env && process.env[rs.env ?? "DBXORDER_OFF"]);\n'
 '\t\tif (rsOn && scan.nBefore > 0) return [...content.slice(0, scan.nBefore), btn, note, ...content.slice(scan.nBefore)].join("\\n");\n'
 '\t\treturn [btn, note, ...content].join("\\n");\n')

edit(ET, [(ANCH, DATA_NEW)])
edit(IB, [(IB_A_OLD, IB_A_NEW), (IB_D_OLD, IB_D_NEW), (IB_B_OLD, IB_B_NEW), (IB_C_OLD, IB_C_NEW)])
print("done")
