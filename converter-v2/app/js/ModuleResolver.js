/**
 * ModuleResolver.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Three jobs — two pure data lookups plus THE shared run-preparation choke
 * point both conversion entries call:
 *  1. DETECT the module code from the uploaded material (filename and/or
 *     front-matter text) — never asked of the user.
 *  2. RESOLVE that code's structural ruleset through the Style Anchor
 *     Registry's four-tier cascade (defaults → subject → base → level),
 *     falling back to the Majority+Deviations registry for modules the
 *     corpus has never seen.
 *  3. PREPARE the ConversionRun — the "run" object, one mutable scratchpad
 *     created per conversion job that every later step reads from and
 *     writes onto (detected code, resolved rules, pages, notes, output
 *     files) — via PrepareRun: classify the extracted docs as the WT (the
 *     Writers Template — the source .docx full of the writer's [bracketed]
 *     tags) versus the media list (the companion .docx table of every
 *     image/video/audio used, with its source URL), detect + resolve, set
 *     run.mtkFlag, apply the unsupported-pathway refusal, parse the media
 *     items, and trim the WT front-matter — ONE sequence, so App.js (the
 *     browser entry point) and batch_convert.cjs (the Node command-line
 *     tool that converts many modules in bulk, for testing/regression —
 *     not something an end user runs) can never drift apart again. This
 *     exists because the two entry points used to each run their OWN
 *     separate copy of this prep logic, and those two copies quietly
 *     drifted apart over time — one set a flag the other forgot to set,
 *     one applied a refusal rule the other had already relaxed — so the
 *     SAME module could produce DIFFERENT HTML depending on which entry
 *     point converted it (a real example: the module HPFUN903 converted
 *     differently through the browser than through the batch tool).
 *     PrepareRun is the fix: one shared sequence that both entries are
 *     required to call, so that kind of silent divergence can't happen
 *     again.
 *
 * WHY THE CASCADE (the project's core design):
 * Knowledge is layered and additive — a new module INHERITS from its
 * anchor. The resolver only WALKS the data; it never derives or rebuilds
 * rules. If a module needs different structure, that is a registry edit.
 *
 * DATA THIS FILE READS:
 * Style_Anchor_Registry.json (cascade + _meta.module_code_to_level),
 * Style_Anchor_Registry_Majority_And_Deviations.json (unknown modules);
 * PrepareRun additionally reads Emit_Templates.elements.dual_language
 * (the flag controlling whether the bilingual/Te Reo rendering pathway is
 * enabled — see PrepareRun's unsupported-pathway check below) +
 * Input_Doc_Rules (unsupported_pathways, wt_page_tracking).
 *
 * NEVER IN THIS FILE: `if (moduleCode === "…")` — that is the v1 death
 * spiral. Module-specific knowledge lives in the registry only.
 * ===========================================================================
 */

class ModuleResolver {

	/**
	 * Detects the module code from the available evidence.
	 *
	 * HOW IT WORKS (strongest evidence first):
	 *  1. Filenames: "OSAH401 Writers Template.docx" → leading CODE token.
	 *  2. Front-matter text: a "Module code: XYZ123" style line, or any
	 *     registry-known code appearing in the first blocks.
	 * Conflicting candidates → keep the filename one, surface a warning
	 * (never silently pick).
	 *
	 * @param {Object} options
	 * @param {string[]} options.filenames - uploaded file names
	 * @param {Object[]} options.allBlocks - extracted blocks (pre-trim, so
	 *                   front-matter fields are still visible)
	 * @param {ConversionRun} options.run - for surfacing notes
	 * @returns {string|null} the module code (uppercased) or null
	 */
	static DetectModuleCode({ filenames = [], allBlocks = [], run }) {
		// code shape: 2–6 letters + 2–4 digits, optionally a trailing
		// letter pair (e.g. ANZH102RR). Matches the corpus naming.
		const codeRx = /\b([A-Z]{2,6}\d{2,4}(?:RR)?)\b/;

		const candidates = [];

		// 1) filenames — the strongest signal in practice
		for (const name of filenames) {
			const m = name.toUpperCase().match(codeRx);
			if (m) candidates.push({ code: m[1], from: `filename "${name}"` });
		}

		// 2) front-matter "Module code:" line or early code mention
		for (const b of allBlocks.slice(0, 40)) {
			if (b.kind !== "para") continue;
			const m = b.text.toUpperCase().match(codeRx);
			if (m) { candidates.push({ code: m[1], from: "document front-matter" }); break; }
		}

		if (!candidates.length) {
			run?.AddNote("error", "ModuleResolver",
				"No module code found in filenames or front-matter — converting with global defaults; outputs named MODULE.");
			return null;
		}

		// conflict check — surfacing rule: report disagreement, use the first
		const unique = [...new Set(candidates.map((c) => c.code))];
		if (unique.length > 1) {
			run?.AddNote("warn", "ModuleResolver",
				`Multiple module-code candidates found (${unique.join(", ")}) — using ${candidates[0].code} from ${candidates[0].from}.`);
		}
		if (run) run.codeSource = candidates[0].from;
		return candidates[0].code;
	};

