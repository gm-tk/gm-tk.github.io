"""_s31_r425_menu.py — round 425: the XOTP family's two-column ITEM menu (menu.two_col_li.item_family):
`col-md-6 col-sm-12 > div.item` columns, `h3><span` labels (Overview / Understand / Know / Do), the trailing prose in
the right column; the adapter emits the Overview row's own left-cell label as the first bold label.
Run under WSL from CONVERTER_V2/outputs: python3 _s31_r425_menu.py"""
import io, os
JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2", "app", "js")

def patch(name, old, new, count=1):
    p = os.path.join(JS, name)
    s = io.open(p, encoding="utf-8", newline="").read()
    assert s.count(old) == count, (name, s.count(old), old[:70])
    s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("patched", name)

# ---- MenuBuilder: the family resolver ------------------------------------------------------------
patch("MenuBuilder.js",
"""	/** ROUND 359 — the public face of #inquiryFamilyFor (ContentConverter's overview partition asks it for the colon label match). */
	static inquiryFamilyFor(run, page) {
		return this.#inquiryFamilyFor(run, page);
	}
""",
"""	/** ROUND 359 — the public face of #inquiryFamilyFor (ContentConverter's overview partition asks it for the colon label match). */
	static inquiryFamilyFor(run, page) {
		return this.#inquiryFamilyFor(run, page);
	}

	/**
	 * ROUND 425 (the autonomous loop's session 31 Round 3 — the XOTP activity-table adapter). The two-column
	 * FAMILY for this page: the r359 Inquiry family (overviews of Inquiry-template modules), else the ITEM
	 * family — a module whose code starts with one of menu.two_col_li.item_family.code_prefixes, on EVERY page
	 * (the XOTP modules have no overview page; their lesson menu is the same two-column form: `col-md-6
	 * col-sm-12 > div.item` columns, `h3><span` labels, the trailing prose in the right column — 24 / 24 gold
	 * pages). A family carries its own shell / heading templates / left_match; the composer treats both alike.
	 */
	static #familyFor(run, page) {
		const inq = this.#inquiryFamilyFor(run, page);
		if (inq) return inq;
		const cfg = DataService.Data.EmitTemplates?.menu?.two_col_li?.item_family;
		if (!cfg || cfg.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "ITEMMENU_OFF"]) return null;
		const code = String(run?.moduleCode || "").toUpperCase();
		if (!(cfg.code_prefixes ?? []).some((p) => code.startsWith(String(p).toUpperCase()))) return null;
		return cfg;
	}
""")

patch("MenuBuilder.js",
"""		const inqCfg = this.#inquiryFamilyFor(run, page);
		const inqFamily = !!inqCfg && !engFamily && archetype !== "tabs";
		if (inqFamily) { archetype = "two_col_li"; bannerFamily = false; }
""",
"""		const inqCfg = this.#familyFor(run, page);   // r425: the Inquiry family OR the item family
		const inqFamily = !!inqCfg && !engFamily && archetype !== "tabs";
		if (inqFamily) { archetype = "two_col_li"; bannerFamily = false; }
""")

patch("MenuBuilder.js",
"""		const out = { kind: menuType, archetype, engFamily, bannerFamily, inquiryFamily: inqFamily, bannerLabel: "", tab1: "", tab2: "", content: "", left: "", right: "", tab1Cols: null, tab2Cols: null };
""",
"""		const out = { kind: menuType, archetype, engFamily, bannerFamily, inquiryFamily: inqFamily, familyShell: (inqFamily && inqCfg.shell) || null, bannerLabel: "", tab1: "", tab2: "", content: "", left: "", right: "", tab1Cols: null, tab2Cols: null };
""")

# the bold-label routing: a family's own left_match outranks the consume vocabulary; trailing prose → right
patch("MenuBuilder.js",
"""							const folded = Utils.Fold(label);
							if (isLabel(folded)) continue;   // section label → consumed
							const left = cfg.left_match.some((m) => folded.startsWith(m));
							const right = (cfg.right_match ?? []).some((m) => folded.includes(m));
""",
"""							const folded = Utils.Fold(label);
							// r425: a family's own left_match (the item family's "overview") outranks the consume vocabulary
							const famLeft = (inqFamily && Array.isArray(inqCfg.left_match)) ? inqCfg.left_match : null;
							const famHit = !!famLeft && famLeft.some((m) => folded.startsWith(m));
							if (isLabel(folded) && !famHit) continue;   // section label → consumed
							const left = famHit || (famLeft ?? cfg.left_match).some((m) => folded.startsWith(m));
							const right = (cfg.right_match ?? []).some((m) => folded.includes(m));
""")

patch("MenuBuilder.js",
"""						if (line.trim()) textBuf.push(line);   // buffer (grouped at the next label / heading / end)
					}
					continue;
				}
""",
"""						// r425: the item family's TRAILING PROSE — a long unlabelled paragraph after the left column's
						// labels moves to the right column (the gold's `col-md-6 col-sm-12 > div.item` right pane holds
						// the Overview row's closing paragraphs; the short "I can" items stay left).
						if (inqFamily && inqCfg.trailing_prose_right && bucket === "left" && line.trim()
							&& !/^\\*\\*/.test(line.trim())
							&& line.trim().split(/\\s+/).length >= (inqCfg.trailing_prose_min_words ?? 12)) {
							flushText(); bucket = "right";
						}
						if (line.trim()) textBuf.push(line);   // buffer (grouped at the next label / heading / end)
					}
					continue;
				}
""")

# ---- SkeletonBuilder: the family's own shell ------------------------------------------------------
patch("SkeletonBuilder.js",
"""						? (content.menu.engFamily ? "two_col_offset" : (content.menu.inquiryFamily ? "two_col_inquiry" : "two_col_li"))   // r359: the Inquiry two-column shell
""",
"""						? (content.menu.engFamily ? "two_col_offset" : (content.menu.inquiryFamily ? ((content.menu.familyShell && tpl.menu.shells[content.menu.familyShell]) ? content.menu.familyShell : "two_col_inquiry") : "two_col_li"))   // r359: the Inquiry two-column shell; r425: a family names its own
""")

# ---- DocxExtractor: the adapter emits the Overview row's left-cell label as the first bold label ---
patch("DocxExtractor.js",
"""			if (role === "overview") { overview = rightLines.slice(); overviewLinks = links; continue; }
""",
"""			if (role === "overview") {
				overview = rightLines.slice(); overviewLinks = links;
				// the row's own left-cell label ("Overview") leads the menu as a bold label (the gold's first
				// `<h3><span>Overview</span></h3>`, 24 / 24 pages) — data overview_label_from_cell
				const lab = ad.overview_label_from_cell !== false ? plain(leftLines[0] ?? "") : "";
				if (lab && !/^\\*\\*/.test(String(overview[0] ?? "").trim())) overview.unshift(`**${lab}**`);
				continue;
			}
""")
