/**
 * TemplateModeResolver.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * The single place that composes a page's <body> TEMPLATE MODE — the body
 * class (in canonical token order) and the body language/translation attrs —
 * from the module's resolved registry body_class. A module's template is a
 * BASE layout (standard / fundamentals / inquiry) plus optional MODIFIERS
 * (mathJax / reoTranslate). The HUMAN convention (measured):
 *   - BASE tokens (fundamentals / inquiry) PREPEND before 'container-fluid';
 *   - MODIFIER tokens (mathJax / reoTranslate) APPEND after it;
 *   - fundamentals + reoTranslate additionally carry language/translation
 *     body attributes (the language-toggle the site JS reads).
 *
 * CURRENT SCOPE: this NORMALISES whatever mode the Style_Anchor_Registry
 * already encodes — the registry stored fundamentals/inquiry in the WRONG
 * order ('container-fluid fundamentals' / 'container-fluid inquiry') and
 * dropped the attrs. It does NOT detect brand-new modes that the registry
 * doesn't already encode (e.g. crumbs/panels, or dual-language element
 * pairing) — those would be separate, not-yet-built extensions. It is
 * provably BYTE-NEUTRAL on Standard ('container-fluid') and on
 * already-correct 'container-fluid mathJax', and it passes sentinel values
 * ('n/a' / '—' / no core token) through untouched.
 *
 * DATA: data/Template_Modes.json (DataService.Data.TemplateModes).
 * ENV:  TEMPLATEMODE_OFF (or data enabled:false) reverts to the raw registry
 *       body_class with no reorder and no attrs — the A/B mandate (§11).
 * ===========================================================================
 */
class TemplateModeResolver {

	/**
	 * Normalises one module's raw body_class into the human's canonical
	 * token order, and derives the matching body attributes.
	 *
	 * HOW IT WORKS:
	 * Splits the raw class string into three buckets — BASE tokens
	 * (fundamentals / inquiry), the core layout token (container-fluid),
	 * and MODIFIER tokens (mathJax / reoTranslate) — then re-joins them in
	 * the fixed order bases + core + anything unrecognised + modifiers.
	 * Any base/modifier that carries body_attrs in Template_Modes.json
	 * (e.g. fundamentals' language/translation pair) gets those attrs
	 * merged onto the result.
	 *
	 * USAGE (verified against data/Template_Modes.json):
	 * TemplateModeResolver.Resolve("container-fluid fundamentals")
	 *   → { bodyClass: "fundamentals container-fluid",
	 *       bodyAttrs: ' language="eng" translation="reo"' }
	 *
	 * @param {string|undefined} bodyClassRaw - the resolved registry body_class
	 * @param {ConversionRun} [run] - run context (for notes; optional, currently unused)
	 * @returns {{bodyClass: string, bodyAttrs: string}} canonical class +
	 *          the leading-space-prefixed body attribute string ("" if none)
	 */
	static Resolve(bodyClassRaw, run) {
		const raw = bodyClassRaw ?? "container-fluid";
		const data = (typeof DataService !== "undefined" && DataService.Data && DataService.Data.TemplateModes) || null;
		const off = typeof process !== "undefined" && process.env && process.env.TEMPLATEMODE_OFF;

		// OFF / no-data / disabled → byte-identical to skipping this normalisation entirely
		if (off || !data || data.enabled === false) {
			return { bodyClass: raw, bodyAttrs: "" };
		}

		const core  = data.core_token || "container-fluid";
		const bases = data.bases || {};
		const mods  = data.modifiers || {};

		const baseTok = [], modTok = [], otherTok = [];
		let hasCore = false;
		for (const t of raw.split(/\s+/).filter(Boolean)) {
			if (t === core) hasCore = true;
			else if (Object.prototype.hasOwnProperty.call(bases, t)) baseTok.push(t);
			else if (Object.prototype.hasOwnProperty.call(mods, t)) modTok.push(t);
			else otherTok.push(t);
		}

		// No core layout token (sentinels 'n/a' / '—' / 'absent', or empty) →
		// never invent a layout; pass the registry value through untouched.
		if (!hasCore) return { bodyClass: raw, bodyAttrs: "" };

		// canonical order: bases, core, unknowns, modifiers
		const bodyClass = [...baseTok, core, ...otherTok, ...modTok].join(" ");

		// body attrs: merge each active mode's attrs (base first, then modifier)
		const attrs = {};
		for (const t of baseTok) Object.assign(attrs, (bases[t] && bases[t].body_attrs) || {});
		for (const t of modTok) Object.assign(attrs, (mods[t] && mods[t].body_attrs) || {});
		let bodyAttrs = "";
		for (const [k, v] of Object.entries(attrs)) bodyAttrs += ` ${k}="${v}"`;

		return { bodyClass, bodyAttrs };
	}
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { TemplateModeResolver };