	/**
	 * Resolves the full ruleset for a module code through the cascade.
	 *
	 * HOW THE WALK WORKS (registry _meta.resolver):
	 * Start from defaults, then overlay subject_rules, base_rules, and the
	 * level delta — lowest tier wins because it is applied last. PATTERN
	 * fields ({overview, lesson[, final]} objects) resolve as WHOLE objects,
	 * never per-key merged (a half-merged pattern would invent a structure
	 * no real module has).
	 *
	 * UNKNOWN MODULES:
	 * - Known base, new module → the level's rules at that base (sibling
	 *   inheritance; nearest level when the exact one is absent).
	 * - Entirely new series → Majority_And_Deviations master_instructions
	 *   for the subject+phase… which requires knowing the subject. When we
	 *   can't even find the base prefix, we fall back to global defaults
	 *   and SAY SO loudly.
	 *
	 * @param {string|null} code - detected module code
	 * @param {ConversionRun} run - for surfacing the resolution path
	 * @returns {Object} resolved ruleset (all 11 tracked fields present)
	 */
	static Resolve(code, run) {
		const REG = DataService.Data.StyleRegistry;
		// defensive clone — resolved rules get annotated downstream and must
		// never mutate the loaded registry (standards §5)
		const rules = structuredClone(REG.defaults);
		const path = ["defaults"];

		if (!code) {
			run?.AddNote("warn", "ModuleResolver", "No module code — resolved from global defaults only.");
			run && (run.resolutionPath = path.join(" → "));
			return rules;
		}

		const found = this.#findInRegistry(code, REG);

		if (found) {
			const { subjectName, subject, baseName, base, levelName, level, exactMember } = found;
			Object.assign(rules, structuredClone(subject.subject_rules ?? {}));
			path.push(`subject "${subjectName}"`);
			// group identity for the HTML-convention cascade (resolved after
			// the field merge below, once template_phase is known)
			if (run) { run.subjectName = subjectName; run.seriesCode = baseName; }
			Object.assign(rules, structuredClone(base.base_rules ?? {}));
			path.push(`base ${baseName}`);
			if (level) {
				Object.assign(rules, structuredClone(level.delta ?? {}));
				path.push(`level ${levelName}`);
			}
			if (!exactMember) {
				run?.AddNote("info", "ModuleResolver",
					`${code} is not in the registry members — inherited from its ${level ? `level ${levelName}` : `base ${baseName}`} (sibling rule).`);
			}

			// page_model exceptions: a member listed as deviating from the
			// level's majority flips between single-file and multi-file
			const exceptions = level?.delta?.page_model_exceptions ?? [];
			if (exceptions.includes(code)) {
				rules.page_model = rules.page_model === "single-file" ? "multi-file" : "single-file";
				run?.AddNote("info", "ModuleResolver",
					`${code} is a recorded page_model exception — using ${rules.page_model}.`);
			}
		} else {
			// entirely unknown series → majority master instructions
			const majority = this.#resolveFromMajority(code, run);
			if (majority) {
				Object.assign(rules, majority.rules);
				path.push(majority.path);
			} else {
				run?.AddNote("warn", "ModuleResolver",
					`${code}: no registry entry and no majority ruleset found — using global defaults. Check the code, or add the series to the registry.`);
			}
		}

		if (run) {
			run.resolutionPath = path.join(" → ");
			// the convention-registry group key: subject × template_phase —
			// the SAME grouping as the level-scope/phase-consistency audits
			run.groupKey = run.subjectName && rules.template_phase
				? `${run.subjectName}|${rules.template_phase}` : null;
		}
		return rules;
	};

