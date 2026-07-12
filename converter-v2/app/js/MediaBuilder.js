/**
 * MediaBuilder.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * The MEDIA emitters, split out of ContentConverter (the main content-emitting
 * class) into their own file to keep that file's size manageable. An
 * [image] / [video] / [audio] tag resolves to a media element whose pasted
 * URL is an asset REFERENCE — that URL string itself is never shown as
 * visible page text. These statics build the embed (or the Mode-P
 * placeholder), strip out the reference-URL residue the reference site never
 * ships as visible text, and gather up the element's following black text
 * (its caption). Four statics, grouped by family:
 *
 *   - image  the Mode P (a visible placeholder plus a commented-out real
 *         reference, left for the developer) / Mode D (a direct <img>) image
 *         emitter; an iStock id found in the pasted URL drives the filename,
 *         otherwise a filename is slugified from the caption text
 *   - media  the video/audio emitter: a YouTube URL -> the site's standard
 *         embed form, any other URL -> a generic iframe, audio -> the audio
 *         player; carries the video-title drop (VIDTITLE_OFF) and its own
 *         raw-text URL search (MEDIAURLTEXT_OFF — note that the general
 *         element dispatcher elsewhere in ContentConverter keeps a SECOND,
 *         independent check of this same toggle at its own [Embed video]
 *         route)
 *   - stripMediaResidue  strips the reference URL plus any now-empty or
 *         orphaned parentheses left behind after removing it
 *         (MEDIAPAREN_OFF; the URL strip itself always runs unconditionally)
 *   - gatherFollowing  the "following black text" gatherer: collects a
 *         tag's own trailing text plus any directly-following black items
 *         (marking each one _consumed so the main render loop doesn't emit
 *         it a second time) — PUBLIC, because three OTHER call sites
 *         elsewhere in ContentConverter (the general element dispatcher,
 *         the side-alert column builder, and the callout-box opener) also
 *         need this same gathering logic
 *
 * WHY SEPARATE FILE:
 * These four methods were natural candidates for their own file because none
 * of them depend on ContentConverter's own internal state (its private
 * instance fields) — they only need DataService.Data (the shared global data
 * store, same as everywhere else in the app). Being self-contained like this
 * means they can live here without any awkward back-references into
 * ContentConverter.
 *
 * WHEN TO WORK HERE:
 * Any change to how an [image]/[video]/[audio] tag becomes its embed or
 * placeholder markup, how its reference URL gets cleaned out of the visible
 * caption text, or how its following caption text gets collected. Env
 * toggles VIDTITLE_OFF, MEDIAURLTEXT_OFF, MEDIAPAREN_OFF, and VIDEOICON_OFF
 * (all explained inline below, next to the behaviour they control) let each
 * individual behaviour be reverted for A/B comparison without a code change.
 * ===========================================================================
 */

class MediaBuilder {

