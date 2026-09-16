#!/usr/bin/env python3
"""ROUND 349 (loop session 13 Round 2 — Chris's D10-9: KB constraint 23 / 01B lesson-menu labels everywhere) — the splice.

(1) data/Emit_Templates.json: `menu.lesson_label_form` {enabled, env MENULABEL_OFF, level, role_lexicon, title_lexicon,
    label_max_words, drop_titles, overview_labels, colon_form, learning_to_normalise, learning_label, item_prefix, year_table}
    — inserted TEXTUALLY as the LAST key of `menu` (the `menu` → `footer` seam) (tab-indented, never json.dumps — CLAUDE.md §16).
(2) app/js/ContentConverter.js: `#menuLabelForm(html, isOverview)` — a post-pass on every menu pane string, run right after the
    lesson-repeats-overview block; the method is added before `#promoteNamedHeadings`'s doc comment.
Idempotent. LF kept. §6 atomic writes: encode first, temp file, `node --check` / a duplicate-key JSON load, then os.replace."""
import io, os, json, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.normpath(os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2"))
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def atomic(p, s, check):
    b = s.encode("utf-8"); assert len(b) > 10000, "refusing a near-empty write"
    tmp = p[:-len(os.path.splitext(p)[1])] + ".r349tmp" + os.path.splitext(p)[1]
    with open(tmp, "wb") as f: f.write(b)
    ok, msg = check(tmp)
    if not ok: os.remove(tmp); sys.exit(f"CHECK FAILED for {p}: {msg}")
    os.replace(tmp, p)
def js_ok(tmp):
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True); return r.returncode == 0, r.stderr
def json_ok(tmp):
    def nodup(pairs):
        d = {}
        for k, v in pairs:
            if k in d: raise ValueError(f"duplicate key {k}")
            d[k] = v
        return d
    try: json.loads(rd(tmp), object_pairs_hook=nodup); return True, ""
    except Exception as e: return False, str(e)

