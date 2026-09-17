/**
 * SkeletonBuilder.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Pipeline stage [7] — the LAST stage before a page becomes a finished HTML
 * document. Takes ContentConverter's already-built body HTML and wraps it in
 * the full page shell: doctype, <html> attributes, <head>, the #header (the
 * module-code "chip", the title <h1>(s), the menu-open button, and the menu
 * content itself), #body, and #footer.
 *
 * WHAT "SKELETON" MEANS HERE:
 * The "skeleton" (sometimes called the page "scaffold") is the structural
 * shell every module page shares — the same doctype/head/header/footer
 * wiring regardless of which subject or lesson the page happens to be. This
 * file builds that shared shell; ContentConverter and its collaborators
 * build what goes INSIDE it.
 *
 * WHY DATA-DRIVEN, NOT HAND-CODED PER MODULE:
 * Every shape emitted here comes from Emit_Templates.json, filled in using
 * values already resolved from the module's registry (its subject, phase,
 * template type, and so on) — there is no separate skeleton file per module
 * or per series to copy from, and no per-module special-casing in this
 * file's code. A module "inherits" its skeleton purely by matching the same
 * resolved registry values as other modules like it.
 *
 * NON-NEGOTIABLES HONOURED HERE (all sourced from data):
 *  - never emit stickyNav.js, never emit inline embedded_css
 *  - iDoc host is ALWAYS tekura (registry value, policy-fixed)
 *  - <span> wrappers ONLY inside header <h1> titles
 *  - registry value "—" / "n/a" / "absent" = element absent by design
 *
 * WHEN TO WORK HERE:
 * When the page SHELL itself needs to change — a new <head> tag, a
 * different #header/#footer shape, a new title or menu layout variant. If
 * the change is about what appears INSIDE the body content, it belongs in
 * ContentConverter or one of its collaborator builder files instead.
 * ===========================================================================
 */

class SkeletonBuilder {

