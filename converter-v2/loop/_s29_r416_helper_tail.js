		const free = String(p.free ?? "").trim();
		if (!free || !/[a-zĀ-ſ]/i.test(free)) return null;
		if (/^\(|\)$/.test(free) || /^\d/.test(free) || /:$/.test(free)) return null;
		let title = String(this.#norm.RenderText(it.text) || "").replace(/\*+/g, "").replace(/\s+/g, " ").trim();
		if (!title || /^\(|^\d|:$/.test(title)) return null;
		// THE RED RUN THAT ENDS MID-SENTENCE: Word split the writer's line into a red run and a black
		// one — `[Activity 5A] L` + `ooking at precise word choice` (mid-word, no space), `[Activity 1]
		// Click` + ` on the link below to load…` (mid-sentence). A black tail opening with a LOWERCASE
		// letter continues the red words: joined and short it is the title (`Looking at precise word
		// choice`, the black first line consumed — mode "join"); joined and long it is a sentence, so the
		// red words are PREPENDED to the black tail and the r66 rule reads the whole line (mode "prefix").
		let mode = "plain";
		const tail = String(it.blackAfter ?? "");
		if (tail.trim() && /^\s*\p{Ll}/u.test(tail)) {
			const nl = tail.search(/\n/);
			const first = (nl >= 0 ? tail.slice(0, nl) : tail);
			const joined = (title + (/^\s/.test(tail) ? " " : "") + first.trim()).replace(/\s+/g, " ").trim();
			if (joined.split(/\s+/).length <= (cfg.max_words ?? 8)) { title = joined; mode = "join"; }
			else return { title, mode: "prefix" };
		}
		const cand = title.trim();
		if (cand.length < (cfg.min_chars ?? 3) || cand.split(/\s+/).length > (cfg.max_words ?? 8)) return mode === "join" ? { title: title.slice(0, title.length - (title.length - String(this.#norm.RenderText(it.text) || "").replace(/\*+/g, "").replace(/\s+/g, " ").trim().length)), mode: "prefix" } : null;
		if (this.#norm.HasInstructionCue(cand)) return mode === "join" ? { title: String(this.#norm.RenderText(it.text) || "").replace(/\*+/g, "").replace(/\s+/g, " ").trim(), mode: "prefix" } : null;
		let q = null; try { q = this.#norm.Parse("[" + cand + "]"); } catch { q = null; }
		if (q && q.primary) return null;   // the text IS a lexicon tag — a widget name, never a title
		// a title is CAPITALISED (`Concrete poems`, `Ka pai!`); a lowercase tail (`wide`, `type and check`,
		// `tick the pictures that show fractions.`) is a writer's aside — measured, never a gold title
		const _c0 = cand.charAt(0);
		if (cfg.require_capital !== false && !(_c0 === _c0.toUpperCase() && _c0 !== _c0.toLowerCase())) return null;
		title = cfg.strip_trailing_stop !== false ? cand.replace(/\.$/, "").trim() : cand;
		if (title.length < (cfg.min_chars ?? 3)) return null;
		return { title, mode };
