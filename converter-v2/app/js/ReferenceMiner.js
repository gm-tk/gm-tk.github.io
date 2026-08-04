/**
 * ReferenceMiner.js
 * ===========================================================================
 * WHAT THIS FILE DOES (ROUND 249 — the REFERENCE-MODULE feature):
 * Three jobs, all in service of letting the person converting a module SEE
 * and STEER which already-built module their conversion inherits its page
 * structure from (the "reference module"):
 *
 *  1. PreviewSuggestion — the UPLOAD-TIME advisory: given the uploaded
 *     filenames (and optionally the extracted front-matter blocks), detect
 *     the module code and name the SUGGESTED reference module (the nearest
 *     already-built relative in the library index) plus the registry
 *     resolution path. Display-only — it changes nothing about the
 *     conversion. App.js calls THIS (never ModuleResolver directly — the
 *     entry-parity gate forbids prep calls in entry files; this wrapper
 *     keeps the advisory out of the entry's own source).
 *
 *  2. Distil — the REFERENCE-HTML miner: when no suitable library module
 *     exists, the person can upload the finished HTML pages of a module
 *     they want to emulate. This mines the Style-Anchor tracked fields
 *     (the SAME page-level field vocabulary Style_Anchor_Registry.json
 *     resolves: body_class, level_attr, idoc_host, footer_class,
 *     acknowledgements, module_code chip format, h1_count, menu_type,
 *     menu_button_tooltip, footer_links, page_model, plus template_phase)
 *     out of those pages with plain text/regex scanning (no DOM — this
 *     must run identically in the browser and the node harness), and
 *     packages them as a DISTILLED TEMPLATE object. The conversion applies
 *     the mined fields live (see Overlay), and the distilled JSON ships as
 *     an extra output file ({CODE}_reference-template.json) to send to
 *     Chris, so the reference module can be added to PageForge's templated
 *     modules for future conversions.
 *
 *  3. Overlay — applies a distilled template's MINED fields onto the run's
 *     resolved rules. Pattern fields ({overview, lesson} objects) are
 *     rebuilt as WHOLE objects (mined roles over the existing resolved
 *     values), honouring the resolver's never-half-merge rule.
 *
 * HONEST SCOPE: this mines the PAGE-LEVEL structural profile only — the
 * fields the live resolver actually consumes. The element-level granular
 * ladder (Granular_Scaffold_Registry / Module_Structure_Index) still comes
 * from the Python registry rebuild once the reference module's HTML joins
 * the library; the distilled file says so in its how_to_use note.
 *
 * DATA FLAG: Emit_Templates.reference_module (enabled) · ENV: REFMOD_OFF
 * (both checked by the caller, ModuleResolver.PrepareRun — this file just
 * does the work it is asked to do).
 * NEVER IN THIS FILE: `if (moduleCode === "…")` — module-specific knowledge
 * lives in the registries.
 * ===========================================================================
 */

class ReferenceMiner {

	// the corpus module-code shape (mirrors ModuleResolver.DetectModuleCode)
	static #CODE_RX = /\b([A-Z]{2,6}\d{2,4}(?:RR)?)\b/;

	/**
	 * UPLOAD-TIME advisory for the browser UI: detect the module code from
	 * the uploaded material and name the suggested reference module.
	 * Display-only — never mutates anything, never part of the conversion.
	 *
	 * @param {Object} options
	 * @param {string[]} options.filenames - the uploaded .docx filenames
	 * @param {Object[]} [options.allBlocks] - extracted blocks (optional —
	 *                   lets the front-matter "Module code:" line decide
	 *                   when the filenames carry no code)
	 * @returns {{code: ?string, suggestion: ?Object, path: ?string}} the
	 *   detected code, the SuggestReference result (see
	 *   PrecedenceResolver.SuggestReference), and the registry resolution
	 *   path ("defaults → subject … → level …") for display
	 */
	static PreviewSuggestion({ filenames = [], allBlocks = [] } = {}) {
		const stub = { AddNote() { } };   // swallow advisory-time notes
		let code = null;
		try {
			code = ModuleResolver.DetectModuleCode({ filenames, allBlocks, run: stub });
		} catch { /* detection is advisory — never let it break the UI */ }
		if (!code) return { code: null, suggestion: null, path: null };
		const probe = { AddNote() { } };
		try { ModuleResolver.Resolve(code, probe); } catch { /* registry unavailable */ }
		let suggestion = null;
		try {
			suggestion = (typeof PrecedenceResolver !== "undefined")
				? PrecedenceResolver.SuggestReference(code) : null;
		} catch { /* advisory only */ }
		return { code, suggestion, path: probe.resolutionPath ?? null };
	};