	/**
	 * THE SHARED RUN-PREPARATION CHOKE POINT.
	 *
	 * A "choke point" here means a single function that both conversion
	 * entry points are REQUIRED to funnel their setup work through, instead
	 * of each writing its own version of that setup. That is what makes it
	 * impossible for the two entries to quietly reinvent — and diverge
	 * from — the same sequence of steps.
	 *
	 * Both conversion entries (App.js #convert and batch_convert.cjs
	 * convertModule) MUST call this instead of running their own prep
	 * sequence. The exact ORDER of the statements below matters and should
	 * not be reordered casually: a large number of already-converted
	 * modules depend on this precise sequence to reproduce byte-identical
	 * output, so shuffling the steps — even ones that look independent —
	 * risks silently changing the output for modules that already convert
	 * correctly today.
	 *
	 * One known imprecision, kept as-is deliberately: run.mtkFlag (set
	 * below) currently causes bilingual/Te Reo rendering to trigger a
	 * little more broadly than strictly necessary. Narrowing exactly when
	 * it fires is known, separate follow-up work — not something to "fix"
	 * opportunistically inside this function.
	 *
	 * Entries keep for themselves ONLY what genuinely differs: acquiring +
	 * extracting the .docx bytes (browser File objects vs fs), UI/progress
	 * reporting, and what to DO on a refusal (App renders the summary;
	 * batch throws). `_verify_entry_parity.cjs` guards this contract.
	 *
	 * @param {Object} options
	 * @param {Object[]} options.docs - [{name, doc}] extracted uploads, in
	 *                   the entry's natural order (upload order / readdir)
	 * @param {ConversionRun} options.run - the run to prepare (mutated)
	 * @param {TagNormaliser} options.normaliser - the compiled matcher
	 * @returns {Object} { ok:true, wt, mediaSource } on success;
	 *                   { ok:false, reason:"no-wt" } when no WT was found;
	 *                   { ok:false, reason:"unsupported", unsupported, wt,
	 *                     mediaSource } on a data-driven refusal.
	 */
	static PrepareRun({ docs = [], run, normaliser, istockAcksText = null, istockAcksFiles = null }) {
		// ---- classify the inputs (WT = content opener; media list = table) --
		let wt = null;
		let mediaSource = null;
		for (const d of docs) {
			const mediaTable = MediaListParser.FindMediaTable(d.doc.blocks);
			const isWt = DocxExtractor.LooksLikeWritersTemplate(d.doc.blocks, normaliser);
			if (isWt && !wt) wt = d;
			if (mediaTable && !mediaSource) mediaSource = { ...d, mediaTable };
		}
		if (!wt) return { ok: false, reason: "no-wt", wt: null, mediaSource };

		// ---- module identity + rules (this exact order is load-bearing — see the ORDER note in this method's JSDoc above) ----
		// filenames: WT-name FIRST (preserves the batch candidate priority),
		// then the other uploads (preserves the App coverage superset).
		run.moduleCode = this.DetectModuleCode({
			filenames: [wt.name, ...docs.filter((d) => d !== wt).map((d) => d.name)],
			allBlocks: wt.doc.blocks,
			run,
		});
		run.metadata = wt.doc.metadata ?? {};   // front-matter info fields
		run.mtkFlag = !!wt.doc.mtkFlag;   // the docx's own bilingual/Te-Reo signature flag, set independently of whatever the Style Anchor Registry resolved for this module -> feeds reoMode below
		run.resolvedRules = this.Resolve(run.moduleCode, run);

		// MTK/TRR unsupported pathway: this used to refuse EVERY module
		// carrying the MTK/TRR bilingual signature, because the converter
		// didn't yet know how to render bilingual (Te Reo + English) content.
		// Now that genuine bilingual (reoTranslate) support exists, the
		// refusal is narrowed so it only fires on a flagged module that
		// ISN'T actually recognised as bilingual — a real bilingual module
		// now converts normally, while anything else still gets refused
		// safely rather than risk wrong output. Env REOTRANSLATE_OFF (or
		// data flag dual_language.enabled:false) reverts to the old, wider
		// refusal, for side-by-side comparison testing.
		const dlOn = (DataService.Data.EmitTemplates?.elements?.dual_language?.enabled !== false)
			&& !(typeof process !== "undefined" && process.env && process.env.REOTRANSLATE_OFF);
		const reoModule = /reoTranslate/i.test(run.resolvedRules?.body_class || "");
		const unsupported = (dlOn && reoModule) ? null
			: DataService.Data.InputDocRules.unsupported_pathways.find((u) =>
				wt.doc.mtkFlag && (u.also_requires_code_prefix ?? [])
					.some((p) => (run.moduleCode ?? "").startsWith(p)));
		if (unsupported) return { ok: false, reason: "unsupported", unsupported, wt, mediaSource };

		// ---- verified iStock acknowledgements file (optional) ---------------
		// ROUND 235 (Chris) — a *_istock-acks.txt supplied with the uploads (or
		// sitting in the module folder for a batch run) carries API-sourced,
		// definitely-correct iStock acknowledgement lines; parsed HERE (the one
		// shared prep sequence — entry parity) so both entries behave identically.
		// Data flag: Acks_Formats.istock_acks_file · Env toggle: ISTOCKACKS_OFF
		//
		// ROUND 236 (Chris) — WHICH uploaded .txt is the acks file is now decided
		// HERE too, from the file CONTENTS rather than its name (per-module names
		// like _istock-acks-OSAI501.txt are coming, and the old
		// filename-ends-with rule cannot cover the family). Both entries hand in
		// every .txt they were given as `istockAcksFiles`; AcksBuilder.PickIstockAcks
		// applies the one shared content test, so the browser and the batch
		// harness can never disagree about what counts as an acks file. It runs
		// AFTER run.moduleCode is resolved above, so a filename naming a
		// DIFFERENT module can be warned about. `istockAcksText` remains
		// supported for callers that already know which file they hold.
		// Data flag: …istock_acks_file.detect · Env toggle: ISTOCKDETECT_OFF
		let acksText = istockAcksText;
		if (acksText == null && istockAcksFiles?.length) {
			acksText = AcksBuilder.PickIstockAcks(istockAcksFiles, run)?.text ?? null;
		}
		run.istockAcks = AcksBuilder.ParseIstockAcks(acksText, run);

		// ---- media list ------------------------------------------------------
		if (mediaSource) {
			run.mediaItems = MediaListParser.ParseItems(mediaSource.mediaTable);
			run.mediaListFound = true;
		} else {
			run.AddNote("warn", "ModuleResolver",
				"No media list found — acknowledgements will hold the standing items plus per-lesson designer-media check lines only.");
		}

		// WT pagination trustworthy? (drives acks evidence rule 2)
		run.pageRecordsUsable = Math.max(...wt.doc.blocks.map((b) => b.wtPage ?? 1))
			>= DataService.Data.InputDocRules.wt_page_tracking.min_pages_for_trust;

		// ---- trim front-matter; exclude an embedded media table --------------
		run.wtBlocks = DocxExtractor.TrimFrontMatter(wt.doc.blocks, normaliser, run)
			.filter((b) => b !== mediaSource?.mediaTable.block);

		return { ok: true, wt, mediaSource };
	};

