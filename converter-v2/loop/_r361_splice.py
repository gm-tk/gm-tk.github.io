#!/usr/bin/env python3
"""ROUND 361 (loop session 19, Round 5 — the EXPlore "Navigation with N sections" inquiry dialect) — the anchored splice:
data body_region.inquiry_tabs.section_nav (Emit_Templates.json, tabs), PanelsBuilder.detectInquirySections + the
sectionMode branch of inquiryPanels, ContentConverter detection / body-loop split / call site. Idempotent; LF preserved."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
APP = os.path.join(ROOT, "pageforge-site", "converter-v2", "app", "js"); DATA = os.path.join(ROOT, "pageforge-site", "converter-v2", "data")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
def splice(path, anchor, new, before=False, marker=None):
    s = rd(path)
    if (marker or new) in s: print(f"{os.path.basename(path)}: already"); return
    assert s.count(anchor) == 1, (path, anchor[:60], s.count(anchor))
    s = s.replace(anchor, (new + anchor) if before else (anchor + new), 1); wr(path, s); print(f"{os.path.basename(path)}: spliced")

# ---- data
T = "\t"
DOC = ("ROUND 361 (the autonomous loop's session 19, Round 5 — the DIFF MINER's crumbs fact F23; KB 06 §3.4). THE EXPlore "
       "\\\"NAVIGATION WITH N SECTIONS\\\" INQUIRY DIALECT (EXPFUN02–05, the only WTs carrying the phrase). The writer declares the crumb "
       "trail in ONE instruction — `[Side Navigation with 6 sections: Learner, Communicator, Scientist, Social Scientist, Mathematician "
       "and Innovator]` or `[Tab Navigation with …]` — and opens each section with `[section N] Label` (EXPFUN02), a `TAB NAV N: Label` "
       "line (03 / 04 / 05; the first, `TAB NAV: Intro` / `TAB NAV 1: Introduction`, opens the intro panel) or a top-level [H1] / [H2] "
       "heading naming the label (EXPFUN02's last four: 'Think like a scientist' …). PanelsBuilder.detectInquirySections finds the "
       "instruction, parses the labels (split on commas / 'and'), matches every label IN ORDER to the next opener after it and fires only "
       "when all are found; the instruction and the tag / line openers are consumed, a heading opener stays as the panel's first heading; "
       "with no explicit intro opener the instruction itself opens the intro panel. inquiryPanels sectionMode: the content BEFORE the "
       "first sentinel stays outside the scaffold (the overview's learning-intention rows), then N+1 unified crumbs (intro_label + the "
       "list, the first showing) and N+1 inquiryPanels (the first showing) via the page_split templates. Guards: single-file pages, never "
       "alongside the BLL / heading-label / CED modes. Measured: the gold builds 7 crumbs + 7 panels on all four; Claude shipped a flat "
       "body at 7–9 % SCAFFOLD. Env SECTIONNAV_OFF = byte-identical.")
DATA_BLOCK = (
    f'{T*3}"section_nav": {{\n'
    f'{T*4}"_doc": "{DOC}",\n'
    f'{T*4}"enabled": true,\n'
    f'{T*4}"env": "SECTIONNAV_OFF",\n'
    f'{T*4}"intro_label": "Intro",\n'
    f'{T*4}"intro_words": [\n{T*5}"intro",\n{T*5}"introduction"\n{T*4}],\n'
    f'{T*4}"min_sections": 3,\n'
    f'{T*4}"heading_openers": [\n{T*5}"h1",\n{T*5}"h2"\n{T*4}]\n'
    f'{T*3}}},\n')
P = os.path.join(DATA, "Emit_Templates.json")
splice(P, f'{T*3}"recover_consumed_openers": true,\n', DATA_BLOCK, marker='"section_nav": {')
d = json.loads(rd(P)); assert d["body_region"]["inquiry_tabs"]["section_nav"]["env"] == "SECTIONNAV_OFF"

# ---- PanelsBuilder: signature + early return + sectionMode branch + detector
P = os.path.join(APP, "PanelsBuilder.js"); s = rd(P)
if "detectInquirySections" not in s:
    old_sig = "\tstatic inquiryPanels(body, { on, sentinel, labels, cedMode, cedLabels, headingLabel } = {}) {"
    assert s.count(old_sig) == 1
    s = s.replace(old_sig, "\tstatic inquiryPanels(body, { on, sentinel, labels, cedMode, cedLabels, headingLabel, sectionMode, sectionLabels } = {}) {", 1)
    old_ret = '\t\tif (!(on || cedMode) || !cfg || cfg.enabled === false || !body.includes(sent)) return body.split(sent).join("");'
    assert s.count(old_ret) == 1
    s = s.replace(old_ret, '\t\tif (!(on || cedMode || sectionMode) || !cfg || cfg.enabled === false || !body.includes(sent)) return body.split(sent).join("");', 1)
    old_segs = '\t\tconst panelSegs = segs.slice(1).map((s) => s.trim());\n'
    assert s.count(old_segs) == 1
    BRANCH = '''\t\t// ROUND 361 — SECTION-NAV mode (the EXPlore "Navigation with N sections" dialect; see
\t\t// PanelsBuilder.detectInquirySections): segment 0 — everything BEFORE the first sentinel (the
\t\t// overview's learning-intention rows) — stays OUTSIDE the scaffold; then N+1 UNIFIED crumbs
\t\t// (intro_label + the instruction's labels, the first `showing`) and N+1 panels (the first
\t\t// `showing`), built with the page_split templates. The detector fires only when every label
\t\t// found an opener, so the label and panel counts agree; a stray extra panel gets an empty crumb.
\t\t// Data: inquiry_tabs.section_nav   Env toggle: SECTIONNAV_OFF (the detector never fires)
\t\tif (sectionMode) {
\t\t\tconst ps = cfg.page_split || {};
\t\t\tconst labs = sectionLabels || [];
\t\t\tconst n = panelSegs.length;
\t\t\tif (!n) return body.split(sent).join("");
\t\t\tconst crumbs = [cfg.crumbs_open];
\t\t\tfor (let i = 0; i < n; i++)
\t\t\t\tcrumbs.push(Utils.FillTemplate(ps.crumb_item || cfg.crumb_item, {
\t\t\t\t\tn: String(i + 1), label: labs[i] || "", showing: i === 0 ? " class=\\"showing\\"" : "" }));
\t\t\tcrumbs.push(cfg.crumbs_close);
\t\t\tconst panels = [];
\t\t\tfor (let i = 0; i < n; i++)
\t\t\t\tpanels.push(Utils.FillTemplate(ps.panel_open || cfg.panel_open, { n: String(i + 1), showing: i === 0 ? " showing" : "" }) + "\\n" + panelSegs[i] + "\\n" + cfg.panel_close);
\t\t\treturn (intro ? intro + "\\n" : "") + crumbs.join("\\n") + "\\n" + panels.join("\\n");
\t\t}
'''
    s = s.replace(old_segs, old_segs + BRANCH, 1)
    old_end = "\t\treturn { on: true, labels, suppressBundles };\n\t};\n}\n"
    assert s.count(old_end) == 1
    DETECT = '''\t\treturn { on: true, labels, suppressBundles };
\t};

\t/**
\t * ROUND 361 (the autonomous loop's session 19, Round 5 — the DIFF MINER's crumbs fact F23; KB 06 §3.4).
\t * THE EXPlore "NAVIGATION WITH N SECTIONS" INQUIRY DIALECT (EXPFUN02–05). The writer declares the whole
\t * crumb trail in ONE instruction — `[Side Navigation with 6 sections: Learner, Communicator, Scientist,
\t * Social Scientist, Mathematician and Innovator]` (or `[Tab Navigation with …]`) — and then opens each
\t * section with `[section N] Label` (a `shape n` SUBTAG once normalised, the label in blackAfter), with a
\t * `TAB NAV N: Label` line (a red instruction run or a plain black run; the first one — `TAB NAV: Intro`,
\t * `TAB NAV 1: Introduction` — opens the INTRO panel) or, on EXPFUN02, simply with a top-level [H1] / [H2]
\t * heading that names the label ("Think like a scientist"). The human builds N+1 unified crumbs («Intro» +
\t * the list, the first `showing`) and N+1 `div.inquiryPanel`s (the first `showing`) inside div#body.
\t *
\t * Scans the WHOLE item stream: finds the instruction, parses the labels (split on commas and "and"), then
\t * walks the items after it matching each expected label IN ORDER to the next opener; fires only when every
\t * label found one (a conservative all-or-nothing test — no partial scaffold). Flags for the body loop in
\t * ContentConverter: `_inqSection` = the panel ordinal (0 = intro) on every opener (a sentinel is pushed
\t * there), `_inqSectionConsume` on the instruction and on the tag / line openers (they render nothing); a
\t * heading opener keeps rendering as the panel's first heading. With no explicit intro opener before the
\t * first section opener, the instruction item itself opens the intro panel. Returns the crumb labels
\t * (intro_label first) for inquiryPanels' sectionMode.
\t *
\t * Data: body_region.inquiry_tabs.section_nav   Env toggle: SECTIONNAV_OFF
\t */
\tstatic detectInquirySections(page, tpl) {
\t\tconst off = { on: false, labels: [] };
\t\tconst cfg = tpl?.body_region?.inquiry_tabs?.section_nav;
\t\tif (!cfg || cfg.enabled === false) return off;
\t\tif (typeof process !== "undefined" && process.env && process.env[cfg.env || "SECTIONNAV_OFF"]) return off;
\t\tconst items = page.items || [];
\t\tconst txt = (it) => `${it.text || ""} ${it.blackAfter || ""}`.replace(/\\*/g, "").replace(/\\s+/g, " ").trim();
\t\tconst norm = (s) => String(s || "").toLowerCase().replace(/[^a-z0-9āēīōū]+/g, " ").trim();
\t\tconst RX_INSTR = /\\b(?:side|tab)\\s*navigation\\s*with\\s*(\\d+)\\s*sections?\\s*:\\s*([^\\]]+)/i;
\t\tlet instrIx = -1, labels = [];
\t\tfor (let i = 0; i < items.length; i++) {
\t\t\tconst it = items[i];
\t\t\tif (it.type !== "tag" && it.type !== "black") continue;
\t\t\tconst m = RX_INSTR.exec(txt(it));
\t\t\tif (!m) continue;
\t\t\tlabels = m[2].split(/\\s*,\\s*|\\s+and\\s+/i).map((x) => x.replace(/[\\].\\s]+$/g, "").trim()).filter(Boolean);
\t\t\tinstrIx = i;
\t\t\tbreak;
\t\t}
\t\tif (instrIx < 0 || labels.length < (cfg.min_sections ?? 3)) return off;
\t\tconst introWords = new Set((cfg.intro_words || ["intro", "introduction"]).map(norm));
\t\tconst hTags = new Set((cfg.heading_openers || ["h1", "h2"]).map((t) => String(t).toLowerCase()));
\t\tconst RX_SECTION = /^\\s*\\[\\s*section\\s*\\d*\\s*\\]/i;
\t\tconst RX_TABNAV = /^\\s*(?:\\u2705\\s*)?tab\\s*nav\\s*(\\d*)\\s*:\\s*(.*)$/i;
\t\tconst openers = [];   // { it, k, consume }
\t\tlet next = 0, introIx = -1;
\t\tfor (let i = instrIx + 1; i < items.length && next < labels.length; i++) {
\t\t\tconst it = items[i];
\t\t\tif (it.type !== "tag" && it.type !== "black") continue;
\t\t\tif (it.consumedBy !== undefined) continue;
\t\t\tconst t = txt(it);
\t\t\tif (it.type === "tag" && RX_SECTION.test(String(it.text || ""))) {
\t\t\t\topeners.push({ it, k: next + 1, consume: true }); next++; continue;
\t\t\t}
\t\t\tconst m = RX_TABNAV.exec(t);
\t\t\tif (m) {
\t\t\t\tif (!openers.length && introWords.has(norm(m[2]))) { introIx = i; openers.push({ it, k: 0, consume: true }); continue; }
\t\t\t\topeners.push({ it, k: next + 1, consume: true }); next++; continue;
\t\t\t}
\t\t\tconst ptag = String(it.parse?.primary?.tag || "").toLowerCase();
\t\t\tconst want = norm(labels[next]);
\t\t\tif (it.type === "tag" && hTags.has(ptag) && want && norm(t).includes(want)) {
\t\t\t\topeners.push({ it, k: next + 1, consume: false }); next++; continue;
\t\t\t}
\t\t}
\t\tif (next < labels.length) return off;
\t\tconst instr = items[instrIx];
\t\tinstr._inqSectionInstr = true;
\t\tinstr._inqSectionConsume = true;
\t\tif (introIx < 0) instr._inqSection = 0;   // no explicit intro opener: the instruction opens the intro panel
\t\tfor (const o of openers) {
\t\t\to.it._inqSection = o.k;
\t\t\tif (o.consume) o.it._inqSectionConsume = true;
\t\t}
\t\treturn { on: true, labels: [cfg.intro_label || "Intro", ...labels] };
\t};
}
'''
    s = s.replace(old_end, DETECT, 1)
    wr(P, s); print("PanelsBuilder.js: spliced")
else:
    print("PanelsBuilder.js: already")

# ---- ContentConverter: detection, body-loop split, call site
P = os.path.join(APP, "ContentConverter.js"); s = rd(P)
if "secInquiryMode" not in s:
    a1 = "\t\tconst cedInq = PanelsBuilder.detectInquiryCed(page, tpl);\n\t\tconst cedInquiryMode = cedInq.on;\n"
    assert s.count(a1) == 1
    s = s.replace(a1, a1 + '''\t\t// ROUND 361 — the EXPlore "Navigation with N sections" inquiry dialect (EXPFUN02–05):
\t\t// PanelsBuilder.detectInquirySections flags the instruction and its section openers; the body
\t\t// loop below pushes a panel sentinel at each flagged opener (and renders the consumed ones as
\t\t// nothing), and inquiryPanels' sectionMode wraps the result. Single-file pages only (the r112
\t\t// scope) and never alongside the BLL / heading-label / CED modes above — each of those needs
\t\t// its own opener grammar, which this dialect does not carry.
\t\t// Data flag: inquiry_tabs.section_nav   Env toggle: SECTIONNAV_OFF
\t\tconst secInq = (!inquiryMode && !cedInquiryMode && _singleFile)
\t\t\t? PanelsBuilder.detectInquirySections(page, tpl) : { on: false, labels: [] };
\t\tconst secInquiryMode = secInq.on;
''', 1)
    a2 = "\t\t\tif (it._inquiryCrumb) continue;\n"
    assert s.count(a2) == 1
    s = s.replace(a2, a2 + '''
\t\t\t// ROUND 361 — the EXPlore "Navigation with N sections" dialect (PanelsBuilder.detectInquirySections):
\t\t\t// a flagged section opener closes any still-open activity, breaks the row and pushes the panel
\t\t\t// sentinel (the r102 `[page N]` split, verbatim); a CONSUMED opener — the instruction, a
\t\t\t// `[section N]` tag, a `TAB NAV N:` line — then renders nothing, while a heading opener falls
\t\t\t// through and renders as its panel's first heading.
\t\t\t// Env toggle: SECTIONNAV_OFF (the detector never flags, so nothing here can fire)
\t\t\tif (secInquiryMode && (it._inqSection !== undefined || it._inqSectionConsume)) {
\t\t\t\tif (it._inqSection !== undefined) {
\t\t\t\t\twhile (stack.length && stack[stack.length - 1].tag === "activity") {
\t\t\t\t\t\temit(stack.pop().close);
\t\t\t\t\t\tif (!stack.length) breakRow();
\t\t\t\t\t}
\t\t\t\t\tif (!stack.length) {
\t\t\t\t\t\tbreakRow();
\t\t\t\t\t\tparts.push(INQ_SENTINEL);
\t\t\t\t\t\tpageLabelHold = "";
\t\t\t\t\t\theadingHold = false;
\t\t\t\t\t}
\t\t\t\t}
\t\t\t\tif (it._inqSectionConsume) continue;
\t\t\t}
''', 1)
    a3 = "\t\t\t\tcedMode: cedInquiryMode, cedLabels: cedInq.labels, headingLabel: _headingLabelOn });\n\t\tconst inquiryActive = (inquiryMode || cedInquiryMode) && finalBody !== bodyHtml;\n"
    assert s.count(a3) == 1
    s = s.replace(a3, "\t\t\t\tcedMode: cedInquiryMode, cedLabels: cedInq.labels, headingLabel: _headingLabelOn,\n\t\t\t\tsectionMode: secInquiryMode, sectionLabels: secInq.labels });\n\t\tconst inquiryActive = (inquiryMode || cedInquiryMode || secInquiryMode) && finalBody !== bodyHtml;\n", 1)
    wr(P, s); print("ContentConverter.js: spliced")
else:
    print("ContentConverter.js: already")
print("splice done")
