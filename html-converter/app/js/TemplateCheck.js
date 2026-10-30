/**
 * TemplateCheck.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Builds the Template check: a short, grouped list of plain-English
 * questions about the things PageForge was unsure of while converting one
 * Writers Template. It reads only what the finished conversion already
 * produced —
 *   - the run notes (run.notes — the batch converter saves the same list in
 *     each module's _run.json),
 *   - the notes printed in the pages (class "cv2-note": Red Flag / Writers
 *     Note / Designer/Developer To Do), and
 *   - the un-built interactive boxes (class "cv2-interactive cv2-int-ref")
 *     plus the interactives worklist ({CODE}_interactives.txt)
 * — and never changes a note, a page or run.outputs. It also builds and
 * reads the answers file ({CODE}_template-answers.json).
 *
 * WHY SEPARATE FILE:
 * Every question — which notes it matches, how matches are grouped, its
 * wording with {blanks}, its answer choices — lives in
 * data/Template_Check_Questions.json. This file only matches, fills in
 * blanks and orders, with pure functions and no page code (no DOM), so the
 * browser app and node tools run the same check.
 *
 * DATA FLAG + ENV TOGGLE:
 * Template_Check_Questions.json "enabled" and env TEMPLATECHECK_OFF. With
 * either one off, Classify() returns null and nothing is shown or added.
 *
 * THE ANSWER FUNCTIONS TRAVEL:
 * The stand-alone check page carries this class's source, so the answer
 * functions it calls (AnswerUnits, Counts, BuildAnswers, ReadAnswers) use
 * nothing outside this class. The classifier itself runs only in the app
 * and in node, where Utils is loaded.
 * ===========================================================================
 */

class TemplateCheck {

	// compiled regexes per catalogue object (the catalogue never changes in a run)
	static #compiled = new WeakMap();
	// the plural blank names ({s}, {rows_s} …): an empty value is a real value for these
	static #pluralKeys = new Set();

	/**
	 * Is the check switched on? The data flag and the env toggle both apply.
	 *
	 * @param {Object} cat - the Template_Check_Questions.json object
	 * @returns {boolean}
	 */
	static Enabled(cat) {
		if (!cat || cat.enabled === false) return false;
		const env = (typeof process !== "undefined" && process.env) ? process.env : {};
		return !env[cat.env ?? "TEMPLATECHECK_OFF"];
	};

	/**
	 * Runs the check on a finished browser run.
	 *
	 * @param {ConversionRun} run - the completed run (read only)
	 * @param {Object} data - the loaded data files (DataService.Data)
	 * @returns {Object|null} the check, or null when switched off
	 */
	static FromRun(run, data) {
		const outputs = run.outputs ?? [];
		return this.Classify({
			moduleCode: run.moduleCode,
			notes: run.notes ?? [],
			pages: this.PagesFromOutputs(outputs),
			worklist: outputs.find((o) => o.kind === "manifest")?.content ?? null,
			data,
		});
	};

	/**
	 * The page files among a run's outputs, as plain { filename, content }.
	 *
	 * @param {Object[]} outputs - run.outputs
	 * @returns {Object[]}
	 */
	static PagesFromOutputs(outputs) {
		return (outputs ?? [])
			.filter((o) => o.kind === "page" && typeof o.content === "string")
			.map((o) => ({ filename: o.filename, content: o.content }));
	};