	/**
	 * Derives a coarse "phase" (year-level band) key from a module code.
	 *
	 * WHY: used to find the matching phase-group bucket in the
	 * Majority+Deviations registry (registry _meta.module_code_to_level)
	 * when a module's series has never been seen before — see
	 * #resolveFromMajority below, which is this method's only caller.
	 *
	 * HOW: "FUN" anywhere in the code (case-insensitive) means the
	 * Fundamentals track; "ECH" means the Early-Childhood track; those
	 * letter infixes OVERRIDE the normal digit-based rule below. Otherwise,
	 * take the code's run of digits: 4 digits means an NCEA (senior
	 * secondary) module; 3 digits uses the FIRST digit as the phase number
	 * (e.g. "212" → "2xx"), except a leading "5" which also means NCEA;
	 * anything else (no digits found) returns "unknown".
	 *
	 * @param {string} code - module code, e.g. "ENGC212" or "HPFUN101"
	 * @returns {string} e.g. "3xx" | "FUN" | "ECH" | "NCEA" | "unknown"
	 */
	static PhaseKeyFor(code) {
		if (/FUN/i.test(code)) return "FUN";
		if (/ECH/i.test(code)) return "ECH";
		const digits = code.match(/(\d{2,4})/)?.[1] ?? "";
		if (digits.length === 4) return "NCEA";
		if (digits.length === 3) {
			const h = digits[0];
			return h === "5" ? "NCEA" : `${h}xx`;
		}
		return "unknown";
	};

