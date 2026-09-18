#!/usr/bin/env python3
"""Session 26 Round 4 (engine r390) — the supervisor note's explicit closer makes the panel a SPAN.
Data: `callouts.by_tag."supervisor note".explicit_close_span {enabled, env: SUPSPAN_OFF}`.
Engine (ContentConverter.js): (1) `#explicitCloseAhead(bodyItems, i, canonTag, stopAtActivity)` — the family set also accepts
the closer of a tag_promote source; an [Activity] opener ends the scan when asked; (2) the own_row branch opens the panel in
SPAN mode on a hit (stack mode `span-own`); (3) emit() opens no content row while an own-row span is open and pushes its close
directly; (4) autoClose treats `span-own` like a writer's span. LF preserved. Idempotent. Run under WSL: python3 _s26_r390_splice.py"""
import io, sys
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2"

# ---- data ----
P = ROOT + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"explicit_close_span"' not in s:
    old = '\t\t\t\t"fold_page_label": {\n\t\t\t\t\t"enabled": true,\n\t\t\t\t\t"_note": "ROUND 163'
    assert s.count(old) == 1, s.count(old)
    new = ('\t\t\t\t"explicit_close_span": {\n'
           '\t\t\t\t\t"enabled": true,\n'
           '\t\t\t\t\t"env": "SUPSPAN_OFF",\n'
           '\t\t\t\t\t"stop_at_activity": true,\n'
           '\t\t\t\t\t"_doc": "ROUND 390 (the autonomous loop\'s session 26 Round 4 — the paired row-break census direction A, kind `row` = the super-content panel: outputs/_s26_rowpair.py, _s26_r390_supclose.py, _s26_r390_supshape.py). A writer who CLOSES the note explicitly — `[Supervisor Button] … [End Supervisor button]` (XDLS904 / 905 / 906, 21 pairs) or `[Supervisor note] … [end supervisor note]` (XDLS502, XDLS901) — means the whole run to the closer is the panel\'s content: the gold\'s panel holds every paragraph and bullet between (Leaving to Learn paired 22 / 0); the strict gather stopped at the first tag item (a bullet\'s trailing inline `[link to X]`) and shipped the rest as free rows. On a matching closer ahead (#explicitCloseAhead — the family set also accepts the closer of a tag_promote source, `end supervisor button`; an [Activity] opener ends the scan so an own-row span never swallows an activity) the own_row panel opens in SPAN mode (stack mode span-own): the loop renders the items between inside the panel\'s column, a heading never closes it (the writer\'s closer is authoritative; a section marker / page boundary does), the closer pops it. Every family without an explicit closer is untouched by construction. OFF = the strict panel (the r389 output)."\n'
           '\t\t\t\t},\n' + old)
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: explicit_close_span added")
else:
    print("data: already")

