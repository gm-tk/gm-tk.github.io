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
	/**
	 * A TAGGED ITEM TAKES ITS OWN LINK, NOT THE LINE'S FIRST. Several tagged items on one line ("[Button: Virtual
	 * drumming] [Button: Incredibox demo]", "[image] … [video] …") share the paragraph's one block.links list, and each
	 * read links[0] — so the second sent the learner to the first one's address. When the block holds two or more links
	 * with different targets, the item takes the link whose words stand in its OWN words (it.blackAfter). Returns the
	 * target, or null when the rule does not decide (the caller's own reading stands).
	 * Data elements.item_own_link {enabled, env ITEMOWNLINK_OFF, min_text_chars}.
	 *
	 * A MEDIA item (kind "image" / "video") takes only a link of its own kind (data kind_patterns: a picture host or file,
	 * a video host); a kind with no pattern is never re-read, and a button (no kind) takes any address.
	 *
	 * @param {Object} it - the tagged content item
	 * @param {string} [kind] - "image" / "video" for a media item; omitted for a button
	 * @returns {string|null}
	 */
	static ItemOwnLink(it, kind) {
		const cfg = DataService.Data.EmitTemplates?.elements?.item_own_link;
		if (!cfg || cfg.enabled === false) return null;
		const kindRe = kind ? (cfg.kind_patterns?.[kind] ? new RegExp(cfg.kind_patterns[kind], "i") : null) : undefined;
		if (kindRe === null) return null;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "ITEMOWNLINK_OFF"]) return null;
		const links = (it?.block?.links ?? []).filter((l) => l && String(l.target ?? "").trim());
		if (links.length < 2 || new Set(links.map((l) => String(l.target).trim())).size < 2) return null;
		const fold = (s) => String(s ?? "").replace(/[*_]/g, "").replace(/\s+/g, " ").trim().toLowerCase();
		const own = fold(it.blackAfter);
		if (!own) return null;
		const min = cfg.min_text_chars ?? 3;
		// the line's FIRST link stays the reading whenever its words are this item's own — the rule only corrects an item
		// whose own words hold another link's words and not the first one's (a garbled paste that runs two addresses
		// together, HIS1002 10.0, keeps the first)
		const first = fold(links[0].text);
		if (first.length >= min && own.includes(first)) return null;
		const hit = links.find((l) => { const t = fold(l.text); return t.length >= min && own.includes(t); });
		if (!hit || (kindRe && !kindRe.test(String(hit.target)))) return null;
		return String(hit.target).trim();
	}

	static image(it, bodyItems, i, run) {
		const tpl = DataService.Data.EmitTemplates.image;
		const out = [];
		const gathered = this.gatherFollowing(it, bodyItems, i);
		const url = this.CanonicalStockUrl(this.ItemOwnLink(it, "image") ?? it.block?.links?.[0]?.target
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
		// the address the writer typed in RED on the next line («[video] <title>» then a red «https://www.youtube.com/…»)
		// — a line the page never shows: the video takes it and consumes the line
		// (elements.media_request_before_media.red_address_line; env MEDIAREDADDR_OFF)
		let redAddrUrl;
		if (!it._mediaUrl && !(it.block?.links?.[0]?.target) && !gathered.match(_re) && !followLink && !linkTagUrl && kind === "video"
			&& !(_urlInTextOn && String(it.text || "").match(_re)) && !this.ItemOwnLink(it, kind)) {
			const hit = this.#nextRedAddress(bodyItems, i, tpl);
			if (hit) { redAddrUrl = hit.url; hit.item._consumed = true; }
		}
		// it._mediaUrl: the URL a caller has already judged to be this element's own (the media-item video route)
		const url = it._mediaUrl
			?? this.ItemOwnLink(it, kind)
			?? it.block?.links?.[0]?.target
			?? gathered.match(_re)?.[0]
			?? followLink
			?? linkTagUrl
			?? (_urlInTextOn ? String(it.text || "").match(_re)?.[0] : undefined)
			?? redAddrUrl
			// a numbered tag («[Item 1] [Video] <title>») with no address of its own takes its Media List row's
			// (elements.media_list_item_row; env MLITEMROW_OFF) — read last, after every address on the page; an
			// address the page cannot embed is kept for the developer's flag below (it._mlRowUrl), not framed
			?? this.#mediaListRowEmbedUrl(it, kind, run)
			?? "";

		let builtVideoEmbed = false;
		// THE AUDIO ANIMATION IS A VIDEO: an audio-resolved tag whose own words name an animation («[Audio animation]») is
		// the audiovisual team's animation video — the video embed when a YouTube / Vimeo address is found, otherwise the
		// video frame shell and a developer To Do (never an empty audio player). Data elements.audio_animation; env
		// AUDIOANIM_OFF.
		const aa = tpl.elements?.audio_animation;
		const animation = kind === "audio" && !!aa && aa.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[aa.env ?? "AUDIOANIM_OFF"])
			&& new RegExp(aa.tag_pattern ?? "\\banimation\\b", "i").test(String(it.text ?? ""));
		if (animation) {
			const videoId = url.match(new RegExp(acks.youtube_id))?.[1] ?? null;
			if (videoId) {
				let embed = Utils.FillTemplate(tpl.video.youtube, { videoId, params: "" });
				if (run.conventions?.videoHost === "youtube") embed = embed.replace("youtube-nocookie.com", "youtube.com");
				out.push(this.#applyVideoIcon(embed, run));
			} else if (url && new RegExp(aa.video_pattern ?? "youtu\\.?be|youtube\\.com|vimeo\\.com", "i").test(url)) {
				out.push(this.#applyVideoIcon(Utils.FillTemplate(tpl.video.generic_iframe, { url: Utils.EscapeHtml(url) }), run));
			} else {
				const tag = (String(it.text ?? "").match(/\[[^\]]*\]/) ?? [String(it.text ?? "").trim()])[0].replace(/\s+/g, " ");
				const link = url ? Utils.FillTemplate(aa.link_text ?? " The writer's link: {url}", { url }) : "";
				out.push(Utils.FillTemplate(tpl.red_flag.todo_form, { text: Utils.EscapeHtml(Utils.FillTemplate(aa.todo_text ?? "{tag}{link}", { tag, link })) }));
				out.push(aa.frame);
			}
		} else if (kind === "audio") {
			const file = url.split("/").pop() || tpl.audio.default_filename;
			out.push(Utils.FillTemplate(tpl.audio.form, {
				filename: Utils.EscapeHtml(/\.\w{2,4}$/.test(file) ? file : tpl.audio.default_filename),
				title: "",
			}));
		} else {
			const videoId = url.match(new RegExp(acks.youtube_id))?.[1] ?? null;
			if (videoId) {
				let embed = Utils.FillTemplate(tpl.video.youtube, { videoId, params: this.#timeParams(it, bodyItems, i, run, videoId) });
				if (run) (run._timeParamsIds ??= new Set()).add(videoId);   // the page post-pass leaves this id alone
				// the embed HOST follows the module's group convention
				// (Html_Convention_Registry; global default is nocookie)
				if (run.conventions?.videoHost === "youtube") {
					embed = embed.replace("youtube-nocookie.com", "youtube.com");
				}
				out.push(this.#applyVideoIcon(embed, run));
				builtVideoEmbed = true;
			} else if (url && this.#loginWall(url)) {
				// a login-walled address (the audiovisual team's SharePoint draft, or the request document itself) is the
				// developer's record, not a learner frame: the red flag naming the line and the address, over the empty
				// frame shell (elements.video_login_wall and its document_hosts; env VIDLOGINWALL_OFF / VIDLOGINWALLDOC_OFF)
				const lw = tpl.elements.video_login_wall;
				out.push(this.MediaListRowFlag(it, run, url, undefined, this.#loginWall(url).flag ?? lw.flag));
				out.push(lw.shell ?? '<div class="videoSection ratio ratio-16x9">\n<iframe></iframe>\n</div>');
				builtVideoEmbed = true;   // the line's own words (the video's name, its link) are the flag's; the shell stands for the frame
			} else if (url) {
				out.push(this.#applyVideoIcon(Utils.FillTemplate(tpl.video.generic_iframe, { url: Utils.EscapeHtml(url) }), run));
				builtVideoEmbed = true;
			} else {
				// the writer's request about the NEXT video («[please embed video with image and play button]» then «[Video link]
				// <address>») ships as their Writers Note, not as a missing-source flag (elements.media_request_before_media)
				const req = this.#requestBeforeMedia(it, bodyItems, i, kind, run);
				if (req !== null) out.push(...req);
				else if (it._mlRowUrl) out.push(this.MediaListRowFlag(it, run, it._mlRowUrl));
				else out.push(this.NoUrlFlag(it, kind, run));
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
	/**
	 * THE WRITER'S CROP TIMES ON A BUILT YOUTUBE EMBED. A writer types where the video should start and stop after its
	 * link («[LINK: …] (0:10- 2:12)», «Start 0.56 Finish 1.40 mins», «Start at 0:23 seconds, cut at 3:22.»); the embed
	 * builds and drops its own words, so the instruction reached no output, while the human build appends it to the
	 * embed's address. ONE crop is read from the tag's own paragraph (addresses removed): a single range, or a start /
	 * finish pair; two ranges, a duration alone or an end before the start give none. Start 0 is omitted.
	 * Data elements.video_time_range; env VIDTIME_OFF.
	 * The red spans that FOLLOW the tag in the same paragraph («[video] <address> 🔴(0.27-3:06)🔴») are read too, up to the
	 * next element tag — next_spans; env VIDTIMENEXT_OFF.
	 * @param {object} it - the video tag's body item
	 * When the tag's own line holds no crop, the ONE crop written in the video's Media List row(s) — matched by the video
	 * id, the row's visible words — is used (media_list_row; env VIDTIMEML_OFF); rows with two different crops give none.
	 * @param {object[]} [bodyItems] - the page's items (for the following spans)
	 * @param {number} [i] - the item's index
	 * @param {ConversionRun} [run] - the run (its mediaItems)
	 * @param {string} [videoId] - the YouTube id (for the Media List row)
	 * @returns {string} the embed address's query («?start=10&amp;end=132») or ""
	 */
	static #timeParams(it, bodyItems, i, run, videoId) {
		const c = DataService.Data.EmitTemplates.elements?.video_time_range;
		if (!c || c.enabled === false || (typeof process !== "undefined" && process.env && process.env[c.env ?? "VIDTIME_OFF"])) return "";
		const RED = /\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu;
		let raw = `${String(it?.text ?? "")} ${String(it?.blackAfter ?? "")}`;
		const nx = c.next_spans;
		if (nx && nx.enabled !== false && Array.isArray(bodyItems) && Number.isInteger(i) && it?.block
			&& !(typeof process !== "undefined" && process.env && process.env[nx.env ?? "VIDTIMENEXT_OFF"])) {
			for (let j = i + 1; j < bodyItems.length && bodyItems[j]?.block === it.block; j++) {
				const n = bodyItems[j];
				if (n.type === "tag" && n.parse?.primary) break;      // the next element of the paragraph
				raw += ` ${String(n.text ?? "")} ${String(n.blackAfter ?? "")}`;
			}
		}
		const read = (words) => this.#readCrop(words, c);
		let got = read(raw);
		// the video's Media List row(s), when the line itself holds no crop — media_list_row; env VIDTIMEML_OFF
		const ml = c.media_list_row;
		if (got === null && videoId && ml && ml.enabled !== false && Array.isArray(run?.mediaItems)
			&& !(typeof process !== "undefined" && process.env && process.env[ml.env ?? "VIDTIMEML_OFF"])) {
			const seen = new Map();
			for (const m of run.mediaItems) {
				if (!String(m?.url ?? "").includes(videoId) && !String(m?.rowText ?? "").includes(videoId)) continue;
				const r = read(m.rowText);
				if (r !== null) seen.set(JSON.stringify(r), r);
			}
			if (seen.size === 1) got = [...seen.values()][0];
		}
		return this.#cropQuery(got);
	}

	/**
	 * One crop from a run of the writer's words (red markers, links and addresses removed): { start, end } (either may be
	 * null), null when none, "multi" when two ranges. Data elements.video_time_range (its patterns and up_to).
	 * @param {string} words - the words to read
	 * @param {object} c - elements.video_time_range
	 * @returns {object|string|null} the crop
	 */
	static #readCrop(words, c) {
		const RED = /\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu;
		const sec = (m, s) => Number(m) * 60 + Number(s);
		const text = String(words ?? "").replace(RED, " ").replace(/\[LINK:[^\]]*\]/g, " ").replace(/https?:\/\/\S+/g, " ");
		let ranges = [...text.matchAll(new RegExp(c.range_pattern, "gi"))];
		// «starting at 0:07, to 0:22» — a comma before the range's «to» (range_comma; env VIDTIMECOMMA_OFF)
		const rc = c.range_comma;
		if (!ranges.length && rc && rc.enabled !== false && rc.pattern
			&& !(typeof process !== "undefined" && process.env && process.env[rc.env ?? "VIDTIMECOMMA_OFF"])) {
			ranges = [...text.matchAll(new RegExp(rc.pattern, "gi"))];
		}
		if (ranges.length > 1) return "multi";
		if (ranges.length === 1) return { start: sec(ranges[0][1], ranges[0][2]), end: sec(ranges[0][3], ranges[0][4]) };
		const s = text.match(new RegExp(c.start_pattern, "i")), e = text.match(new RegExp(c.end_pattern, "i"));
		// a start in seconds alone («start at 42 seconds», «start at :58») — start_seconds_pattern
		const ss = !s && c.start_seconds_pattern ? text.match(new RegExp(c.start_seconds_pattern, "i")) : null;
		// «(up to 1:38)», «until 3:16» — up_to; env VIDTIMEUPTO_OFF
		const ut = c.up_to;
		const u = !e && ut && ut.enabled !== false && ut.pattern
			&& !(typeof process !== "undefined" && process.env && process.env[ut.env ?? "VIDTIMEUPTO_OFF"])
			? text.match(new RegExp(ut.pattern, "i")) : null;
		const start = s ? sec(s[1], s[2]) : (ss ? Number(ss[1] ?? ss[2]) : null);
		const end = e ? sec(e[1], e[2]) : (u ? sec(u[1], u[2]) : null);
		return start === null && end === null ? null : { start, end };
	}

	/** A crop as the embed address's query («?start=10&amp;end=132»; start omitted at 0), or "" for none / an end before
	 *  the start / two ranges. */
	static #cropQuery(got) {
		if (got === null || got === "multi" || !got) return "";
		const { start, end } = got;
		if (start !== null && end !== null && end <= start) return "";
		const p = [];
		if (start) p.push(`start=${start}`);
		if (end !== null) p.push(`end=${end}`);
		return p.length ? `?${p.join("&amp;")}` : "";
	}

	/**
	 * THE CROP OF A VIDEO BUILT INSIDE A WIDGET. A carousel slide's, a tab's or an accordion panel's YouTube embed is built
	 * by its widget builder from the video id alone, so the crop the writer typed beside the video («[Video starting at
	 * 0:07, to 0:22] <address>», a Media List row's «<address> (Please start video at 1:00)») never reached it. This page
	 * post-pass gives a YouTube embed with no query whose id the media builder never handled the ONE crop written beside
	 * that id in the Writers Template — the paragraph that holds it, or the table cell (else the row) — or in its Media
	 * List row; two different crops give none. Data elements.video_time_range.widget_postpass; env VIDTIMEWIDGET_OFF.
	 * @param {string} bodyHtml - the page body
	 * @param {ConversionRun} run - the run (wtBlocks, mediaItems, the ids the media builder handled)
	 * @returns {string} the body
	 */
	static videoTimePostpass(bodyHtml, run) {
		const c = DataService.Data.EmitTemplates.elements?.video_time_range;
		const w = c?.widget_postpass;
		if (!c || c.enabled === false || !w || w.enabled === false) return bodyHtml;
		if (typeof process !== "undefined" && process.env && (process.env[c.env ?? "VIDTIME_OFF"] || process.env[w.env ?? "VIDTIMEWIDGET_OFF"])) return bodyHtml;
		if (!bodyHtml || bodyHtml.indexOf("/embed/") < 0) return bodyHtml;
		const done = run?._timeParamsIds ?? new Set();
		const cache = new Map();
		return bodyHtml.replace(/(youtube(?:-nocookie)?\.com\/embed\/)([\w-]{11})(?=")/g, (whole, host, id) => {
			if (done.has(id)) return whole;
			if (!cache.has(id)) cache.set(id, this.#cropFor(id, run, c));
			return whole + cache.get(id);
		});
	}

	/**
	 * A STOCK PICTURE IS NEVER A WEBSITE BUTTON. Through several authoring forms («[image] <address>» after a modal, an
	 * activity table's picture cell, a tile's picture, «Image: iStock: stepping stone: <address>») an iStock picture's
	 * address reached the external-destination rule and shipped as «Go to website», or as the address of the writer's own
	 * button («Yes», «Go to journal»), while the human build shows the picture. This page post-pass renders such an
	 * address as the picture placeholder (the image path's own form): a button carrying a default label is replaced by the
	 * picture; a writer's labelled button keeps its label with an empty link, and the picture follows it.
	 * Data image.stock_button {host_pattern, default_labels}; env STOCKBUTTON_OFF.
	 * @param {string} bodyHtml - the page body
	 * @param {ConversionRun} run - the run (image mode, iStock titles)
	 * @returns {string} the body
	 */
	static stockButtonPostpass(bodyHtml, run) {
		const tpl = DataService.Data.EmitTemplates.image;
		const c = tpl?.stock_button;
		if (!c || c.enabled === false) return bodyHtml;
		if (typeof process !== "undefined" && process.env && process.env[c.env ?? "STOCKBUTTON_OFF"]) return bodyHtml;
		if (!bodyHtml || bodyHtml.indexOf("externalButton") < 0) return bodyHtml;
		const host = new RegExp(c.host_pattern ?? "^https?:\\/\\/(?:www\\.)?istockphoto\\.com\\/", "i");
		const defaults = new Set((c.default_labels ?? ["Go to website"]).map((l) => Utils.Fold(l)));
		return bodyHtml.replace(/<a href="([^"]*)" target="_blank"><div class="externalButton">([^<]*)<\/div><\/a>/g, (whole, href, label) => {
			const url = Utils.DecodeHtml ? Utils.DecodeHtml(href) : href.replace(/&amp;/g, "&");
			if (!host.test(url)) return whole;
			const id = this.CanonicalStockUrl(url).match(/gm-?(\d{6,10})/)?.[1] ?? null;
			if (!id) return whole;
			const pic = run?.imageMode === "P"
				? [this.FinishImg(Utils.FillTemplate(tpl.mode_P.visible, { label: `iStock-${id}` }), url, id, run),
					this.FinishImg(Utils.FillTemplate(tpl.mode_P.comment, { filename: Utils.FillTemplate(tpl.filename_rules.istock, { id }) }), url, id, run)].join("\n")
				: this.FinishImg(Utils.FillTemplate(tpl.mode_D.visible, { filename: Utils.FillTemplate(tpl.filename_rules.istock, { id }) }), url, id, run);
			if (defaults.has(Utils.Fold(label))) return pic;
			return `<a href="" target="_blank"><div class="externalButton">${label}</div></a>\n${pic}`;
		});
	}

	/** The one crop written beside a video id in the run's Writers Template blocks and Media List rows, as a query. */
	static #cropFor(id, run, c) {
		const seen = new Map();
		const add = (words) => {
			const r = this.#readCrop(words, c);
			if (r === "multi") seen.set("multi", r);
			else if (r) seen.set(JSON.stringify(r), r);
		};
		const has = (s) => String(s ?? "").includes(id);
		for (const b of (run?.wtBlocks ?? [])) {
			if (b?.kind === "para") {
				if (has(b.text) || (b.links ?? []).some((l) => has(l?.target))) add(b.text);
			} else if (b?.kind === "table" && Array.isArray(b.rows)) {
				b.rows.forEach((cells, r) => {
					const inCells = (cells ?? []).filter((x) => has(x));
					if (inCells.length) inCells.forEach(add);
					else if ((b.rowLinks?.[r] ?? []).some((l) => has(l?.target))) add((cells ?? []).join(" ║ "));
				});
			}
		}
		for (const m of (run?.mediaItems ?? [])) if (has(m?.url) || has(m?.rowText)) add(m.rowText);
		if (seen.size !== 1 || seen.has("multi")) return "";
		return this.#cropQuery([...seen.values()][0]);
	}

	/**
	 * The missing-source flag of an address-less media tag. When the tag's line is the writer's brackets only and they
	 * carry words beyond the bare kind («[Insert video – 1. section one teaching]», «[Insert Video Item 4]», «[Video]
	 * [Audiovisual item 11]»), the flag names those brackets, verbatim, in place of «[video]» — the developer's only
	 * record of WHICH video goes there. A line with words outside its brackets keeps the bare flag (media_free_note ships
	 * those words as the Writers Note). Data elements.no_url_writer_tag; env NOURLTAG_OFF.
	 * @param {object} it - the media tag's body item
	 * @param {string} kind - "video" / "embed" / …
	 * @param {ConversionRun} run - the current conversion run
	 * @returns {string} the red flag's HTML
	 */
	/**
	 * The Media List row a NUMBERED media tag with no address of its own points at («[Item 1] [Video] Youtube Matike
	 * Maranga (Karaoke)»): the row with the tag's number where the list numbers its rows; else, among the rows of the
	 * tag's kind that carry an address, the one sharing the most of the tag's title words (kind words removed) with the
	 * row's visible words, weighted up when the row's page is the tag's block's own page (the acknowledgements' page-record
	 * evidence, counted only when the run trusts the page records) — a unique best with a positive score; a title-less tag
	 * takes only a unique same-page row. Data elements.media_list_item_row; env MLITEMROW_OFF. The bilingual cell's video
	 * part (BilingualBuilder) resolves through the same reading.
	 * @param {Object} it - the media tag's body item (text, blackAfter, block.wtPage)
	 * @param {string} kind - "video" / "audio" / "embed"
	 * @param {ConversionRun} run - the run (its mediaItems, pageRecordsUsable)
	 * @returns {string|undefined} the row's address, or undefined when the rule does not decide
	 */
	static MediaListRowUrl(it, kind, run) {
		const c = DataService.Data.EmitTemplates.elements?.media_list_item_row;
		if (!c || c.enabled === false || (typeof process !== "undefined" && process.env && process.env[c.env ?? "MLITEMROW_OFF"])) return undefined;
		if (!(c.kinds ?? ["video"]).includes(kind) || !Array.isArray(run?.mediaItems) || !run.mediaItems.length) return undefined;
		const RED = /\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu;
		const own = `${String(it?.text ?? "")} ${String(it?.blackAfter ?? "")}`.replace(RED, " ");
		const ref = own.match(new RegExp(c.item_pattern ?? "\\[\\s*(?:insert\\s+)?(?:media\\s+)?item\\s*(\\d*)\\s*\\]", "i"));
		if (!ref) return undefined;
		const n = parseInt(ref[1], 10);
		const num = (s) => parseInt(String(s ?? "").replace(/\D/g, ""), 10);
		const items = run.mediaItems;
		// a mail-safety wrapper around the address («…safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.youtube…»)
		// is unwrapped (unwrap_pattern: its first group is the encoded address)
		const unwrapRe = c.unwrap_pattern ? new RegExp(c.unwrap_pattern, "i") : null;
		const addr = (m) => {
			const u = String(m?.url ?? "").trim();
			const w = unwrapRe ? u.match(unwrapRe) : null;
			if (!w) return u;
			try { return decodeURIComponent(w[1]); } catch { return u; }
		};
		// a row embeds once: the rows this reading has already given to an earlier tag of the run — the same writer's
		// line asked again (a bilingual row's second language cell) is the same tag, not an earlier one
		const used = (run._mlRowsUsed ??= new Map());
		const key = own.replace(/\s+/g, " ").trim().toLowerCase();
		const take = (m) => { if (!used.has(m)) used.set(m, key); return addr(m); };
		// (1) the writer's number, where the list numbers its rows (a number that finds no addressed row falls to the words)
		if (Number.isInteger(n) && items.some((m) => Number.isInteger(num(m.itemNo)))) {
			const hit = items.find((m) => num(m.itemNo) === n);
			if (hit && addr(hit)) return take(hit);
		}
		// (2) the row of the tag's kind whose visible words hold the tag's title words
		const fold = (s) => String(s ?? "").replace(RED, " ").replace(/\[LINK:[^\]]*\]/g, " ").replace(/https?:\/\/\S+/g, " ")
			.replace(/[*_]/g, "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
		const kindWords = new Set(c.kind_words ?? []);
		const minLen = c.min_word_chars ?? 2;
		const title = new Set(fold(own.replace(/\[[^[\]]*\]/g, " ")).split(" ").filter((w) => w.length >= minLen && !kindWords.has(w)));
		const typeRe = new RegExp(c.row_type_pattern ?? "video", "i");
		const page = run.pageRecordsUsable && Number.isInteger(it?.block?.wtPage) ? it.block.wtPage : null;
		const weight = c.same_page_weight ?? 10;
		const penalty = c.used_penalty ?? 5;
		const scored = [];
		for (const m of items) {
			if (!typeRe.test(String(m?.itemType ?? "")) || !addr(m)) continue;
			const rw = new Set(fold(m.rowText ?? `${m.description ?? ""} ${m.source ?? ""}`).split(" "));
			let s = [...title].filter((w) => rw.has(w)).length;
			if (page !== null && m.wtPage === page) s += weight;
			if (used.has(m) && used.get(m) !== key) s -= penalty;   // a row an earlier tag took is this tag's only when nothing else names it
			if (s > 0) scored.push({ m, s });
		}
		if (!title.size && !(page !== null)) return undefined;
		scored.sort((a, b) => b.s - a.s);
		if (!scored.length || (scored.length > 1 && scored[0].s === scored[1].s)) return undefined;
		if (!title.size && scored[0].s < weight) return undefined;
		return take(scored[0].m);
	}

	/** The Media List row's address when the page can embed it (embed_host_pattern); otherwise it is kept on
	 *  it._mlRowUrl for the developer's flag and undefined is returned. */
	static #mediaListRowEmbedUrl(it, kind, run) {
		const url = this.MediaListRowUrl(it, kind, run);
		if (!url) return undefined;
		if (this.MediaListRowEmbeddable(url)) return url;
		it._mlRowUrl = url;
		return undefined;
	}

	/** True when a Media List row's address is on a host the page embeds (data media_list_item_row.embed_host_pattern;
	 *  no pattern = every address). */
	static MediaListRowEmbeddable(url) {
		const c = DataService.Data.EmitTemplates.elements?.media_list_item_row;
		if (!c || !c.embed_host_pattern) return true;
		return new RegExp(c.embed_host_pattern, "i").test(String(url ?? ""));
	}

	/**
	 * The developer's flag for a Media List address the page cannot embed: the writer's own line and the address, so
	 * whoever finishes the page knows which file to re-host (data media_list_item_row.not_embeddable_flag).
	 * @param {Object} it - the media tag's body item (its text names the writer's line)
	 * @param {ConversionRun} run - the run
	 * @param {string} url - the row's address
	 * @param {string} [label] - the line to name (default: the tag's own words)
	 * @param {string} [template] - the flag's wording (default: media_list_item_row.not_embeddable_flag)
	 * @returns {string} the red flag's HTML
	 */
	static MediaListRowFlag(it, run, url, label, template) {
		const c = DataService.Data.EmitTemplates.elements?.media_list_item_row ?? {};
		const RED = /\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu;
		const l = (label ?? `${String(it?.text ?? "")} ${String(it?.blackAfter ?? "")}`).replace(RED, " ").replace(/https?:\/\/\S+/g, " ")
			.replace(/\s+/g, " ").trim();
		return NotesAndComments.redFlag(Utils.FillTemplate(template ?? c.not_embeddable_flag
			?? "{label} — the Media List address is not one the page can embed; re-host the video: {url}", { label: l, url }), run);
	}

	/**
	 * The login-wall form for a widget builder's own video frame (a carousel slide): the red flag naming the slide's
	 * words and the address, then the empty frame shell — or null when the page may frame the address. The same reading
	 * as media()'s (elements.video_login_wall and its document_hosts); the caller's own switch decides whether to ask.
	 * @param {string} url - the slide's address
	 * @param {string} [label] - the slide's words
	 * @param {ConversionRun} [run] - the run
	 * @returns {string|null} the flag and the shell, or null
	 */
	static LoginWallFrame(url, label, run) {
		const hit = this.#loginWall(url);
		if (!hit) return null;
		const lw = DataService.Data.EmitTemplates.elements.video_login_wall;
		const it = { text: String(label ?? ""), blackAfter: "" };
		const r = run && typeof run.CountRedFlag === "function" ? run : { CountRedFlag() {} };   // a caller without the run still gets the flag
		return `${this.MediaListRowFlag(it, r, url, undefined, hit.flag ?? lw.flag)}\n${lw.shell ?? '<div class="videoSection ratio ratio-16x9">\n<iframe></iframe>\n</div>'}`;
	}

	/** The login-wall block a video address falls under — the block itself (a SharePoint video file, host_pattern) or its
	 *  document_hosts sub-block (the request document, its own flag wording) — or null when the page may frame the address
	 *  (data elements.video_login_wall; off, or no pattern, = never). */
	static #loginWall(url) {
		const c = DataService.Data.EmitTemplates.elements?.video_login_wall;
		if (!c || c.enabled === false || !c.host_pattern
			|| (typeof process !== "undefined" && process.env && process.env[c.env ?? "VIDLOGINWALL_OFF"])) return null;
		const u = String(url ?? "");
		if (new RegExp(c.host_pattern, "i").test(u)) return c;
		const d = c.document_hosts;
		if (d && d.enabled !== false && d.host_pattern
			&& !(typeof process !== "undefined" && process.env && process.env[d.env ?? "VIDLOGINWALLDOC_OFF"])
			&& new RegExp(d.host_pattern, "i").test(u)) return d;
		return null;
	}

	static NoUrlFlag(it, kind, run) {
		let label = `[${kind}]`;
		const c = DataService.Data.EmitTemplates.elements?.no_url_writer_tag;
		if (c && c.enabled !== false && !(typeof process !== "undefined" && process.env && process.env[c.env ?? "NOURLTAG_OFF"])) {
			const RED = /\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu;
			const text = String(it?.text ?? "").replace(RED, " ").replace(/\s+/g, " ").trim();
			const brackets = text.match(/\[[^[\]]*\]/g) ?? [];
			if (brackets.length && !/[\p{L}\p{N}]/u.test(text.replace(/\[[^[\]]*\]/g, " "))) {
				const kindWords = new Set(c.kind_words ?? ["insert", "video", "embed", "link", "interactive"]);
				const words = Utils.Fold(brackets.join(" ").replace(/[[\]]/g, " ")).replace(/[^\p{L}\p{N}]+/gu, " ").split(" ")
					.filter((w) => w && !kindWords.has(w));
				if (words.length) label = brackets.map((b) => b.replace(/^\[\s+/, "[").replace(/\s+\]$/, "]")).join(" ");
			}
		}
		return NotesAndComments.redFlag(`${label} with no URL found — add the ${kind} source.`, run);
	}

	/**
	 * A media tag with no address whose NEXT item (blank lines skipped) is a media tag of a listed kind is the writer's
	 * request about that next element, not a missing source: its own words (the kind words aside) ship as the red
	 * Writers Note, and a bare tag («[Video Link]» before «[video link][item 28]») ships nothing. Null = not this form
	 * (the missing-source flag as before). Data elements.media_request_before_media; env MEDIAREQNEXT_OFF.
	 */
	static #requestBeforeMedia(it, bodyItems, i, kind, run) {
		const c = DataService.Data.EmitTemplates.elements?.media_request_before_media;
		if (!c || c.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env[c.env ?? "MEDIAREQNEXT_OFF"]) return null;
		if (!(c.kinds ?? ["video"]).includes(kind) || !Array.isArray(bodyItems)) return null;
		let j = i + 1;
		while (j < bodyItems.length && bodyItems[j]?.type === "black" && !String(bodyItems[j].text ?? "").trim()) j++;
		const nx = bodyItems[j];
		if (!nx) return null;
		const RED = /\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu;
		// the next tag must carry the address — on its own line or the plain lines after it, where the video gathers it
		// (a run of address-less videos is each its own missing source)
		const addr = /https?:\/\/\S/;
		const hasAddr = (x) => (x?.block?.links ?? []).some((l) => String(l?.target ?? "").trim())
			|| addr.test(String(x?.text ?? "")) || addr.test(String(x?.blackAfter ?? ""));
		const tagNext = () => {
			if (nx.type !== "tag" || nx.parse?.instructionFragment) return false;
			if (!(c.next_tags ?? ["video"]).includes(String(nx.parse?.primary?.tag ?? "").toLowerCase())) return false;
			let found = hasAddr(nx);
			for (let k = j + 1; !found && k < bodyItems.length && bodyItems[k]?.type === "black"; k++) found = hasAddr(bodyItems[k]);
			return found;
		};
		// or the next line holds ONLY a video address — black, perhaps in (red) brackets — the line the video embeds from
		// («(https://www.youtube.com/watch?v=…)»); a red address the page never shows is not this form (address_line)
		const ac = c.address_line;
		const lineOn = !!ac && ac.enabled !== false
			&& !(typeof process !== "undefined" && process.env && process.env[ac.env ?? "MEDIAREQADDR_OFF"]);
		const addressLine = () => {
			if (!lineOn) return false;
			const black = String(nx.type === "tag" ? (nx.blackAfter ?? "") : (nx.text ?? ""));
			if (/\u{1f534}/u.test(black)) return false;
			if (nx.type === "tag" && /[\p{L}\p{N}]/u.test(String(nx.text ?? "").replace(RED, " "))) return false;
			const urls = black.match(/https?:\/\/\S+/g) ?? [];
			if (urls.length !== 1 || black.replace(/https?:\/\/\S+/g, " ").replace(/[\s()[\]]+/g, "")) return false;
			return new RegExp(ac.host_pattern ?? "youtu\\.?be|youtube\\.com|vimeo\\.com", "i").test(urls[0]);
		};
		if (!tagNext() && !addressLine()) return null;
		const text = String(it.text ?? "").replace(RED, " ").replace(/\s+/g, " ").trim();
		const kindWords = new Set(c.kind_words ?? ["insert", "video", "link", "embed", "clip", "item"]);
		const rest = Utils.Fold(text.replace(/[[\]]/g, " ")).replace(/[^\p{L}\p{N}]+/gu, " ").split(" ")
			.filter((w) => w && !kindWords.has(w) && !/^\d+$/.test(w));
		// the writer's timestamps («[Video 0:29- 0:46]») are words too (address_line.keep_pattern)
		const keep = lineOn && !!ac.keep_pattern && new RegExp(ac.keep_pattern).test(text);
		if (rest.length < (c.min_words ?? 2) && !keep) return [];
		return [NotesAndComments.redFlag(text, run, "cs")];
	}

	/**
	 * The next unconsumed item after an address-less video, when it is a line holding ONLY one red YouTube / Vimeo
	 * address (its black words brackets at most) — the address the writer typed for that video, which no other reader
	 * shows. Returns { item, url } or null; the caller consumes the item.
	 * Data elements.media_request_before_media.red_address_line; env MEDIAREDADDR_OFF.
	 */
	static #nextRedAddress(bodyItems, i, tpl) {
		const c = tpl.elements?.media_request_before_media?.red_address_line;
		if (!c || c.enabled === false || !Array.isArray(bodyItems)) return null;
		if (typeof process !== "undefined" && process.env && process.env[c.env ?? "MEDIAREDADDR_OFF"]) return null;
		const RED = /\u{1f534}\[RED TEXT\]|\[\/RED TEXT\]\u{1f534}/gu;
		for (let j = i + 1; j < bodyItems.length; j++) {
			const nx = bodyItems[j];
			if (!nx) return null;
			if (nx._consumed || nx.consumedBy !== undefined) continue;
			if (nx.type === "black" && !String(nx.text ?? "").trim()) continue;
			if (nx.type !== "tag" || nx.parse?.primary) return null;               // a parsed tag is its own element
			if (String(nx.blackAfter ?? "").replace(/[\s()[\]]+/g, "")) return null;
			const red = String(nx.text ?? "").replace(RED, " ");
			const urls = red.match(/https?:\/\/[^\s()[\]]+/g) ?? [];
			if (urls.length !== 1 || red.replace(/https?:\/\/[^\s()[\]]+/g, " ").replace(/[\s()[\]]+/g, "")) return null;
			if (!new RegExp(c.host_pattern ?? "youtu\\.?be|youtube\\.com|vimeo\\.com", "i").test(urls[0])) return null;
			return { item: nx, url: urls[0] };
		}
		return null;
	}

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