	/**
	 * Walks the registry for a code: exact member first, then the base
	 * whose code prefixes the module, then that base's nearest level.
	 *
	 * WHY TWO PASSES: an exact member match is authoritative — the registry
	 * was built by cataloguing real, already-converted modules, so if the
	 * code is literally listed we trust that entry completely. Only when
	 * the code has never been seen before do we fall back to guessing its
	 * home from the shared letter+digit PREFIX of an existing base (e.g. a
	 * brand-new "ENGC215" inherits from the "ENGC2" base because no module
	 * called exactly "ENGC215" exists yet, but other "ENGC2xx" modules do).
	 *
	 * RETURN SHAPE (consumed by Resolve — a concrete example):
	 * {
	 *   subjectName: "English",
	 *   subject:     { subject_rules: {...}, bases: {...} },
	 *   baseName:    "ENGC2",
	 *   base:        { base_rules: {...}, levels: {...} },
	 *   levelName:   "215" | null,
	 *   level:       { delta: {...}, members: [...] } | null,
	 *   exactMember: true | false   // false = found via the prefix/sibling guess, not a listed member
	 * }
	 *
	 * @param {string} code - module code to look up, e.g. "ENGC215"
	 * @param {Object} REG - the loaded Style_Anchor_Registry.json
	 * @returns {Object|null} location info as above, or null when even the
	 *          base prefix can't be matched (Resolve then falls back
	 *          further, to #resolveFromMajority)
	 */
	static #findInRegistry(code, REG) {
		const upper = code.toUpperCase();

		// pass 1 — exact membership (authoritative). A member matches when
		// it equals the code, or is the code plus a file suffix (the
		// registry keeps oddities like "ARWHA.html" as members).
		for (const [subjectName, subject] of Object.entries(REG)) {
			if (subjectName.startsWith("_") || subjectName === "defaults") continue;
			for (const [baseName, base] of Object.entries(subject.bases ?? {})) {
				for (const [levelName, level] of Object.entries(base.levels ?? {})) {
					const isMember = (level.members ?? []).some((m) => {
						const mu = m.toUpperCase();
						return mu === upper || mu === `${upper}.HTML`;
					});
					if (isMember) {
						return { subjectName, subject, baseName, base, levelName, level, exactMember: true };
					}
				}
			}
		}

		// pass 2 — longest base prefix match, then nearest level by the
		// code's hundreds digit (a new module inherits its level sibling)
		let best = null;
		for (const [subjectName, subject] of Object.entries(REG)) {
			if (subjectName.startsWith("_") || subjectName === "defaults") continue;
			for (const [baseName, base] of Object.entries(subject.bases ?? {})) {
				if (upper.startsWith(baseName.toUpperCase())
					&& (!best || baseName.length > best.baseName.length)) {
					best = { subjectName, subject, baseName, base };
				}
			}
		}
		if (!best) return null;

