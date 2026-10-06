/**
 * Config.js
 * ===========================================================================
 * WHAT THIS FILE DOES:
 * Single source of truth for ALL static app-level values: version, data file
 * paths, DOM selectors, and UI strings. Nothing is hard-coded at point of use.
 *
 * WHY SEPARATE FILE:
 * Per the Te Kura coding standards (§6), every project has exactly one Config
 * static class. If a path, selector, or label changes, you edit it HERE once
 * instead of hunting for it across the codebase.
 *
 * WHEN TO WORK HERE:
 * - The data/ folder moves, or a runtime data file is renamed.
 * - A DOM id/class in index.html changes.
 * - UI wording needs a tweak.
 *
 * IMPORTANT BOUNDARY:
 * Config holds APP plumbing only. Everything about MODULES — the tag
 * vocabulary, styles, output HTML shapes, acknowledgement formats — lives in
 * the ../data/*.json files, never here. That separation is the whole point of
 * the design: the engine reads its domain knowledge from data files, and
 * Config is just the address book that says where those files are.
 * ===========================================================================
 */

class Config {

	// ---------------------------------------------------------------------
	// APP VERSION
	// ---------------------------------------------------------------------
	// Format: YYMMDD.iteration — a date stamp plus that day's build number.
	//   e.g. 250102.3  ->  2025-01-02, build 3.
	// This is shown in the UI so a developer can tell which build produced a
	// page. It is NOT written into the converted HTML, so changing it never
	// changes any output — bump it with every release.
	static AppVersion = "260623.12";

	// ---------------------------------------------------------------------
	// RUNTIME DATA FILES (paths are relative to app/index.html — served over HTTP)
	// ---------------------------------------------------------------------
	// WHAT: every file the engine reads at runtime, listed by a friendly key.
	// WHY:  DataService loads exactly this list at startup, so adding a new
	//       data file is a one-line change here.
	// USAGE: DataService reads Config.DataFiles.TagLexicon, etc.
	static DataFiles = {
		TagLexicon:        "../data/Tag_Lexicon.json",
		TagExceptions:     "../data/Tag_Exceptions.json",
		InstructionCues:   "../data/Instruction_Cues.json",
		InputDocRules:     "../data/Input_Doc_Rules.json",
		StyleRegistry:     "../data/Style_Anchor_Registry.json",
		MajorityRegistry:  "../data/Style_Anchor_Registry_Majority_And_Deviations.json",
		BoundaryBank:      "../data/Interactive_Boundary_ChildTag_Bank.json",
		// NOTE: Interactive_Wrapper_Catalogue.json is reference-only and is
		// deliberately NOT loaded at runtime — widget RECOGNITION comes from the
		// lexicon + boundary bank, and widget MARKUP from
		// Emit_Templates.interactive_builders. Re-adding it would just load
		// ~1,400 unused lines at every startup.
		EmitTemplates:     "../data/Emit_Templates.json",
		AcksFormats:       "../data/Acks_Formats.json",
		ManifestPatterns:  "../data/Manifest_Patterns.json",
		ConventionRegistry: "../data/Html_Convention_Registry.json",
		// The menu type (tabs / simplified / none) per subject × phase,
		// derived from the human-built modules.
		MenuScaffold:      "../data/Menu_Scaffold_Registry.json",
		// The whitelist of Creative-Services authors whose native Word comments
		// we surface into the page, plus how to render them.
		CommentAuthors:    "../data/Comment_Authors.json",
		// Whole-page "template mode": the order of the <body> class tokens plus
		// the language / translation attributes.
		TemplateModes:     "../data/Template_Modes.json",
		// The three files behind the module precedence cascade (see
		// PrecedenceResolver.js): the per-module built-structure index (plus
		// module_meta, the data the cascade filters over), the cascade's level
		// order and reliability floors, and the subject-level default parameters.
		// These are loaded but the live engine application ships turned OFF
		// (Precedence_Cascade.engine_inherit.enabled === false), so today they
		// are read-only reference data.
		ModuleStructureIndex: "../data/Module_Structure_Index.json",
		PrecedenceCascade:    "../data/Precedence_Cascade.json",
		SubjectParameters:    "../data/Subject_Global_Parameters.json",
		// A frequency list of overview-menu heading phrases seen across the
		// human corpus. MenuBuilder uses it to decide when a one-line
		// "**Title:** content" heading should be split (env MENUHEADINGLEX_OFF).
		OverviewMenuHeadingLexicon: "../data/Overview_Menu_Heading_Lexicon.json",
	};

