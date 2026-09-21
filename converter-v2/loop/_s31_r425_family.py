"""_s31_r425_family.py — round 425: the XOTP family's page conventions behind the adapter's run flags.
  A. the bare activity box (run.activityBoxBare → activity_wrapper.open_bare / close_bare)
  B. the lesson h1 repeats the module title when h1_count asks for more than the source gives (run.lessonTitleRepeatsModule)
  C. a callout def VARIANT by module-code prefix (callouts.by_tag.<tag>.variants[] — lead_element / wrap_content / column)
Run under WSL from CONVERTER_V2/outputs: python3 _s31_r425_family.py"""
import io, os
JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2", "app", "js")

def patch(name, old, new, count=1):
    p = os.path.join(JS, name)
    s = io.open(p, encoding="utf-8", newline="").read()
    assert s.count(old) == count, (name, s.count(old), old[:60])
    s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("patched", name)

# ---- A. the bare activity box -------------------------------------------------------------
patch("ActivitiesBuilder.js",
"""		const panelBare = !!it._r307PanelId && !!pnrCfg && pnrCfg.enabled !== false
			&& !!tpl.activity_wrapper.open_bare
			&& !(typeof process !== "undefined" && process.env && process.env[pnrCfg.env || "CDPANELROW_OFF"]);
""",
"""		const panelBare = (!!it._r307PanelId && !!pnrCfg && pnrCfg.enabled !== false
			&& !!tpl.activity_wrapper.open_bare
			&& !(typeof process !== "undefined" && process.env && process.env[pnrCfg.env || "CDPANELROW_OFF"]))
			// ROUND 425 — the activity-table adapter's family (XOTP): every gold box holds its content
			// DIRECTLY (63 / 63 boxes on the 24 gold pages); the adapter sets run.activityBoxBare from
			// input_shapes.activity_table.adapter.activity_box === "bare" (env ACTTABLEADAPT_OFF).
			|| (!!run?.activityBoxBare && !!tpl.activity_wrapper.open_bare && !!tpl.activity_wrapper.close_bare);
""")

# ---- B. the lesson h1 repeats the module title ----------------------------------------------
patch("SkeletonBuilder.js",
"""			const cap = pairTitles ? Math.max(wanted, pairTitles.length) : wanted;
			while (titles.length > cap) titles.pop();
			if (titles.filter(Boolean).length < wanted) {
""",
"""			const cap = pairTitles ? Math.max(wanted, pairTitles.length) : wanted;
			while (titles.length > cap) titles.pop();
			// ROUND 425 — the activity-table adapter's family (XOTP): a lesson page with no title of its own
			// and no Te Reo title repeats the MODULE title as its lesson h1 where the registry's h1_count
			// asks for two (23 / 24 gold pages carry two identical `<h1><span>` titles). The adapter sets
			// run.lessonTitleRepeatsModule from adapter.lesson_title_repeats_module (env ACTTABLEADAPT_OFF).
			if (run.lessonTitleRepeatsModule && !pairTitles && titles.length === 1 && titles[0]
				&& titles.filter(Boolean).length < wanted) titles.push(titles[0]);
			if (titles.filter(Boolean).length < wanted) {
""")

# ---- C. the callout def variant by code prefix -----------------------------------------------
patch("ContentConverter.js",
"""		const _kbf = def.kb_form;
		if (_kbf && _kbf.enabled !== false && _kbf.open
			&& !(typeof process !== "undefined" && process.env && process.env[_kbf.env ?? "WANANGA_OFF"])) {
			def = Object.assign({}, def, { open: _kbf.open, close: _kbf.close ?? def.close,
				wrap_content: _kbf.wrap_content ?? def.wrap_content });
		}
""",
"""		const _kbf = def.kb_form;
		if (_kbf && _kbf.enabled !== false && _kbf.open
			&& !(typeof process !== "undefined" && process.env && process.env[_kbf.env ?? "WANANGA_OFF"])) {
			def = Object.assign({}, def, { open: _kbf.open, close: _kbf.close ?? def.close,
				wrap_content: _kbf.wrap_content ?? def.wrap_content });
		}
		def = ContentConverter.#calloutVariant(def, run);   // ROUND 425 — a family variant by module-code prefix
""")