	/**
	 * Image emitter. Renders either Mode P (a visible placeholder box, with a
	 * commented-out HTML comment holding the real image reference just below
	 * it — one of the only two places in the whole app an HTML comment is
	 * deliberately emitted) or Mode D (a direct <img> tag), depending on
	 * run.imageMode. Either way, the writer's pasted iStock URL is the asset
	 * REFERENCE — it gets consumed to build the output filename, and is
	 * never itself rendered as visible page text.
	 *
	 * @param {Object} it - the current content item, e.g.
	 *        { text: "[image]", block: { links: [{ target: "https://..." }] },
	 *          parse: { remainders: ["a smiling dog"] } }
	 * @param {Object[]} bodyItems - the page's flat list of content items (see gatherFollowing)
	 * @param {number} i - this item's index within bodyItems
	 * @param {ConversionRun} run - the current conversion run (drives imageMode)
	 * @returns {string[]} the rendered HTML fragments — the image markup,
	 *          plus any caption text found after it
	 */
	static image(it, bodyItems, i, run) {
		const tpl = DataService.Data.EmitTemplates.image;
		const out = [];
		const gathered = this.gatherFollowing(it, bodyItems, i);
		const url = it.block?.links?.[0]?.target
			?? (gathered.match(/https?:\/\/[^\s\]\)"<>]+/)?.[0] ?? "");

		// filename: iStock id when present (data rule), else a slug
		const istockId = url.match(/gm-?(\d{6,10})/)?.[1] ?? null;
		const filename = istockId
			? Utils.FillTemplate(tpl.filename_rules.istock, { id: istockId })
			: `${Utils.Slugify(it.parse.remainders.join(" ") || "image") || "image"}.jpg`;
		const label = istockId ? `iStock-${istockId}` : "image";

		if (run.imageMode === "P") {
			out.push(Utils.FillTemplate(tpl.mode_P.visible, { label }));
			out.push(Utils.FillTemplate(tpl.mode_P.comment, { filename }));
		} else {
			out.push(Utils.FillTemplate(tpl.mode_D.visible, { filename }));
		}

		// Whatever non-URL text was gathered is a caption / learner-facing line — keep it;
		// the URL itself never renders. Also strip out any now-empty or orphaned parenthesis
		// residue left behind once the URL is gone (shared stripMediaResidue below; env
		// MEDIAPAREN_OFF), which the reference site never ships as visible text.
		const caption = this.stripMediaResidue(gathered);
		if (caption) out.push(...ListsAndRuns.renderBlackText(caption, run));
		return out;
	};

	/**
	 * Video/audio emitter. A YouTube URL becomes the site's standard embed
	 * form; any other URL becomes a generic iframe; an audio tag becomes the
	 * audio player. A writer's own timing/editing note near the media (e.g.
	 * "edit to start at 0:45") stays visible as a red flag note right next to
	 * the embed — that note is meant for the developer, not the learner, but
	 * it still needs to be SEEN by whoever finishes the page, so it is never
	 * silently dropped.
	 *
	 * @param {Object} it - the current content item (the [video]/[audio] tag)
	 * @param {Object[]} bodyItems - the page's flat list of content items (see gatherFollowing)
	 * @param {number} i - this item's index within bodyItems
	 * @param {"video"|"audio"} kind - which kind of media element this is
	 * @param {ConversionRun} run - the current conversion run
	 * @returns {string[]} the rendered HTML fragments — the embed/player
	 *          markup, plus any caption text found after it
	 */
	static media(it, bodyItems, i, kind, run) {
		const tpl = DataService.Data.EmitTemplates;
		const acks = DataService.Data.AcksFormats.extraction_regexes;
		const out = [];
		const gathered = this.gatherFollowing(it, bodyItems, i);
		// Also search the element's OWN raw it.text for a video URL — a writer sometimes
		// types the URL directly INSIDE the tag's own red span itself (e.g. "[Embed video]
		// edit to start at ... https://youtu.be/..."), so it won't show up in blackAfter, in
		// a captured hyperlink, or in a following black item, the three sources checked
		// above. Data flag: elements.media_url_in_text. Env toggle: MEDIAURLTEXT_OFF. (The
		// surrounding instruction text itself stays OUT of `rest` below, which is built only
		// from `gathered`/the element's own trailing text — so the timing note isn't
		// re-rendered as if it were ordinary caption text.)
		const _urlInTextOn = (tpl.elements?.media_url_in_text?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.MEDIAURLTEXT_OFF);
		const _re = /https?:\/\/[^\s\]\)"<>]+/;
		const url = it.block?.links?.[0]?.target
			?? gathered.match(_re)?.[0]
			?? (_urlInTextOn ? String(it.text || "").match(_re)?.[0] : undefined)
			?? "";

		let builtVideoEmbed = false;
		if (kind === "audio") {
			const file = url.split("/").pop() || tpl.audio.default_filename;
			out.push(Utils.FillTemplate(tpl.audio.form, {
				filename: Utils.EscapeHtml(/\.\w{2,4}$/.test(file) ? file : tpl.audio.default_filename),
				title: "",
			}));
		} else {
			const videoId = url.match(new RegExp(acks.youtube_id))?.[1] ?? null;
			if (videoId) {
				let embed = Utils.FillTemplate(tpl.video.youtube, { videoId, params: "" });
				// the embed HOST follows the module's group convention
				// (Html_Convention_Registry; global default is nocookie)
				if (run.conventions?.videoHost === "youtube") {
					embed = embed.replace("youtube-nocookie.com", "youtube.com");
				}
				out.push(this.#applyVideoIcon(embed, run));
				builtVideoEmbed = true;
			} else if (url) {
				out.push(this.#applyVideoIcon(Utils.FillTemplate(tpl.video.generic_iframe, { url: Utils.EscapeHtml(url) }), run));
				builtVideoEmbed = true;
			} else {
				out.push(NotesAndComments.redFlag(`[${kind}] with no URL found — add the ${kind} source.`, run));
			}
		}

		// A [video] tag that successfully built a real embed DROPS its own title line
		// (it.blackAfter) from the rendered page — that text is really the video's NAME
		// (its title), which AcksBuilder separately ships in the page's acknowledgements
		// section; the reference site renders ONLY the video embed itself in the body, with
		// no separate title paragraph repeating the name. This drop is scoped carefully: it
		// still KEEPS any genuinely-following, separate prose (for example a later
		// paragraph — with no [body] tag of its own — that gatherFollowing also swept up,
		// such as "Here is an alternative video...") and it keeps ALL text belonging to an
		// AUDIO element (e.g. a transcript/dialogue line), since that text is never just a
		// repeated title. The residue strip (stripMediaResidue below) separately removes the
		// URL itself plus any now-empty or orphaned parenthesis left behind.
		// Data flag: elements.video_embed_title_drop. Env toggle: VIDTITLE_OFF.
		const dropTitleOn = (tpl.elements?.video_embed_title_drop?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.VIDTITLE_OFF);
		const own = it.blackAfter ?? "";
		const following = gathered.length > own.length ? gathered.slice(own.length) : "";
		const keepRaw = (dropTitleOn && kind === "video" && builtVideoEmbed) ? following : gathered;
		const rest = this.stripMediaResidue(keepRaw);
		if (rest) out.push(...ListsAndRuns.renderBlackText(rest, run, it.block?.links));
		return out;
	};

	/**
	 * Adds a play-button `icon` CSS class to a just-built videoSection embed,
	 * but only for modules belonging to a group the reference site
	 * consistently styles that way.
	 *
	 * WHY THIS EXISTS: the reference site sometimes adds an `icon` class to
	 * its video wrapper to show a play-button overlay, and sometimes doesn't
	 * — but this choice turns out to be a per-SUBJECT/SERIES HOUSE STYLE
	 * decision, not something decided video-by-video. Measurement
	 * (outputs/_measure_videoicon.cjs) found that 82% of modules containing
	 * videos are internally consistent — either ALL their videos use the
	 * icon style, or NONE of them do — which means there is no reliable
	 * per-video rule to discover; the real signal lives at the
	 * subject/series level.
	 *
	 * HOW THE GROUPS ARE DECIDED: a subject/series is only added to the
	 * data-driven `icon_series` / `icon_subject_template` lists (and so gets
	 * the icon style applied) when the reference examples for that group are
	 * OVERWHELMINGLY consistent one way — a large enough sample size, with a
	 * clear majority sharing the same icon-or-plain choice. A group that
	 * doesn't clear that bar is left out of the lists entirely and keeps the
	 * plain (no-icon) default. This method is applied as a simple string
	 * post-replace on the already-fully-built embed HTML (the same technique
	 * used just above for swapping the video host), which is why the shared
	 * video templates — and the widget builders (InteractiveBuilder,
	 * carousels) that reuse those same templates for videos embedded INSIDE
	 * a widget — are left completely unaffected; widget-embedded videos
	 * always stay in the plain form for now.
	 *
	 * @param {string} embed - the already-rendered videoSection embed HTML
	 * @param {ConversionRun} run - the current conversion run (for run.moduleCode,
	 *        used to look up the module's subject/series)
	 * @returns {string} the embed HTML, with the `icon` class added when this
	 *          module's group calls for it, otherwise unchanged
	 * The module's series / subject+template come from
	 * Module_Structure_Index.module_meta (the same lookup PrecedenceResolver
	 * uses elsewhere), with a simple code-prefix-derived series as a
	 * fallback when that data is missing. Data flag: video.icon_rule.
	 * Env toggle: VIDEOICON_OFF (or the data's own enabled:false) disables
	 * this method entirely, so every video embed stays in the plain form.
	 */
	static #applyVideoIcon(embed, run) {
		const rule = DataService.Data.EmitTemplates.video?.icon_rule;
		if (!rule || rule.enabled === false) return embed;
		if (typeof process !== "undefined" && process.env && process.env.VIDEOICON_OFF) return embed;
		const code = run?.moduleCode;
		if (!code) return embed;
		const m = (DataService.Data.ModuleStructureIndex?.module_meta || {})[code] || {};
		let series = m.series;
		if (!series) {
			const g = /^([A-Za-z]+)(\d+)/.exec(code);
			series = g ? g[1] + g[2].slice(0, 2) : null;   // prefix + first two digits (fallback)
		}
		const st = (m.subject && m.template_type) ? `${m.subject}|${m.template_type}` : null;
		const iconGroup = (rule.icon_series || []).includes(series)
			|| (st && (rule.icon_subject_template || []).includes(st));
		return iconGroup ? embed.replace('class="videoSection ', 'class="videoSection icon ') : embed;
	};

	/**
	 * Strips a media-reference URL, and any now-empty / orphaned parenthesis
	 * left behind by removing it, out of a media caption. Writers often paste
	 * a reference URL wrapped in parentheses right next to their caption text
	 * (e.g. "A red panda eating bamboo (https://...)"), but the reference
	 * site never ships that URL — or an empty "()"/"( )" wrapper, or a lone
	 * stray ")" or "(" — as visible caption text. Only EMPTY parenthesis
	 * pairs and ISOLATED single parens are removed here; a genuine
	 * parenthetical remark inside real prose, like "(this is important)", is
	 * always preserved untouched.
	 *
	 * @param {string} text - the raw caption text (may contain a reference URL)
	 * @returns {string} the cleaned caption text, whitespace-normalised
	 * The URL strip itself always runs, unconditionally. The paren cleanup
	 * is behind data flag elements.media_url_paren_strip and env toggle
	 * MEDIAPAREN_OFF (disables just the paren cleanup, leaving the URL strip
	 * active).
	 */
	static stripMediaResidue(text) {
		let s = String(text ?? "");
		const parenOn = (DataService.Data.EmitTemplates.elements?.media_url_paren_strip?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.MEDIAPAREN_OFF);
		// (url) → remove including its wrapper parens, then any remaining bare url
		s = s.replace(/\(\s*https?:\/\/[^\s)]+\s*\)/g, " ")
			.replace(/https?:\/\/[^\s\]\)"<>]+/g, "");
		if (parenOn) {
			s = s.replace(/\(\s*\)/g, "")                        // empty ()
				.replace(/(^|[\n\s])\)+(?=[\n\s]|$)/g, "$1")    // orphan )
				.replace(/(^|[\n\s])\(+(?=[\n\s]|$)/g, "$1");   // orphan (
		}
		return s.replace(/[ \t]+/g, " ").replace(/[ \t]*\n[ \t]*/g, "\n").replace(/\n{2,}/g, "\n").trim();
	};

	/**
	 * Gathers an element's "following black text" — the tag's own trailing
	 * text (blackAfter) plus any plain black content items that directly
	 * follow it in the page's item list. This is where writers most
	 * commonly put a media element's caption: not inside the tag itself, but
	 * as one or more ordinary paragraphs immediately after it. Each
	 * following item that gets swept up this way is marked _consumed, so the
	 * page's main render loop knows to skip it and doesn't render it a
	 * second time as a separate, stray paragraph.
	 *
	 * @param {Object} it - the current content item (the tag whose following
	 *        text is being gathered)
	 * @param {Object[]} bodyItems - the page's flat list of content items
	 * @param {number} i - this item's index within bodyItems
	 * @returns {string} the combined following text, newline-separated
	 */
	static gatherFollowing(it, bodyItems, i) {
		let text = it.blackAfter ?? "";
		for (let j = i + 1; j < bodyItems.length; j++) {
			const next = bodyItems[j];
			if (next.type !== "black" || next.consumedBy !== undefined) break;
			text += `\n${next.text}`;
			next._consumed = true;
		}
		return text;
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { MediaBuilder };