	// ---------------------------------------------------------------------
	// DOM SELECTORS — the element ids used in app/index.html
	// ---------------------------------------------------------------------
	// HOW TO USE: document.getElementById(Config.Selectors.DropZone)
	static Selectors = {
		FileGuard:     "file-guard",       // the "you opened this via file://" warning screen
		AppRoot:       "app-root",
		DropZone:      "drop-zone",
		FileInput:     "file-input",
		FileList:      "file-list",
		ModeP:         "mode-p",
		ModeD:         "mode-d",
		ConvertButton: "convert-button",
		// The Reference-module panel (suggested-module dropdown / reference-HTML
		// upload; the dropdown auto-selects the suggestion).
		ReferencePanel:  "reference-panel",
		ReferenceStatus: "reference-status",
		RefPick:         "ref-pick",
		RefHtml:         "ref-html",
		RefPickBlock:    "ref-pick-block",
		RefHtmlBlock:    "ref-html-block",
		RefCodeSelect:   "ref-code-select",
		RefCodeFilter:   "ref-code-filter",   // the type-to-filter box
		RefCodeCount:    "ref-code-count",    // the live "showing N of M" line
		RefSubjectFilter: "ref-subject-filter",   // subject filter dropdown
		RefPhaseFilter:   "ref-phase-filter",     // phase-level filter dropdown
		ConvertGateNote:  "convert-gate-note",    // the red "why Convert is inactive" note
		RefTemplateFilter: "ref-template-filter", // template filter dropdown
		RefFilterReset:    "ref-filter-reset",    // the "Reset filters" button
		// The "Make your own template" choice + its three required dropdowns
		RefCustom:         "ref-custom",
		RefCustomBlock:    "ref-custom-block",
		RefCustomSubject:  "ref-custom-subject",
		RefCustomPhase:    "ref-custom-phase",
		RefCustomTemplate: "ref-custom-template",
		RefHtmlInput:    "ref-html-input",
		RefHtmlList:     "ref-html-list",
		// The "clear everything & convert another module" reset control (its
		// wrapper + the button). Shown only after a conversion completes; the
		// reset returns the converter to its fresh state IN PLACE, without a
		// page reload (a reload would drop back to the site's landing view).
		ResetPanel:    "reset-panel",
		ResetButton:   "reset-button",
		ProgressLog:   "progress-log",
		// The Convert-panel progress bar. App.js drives it; the engine reports
		// progress through the guarded run.onProgress hook (see ConversionRun.js).
		ProgressBar:      "progress-bar",
		ProgressBarFill:  "progress-bar-fill",
		ProgressBarLabel: "progress-bar-label",
		SummaryPanel:  "summary-panel",
		DownloadAll:   "download-all",
		OutputList:    "output-list",
	};

	// ---------------------------------------------------------------------
	// UI STRINGS — the words shown to the person using the tool
	// ---------------------------------------------------------------------
	static Strings = {
		ReadyToConvert: "Ready — drop the Writers Template (+ Media List) above, choose the image mode, then Convert.",
		Converting:     "Converting…",
		Done:           "Conversion complete.",
		// Progress-bar stage labels (set by App.#progressSet).
		ProgressExtract: "Reading files",
		ProgressPrep:    "Preparing module",
		ProgressPages:   "Converting pages",
		ProgressAcks:    "Acknowledgements & media",
		ProgressDone:    "Done",
		ProgressFailed:  "Failed — see the log below",
		// Shown in red under the deactivated Convert button when the
		// reference requirement is what's blocking it.
		ConvertGateReference: "Please select a reference module, or upload a reference module's HTML pages in Section 3",
		// Shown when "Make your own template" is active but incomplete.
		ConvertGateCustom: "Please select a subject, phase and template in Section 3 (all three are required)",
	};

	// ---------------------------------------------------------------------
	// FAIL-SAFE — the last-resort UI when the app cannot recover (standards §6).
	// ---------------------------------------------------------------------
	// Replaces the whole app body with a plain message and a Retry button.
	static FULL_BREAK(message) {
		const root = document.getElementById(Config.Selectors.AppRoot);
		if (!root) return;
		root.innerHTML = `
			<div class="full-break">
				<p>${message || "Something went wrong loading the converter."}</p>
				<button onclick="location.reload()">Retry</button>
			</div>
		`;
	};
}