patch("ContentConverter.js",
"""		const leadEl = def.lead_element
			? (run.conventions?.calloutLead || def.lead_element) : null;
		const leadHtml = (text) => leadEl
""",
"""		const leadEl = def.lead_element
			? (def._variantLead ? def.lead_element : (run.conventions?.calloutLead || def.lead_element)) : null;   // r425: a variant's lead is fixed
		const leadHtml = (text) => leadEl
""")

# the helper, placed before #calloutOpen
patch("ContentConverter.js",
"""	static #calloutOpen(it, bodyItems, i, stack, run, spans, wrapStructured = false) {
		const tpl = DataService.Data.EmitTemplates;
""",
"""	/**
	 * ROUND 425 — A CALLOUT DEF VARIANT BY MODULE-CODE PREFIX. A def may carry `variants: [{ code_prefixes, env,
	 * open, close, wrap_content, lead_element, column }]`; the first variant whose prefix matches the run's module
	 * code overlays the def (the r399 kb_form swap generalised to a family). `lead_element` on a variant is FIXED
	 * (the group convention does not override it); `column` is the section column class the callout's row opens
	 * with (ContentConverter's lazy row open reads it through #calloutColumn). The activity-table family's alert:
	 * no inner row > col-12, an h3 lead, a `col-md-9 col-12` column (12 / 12 gold alerts, 10 / 12 col-md-9).
	 */
	static #calloutVariant(def, run) {
		if (!def || !Array.isArray(def.variants) || !def.variants.length) return def;
		const code = String(run?.moduleCode || "").toUpperCase();
		for (const v of def.variants) {
			if (!v || v.enabled === false) continue;
			if (v.env && typeof process !== "undefined" && process.env && process.env[v.env]) continue;
			if (!(v.code_prefixes ?? []).some((p) => code.startsWith(String(p).toUpperCase()))) continue;
			const out = Object.assign({}, def);
			for (const k of ["open", "close", "wrap_content", "lead_element", "column"]) if (v[k] !== undefined) out[k] = v[k];
			if (v.lead_element !== undefined) out._variantLead = true;
			return out;
		}
		return def;
	}

	/** ROUND 425 — the section column class a callout tag's variant asks for (null = the default). */
	static #calloutColumn(tag, run) {
		const tpl = DataService.Data.EmitTemplates;
		const def = ContentConverter.#calloutVariant(tpl.callouts?.by_tag?.[tag], run);
		return def && def.column ? String(def.column) : null;
	}

	static #calloutOpen(it, bodyItems, i, stack, run, spans, wrapStructured = false) {
		const tpl = DataService.Data.EmitTemplates;
""")

# the lazy row open honours a one-shot column class
patch("ContentConverter.js",
"""		let nextRowClass = "";
""",
"""		let nextRowClass = "";
		let nextColClass = "";   // ROUND 425 — a one-shot section column class (a callout variant's `column`)
""")
patch("ContentConverter.js",
"""					{ contentColClass: tpl.body_region.content_col_class_default, rowClass: nextRowClass }));
				rowOpen = true; nextRowClass = "";
""",
"""					{ contentColClass: nextColClass || tpl.body_region.content_col_class_default, rowClass: nextRowClass }));
				rowOpen = true; nextRowClass = ""; nextColClass = "";
""")
patch("ContentConverter.js",
"""					const _r387Parts = this.#calloutOpen(it, bodyItems, i, stack, run, spans, wrapStructured);
					const _r388BoxOpen = _r387Parts.find((p) => typeof p === "string" && /^\\s*<div class="/.test(p)) ?? "";
					emit(..._r387Parts);
""",
"""					const _r387Parts = this.#calloutOpen(it, bodyItems, i, stack, run, spans, wrapStructured);
					const _r388BoxOpen = _r387Parts.find((p) => typeof p === "string" && /^\\s*<div class="/.test(p)) ?? "";
					if (!rowOpen) nextColClass = ContentConverter.#calloutColumn(primary.tag, run) ?? "";   // r425: the variant's column
					emit(..._r387Parts);
""")