# ---- engine ----
P2 = ROOT + "/app/js/ContentConverter.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "ownSpanClose" not in s:
    # (1) explicitCloseAhead: promoted-source closers + the activity stop
    old = ("\tstatic #explicitCloseAhead(bodyItems, i, canonTag) {\n")
    assert s.count(old) == 1
    s = s.replace(old, "\tstatic #explicitCloseAhead(bodyItems, i, canonTag, stopAtActivity = false) {\n", 1)
    old = ("\t\tif (canonTag === \"alert\") family.add(\"end important\");\n")
    assert s.count(old) == 1
    new = old + ("\t\t// ROUND 390: a tag_promote SOURCE's closer counts for its promoted target — the writer who types\n"
                 "\t\t// [Supervisor Button] … [End Supervisor button] closes the promoted `supervisor note` span.\n"
                 "\t\tfor (const r of (DataService.Data.TagLexicon?._meta?.tag_promote?.rules ?? [])) {\n"
                 "\t\t\tif (r && r.to === canonTag && r.from) family.add(`end ${r.from}`);\n"
                 "\t\t}\n")
    s = s.replace(old, new, 1)
    old = ("\t\t\tif (p.directive === \"CONTAINER_OPEN\" && p.tag !== \"activity\") return false;\n")
    assert s.count(old) == 1
    s = s.replace(old, "\t\t\tif (p.directive === \"CONTAINER_OPEN\" && (stopAtActivity || p.tag !== \"activity\")) return false;   // ROUND 390: an own-row span never swallows an activity\n", 1)
    # (2) the rowOpen companion
    old = "\t\tlet rowOpen = false;\n"
    assert s.count(old) == 1
    s = s.replace(old, old + "\t\tlet ownSpanClose = null;   // ROUND 390: the close string of an OPEN own-row span (the supervisor panel a writer closes explicitly) — emit() opens no content row while it is set and pushes that close directly\n", 1)
    # (3) emit()
    old = ("\t\t\tconst content = html.filter(Boolean);\n"
           "\t\t\tif (!content.length) return;\n"
           "\t\t\tif (!rowOpen) {\n")
    assert s.count(old) == 1, s.count(old)
    new = ("\t\t\tconst content = html.filter(Boolean);\n"
           "\t\t\tif (!content.length) return;\n"
           "\t\t\tif (ownSpanClose !== null && content.length === 1 && content[0] === ownSpanClose) {   // ROUND 390: the own-row span's close — no content row around it\n"
           "\t\t\t\tparts.push(content[0]); ownSpanClose = null; rowOpen = false; return;\n"
           "\t\t\t}\n"
           "\t\t\tif (!rowOpen && ownSpanClose === null) {\n")
    s = s.replace(old, new, 1)
    # (4) autoClose: span-own = a writer's span
    old = "\t\t\t\tif (top.mode === \"span\" || top.mode === \"span-wrap\") {\n"
    assert s.count(old) == 1
    s = s.replace(old, "\t\t\t\tif (top.mode === \"span\" || top.mode === \"span-wrap\" || top.mode === \"span-own\") {   // ROUND 390: span-own = the explicitly closed supervisor panel\n", 1)
    # (5) the own_row branch
    old = ("\t\t\t\t\tif (defOwn?.own_row && !stack.length) {\n"
           "\t\t\t\t\t\tbreakRow();\n"
           "\t\t\t\t\t\theadingHold = false;\n"
           "\t\t\t\t\t\tconst boxParts = this.#calloutOpen(it, bodyItems, i, stack, run, false).filter(Boolean);\n")
    assert s.count(old) == 1, s.count(old)
    new = ("\t\t\t\t\tif (defOwn?.own_row && !stack.length) {\n"
           "\t\t\t\t\t\tbreakRow();\n"
           "\t\t\t\t\t\theadingHold = false;\n"
           "\t\t\t\t\t\t// ROUND 390 (the autonomous loop's session 26 Round 4): a writer who CLOSES the note explicitly —\n"
           "\t\t\t\t\t\t// [Supervisor Button] … [End Supervisor button] / [Supervisor note] … [end supervisor note] — means the\n"
           "\t\t\t\t\t\t// whole run to the closer is the panel's content (the gold's panel: Leaving to Learn 22 / 0). The\n"
           "\t\t\t\t\t\t// panel opens in SPAN mode (stack mode span-own): the loop renders the items between inside its\n"
           "\t\t\t\t\t\t// column, emit() opens no content row meanwhile, the closer pops it. Data\n"
           "\t\t\t\t\t\t// callouts.by_tag.<tag>.explicit_close_span; env SUPSPAN_OFF.\n"
           "\t\t\t\t\t\tconst _ecs = defOwn.explicit_close_span;\n"
           "\t\t\t\t\t\tif (_ecs && _ecs.enabled !== false\n"
           "\t\t\t\t\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[_ecs.env ?? \"SUPSPAN_OFF\"])\n"
           "\t\t\t\t\t\t\t&& this.#explicitCloseAhead(bodyItems, i, primary.tag, _ecs.stop_at_activity !== false)) {\n"
           "\t\t\t\t\t\t\tconst spanParts = this.#calloutOpen(it, bodyItems, i, stack, run, true).filter(Boolean);\n"
           "\t\t\t\t\t\t\tconst topE = stack[stack.length - 1];\n"
           "\t\t\t\t\t\t\tif (topE && topE.tag === primary.tag) { topE.mode = \"span-own\"; ownSpanClose = topE.close; }\n"
           "\t\t\t\t\t\t\tparts.push(...spanParts);\n"
           "\t\t\t\t\t\t\trun.AddNote(\"info\", \"ContentConverter\",\n"
           "\t\t\t\t\t\t\t\t`Page ${page.lessonLabel}: [${primary.tag}] spans to its explicit closer — the panel holds everything between (round 390).`);\n"
           "\t\t\t\t\t\t\twhile (bodyItems[i + 1]?._consumed) i++;\n"
           "\t\t\t\t\t\t\tbreak;\n"
           "\t\t\t\t\t\t}\n"
           "\t\t\t\t\t\tconst boxParts = this.#calloutOpen(it, bodyItems, i, stack, run, false).filter(Boolean);\n")
    s = s.replace(old, new, 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: explicit-close span for own_row callouts")
else:
    print("engine: already")
