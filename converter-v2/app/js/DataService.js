/**
 * DataService.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Handles ALL data fetching for the app — the runtime data files in
 * ../data/ at startup, and the YouTube oEmbed metadata fetch during acks
 * generation. Nothing else in the app fetches. This is where we talk to
 * the outside world.
 *
 * WHY SEPARATE FILE:
 * Standards §2: all HTTP traffic lives in one data layer. If a data file
 * moves or the oEmbed endpoint changes, this is the only file (plus
 * Config/Acks_Formats data) that cares.
 *
 * WHEN TO WORK HERE:
 * - A new runtime data file is added (also add it to Config.DataFiles)
 * - Fetch/caching behaviour needs adjusting
 *
 * FAILURE PHILOSOPHY:
 * Data files are load-or-die: a converter running on partial rules would
 * "handle" things silently, which is exactly the bug this project bans —
 * so a missing/invalid data file stops startup with a clear message.
 * oEmbed, by contrast, degrades per the acks spec: a failed fetch becomes
 * a visible ACK-TODO[video-meta], never a fabricated field.
 * ===========================================================================
 */

class DataService {

	// All loaded data files, keyed like Config.DataFiles. Filled by Init().
	static Data = {};

	// oEmbed responses cached by video id — repeat videos in one module
	// (or repeat runs in one session) cost one request total.
	static #oembedCache = new Map();

	/**
	 * Loads every runtime data file in parallel and validates the result.
	 *
	 * HOW IT WORKS:
	 * Builds one fetch task per Config.DataFiles entry, awaits them all
	 * (Promise.all — standards §7b), stores under DataService.Data.
	 *
	 * @returns {Promise<void>} resolves when all data is ready
	 * @throws {Error} when any file fails to load or parse
	 */
	static async Init() {
		const entries = Object.entries(Config.DataFiles);
		const results = await Promise.all(
			entries.map(([key, url]) => this.#fetchJSON(url).then((json) => [key, json]))
		);
		for (const [key, json] of results) this.Data[key] = json;

		// sanity guards — fail loudly NOW, not mid-conversion
		if (!this.Data.TagLexicon?.tags) throw new Error("Tag_Lexicon.json loaded but has no tags");
		if (!this.Data.StyleRegistry?.defaults) throw new Error("Style_Anchor_Registry.json loaded but has no defaults");
		if (!this.Data.EmitTemplates?.red_flag) throw new Error("Emit_Templates.json loaded but has no red_flag form");

		console.log(`🟢 DataService: ${entries.length} runtime data files loaded`);
	};

	/**
	 * Generic JSON fetcher — load-or-die (no fallback data: see the
	 * failure philosophy in the header).
	 *
	 * @param {string} url - relative path to the JSON file
	 * @returns {Promise<Object>} parsed JSON
	 */
	static async #fetchJSON(url) {
		try {
			// { cache: 'no-store' } so a freshly-edited data file is always
			// re-read on reload — the edit-data → reload → convert workflow
			const response = await fetch(url, { cache: "no-store" });
			if (!response.ok) throw new Error(`HTTP ${response.status}`);
			return await response.json();
		} catch (error) {
			console.error(`🔴 DataService: failed to load ${url}:`, error.message);
			throw new Error(`Could not load required data file: ${url} (${error.message})`);
		}
	};

	/**
	 * Fetches YouTube title/channel via the keyless oEmbed endpoint.
	 *
	 * WHAT IT RETURNS:
	 * { ok: true, title, channel }            on success
	 * { ok: false, reason: 'unavailable' | 'offline' | 'error' }  on failure
	 * — the reason strings match Acks_Formats.json ack_todo.types.video-meta.
	 *
	 * DATA SHAPE (real response, verified 12/06/26):
	 * { "title": "FORGOTTEN FIBRE", "author_name": "1News",
	 *   "provider_name": "YouTube", ... }   ← only title/author_name are used
	 *
	 * @param {string} videoUrl - the writer's pasted YouTube URL
	 * @param {string} videoId  - extracted 11-char id (cache key)
	 * @returns {Promise<Object>} result object as above
	 */
	static async FetchOembed(videoUrl, videoId) {
		if (this.#oembedCache.has(videoId)) return this.#oembedCache.get(videoId);

		const cfg = this.Data.AcksFormats.oembed;
		const url = Utils.FillTemplate(cfg.endpoint, { encodedUrl: encodeURIComponent(videoUrl) });
		let result;
		try {
			const response = await fetch(url);
			if (!response.ok) {
				// 4xx = video deleted/private/restricted → 'unavailable'
				result = { ok: false, reason: "unavailable" };
			} else {
				const body = await response.text();
				if (!body) {
					// verified failure mode: empty body = unavailable video
					result = { ok: false, reason: "unavailable" };
				} else {
					const json = JSON.parse(body);
					result = { ok: true, title: json.title, channel: json.author_name };
				}
			}
		} catch (error) {
			// fetch threw = no network (offline) or CORS/parse problem (error)
			const offline = typeof navigator !== "undefined" && navigator.onLine === false;
			result = { ok: false, reason: offline ? "offline" : "error" };
			console.warn(`🟠 oEmbed fetch failed for ${videoId}:`, error.message);
		}
		this.#oembedCache.set(videoId, result);
		return result;
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { DataService };
