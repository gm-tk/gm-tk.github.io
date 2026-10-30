/**
 * TemplateCheckPanel.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Draws the Template check and lets the developer answer it. ONE renderer,
 * used in two places:
 *   - the "Template check" panel of the HTML Generator (Show), and
 *   - the stand-alone page in the download zip,
 *     template-check/{CODE}_template-check.html (BuildPage), which works
 *     offline when opened straight from the unzipped folder.
 * Every question has its answer choices, a comment box and Skip. There is a
 * Skip all, a Save my answers (downloads {CODE}_template-answers.json) and a
 * Load saved answers (so the developer can carry on later).
 *
 * WHY SEPARATE FILE:
 * Presentation only: it reads the check TemplateCheck built and writes DOM;
 * it never touches a conversion or run.outputs. The check's files reach the
 * zip only through ZipFiles(), which App.js adds to the "Download all" list.
 *
 * THE STAND-ALONE PAGE CARRIES THIS CLASS'S SOURCE (and TemplateCheck's), so
 * everything the page calls here — Mount and the private helpers it uses —
 * relies on nothing outside the two classes: no Config, no Utils, no
 * network. The styles below are the same in both places.
 * ===========================================================================
 */

class TemplateCheckPanel {

	/** The check's styles, shared by the app panel and the stand-alone page. */
	static Css = `
.tc { --tc-ink: #1d2733; --tc-soft: #5a6878; --tc-line: #d8dee5; --tc-accent: #0b6e4f;
	--tc-accent-soft: #e2f1ec; --tc-attention: #c0392b; --tc-paper: #f4f6f8; --tc-done: #2f9e44;
	color: var(--tc-ink); font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; line-height: 1.5; }
.tc [hidden] { display: none !important; }
body.tc-page { margin: 0; background: #f4f6f8; }
body.tc-page .tc { max-width: 880px; margin: 0 auto; padding: 24px 20px 64px; }
.tc-title { font-size: 1.5rem; margin: 0 0 6px; }
.tc-intro { color: var(--tc-soft); margin: 0 0 14px; }
.tc-summary { font-weight: 600; margin: 0 0 12px; }
.tc-toolbar { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 0 0 6px; }
.tc-btn { font: inherit; font-size: 0.95rem; padding: 6px 14px; border: 1px solid var(--tc-line); border-radius: 6px;
	background: #fff; color: var(--tc-ink); cursor: pointer; display: inline-block; }
.tc-btn:hover { filter: brightness(0.95); }
.tc-btn-primary { background: var(--tc-accent); border-color: var(--tc-accent); color: #fff; font-weight: 600; }
.tc-load input { display: none; }
.tc-progress { color: var(--tc-soft); font-size: 0.9rem; margin-left: auto; }
.tc-status { min-height: 1.3em; margin: 2px 0 6px; color: var(--tc-accent); font-size: 0.9rem; }
.tc-status.tc-bad { color: var(--tc-attention); }
.tc-name { display: flex; gap: 8px; align-items: center; margin: 0 0 10px; font-size: 0.9rem; color: var(--tc-soft); }
.tc-name input { max-width: 260px; }
.tc-section { margin: 18px 0 0; }
.tc-section-title { font-size: 1.05rem; margin: 0 0 2px; }
summary.tc-section-title { cursor: pointer; }
.tc-count { color: var(--tc-soft); font-weight: normal; }
.tc-section-desc { color: var(--tc-soft); margin: 0 0 8px; font-size: 0.92rem; }
.tc-q { border: 1px solid var(--tc-line); border-left: 4px solid var(--tc-accent); border-radius: 6px; background: #fff;
	padding: 10px 14px; margin: 0 0 10px; }
.tc-q.tc-done { border-left-color: var(--tc-done); }
.tc-q.tc-skipped { opacity: 0.6; border-left-color: var(--tc-line); }
.tc-q-text { margin: 0 0 6px; }
.tc-q-details { margin: 0 0 8px; padding-left: 20px; color: var(--tc-soft); font-size: 0.92rem; }
.tc-quote { margin: 0 0 8px; padding: 6px 10px; background: var(--tc-paper); border-left: 3px solid var(--tc-line); font-size: 0.95rem; }
.tc-quote-label { display: block; color: var(--tc-soft); font-size: 0.85rem; }
.tc-answer { margin: 4px 0; }
.tc-opt, .tc-check { display: block; margin: 2px 0; cursor: pointer; }
.tc-field, .tc-say { display: block; margin: 4px 0; }
.tc-field > span, .tc-say > span, .tc-comment > span { display: block; font-size: 0.85rem; color: var(--tc-soft); }
.tc input[type="text"], .tc textarea, .tc select { font: inherit; font-size: 0.95rem; padding: 4px 8px; border: 1px solid var(--tc-line);
	border-radius: 4px; width: 100%; max-width: 560px; box-sizing: border-box; background: #fff; color: var(--tc-ink); }
.tc textarea { resize: vertical; }
.tc-table { border-collapse: collapse; width: 100%; margin: 4px 0; font-size: 0.95rem; }
.tc-table td { border-top: 1px solid var(--tc-line); padding: 6px 10px 6px 0; vertical-align: top; }
.tc-table td:last-child { width: 42%; padding-right: 0; }
.tc-row-say { margin-top: 4px; }
.tc-q-foot { display: flex; gap: 10px; align-items: flex-end; margin-top: 6px; }
.tc-comment { flex: 1; }
.tc-skip { font: inherit; font-size: 0.9rem; padding: 4px 12px; border: 1px solid var(--tc-line); border-radius: 6px;
	background: #fff; color: var(--tc-ink); cursor: pointer; white-space: nowrap; }
.tc-info { margin: 0; padding-left: 20px; font-size: 0.92rem; }
.tc-info li { margin: 2px 0; }
.tc-foot { color: var(--tc-soft); font-size: 0.9rem; margin: 14px 0 0; }
.tc-panel > summary { cursor: pointer; list-style: none; display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px; }
.tc-panel > summary::-webkit-details-marker { display: none; }
.tc-panel > summary::before { content: "▸"; display: inline-block; transition: transform 0.15s; color: #5a6878; }
.tc-panel[open] > summary::before { transform: rotate(90deg); }
.tc-panel-title { font-size: 1.15rem; font-weight: 700; }
.tc-panel-mini { color: #5a6878; font-size: 0.9rem; }
.tc-panel-body { margin-top: 12px; }
`;

