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
 * (its caption). Five statics, grouped by family:
 *
 *   - image  the Mode P (a visible placeholder plus a commented-out real
 *         reference, left for the developer) / Mode D (a direct <img>) image
 *         emitter; an iStock id found in the pasted URL drives the filename,
 *         otherwise a filename is slugified from the caption text; a
 *         title-form reference line (the hyperlink's anchor text) is dropped
 *         from the caption (IMGREFTITLE_OFF)
 *   - FinishImg  the alt-text + loading="lazy" post-fill applied to every
 *         content image built here and in TablesAndGrids.cellImage
 *         (IMGATTRS_OFF)
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
		const url = this.CanonicalStockUrl(it.block?.links?.[0]?.target
			?? (gathered.match(/https?:\/\/[^\s\]\)"<>]+/)?.[0] ?? ""));

		// filename: iStock id when present (data rule), else a slug
		const istockId = url.match(/gm-?(\d{6,10})/)?.[1] ?? null;
		const filename = istockId
			? Utils.FillTemplate(tpl.filename_rules.istock, { id: istockId })
			: `${Utils.Slugify(it.parse.remainders.join(" ") || "image") || "image"}.jpg`;
		const label = istockId ? `iStock-${istockId}` : "image";

		if (run.imageMode === "P") {
			out.push(this.FinishImg(Utils.FillTemplate(tpl.mode_P.visible, { label }), url, istockId, run));
			out.push(this.FinishImg(Utils.FillTemplate(tpl.mode_P.comment, { filename }), url, istockId, run));
		} else {
			out.push(this.FinishImg(Utils.FillTemplate(tpl.mode_D.visible, { filename }), url, istockId, run));
		}

		// MEDIA-REFERENCE TITLE LINE DROP. When the
		// writer authors an image BY TITLE (the docx hyperlink's anchor TEXT is the
		// asset's title, e.g. "[image] Homogeneous Vs … – iStock", with the URL living
		// only in the link target), that title line is the media REFERENCE, not a
		// caption — the same class as the video-title drop, and the gold library never
		// ships such reference paragraphs (no "Download Image Now" <p>s). The
		// drop is scoped to the element's OWN text lines only (it.blackAfter), keeping
		// genuinely-following prose, and a line is dropped only when (a) it fold-equals
		// a non-URL hyperlink anchor of this same paragraph (the anchor IS the
		// reference), or (b) it matches the data-driven iStock reference-form pattern
		// (catches an anchor the extractor split across runs). Data flag:
		// elements.image_reference_title_drop. Env toggle: IMGREFTITLE_OFF.
		const refCfg = DataService.Data.EmitTemplates.elements?.image_reference_title_drop;
		const refDropOn = refCfg && refCfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env.IMGREFTITLE_OFF);
		let keep = gathered;
		if (refDropOn) {
			const own = it.blackAfter ?? "";
			const following = gathered.length > own.length ? gathered.slice(own.length) : "";
			const fold = (s) => String(s ?? "").toLowerCase().replace(/\s+/g, " ").trim();
			const anchors = (it.block?.links ?? [])
				.filter((l) => l.target && !/^https?:\/\//i.test(String(l.text ?? "").trim()))
				.map((l) => fold(l.text)).filter((t) => t.length >= (refCfg.min_anchor_length ?? 8));
			const refRe = new RegExp(refCfg.reference_line_pattern
				?? "download image now|stock (?:photo|illustration|vector)\\s*[\\u2013\\u2014-]", "i");
			const ownKept = own.split("\n").filter((line) => {
				const f = fold(line);
				if (!f) return true;
				if (anchors.includes(f)) return false;          // (a) the anchor IS this line
				if (refRe.test(f)) return false;                 // (b) the iStock reference form
				return true;
			}).join("\n");
			keep = ownKept + following;
		}

		// Whatever non-URL text was gathered is a caption / learner-facing line — keep it;
		// the URL itself never renders. Also strip out any now-empty or orphaned parenthesis
		// residue left behind once the URL is gone (shared stripMediaResidue below; env
		// MEDIAPAREN_OFF), which the reference site never ships as visible text.
		const caption = this.stripMediaResidue(keep);
		if (caption) out.push(...ListsAndRuns.renderBlackText(caption, run));
		return out;
	};

	/**
	 * IMAGE ALT TEXT + loading="lazy".
	 * A post-fill finisher applied to just-built content-image markup (a
	 * post-replace, so the shared templates and every OTHER consumer of them stay
	 * unchanged): fills the empty alt="" with the asset's title and injects the
	 * loading="lazy" hint.
	 *
	 * WHERE THE TITLE COMES FROM (authority order, as for the acknowledgements):
	 *   1. the VERIFIED iStock API title from the uploaded *_istock-acks.txt
	 *      (run.istockAcks — definitely correct, the developer's stated form)
	 *   2. the URL slug, Title-Cased (the slug IS the official title — the
	 *      rule the acknowledgements already rely on)
	 *   3. nothing derivable → alt stays "" (never invent a description).
	 * Applies uniformly to the Mode-P visible placeholder, the Mode-P
	 * commented-out real reference (the tag the developer copies out), and
	 * the Mode-D direct <img>. loading="lazy" is a FORWARD rule: the gold is
	 * era-mixed because older modules predate it — recorded as an
	 * overrides-gold convention in Subject_Global_Parameters._universal_conventions
	 * (img_alt_lazy), so gold divergences here are intentional.
	 *
	 * @param {string} html - the just-built image markup (may be a comment)
	 * @param {string} url - the asset reference URL ("" when none)
	 * @param {string|null} istockId - the iStock id from the URL, when present
	 * @param {ConversionRun} run - the run (run.istockAcks = verified titles)
	 * @returns {string} the markup with alt filled + loading="lazy" injected
	 * Data flag: elements.image_attrs (alt_from_reference / loading_lazy).
	 * Env toggle: IMGATTRS_OFF (reverts BOTH — alt stays "", no loading).
	 */
	/**
	 * THE iSTOCK IMAGE ADDRESS NAMES ITS ASSET. A writer often pastes iStock's image-FILE address
	 * (media.istockphoto.com/id/<id>/<kind>/<slug>.jpg) instead of the asset PAGE address
	 * (istockphoto.com/<kind>/<slug>-gm<id>-…); both carry the same asset id and title slug. The file
	 * form is rewritten to the page form, so the id that names the file (iStock-<id>.jpg) and the slug
	 * that gives its alt are read by the same patterns as every other iStock link. Any other address is
	 * returned unchanged. Data image.istock_cdn_form {pattern, canonical}; env ISTOCKCDN_OFF.
	 *
	 * @param {string} url
	 * @returns {string}
	 */
	static CanonicalStockUrl(url) {
		const cfg = DataService.Data.EmitTemplates.image?.istock_cdn_form;
		if (!url || !cfg || cfg.enabled === false) return url;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "ISTOCKCDN_OFF"]) return url;
		const m = String(url).match(new RegExp(cfg.pattern, "i"));
		return m ? Utils.FillTemplate(cfg.canonical, { id: m[1], kind: m[2].toLowerCase(), slug: m[3].toLowerCase() }) : url;
	};

	static FinishImg(html, url, istockId, run) {
		const cfg = DataService.Data.EmitTemplates.elements?.image_attrs;
		if (!cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && process.env.IMGATTRS_OFF) return html;
		let s = String(html);
		if (cfg.alt_from_reference !== false) {
			let title = (istockId && run?.istockAcks?.get(istockId)?.title) || null;
			if (!title && url) {
				const rx = DataService.Data.AcksFormats?.extraction_regexes?.istock_slug_from_url;
				const st = DataService.Data.AcksFormats?.istock_slug_title ?? {};
				let clean = url;
				try { clean = decodeURIComponent(url); } catch { /* keep raw on bad escapes */ }
				const slug = rx ? Utils.Fold(clean).replace(/\s+/g, "-").match(new RegExp(rx))?.[1] : null;
				if (slug) title = Utils.TitleCaseWords(slug.split("-").filter(Boolean),
					st.special_tokens ?? {}, st.lowercase_small_words ?? []);
			}
			if (title) s = s.replace(/alt=""/g, `alt="${Utils.EscapeHtml(title)}"`);
		}
		if (cfg.loading_lazy !== false) {
			s = s.replace(/<img class="img-fluid"(?![^>]*loading=)/g, '<img class="img-fluid" loading="lazy"');
		}
		return s;
	};

	/**
	 * KB CONSTRAINT 52's POSITIVE HALF ON EVERY IMAGE:
	 * "for an iStock image, the preferred alt value is the iStock/Getty API image name — the descriptive title carried
	 * in the supplied iStock acknowledgements file or recoverable from the iStock link".
	 *
	 * WHY. FinishImg fills the alt on the content-image path, where the URL is at hand. The widget-internal images
	 * (InteractiveBuilder.#assetImage) follow the same rule, but that point sees only the filename, so the slug fallback
	 * never fires there — many iStock images whose title IS recoverable from the module's own link (flipCard, carousel,
	 * activity, speechBubble, accordion …) would ship `alt=""`, while the gold fills most of its iStock alts.
	 *
	 * THE RULE, once per page, LAST: every `<img … alt="">` (the Mode-P placeholder, the commented-out reference and a
	 * Mode-D image alike) whose tag names `iStock-<id>` takes FinishImg's title for that id — the VERIFIED
	 * *_istock-acks.txt title, else the Title-Cased slug of the id's URL found anywhere in the module (the Media List
	 * items, the Writers Template blocks). An id with no URL and no verified title keeps "" (never invent a
	 * description); a non-iStock image is never touched; "stock photo" never reaches an alt (c52's negative half).
	 * Data elements.image_attrs.widget_alt_postpass {enabled, env WIDGETALT_OFF}.
	 *
	 * @param {string} html - one finished page
	 * @param {ConversionRun} run - the run (istockAcks, mediaItems, wtBlocks)
	 * @returns {string} the page with every derivable iStock alt filled
	 */
	static FillWidgetAlts(html, run) {
		const base = DataService.Data.EmitTemplates.elements?.image_attrs;
		const cfg = base?.widget_alt_postpass;
		if (!base || base.enabled === false || !cfg || cfg.enabled === false) return html;
		if (typeof process !== "undefined" && process.env && (process.env[cfg.env ?? "WIDGETALT_OFF"] || process.env.IMGATTRS_OFF)) return html;
		const titles = this.#istockAltMap(run, cfg);
		if (!titles.size) return html;
		return String(html).replace(/<img\b[^>]*>/g, (tag) => {
			if (!/\balt=""/.test(tag)) return tag;
			const id = tag.match(/iStock-(\d{6,10})/)?.[1];
			const title = id ? titles.get(id) : null;
			return title ? tag.replace(/\balt=""/, `alt="${Utils.EscapeHtml(title)}"`) : tag;
		});
	}

	/** {iStock id → alt title} for the module (cached on the run): verified acks title > URL-slug title. */
	static #istockAltMap(run, cfg) {
		if (run && run._altMap) return run._altMap;
		const map = new Map();
		const rx = DataService.Data.AcksFormats?.extraction_regexes ?? {};
		const st = DataService.Data.AcksFormats?.istock_slug_title ?? {};
		const strip = new RegExp(cfg.strip_pattern ?? "[\\s.,\\-–—]*\\bstock\\s+(?:photo|image|vector|illustration|video)s?\\b.*$", "i");
		const urls = [];
		for (const m of (run?.mediaItems ?? [])) if (m?.url) urls.push(String(m.url));
		let blob = "";
		try { blob = JSON.stringify(run?.wtBlocks ?? []); } catch { blob = ""; }
		for (const u of blob.match(/https?:\/\/(?:www\.)?istockphoto\.com\/[^\s"\\\]<>)]+/gi) ?? []) urls.push(u);
		// iStock's image-file addresses, in the page form (CanonicalStockUrl; unchanged when ISTOCKCDN_OFF)
		for (const u of blob.match(/https?:\/\/media\.istockphoto\.com\/[^\s"\\\]<>)]+/gi) ?? []) {
			const c = this.CanonicalStockUrl(u);
			if (c !== u) urls.push(c);
		}
		for (const url of urls) {
			let clean = url;
			try { clean = decodeURIComponent(url); } catch { /* keep raw on bad escapes */ }
			clean = Utils.Fold(clean).replace(/\s+/g, "-");
			const id = clean.match(new RegExp(rx.istock_id_from_url ?? "gm-?(\\d{6,10})"))?.[1];
			if (!id || map.has(id)) continue;
			let title = run?.istockAcks?.get(id)?.title ?? null;
			if (!title && rx.istock_slug_from_url) {
				const slug = clean.match(new RegExp(rx.istock_slug_from_url))?.[1] ?? null;
				if (slug) title = Utils.TitleCaseWords(slug.split("-").filter(Boolean), st.special_tokens ?? {}, st.lowercase_small_words ?? []);
			}
			title = title ? String(title).replace(strip, "").trim() : "";
			if (title) map.set(id, title);
		}
		// ids named only in a verified acks file (no link in the module) still carry their verified title
		if (run?.istockAcks?.forEach) run.istockAcks.forEach((v, id) => {
			if (!map.has(id) && v?.title) { const t = String(v.title).replace(strip, "").trim(); if (t) map.set(id, t); }
		});
		if (run) run._altMap = map;
		return map;
	}

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
	 * @param {TagNormaliser} [norm] - the run's normaliser (renders the hyperlinked lead)
	 * @returns {string[]} the rendered HTML fragments — the embed/player
	 *          markup, plus any caption text found after it
	 */
	static media(it, bodyItems, i, kind, run, norm) {
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
		// The FOLLOWING-LINE HYPERLINK source (as in ENGS404): the
		// WT authors "[insert video]" on its own line with the video as a TITLE-ANCHORED
		// hyperlink on the NEXT black line ("Pixar in a Box… - YouTube" → the URL lives in
		// the docx hyperlink, not the visible text — the image title-line class on the media path).
		// gatherFollowing above already absorbed that line's TEXT; this reads the same
		// following-black range's first hyperlink TARGET. Data elements.media_url_in_text
		// .following_link (default on); env MEDIAFOLLOWLINK_OFF.
		let followLink, followLinkLine;
		if ((tpl.elements?.media_url_in_text?.following_link ?? true)
			&& !(typeof process !== "undefined" && process.env && process.env.MEDIAFOLLOWLINK_OFF)) {
			for (let j = i + 1; j < bodyItems.length; j++) {
				const next = bodyItems[j];
				if (next.type !== "black") break;
				if (next.block?.links?.[0]?.target) {
					followLink = next.block.links[0].target;
					followLinkLine = String(next.text ?? "").trim();   // the reference line itself
					break;
				}
			}
		}
		// Seam B of elements.external_link_video_embed: a [video]/[embed] element
		// with NO url of its own whose next unconsumed item is a url-only [link]-family TAG
		// item carrying a VIDEO url ("[embed video with image and play button]" then
		// "[link] https://www.youtube.com/watch?v=…" — HIS1006/HIS1008) takes that url and
		// consumes the item, exactly as the following-link rule takes a following BLACK reference line.
		// Without it the element would print a "no URL" note and the link would ship as a button;
		// the gold embeds the video. Env LINKVID_OFF turns it off.
		let linkTagUrl;
		if (!it._mediaUrl && !(it.block?.links?.[0]?.target) && !gathered.match(_re) && !followLink && kind === "video") {
			const hit = this.FollowingVideoLinkTag(bodyItems, i, tpl);
			if (hit) { linkTagUrl = hit.url; hit.item._consumed = true; }
		}
		// it._mediaUrl: the URL a caller has already judged to be this element's own (the media-item video route)
		const url = it._mediaUrl
			?? it.block?.links?.[0]?.target
			?? gathered.match(_re)?.[0]
			?? followLink
			?? linkTagUrl
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
		let keepRaw = (dropTitleOn && kind === "video" && builtVideoEmbed) ? following : gathered;
		// THE HYPERLINKED LEAD. When the writer hyperlinked the WHOLE
		// line "[audio] snail, paint, trail, stain, faint, train" to its sound file, the
		// extractor counts the run as red so the tag is seen — but the words after the
		// bracket are CONTENT, exactly what a black run after a red "[audio 1]" is (BLL146),
		// and the element's own span text is not otherwise rendered here. On a block the extractor
		// marked hyperTag, the embedded lead (RenderText of the span) is folded in FRONT of
		// the own/black-after text and the rules above apply unchanged: a built video has
		// already dropped its own text as the title, audio / un-built keep the caption.
		// Scoped to the hyperlinked class: the gold mostly drops a RED-span lead's words, so
		// those stay dropped. Data: elements.media_hyperlinked_lead   Env toggle: MEDIALEAD_OFF
		const hlOn = (tpl.elements?.media_hyperlinked_lead?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.MEDIALEAD_OFF);
		if (hlOn && it.block?.hyperTag && !(dropTitleOn && kind === "video" && builtVideoEmbed)) {
			let lead = "";
			try { lead = norm ? (norm.RenderText(String(it.text ?? "")) ?? "") : ""; } catch { lead = ""; }
			if (lead && lead.trim()) keepRaw = keepRaw.trim() ? `${lead.trim()}\n${keepRaw}` : lead.trim();
		}
		// When the embed's URL came from a FOLLOWING title-anchored reference line,
		// that line IS the video's title — drop exactly it (the same title-line drop; any
		// other genuinely-following prose is kept untouched).
		if (dropTitleOn && builtVideoEmbed && followLinkLine && url === followLink) {
			keepRaw = keepRaw.split("\n").filter((L) => L.trim() !== followLinkLine).join("\n");
		}
		const rest = this.stripMediaResidue(keepRaw);
		// a gathered line that is wholly a titled video link keeps that link (see WholeLineVideoLinks), so the page's
		// video-line pass can build its embed
		const _wl = rest ? this.WholeLineVideoLinks(it._gatheredLinks ?? [], rest) : null;
		const _links = _wl && _wl.merged.length ? [...(it.block?.links ?? []), ..._wl.merged] : it.block?.links;
		if (rest) out.push(...ListsAndRuns.renderBlackText(rest, run, _links));
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
	 * decision, not something decided video-by-video. Most modules containing
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
	 * a widget — are left unaffected here; widget-embedded videos take the
	 * icon from the page-level videoIconPostpass below instead.
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
		return this.#videoIconGroup(run) ? embed.replace('class="videoSection ', 'class="videoSection icon ') : embed;
	};

	/**
	 * The icon-group decision, shared by the per-embed replace above
	 * and the page-level post-pass below. The cascade is SERIES first (the
	 * module's own product line), then the subject|template fallback:
	 *   1. a series in `icon_series`  → icon
	 *   2. a series in `plain_series` → plain (the carve-out that lets a
	 *      subject-level group solidify while its plain-majority series —
	 *      NCEA1's PHE10 / HES10 — keep the plain form)
	 *   3. else the module's subject|template in `icon_subject_template` → icon
	 * Returns false whenever the rule is off (data `enabled:false` or env
	 * VIDEOICON_OFF), so every caller stays plain together.
	 */
	static #videoIconGroup(run) {
		const rule = DataService.Data.EmitTemplates.video?.icon_rule;
		if (!rule || rule.enabled === false) return false;
		if (typeof process !== "undefined" && process.env && process.env.VIDEOICON_OFF) return false;
		const code = run?.moduleCode;
		if (!code) return false;
		const m = (DataService.Data.ModuleStructureIndex?.module_meta || {})[code] || {};
		let series = m.series;
		if (!series) {
			const g = /^([A-Za-z]+)(\d+)/.exec(code);
			series = g ? g[1] + g[2].slice(0, 2) : null;   // prefix + first two digits (fallback)
		}
		// the registry's extension (series and groups mined after its base lists) joins them unless its env is set
		const ext = rule.extension;
		const extOn = !!ext && ext.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[ext.env || "ICONEXT_OFF"]);
		const iconSeries = [...(rule.icon_series || []), ...(extOn ? ext.icon_series || [] : [])];
		const iconGroups = [...(rule.icon_subject_template || []), ...(extOn ? ext.icon_subject_template || [] : [])];
		if (iconSeries.includes(series)) return true;
		if ((rule.plain_series || []).includes(series)) return false;
		const st = (m.subject && m.template_type) ? `${m.subject}|${m.template_type}` : null;
		return !!(st && iconGroups.includes(st));
	};

	/**
	 * THE WIDGET-EMBEDDED VIDEO FOLLOWS THE ICON RULE. `#applyVideoIcon`
	 * runs at `media()`, so a video emitted by a widget builder — a carousel
	 * slide, an accordion / tab / clickDrop panel, the bilingual builder — would
	 * stay plain in an icon-group module, where the gold puts `icon` on those too.
	 * This post-pass runs LAST in ContentConverter's final-body chain and adds the
	 * token to every `class="videoSection …"` in the body that lacks it, so
	 * every emitter is covered at one point. Idempotent (a class list that
	 * already holds `icon` is untouched). Data
	 * `video.icon_rule.widget_embedded {enabled, env_off}`; env
	 * VIDEOICONWIDGET_OFF turns the post-pass off alone, VIDEOICON_OFF the
	 * whole rule.
	 */
	static videoIconPostpass(bodyHtml, run) {
		const cfg = DataService.Data.EmitTemplates.video?.icon_rule?.widget_embedded;
		if (!cfg || cfg.enabled === false) return bodyHtml;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env_off || "VIDEOICONWIDGET_OFF"]) return bodyHtml;
		if (!bodyHtml || bodyHtml.indexOf("videoSection") < 0) return bodyHtml;
		if (!this.#videoIconGroup(run)) return bodyHtml;
		return bodyHtml.replace(/class="([^"]*)"/g, (whole, cls) => {
			const toks = cls.split(/\s+/).filter(Boolean);
			if (!toks.includes("videoSection") || toks.includes("icon")) return whole;
			const i = toks.indexOf("videoSection");
			toks.splice(i + 1, 0, "icon");
			return `class="${toks.join(" ")}"`;
		});
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
	/**
	 * elements.external_link_video_embed: is the rule live? (data flag + env LINKVID_OFF)
	 */
	static LinkVideoEmbedOn(tpl) {
		const cfg = tpl.elements?.external_link_video_embed;
		return !!(cfg && cfg.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[cfg.env ?? "LINKVID_OFF"]));
	};

	/**
	 * The VIDEO-url test shared by both seams: a youtube watch / shorts / embed id,
	 * youtu.be, or a vimeo video id (a channel or user page is NOT a video). Falls back to the
	 * buttons.video_destination.host_match so the two rules can never disagree.
	 */
	static LinkVideoHost(tpl) {
		const pat = tpl.elements?.external_link_video_embed?.host_match
			?? tpl.buttons?.video_destination?.host_match
			?? "youtube\\.com/(?:watch\\?|shorts/|embed/)|youtu\\.be/|vimeo\\.com/(?:video/)?\\d";
		return new RegExp(pat, "i");
	};

	/**
	 * The url-only test shared by both seams: the link item's WHOLE PARAGRAPH (its
	 * docx block) carries no visible words once the red tag spans, the urls and the bold
	 * markers are removed — the form the gold embeds. `blackAfter` alone
	 * is NOT enough: a trailing "[link] URL" after a prose sentence ("If you need help reading
	 * the bar chart then click on this link to watch a video [link] https://…" — HPRE203,
	 * TEFUN07, XDLS908) has an empty blackAfter but many visible words before the tag, and
	 * the gold anchors that phrase inline (the prose form the class excludes).
	 */
	static LinkVideoUrlOnly(it) {
		const RED = /\u{1f534}\[RED TEXT\][\s\S]*?\[\/RED TEXT\]\u{1f534}/gu;
		const src = it?.block?.text != null ? String(it.block.text) : String(it?.blackAfter ?? "");
		return !src.replace(RED, " ").replace(/https?:\/\/[^\s\]\)"<>]+/g, " ").replace(/\*/g, "").trim();
	};

	/**
	 * Seam B — the next unconsumed item after a url-less media element, when it is a
	 * url-only [link]-family TAG item carrying a VIDEO url. Walks over already-consumed items and
	 * blank black lines; stops at the first other item. Returns { item, url } or null. The
	 * caller consumes the item.
	 */
	static FollowingVideoLinkTag(bodyItems, i, tpl) {
		if (!this.LinkVideoEmbedOn(tpl) || tpl.elements?.external_link_video_embed?.media_follow === false) return null;
		const host = this.LinkVideoHost(tpl);
		const _re = /https?:\/\/[^\s\]\)"<>]+/;
		for (let j = i + 1; j < bodyItems.length; j++) {
			const nx = bodyItems[j];
			if (!nx) return null;
			if (nx._consumed || nx.consumedBy !== undefined) continue;
			if (nx.type === "black" && !String(nx.text ?? "").trim()) continue;
			if (nx.type !== "tag") return null;
			const isExt = nx.parse?.primary?.tag === "external link"
				|| (nx.parse?.tags ?? []).some((t) => t.tag === "external link");
			if (!isExt) return null;
			const ba = String(nx.blackAfter ?? "");
			const url = nx.block?.links?.[0]?.target ?? (ba.match(_re)?.[0] ?? "");
			if (!url || !host.test(url)) return null;
			if (!this.LinkVideoUrlOnly(nx)) return null;   // a titled / prose link stays a link
			return { item: nx, url };
		}
		return null;
	};

	static gatherFollowing(it, bodyItems, i) {
		let text = it.blackAfter ?? "";
		// KB c75 (body_region.gathered_links): the gathered items' own hyperlinks, recorded beside the text
		// so a caller can weave them (#element's body default, the callout content) — read-only here
		const links = [...(it.block?.links ?? [])];
		for (let j = i + 1; j < bodyItems.length; j++) {
			const next = bodyItems[j];
			if (next.type !== "black" || next.consumedBy !== undefined) break;
			text += `\n${next.text}`;
			next._consumed = true;
			for (const l of (next.block?.links ?? [])) links.push(l);
		}
		it._gatheredLinks = links;
		return text;
	};

	/**
	 * THE TITLE-ANCHORED VIDEO LINE. Of `links` (block.links: one {text, target}
	 * per Word run), the YouTube / Vimeo links whose words — the consecutive runs
	 * of one target joined — make a WHOLE line of `text` (bold / italic /
	 * underline markers, a leading bullet and closing punctuation ignored): the
	 * writer's video reference typed as a titled line. `merged` holds one link per
	 * such line ({text: the joined words, target}), `runs` the run records it
	 * replaces. Both empty when elements.title_video_line_embed is off (env
	 * TITLEVIDEO_OFF) — the caller then keeps its links as they are.
	 *
	 * @param {Array<Object>} links - the block / gathered links
	 * @param {string} text - the text those links sit in
	 * @returns {{merged: Array<Object>, runs: Set<Object>}}
	 */
	static WholeLineVideoLinks(links, text) {
		const none = { merged: [], runs: new Set() };
		const cfg = DataService.Data.EmitTemplates.elements?.title_video_line_embed;
		if (!cfg || cfg.enabled === false) return none;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env || "TITLEVIDEO_OFF"]) return none;
		if (!Array.isArray(links) || !links.length || !text) return none;
		const hostRe = new RegExp(cfg.host_pattern ?? "youtube\\.com/(?:watch\\?|shorts/|embed/|live/)|youtu\\.be/|vimeo\\.com/(?:video/)?\\d", "i");
		const fold = (s) => String(s ?? "").replace(/\*\*|__|\*/g, "").replace(/^[\s•·]+/, "")
			.replace(/[\s.:;,]+$/, "").replace(/\s+/g, " ").trim().toLowerCase();
		const lines = new Set(String(text).split("\n").map(fold).filter(Boolean));
		const out = { merged: [], runs: new Set() };
		for (let i = 0; i < links.length; i++) {
			const target = String(links[i]?.target ?? "").trim();
			if (!hostRe.test(target)) continue;
			let words = String(links[i]?.text ?? ""), j = i + 1;
			while (j < links.length && String(links[j]?.target ?? "").trim() === target) words += String(links[j++]?.text ?? "");
			const w = fold(words);
			if (w && !/^(?:https?:|www\.)/.test(w) && lines.has(w)) {
				out.merged.push({ text: words.replace(/\s+/g, " ").trim(), target });
				for (let k = i; k < j; k++) out.runs.add(links[k]);
			}
			i = j - 1;
		}
		return out;
	};
}

// Node module export; browsers ignore it.
if (typeof module !== "undefined") module.exports = { MediaBuilder };