	/**
	 * Builds one complete HTML page: everything from <!DOCTYPE html> to
	 * </html>, wrapping ContentConverter's already-built body HTML in the
	 * shared page shell described in the file banner above.
	 *
	 * HOW: every piece (the <html> attributes, <head>, #header, #footer) is
	 * produced by filling an Emit_Templates.json string template with values
	 * resolved from the module's registry rules (run.resolvedRules) — this
	 * method itself carries no per-module logic, only template selection
	 * and filling.
	 *
	 * @param {Object} options
	 * @param {Object} options.page - the PageSplitter page being built
	 * @param {Object} options.content - ContentConverter's result for this
	 *                  page: { bodyHtml, menu, titleBar }
	 * @param {ConversionRun} options.run - resolved rules + module identity
	 * @param {string} options.acksHtml - the acknowledgements block HTML
	 *                  ("" on lesson pages; only the overview/first page
	 *                  receives the real block)
	 * @param {boolean} options.isFinal - true on the module's last page
	 *                  (selects the footer_links "final" pattern)
	 * @param {string} [options.prevHref] - the previous page's output
	 *                  filename, used for the footer's "previous" link
	 * @param {string} [options.nextHref] - the next page's output filename,
	 *                  used for the footer's "next" link
	 * @returns {string} the full HTML document, ready to write to disk
	 */
	static BuildPage({ page, content, run, acksHtml = "", isFinal = false, prevHref = "", nextHref = "" }) {
		const tpl = DataService.Data.EmitTemplates;
		const rules = run.resolvedRules;
		const pageType = page.isOverview ? "overview" : "lesson";

		// ---- <html> attributes -------------------------------------------
		// level: the map knows empty/absent/prm/ech; any other value renders
		// literally (the _rule in the data file)
		const levelMap = tpl.skeleton.level_attr_map;
		const levelAttr = levelMap[rules.level_attr] !== undefined
			? levelMap[rules.level_attr]
			: ` level="${Utils.EscapeHtml(rules.level_attr ?? "")}"`;
		// THE TEMPLATE-ATTRIBUTE PRESET RULE (ROUND 221 — module ENGJ403, Chris).
		// The <html template="…"> attribute (which decides the stylesheet the
		// iDoc host loads) must follow the PRESET module-level rule — level
		// digit 1→"1-3", 2→"4-6", 3→"7-8", 4→"9-10", 5→"NCEA" — and this rule
		// SUPERSEDES sibling inheritance for THIS ATTRIBUTE ONLY. ENGJ403
		// inherited template="4-6" from its series sibling ENGJ402, whose own
		// human-built value is itself wrong (the human ENGJ403 ships "9-10");
		// Chris's directive: the level preset always wins here, regardless of
		// what any previously-developed sibling carries. Everything ELSE
		// (menu conventions, groupKey lookups, page model, chip forms…) keeps
		// the sibling-emulation rule untouched — rules.template_phase itself
		// is NOT changed, only the emitted attribute value. Scope is measured
		// (232/305 golds already follow the preset): 3-digit codes with a
		// level digit 1-5, subject in the preset list (families whose code
		// digit is NOT a curriculum level — BLL, HPFUN, OS-shortcourse, XMES,
		// MXEO, CEDK — are excluded), and a resolved "combo" value is
		// preserved (combo marks a combined-cohort template decision, not a
		// level band). Data: skeleton.template_phase_presets.
		// Env toggle: TPLPRESET_OFF (reverts to the pure sibling value).
		let phaseForAttr = rules.template_phase;
		const tppCfg = tpl.skeleton.template_phase_presets;
		const tppOn = tppCfg && tppCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.TPLPRESET_OFF);
		if (tppOn) {
			const tm = String(run.moduleCode || "").match(
				new RegExp(tppCfg.code_pattern ?? "^([A-Z]+)([1-5])\\d{2}$"));
			const preset = tm && (tppCfg.subjects ?? []).includes(tm[1])
				? (tppCfg.by_level_digit ?? {})[tm[2]] : null;
			if (preset && preset !== phaseForAttr
				&& !(tppCfg.preserve_values ?? ["combo"]).includes(phaseForAttr)) {
				if (!run._tppNoted) {
					run._tppNoted = true;
					run.AddNote("info", "SkeletonBuilder",
						`template attribute "${phaseForAttr}" overridden to the level-${tm[2]} preset "${preset}" (template_phase_presets — the module-level rule outranks sibling inheritance for this attribute only).`);
				}
				phaseForAttr = preset;
			}
		}
		// THE UNKNOWN-SUBJECT DIGIT FALLBACK (ROUND 238 — Dev-Feedback R1
		// Family A, module SCCH302). A subject NOT in the preset list above
		// (a brand-new subject the registry has never seen) used to ship an
		// EMPTY template attribute — and the iDoc host loads the stylesheet
		// by this attribute, so the page rendered unstyled. When the module
		// resolved NO template_phase at all (phaseForAttr empty — a pure
		// fallback: every module with a real resolved value, and every
		// digit-is-not-a-level family, is untouched BY CONSTRUCTION), the
		// code's own level digit supplies the band via the same
		// by_level_digit map (SCCH302 → 3 → "7-8", exactly the value the
		// reference developer confirmed correct). A code that does not match
		// code_pattern (FUN-shaped codes, 4-digit codes) still ships empty —
		// MEASURED: the FUN families' template values are genuinely MIXED
		// (10 combo vs 5 NCEA bases), so no confident fallback exists there
		// and the rule refuses to guess. prefix_overrides (r224) and
		// cohort_overrides (r231) below still outrank this fallback.
		// Data: skeleton.template_phase_presets.unknown_subject_digit_fallback.
		// Env toggle: TPLFALLBACK_OFF (reverts to the empty attribute).
		const usfCfg = tppCfg && tppCfg.unknown_subject_digit_fallback;
		const usfOn = usfCfg && usfCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.TPLFALLBACK_OFF);
		if (usfOn && (phaseForAttr == null || phaseForAttr === "")) {
			const um = String(run.moduleCode || "").match(
				new RegExp(tppCfg.code_pattern ?? "^([A-Z]+)([1-5])\\d{2}$"));
			if (um && !(tppCfg.subjects ?? []).includes(um[1])) {
				const fb = (tppCfg.by_level_digit ?? {})[um[2]];
				if (fb) {
					if (!run._tppNoted) {
						run._tppNoted = true;
						run.AddNote("info", "SkeletonBuilder",
							`unknown subject "${um[1]}" resolved no template — the code's level digit ${um[2]} supplies template="${fb}" (unknown_subject_digit_fallback; env TPLFALLBACK_OFF reverts to the empty attribute).`);
					}
					phaseForAttr = fb;
				}
			}
		}
		// THE CODE-PREFIX TEMPLATE OVERRIDE (ROUND 224 — the BLL200 exception,
		// Chris). Some families' code digits are NOT curriculum levels, so the
		// digit preset excludes them — but the design team still fixes their
		// template by an explicit exception list. BLL2xx modules are actually
		// PHASE 1 → template="1-3" (NOT the "4-6" a mis-built sibling would
		// hand down); BLLR2xx ARE phase 2 and keep "4-6" (guard entry — a
		// "BLLR…" code can never startsWith "BLL2", but the r218 "BLLR is NOT
		// BLL" startswith trap earns the explicit fence). LONGEST matching
		// prefix wins; null = explicitly no override. Unconditional: outranks
		// sibling inheritance AND the digit preset; preserve_values does not
		// apply. Data: skeleton.template_phase_presets.prefix_overrides.
		// Env toggle: TPLPREFIX_OFF (independent of TPLPRESET_OFF).
		const poCfg = tppCfg && tppCfg.prefix_overrides;
		const poOn = poCfg && poCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.TPLPREFIX_OFF);
		if (poOn) {
			const codeStr = String(run.moduleCode || "");
			const poKey = Object.keys(poCfg.map ?? {})
				.filter(k => !k.startsWith("_") && codeStr.startsWith(k))
				.sort((a, b) => b.length - a.length)[0];
			const poVal = poKey !== undefined ? (poCfg.map ?? {})[poKey] : undefined;
			if (poVal != null && poVal !== phaseForAttr) {
				if (!run._tppNoted) {
					run._tppNoted = true;
					run.AddNote("info", "SkeletonBuilder",
						`template attribute "${phaseForAttr}" overridden to "${poVal}" (template_phase_presets.prefix_overrides — the "${poKey}" exception list outranks sibling inheritance and the level preset).`);
				}
				phaseForAttr = poVal;
			}
		}
		// THE LANGUAGES COMBO COHORT (ROUND 231 — Change Ledger CL-0033, Chris).
		// Every page of a Languages-cohort module (doc-14 §14.1: the six
		// languages × FUN + non-FUN code prefixes — CHIFUN…SPAFUN, CHI…SPA)
		// ships template="combo" on <html>; the sub-type still comes from the
		// <body> class. UNCONDITIONAL within the cohort: outranks sibling
		// inheritance AND the digit preset (preserve_values does not apply —
		// the r224 semantics), applied after prefix_overrides (no key overlap).
		// The corpus holds ZERO Languages dirs today (census, round 231), so
		// this is an inert forward-looking GUARANTEE (the r224/r230 class):
		// without it a fresh Languages code would ship the TEDC-style EMPTY
		// attribute — no registry row, no sibling ever resolves "combo" for it.
		// Kept separate from prefix_overrides so each fix reverses
		// independently (§2). Data:
		// skeleton.template_phase_presets.cohort_overrides.
		// Env toggle: LANGCOMBO_OFF (independent of TPLPRESET/TPLPREFIX_OFF).
		const coCfg = tppCfg && tppCfg.cohort_overrides;
		const coOn = coCfg && coCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.LANGCOMBO_OFF);
		if (coOn) {
			const codeStr = String(run.moduleCode || "");
			const coVal = coCfg.value ?? "combo";
			if ((coCfg.prefixes ?? []).some((p) => codeStr.startsWith(p))
				&& coVal !== phaseForAttr) {
				if (!run._tppNoted) {
					run._tppNoted = true;
					run.AddNote("info", "SkeletonBuilder",
						`template attribute "${phaseForAttr}" overridden to "${coVal}" (template_phase_presets.cohort_overrides — the Languages cohort ships combo, CL-0033).`);
				}
				phaseForAttr = coVal;
			}
		}
		// THE LAST-RESORT TEMPLATE DEFAULT (ROUND 245 — Chris, the FRNO901
		// developer test; the r238 Family-A class completed).
		//
		// FRNO901 is a brand-new subject: no registry row, no gold sibling, and
		// its code digit 9 is not a curriculum level, so code_pattern never
		// matches and the r238 unknown_subject_digit_fallback rightly declines
		// to guess. Every OTHER universal field resolved correctly through the
		// r238 evidence floor — but the template attribute shipped EMPTY, and
		// the iDoc host loads the page stylesheet BY that attribute, so the page
		// renders completely unstyled. That is the same Prio-high failure the
		// reference developer reported for SCCH302, reached by another route.
		//
		// After every other rule has had its say, a still-empty attribute takes
		// the configured value. A LAST RESORT, never a preference: unreachable
		// BY CONSTRUCTION for any module that resolved anything at all, and
		// MEASURED zero-blast — not one page of the shipped corpus carries
		// template="" today, so this changes no existing byte (the r224/r231
		// forward-guarantee class). The run carries a loud note because a
		// default only holds until the developer builds the first proof, which
		// then becomes the templated reference future conversions inherit from.
		// Data: skeleton.template_phase_presets.last_resort_default.
		// Env toggle: TPLDEFAULT_OFF (reverts to the empty attribute).
		const lrdCfg = tppCfg && tppCfg.last_resort_default;
		const lrdOn = lrdCfg && lrdCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.TPLDEFAULT_OFF);
		if (lrdOn && (phaseForAttr == null || phaseForAttr === "")) {
			const lrdVal = lrdCfg.value ?? "combo";
			if (!run._tplDefaultNoted) {
				run._tplDefaultNoted = true;
				run.AddNote("warn", "SkeletonBuilder",
					`No template could be resolved for "${run.moduleCode}" — no registry row, no developed sibling, and its code carries no level digit. Defaulting to template="${lrdVal}" so the page loads styled (last_resort_default). Once the first proof of this module is developed, add it as the templated reference so future conversions inherit the real value.`);
			}
			phaseForAttr = lrdVal;
		}

		const templateAttr = tpl.skeleton.template_attr_map[phaseForAttr]
			?? phaseForAttr ?? "";
		if (!tpl.skeleton.template_attr_map[phaseForAttr]) {
			run.AddNote("warn", "SkeletonBuilder",
				`template_phase "${phaseForAttr}" has no template_attr_map entry — emitted literally.`);
		}

		// ---- <head> ---------------------------------------------------------
		const code = run.moduleCode ?? "MODULE";
		const title = pageType === "overview"
			? Utils.FillTemplate(tpl.skeleton.title_patterns.overview, {
				code, englishTitle: SkeletonBuilder.#englishOf(content.titleBar.english, content.titleBar.teReo, tpl) || run.englishTitle || "",
			}).trim()
			: Utils.FillTemplate(tpl.skeleton.title_patterns.lesson, {
				code, lesson: page.lessonLabel ?? "",
			}).trim();

		// iDoc host: ALWAYS tekura by policy; registry "none" = no script line
		const idocScript = rules.idoc_host && rules.idoc_host !== "none"
			? Utils.FillTemplate(tpl.skeleton.idoc_script, { idocHost: rules.idoc_host })
			: "";

		const head = Utils.FillTemplate(tpl.skeleton.head, {
			title: Utils.EscapeHtml(title),
			idocScript,
		});

		// ---- header -----------------------------------------------------------
		const header = this.#buildHeader({ page, content, run, pageType });

		// ---- footer -----------------------------------------------------------
		// When this page actually built an INQUIRY layout (content.inquiryActive), use the inquiry-specific footer nav CSS class instead of this page type's default.
		const inqCfg = tpl.body_region?.inquiry_tabs;
		const footer = this.#buildFooter({ run, pageType, isFinal, prevHref, nextHref,
			footerClassOverride: content.inquiryActive && inqCfg ? inqCfg.footer_class : null,
			// A CED-subject inquiry page whose registry produced no footer links at all (a
			// single-file CED module has an empty footer by default) falls back instead to a
			// fixed home/prev/next nav shell so navigation never disappears. Scoped to
			// content.cedInquiry — BLL-family inquiry pages are untouched.
			forceLinks: content.cedInquiry && inqCfg ? inqCfg.footer_nav_links : null });

		// ---- body MODE: canonical class token order + language/translation
		// attrs, composed by the TemplateModeResolver from the registry's
		// body_class (env TEMPLATEMODE_OFF reverts this composition byte-identically
		// to the plain un-composed class list).
		const mode = TemplateModeResolver.Resolve(rules.body_class, run);
		// When this page actually built an INQUIRY layout, force the body class to the inquiry container shell ("inquiry container-fluid").
		if (content.inquiryActive && inqCfg) {
			mode.bodyClass = inqCfg.body_class || "inquiry container-fluid";
		} else if (inqCfg && inqCfg.body_class_requires_build !== false
			&& !(typeof process !== "undefined" && process.env && process.env.INQBODY_OFF)
			&& /\binquiry\b/.test(mode.bodyClass)) {
			// The "inquiry" body-class token must only appear on a page that ACTUALLY
			// built the inquiry layout — not merely because the page happens to belong
			// to a subject whose registry default includes it. The module registry
			// stamps "container-fluid inquiry" as a whole-SUBJECT default (ConnectED,
			// Blended Literacy, the *WHA subjects), so every lesson page in those
			// subjects would otherwise inherit the "inquiry" token even on pages that
			// never build the inquiry crumbs/landing panel. The correct target shape
			// ships "inquiry" ONLY on the page that actually built it, and plain
			// "container-fluid" on every other page of the same module. So: when this
			// page did NOT build an inquiry layout (content.inquiryActive is false),
			// strip the "inquiry" token back out of the resolved body class, while
			// leaving any other modifier tokens (fundamentals/mathJax/reoTranslate)
			// untouched.
			// Data flag: body_region.inquiry_tabs.body_class_requires_build.
			// Env toggle: INQBODY_OFF (disables the strip, so a non-building page keeps
			// the raw subject-default body class, "inquiry" token and all).
			mode.bodyClass = mode.bodyClass.replace(/\binquiry\b/g, "").replace(/\s{2,}/g, " ").trim();
		}

		// ---- assemble -----------------------------------------------------------
		return [
			tpl.skeleton.doctype,
			SkeletonBuilder.#cohortHtmlClass(Utils.FillTemplate(tpl.skeleton.html_open, { levelAttr, templateAttr }), run, tpl),
			head,
			Utils.FillTemplate(tpl.skeleton.body_open, { bodyClass: mode.bodyClass, bodyAttrs: mode.bodyAttrs }),
			header,
			tpl.body_region.open,
			content.bodyHtml,
			tpl.body_region.close,
			footer,
			acksHtml,            // overview only — div.acks AFTER #footer (policy)
			tpl.skeleton.body_close,
			tpl.skeleton.html_close,
		].filter(Boolean).join("\n");
	};

	/**
	 * ROUND 319 (loop Round 6 — KB constraint 89): a code-prefix COHORT adds a class to
	 * the <html> tag — the X-prefixed learning-support modules ship `learningSupport`
	 * appended to the existing class list on every page (a CSS hook for the larger
	 * font; no font CSS is ever written). Data skeleton.html_class_cohorts (a list of
	 * { code_prefix, add_class } rules); env HTMLCOHORT_OFF. Returns the tag unchanged
	 * when off, when no rule matches, or when the class is already present.
	 */
	static #cohortHtmlClass(htmlOpen, run, tpl) {
		const cfg = tpl.skeleton?.html_class_cohorts;
		if (!cfg || cfg.enabled === false || !Array.isArray(cfg.rules)) return htmlOpen;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "HTMLCOHORT_OFF"]) return htmlOpen;
		const code = String(run?.moduleCode || "");
		let tag = htmlOpen;
		for (const r of cfg.rules) {
			if (!r || !r.code_prefix || !r.add_class || !code.startsWith(r.code_prefix)) continue;
			const m = /\bclass="([^"]*)"/.exec(tag);
			if (!m) { tag = tag.replace(/>$/, ` class="${r.add_class}">`); continue; }
			if (m[1].split(/\s+/).includes(r.add_class)) continue;
			tag = tag.replace(m[0], `class="${(m[1] + " " + r.add_class).trim()}"`);
		}
		return tag;
	}

	/** ROUND 321 — is header.mtk_titles on for this module (a reoTranslate body class)? */
	static #mtkOn(rules, tpl) {
		const mtk = tpl.header?.mtk_titles;
		if (!mtk || mtk.enabled === false) return false;
		if (typeof process !== "undefined" && process.env && process.env[mtk.env ?? "MTKTITLES_OFF"]) return false;
		return new RegExp(mtk.body_class ?? "reoTranslate", "i").test(String(rules?.body_class || ""));
	}

	/**
	 * ROUND 327 (the KB's title-casing rule — 01A "normalise a MULTI-WORD ALL-CAPS title",
	 * 10_CORPUS_VALIDATED_SCAFFOLDING §1). A header title whose words are ALL CAPS and
	 * number >= min_words renders in SENTENCE CASE: the first letter capitalised, the rest
	 * lowercase (macrons survive a lowercase), a token carrying a digit ("(US7121)") kept
	 * as the code it is. A single all-caps token ("STOMP") and any title already in
	 * sentence / title / mixed case are returned untouched. Returns { text, changed }.
	 * Data header.title_casing; env TITLECASE_OFF.
	 */
	static #titleCasing(title, tpl) {
		const cfg = tpl?.header?.title_casing;
		const t = String(title ?? "");
		if (!cfg || cfg.enabled === false || !t.trim()) return { text: t, changed: false };
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "TITLECASE_OFF"]) return { text: t, changed: false };
		const keepDigits = cfg.keep_tokens_with_digits !== false;
		const tokens = t.split(/\s+/).filter(Boolean);
		const words = tokens.filter((w) => /\p{L}/u.test(w) && !(keepDigits && /\d/.test(w)));
		if (words.length < (cfg.min_words ?? 2)) return { text: t, changed: false };
		if (!words.every((w) => w === w.toUpperCase() && w !== w.toLowerCase())) return { text: t, changed: false };
		if (!words.some((w) => w.replace(/[^\p{L}]/gu, "").length > 1)) return { text: t, changed: false };
		let lowered = t.replace(/\S+/g, (w) => (keepDigits && /\d/.test(w)) ? w : w.toLowerCase());
		lowered = lowered.replace(/\p{L}/u, (ch) => ch.toUpperCase());
		return { text: lowered, changed: lowered !== t };
	}

	/** ROUND 321 — does a title read as te reo Māori? A macron, or letters only from the
	 *  Māori alphabet (a e i o u h k m n p r t w g) — the round-153 lone-title guard's test. */
	static #looksMaori(s) {
		const t = String(s ?? "");
		if (/[\u0101\u0113\u012b\u014d\u016b\u0100\u0112\u012a\u014c\u016a]/.test(t)) return true;
		const letters = t.toLowerCase().replace(/[^a-z]/g, "");
		return letters.length > 0 && !/[bcdfjlqsvxyz]/.test(letters);
	}

	/**
	 * ROUND 316 (loop Round 3 — KB constraint 79, the lesson's own bilingual pair).
	 * Splits a lesson's OWN title into [first, second] when it carries one of the
	 * data separators, or returns null (no separator / feature off / an empty half).
	 * A leading module-code token (+ an optional dash or colon) is stripped first —
	 * the writer's "TRR102 –The vowel blend: ao | Te oropuare pūrua: ao" — because
	 * gold lesson pages never carry the code (0 of 1371). ORDER: in a module whose
	 * resolved body class matches reo_first_when_body_class (the reoTranslate
	 * Māori-medium modules) the Te Reo half goes first — the macron-bearing half,
	 * or the reo_fallback half when the macron cannot decide (PNR101 "Number 1 |
	 * Te tau 1"); everywhere else the halves keep the writer's order, the same rule
	 * the overview [TITLE BAR] splitter follows. Pure; never touches the overview.
	 */
	/** ROUND 358 — is header.te_reo_detect on (the Māori-alphabet title test; env REODETECT_OFF)? */
	static #teReoDetectOn(tpl) {
		const td = tpl?.header?.te_reo_detect;
		return !!td && td.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[td.env ?? "REODETECT_OFF"]);
	}

	/**
	 * ROUND 358 — the ENGLISH one of a module's two titles, BY LANGUAGE. The title-bar slots keep the writer's order
	 * (so the overview h1s do — 01A: 'the parts are emitted in the order the writer wrote them'; CEDW501's gold is Te Reo
	 * first), which means the 'english' slot holds the Māori half of a Māori-first pair. The two consumers that need the
	 * ENGLISH text — the <title> element (01A: English-only) and a lesson page's module-title FALLBACK (constraint 79 (5):
	 * 'the module English title') — ask here: when both titles exist and exactly one reads as Te Reo (Utils.LooksMaori),
	 * the other is returned; otherwise the first slot, exactly as before. Data header.te_reo_detect.english_slot_by_language.
	 */
	static #englishOf(a, b, tpl) {
		const td = tpl?.header?.te_reo_detect;
		if (!a || !b || !SkeletonBuilder.#teReoDetectOn(tpl) || td.english_slot_by_language === false
			|| (typeof process !== "undefined" && process.env && process.env.ENGSLOT_OFF)) return a;
		const ma = Utils.LooksMaori(a, td), mb = Utils.LooksMaori(b, td);
		return (ma && !mb) ? b : a;
	}
	static #lessonPair(title, run, rules, cfg) {
		if (!cfg || cfg.enabled === false || !title) return null;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "LESSONPAIR_OFF"]) return null;
		const seps = Array.isArray(cfg.separators) && cfg.separators.length ? cfg.separators : ["|"];
		let t = String(title);
		if (cfg.strip_module_code !== false && run.moduleCode) {
			const esc = String(run.moduleCode).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
			t = t.replace(new RegExp("^\\s*" + esc + "\\s*[\\-\u2013\u2014:]?\\s*", "i"), "");
		}
		let sep = seps.find((s) => t.includes(s));
		if (!sep) {
			// ROUND 358 (the autonomous loop's session-19 Round 2 — the diff miner's TITLE class). The SOFT separators
			// (a spaced dash / slash / colon — the overview splitters' own, data lesson_bilingual_pair.soft_separators)
			// split a lesson's OWN title only when exactly ONE half reads as Te Reo under Utils.LooksMaori (a macron
			// OR the Māori alphabet + phonotactics; header.te_reo_detect): "Ngā Whare - Housing" splits (ANZH104's
			// gold), "Time – Quarter Past" does not (MXFL103's). The pipe above stays unconditional (r316).
			// Env toggle: REODETECT_OFF (the whole soft path off — the r357 output).
			const td = DataService.Data.EmitTemplates.header?.te_reo_detect;
			const tdOn = td && td.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[td.env ?? "REODETECT_OFF"]);
			const softs = Array.isArray(cfg.soft_separators) ? cfg.soft_separators : [];
			if (tdOn) {
				for (const s of softs) {
					if (t.split(s).length !== 2) continue;                       // exactly ONE occurrence
					const p = t.slice(0, t.indexOf(s)), q = t.slice(t.indexOf(s) + s.length);
					if (!p.trim() || !q.trim()) continue;
					if (/[.!?]\s/.test(p.trim()) || /[.!?]\s/.test(q.trim())) continue;   // a multi-sentence title is not a pair (XMES101)
					if (Utils.LooksMaori(p, td) !== Utils.LooksMaori(q, td)) { sep = s; break; }
				}
			}
			if (!sep) return null;
		}
		const i = t.indexOf(sep);
		if (i < 0) return null;
		const clean = (s) => s.replace(/^[\s\-\u2013\u2014:|]+|[\s\-\u2013\u2014:|]+$/g, "").replace(/\s+/g, " ").trim();
		const a = clean(t.slice(0, i)), b = clean(t.slice(i + sep.length));
		if (!a || !b) return null;
		const reoCls = cfg.reo_first_when_body_class;
		const reoMode = !!reoCls && new RegExp(reoCls, "i").test(String(rules?.body_class || ""));
		const M = /[\u0101\u0113\u012b\u014d\u016b\u0100\u0112\u012a\u014c\u016a]/;   // āēīōū
		const ma = M.test(a), mb = M.test(b);
		if (!reoMode) {
			// ROUND 345 (Chris's D10-2): outside the reoTranslate modules the ENGLISH half goes
			// first — when exactly one half reads as Te Reo (a macron decides; when neither or both
			// halves carry one, the r321 #looksMaori alphabet test decides) it ships SECOND; both /
			// neither → the writer's order stands. Data lesson_bilingual_pair.english_first; env ENGFIRST_OFF.
			const ef = cfg.english_first;
			const efOn = !!ef && ef.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[ef.env ?? "ENGFIRST_OFF"]);
			if (efOn) {
				let reoA = ma, reoB = mb;
				if (ma === mb && /alphabet/.test(String(ef.reo_detect ?? "macron+alphabet"))) {
					reoA = SkeletonBuilder.#looksMaori(a); reoB = SkeletonBuilder.#looksMaori(b);
				}
				if (reoA && !reoB) return [b, a];
			}
			return [a, b];
		}
		if (mb && !ma) return [b, a];
		if (ma && !mb) return [a, b];
		return (cfg.reo_fallback ?? "second") === "second" ? [b, a] : [a, b];
	}

	/**
	 * Builds the #header element: the module-code "chip", the title <h1>
	 * line(s) (the WT's own English/Te Reo split, or an editorial fallback
	 * when no title could be derived), the menu-open button, and the menu
	 * content itself (built earlier by ContentConverter/MenuBuilder).
	 *
	 * HOW: the title count follows rules.h1_count (per pageType), except an
	 * overview page always emits every language its own [TITLE BAR] split
	 * actually produced (see the inline comment below for why). The menu
	 * "shell" — which HTML wrapper the already-built menu content drops
	 * into — is chosen from tpl.menu.shells by the menu's resolved
	 * "archetype", again driven entirely by data.
	 *
	 * @param {Object} options
	 * @param {Object} options.page - the PageSplitter page being built
	 * @param {Object} options.content - ContentConverter's result for this
	 *                 page: { bodyHtml, menu, titleBar }
	 * @param {ConversionRun} options.run - resolved registry rules + module identity
	 * @param {string} options.pageType - "overview" | "lesson"
	 * @returns {string} the #header element's HTML
	 */
	static #buildHeader({ page, content, run, pageType }) {
		const tpl = DataService.Data.EmitTemplates;
		const rules = run.resolvedRules;
		const parts = [tpl.header.open];

		// ---- #module-code: how the page code renders (pattern field) ------
		const mcValue = rules.module_code?.[pageType];
		const mcMap = tpl.header.module_code_value_map;
		let rendered = null;
		if (typeof mcValue === "string" && mcValue.startsWith("free-text")) {
			// registry form: 'free-text:"Module' → the literal after the colon
			let literal = mcValue.split(":")[1]?.replace(/"/g, "") ?? "";
			// MODULE-CODE-SHAPED LITERAL GUARD.
			// The shared template data for a family of modules can sometimes record a
			// module-code "chip" value as a hardcoded literal string that was really only
			// ever correct for ONE specific module in that family (its config was copied
			// from that module's own reference output, code and all). Every OTHER module
			// in the family then wrongly inherits and displays that literal, wrong code in
			// its overview chip. The fix: if the configured literal LOOKS like a module
			// code (it matches code_pattern, e.g. "XFUN02") but does NOT match the module
			// we're actually building right now (run.moduleCode), treat it as a mistake and
			// substitute this module's own real code instead. A genuine free-text literal
			// that isn't code-shaped ("Module", "Lesson 5") is left completely untouched.
			// This guard only affects the #header element, which the structural-comparison
			// gates strip of all text, so it can never move those gates either way.
			// Data flag: header.module_code_literal_guard.
			// Env toggle: CHIPLIT_OFF (disables the guard, so a mismatched literal chip
			// renders exactly as configured, wrong code and all).
			const litGuard = tpl.header.module_code_literal_guard;
			if (litGuard && litGuard.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.CHIPLIT_OFF)
				&& new RegExp(litGuard.code_pattern || "^[A-Z][A-Z-]*\\d+$").test(literal)
				&& run.moduleCode && literal !== run.moduleCode) {
				literal = run.moduleCode;
			}
			rendered = `${literal} ${page.lessonNumber ?? ""}`.trim();
		} else if (mcValue in mcMap && mcMap[mcValue] !== null) {
			rendered = Utils.FillTemplate(mcMap[mcValue], {
				code: run.moduleCode ?? "MODULE",
				lesson: page.lessonLabel ?? "0.0",
				lessonPadded: Utils.Pad2(page.lessonNumber ?? 0),
			});
		} else if (mcValue && !(mcValue in mcMap)) {
			run.AddNote("warn", "SkeletonBuilder",
				`module_code value "${mcValue}" has no module_code_value_map entry — element omitted; add the value to Emit_Templates.`);
		}
		// A "Module N - ..." title-bar prefix family: some modules' writers open the
		// document with a heading like "Module 3 - Some Title". For those, the OVERVIEW
		// page's #module-code chip is rendered as "Module {N}", where N comes from the
		// LAST DIGIT of the module's own code — not from the writer's title-bar prefix
		// number, which is sometimes simply a typo. run.modulePrefix is set upstream by
		// ContentConverter/PageAssembler once this pattern is detected.
		// Data flag: header.title_split.module_prefix_split.chip_from_code.
		if (run.modulePrefix && pageType === "overview"
			&& tpl.header.title_split?.module_prefix_split?.chip_from_code !== false) {
			const num = (run.moduleCode || "").match(/(\d)\D*$/)?.[1] ?? "";
			if (num) rendered = `Module ${num}`;
		}
		// A phonics-family OVERVIEW page whose chip resolved to the bare, non-numeric
		// word "Module" (i.e. the "Module N -" prefix handling above did NOT apply, so
		// there's still no digit in the chip) instead shows the module's own CODE in the
		// chip. Scoped to phonics overviews with a non-numeric chip, so it only fires on
		// that specific bare-"Module" shape and never touches the padded "Module N" chips
		// handled above. Data flag: header.title_split.phonics_overview_split.
		// Env toggle: PHONICSTITLE_OFF.
		if (content.titleBar?.phonicsLead && pageType === "overview" && rendered && !/\d/.test(rendered)) {
			rendered = run.moduleCode ?? rendered;
		}
		// null mapping ("absent"/"jsfilled/absent"/"—") = omit by design
		if (rendered !== null && rendered !== "") {
			parts.push(Utils.FillTemplate(tpl.header.module_code_element, {
				rendered: Utils.EscapeHtml(rendered),
			}));
		}

		// ---- the title h1s (the ONLY place <span> wraps a heading) --------
		const wanted = parseInt(rules.h1_count?.[pageType] ?? "1", 10) || 1;
		const titles = [];
		let pairCapsSet = null;   // ROUND 358: the halves of a lesson pair split from an ALL-CAPS title (sentence-cased per half below)
		if (pageType === "overview") {
			// the WT [TITLE BAR] split IS the derivable title count — emit EVERY
			// language it produced (English + Te Reo). The registry h1_count is a
			// per-group guess that UNDER-counts bilingual titles: measured 31
			// overviews where capping at h1_count=1 dropped the Te Reo title (vs
			// only 2 the other way). So the overview is not capped by the registry.
			if (content.titleBar.english) titles.push(content.titleBar.english);
			// A Te Reo (Māori-language) title line the writer placed directly next to the
			// [TITLE BAR] can sometimes actually carry a PAIR of Te Reo titles (a
			// colon-separated form) rather than one — the target output ships BOTH as
			// separate <h1> lines. content.titleBar.teReoLines is populated upstream by
			// ContentConverter's te_reo_line rule whenever this pair shape is detected,
			// and takes priority over the plain single teReo slot below.
			if (content.titleBar.teReoLines?.length) titles.push(...content.titleBar.teReoLines);
			else if (content.titleBar.teReo) titles.push(content.titleBar.teReo);
			// ROUND 321 (the MTK title source): in a reoTranslate module the overview shows
			// the Māori title first, English second (07C/07D rule 7) — decided by the text
			// (a macron, or the Māori alphabet), not by the slot, because the r212 metadata
			// fallback files the halves in payload order. Data header.mtk_titles; env MTKTITLES_OFF.
			if (SkeletonBuilder.#mtkOn(rules, tpl) && titles.length === 2 && SkeletonBuilder.#looksMaori(titles[1]) && !SkeletonBuilder.#looksMaori(titles[0])) titles.reverse();
			// SUBJECT-FAMILY DISPLAY TITLE for an overview page whose [Title] tag was left
			// completely empty by the writer. When no title could be derived from the
			// source document at all (titles is still empty at this point) and this is a
			// Fundamentals-template overview, fall back to a human-readable display name
			// for the whole subject family (header.family_title_default.by_prefix) — this
			// is the general rule the reference developer follows for an empty [Title],
			// even though that family name never literally appears anywhere in the source
			// Writers Template. Fires ONLY when titles is genuinely empty — a module with
			// a filled-in [Title] (e.g. "About me") is completely unaffected. Scoped to the
			// #header element, so it cannot affect the body-content comparison gates.
			// Env toggle: FAMILYTITLE_OFF.
			if (titles.filter(Boolean).length === 0) {
				const ftd = tpl.header.family_title_default;
				const ftdOn = ftd && ftd.enabled !== false
					&& !(typeof process !== "undefined" && process.env && process.env.FAMILYTITLE_OFF)
					&& /(^|\s)fundamentals(\s|$)/.test(rules.body_class || "");
				if (ftdOn) {
					const code = run.moduleCode || "";
					for (const [pfx, famTitle] of Object.entries(ftd.by_prefix || {})) {
						if (code.startsWith(pfx)) { titles.push(famTitle); break; }
					}
				}
			}
		} else {
			// lesson pages: the lesson's own title (corpus practice), falling
			// back to the module title when the writer gave none. Lessons DO
			// follow the registry count (they show the lesson title only).
			// ROUND 316 (loop Round 3 — KB constraint 79). A lesson whose OWN title is a
			// pipe-joined bilingual pair ("One | Tahi", "TRR102 The vowels: Aa | Ngā
			// Oropuare: Aa") ships the LESSON's English + Te Reo pair as two h1 spans —
			// the gold's form on 40/40 measured pages — with the module code stripped and,
			// in a reoTranslate module, Te Reo first (07D MTK rule 7). See #lessonPair.
			// Data header.lesson_bilingual_pair; env LESSONPAIR_OFF.
			let pairTitles = SkeletonBuilder.#lessonPair(page.pageTitle || "", run, rules, tpl.header.lesson_bilingual_pair);
			// ROUND 321 (the MTK title source): a reoTranslate lesson page with no own title
			// (none harvested, or one that fold-equals a module title) repeats BOTH module
			// titles, Māori first (07D rule 7; the gold on every such TRR/PNR lesson), exempt
			// from the registry h1_count cap. Data header.mtk_titles; env MTKTITLES_OFF.
			if (!pairTitles && SkeletonBuilder.#mtkOn(rules, tpl) && run.englishTitle && run.teReoTitle) {
				const own = Utils.Fold(page.pageTitle || "");
				if (!own || own === Utils.Fold(run.englishTitle) || own === Utils.Fold(run.teReoTitle)) {
					const pair = [run.englishTitle, run.teReoTitle];
					if (SkeletonBuilder.#looksMaori(pair[1]) && !SkeletonBuilder.#looksMaori(pair[0])) pair.reverse();
					pairTitles = pair;
				}
			}
			// ROUND 358: a pair split from an ALL-CAPS title is sentence-cased PER HALF (the r327 rule applied to each
			// title, so a single-word Māori half — HES1005 "KAITIAKITANGA" — is not left in caps by the single-token
			// exception), and a half never starts with a lowercase letter (a colon pair's second half). Data
			// header.te_reo_detect.pair_half_casing; env REODETECT_OFF.
			if (pairTitles && SkeletonBuilder.#teReoDetectOn(tpl) && tpl.header.te_reo_detect?.pair_half_casing !== false) {
				if (SkeletonBuilder.#titleCasing(page.pageTitle || "", tpl).changed) pairCapsSet = new Set(pairTitles);   // sentence-cased per half in the emit loop below (the red flag kept)
				else pairTitles = pairTitles.map((h) => /\s/.test(String(h).trim()) ? String(h).replace(/\p{L}/u, (ch) => ch.toUpperCase()) : String(h));   // a multi-word half never starts lowercase; a phonics team ("io") is left alone
			}
			if (pairTitles) titles.push(...pairTitles);
			else titles.push(page.pageTitle || SkeletonBuilder.#englishOf(run.englishTitle, run.teReoTitle, tpl) || content.titleBar.english || "");
			// CL-0042 (ROUND 230 — the OSSC pair, Chris). For the subject code
			// prefixes in header.lesson_title_h1.subjects (the OSSC short-course
			// family), a lesson page carries EXACTLY ONE title h1 — its own lesson
			// title — at EVERY level: the module's Te Reo title is never pushed as
			// a second lesson h1, even where the registry's mined h1_count asks for
			// 2 (the OSSC301 gold pre-dates the rule and repeats "Ngā Tāware" on
			// every lesson; that divergence is a recorded intentional override —
			// never chase it back in). Output-inert today: no OSSC module currently
			// derives a Te Reo title (OSSC301's ✅-glued [TITLE BAR] never splits),
			// so this converts an accident into a guarantee — the round-224
			// prefix-override pattern. Data: header.lesson_title_h1.
			// Env toggle: OSSCH1_OFF (restores the pre-230 push).
			const lth = tpl.header.lesson_title_h1;
			const lthSuppress = lth && lth.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env.OSSCH1_OFF)
				&& (lth.subjects ?? []).some((pfx) => String(run.moduleCode || "").startsWith(pfx));
			// E2 (ROUND 241 — Dev-Feedback R4; the recorded r199 follow-up, dev-confirmed).
			// The module's Te Reo title joins a lesson page as a second h1 ONLY when the
			// lesson has NO distinct title of its own — i.e. its title fell back to (or
			// fold-equals) the module English title, the XMES102/103 gold form where the
			// module's bilingual pair repeats on every lesson. A lesson with a DISTINCT
			// own title ships ONE h1, the lesson's own — the gold form on every measured
			// distinct-title lesson (XMES101 ×8, CEDT207 ×6, CEDT301 ×6; 35 dual-h1 pages
			// measured round 241 → 25 suppress / 10 keep). Composes with (independent of)
			// the CL-0042 OSSC gate above. Data: header.lesson_te_reo_suppress.
			// Env toggle: LESSONTEREO_OFF (restores the unconditional push).
			const ltr = tpl.header.lesson_te_reo_suppress;
			const modEng = run.englishTitle || content.titleBar.english || "";
			const distinctSuppress = ltr && ltr.enabled !== false
				&& (ltr.suppress_when_distinct_title ?? true)
				&& !(typeof process !== "undefined" && process.env && process.env.LESSONTEREO_OFF)
				&& !!page.pageTitle && !!modEng
				&& Utils.Fold(page.pageTitle) !== Utils.Fold(modEng);
			// ROUND 316: a lesson that carries its OWN pair never takes the module's Te Reo
			// title beside it, and the pair is exempt from the registry h1_count cap.
			if (!pairTitles && run.teReoTitle && wanted > 1 && !lthSuppress && !distinctSuppress) titles.push(run.teReoTitle);
			const cap = pairTitles ? Math.max(wanted, pairTitles.length) : wanted;
			while (titles.length > cap) titles.pop();
			if (titles.filter(Boolean).length < wanted) {
				run.AddNote("info", "SkeletonBuilder",
					`Page ${page.lessonLabel}: h1_count wants ${wanted} title(s) but the source provided ${titles.filter(Boolean).length} — emitted what exists.`);
			}
		}
		// For a "Module N - ..." prefix-family title (see above), the title's <h1> text
		// is wrapped in a lowercase span (a text-transform:lowercase style) instead of
		// the plain title template. This stops the site's shared CSS from Title-Casing
		// the phonics "letter team" text (e.g. "th", "sh", "ue") that follows the
		// prefix, which is meant to stay visually lowercase.
		const titleTpl = (run.modulePrefix
				&& tpl.header.title_split?.module_prefix_split?.lowercase_span !== false
				&& tpl.header.title_h1_lowercase)
			? tpl.header.title_h1_lowercase
			: tpl.header.title_h1;
		// Render the FIRST overview title via the dedicated title_h1_phonics template when
		// this is a phonics-family overview — it separately marks up the normal-cased lead
		// text (CSS-capitalised by the site) and the lowercase letter-team span.
		let firstTitle = true;
		for (const t of titles.filter(Boolean)) {
			if (firstTitle && pageType === "overview" && content.titleBar?.phonicsLead
				&& tpl.header.title_h1_phonics) {
				parts.push(Utils.FillTemplate(tpl.header.title_h1_phonics, {
					lead: Utils.EscapeHtml(content.titleBar.phonicsLead),
					sep: Utils.EscapeHtml(content.titleBar.phonicsSep || "\u2013"),
					tail: Utils.EscapeHtml(content.titleBar.phonicsTail || ""),
				}));
				firstTitle = false;
				continue;
			}
			firstTitle = false;
			// ROUND 327: a multi-word ALL-CAPS writer title renders in sentence case (the KB's
			// title-casing rule) + one red flag quoting the original (proper-noun caution)
			// ROUND 358: a half of a pair split from an ALL-CAPS title is sentence-cased as a whole title would be (the single-token
			// exception does not apply to a half — HES1005 "KAITIAKITANGA"), and the r327 red flag still names the original.
			const cased = (pairCapsSet && pairCapsSet.has(t))
				? { text: String(t).toLowerCase().replace(/\p{L}/u, (ch) => ch.toUpperCase()), changed: true }
				: SkeletonBuilder.#titleCasing(t, tpl);
			parts.push(Utils.FillTemplate(titleTpl, { title: Utils.EscapeHtml(cased.text) }));
			if (cased.changed && tpl.header.title_casing?.red_flag) {
				parts.push(NotesAndComments.redFlag(
					Utils.FillTemplate(tpl.header.title_casing.red_flag, { original: t }), run, "diagnostic"));
			}
		}

		// ---- menu button + content (menu_type pattern) ---------------------
		if (content.menu.kind !== "none") {
			const tooltipWanted = (rules.menu_button_tooltip?.[pageType] ?? "no") === "yes";
			parts.push(Utils.FillTemplate(tpl.header.menu_buttons, {
				tooltipAttr: tooltipWanted
					? Utils.FillTemplate(tpl.header.tooltip_attr, { tooltipText: tpl.header.tooltip_text_default })
					: "",
			}));
			// shell by ARCHETYPE (the convention cascade decided it in the
			// menu builder); "tabs"/"flat" map to the original shells
			// The English-subject family's two-column overview menu (identified by the resolved convention banner_h4_span being false) uses the
			// 'two_col_offset' shell (no top banner; 'col-md-6 offset-md-0 col-12' columns) instead of the default 'two_col_li' shell, which the BLL
			// banner family keeps unchanged. content.menu.engFamily is set upstream by MenuBuilder.buildMenu whenever this family's convention is detected.
			// A tabs-style overview menu whose first pane's content MenuBuilder split
			// into two side-by-side registry-driven columns (content.menu.tab1Cols is
			// set when this happens) renders via the tabs_two_col shell instead of the
				// original single-column tabs shell; that shell (plus the hand-tuned
			// pane1_col_by_phase width table below) remains the fallback for lesson pages,
				// families this rule doesn't cover, declined cases, or when the
				// TABTWOCOL_OFF env toggle disables the feature.
			// A Fundamentals-template overview page
			// whose [Overview] "WALT / I can..." learning-intentions block MenuBuilder
			// composed into two registry-driven columns (content.menu.funLiCols is set
				// when this happens) renders via the dedicated fundamentals_li shell.
			// The MTK drop-down-menu bilingual tabs menu (ROUND 212 — the PNR
			// family) renders via its own reo_tabs shell: MenuBuilder set
			// content.menu.reoNav/reoPanes when it composed the "[Content for
			// DROP DOWN MENU]" table. Data: menu.shells.reo_tabs +
			// elements.dual_language.dropdown_menu; env REODROPMENU_OFF.
			// The WRITER-AUTHORED tab partition (ROUND 221 — module ENGJ403)
			// renders via its own writer_tabs shell: MenuBuilder set
			// content.menu.wtNav/wtPanes when it composed the menu from the
			// writer's own [tab N]/[close tab] markers. Data:
			// menu.shells.writer_tabs + menu.writer_tab_partition;
			// env MENUTABPART_OFF.
			const shellKey = (content.menu.archetype === "writer_tabs" && content.menu.wtPanes)
				? "writer_tabs"
				: (content.menu.archetype === "reo_tabs" && content.menu.reoNav)
				? "reo_tabs"
				: (content.menu.funLiCols && content.menu.funLiCols.length)
					? "fundamentals_li"
					: content.menu.archetype === "two_col_li"
						? (content.menu.engFamily ? "two_col_offset" : (content.menu.inquiryFamily ? "two_col_inquiry" : "two_col_li"))   // r359: the Inquiry two-column shell
						: (content.menu.kind === "tabs"
							? (content.menu.tab1Cols ? "tabs_two_col" : "tabs") : "simplified");
			const shell = tpl.menu.shells[shellKey];
			if (shell) {
				// tab pane 1's column class is phase-dependent (corpus-
				// dominant per phase; data: menu.pane1_col_by_phase)
				const colByPhase = tpl.menu.pane1_col_by_phase ?? {};
				// TAB-2 TWO-COLUMN body. When MenuBuilder moved the Learning-Intentions /
				// Success-Criteria content onto the second tab and split it into two
				// side-by-side columns (content.menu.tab2Cols is set when this happens),
				// render those two columns in the tab-2 pane; otherwise fall back to the
				// original single 'col-md-8 col-12' column this shell always rendered
				// before the {tab2Body} slot existed.
				const tab2Body = (content.menu.tab2Cols && content.menu.tab2Cols.length)
					? content.menu.tab2Cols.map((c) => Utils.FillTemplate(
						tpl.menu.tabs_pane1_col ?? "<div class=\"{cls}\">\n{content}</div>",
						{ cls: c.cls, content: c.html ? c.html + "\n" : "" })).join("\n")
					: "<div class=\"col-md-8 col-12\">\n" + (content.menu.tab2 ?? "") + "\n</div>";
				// EXTRA MODULE-MENU TABS (module AGH1001's "[Module menu tab
				// rules]" screenshot): sections MenuBuilder promoted to their own
				// nav tabs (content.menu.extraTabs) render as additional
				// <li><a>label</a></li> nav items + tab-pane divs through the
				// {extraNav}/{extraPanes} shell slots. Both slots fill with ""
				// when no tab was promoted, leaving the two-tab shells
				// byte-identical to their pre-slot form. Data: menu.extra_tabs.
				const xt = content.menu.extraTabs ?? [];
				const xtCfg = tpl.menu.extra_tabs ?? {};
				const extraNav = xt.map((t) => Utils.FillTemplate(
					xtCfg.nav_item_template ?? "\n<li><a>{label}</a></li>",
					{ label: Utils.EscapeHtml(t.label) })).join("");
				const extraPanes = xt.map((t) => Utils.FillTemplate(
					xtCfg.pane_template ?? "\n<div class=\"tab-pane\">\n<div class=\"row\">\n<div class=\"{col}\">\n{content}\n</div>\n</div>\n</div>",
					{ col: xtCfg.pane_col ?? "col-md-8 col-12", content: t.html })).join("");
				// ROUND 263 (curriculum tabs — module SCCH302): the tabs shells'
				// Information nav item + pane are now {tab2Nav}/{tab2Pane} slots.
				// The defaults below reconstruct the previously hard-wired strings
				// BYTE-IDENTICALLY (the r172 {tab2Body}-slot precedent), so every
				// existing tabs menu is unchanged; only a menu MenuBuilder flagged
				// dropTab2 (a registry row with _drop_empty_tab2 whose sections all
				// promoted away — SCCH301's Overview | Knowledge | Practices form)
				// fills them empty. Data: menu.tab2_nav_item + menu.tab2_pane_template.
				const dropT2 = content.menu.dropTab2 === true;
				const tab2Nav = dropT2 ? "" : Utils.FillTemplate(
					tpl.menu.tab2_nav_item ?? "\n<li><a>{tab2Label}</a></li>",
					{ tab2Label: Utils.EscapeHtml(content.menu.tab2Label ?? "Information") });
				const tab2Pane = dropT2 ? "" : Utils.FillTemplate(
					tpl.menu.tab2_pane_template ?? "\n<div class=\"tab-pane\">\n<div class=\"row\">\n{tab2Body}\n</div>\n</div>",
					{ tab2Body });
				parts.push(Utils.FillTemplate(shell, {
					// the reo_tabs / writer_tabs shells' two slots (ROUNDS 212 + 221)
					navItems: content.menu.wtNav ?? content.menu.reoNav ?? "",
					panes: content.menu.wtPanes ?? content.menu.reoPanes ?? "",
					extraNav,
					extraPanes,
					tab2Nav,
					tab2Pane,
					// The tabs shells' second nav label is a {tab2Label} slot: the
					// default "Information" keeps every existing menu byte-identical;
					// MenuBuilder sets content.menu.tab2Label = "Learning" for the
					// MXEO/ENGS102 family (data menu.learning_tab; env LEARNTAB_OFF).
					tab2Label: Utils.EscapeHtml(content.menu.tab2Label ?? "Information"),
					// the fundamentals_li shell's two registry-driven columns (see above)
					cols: (content.menu.funLiCols ?? []).map((c) => Utils.FillTemplate(
						tpl.menu.tabs_pane1_col ?? "<div class=\"{cls}\">\n{content}</div>",
						{ cls: c.cls, content: c.html ? c.html + "\n" : "" })).join("\n"),
					tab1Col: colByPhase[rules.template_phase] ?? colByPhase._default ?? "col-md-12 col-12",
					tab1Content: content.menu.tab1 ?? "",
					tab1Cols: (content.menu.tab1Cols ?? []).map((c) => Utils.FillTemplate(
						tpl.menu.tabs_pane1_col ?? "<div class=\"{cls}\">\n{content}</div>",
						{ cls: c.cls, content: c.html ? c.html + "\n" : "" })).join("\n"),
					tab2Content: content.menu.tab2 ?? "",
					tab2Body,
					menuContent: content.menu.content ?? "",
					// two_col_li slots (Blended-Literacy form); ENG family suppresses the banner
					// The BANNER-style menu family renders its top banner text from the
					// module's own [H1] heading (reduced to its English form,
					// content.menu.bannerLabel), rather than a fixed hardcoded label.
					banner: (content.menu.engFamily || content.menu.inquiryFamily) ? ""
						: (content.menu.bannerLabel
							? Utils.FillTemplate(
								tpl.menu.two_col_li?.banner_template
									?? "<div class=\"col-md-12 col-12 paddingR\">\n<h4><span>{label}</span></h4>\n</div>\n",
								{ label: Utils.EscapeHtml(content.menu.bannerLabel) })
							: (tpl.menu.two_col_li?.banner ?? "")),
					// ROUND 359: an Inquiry family menu with NO curriculum (Understand / Know / Do) block leaves the left column
					// to the developer with a Writers Note (TWHA's gold writes the statements from the curriculum; the WT has none).
					leftContent: (content.menu.left || ((content.menu.inquiryFamily && tpl.menu.two_col_li?.inquiry_family?.empty_left_note) || "")),
					rightContent: content.menu.right ?? "",
				}));
			}
		}

		parts.push(tpl.header.close);
		return parts.join("\n");
	};

	/**
	 * Builds the #footer element: the nav CSS class (from footer_class) and
	 * the prev/next/home links appropriate for this page (from the
	 * footer_links registry pattern) — "final" wins on the module's very
	 * last page, so that footer only ever offers "home", never "next".
	 *
	 * @param {Object} options
	 * @param {ConversionRun} options.run - resolved registry rules + module identity
	 * @param {string} options.pageType - "overview" | "lesson"
	 * @param {boolean} options.isFinal - true on the module's last page
	 * @param {string} [options.prevHref] - the previous page's output filename
	 * @param {string} [options.nextHref] - the next page's output filename
	 * @param {string|null} [options.footerClassOverride] - forces the nav CSS
	 *                 class (used by the inquiry-layout case above)
	 * @param {string[]|null} [options.forceLinks] - forces which link keys
	 *                 render, bypassing the registry lookup (used by the
	 *                 CED inquiry fallback above)
	 * @returns {string} the #footer element's HTML
	 */
	static #buildFooter({ run, pageType, isFinal, prevHref = "", nextHref = "", footerClassOverride = null, forceLinks = null }) {
		const tpl = DataService.Data.EmitTemplates;
		const rules = run.resolvedRules;

		const patternKey = isFinal && rules.footer_links?.final ? "final" : pageType;
		let value = rules.footer_links?.[patternKey] ?? "none";
		let linkKeys = tpl.footer.value_map[value];

		if (linkKeys === undefined) {
			// ROUND 332 (KB 01B): a registry footer_links value with NO value_map entry is the
			// style-anchor miner's no-evidence marker (an em dash / "n/a"), not a pattern — the
			// footer shipped with no links on 141 pages. Fall back to the KB's form for the page
			// position (overview next+home / lesson prev+next+home / final prev+home). A value
			// that IS in the map is never touched. Data footer.kb_position_defaults; env FOOTERPOS_OFF.
			const kb = tpl.footer.kb_position_defaults;
			const kbOn = kb && kb.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[kb.env || "FOOTERPOS_OFF"]);
			// the sub-type form first (fundamentals-nav = home only, keyed by a token of the
			// resolved footer class), else the KB's position rule; a caller-forced link set
			// (the CED inquiry shell) outranks both and is left to the path below.
			const fcls = String(footerClassOverride ?? rules.footer_class ?? "").split(/\s+/);
			const byCls = kbOn && kb.by_footer_class
				? Object.keys(kb.by_footer_class).find((k) => k !== "_doc" && fcls.includes(k)) : undefined;
			const kbValue = !kbOn || (forceLinks && forceLinks.length) ? undefined
				: (byCls ? kb.by_footer_class[byCls][patternKey] : kb[patternKey]);
			if (kbValue !== undefined && tpl.footer.value_map[kbValue] !== undefined) {
				run.AddNote("info", "SkeletonBuilder",
					`footer_links "${patternKey}" value "${value}" is not a footer pattern (the registry's no-evidence marker) — the KB's ${patternKey}-page form "${kbValue}" applied (footer.kb_position_defaults).`);
				value = kbValue;
				linkKeys = tpl.footer.value_map[value];
			} else {
				run.AddNote("warn", "SkeletonBuilder",
					`footer_links value "${value}" has no footer.value_map entry — footer emitted with no links; add the value to Emit_Templates.`);
			}
		}

		const parts = [tpl.footer.open];
		// A CED-subject inquiry page whose registry produced no footer links at all uses
		// the fixed inquiry nav shell (the forceLinks value the caller passed in above);
		// modules that already have registry-defined footer links keep using those.
		let keys = linkKeys ?? [];
		if (!keys.length && forceLinks && forceLinks.length) keys = forceLinks;
		if (keys.length) {
			parts.push(Utils.FillTemplate(tpl.footer.nav_open, {
				footerClass: footerClassOverride ?? rules.footer_class ?? "footer-nav",
			}));
			// prev/next hrefs auto-chained to the sibling output files so the
			// generated bundle navigates page-to-page (data: footer.links)
			for (const k of keys) {
				parts.push(Utils.FillTemplate(tpl.footer.links[k], { prevHref, nextHref }));
			}
			parts.push(tpl.footer.nav_close);
		}
		parts.push(tpl.footer.close);
		return parts.join("\n");
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { SkeletonBuilder };
