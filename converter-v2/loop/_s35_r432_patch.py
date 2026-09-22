#!/usr/bin/env python3
"""r432 — replace the first-draft implicit-block detection (lines between the `let loiAlias …` declaration and the block's
closing brace) with the refined form: an EMPTY alias followed by a lead; a lead line of <= lead_max_words; the block bounded to
lead / list / blank lines by the rule itself (loiSet), a prose line ending it; no set with a lead AND a list → no fire.
Exact-anchor edit, written to a temp file, syntax-checked by the caller. Run under WSL."""
import io, re, sys
P = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/app/js/ContentConverter.js"
s = io.open(P, encoding="utf-8", newline="").read()
a = s.index("\t\tlet loiAlias = false, loiLeadFirst = false, loiImplicit = false;\n")
b = s.index("\t\t// Where does the lesson menu END? The [Lesson Overview] block", a)
new = r'''		let loiAlias = false, loiLeadFirst = false, loiImplicit = false, loiSet = null;
		{
			const loiCfg = DataService.Data.EmitTemplates.menu?.lesson_overview_implicit;
			const loiOn = !!loiCfg && loiCfg.enabled !== false
				&& !(typeof process !== "undefined" && process.env && process.env[loiCfg.env ?? "LESSONWALT_OFF"])
				&& !page.isOverview && menuType !== "none" && overviewIdx < 0;
			if (loiOn) {
				const leadRe = new RegExp(loiCfg.lead_pattern
					?? "^(we are learning|learning intentions?|you will show|how will i know|i can\\b|success criteria|wh[aā]inga ako|paearu angitu)", "i");
				const aliasWords = new Set((loiCfg.alias_words ?? ["overview"]).map(String));
				const maxScan = Math.min(items.length, loiCfg.max_scan_items ?? 14);
				const maxBlock = loiCfg.max_block_items ?? 24;
				const leadMaxW = loiCfg.lead_max_words ?? 8;
				const openTags = new Set(loiCfg.opening_tags ?? ["title bar", "h1", "h2", "lesson content", "page", "body", "sub head"]);
				const listRe = /^\s*(?:[•\-–—*·o]|\d+[.)]|[a-z][.)])\s+/i;
				const foldT = (t) => Utils.Fold(String(t || "")).replace(/[*_]/g, "").trim();
				const textOf = (x) => x.type === "black" ? String(x.text || "")
					: (x.type === "tag" ? (String(x.blackAfter || "").trim() || this.#norm.RenderText(x.text) || "") : "");
				// a LEAD line: short ("We are learning:", "You will show your understanding by:"), never a prose sentence
				// ("We are learning what an event is. You will show …" — COM1006)
				const isLeadLine = (line) => { const f = foldT(line); return !!f && leadRe.test(f) && f.split(/\s+/).length <= leadMaxW; };
				const isListLine = (line) => listRe.test(String(line || ""));
				const isLead = (x) => (x.type === "black" || (x.type === "tag" && (!x.parse?.primary || openTags.has(x.parse.primary.tag) || /^h[1-6]$/.test(x.parse.primary.tag))))
					&& isLeadLine(textOf(x).split(/\n/)[0]);
				// a BLOCK member: blank, a lead line, a list line, a black run whose every line is lead / list, a list tag
				const isMember = (x) => {
					if (x.type === "black") {
						const lines = String(x.text || "").split(/\n/).map((l) => l.trim()).filter(Boolean);
						return !lines.length || lines.every((l) => isLeadLine(l) || isListLine(l));
					}
					if (x.type !== "tag") return false;
					const p = x.parse?.primary;
					if (!p) return x.parse?.class === "instruction" || x.parse?.class === "noise";
					if (p.tag === "list") return true;
					if (["body", "sub head", "h3", "h4", "h5"].includes(p.tag)) {
						const lines = String(x.blackAfter || "").split(/\n/).map((l) => l.trim()).filter(Boolean);
						const own = this.#norm.RenderText(x.text) || "";
						return (isLeadLine(own) || !own.trim()) && lines.every((l) => isLeadLine(l) || isListLine(l));
					}
					return false;
				};
				const buildSet = (start) => {
					const set = new Set(); let leads = 0, lists = 0;
					for (let j = start; j < Math.min(items.length, start + maxBlock); j++) {
						const x = items[j];
						if (!isMember(x)) break;
						set.add(j);
						const txt = x.type === "black" ? String(x.text || "") : (String(x.blackAfter || "") + "\n" + (x.parse?.primary ? (this.#norm.RenderText(x.text) || "") : ""));
						for (const l of txt.split(/\n/)) { if (isLeadLine(l)) leads++; else if (isListLine(l.trim())) lists++; }
						if (x.type === "tag" && x.parse?.primary?.tag === "list") lists++;
					}
					return (leads >= 1 && lists >= 1) ? set : null;
				};
				// (a) an EMPTY [Overview] alias among the opening items, followed by the block
				let aIdx = -1;
				for (let k = 0; k < maxScan; k++) {
					const x = items[k];
					if (x.type === "tag" && x.parse?.primary?.tag === "title bar" && aliasWords.has(String(x.parse.primary.fragment ?? ""))
						&& !String(x.blackAfter || "").trim()) { aIdx = k; break; }
				}
				if (aIdx >= 0) {
					const set = buildSet(aIdx + 1);
					if (set) { overviewIdx = aIdx; loiAlias = true; loiSet = set; }
				}
				if (!loiSet) {
					// (b) the first lead item reached through opening items only
					const opening = (x) => {
						if (x.type === "black") return !String(x.text || "").trim();
						if (x.type !== "tag") return false;
						const p = x.parse?.primary;
						if (!p) return true;                                                   // an unresolved red span
						if (x.parse?.class === "instruction" || x.parse?.class === "noise") return true;
						if (!openTags.has(p.tag)) return false;
						return p.tag !== "body" || !String(x.blackAfter || "").trim();         // a body tag only when empty
					};
					for (let k = 0; k < maxScan; k++) {
						const x = items[k];
						if (isLead(x)) {
							const set = buildSet(k);
							if (set) { overviewIdx = k > 0 ? k - 1 : 0; loiLeadFirst = (k === 0); loiImplicit = true; loiSet = set; }
							break;
						}
						if (!opening(x)) break;
					}
				}
				if (loiSet) run.AddNote("info", "ContentConverter",
					`Lesson menu taken from the ${loiAlias ? "[Overview] alias" : "unmarked WALT / SC block"} at the lesson's start (menu.lesson_overview_implicit).`);
			}
		}

'''
s2 = s[:a] + new + s[b:]
# the set built by the rule replaces the generic section-stop set, and bounds the region
anchor = "\t\tif (loiLeadFirst && menuIdxSet) menuIdxSet.add(0);   // ROUND 432 — a lead at the very first item is the block's own start\n"
assert s2.count(anchor) == 1
s2 = s2.replace(anchor, "\t\tif (loiSet) { menuIdxSet = loiSet; lessonMenuEnd = Math.max(...loiSet) + 1; }   // ROUND 432 — the implicit block's own bounds\n")
io.open(P + ".r432.tmp", "w", encoding="utf-8", newline="").write(s2)
print("written", len(s2))