	/**
	 * Every module code the library index knows, with its classification —
	 * the pool the UI's "pick a different reference module" list shows.
	 *
	 * @returns {Object[]} sorted [{code, subject, template_type, …}]
	 */
	static ListLibraryCodes() {
		const meta = (typeof DataService !== "undefined"
			&& DataService.Data?.ModuleStructureIndex?.module_meta) || {};
		return Object.keys(meta).sort().map((c) => ({ code: c, ...meta[c] }));
	};

	/**
	 * Mines the Style-Anchor tracked fields out of uploaded reference HTML
	 * pages and packages them as a distilled template. Never throws; a
	 * field it cannot determine confidently is listed in `unmined` and NOT
	 * applied (the resolved defaults stay), so a partial upload can never
	 * invent structure.
	 *
	 * @param {Object[]} files - [{name, text}] the uploaded .html pages
	 * @param {ConversionRun} [run] - for surfacing notes (optional)
	 * @returns {?Object} { referenceCode, rules, unmined, notes, file } —
	 *   `rules` holds ONLY the mined fields (registry vocabulary);
	 *   `file` is the full distilled-template object to serialise for Chris.
	 *   Returns null when no readable .html page was supplied.
	 */
	static Distil(files, run) {
		const pages = (files ?? []).filter((f) =>
			/\.html?$/i.test(f?.name ?? "") && typeof f?.text === "string" && f.text.length);
		if (!pages.length) {
			run?.AddNote("warn", "ReferenceMiner",
				"No readable .html reference pages were supplied — reference mining skipped.");
			return null;
		}

		// ---- reference code + page roles ------------------------------------
		// NB: underscores are word characters, so a filename like
		// "OSSC301_0_0.html" defeats a plain \b match — separators are folded
		// to spaces before matching.
		let refCode = null;
		for (const p of pages) {
			const m = p.name.toUpperCase().replace(/[_\-.]/g, " ").match(this.#CODE_RX);
			if (m) { refCode = m[1]; break; }
		}
		// role: overview = the 0/0.0 page by any known filename form
		// ({code}_0_0.html · {code}-00.html · {code}-0.0.html); no numeric key
		// on ANY page → the first page stands in as the overview.
		const keyed = pages.map((p) => ({ ...p, key: this.#pageKey(p.name) }));
		let overviews = keyed.filter((p) => p.key === 0);
		let lessons = keyed.filter((p) => p.key !== 0 && p.key != null);
		if (!overviews.length && keyed.every((p) => p.key == null)) {
			overviews = [keyed[0]];
			lessons = keyed.slice(1);
		}

		const notes = [];
		const unmined = [];
		const rules = {};
		const mineRole = (list, fn) => {
			for (const p of list) {
				const v = fn(p.text, p.name);
				if (v != null) return v;
			}
			return null;
		};
		const pattern = (field, fn) => {
			const ov = mineRole(overviews, fn);
			const ls = mineRole(lessons, fn);
			if (ov == null && ls == null) { unmined.push(field); return; }
			const out = {};
			if (ov != null) out.overview = ov;
			if (ls != null) out.lesson = ls;
			else notes.push(`${field}: no lesson page uploaded — the lesson value stays at the resolved default.`);
			rules[field] = out;
		};
		const scalar = (field, fn) => {
			const v = mineRole(keyed, fn);
			if (v == null) { unmined.push(field); return; }
			rules[field] = v;
		};

		// ---- the tracked fields, mined --------------------------------------
		scalar("template_phase", (t) => this.#attr(this.#tag(t, "html"), "template"));
		scalar("level_attr", (t) => {
			const v = this.#attr(this.#tag(t, "html"), "level") ?? this.#attr(this.#tag(t, "body"), "level");
			return v == null ? null : (v.trim() === "" ? "empty" : v.trim());
		});
		scalar("body_class", (t) => this.#attr(this.#tag(t, "body"), "class"));
		scalar("idoc_host", (t) => /([a-z0-9-]+)\.desire2learn\.com/i.exec(t)?.[1] ?? null);
		scalar("footer_class", (t) => {
			const i = t.indexOf("id=\"footer\"");
			if (i < 0) return null;
			return /<ul\b[^>]*\bclass="([^"]*)"/i.exec(t.slice(i, i + 2000))?.[1] ?? null;
		});
		rules.acknowledgements = keyed.some((p) => /class="[^"]*\backs\b/.test(p.text)) ? "yes" : "no";
		rules.page_model = pages.length > 1 ? "multi-file" : "single-file";
		if (pages.length === 1) {
			notes.push("page_model: derived from ONE uploaded page — upload every page of the reference module for an accurate multi-file/single-file reading.");
		}
		pattern("module_code", (t) => this.#chipFormat(t, refCode));
		pattern("h1_count", (t) => this.#headerH1Count(t));
		pattern("menu_type", (t) => this.#menuType(t));
		pattern("menu_button_tooltip", (t) => this.#menuTooltip(t));
		pattern("footer_links", (t) => this.#footerLinks(t));

		run?.AddNote("info", "ReferenceMiner",
			`Distilled a reference template from ${pages.length} uploaded page(s)`
			+ `${refCode ? ` of ${refCode}` : ""}: ${Object.keys(rules).length} field(s) mined`
			+ `${unmined.length ? `, ${unmined.length} left at the resolved defaults (${unmined.join(", ")})` : ""}.`);

		// ---- the distilled-template file object (send to Gavin) -------------
		const file = {
			kind: "pageforge_reference_template",
			generated: new Date().toISOString().slice(0, 10),
			app_version: (typeof Config !== "undefined") ? Config.AppVersion : null,
			reference_code: refCode,
			source_files: pages.map((p) => p.name),
			rules,
			unmined_fields: unmined,
			module_meta_guess: this.#metaGuess(refCode),
			notes,
			how_to_use: "Send this file to Gavin. It holds the reference module's PAGE-LEVEL "
				+ "structural profile, mined from its finished HTML, in the Style_Anchor_Registry "
				+ "field vocabulary — ready to be added to PageForge's templated modules so future "
				+ "conversions can inherit from this module by code. The element-level detail "
				+ "(the granular scaffold ladder) still comes from the registry rebuild once this "
				+ "module's HTML pages join the module library.",
		};
		return { referenceCode: refCode, rules, unmined, notes, file };
	};

	/**
	 * Applies a distilled template's mined fields onto the run's resolved
	 * rules. A pattern field is rebuilt as a WHOLE object — the existing
	 * resolved pattern with the mined role values over it — honouring the
	 * resolver's rule that pattern fields are never half-merged into
	 * structures no real module has.
	 *
	 * @param {ConversionRun} run - the run being prepared (mutated)
	 * @param {Object} distilled - a Distil() result
	 * @returns {number} how many fields were applied
	 */
	static Overlay(run, distilled) {
		const rr = run?.resolvedRules;
		if (!rr || !distilled?.rules) return 0;
		let applied = 0;
		for (const [k, v] of Object.entries(distilled.rules)) {
			if (v == null) continue;
			if (typeof v === "object" && !Array.isArray(v)) {
				rr[k] = Object.assign(structuredClone(rr[k] ?? {}), v);
			} else {
				rr[k] = v;
			}
			applied++;
		}
		return applied;
	};

	// =======================================================================
	// mining helpers (plain text/regex — identical in browser + node)
	// =======================================================================

	/** The opening tag string for `name` ("<html …>"), or null. */
	static #tag(text, name) {
		return new RegExp(`<${name}\\b[^>]*>`, "i").exec(text)?.[0] ?? null;
	};

	/** One attribute's value out of an opening-tag string, or null. */
	static #attr(tag, name) {
		if (!tag) return null;
		return new RegExp(`\\b${name}="([^"]*)"`, "i").exec(tag)?.[1] ?? null;
	};

	/**
	 * Numeric page key from a filename: 0 = the overview. Reads all three
	 * filename eras — the library {code}_{lesson}_{part}.html form, the
	 * legacy {code}-NN(.S).html dash form, and the gold {code}-L.S.html —
	 * mirroring the gate tools' shared page-key idiom.
	 */
	static #pageKey(name) {
		let m = /_(\d+)_(\d+)\.html?$/i.exec(name);
		if (m) return parseFloat(`${m[1]}.${m[2]}`);
		m = /[-.](\d+)\.(\d+)\.html?$/i.exec(name);
		if (m) return parseFloat(`${m[1]}.${m[2]}`);
		m = /-(\d+)\.html?$/i.exec(name);
		if (m) return parseInt(m[1], 10);
		return null;
	};

	/** The #header region (everything before the #body div). */
	static #header(text) {
		const i = text.indexOf("id=\"body\"");
		return i < 0 ? text : text.slice(0, i);
	};

	/**
	 * The module-code chip's registry value: "full-code" (the chip shows
	 * the module code), "decimal" (a lesson number like "2.0"), or the
	 * literal free text; null when the page has no chip.
	 */
	static #chipFormat(text, refCode) {
		const i = text.indexOf("id=\"module-code\"");
		if (i < 0) return null;
		const chunk = text.slice(i, i + 400);
		const inner = chunk.slice(chunk.indexOf(">") + 1, chunk.indexOf("</div>"));
		const label = inner.replace(/<[^>]*>/g, "").trim();
		if (!label) return null;
		if (refCode && label.toUpperCase() === refCode) return "full-code";
		if (/^\d+(?:\.\d+)?$/.test(label)) return "decimal";
		return label;
	};

	/** Title-h1 count in the header, excluding the module-code chip's h1. */
	static #headerH1Count(text) {
		const head = this.#header(text);
		if (!/<h1\b/i.test(head)) return null;
		const chipless = head.replace(/id="module-code"[\s\S]{0,400}?<\/div>/i, "");
		return String((chipless.match(/<h1\b/gi) ?? []).length);
	};

	/** The menu archetype: "tabs" | "simplified" | "none"; null = no header. */
	static #menuType(text) {
		const head = this.#header(text);
		const i = head.indexOf("id=\"module-menu-content\"");
		if (i < 0) return "none";
		const menu = head.slice(i);
		if (/nav-tabs|class="[^"]*\btabs\b/.test(menu)) return "tabs";
		if (/<h[45]\b|<li\b/i.test(menu)) return "simplified";
		return "none";
	};

