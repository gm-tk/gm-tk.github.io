#!/usr/bin/env python3
"""ROUND 362 (loop session 19, Round 6 — the unclassified activity keeps its title heading and lead prose free) — the
anchored splice: data Interactive_Boundary_ChildTag_Bank._meta.opener_rule.unclassified_activity_lead (tabs, LF) and the
InteractiveScanner unclassified-activity path (the normal path's activityOwner / activityLeadItems form). Idempotent."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
APP = os.path.join(ROOT, "pageforge-site", "converter-v2", "app", "js"); DATA = os.path.join(ROOT, "pageforge-site", "converter-v2", "data")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

# ---- data (tabs; insert before the last key of opener_rule)
P = os.path.join(DATA, "Interactive_Boundary_ChildTag_Bank.json"); s = rd(P)
if '"unclassified_activity_lead"' not in s:
    A = '\t\t\t"_opener_tags_note": '
    assert s.count(A) == 1, s.count(A)
    DOC = ("ROUND 362 (the autonomous loop's session 19, Round 6 — the DIFF MINER's activity classes #542 / #535 / #533; KB 01F "
           "activity_heading). THE UNCLASSIFIED ACTIVITY KEEPS ITS TITLE HEADING AND LEAD PROSE FREE. An `[Activity N] Title` whose "
           "only widget signal is a data table (the BLL phonics pattern) is captured as an UNCLASSIFIED bundle; before this round the "
           "opener item itself was the bundle's first member, so the whole activity — title and instruction paragraph included — became "
           "the placeholder box, while the gold opens the box with `<h3>Title</h3>` + the instruction `<p>` and the widget follows "
           "(measured `outputs/_measure_r362_actlead.py`: 958 boxes / 247 modules / 535 pages open with h3 in the gold and with a "
           "capture in Claude's; 2605 boxes agree). Now the unclassified path records the opener as `bundle.activityOwner` and the items "
           "between it and the first TABLE (black runs, ELEMENT tags — [body] / headings / media —, instruction spans) as "
           "`bundle.activityLeadItems`, and swallows members from that table — exactly the normal path's activity-owner form, which "
           "ContentConverter already renders as the box's h3 title + lead prose + the placeholder box. Env UNCLASSLEAD_OFF = the opener "
           "collected as a member as before (byte-identical).")
    BLOCK = ('\t\t\t"unclassified_activity_lead": {\n'
             f'\t\t\t\t"_doc": "{DOC}",\n'
             '\t\t\t\t"enabled": true,\n'
             '\t\t\t\t"env": "UNCLASSLEAD_OFF"\n'
             '\t\t\t},\n')
    s = s.replace(A, BLOCK + A, 1); wr(P, s); print("BoundaryBank: spliced")
    d = json.loads(rd(P)); assert d["_meta"]["opener_rule"]["unclassified_activity_lead"]["env"] == "UNCLASSLEAD_OFF"
else:
    print("BoundaryBank: already")

# ---- scanner
P = os.path.join(APP, "InteractiveScanner.js"); s = rd(P)
if "unclassified_activity_lead" not in s:
    OLD = ('\t\t\t\t\t// the activity item itself is the first member (its\n'
           '\t\t\t\t\t// blackAfter carries the activity title/instructions)\n'
           '\t\t\t\t\tthis.#collectMember(bundle, it, run);\n'
           '\t\t\t\t\tbundle.endIndex = this.#swallowMembers(bundle, items, i + 1,\n'
           '\t\t\t\t\t\t/* headings terminate the unknown widget: */ true, absolute, run, normaliser);\n')
    assert s.count(OLD) == 1, s.count(OLD)
    NEW = ('\t\t\t\t\t// ROUND 362 — THE UNCLASSIFIED ACTIVITY KEEPS ITS TITLE AND LEAD PROSE FREE (the\n'
           '\t\t\t\t\t// autonomous loop\'s session 19 Round 6; the DIFF MINER\'s activity classes #542 /\n'
           '\t\t\t\t\t// #535 / #533; KB 01F activity_heading). The gold opens such a box with the\n'
           '\t\t\t\t\t// <h3> title + the instruction paragraph and the widget follows; collecting the\n'
           '\t\t\t\t\t// opener as the first member swallowed both into the placeholder box. This is\n'
           '\t\t\t\t\t// the NORMAL path\'s activity-owner form applied here: the opener becomes\n'
           '\t\t\t\t\t// bundle.activityOwner, the items between it and the first TABLE (black runs,\n'
           '\t\t\t\t\t// ELEMENT tags — [body] / headings / media —, instruction spans) become\n'
           '\t\t\t\t\t// bundle.activityLeadItems, and the members start at that table. ContentConverter\n'
           '\t\t\t\t\t// already renders an owned bundle as h3 title + lead prose + the widget box.\n'
           '\t\t\t\t\t// Data: BoundaryBank._meta.opener_rule.unclassified_activity_lead   Env: UNCLASSLEAD_OFF\n'
           '\t\t\t\t\tconst _ualCfg = DataService.Data.BoundaryBank?._meta?.opener_rule?.unclassified_activity_lead;\n'
           '\t\t\t\t\tconst _ualOn = !!_ualCfg && _ualCfg.enabled !== false\n'
           '\t\t\t\t\t\t&& !(typeof process !== "undefined" && process.env && process.env[_ualCfg.env || "UNCLASSLEAD_OFF"]);\n'
           '\t\t\t\t\tif (_ualOn) {\n'
           '\t\t\t\t\t\tlet j = i + 1;\n'
           '\t\t\t\t\t\twhile (j < items.length && items[j].consumedBy === undefined && items[j].type !== "table"\n'
           '\t\t\t\t\t\t\t&& (items[j].type === "black" || items[j].type === "assettodo"\n'
           '\t\t\t\t\t\t\t\t|| (items[j].type === "tag" && (!items[j].parse?.primary || items[j].parse.primary.directive === "ELEMENT")))) j++;\n'
           '\t\t\t\t\t\tbundle.activityOwner = it;\n'
           '\t\t\t\t\t\tbundle.activityLeadItems = items.slice(i + 1, j);\n'
           '\t\t\t\t\t\tbundle.endIndex = this.#swallowMembers(bundle, items, j,\n'
           '\t\t\t\t\t\t\t/* headings terminate the unknown widget: */ true, absolute, run, normaliser);\n'
           '\t\t\t\t\t} else {\n'
           '\t\t\t\t\t\t// the activity item itself is the first member (its\n'
           '\t\t\t\t\t\t// blackAfter carries the activity title/instructions)\n'
           '\t\t\t\t\t\tthis.#collectMember(bundle, it, run);\n'
           '\t\t\t\t\t\tbundle.endIndex = this.#swallowMembers(bundle, items, i + 1,\n'
           '\t\t\t\t\t\t\t/* headings terminate the unknown widget: */ true, absolute, run, normaliser);\n'
           '\t\t\t\t\t}\n')
    s = s.replace(OLD, NEW, 1); wr(P, s); print("InteractiveScanner.js: spliced")
else:
    print("InteractiveScanner.js: already")
print("splice done")