	/**
	 * THE CLASSIFIER. Matches every run note, page note and hand-off box
	 * against the catalogue (the first entry that matches claims it), groups
	 * the matches, fills in each question's wording and orders the result.
	 *
	 * @param {Object} input
	 * @param {string} input.moduleCode - e.g. "ENGS404"
	 * @param {Object[]} input.notes - [{ level, stage, text }]
	 * @param {Object[]} input.pages - [{ filename, content }]
	 * @param {string|null} input.worklist - the {CODE}_interactives.txt text
	 * @param {Object} input.data - the loaded data files (needs TemplateCheckQuestions)
	 * @returns {Object|null} the check:
	 *   { module, sections, strings, files, plurals, tickSections,
	 *     questions: [{ id, type, section, page, pageFile, activity, text,
	 *     blanks, writerText, writerLabel, sourceNote, details, rows, choices }],
	 *     counts: { questions, ticks, info, handled, writerNotes }, minutes,
	 *     summary, mini }
	 */
	static Classify({ moduleCode, notes, pages, worklist, data }) {
		const cat = data?.TemplateCheckQuestions;
		if (!this.Enabled(cat)) return null;
		const meta = cat._meta;
		const rx = this.#compile(cat);
		const code = moduleCode ?? "";

		// ---- the pages: label, notes, activities, boxes ------------------
		const pageInfo = (pages ?? []).map((p) => this.#readPage(p, rx, meta))
			.sort((a, b) => this.#comparePages(a.page, b.page));
		const fileOf = new Map(pageInfo.map((p) => [p.page, p.filename]));
		const renumbered = this.#renumberedActivities(notes ?? [], rx);
		const work = this.#readWorklist(worklist);

		// ---- every source item, classified -------------------------------
		const matches = [];   // { q, qi, rule, item, blanks }
		const other = [];
		let handled = 0;
		let writerNotes = 0;
		const claim = (item) => {
			const found = this.#match(cat, rx, item, code);
			if (found.length) { matches.push(...found); return; }
			if (this.#ignored(meta, rx, item)) { handled++; return; }
			if (item.source === "run") {
				if ((meta.other.run_levels ?? []).includes(item.level)) other.push(item);
				else handled++;
			} else if (item.source === "page") {
				if ((meta.other.page_prefixes ?? []).includes(item.prefix)) other.push(item);
				else writerNotes++;
			}
		};
		(notes ?? []).forEach((n, i) => claim({ source: "run", level: n.level, stage: n.stage, text: String(n.text ?? ""), order: i }));
		for (const p of pageInfo) {
			for (const n of p.notes) claim({ source: "page", prefix: n.prefix, text: n.body, full: n.full, page: p.page, pageObj: p, offset: n.offset });
			for (const b of p.boxes) claim({ source: "box", page: p.page, pageObj: p, offset: b.offset, box: b });
		}

		// ---- blanks every match carries ----------------------------------
		for (const m of matches) this.#placeMatch(m, meta, rx, pageInfo, renumbered, work);

		// ---- group the matches into questions ----------------------------
		const questions = [];
		cat.questions.forEach((q, qi) => {
			if (q.enabled === false) return;
			const mine = matches.filter((m) => m.q === q);
			if (!mine.length) return;
			for (const g of this.#groups(q, mine)) questions.push(this.#question(q, qi, g, meta, data, pageInfo, fileOf));
		});
		for (const item of other) questions.push(this.#otherQuestion(item, meta, fileOf));

		// ---- order: section, then catalogue order, then page, then position
		const sectionOrder = new Map(meta.sections.map((s, i) => [s.id, i]));
		questions.sort((a, b) =>
			(sectionOrder.get(a.section) ?? 99) - (sectionOrder.get(b.section) ?? 99)
			|| a._qi - b._qi
			|| this.#comparePages(a.page, b.page)
			|| a._order - b._order);
		const seen = new Map();
		for (const q of questions) {
			// ids are unique within a check (a repeat gets -2, -3, …)
			const n = (seen.get(q.id) ?? 0) + 1;
			seen.set(q.id, n);
			if (n > 1) q.id = `${q.id}-${n}`;
			delete q._qi; delete q._order;
		}

		const check = {
			module: code,
			sections: meta.sections,
			strings: meta.strings,
			files: meta.files,
			plurals: meta.plurals,
			tickSections: meta.tick_sections ?? [4, 5],
			questions,
			counts: { handled, writerNotes },
		};
		this.#summarise(check, meta);
		return check;
	};

	// =======================================================================
	// READING THE PAGES
	// =======================================================================

	/**
	 * One page: its label (from the file name), its notes (with their
	 * prefix and plain text), its activity spans and its hand-off boxes.
	 */
	static #readPage(p, rx, meta) {
		const html = p.content ?? "";
		const fm = (p.filename ?? "").match(rx.pageFile);
		const page = fm ? fm[2].replace(/_/g, ".") : (p.filename ?? "");
		const notes = [];
		for (const m of html.matchAll(rx.noteElement)) {
			const full = this.#plainText(m[1]);
			const pm = full.match(rx.notePrefix);
			notes.push({ offset: m.index, full, prefix: pm ? pm[1] : "", body: pm ? full.slice(pm[0].length) : full });
		}
		// activity and box spans, from the <div> nesting
		const acts = [];
		const boxSpans = [];
		const stack = [];
		for (const m of html.matchAll(/<div\b[^>]*>|<\/div\s*>/gi)) {
			if (m[0][1] === "/") {
				const top = stack.pop();
				if (top?.act) acts.push({ num: top.act, start: top.start, end: m.index });
				if (top?.box) boxSpans.push({ ...top.box, start: top.start, end: m.index });
				continue;
			}
			const a = m[0].match(rx.activity);
			const b = m[0].match(rx.box);
			stack.push({ start: m.index, act: a ? a[1] : null, box: b ? { index: b[1], ref: b[2] } : null });
		}
		const boxes = [];
		for (const m of html.matchAll(rx.boxGlobal)) {
			const lab = html.slice(m.index).match(rx.boxLabel);
			boxes.push({ offset: m.index, index: m[1], ref: m[2], label: lab ? lab[1] : "", type: lab ? lab[2] : "" });
		}
		return { page, filename: p.filename, html, notes, acts, boxSpans, boxes, text: null };
	};

	/** The innermost span (a hand-off box) that contains an offset. */
	static #innermost(spans, offset) {
		let best = null;
		for (const s of spans) if (s.start < offset && offset < s.end && (!best || s.start > best.start)) best = s;
		return best;
	};

	/**
	 * The nearest activity opened above an offset on the page. PageForge
	 * prints a note straight after the element it belongs to, so a note just
	 * below an activity box belongs to that activity.
	 */
	static #nearestAbove(spans, offset) {
		let best = null;
		for (const s of spans) if (s.start < offset && (!best || s.start > best.start)) best = s;
		return best;
	};

	/** A note's inner HTML as plain text: tags out, entities decoded, one line. */
	static #plainText(html) {
		return String(html)
			.replace(/<br\s*\/?>/gi, " ")
			.replace(/<[^>]+>/g, "")
			.replace(/&#(\d+);/g, (w, d) => String.fromCodePoint(Number(d)))
			.replace(/&#x([0-9a-f]+);/gi, (w, h) => String.fromCodePoint(parseInt(h, 16)))
			.replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">")
			.replace(/&nbsp;/g, " ").replace(/&amp;/g, "&")
			.replace(/\s+/g, " ").trim();
	};

	/** Page labels compare part by part as numbers: 3.1 < 10.0. */
	static #comparePages(a, b) {
		if (a === b) return 0;
		if (!a) return -1;
		if (!b) return 1;
		const pa = String(a).split("."), pb = String(b).split(".");
		for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
			const d = (Number(pa[i] ?? -1) || 0) - (Number(pb[i] ?? -1) || 0);
			if (d) return d;
		}
		return String(a).localeCompare(String(b));
	};