		// nearest level: same leading digit of the numeric part, else the
		// highest level present (most-recent practice)
		const digit = upper.match(/(\d)/)?.[1];
		const levels = Object.entries(best.base.levels ?? {});
		let chosen = levels.find(([name]) => digit && name.endsWith(digit));
		if (!chosen && levels.length) chosen = levels[levels.length - 1];
		return {
			...best,
			levelName: chosen?.[0] ?? null,
			level: chosen?.[1] ?? null,
			exactMember: false,
		};
	};

	/**
	 * Majority master-instructions fallback for a brand-new series:
	 * find the subject whose bases share the code's letter prefix, then the
	 * phase group matching the code's level, and adopt master_instructions
	 * (per that registry's rule 1).
	 *
	 * WHEN THIS RUNS: only when #findInRegistry found NOTHING — not even a
	 * base whose prefix matches the code — meaning this is an entirely new
	 * series the Style Anchor Registry has never recorded. Rather than
	 * fall straight to bare global defaults, we consult the SEPARATE
	 * Majority+Deviations registry, which answers a different question:
	 * "if we don't know this series specifically, what do MOST modules in
	 * this subject/phase do?"
	 *
	 * TWO-PASS LOOKUP:
	 *  1. find which SUBJECT recognises a series sharing this code's letter
	 *     prefix (in any phase) — that tells us which subject's rules to use;
	 *  2. within that subject, prefer the PHASE group matching this code's
	 *     level (via PhaseKeyFor above); fall back to any phase that knows
	 *     the prefix if the preferred phase has no master_instructions.
	 * Then (rule 2, the important one): if that phase group ALSO records
	 * specific deviations for a series sharing the prefix, those override
	 * the plain majority — a new module in an EXISTING series should match
	 * its own siblings, not just "most modules everywhere in this
	 * subject/phase".
	 *
	 * @param {string} code - module code with no exact/base registry match
	 * @param {ConversionRun} [run] - for surfacing an info note when a
	 *                        series-specific deviation was applied
	 * @returns {Object|null} { rules: {...}, path: "majority Subject / Phase" }
	 *          describing what was applied and why, or null when no subject
	 *          in the whole registry recognises even the letter prefix
	 */
	static #resolveFromMajority(code, run) {
		const MAJ = DataService.Data.MajorityRegistry;
		const prefix = code.match(/^[A-Z]+/)?.[0] ?? "";
		if (!prefix) return null;

		// the module's phase, mapped to the registry's phase-group naming
		// ("Phase 1 (Years 1-3)", "Fundamentals", "NCEA", …)
		const phaseKey = this.PhaseKeyFor(code);
		const phaseNameStart = {
			"1xx": "Phase 1", "2xx": "Phase 2", "3xx": "Phase 3", "4xx": "Phase 4",
			"NCEA": "NCEA", "FUN": "Fundamentals", "ECH": "Early",
		}[phaseKey] ?? null;

		// pass 1 — find the subject that knows a series sharing this letter
		// prefix (in ANY phase): that tells us which subject's majority to use
		let subjectHit = null;
		for (const [subjectName, subject] of Object.entries(MAJ)) {
			if (subjectName.startsWith("_")) continue;
			for (const phase of Object.values(subject)) {
				if (!phase?.series_deviations) continue;
				if (Object.keys(phase.series_deviations).some(
					(s) => prefix.startsWith(s) || s.startsWith(prefix))) {
					subjectHit = { subjectName, subject };
					break;
				}
			}
			if (subjectHit) break;
		}
		if (!subjectHit) return null;

		// pass 2 — inside that subject, prefer the phase group matching the
		// module's level; else any phase that knows the series prefix
		const { subjectName, subject } = subjectHit;
		let phaseName = phaseNameStart
			? Object.keys(subject).find((p) => p.startsWith(phaseNameStart)) : null;
		if (!phaseName || !subject[phaseName]?.master_instructions) {
			phaseName = Object.keys(subject).find((p) => subject[p]?.master_instructions
				&& Object.keys(subject[p].series_deviations ?? {}).some(
					(s) => prefix.startsWith(s) || s.startsWith(prefix)));
		}
		if (!phaseName) return null;

		const phase = subject[phaseName];
		const rules = structuredClone(phase.master_instructions);

		// rule 2 (the most important): an EXISTING series' next module keeps
		// that series' recorded deviations — sibling consistency beats majority
		for (const [series, dev] of Object.entries(phase.series_deviations ?? {})) {
			if (prefix.startsWith(series) || series.startsWith(prefix)) {
				Object.assign(rules, structuredClone(dev));
				run?.AddNote("info", "ModuleResolver",
					`${code}: applied series deviations for ${series} over the ${subjectName} / ${phaseName} majority.`);
				break;
			}
		}
		return { rules, path: `majority ${subjectName} / ${phaseName}` };
	};
}

// Node test-harness hook; browsers ignore it.
if (typeof module !== "undefined") module.exports = { ModuleResolver };