# ------------------------------------------------------------------ (1) Emit_Templates.json
P = os.path.join(PF, "data", "Emit_Templates.json"); s = rd(P)
if '"lesson_label_form"' not in s:
    A = '\t\t}\n\t},\n\t"footer": {'
    assert s.count(A) == 1, "data anchor"
    BLOCK = '''\t\t},
\t\t"lesson_label_form": {
\t\t\t"enabled": true,
\t\t\t"env": "MENULABEL_OFF",
\t\t\t"overrides_gold": true,
\t\t\t"note": "ROUND 349 (Chris's decision D10-9, 2026-09-16 — KB constraint 23 (Universal) + 01B 'Lesson Pages — Simplified Module Menu' lines 221–246 + the overview-tab label row 196–197; KB level 1 over the gold's per-series split, a NAMED override). Inside #module-menu-content on EVERY page: (a) every learning / success LABEL — a p / h3 / h4 / h6 whose folded text starts with a role lead-in (role_lexicon), is at most label_max_words long, and either ends with a colon / ellipsis or is followed by a list — ships as <h{level}> (the r117 exact-phrase list + its 'secondary lead-in stays <p>' discriminator are superseded for menus; the r81 / r142 eng- and banner-family skip_named_promotion no longer keeps a label <p>); (b) the label's FORM is the KB's: trailing '...' / '…' / nothing → ':' (the gold: 'We are learning to:' 160 vs '...' 18; 'You will show your understanding by:' 220 vs the ellipsis forms 23); (c) learning_to_normalise — the writer's 'We are learning to:' / 'We are learning about/to …' family becomes the KB's learning_label 'We are learning:' and, so constraint 24's 'verb form matching heading context' still holds, each item of the list that follows gains item_prefix 'to ' (unless it already starts with it) with its first letter lowercased — exactly what the gold does where it re-words (30 of 39 checked pages: CEDO502, ENGC401 …); 'We are learning about:' is KEPT (its items would need a verb rewrite — editorial); (d) drop_titles — on a LESSON page a section TITLE (title_lexicon: 'Learning intentions', 'How will I know if I've learned it?', 'Success criteria' …) that sits IMMEDIATELY ABOVE a label is dropped (01B line 223: the h5 IS the label; 117 such titles on 116 pages); a title that is the label of its own list (followed by <ul>) or a two-column banner (followed by a curriculum heading) is KEPT; on the OVERVIEW page every title stays (01B's <h4><span> overview titles); (e) overview_labels — the overview tab's 'We are learning:' / 'I can:' labels are <h5> too (01B 196–197 / constraint 67) — the r81 two_col eng-family overview <p> form is retired (a NAMED override on the ~480 overview labels whose gold keeps <p>); (f) a SENTENCE (a role lead-in longer than label_max_words, or with no colon / ellipsis and no list after it — the constraint-70 OSSC 'Ākonga will learn …' lead-in, 'You will be able to …') is never a label and stays <p>; (g) the SUCCESS label's wording is the writer's (colon form only): 01B's year table ('I can:' years 7–10 / 'You will show your understanding by:' years 1–6) needs a year the data does not hold (session-12 pre-measurement: the code's level digit is not a year; the gold is per-MODULE consistent) — year_table {CODE: '7-10' | '1-6'} is the hook, empty until a data / KB session fills it. Menu is #header-scoped → invisible to compare_structure / body_compare; the p→h5 node change and the dropped titles are skeleton-visible (expected ≈ −0.1pp, named). Verifier: reference/tests/_verify_menulabels.cjs (protected, defect 0). Env MENULABEL_OFF reverts the whole pass.",
\t\t\t"level": 5,
\t\t\t"role_lexicon": {
\t\t\t\t"learning": "^(we are learning|we're learning|we learning|what are we learning|learning intentions?|ākonga will|akonga will|ākonga can|akonga can|students will|i am learning to|walt|what am i learning|what will i learn)\\\\b",
\t\t\t\t"success": "^(i can|you will (?:show|demonstrate) your understanding|success criteria|how will i know|wilf|you will be able to)\\\\b"
\t\t\t},
\t\t\t"title_lexicon": ["learning intentions", "learning intention", "success criteria", "how will i know if i've learned it", "how will i know i have learned it", "how will i know", "what are we learning", "what are we learning today", "lesson objectives", "lesson objective", "lesson goals", "lesson goal", "ngā whāinga ako", "nga whainga ako", "whāinga ako", "whainga ako", "paearu angitu"],
\t\t\t"label_max_words": 8,
\t\t\t"drop_titles": true,
\t\t\t"overview_labels": true,
\t\t\t"colon_form": true,
\t\t\t"learning_to_normalise": true,
\t\t\t"learning_to_pattern": "^we are learning (?:about )?to$",
\t\t\t"learning_label": "We are learning:",
\t\t\t"item_prefix": "to ",
\t\t\t"year_table": {},
\t\t\t"_year_table_note": "01B lines 240–244: the SUCCESS label is 'I can:' for years 7–10 and 'You will show your understanding by:' for years 1–6. Fill {CODE: '7-10'} / {CODE: '1-6'} per module (the gold is per-module consistent — 6 of ~130 modules mix); an entry re-words that module's success label; no entry = the writer's own label, colon form."
\t\t}
\t},
\t"footer": {'''
    s = s.replace(A, BLOCK, 1)
    atomic(P, s, json_ok); print("Emit_Templates.json: menu.lesson_label_form added")
else: print("Emit_Templates.json already has lesson_label_form")