	/** "yes" when the menu button carries a non-empty tooltip attribute. */
	static #menuTooltip(text) {
		const head = this.#header(text);
		const i = head.indexOf("id=\"module-menu-button\"");
		if (i < 0) return null;
		const tag = head.slice(i, head.indexOf(">", i) + 1);
		return /\btooltip="[^"]+"/.test(tag) ? "yes" : "no";
	};

	/** The footer-nav composition ("prev+next+home" vocabulary), or null. */
	static #footerLinks(text) {
		const i = text.indexOf("id=\"footer\"");
		if (i < 0) return null;
		const foot = text.slice(i);
		const tokens = [];
		if (/id="prev-lesson"/.test(foot)) tokens.push("prev");
		if (/id="next-lesson"/.test(foot)) tokens.push("next");
		if (/class="[^"]*\bhome-nav\b/.test(foot)) tokens.push("home");
		return tokens.length ? tokens.join("+") : null;
	};

	/**
	 * A best-effort module_meta shape for the distilled file — the fields
	 * Module_Structure_Index.module_meta carries. Copied from the library
	 * index when the code is already known there; otherwise derived from
	 * the code's own letters/digits with subject/template left for Chris.
	 */
	static #metaGuess(code) {
		if (!code) return null;
		const known = (typeof DataService !== "undefined"
			&& DataService.Data?.ModuleStructureIndex?.module_meta?.[code]);
		if (known) return { ...known, note: "already in the library index" };
		const m = /^([A-Za-z]+)(\d*)/.exec(code) ?? [null, code, ""];
		const [, pre, digits] = m;
		return {
			subject: null, template_type: null, prefix: pre,
			phase: digits ? pre + digits.slice(0, 1) : null,
			series: digits.length >= 2 ? pre + digits.slice(0, 2) : (digits ? pre + digits : null),
			dev_order: digits ? parseInt(digits, 10) : null,
			note: "subject/template_type to be confirmed when adding to the registries",
		};
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { ReferenceMiner };