	/** page → { activity as shipped → the writer's number }, from the renumbering notes. */
	static #renumberedActivities(notes, rx) {
		const out = new Map();
		for (const n of notes) {
			const m = String(n.text ?? "").match(rx.renumbered);
			if (!m) continue;
			const map = out.get(m.groups.page) ?? new Map();
			for (const p of m.groups.changes.matchAll(rx.renumberedPair)) if (!map.has(p[2])) map.set(p[2], p[1]);
			out.set(m.groups.page, map);
		}
		return out;
	};

	/** The worklist's entries: "File:" + data-cv2-index → { type, activity }. */
	static #readWorklist(text) {
		const out = new Map();
		if (!text) return out;
		for (const block of String(text).split(/\n(?=INTERACTIVE \d+ of \d+)/)) {
			const file = block.match(/^File:\s*(\S+)/m)?.[1];
			const index = block.match(/data-cv2-index="(\d+)"/)?.[1];
			if (!file || !index) continue;
			const activity = block.match(/^Activity:\s*(.+)$/m)?.[1]?.trim() ?? "";
			out.set(`${file}#${index}`, {
				type: block.match(/^Type:\s*(.+)$/m)?.[1]?.trim() ?? "",
				activity: /^\(none/.test(activity) ? "" : activity,
			});
		}
		return out;
	};

	// =======================================================================
	// MATCHING
	// =======================================================================

	/** Compiles the catalogue's regexes once per catalogue object. */
	static #compile(cat) {
		let c = this.#compiled.get(cat);
		if (c) return c;
		const m = cat._meta;
		const pn = m.page_notes;
		c = {
			request: new RegExp(m.request_words, m.request_flags ?? "i"),
			noteElement: new RegExp(pn.element, "g"),
			notePrefix: new RegExp(pn.prefix),
			activity: new RegExp(pn.activity),
			box: new RegExp(pn.box),
			boxGlobal: new RegExp(pn.box, "g"),
			boxLabel: new RegExp(pn.box_label),
			pageFile: new RegExp(pn.page_file),
			renumbered: new RegExp(m.activity_renumbered.pattern),
			renumberedPair: new RegExp(m.activity_renumbered.pair, "g"),
			tagForms: (m.tag_forms ?? []).map((t) => ({ re: new RegExp(t.pattern), form: t.form })),
			ignore: (m.ignore?.rules ?? []).map((r) => ({ ...r, re: new RegExp(r.pattern, r.flags ?? "") })),
			rules: new Map(),
		};
		for (const q of cat.questions) {
			for (const r of q.match ?? []) {
				if (r.pattern == null) continue;
				c.rules.set(r, {
					re: new RegExp(r.pattern, r.flags ?? ""),
					all: r.repeat ? new RegExp(r.pattern, (r.flags ?? "") + "g") : null,
				});
			}
		}
		this.#compiled.set(cat, c);
		return c;
	};

	/**
	 * The first catalogue entry whose rule matches an item claims it. A
	 * "repeat" rule makes one match per occurrence in the note.
	 *
	 * @returns {Object[]} the matches (empty when nothing claims the item)
	 */
	static #match(cat, rx, item, code) {
		for (let qi = 0; qi < cat.questions.length; qi++) {
			const q = cat.questions[qi];
			if (q.enabled === false) continue;
			for (const rule of q.match ?? []) {
				if ((rule.source ?? "page") !== item.source) continue;
				if (item.source === "box") return [{ q, qi, rule, item, blanks: {} }];
				if (item.source === "page" && rule.prefix && !rule.prefix.includes(item.prefix)) continue;
				if (item.source === "run" && rule.level && !rule.level.includes(item.level)) continue;
				if (rule.requires === "request_words" && !rx.request.test(item.text)) continue;
				const cr = rx.rules.get(rule);
				const m = cr ? item.text.match(cr.re) : [item.text];
				if (!m) continue;
				if (rule.not_own_code && m.groups?.[rule.not_own_code]
					&& m.groups[rule.not_own_code].toUpperCase() === String(code).toUpperCase()) continue;
				if (cr?.all) {
					return [...item.text.matchAll(cr.all)].map((x) => ({ q, qi, rule, item, blanks: { ...(x.groups ?? {}) } }));
				}
				return [{ q, qi, rule, item, blanks: { ...(m.groups ?? {}) } }];
			}
		}
		return [];
	};

	/** Is an unclaimed item PageForge's own routine work? */
	static #ignored(meta, rx, item) {
		for (const r of rx.ignore) {
			if ((r.source ?? "run") !== item.source) continue;
			if (item.source === "page" && r.prefix && !r.prefix.includes(item.prefix)) continue;
			if (r.re.test(item.text)) return true;
		}
		return false;
	};

	/**
	 * Gives a match its place — page, activity, the writer's activity number,
	 * the hand-off box it sits in — plus its context blanks (a button's label,
	 * the writer's nearby note) and its derived blanks (tag and type wording).
	 */
	static #placeMatch(m, meta, rx, pageInfo, renumbered, work) {
		const b = m.blanks;
		const item = m.item;
		let p = item.pageObj ?? null;
		let page = item.page ?? b.page ?? "";
		if (!p && m.rule.locate && b[m.rule.locate]) {
			// a run note that quotes the page's own words: find that page
			const needle = String(b[m.rule.locate]).trim();
			p = pageInfo.find((x) => {
				x.text ??= this.#plainText(x.html);
				return needle && x.text.includes(needle);
			}) ?? null;
			if (p) page = p.page;
		}
		if (!p && page) p = pageInfo.find((x) => x.page === page) ?? null;
		b.page = page;
		if (p && item.offset != null) {
			const act = this.#nearestAbove(p.acts, item.offset);
			if (act) {
				b.activity = act.num;
				b.writer_activity = renumbered.get(page)?.get(act.num) ?? "";
				if (b.writer_activity === act.num) b.writer_activity = "";
			}
			if (item.source !== "box") {
				const box = this.#innermost(p.boxSpans, item.offset);
				if (box) b.box = box.ref;
			}
		}
		if (item.source === "box") {
			const bx = item.box;
			const w = work.get(`${p?.filename}#${bx.index}`);
			b.ref = bx.label || bx.ref;
			b.type = bx.type || w?.type || "";
			if (!b.activity && w?.activity) b.activity = w.activity;
		}
		if (item.source === "page") b.note = item.text;
		// context captured from the page next to the note: the nearest match
		// "before" it, or the first one "after" it (a rule may set its own)
		const ctx = m.rule.context ?? m.q.context ?? {};
		for (const [name, c] of Object.entries(ctx)) {
			if (!p || item.offset == null || b[name]) continue;
			const within = c.within ?? 600;
			if (c.after) {
				const hit = p.html.slice(item.offset, item.offset + within).match(new RegExp(c.after));
				if (hit) b[name] = this.#plainText(hit[1]);
				continue;
			}
			const win = p.html.slice(Math.max(0, item.offset - within), item.offset);
			const all = [...win.matchAll(new RegExp(c.before, "g"))];
			if (all.length) b[name] = this.#plainText(all[all.length - 1][1]);
		}
		// the writer's own note just before this one
		const wt = m.rule.writer_text ?? m.q.writer_text;
		if (wt === "nearby" && p && item.offset != null) {
			const within = meta.nearby_note_within ?? 4000;
			const prior = p.notes.filter((n) => n.prefix === meta.page_notes.writer_prefix
				&& n.offset < item.offset && item.offset - n.offset <= within);
			if (prior.length) b.nearby = prior[prior.length - 1].body;
		}
		if (b.tag) b.tag_form = this.#tagForm(rx, b.tag);
		if (b.type) {
			b.type_name = String(b.type).split(/\s*\+\s*/).map((t) => meta.type_names?.[t] ?? t).join(" + ");
			const art = meta.article ?? {};
			b.type_article = (art.forms ?? ["a", "an"])[new RegExp(art.an_pattern ?? "^[aeiou]", "i").test(b.type_name) ? 1 : 0];
		}
		m.where = this.#where(meta, b);
		m.order = item.offset ?? item.order ?? 0;
	};

	/** [tab 1], [tab 2] … for a numbered tag; [correct] for the rest. */
	static #tagForm(rx, tag) {
		for (const f of rx.tagForms) {
			const m = String(tag).match(f.re);
			if (m) return Utils.FillTemplate(f.form, { ...(m.groups ?? {}), tag });
		}
		return `[${tag}]`;
	};

	/** "Page 4.0, activity 4A" — the first where-form whose blanks are all known. */
	static #where(meta, b) {
		if (!b.page) return "";
		return this.#pick(meta.where.forms, b) ?? "";
	};

	// =======================================================================
	// GROUPING AND WORDING
	// =======================================================================

	/** Splits one catalogue entry's matches into its questions. */
	static #groups(q, mine) {
		const groups = new Map();
		const add = (key, m) => { if (!groups.has(key)) groups.set(key, []); groups.get(key).push(m); };
		const itemKey = (m) => {
			for (const name of q.item ?? []) {
				const s = this.#slug(m.blanks[name]);
				if (s) return s;
			}
			return "";
		};
		const counters = new Map();
		for (const m of mine) {
			if (q.group === "module" || q.group === "table") add("module|all", m);
			else if (q.group === "page_item") add(`${m.blanks.page || "module"}|${itemKey(m) || "all"}`, m);
			else {
				const page = m.blanks.page || "module";
				let k = itemKey(m);
				if (!k) {
					const n = (counters.get(page) ?? 0) + 1;
					counters.set(page, n);
					k = `n${n}`;
				}
				add(`${page}|${k}|${m.order}|${groups.size}`, m);
			}
		}
		return [...groups.entries()].map(([key, ms]) => {
			const [page, item] = key.split("|");
			return { page: page === "module" ? "" : page, item, matches: ms };
		});
	};

	/** One question object from a group of matches. */
	static #question(q, qi, g, meta, data, pageInfo, fileOf) {
		const first = g.matches[0];
		const blanks = { ...first.blanks };
		const pagesOf = [...new Set(g.matches.map((m) => m.blanks.page).filter(Boolean))]
			.sort((a, b) => this.#comparePages(a, b));
		const actsOf = [...new Set(g.matches.map((m) => m.blanks.activity).filter(Boolean))];
		let count;
		if (q.group === "each") count = Number(first.blanks.count) || 1;
		else if (q.count_from) {
			const n = g.matches.map((m) => Number(m.blanks[q.count_from])).find((x) => x > 0);
			count = n || g.matches.length;
		} else count = g.matches.length;
		blanks.count = count;
		if (pagesOf.length) blanks.pages = this.#pluralForm(meta.pages_form, pagesOf.length, this.#list(meta, pagesOf));
		if (q.group !== "each") {
			// a group spanning several pages or activities names them all
			if (pagesOf.length !== 1) { blanks.page = ""; blanks.activity = ""; blanks.writer_activity = ""; }
			else if (actsOf.length > 1) {
				blanks.activity = "";
				blanks.writer_activity = "";
				blanks.activities = this.#activityList(meta, actsOf);
			}
		}
		if (q.pagelist) blanks.pagelist = pageInfo.map((p) => p.page).join(", ");
		blanks.where = this.#where(meta, blanks);
		this.#plurals(meta, blanks);

		const rule = q.group === "each" ? first.rule : null;
		const text = this.#pick(rule?.question ?? q.question, blanks) ?? "";
		const details = [];
		if (q.group !== "each" && q.group !== "table") {
			for (const m of g.matches) {
				const tpl = m.rule.detail ?? q.detail;
				if (!tpl) continue;
				const mb = { ...m.blanks, where: m.where };
				this.#plurals(meta, mb);
				const line = this.#pick(tpl, mb);
				if (line) details.push(line);
			}
		}
		const rows = q.group === "table" ? this.#rows(q, g, meta) : [];
		if (q.group === "table") {
			blanks.rows = rows.length;
			this.#plurals(meta, blanks);
		}
		const id = `${q.id}:${g.page || "module"}:${g.item || "all"}`;
		const wt = first.rule.writer_text ?? q.writer_text;
		const writerText = wt === "note" ? (first.blanks.note ?? "")
			: wt === "nearby" ? (first.blanks.nearby ?? "")
				: wt ? (first.blanks[wt] ?? "") : "";
		return {
			id,
			type: q.id,
			section: q.section,
			page: g.page,
			pageFile: g.page ? (fileOf.get(g.page) ?? "") : "",
			activity: blanks.activity || (actsOf.length > 1 ? actsOf.join(", ") : ""),
			text: q.group === "table" ? (this.#pick(q.question, blanks) ?? "") : text,
			blanks,
			writerText,
			// the quote's label: none when the question itself says the writer wrote it
			writerLabel: wt === "nearby" ? "nearby_note" : (writerText && wt !== "note" ? "writer_said" : ""),
			sourceNote: this.#sourceNote(first.item),
			details: this.#collapse(details),
			rows,
			choices: this.#choices(q, data),
			_qi: qi,
			_order: first.order,
		};
	};

	/**
	 * Table rows: one per row key, each with its own answer id. A "row_each"
	 * rule gives every match its own row (a repeated key gets -2, -3, …).
	 */
	static #rows(q, g, meta) {
		const rows = new Map();
		for (const m of g.matches) {
			const raw = Utils.FillTemplate(m.rule.row ?? "{item}", m.blanks);
			let key = this.#slug(raw) || "row";
			if (m.rule.row_each) {
				let n = 1;
				while (rows.has(n === 1 ? key : `${key}-${n}`)) n++;
				if (n > 1) key = `${key}-${n}`;
			}
			if (!rows.has(key)) rows.set(key, { key, rule: m.rule, matches: [] });
			rows.get(key).matches.push(m);
		}
		return [...rows.values()].map((r) => {
			const b = { ...r.matches[0].blanks, where: r.matches[0].where };
			// a one-note row keeps the number its note gives («2 empty callouts …»)
			const captured = Number(r.matches[0].blanks.count);
			b.count = r.matches.length === 1 && captured > 0 ? captured : r.matches.length;
			const items = [...new Set(r.matches.map((m) => String(m.blanks.item ?? "").trim()).filter(Boolean))];
			b.items = items.length ? this.#list(meta, items) : "";
			this.#plurals(meta, b);
			return {
				id: `${q.id}:module:${r.key}`,
				label: this.#pick(r.rule.row_label ?? "{item}", b) ?? r.key,
				blanks: b,
				sourceNote: this.#sourceNote(r.matches[0].item),
			};
		});
	};

	/** A question for something no entry claims (section 7, information only). */
	static #otherQuestion(item, meta, fileOf) {
		const b = { note: item.source === "page" ? item.full : item.text, page: item.page ?? "" };
		const p = item.pageObj;
		if (p && item.offset != null) {
			const act = this.#nearestAbove(p.acts, item.offset);
			if (act) b.activity = act.num;
		}
		b.where = this.#where(meta, b);
		return {
			id: `OTHER:${b.page || "module"}:${this.#slug(b.note) || "note"}`,
			type: "OTHER",
			section: meta.other.section,
			page: b.page,
			pageFile: b.page ? (fileOf.get(b.page) ?? "") : "",
			activity: b.activity ?? "",
			text: this.#pick(meta.other.question, b) ?? b.note,
			blanks: b,
			writerText: "",
			writerLabel: "",
			sourceNote: this.#sourceNote(item),
			details: [],
			rows: [],
			choices: { kind: "info" },
			_qi: 1e6,
			_order: item.offset ?? item.order ?? 0,
		};
	};

	/** The note a question came from, as PageForge wrote it. */
	static #sourceNote(item) {
		if (item.source === "page") return item.full;
		if (item.source === "box") return `${item.box.label || item.box.ref} (data-cv2-index ${item.box.index})`;
		return item.text;
	};

	/** The answer spec, with any options listed in another data file filled in. */
	static #choices(q, data) {
		const a = { ...(q.answer ?? { kind: "info" }) };
		if (a.options_from) {
			const src = data?.[a.options_from.data]?.[a.options_from.key] ?? {};
			const values = [...new Set(Object.entries(src).filter(([k]) => !k.startsWith("_")).map(([, v]) => String(v)))]
				.sort((x, y) => x.localeCompare(y));
			a.options = [...values.map((v) => ({ id: v, label: v })), ...(a.options ?? [])];
			delete a.options_from;
		}
		return a;
	};

	/** Repeated detail lines collapse into one line with a count. */
	static #collapse(lines) {
		const counts = new Map();
		for (const l of lines) counts.set(l, (counts.get(l) ?? 0) + 1);
		return [...counts].map(([l, n]) => (n > 1 ? `${l} (×${n})` : l));
	};

	/** The one-line summary, the counts and the time estimate. */
	static #summarise(check, meta) {
		const qs = new Set(meta.question_sections ?? [1, 2, 3]);
		const ts = new Set(meta.tick_sections ?? [4, 5]);
		const answerable = check.questions.filter((q) => q.choices.kind !== "info");
		const questions = answerable.filter((q) => qs.has(q.section)).length;
		const ticks = answerable.filter((q) => ts.has(q.section)).length;
		const t = meta.timing ?? {};
		const seconds = questions * (t.seconds_per_question ?? 40) + ticks * (t.seconds_per_tick ?? 10);
		const minutes = Math.max(1, Math.ceil(seconds / 60));
		Object.assign(check.counts, {
			questions,
			ticks,
			info: check.questions.length - answerable.length,
		});
		check.minutes = minutes;
		const s = meta.strings;
		const b = { questions, ticks, minutes };
		this.#plurals(meta, b);
		b.ticks_part = ticks ? Utils.FillTemplate(s.summary_ticks, b) : "";
		check.summary = !questions && !ticks ? s.summary_none
			: !questions ? Utils.FillTemplate(s.summary_ticks_only, b)
				: Utils.FillTemplate(s.summary, b);
		check.mini = !questions && !ticks ? s.mini_none : Utils.FillTemplate(s.mini, b);
	};

	// =======================================================================
	// SMALL HELPERS (wording)
	// =======================================================================

	/**
	 * The first template (a string or a list) whose {blanks} are all filled
	 * (a plural blank may be empty — «1 item{s}»); null when none is.
	 */
	static #pick(templates, blanks) {
		const list = Array.isArray(templates) ? templates : [templates];
		const filled = (k) => blanks[k] != null && (String(blanks[k]) !== "" || this.#pluralKeys.has(k));
		for (const t of list) {
			if (typeof t !== "string") continue;
			const keys = [...t.matchAll(/\{(\w+)\}/g)].map((m) => m[1]);
			if (keys.every(filled)) return Utils.FillTemplate(t, blanks);
		}
		return null;
	};

	/** {s}, {is_are} … follow {count}; any other number blank X gets {X_s} … */
	static #plurals(meta, b) {
		const forms = Object.entries(meta.plurals ?? {}).filter(([k]) => !k.startsWith("_"));
		for (const [name, value] of Object.entries(b)) {
			const n = typeof value === "number" ? value : (name === "count" ? Number(value) : NaN);
			if (!Number.isFinite(n) || this.#pluralKeys.has(name)) continue;
			for (const [k, pair] of forms) {
				const key = name === "count" ? k : `${name}_${k}`;
				this.#pluralKeys.add(key);
				b[key] = n === 1 ? pair[0] : pair[1];
			}
		}
	};

	/** "a, b and c" — at most lists.max entries, then "and N more". */
	static #list(meta, items) {
		const l = meta.lists ?? {};
		const max = l.max ?? 6;
		// one left over is named rather than counted ("… and 1 more" says nothing)
		const shown = items.length > max + 1 ? items.slice(0, max) : items;
		const rest = items.length - shown.length;
		if (rest > 0) return shown.join(l.sep ?? ", ") + Utils.FillTemplate(l.more ?? " and {n} more", { n: rest });
		if (shown.length < 2) return shown.join("");
		return shown.slice(0, -1).join(l.sep ?? ", ") + (l.last ?? " and ") + shown[shown.length - 1];
	};

	/**
	 * Several activities on one page: "activities 4A to 4L" when they run on
	 * letter by letter (three or more), else "activities 6A, 6B and 6G".
	 */
	static #activityList(meta, acts) {
		const parts = acts.map((a) => String(a).match(/^(\d+(?:\.\d+)?)([A-Z])$/));
		if (acts.length >= 3 && meta.activities_range_form && parts.every((m) => m && m[1] === parts[0][1])) {
			const letters = parts.map((m) => m[2].charCodeAt(0)).sort((a, b) => a - b);
			if (letters.every((c, i) => !i || c === letters[i - 1] + 1)) {
				return Utils.FillTemplate(meta.activities_range_form, {
					first: parts[0][1] + String.fromCharCode(letters[0]),
					last: parts[0][1] + String.fromCharCode(letters[letters.length - 1]),
				});
			}
		}
		return this.#pluralForm(meta.activities_form, acts.length, this.#list(meta, acts));
	};

	/** ["page {list}", "pages {list}"] by number. */
	static #pluralForm(forms, n, list) {
		const f = Array.isArray(forms) ? forms[n === 1 ? 0 : 1] : forms;
		return Utils.FillTemplate(f ?? "{list}", { list });
	};

	/** A short, stable id part from free text. */
	static #slug(s) {
		return s == null ? "" : Utils.Slugify(String(s), 40);
	};

	// =======================================================================
	// THE ANSWERS (these travel into the stand-alone page: no outside calls)
	// =======================================================================

	/**
	 * The answerable units of a check: one per question, plus one per row of
	 * a table question (the table's own unit holds its comment and Skip).
	 * Information-only questions have none.
	 *
	 * @param {Object} check
	 * @returns {Object[]} [{ id, question, row }]
	 */
	static AnswerUnits(check) {
		const units = [];
		for (const q of check?.questions ?? []) {
			if (!q.choices || q.choices.kind === "info") continue;
			units.push({ id: q.id, question: q, row: null });
			if (q.choices.kind === "table") for (const r of q.rows ?? []) units.push({ id: r.id, question: q, row: r });
		}
		return units;
	};

	/**
	 * Has this answer anything in it? (A comment alone counts.)
	 *
	 * @param {Object|undefined} a - { choice, text, comment, skipped }
	 * @returns {boolean}
	 */
	static IsAnswered(a) {
		return !!a && !a.skipped && !!(a.choice || a.text || a.comment);
	};

	/**
	 * The counts for the answers file: a table counts as one question,
	 * answered when it or any of its rows is.
	 *
	 * @param {Object} check
	 * @param {Object} state - { answers: { id: { choice, text, comment, skipped } } }
	 * @returns {Object} { questions, ticks, answered, skipped }
	 */
	static Counts(check, state) {
		const answers = state?.answers ?? {};
		const ticks = new Set(check?.tickSections ?? [4, 5]);
		const out = { questions: 0, ticks: 0, answered: 0, skipped: 0 };
		for (const q of check?.questions ?? []) {
			if (!q.choices || q.choices.kind === "info") continue;
			const ids = [q.id, ...(q.choices.kind === "table" ? (q.rows ?? []).map((r) => r.id) : [])];
			if (ticks.has(q.section)) out.ticks++; else out.questions++;
			if (ids.some((id) => this.IsAnswered(answers[id]))) out.answered++;
			else if (answers[q.id]?.skipped) out.skipped++;
		}
		return out;
	};

	/**
	 * Builds the answers file's object ({CODE}_template-answers.json).
	 *
	 * @param {Object} check
	 * @param {Object} state - { answers: { id: {...} }, answeredBy }
	 * @param {Object} info - { version, wtFile, wtSha256, checkedAt, savedAt }
	 * @returns {Object} the plain object to JSON.stringify
	 */
	static BuildAnswers(check, state, info = {}) {
		const files = check?.files ?? {};
		const answers = state?.answers ?? {};
		return {
			format: files.format ?? "pageforge-template-answers",
			format_version: files.format_version ?? 1,
			module: check?.module ?? "",
			pageforge_version: info.version ?? "",
			writers_template: { file: info.wtFile ?? "", sha256: info.wtSha256 ?? "" },
			checked_at: info.checkedAt ?? "",
			saved_at: info.savedAt ?? new Date().toISOString(),
			answered_by: String(state?.answeredBy ?? ""),
			counts: this.Counts(check, state),
			answers: this.AnswerUnits(check).map((u) => {
				const a = answers[u.id] ?? {};
				const q = u.question;
				// a table row is skipped with its table (Skip sits on the table)
				const skipped = u.row ? !!answers[q.id]?.skipped : !!a.skipped;
				return {
					id: u.id,
					type: q.type,
					section: q.section,
					page: q.page ?? "",
					activity: q.activity ?? "",
					question: q.text ?? "",
					row: u.row ? u.row.label : "",
					writer_text: q.writerText ?? "",
					pageforge_note: u.row ? (u.row.sourceNote ?? "") : (q.sourceNote ?? ""),
					choice: String(a.choice ?? ""),
					text: String(a.text ?? ""),
					comment: String(a.comment ?? ""),
					skipped,
				};
			}),
		};
	};

	/**
	 * Reads a saved answers object back into a state for this check.
	 *
	 * @param {Object} saved - the parsed answers file
	 * @param {Object} check
	 * @returns {Object} { ok, state, unknown } — or { ok:false, reason:"bad" |
	 *   "other_module", module }
	 */
	static ReadAnswers(saved, check) {
		const files = check?.files ?? {};
		if (!saved || typeof saved !== "object" || saved.format !== (files.format ?? "pageforge-template-answers")
			|| !Array.isArray(saved.answers)) {
			return { ok: false, reason: "bad" };
		}
		if (saved.module && check?.module && String(saved.module).toUpperCase() !== String(check.module).toUpperCase()) {
			return { ok: false, reason: "other_module", module: saved.module };
		}
		const units = new Map(this.AnswerUnits(check).map((u) => [u.id, u]));
		const state = { answers: {}, answeredBy: String(saved.answered_by ?? "") };
		let unknown = 0;
		for (const a of saved.answers) {
			const u = a ? units.get(a.id) : null;
			if (!u) { unknown++; continue; }
			state.answers[a.id] = {
				choice: String(a.choice ?? ""),
				text: String(a.text ?? ""),
				comment: String(a.comment ?? ""),
				// a row's skip is its table's, so it is read from the table's own entry
				skipped: u.row ? false : !!a.skipped,
			};
		}
		return { ok: true, state, unknown };
	};
}

// Node export hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { TemplateCheck };