# ------------------------------------------------------------------ (2) ContentConverter.js
P = os.path.join(PF, "app", "js", "ContentConverter.js"); s = rd(P)
if "#menuLabelForm(" not in s:
    # (2a) the call site — after the lesson-repeats-overview block, before the precedence cascade
    A = ('\t\t// THE 6-LEVEL PRECEDENCE CASCADE — live engine application. This lets a module\'s\n')
    assert s.count(A) == 1, "call-site anchor"
    CALL = ('\t\t// ROUND 349 (Chris\'s D10-9 — KB constraint 23 / 01B): every learning / success LABEL in the module menu is an\n'
            '\t\t// <h5> in the KB\'s form, a section title directly above a label is dropped on a lesson page, the overview tab\'s\n'
            '\t\t// labels are <h5> too, and the writer\'s "We are learning to:" family becomes "We are learning:" with its items in\n'
            '\t\t// "to …" form (constraint 24). Runs AFTER the lesson-repeat copy above so a repeated overview menu gets the\n'
            '\t\t// lesson treatment on a lesson page. Data flag: menu.lesson_label_form. Env toggle: MENULABEL_OFF.\n'
            '\t\tfor (const k of ["tab1", "tab2", "content", "left", "right", "wtPanes", "reoPanes"]) {\n'
            '\t\t\tif (typeof menu[k] === "string" && menu[k]) menu[k] = this.#menuLabelForm(menu[k], !!page.isOverview);\n'
            '\t\t}\n'
            '\t\t// the two-column / fundamentals / tabbed-overview panes are ARRAYS of { cls, html } columns\n'
            '\t\tfor (const k of ["tab1Cols", "tab2Cols", "funLiCols", "cols"]) {\n'
            '\t\t\tif (Array.isArray(menu[k])) for (const c of menu[k]) if (c && typeof c.html === "string" && c.html) c.html = this.#menuLabelForm(c.html, !!page.isOverview);\n'
            '\t\t}\n\n')
    s = s.replace(A, CALL + A, 1)
    # (2b) the method — before #promoteNamedHeadings's doc comment
    B = ('\t/**\n\t * NAMED LEARNING-DESIGN HEADING promotion — a post-pass run on the assembled body\n')
    assert s.count(B) == 1, "method anchor"
    METHOD = r'''	/**
	 * ROUND 349 — THE LESSON-MENU LABEL FORM (Chris's decision D10-9, 2026-09-16; KB constraint 23 (Universal) +
	 * 01B "Lesson Pages — Simplified Module Menu" + the overview-tab label row). A post-pass on ONE menu pane's HTML
	 * string (MenuBuilder.buildMenu returns an object of pane strings). Inside the pane:
	 *   - a LABEL = a <p> / <h3> / <h4> / <h6> (not inside a widget subtree) whose folded text starts with a learning or
	 *     success lead-in (data role_lexicon), is at most label_max_words long, and either ends with a colon / an ellipsis
	 *     or is followed by a list → <h{level}> in the KB's form (trailing "..." / "…" / nothing → ":");
	 *   - the writer's "We are learning to:" family (learning_to_pattern, tested on the FOLDED text where "about/to" reads "about to" — "to:", "to...", "about/to …") → learning_label
	 *     "We are learning:" AND each <li> of the list that follows gains item_prefix "to " (unless it already starts with it)
	 *     with its first letter lowercased, so constraint 24's "verb form matching heading context" still holds — the gold's
	 *     own mechanical re-wording (CEDO502 / ENGC401 …); "We are learning about:" is kept (a verb rewrite would be editorial);
	 *   - on a LESSON page a section TITLE (title_lexicon — "Learning intentions", "How will I know…", "Success criteria")
	 *     that sits IMMEDIATELY ABOVE a label is dropped (01B 223 — the h5 IS the label). A title followed by its own list
	 *     is that list's label (kept); a two-column banner followed by a curriculum heading is kept; on the OVERVIEW page
	 *     every title stays (01B's <h4><span> overview titles);
	 *   - the OVERVIEW tab's "We are learning:" / "I can:" labels are <h5> too (01B 196–197) — the r81 / r142 eng- and
	 *     banner-family <p> form is retired for the labels only;
	 *   - a SENTENCE (a lead-in longer than label_max_words, or with no colon / ellipsis and no list after it — the
	 *     constraint-70 OSSC "Ākonga will learn …" lead-in, "You will be able to …") is never a label and stays <p>;
	 *   - the SUCCESS label keeps the writer's wording (colon form only) unless year_table names the module's year band
	 *     (01B 240–244: "I can:" years 7–10 / "You will show your understanding by:" years 1–6) — the data does not hold a
	 *     year today, so the table ships empty (the hook a data / KB session fills).
	 * The menu is #header-scoped (invisible to compare_structure / body_compare); the node changes are skeleton-visible and
	 * NAMED (KB over gold). Verifier: reference/tests/_verify_menulabels.cjs (protected).
	 * Data flag: menu.lesson_label_form   Env toggle: MENULABEL_OFF
	 */
	static #menuLabelForm(html, isOverview = false) {
		const cfg = DataService.Data.EmitTemplates.menu?.lesson_label_form;
		if (!cfg || cfg.enabled === false || !html) return html;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "MENULABEL_OFF"]) return html;
		const level = cfg.level ?? 5;
		const maxWords = cfg.label_max_words ?? 8;
		const learn = new RegExp(cfg.role_lexicon?.learning ?? "^(we are learning|learning intentions?|i am learning to)\\b", "i");
		const succ = new RegExp(cfg.role_lexicon?.success ?? "^(i can|you will show your understanding|success criteria|how will i know)\\b", "i");
		const toPat = new RegExp(cfg.learning_to_pattern ?? "^we are learning (?:about )?to$", "i");
		const titles = new Set((cfg.title_lexicon ?? []).map((t) => String(t).toLowerCase()));
		const fold = (t) => t.replace(/<[^>]+>/g, " ").replace(/&nbsp;/gi, " ").replace(/&[a-z]+;/gi, " ")
			.toLowerCase().replace(/[‘’`´]/g, "'").replace(/[^a-z0-9'āēīōū ]+/gi, " ").replace(/\s+/g, " ").trim();
		const text = (inner) => inner.replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();   // the label's own words, tags dropped
		const skip = new Set(DataService.Data.EmitTemplates.body_region?.heading_relevel?.skip_classes ?? []);
		const widget = this.#widgetRanges(html, skip);
		const inWidget = (pos) => widget.some(([a, b]) => pos >= a && pos < b);
		// tokenise the pane: heading / paragraph blocks and (flat) lists, in document order
		const els = [];
		const re = /<(p|h[1-6])\b([^>]*)>([\s\S]*?)<\/\1>|<(ul|ol)\b[^>]*>[\s\S]*?<\/\4>/gi;
		let m;
		while ((m = re.exec(html)) !== null) {
			if (m[4]) { els.push({ kind: "list", start: m.index, end: m.index + m[0].length, raw: m[0] }); continue; }
			const inner = m[3], attrs = m[2] || "", f = fold(inner), words = f ? f.split(" ").length : 0;
			const role = succ.test(f) ? "success" : (learn.test(f) ? "learning" : null);
			const tail = text(inner);
			const punct = /:\s*$/.test(tail) ? "colon" : (/(\.\.\.|…)\s*$/.test(tail) ? "ellipsis" : "");
			els.push({ kind: "blk", tag: m[1].toLowerCase(), attrs, start: m.index, end: m.index + m[0].length, raw: m[0], inner, f, words, role, punct,
				title: titles.has(f) || titles.has(f.replace(/\s*:$/, "")), inWidget: inWidget(m.index) });
		}
		const isLabel = (e, i) => {
			if (!e || e.kind !== "blk" || e.inWidget || !e.role || e.title) return false;
			if (e.words > maxWords) return false;   // a sentence (the c70 lead-in) is never a label
			const nxt = els[i + 1];
			return e.punct !== "" || (nxt && nxt.kind === "list");
		};
		const out = []; let pos = 0, prefixNext = null;
		for (let i = 0; i < els.length; i++) {
			const e = els[i];
			out.push(html.slice(pos, e.start)); pos = e.end;
			if (e.kind === "list") {
				if (prefixNext) {
					// constraint 24: the items of a normalised "We are learning:" list read "to …", first letter lowercased
					const pre = prefixNext; prefixNext = null;
					out.push(e.raw.replace(/(<li\b[^>]*>)((?:\s*<[^>]+>)*\s*)([\s\S]*?)(<\/li>)/gi, (all, open, lead, body, close) => {
						if (new RegExp("^\\s*" + pre.trim() + "\\b", "i").test(body.replace(/<[^>]+>/g, ""))) return all;
						const fixed = body.replace(/^(\s*)(\S)/, (mm, sp, ch) => sp + pre + ch.toLowerCase());
						return open + lead + fixed + close;
					}));
				} else out.push(e.raw);
				continue;
			}
			// (d) a lesson-page section title directly above a label is dropped (01B 223)
			if (e.title && !isOverview && cfg.drop_titles !== false && !e.inWidget && isLabel(els[i + 1], i + 1)) {
				// swallow the whitespace that separated the title from the label
				const after = html.slice(e.end, els[i + 1].start);
				if (/^\s*$/.test(after)) { pos = els[i + 1].start; }
				continue;
			}
			if (!isLabel(e, i) || (isOverview && cfg.overview_labels === false)) { out.push(e.raw); continue; }
			// (a) + (b) + (c): the label in the KB's form
			let label = text(e.inner).replace(/\s*(\.\.\.|…|\.|:)+\s*$/g, "").trim();
			const core = fold(label);
			if (cfg.learning_to_normalise !== false && e.role === "learning" && toPat.test(core)) {
				label = String(cfg.learning_label ?? "We are learning:").replace(/:$/, ""); prefixNext = String(cfg.item_prefix ?? "to ");
			}
			if (cfg.colon_form !== false) label += ":";
			out.push(`<h${level}${e.attrs}>${label}</h${level}>`);   // the element's own attributes are kept (the MTK menus' <h5 eng> / <h5 reo>)
		}
		out.push(html.slice(pos));
		return out.join("");
	};

'''
    s = s.replace(B, METHOD + B, 1)
    atomic(P, s, js_ok); print("ContentConverter.js: #menuLabelForm + call site added")
else: print("ContentConverter.js already spliced")