	// =======================================================================
	// THE APP PANEL
	// =======================================================================

	/**
	 * Renders the check into the app's panel (open when there is anything to
	 * answer) and wires it.
	 *
	 * @param {HTMLElement} panel - the panel section
	 * @param {Object} check - from TemplateCheck.Classify / FromRun
	 * @param {Object} opts - { info } (see Mount)
	 * @returns {Object} the controller: { getState() }
	 */
	static Show(panel, check, opts = {}) {
		if (!document.getElementById("tc-styles")) {
			const style = document.createElement("style");
			style.id = "tc-styles";
			style.textContent = this.Css;
			document.head.appendChild(style);
		}
		const s = check.strings;
		const open = check.counts.questions + check.counts.ticks > 0;
		panel.innerHTML = `<details class="tc-panel"${open ? " open" : ""}>`
			+ `<summary class="tc-panel-summary"><span class="tc-panel-title">${this.#esc(s.app_title)}</span>`
			+ `<span class="tc-panel-mini">${this.#esc(check.mini)}</span></summary>`
			+ `<div class="tc-panel-body"></div></details>`;
		const controller = this.Mount(panel.querySelector(".tc-panel-body"), check, opts);
		panel.hidden = false;
		return controller;
	};

	/**
	 * The check's files for the "Download all" zip, in its template-check/
	 * folder: the stand-alone page, plus the answers file when the developer
	 * has already answered or skipped something in the app.
	 *
	 * @param {Object|null} entry - { check, info, controller } (null → none)
	 * @returns {Object[]} [{ filename, content }]
	 */
	static ZipFiles(entry) {
		if (!entry?.check) return [];
		const { check, info } = entry;
		const state = entry.controller?.getState?.() ?? null;
		const f = check.files;
		const code = check.module || "module";
		const out = [{ filename: f.folder + this.#fill(f.page, { code }), content: this.BuildPage(check, info, state) }];
		if (state && this.HasAnswers(state)) {
			const saved = TemplateCheck.BuildAnswers(check, state, { ...info, savedAt: new Date().toISOString() });
			out.push({ filename: f.folder + this.#fill(f.answers, { code }), content: JSON.stringify(saved, null, 2) });
		}
		return out;
	};

	/**
	 * Has the developer answered, skipped or named anything yet?
	 *
	 * @param {Object} state - { answers, answeredBy }
	 * @returns {boolean}
	 */
	static HasAnswers(state) {
		if (state?.answeredBy) return true;
		return Object.values(state?.answers ?? {}).some((a) => a && (a.skipped || a.choice || a.text || a.comment));
	};

	// =======================================================================
	// THE STAND-ALONE PAGE
	// =======================================================================

	/**
	 * The stand-alone check page: all CSS and JavaScript inline, the check
	 * embedded as JSON, no external file and no network.
	 *
	 * @param {Object} check
	 * @param {Object} info - { version, wtFile, wtSha256, checkedAt }
	 * @param {Object|null} state - answers given so far (the page opens with them)
	 * @returns {string} the whole HTML document
	 */
	static BuildPage(check, info = {}, state = null) {
		const s = check.strings;
		// "<" inside the JSON and "</script" inside the code are escaped, so
		// nothing embedded can close its script element early
		const json = JSON.stringify({ check, info, state }).replace(/</g, "\\u003c");
		const safe = (src) => String(src).replace(/<\/(script)/gi, "<\\/$1");
		const boot = "(function () {\n"
			+ "\tvar data = JSON.parse(document.getElementById(\"tc-data\").textContent);\n"
			+ "\tTemplateCheckPanel.Mount(document.getElementById(\"tc-root\"), data.check,\n"
			+ "\t\t{ standalone: true, info: data.info, initialState: data.state });\n"
			+ "})();";
		return [
			"<!DOCTYPE html>",
			"<html lang=\"en\">",
			"<head>",
			"<meta charset=\"utf-8\">",
			"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
			`<title>${this.#esc(this.#fill(s.page_title, { code: check.module }))}</title>`,
			`<style>${this.Css}</style>`,
			"</head>",
			"<body class=\"tc-page\">",
			"<main id=\"tc-root\"></main>",
			`<script type="application/json" id="tc-data">${json}<\/script>`,
			`<script>\n${safe(TemplateCheck)}\n${safe(TemplateCheckPanel)}\n${boot}\n<\/script>`,
			"</body>",
			"</html>",
			"",
		].join("\n");
	};

	// =======================================================================
	// THE RENDERER + ITS CONTROLS (shared by both places)
	// =======================================================================

	/**
	 * Renders the check into a root element and wires every control.
	 *
	 * @param {HTMLElement} root
	 * @param {Object} check
	 * @param {Object} opts
	 * @param {boolean} [opts.standalone] - the page's own title and intro
	 * @param {Object} [opts.info] - { version, wtFile, wtSha256, checkedAt } for the answers file
	 * @param {Object} [opts.initialState] - { answers, answeredBy } to start from
	 * @param {Function} [opts.onChange] - called with a copy of the state after each change
	 * @returns {Object} { getState() } — a copy of the answers so far
	 */
	static Mount(root, check, opts = {}) {
		const T = TemplateCheck;
		const s = check.strings;
		const copy = (st) => JSON.parse(JSON.stringify(st ?? { answers: {}, answeredBy: "" }));
		const state = copy(opts.initialState);
		state.answers ??= {};
		state.answeredBy ??= "";
		const units = new Map(T.AnswerUnits(check).map((u) => [u.id, u]));
		const questions = check.questions.filter((q) => q.choices && q.choices.kind !== "info");

		root.innerHTML = this.#render(check, opts);
		this.#apply(root, state);

		const all = (sel) => [...root.querySelectorAll(sel)];
		const ans = (id) => (state.answers[id] ??= { choice: "", text: "", comment: "", skipped: false });
		const idsOf = (q) => [q.id, ...(q.choices.kind === "table" ? (q.rows ?? []).map((r) => r.id) : [])];
		const isDone = (q) => idsOf(q).some((id) => T.IsAnswered(state.answers[id]));
		const isSkipped = (q) => !isDone(q) && !!state.answers[q.id]?.skipped;
		const optionOf = (q, id) => (q?.choices.options ?? []).find((o) => o.id === state.answers[id]?.choice);
		const status = (text, bad) => {
			const el = root.querySelector("[data-tc-status]");
			if (!el) return;
			el.textContent = text;
			el.classList.toggle("tc-bad", !!bad);
		};

		const refresh = () => {
			for (const card of all("[data-tc-q]")) {
				const q = units.get(card.dataset.tcQ)?.question;
				if (!q) continue;
				card.classList.toggle("tc-done", isDone(q));
				card.classList.toggle("tc-skipped", isSkipped(q));
				const skip = card.querySelector("[data-tc-action=\"skip\"]");
				if (skip) skip.textContent = isSkipped(q) ? s.unskip : s.skip;
			}
			// the text box under a choice that asks for words («say which»)
			for (const box of all("[data-tc-say]")) {
				const q = units.get(box.dataset.tcSay)?.question;
				const opt = optionOf(q, box.dataset.tcSay);
				box.hidden = !opt?.say;
				const label = box.querySelector("[data-tc-say-label]");
				if (label && opt?.say) label.textContent = opt.say;
			}
			for (const input of all("[data-tc-row-say]")) {
				const u = units.get(input.dataset.tcId);
				const opt = optionOf(u?.question, input.dataset.tcId);
				input.hidden = !opt?.say;
				if (opt?.say) input.placeholder = opt.say;
			}
			const c = T.Counts(check, state);
			const progress = root.querySelector("[data-tc-progress]");
			if (progress) progress.textContent = this.#fill(s.progress, { answered: c.answered, questions: c.questions + c.ticks, skipped: c.skipped });
			const skipAll = root.querySelector("[data-tc-action=\"skip-all\"]");
			if (skipAll) skipAll.textContent = questions.some((q) => !isDone(q) && !isSkipped(q)) ? s.skip_all : s.unskip_all;
			opts.onChange?.(copy(state));
		};

		const onField = (e) => {
			const target = e.target;
			if (target?.matches?.("[data-tc-name]")) {
				state.answeredBy = target.value;
				refresh();
				return;
			}
			const el = target?.closest?.("[data-tc-field]");
			if (!el || !root.contains(el)) return;
			const id = el.dataset.tcId;
			const u = units.get(id);
			if (!u) return;
			const a = ans(id);
			const field = el.dataset.tcField;
			if (field === "text") {
				a.text = el.value;
				// a link box's "same link" tick is recorded with the link
				const tick = el.closest("[data-tc-q]")?.querySelector("[data-tc-field=\"check\"]");
				if (tick) a.choice = tick.checked ? tick.dataset.tcValue : `not_${tick.dataset.tcValue}`;
			} else if (field === "check") {
				a.choice = el.checked ? el.dataset.tcValue : `not_${el.dataset.tcValue}`;
			} else if (field === "choice") {
				if (el.type !== "radio" || el.checked) a.choice = el.value;
			} else if (field === "tick") {
				a.choice = el.checked ? "noted" : "";
			} else if (field === "comment") {
				a.comment = el.value;
			}
			// answering a skipped question un-skips it
			const own = ans(u.question.id);
			if (own.skipped && T.IsAnswered({ ...a, skipped: false })) own.skipped = false;
			refresh();
		};

		const onLoad = (input) => {
			const file = input.files?.[0];
			if (!file) return;
			const reader = new FileReader();
			reader.onload = () => {
				let saved = null;
				try { saved = JSON.parse(String(reader.result)); } catch { saved = null; }
				const r = T.ReadAnswers(saved, check);
				if (!r.ok) {
					status(r.reason === "other_module"
						? this.#fill(s.load_other_module, { module: r.module, code: check.module })
						: s.load_bad, true);
				} else {
					state.answers = r.state.answers;
					state.answeredBy = r.state.answeredBy;
					this.#apply(root, state);
					let msg = this.#fill(s.loaded, { file: file.name });
					if (r.unknown) msg += " " + this.#fill(s.load_unknown, this.#numbers(check, { count: r.unknown }));
					status(msg);
					refresh();
				}
				input.value = "";
			};
			reader.readAsText(file);
		};

		root.addEventListener("input", onField);
		root.addEventListener("change", (e) => {
			if (e.target?.matches?.("[data-tc-load]")) onLoad(e.target);
			else onField(e);
		});
		root.addEventListener("click", (e) => {
			const btn = e.target?.closest?.("[data-tc-action]");
			if (!btn || !root.contains(btn)) return;
			const act = btn.dataset.tcAction;
			if (act === "skip") {
				const q = units.get(btn.dataset.tcId)?.question;
				if (!q) return;
				ans(q.id).skipped = !isSkipped(q);
				refresh();
			} else if (act === "skip-all") {
				const skip = questions.some((q) => !isDone(q) && !isSkipped(q));
				for (const q of questions) if (!isDone(q)) ans(q.id).skipped = skip;
				refresh();
			} else if (act === "save") {
				const saved = T.BuildAnswers(check, state, { ...(opts.info ?? {}), savedAt: new Date().toISOString() });
				const name = this.#fill(check.files.answers, { code: check.module || "module" });
				this.#download(name, JSON.stringify(saved, null, 2), "application/json");
				status(this.#fill(s.saved, { file: name }));
			}
		});
		refresh();
		return { getState: () => copy(state) };
	};

	/** The whole check as an HTML string. */
	static #render(check, opts) {
		const s = check.strings;
		const e = (x) => this.#esc(x);
		const h = opts.standalone ? "h2" : "h3";
		const out = ["<div class=\"tc\">"];
		if (opts.standalone) {
			out.push(`<h1 class="tc-title">${e(this.#fill(s.page_title, { code: check.module }))}</h1>`);
			out.push(`<p class="tc-intro">${e(s.page_intro)}</p>`);
		}
		out.push(`<p class="tc-summary">${e(check.summary)}</p>`);
		const answerable = check.questions.some((q) => q.choices && q.choices.kind !== "info");
		if (answerable) {
			out.push("<div class=\"tc-toolbar\">"
				+ `<button type="button" class="tc-btn" data-tc-action="skip-all">${e(s.skip_all)}</button>`
				+ `<button type="button" class="tc-btn tc-btn-primary" data-tc-action="save">${e(s.save)}</button>`
				+ `<label class="tc-btn tc-load">${e(s.load)}<input type="file" accept=".json,application/json" data-tc-load></label>`
				+ "<span class=\"tc-progress\" data-tc-progress></span></div>");
			out.push("<p class=\"tc-status\" data-tc-status role=\"status\" aria-live=\"polite\"></p>");
			out.push(`<label class="tc-name"><span>${e(s.name)}</span><input type="text" data-tc-name autocomplete="name"></label>`);
		}
		const bySection = new Map();
		check.questions.forEach((q, i) => {
			if (!bySection.has(q.section)) bySection.set(q.section, []);
			bySection.get(q.section).push([q, i]);
		});
		for (const sec of check.sections) {
			const qs = bySection.get(sec.id);
			if (!qs?.length) continue;
			const head = `${e(`${sec.id} · ${sec.title}`)} <span class="tc-count">(${qs.length})</span>`;
			const desc = `<p class="tc-section-desc">${e(sec.description)}</p>`;
			const body = qs.every(([q]) => !q.choices || q.choices.kind === "info")
				? `<ul class="tc-info">${qs.map(([q]) => `<li>${e(q.text)}</li>`).join("")}</ul>`
				: qs.map(([q, i]) => this.#question(q, i, check)).join("");
			out.push(sec.collapsed
				? `<details class="tc-section" data-tc-section="${sec.id}"><summary class="tc-section-title">${head}</summary>${desc}${body}</details>`
				: `<section class="tc-section" data-tc-section="${sec.id}"><${h} class="tc-section-title">${head}</${h}>${desc}${body}</section>`);
		}
		const c = check.counts ?? {};
		if (c.handled) out.push(`<p class="tc-foot">${e(this.#fill(s.handled, this.#numbers(check, { count: c.handled })))}</p>`);
		if (c.writerNotes) out.push(`<p class="tc-foot">${e(this.#fill(s.writer_notes_left, this.#numbers(check, { count: c.writerNotes })))}</p>`);
		if (answerable) out.push(`<p class="tc-foot">${e(s.save_hint)}</p>`);
		out.push("</div>");
		return out.join("");
	};

	/** One answerable question card. */
	static #question(q, i, check) {
		const s = check.strings;
		const e = (x) => this.#esc(x);
		if (!q.choices || q.choices.kind === "info") return `<p class="tc-q-text">${e(q.text)}</p>`;
		const out = [`<div class="tc-q" data-tc-q="${e(q.id)}">`];
		if (q.text) out.push(`<p class="tc-q-text">${e(q.text)}</p>`);
		if (q.details?.length) out.push(`<ul class="tc-q-details">${q.details.map((d) => `<li>${e(d)}</li>`).join("")}</ul>`);
		if (q.writerText) {
			const label = q.writerLabel ? `<span class="tc-quote-label">${e(s[q.writerLabel] ?? "")}</span>` : "";
			out.push(`<blockquote class="tc-quote">${label}«${e(q.writerText)}»</blockquote>`);
		}
		out.push(`<div class="tc-answer">${this.#choices(q, i, check)}</div>`);
		out.push("<div class=\"tc-q-foot\">"
			+ `<label class="tc-comment"><span>${e(s.comment)}</span><textarea rows="1" data-tc-field="comment" data-tc-id="${e(q.id)}"></textarea></label>`
			+ `<button type="button" class="tc-skip" data-tc-action="skip" data-tc-id="${e(q.id)}">${e(s.skip)}</button></div>`);
		out.push("</div>");
		return out.join("");
	};

	/** A question's answer controls, by kind: text, tick, choose or table. */
	static #choices(q, i, check) {
		const s = check.strings;
		const e = (x) => this.#esc(x);
		const c = q.choices;
		const id = e(q.id);
		if (c.kind === "text") {
			const field = c.multiline
				? `<textarea rows="3" data-tc-field="text" data-tc-id="${id}"></textarea>`
				: `<input type="text" data-tc-field="text" data-tc-id="${id}">`;
			let html = `<label class="tc-field"><span>${e(c.label ?? "")}</span>${field}</label>`;
			if (c.check) {
				html += `<label class="tc-check"><input type="checkbox" data-tc-field="check" data-tc-id="${id}" data-tc-value="${e(c.check.id)}"`
					+ `${c.check.checked ? " checked" : ""}> ${e(c.check.label)}</label>`;
			}
			return html;
		}
		if (c.kind === "tick") {
			return `<label class="tc-check"><input type="checkbox" data-tc-field="tick" data-tc-id="${id}"> ${e(c.label ?? "")}</label>`;
		}
		if (c.kind === "choose") {
			return (c.options ?? []).map((o) => `<label class="tc-opt"><input type="radio" name="tcq-${i}" value="${e(o.id)}" `
				+ `data-tc-field="choice" data-tc-id="${id}"> ${e(o.label)}</label>`).join("")
				+ `<label class="tc-say" data-tc-say="${id}" hidden><span data-tc-say-label></span>`
				+ `<input type="text" data-tc-field="text" data-tc-id="${id}"></label>`;
		}
		if (c.kind === "table") {
			const options = `<option value="">${e(s.choose)}</option>`
				+ (c.options ?? []).map((o) => `<option value="${e(o.id)}">${e(o.label)}</option>`).join("");
			return `<table class="tc-table"><tbody>${(q.rows ?? []).map((r) => `<tr data-tc-row="${e(r.id)}">`
				+ `<td class="tc-row-label">${e(r.label)}</td>`
				+ `<td><select data-tc-field="choice" data-tc-id="${e(r.id)}">${options}</select>`
				+ `<input type="text" class="tc-row-say" data-tc-field="text" data-tc-row-say data-tc-id="${e(r.id)}" hidden></td></tr>`).join("")}`
				+ "</tbody></table>";
		}
		return "";
	};

	/** Puts a state's answers into the rendered controls. */
	static #apply(root, state) {
		for (const el of root.querySelectorAll("[data-tc-field]")) {
			const a = state.answers?.[el.dataset.tcId] ?? {};
			const field = el.dataset.tcField;
			if (field === "text") el.value = a.text ?? "";
			else if (field === "comment") el.value = a.comment ?? "";
			else if (field === "check") el.checked = a.choice ? a.choice === el.dataset.tcValue : el.defaultChecked;
			else if (field === "tick") el.checked = a.choice === "noted";
			else if (field === "choice") {
				if (el.type === "radio") el.checked = el.value === a.choice;
				else el.value = a.choice ?? "";
			}
		}
		const name = root.querySelector("[data-tc-name]");
		if (name) name.value = state.answeredBy ?? "";
	};

	/** Downloads a text file the browser builds in memory (works offline). */
	static #download(filename, text, type) {
		const blob = new Blob([text], { type });
		const a = document.createElement("a");
		a.href = URL.createObjectURL(blob);
		a.download = filename;
		document.body.appendChild(a);
		a.click();
		a.remove();
		setTimeout(() => URL.revokeObjectURL(a.href), 1000);
	};

	/** {placeholder} filling (the literal token stays when a value is missing). */
	static #fill(template, values) {
		return String(template ?? "").replace(/\{(\w+)\}/g, (whole, key) => (values[key] ?? whole));
	};

	/** A number's plural blanks from the check's data: {s}, {was_were} … */
	static #numbers(check, values) {
		const out = { ...values };
		for (const [name, n] of Object.entries(values)) {
			if (typeof n !== "number") continue;
			for (const [k, pair] of Object.entries(check.plurals ?? {})) {
				if (k.startsWith("_") || !Array.isArray(pair)) continue;
				out[name === "count" ? k : `${name}_${k}`] = n === 1 ? pair[0] : pair[1];
			}
		}
		return out;
	};

	/** HTML-escapes text (the same five characters as Utils.EscapeHtml). */
	static #esc(s) {
		return String(s ?? "")
			.replace(/&/g, "&amp;")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;")
			.replace(/"/g, "&quot;")
			.replace(/'/g, "&#39;");
	};
}

// Node export hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { TemplateCheckPanel };
