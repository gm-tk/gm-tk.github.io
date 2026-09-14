#!/usr/bin/env python3
"""_r322_splice.py — ROUND 322 (the autonomous loop, session 3, Round 9 — Chris's decision 3):
KB constraint 65 / CL-0082 — the [MTKquiz] shell WITHOUT the quiz content.

Idempotent by the prefix test (every "new" text is checked for presence before its anchor is
replaced). Edits the REAL files under pageforge-site/converter-v2/ (the CONVERTER_V2 paths are
symlinks — never sed -i them). Data file: a tab-indented surgical text insertion, never json.dumps.

What it adds:
  DATA  Emit_Templates.interactive_builders.mtk_quiz.omit_quiz_content {enabled, env MTKQUIZOMIT_OFF, …}
  ENGINE ContentConverter:
    (1) page-level state `mtk` (null | {phase:"run"|"silence", marker, frame, kept}) + the closures
        mtkTop / mtkPending / mtkFlush / mtkGuard defined after autoClose;
    (2) the loop-head guard (before the Word-comment surfacing) — the instruction run and the silence;
    (3) the two direct marker sites (element co-tag / opener co-tag) DEFER the emit via mtkPending;
    (4) the bundle branch: a quiz-type bundle carrying a marker builds the SHELL instead of the widget
        (pre-marker members rendered, the post-marker instruction run, note + button), then silence;
    (5) #mtkQuizEmit: note THEN button, always the button (the writer's claimed button renders nothing);
    (6) new static helpers #mtkQuizOmitCfg / #mtkQuizShellBundle / #mtkQuizRunStep / #mtkQuizShellPre.
"""
import io, os, re, sys

ROOT = os.environ.get("R322_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2")   # R322_ROOT = the reproducibility test tree
CC = os.path.join(ROOT, "app", "js", "ContentConverter.js")
ET = os.path.join(ROOT, "data", "Emit_Templates.json")

def rd(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

def splice(src, anchor, new, where="after", label=""):
    """Insert `new` after/before `anchor` (exact, unique). Idempotent: if `new` already present, no-op."""
    if new in src:
        print(f"  = {label}: already applied"); return src
    n = src.count(anchor)
    assert n == 1, f"{label}: anchor count {n} != 1"
    out = src.replace(anchor, anchor + new if where == "after" else new + anchor, 1)
    print(f"  + {label}: applied"); return out

def replace_once(src, old, new, label=""):
    if new in src and old not in src:
        print(f"  = {label}: already applied"); return src
    n = src.count(old)
    assert n == 1, f"{label}: old count {n} != 1"
    print(f"  + {label}: applied"); return src.replace(old, new, 1)

# ---------------------------------------------------------------------------------------------- DATA
et = rd(ET)
DATA_ANCHOR = '\t\t\t"window_forward": 5\n\t\t}'
DATA_NEW = '''\t\t\t"window_forward": 5,
\t\t\t"omit_quiz_content": {
\t\t\t\t"_doc": "ROUND 322 (KB constraint 65 / CL-0082, the designer's locked decision of 21 Aug 2026 — the autonomous loop session 3 Round 9, Chris's decision 3). REVERSES CL-0038's 'writer quiz content stays rendered' limb: an [MTKquiz] activity box holds ONLY (1) its title, (2) the writer's student instructions, (3) the Designer/Developer To Do note, (4) the 'Go to quiz' button — in that order — and the quiz's own content (questions, options, [correct]/[answer] marks, answer keys, option tables, the in-page quiz widget the writer also described, the quiz's own in-D2L title + intro) is omitted SILENTLY: no Red Flag, no comment, no trace (the one sanctioned undisclosed omission, constraint 1(b); the material stays in the Writers Template, the designer's source in MTK DEV). MECHANISM: the marker's emit is DEFERRED — after the marker, a short INSTRUCTION RUN is kept (a [Body]-family item or non-question prose, up to instruction_max_items; a heading only when the marker is a title-less [Activity] opener, ARFUN02 1A); a bracketed answer-mark span (answer_mark_pattern — '[Answers: B, A, B, C]', '[CS … answers …]', '[correct]') is dropped without ending the run (ARFUN04 4D keeps its instruction); anything else (a question line per question_pattern, an option, a table, a bundle trigger, a button, a heading once the box has content, a container/boundary tag) ENDS the run: the note + button flush inside the still-open box and the SILENCE starts — every content item is skipped until the quiz block ends: the box's close (explicit [end …] or the existing heading auto-close — ARFUN04 2E's next [H3]), any CONTAINER_CLOSE, the next [Activity] opener, a page/section boundary, the next marker, or — with no box open — a rendered heading <= container_auto_close.rendered_heading_max / any CONTAINER_OPEN (SSOG301's [H2] ends it at once). A bundle whose trigger item is silenced is marked emitted and never renders. PATH 2a: a quiz-type bundle (quiz_bundle_types) that carries the marker as its opening span or a member builds the SHELL instead of the widget: members before the marker rendered as content (TEFUN03's [Body] instruction), the post-marker instruction run, then note + button (the whole widget IS the quiz: gold ARFUN03 1A, ARFUN04 1H, TEFUN03/06 1A). A marker captured by a NON-quiz container bundle (accordion ENG1004/1005, speechBubble TEDC401, unclassified HPRE203 p1 / MXFU402) is NOT in scope — named follow-up. The writer's own quiz button the r232 pre-pass claimed (_mtkQuizAnchor / _mtkQuizBtn) renders NOTHING under this flag — the button is the box's LAST child (gold 87% / 97%, r320) and the marker's emit always carries it. Measured 2026-09-15 (outputs/_measure_r322_mtkquiz.cjs → _r322_mtkquiz_windows.json): 64 markers / 33 pages / 25 modules; 56 in scope. The box-less marker (13: SCFUN01, TEFUN07, MXFUN02, EXBP901, SSOG301) still gets no synthesised numbered box and no default 'Quiz' <h3> — the KB's remaining shell pieces, named follow-up. Env MTKQUIZOMIT_OFF reverts the whole round byte-for-byte to the round-232 form.",
\t\t\t\t"enabled": true,
\t\t\t\t"env": "MTKQUIZOMIT_OFF",
\t\t\t\t"note_first": true,
\t\t\t\t"todo_note": "create this quiz in MTK DEV and orgunit link it to this module, then insert its D2L quicklink URL into the \\"Go to quiz\\" button href below. Writer's quiz spec: {spec}",
\t\t\t\t"instruction_max_items": 2,
\t\t\t\t"instruction_tags": ["body", "body text"],
\t\t\t\t"question_pattern": "^\\\\s*(\\\\(?\\\\d{1,2}[.)]|\\\\(?[a-h][.)]\\\\s|question\\\\s*\\\\d|q\\\\d|\\u2610|\\\\[\\\\s*\\\\]|true\\\\s*[/|]\\\\s*false)",
\t\t\t\t"answer_mark_pattern": "^\\\\[[^\\\\]]*\\\\b(correct|answers?|answer guide|model answers?|marking|marked answers?)\\\\b",
\t\t\t\t"shell_max_members_before": 2,
\t\t\t\t"quiz_bundle_types": ["multiChoiceQuiz", "radioQuiz", "dragAndDrop", "clickDrop", "dropQuiz", "wordSelect", "wordDrag", "typing", "selectionBox", "reorder", "selfCheck"]
\t\t\t}
\t\t}'''
# the data block REPLACES the anchor's tail (the block's last key + closing brace)
if '"omit_quiz_content": {' in et:
    print("  = data omit_quiz_content: already applied")
else:
    assert et.count(DATA_ANCHOR) == 1, "data anchor not unique"
    et = et.replace(DATA_ANCHOR, DATA_NEW, 1)
    print("  + data omit_quiz_content: applied")
wr(ET, et)

# -------------------------------------------------------------------------------------------- ENGINE
cc = rd(CC)

# (1) state + closures — after the autoClose closure's definition
A1 = '''				run.AddNote("info", "ContentConverter",
					`Page ${page.lessonLabel}: [${top.tag}] auto-closed before the next ${primary?.tag ?? it.type}.`);
				if (!stack.length) breakRow();
			}
		};
'''
N1 = '''
		// [MTKquiz] SHELL WITHOUT THE QUIZ CONTENT (ROUND 322 — KB constraint 65 / CL-0082;
		// the loop's Round 9, Chris's decision 3). The marker's emit is DEFERRED behind a short
		// INSTRUCTION RUN, then the note + button flush inside the still-open box and a
		// SILENCE skips every content item until the quiz block ends (the box's close, any
		// closer, the next [Activity], a boundary, the next marker; unboxed: a section heading
		// or any container open). See #mtkQuizRunStep for the run's classifier and the data
		// block interactive_builders.mtk_quiz.omit_quiz_content for the full story.
		// Env toggle MTKQUIZOMIT_OFF reverts the whole family to the round-232 form.
		let mtk = null;
		const mtkCfg = this.#mtkQuizOmitCfg();
		const mtkTop = () => (stack.length ? stack[stack.length - 1] : null);
		const mtkPending = (marker, isOpener = false) => {
			if (!mtkCfg) return false;
			if (marker._mtkQuizEmitted) return true;
			if (mtk && mtk.marker === marker) return true;      // the same marker reached twice (primary + co-tag test)
			mtk = { phase: "run", marker, frame: mtkTop(), kept: 0, isOpener };
			return true;
		};
		// does an EXPLICIT closer ([end quiz] / [end activity] / [end MTKQuiz] — any
		// CONTAINER_CLOSE) bound the quiz block before the next [Activity] opener, page /
		// section boundary or marker? Then the writer closed the block himself and the
		// silence runs to that closer — a heading inside it is the quiz's own in-D2L
		// title (TEFUN02's second "[H3] Show your kaiako"), not a section break. Without
		// one, the ordinary heading auto-close bounds the block (ARFUN04 2E).
		const mtkCloserAhead = (from) => {
			for (let k = from + 1; k < bodyItems.length; k++) {
				const c = bodyItems[k];
				const p = c.type === "tag" ? c.parse?.primary : null;
				const d = p?.directive ?? null;
				if (d === "CONTAINER_CLOSE") return true;
				if (["PAGE_BOUNDARY", "SECTION_MARKER"].includes(d)) return false;
				if (c.type === "tag" && (c.parse?.tags ?? []).some((t) => t.tag === "mtk quiz"
					|| (t.tag === "activity" && t.directive === "CONTAINER_OPEN"))) return false;
			}
			return false;
		};
		const mtkSilence = (marker) => {
			markContent();
			mtk = { phase: "silence", marker, frame: mtkTop(), closerAhead: mtkCloserAhead(bodyItems.indexOf(marker)) };
		};
		const mtkFlush = () => {
			if (!mtk || mtk.phase !== "run") return;
			const marker = mtk.marker, frame = mtk.frame;
			emit(...this.#mtkQuizEmit(marker, run));
			markContent();
			mtk = { phase: "silence", marker, frame, closerAhead: mtkCloserAhead(bodyItems.indexOf(marker)) };
		};
		// LINE-LEVEL split of the quiz block (the coalesce ran before this loop, so a
		// [Body]'s following questions arrive as ONE multi-line black item that
		// gatherFollowing would sweep into the kept instruction): a kept tag item's
		// black followers are trimmed to their leading non-question lines; the rest is
		// marked consumedBy "mtk-quiz-omit" (gatherFollowing stops at a consumedBy item,
		// and the guard skips it) — silently, per the KB.
		const mtkQRe = mtkCfg ? new RegExp(mtkCfg.question_pattern ?? "^\\\\s*\\\\(?\\\\d{1,2}[.)]", "i") : null;
		const mtkQuizStart = (text) => {   // index of the first question-like line, else -1
			const lines = String(text ?? "").split("\\n");
			for (let k = 0; k < lines.length; k++) {
				const l = lines[k].replace(/\\*/g, "").trim();
				if (l && mtkQRe.test(l)) return k;
			}
			return -1;
		};
		const mtkTrimFollowers = (idx) => {
			let cut = false;
			for (let j = idx + 1; j < bodyItems.length; j++) {
				const f = bodyItems[j];
				if (f.type !== "black" || f.consumedBy !== undefined) break;
				if (cut) { f.consumedBy = "mtk-quiz-omit"; continue; }
				const k = mtkQuizStart(f.text);
				if (k < 0) continue;
				const keep = String(f.text ?? "").split("\\n").slice(0, k).join("\\n");
				if (keep.trim()) f.text = keep; else f.consumedBy = "mtk-quiz-omit";
				cut = true;
			}
			return cut;
		};
		// true → the caller skips this item's turn entirely
		const mtkGuard = (c) => {
			if (c.consumedBy === "mtk-quiz-omit") return true;
			if (!mtk) return false;
			if (mtk.phase === "run" && mtk.endAfter) mtkFlush();   // the previous kept item ended the run
			// the silenced/run frame has already left the stack (closed by an earlier item)
			if (mtk.frame && !stack.includes(mtk.frame)) { mtkFlush(); mtk = null; return false; }
			const p = c.type === "tag" ? c.parse?.primary : null;
			const dir = p?.directive ?? null;
			const isMarker = c.type === "tag" && (c.parse?.tags ?? []).some((t) => t.tag === "mtk quiz");
			const actOpen = c.type === "tag" && (c.parse?.tags ?? []).some((t) => t.tag === "activity" && t.directive === "CONTAINER_OPEN");
			const hardEnd = isMarker || actOpen || ["CONTAINER_CLOSE", "PAGE_BOUNDARY", "SECTION_MARKER"].includes(dir);
			if (mtk.phase === "run") {
				const step = hardEnd ? "end" : this.#mtkQuizRunStep(c, mtk, mtkCfg, renderedHeading);
				if (step === "keep") {
					mtk.kept++;
					// a kept item whose own lines (or whose black followers) hold the quiz's
					// first question keeps only the lines before it and ends the run after it
					if (c.type === "black") {
						const k = mtkQuizStart(c.text);
						if (k > 0) { c.text = String(c.text).split("\\n").slice(0, k).join("\\n"); mtk.endAfter = true; }
					} else if (c.type === "tag") {
						const k = mtkQuizStart(c.blackAfter);
						if (k > 0) { c.blackAfter = String(c.blackAfter).split("\\n").slice(0, k).join("\\n"); mtk.endAfter = true; }
						if (mtkTrimFollowers(bodyItems.indexOf(c))) mtk.endAfter = true;
					}
					return false;
				}
				if (step === "drop") return true;
				mtkFlush();                                  // "end": the shell completes here …
				if (hardEnd) { mtk = null; return false; }   // … and a hard boundary is processed normally
				// fall through into the silence test for this same item
			}
			// phase "silence"
			if (hardEnd) { mtk = null; return false; }
			if (mtk.closerAhead) {
				// the writer's explicit closer bounds the block: nothing before it ends the silence
			} else if (!mtk.frame) {
				const hMax = DataService.Data.EmitTemplates.container_auto_close?.activity_close_before?.rendered_heading_max ?? 4;
				const h = renderedHeading(p);
				if ((h !== null && h <= hMax) || dir === "CONTAINER_OPEN") { mtk = null; return false; }
			} else {
				autoClose(c);                                 // a section heading closes the box the normal way …
				if (!stack.includes(mtk.frame)) { mtk = null; return false; }   // … and ends the silence
			}
			if (c.consumedBy !== undefined && bundles[c.consumedBy] && !bundles[c.consumedBy]._emitted) {
				// a NON-quiz widget after the quiz (HPRE203 2D's closing speech bubble, SSOG103 6A's
				// "Kia ora, friend!" bubble) is content, not the quiz: it ends the silence and renders
				if (mtkCfg.non_quiz_widget_ends_silence !== false) {
					const b = bundles[c.consumedBy], qt = new Set(mtkCfg.quiz_bundle_types ?? []);
					if (![b.type, ...(b.extraTypes ?? [])].some((t) => qt.has(t))) { mtk = null; return false; }
				}
				bundles[c.consumedBy]._emitted = true;      // a silenced widget never renders later
				bundles[c.consumedBy]._mtkSilenced = true;
			}
			return true;
		};
'''
cc = splice(cc, A1, N1, "after", "(1) mtk state + closures")

# (2) the loop-head guard — before the Word-comment surfacing (no trace of the omitted content)
A2 = '''			if (it._inquiryCrumb) continue;

			// ---- whitelisted Word comments → red note JUST BEFORE the element ----'''
N2_OLD = A2
N2_NEW = '''			if (it._inquiryCrumb) continue;

			// [MTKquiz] instruction run / silence (ROUND 322 — see the mtk closures above):
			// placed BEFORE the comment surfacing so an omitted question leaves no trace.
			if (mtkGuard(it)) continue;

			// ---- whitelisted Word comments → red note JUST BEFORE the element ----'''
cc = replace_once(cc, N2_OLD, N2_NEW, "(2) loop-head guard")

# (3a) the element co-tag site
A3a_OLD = '''					if ((it.parse?.tags ?? []).some((t) => t.tag === "mtk quiz")) {
						emit(...this.#mtkQuizEmit(it, run));
					}
					markContent();'''
A3a_NEW = '''					if ((it.parse?.tags ?? []).some((t) => t.tag === "mtk quiz")) {
						// ROUND 322: deferred behind the instruction run (mtkPending); the
						// round-232 immediate emit only when the omit flag is off.
						if (!mtkPending(it)) emit(...this.#mtkQuizEmit(it, run));
					}
					markContent();'''
cc = replace_once(cc, A3a_OLD, A3a_NEW, "(3a) element co-tag site")

# (3b) the opener co-tag site
A3b_OLD = '''						if ((it.parse?.tags ?? []).some((t) => t.tag === "mtk quiz")) {
							emit(...this.#mtkQuizEmit(it, run));
						}
						break;'''
A3b_NEW = '''						if ((it.parse?.tags ?? []).some((t) => t.tag === "mtk quiz")) {
							// ROUND 322: deferred behind the instruction run — an opener that
							// carried no title text may take the next heading as its title.
							if (!mtkPending(it, true)) emit(...this.#mtkQuizEmit(it, run));
						}
						break;'''
cc = replace_once(cc, A3b_OLD, A3b_NEW, "(3b) opener co-tag site")

# (3c) the ELEMENT dispatch site — an mtk-PRIMARY item (SCPH301's "[MTK quiz. …]") would render its
#      button + note at once through #element's own mtk branch; under the flag it defers instead.
A3c_OLD = '''					emit(...actDeBold(this.#element(it, bodyItems, i, stack, run)));
					// An mtk-quiz CO-TAG riding some other element ([H3]-primary etc. —'''
A3c_NEW = '''					// ROUND 322: an mtk-PRIMARY element defers its emit behind the instruction
					// run (mtkPending) instead of rendering at once through #element's mtk branch.
					if (!(mtkCfg && it.parse?.primary?.tag === "mtk quiz" && mtkPending(it)))
						emit(...actDeBold(this.#element(it, bodyItems, i, stack, run)));
					// An mtk-quiz CO-TAG riding some other element ([H3]-primary etc. —'''
# (3c)'s new text ENDS with its anchor — key idempotence on the hook line itself (the r315 trap).
if 'primary?.tag === "mtk quiz" && mtkPending(it)' in cc:
    print("  = (3c) element dispatch site: already applied")
else:
    assert cc.count(A3c_OLD) == 1, "(3c) anchor count != 1"
    cc = cc.replace(A3c_OLD, A3c_NEW, 1); print("  + (3c) element dispatch site: applied")

# (4a) the OWNED bundle site
A4a_OLD = '''						if (!this.#mtkQuizBundleThin(bundle)) emit(this.#interactivePlaceholder(bundle, run));
						// [MTKquiz] markers riding this bundle (captured member or opener co-tag)
						// ship their button + To Do note here, inside the still-open box
						// (ROUND 232 — CL-0038; see #mtkQuizBundleTail).
						emit(...this.#mtkQuizBundleTail(bundle, run, it));'''
A4a_NEW = '''						// ROUND 322 (KB c65 / CL-0082): a quiz-type bundle carrying the [MTKquiz]
						// marker builds the SHELL instead of the widget — the widget IS the quiz.
						// "lead" mode: the note + button follow the instructions, BEFORE whatever widget
						// the walk captured under this box (often the next section's — the r310 class);
						// "widget" mode: the shell replaces the widget itself.
						if (mtkMode === "lead") { emit(...this.#mtkQuizEmit(bundle.activityOwner, run)); markContent(); }
						if (mtkMode === "widget") emit(...this.#mtkQuizShellPre(bundle, it, run, bodyItems, stack, renderedHeading));
						else if (!this.#mtkQuizBundleThin(bundle)) emit(this.#interactivePlaceholder(bundle, run));
						// [MTKquiz] markers riding this bundle (captured member or opener co-tag)
						// ship their button + To Do note here, inside the still-open box
						// (ROUND 232 — CL-0038; see #mtkQuizBundleTail).
						const mtkTail = this.#mtkQuizBundleTail(bundle, run, it);
						emit(...mtkTail);
						if (mtkCfg && (mtkMode || mtkTail.length)) mtkSilence(it);'''
cc = replace_once(cc, A4a_OLD, A4a_NEW, "(4a) owned bundle site")

# (4b) the INLINE bundle site
A4b_OLD = '''						if (!this.#mtkQuizBundleThin(bundle)) emit(this.#interactivePlaceholder(bundle, run));
						emit(...this.#mtkQuizBundleTail(bundle, run, it));   // ROUND 232 — CL-0038 (see above)'''
A4b_NEW = '''						const mtkShellI = this.#mtkQuizShellBundle(bundle, it);   // ROUND 322 — see the owned site above ("lead" cannot occur inline)
						if (mtkShellI === "widget") emit(...this.#mtkQuizShellPre(bundle, it, run, bodyItems, stack, renderedHeading));
						else if (!this.#mtkQuizBundleThin(bundle)) emit(this.#interactivePlaceholder(bundle, run));
						const mtkTailI = this.#mtkQuizBundleTail(bundle, run, it);   // ROUND 232 — CL-0038 (see above)
						emit(...mtkTailI);
						if (mtkCfg && (mtkShellI || mtkTailI.length)) mtkSilence(it);'''
cc = replace_once(cc, A4b_OLD, A4b_NEW, "(4b) inline bundle site")

# (4c) the owned site's LEAD: decide the shell mode BEFORE the lead machinery renders, trim the lead
A4c_OLD = '''						let actProse = false;
						if (bundle.activityOwner) {'''
A4c_NEW = '''						let actProse = false;
						// ROUND 322 (KB c65 / CL-0082): decide the shell MODE before the lead renders —
						// the writer's quiz button never renders as lead text, and in "lead" mode the
						// quiz content in the lead is trimmed to the instructions.
						const mtkMode = this.#mtkQuizShellBundle(bundle, it);
						if (mtkMode) this.#mtkQuizTrimLead(bundle, mtkMode, renderedHeading);
						if (bundle.activityOwner) {'''
cc = replace_once(cc, A4c_OLD, A4c_NEW, "(4c) owned lead trim")

# (5) #mtkQuizEmit — note first, always the button, under the omit flag
A5_OLD = '''		const spec = String(it.text ?? "")
			.replace(/\\u{1f534}/gu, "").replace(/\\[\\/?RED TEXT\\]/g, "")
			.replace(/\\s+/g, " ").trim();
		if (!it._mtkButtonAbsorbed) out.push(cfg.button_html);
		out.push(NotesAndComments.redFlag(Utils.FillTemplate(cfg.todo_note,
			{ spec: spec || "(no further spec given)" }), run, "todo"));
		return out;'''
A5_NEW = '''		const spec = String(it.text ?? "")
			.replace(/\\u{1f534}/gu, "").replace(/\\[\\/?RED TEXT\\]/g, "")
			.replace(/\\s+/g, " ").trim();
		// ROUND 322 (KB c65 / CL-0082): the KB order — the To Do note, THEN the button, and
		// ALWAYS the button (the writer's own claimed button renders nothing under the flag,
		// so the canonical button is the box's last child). Data omit_quiz_content.
		const omit = this.#mtkQuizOmitCfg();
		if (omit) {
			const note = NotesAndComments.redFlag(Utils.FillTemplate(omit.todo_note ?? cfg.todo_note,
				{ spec: spec || "(no further spec given)" }), run, "todo");
			return omit.note_first === false ? [cfg.button_html, note] : [note, cfg.button_html];
		}
		if (!it._mtkButtonAbsorbed) out.push(cfg.button_html);
		out.push(NotesAndComments.redFlag(Utils.FillTemplate(cfg.todo_note,
			{ spec: spec || "(no further spec given)" }), run, "todo"));
		return out;'''
cc = replace_once(cc, A5_OLD, A5_NEW, "(5) #mtkQuizEmit order")

# (5b) the claimed writer button renders nothing under the flag
A5b_OLD = '''			if (it._mtkQuizAnchor) {
				const mq = tpl.interactive_builders?.mtk_quiz;
				if (mq && mq.enabled !== false) { out.push(mq.button_html); return out; }
			}'''
A5b_NEW = '''			if (it._mtkQuizAnchor) {
				const mq = tpl.interactive_builders?.mtk_quiz;
				// ROUND 322: under the omit flag the marker's own emit carries the (last-child)
				// button, so the writer's claimed button renders nothing.
				if (mq && mq.enabled !== false && this.#mtkQuizOmitCfg()) return out;
				if (mq && mq.enabled !== false) { out.push(mq.button_html); return out; }
			}'''
cc = replace_once(cc, A5b_OLD, A5b_NEW, "(5b) claimed button renders nothing")

# (5c) the claimed [Go to quiz]-span bundle's tail button — the marker's emit carries it now
A5c_OLD = '''		if (bundle._mtkQuizBtn && !bundle._mtkQuizBtnEmitted) {
			bundle._mtkQuizBtnEmitted = true;
			out.push(cfg.button_html);
		}
		return out;'''
A5c_NEW = '''		if (bundle._mtkQuizBtn && !bundle._mtkQuizBtnEmitted) {
			bundle._mtkQuizBtnEmitted = true;
			if (!this.#mtkQuizOmitCfg()) out.push(cfg.button_html);   // ROUND 322: the marker's own emit carries the button
		}
		return out;'''
cc = replace_once(cc, A5c_OLD, A5c_NEW, "(5c) claimed bundle button")

# (6) the new static helpers — before #mtkQuizBundleThin's doc comment
A6 = '''	/** A pre-pass-claimed BUTTON bundle with no real content members — its
	 *  placeholder box is suppressed (the canonical button replaces it). */
	static #mtkQuizBundleThin(bundle) {'''
N6 = '''	/**
	 * ROUND 322 — KB constraint 65 / CL-0082: the [MTKquiz] shell WITHOUT the quiz content.
	 * The data block interactive_builders.mtk_quiz.omit_quiz_content, or null when the
	 * family or the round is off (mtk_quiz.enabled false / MTKQUIZ_OFF / omit disabled /
	 * MTKQUIZOMIT_OFF) — every round-322 seam keys off this one predicate.
	 */
	static #mtkQuizOmitCfg() {
		const mq = DataService.Data.EmitTemplates.interactive_builders?.mtk_quiz;
		if (!mq || mq.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env.MTKQUIZ_OFF) return null;
		const o = mq.omit_quiz_content;
		if (!o || o.enabled === false) return null;
		if (typeof process !== "undefined" && process.env && process.env[o.env ?? "MTKQUIZOMIT_OFF"]) return null;
		return o;
	}

	/** ROUND 322 — a quiz-type bundle (omit_quiz_content.quiz_bundle_types) that carries an
	 *  [MTKquiz] marker as its opening span or a member: the widget IS the quiz, so the shell
	 *  replaces it (gold ARFUN03 1A, ARFUN04 1H, TEFUN03/06 1A). A non-quiz container bundle
	 *  (accordion / speechBubble / unclassified) keeps the round-232 behaviour — named follow-up. */
	static #mtkQuizShellBundle(bundle, openerIt = null) {
		const o = this.#mtkQuizOmitCfg();
		if (!o || !bundle) return false;
		const has = (m) => m && m.type === "tag" && (m.parse?.tags ?? []).some((t) => t.tag === "mtk quiz");
		const isActOpen = (m) => m && m.type === "tag" && (m.parse?.tags ?? []).some((t) => t.tag === "activity" && t.directive === "CONTAINER_OPEN");
		const mem = bundle.memberItems ?? [], ops = bundle.openerItems ?? [];
		// "lead": the OWNED box's own [Activity] opener carries the marker and the widget's members do
		// not — the quiz is the box's lead, the widget is whatever the walk captured after it.
		if (has(bundle.activityOwner) && !ops.some(has) && !mem.some(has)) return "lead";
		const types = new Set(o.quiz_bundle_types ?? []);
		if (![bundle.type, ...(bundle.extraTypes ?? [])].some((t) => types.has(t))) return false;
		if (has(openerIt) && openerIt !== bundle.activityOwner) return "widget";   // the opening span
		if (ops.some(has)) return "widget";
		const k = mem.findIndex(has);
		if (k < 0) return false;
		// a marker that is itself an [Activity] opener, or sits deep in the member list, was swept up by
		// an EARLIER widget's over-capture (ARFUN04 1H) — not this widget's quiz: round-232 behaviour
		if (isActOpen(mem[k]) || k > (o.shell_max_members_before ?? 2)) return false;
		return "widget";
	}

	/**
	 * ROUND 322 — trims an OWNED box's lead items for the shell: a writer's own quiz button
	 * (button_label_pattern, or a pre-pass-claimed anchor) never renders as lead text (the
	 * shell's button is the box's last child); in "lead" mode the items after the marker go
	 * through the instruction run (keep instructions, drop answer marks, stop at the first
	 * question / button / widget). Mutates bundle.activityLeadItems in place.
	 */
	static #mtkQuizTrimLead(bundle, mode, renderedHeading) {
		const o = this.#mtkQuizOmitCfg();
		const mq = DataService.Data.EmitTemplates.interactive_builders?.mtk_quiz;
		if (!o || !mq || !bundle || !Array.isArray(bundle.activityLeadItems)) return;
		const lblRe = new RegExp(mq.button_label_pattern ?? "^(go to (the )?quiz|quiz)[.!]?$", "i");
		const isQuizButton = (m) => m && m.type === "tag" && m.parse?.primary?.directive === "ELEMENT"
			&& (m.parse.primary.tag || "").includes("button")
			&& (m._mtkQuizAnchor || lblRe.test(String(m.blackAfter ?? "").replace(/\\*/g, "").replace(/\\s+/g, " ").trim()));
		const has = (m) => m && m.type === "tag" && (m.parse?.tags ?? []).some((t) => t.tag === "mtk quiz");
		const kept = [];
		const state = { phase: "run", kept: 0, frame: null, isOpener: true, titleTaken: true };
		let ended = mode !== "lead";
		for (const m of bundle.activityLeadItems) {
			if (isQuizButton(m)) { if (mode === "lead") ended = true; continue; }
			if (mode !== "lead") { kept.push(m); continue; }
			if (has(m)) continue;
			if (ended) continue;
			// lead items are consumedBy-marked by construction — classify a probe copy with the
			// consumption cleared (the #mtkQuizShellPre idiom)
			const probe = m.type === "tag" ? { ...m, consumedBy: undefined, _consumed: false } : m;
			const step = this.#mtkQuizRunStep(probe, state, o, renderedHeading);
			if (step === "keep") { state.kept++; kept.push(m); }
			else if (step === "end") ended = true;
		}
		bundle.activityLeadItems = kept;
	}

	/**
	 * ROUND 322 — the instruction-run classifier, shared by the page loop (mtkGuard) and the
	 * bundle shell (#mtkQuizShellPre). For an item AFTER the marker: "keep" = the writer's
	 * student instructions (a [Body]-family tag item or non-question black prose, up to
	 * instruction_max_items; a heading only as the title of a title-less [Activity] opener —
	 * ARFUN02 1A); "drop" = a bracketed answer-mark span (dropped without ending the run —
	 * ARFUN04 4D's "[Answers: B, A, B, C]" precedes its instruction); "end" = anything else
	 * (a question line, an option, a table, a widget trigger, a button, a heading once the box
	 * has content, an unknown bracket span, a container or boundary tag): the note + button
	 * flush and the silence begins.
	 */
	static #mtkQuizRunStep(c, state, cfg, renderedHeading) {
		const qRe = new RegExp(cfg.question_pattern ?? "^\\\\s*\\\\(?\\\\d{1,2}[.)]", "i");
		const aRe = new RegExp(cfg.answer_mark_pattern ?? "^\\\\[[^\\\\]]*\\\\b(correct|answers?)\\\\b", "i");
		const max = cfg.instruction_max_items ?? 2;
		const instrTags = new Set(cfg.instruction_tags ?? ["body"]);
		const plain = (s) => String(s ?? "").replace(/\\*/g, "").trim();
		if (c.type === "table") return "end";
		if (c.type === "black") {
			const t = plain(c.text);
			if (!t) return "drop";                                      // a blank line is free
			if (qRe.test(t) || state.kept >= max) return "end";
			return "keep";
		}
		if (c.type !== "tag") return "end";
		if (c.consumedBy !== undefined || c._consumed) return "end";   // a widget's member / trigger
		const red = String(c.text ?? "").replace(/\\u{1f534}/gu, "").replace(/\\[\\/?RED TEXT\\]/g, "").trim();
		if (aRe.test(red)) return "drop";
		const p = c.parse?.primary;
		if (!p) return "end";                                            // an unknown / bracket-less red span
		if (p.directive === "ELEMENT" && instrTags.has(p.tag)) {
			const t = plain(c.blackAfter);
			if (t && (qRe.test(t) || state.kept >= max)) return "end";
			return "keep";
		}
		const h = renderedHeading ? renderedHeading(p) : null;
		if (h !== null) {
			// the title of a title-less opener: nothing kept yet, the box has no content yet
			const boxEmpty = !state.frame || state.frame.hasContent !== true;
			return (state.isOpener && state.kept === 0 && boxEmpty && !state.titleTaken) ? "keep" : "end";
		}
		return "end";
	}

	/**
	 * ROUND 322 — the SHELL a quiz-type bundle builds in place of its widget: the members
	 * BEFORE the marker rendered as ordinary content through #element (TEFUN03's "[Body]
	 * Show your kaiako…"; buttons, tables and answer marks skipped — the shell has exactly one
	 * button), then the post-marker instruction run under #mtkQuizRunStep. The note + button
	 * follow from #mtkQuizBundleTail at the call site. The bundle stays un-built for the
	 * manifest (the designer builds the quiz in MTK DEV from the Writers Template).
	 */
	static #mtkQuizShellPre(bundle, openerIt, run, bodyItems, stack, renderedHeading) {
		const o = this.#mtkQuizOmitCfg();
		if (!o) return [];
		const has = (m) => m && m.type === "tag" && (m.parse?.tags ?? []).some((t) => t.tag === "mtk quiz");
		const isActOpen = (m) => m && m.type === "tag" && (m.parse?.tags ?? []).some((t) => t.tag === "activity" && t.directive === "CONTAINER_OPEN");
		const members = [openerIt, ...(bundle.openerItems ?? []), ...(bundle.memberItems ?? [])]
			.filter((m, k, arr) => m && arr.indexOf(m) === k)
			// the box's own [Activity] owner (its lead is already the h3) is never a member to render
			.filter((m) => m !== bundle.activityOwner && !(isActOpen(m) && !has(m)))
			.sort((a, b) => bodyItems.indexOf(a) - bodyItems.indexOf(b));
		const out = [];
		const frame = stack.length ? stack[stack.length - 1] : null;
		const state = { phase: "run", kept: 0, frame, isOpener: has(openerIt) && !!frame, titleTaken: false };
		let seenMarker = false, ended = false;
		const render = (m) => {
			if (m.type === "black") { const t = String(m.text ?? "").trim(); return t ? ListsAndRuns.renderBlackText(m.text, run, m.block?.links) : []; }
			if (m.type !== "tag") return [];
			const p = m.parse?.primary;
			if (!p) return [];
			if (p.directive === "ELEMENT" && (p.tag || "").includes("button")) return [];
			return this.#element(m, bodyItems, bodyItems.indexOf(m), stack, run) ?? [];
		};
		for (const m of members) {
			if (has(m)) { seenMarker = true; if (m === openerIt) state.isOpener = true; continue; }
			if (!seenMarker) {
				// pre-marker members: content, never a table / answer mark / button
				if (m.type === "table") continue;
				if (m.type === "tag" && m.parse?.primary?.directive === "INTERACTIVE") continue;
				const red = String(m.text ?? "");
				if (m.type === "tag" && new RegExp(o.answer_mark_pattern ?? "^\\\\[[^\\\\]]*\\\\b(correct|answers?)\\\\b", "i").test(red.trim())) continue;
				out.push(...render(m));
				continue;
			}
			if (ended) continue;
			// after the marker: the instruction run
			const probe = { ...m };
			if (probe.type === "tag") { probe.consumedBy = undefined; probe._consumed = false; }   // members are consumed by construction
			const step = this.#mtkQuizRunStep(probe, state, o, renderedHeading);
			if (step === "keep") {
				const h = m.type === "tag" ? renderedHeading?.(m.parse?.primary) : null;
				if (h !== null && h !== undefined) state.titleTaken = true;
				state.kept++;
				out.push(...render(m));
			} else if (step === "end") ended = true;
		}
		bundle._mtkShell = true;
		return out;
	}

	/** A pre-pass-claimed BUTTON bundle with no real content members — its
	 *  placeholder box is suppressed (the canonical button replaces it). */
	static #mtkQuizBundleThin(bundle) {'''
# (6) is an INSERTION before A6 (N6 ends with A6 itself), so the generic suffix-safe test would re-apply
# it — the r315 trap; key idempotence on a substring only the new text carries.
if "static #mtkQuizOmitCfg()" in cc:
    print("  = (6) static helpers: already applied")
else:
    assert cc.count(A6) == 1, "(6) anchor count != 1"
    cc = cc.replace(A6, N6, 1); print("  + (6) static helpers: applied")


# ---------------------------------------------------------------- (7) the retag's `alert` drop (SCCH301)
TN = os.path.join(ROOT, "app", "js", "TagNormaliser.js")
TL = os.path.join(ROOT, "data", "Tag_Lexicon.json")
A7a_OLD = '''					const drop = new Set(mqr.drop_tags ?? []);
'''
A7a_NEW = '''					const drop = new Set(mqr.drop_tags ?? []);
					// ROUND 322 (KB c65 / CL-0082): an extra drop list that rides the omit round's own
					// toggle — a marker's prose word ("Alert teachers", SCCH301) must never leave a
					// callout tag as the survivor primary, or the shell never opens.
					const od = mqr.omit_quiz_content_drop;
					if (od && od.enabled !== false
						&& !(typeof process !== "undefined" && process.env && process.env[od.env ?? "MTKQUIZOMIT_OFF"])) {
						for (const t of (od.tags ?? [])) drop.add(t);
					}
'''
tn = rd(TN)
if A7a_NEW in tn: print("  = (7a) retag alert drop (engine): already applied")
else:
    assert tn.count(A7a_OLD) == 1, "(7a) anchor count != 1"
    tn = tn.replace(A7a_OLD, A7a_NEW, 1); wr(TN, tn); print("  + (7a) retag alert drop (engine): applied")
A7b_OLD = '''			"bracketless_max_words": 12,
'''
A7b_NEW = '''			"bracketless_max_words": 12,
			"omit_quiz_content_drop": {
				"_doc": "ROUND 322 (KB constraint 65 / CL-0082). Extra co-tags dropped by the retag under the omit round's own toggle: a callout tag resolved from the marker's PROSE (SCCH301 '[MTK quiz. Trigger engagement. Automarked. Alert teachers …]' kept `alert` as the survivor primary, so the marker opened an alert box and neither the round-232 emit nor the round-322 shell ever saw it). Measured over all 64 markers: `alert` is the only such survivor; no marker legitimately co-tags a callout. Env MTKQUIZOMIT_OFF reverts (MTKQUIZ_OFF reverts the whole retag).",
				"enabled": true,
				"env": "MTKQUIZOMIT_OFF",
				"tags": ["alert"]
			},
'''
tl = rd(TL)
if '"omit_quiz_content_drop"' in tl: print("  = (7b) retag alert drop (data): already applied")
else:
    assert tl.count(A7b_OLD) == 1, "(7b) anchor count != 1"
    tl = tl.replace(A7b_OLD, A7b_NEW, 1); wr(TL, tl); print("  + (7b) retag alert drop (data): applied")


# ---------------------------------------------------------------- (8) a non-quiz widget ends the silence
A8a_OLD = '''			if (c.consumedBy !== undefined && bundles[c.consumedBy] && !bundles[c.consumedBy]._emitted) {
				bundles[c.consumedBy]._emitted = true;      // a silenced widget never renders later
'''
A8a_NEW = '''			if (c.consumedBy !== undefined && bundles[c.consumedBy] && !bundles[c.consumedBy]._emitted) {
				// a NON-quiz widget after the quiz (HPRE203 2D's closing speech bubble, SSOG103 6A's
				// "Kia ora, friend!" bubble) is content, not the quiz: it ends the silence and renders
				if (mtkCfg.non_quiz_widget_ends_silence !== false) {
					const b = bundles[c.consumedBy], qt = new Set(mtkCfg.quiz_bundle_types ?? []);
					if (![b.type, ...(b.extraTypes ?? [])].some((t) => qt.has(t))) { mtk = null; return false; }
				}
				bundles[c.consumedBy]._emitted = true;      // a silenced widget never renders later
'''
if A8a_NEW in cc: print("  = (8a) non-quiz widget ends silence (engine): already applied")
else:
    assert cc.count(A8a_OLD) == 1, "(8a) anchor count != 1"
    cc = cc.replace(A8a_OLD, A8a_NEW, 1); print("  + (8a) non-quiz widget ends silence (engine): applied")
A8b_OLD = '''				"shell_max_members_before": 2,
'''
A8b_NEW = '''				"shell_max_members_before": 2,
				"non_quiz_widget_ends_silence": true,
'''
et8 = rd(ET)
if '"non_quiz_widget_ends_silence"' in et8: print("  = (8b) non-quiz widget ends silence (data): already applied")
else:
    assert et8.count(A8b_OLD) == 1, "(8b) anchor count != 1"
    et8 = et8.replace(A8b_OLD, A8b_NEW, 1); wr(ET, et8); print("  + (8b) non-quiz widget ends silence (data): applied")


# ---------------------------------------------------------------- (9) the widget-mode shell box is plain `activity`
A9a_OLD = '''						const interactiveTypes = new Set(tpl.activity_wrapper.interactive_widget_types ?? []);
						const forceInt = [bundle.type, ...(bundle.extraTypes ?? [])]
							.some((t) => interactiveTypes.has(t))
'''
A9a_NEW = '''						const interactiveTypes = new Set(tpl.activity_wrapper.interactive_widget_types ?? []);
						// ROUND 322 (KB c65): a "widget"-mode [MTKquiz] SHELL holds no widget — the box is the
						// plain `activity` form (gold 142 plain vs 14 interactive around "Go to quiz")
						const mtkShellEarly = this.#mtkQuizShellBundle(bundle, it);
						const mtkPlainBox = mtkShellEarly === "widget" && mtkCfg && mtkCfg.shell_box_plain !== false;
						const forceInt = !mtkPlainBox && [bundle.type, ...(bundle.extraTypes ?? [])]
							.some((t) => interactiveTypes.has(t))
'''
cc = replace_once(cc, A9a_OLD, A9a_NEW, "(9a) plain shell box (engine)")
A9b_OLD = '''				"non_quiz_widget_ends_silence": true,
'''
A9b_NEW = '''				"non_quiz_widget_ends_silence": true,
				"shell_box_plain": true,
'''
et9 = rd(ET)
if '"shell_box_plain"' in et9: print("  = (9b) plain shell box (data): already applied")
else:
    assert et9.count(A9b_OLD) == 1, "(9b) anchor count != 1"
    et9 = et9.replace(A9b_OLD, A9b_NEW, 1); wr(ET, et9); print("  + (9b) plain shell box (data): applied")


# ---------------------------------------------------------------- (10) a bare [Trigger engagement] riding the marker
A10a_OLD = '''			if (found) it._mtkButtonAbsorbed = true;
		}
	}
'''
A10a_NEW = '''			if (found) it._mtkButtonAbsorbed = true;
			// ROUND 322 (KB c65): a BARE engagement-trigger tag riding the marker ("[button] Quiz
			// [Trigger engagement] [MTK Quiz …]", BLLR201 1F/2E) is the quiz's own attribute, not a
			// journal button — the shell has exactly one button. Label-less items only.
			const omit = this.#mtkQuizOmitCfg();
			if (omit && (omit.absorb_tags ?? []).length) {
				const abs = new Set(omit.absorb_tags), win = omit.absorb_window ?? 2;
				const isAbs = (c) => c.type === "tag" && c.parse?.primary?.directive === "ELEMENT" && abs.has(c.parse.primary.tag)
					&& !String(c.blackAfter ?? "").trim() && c.consumedBy === undefined && !c._consumed;
				const walk = (from, dir) => {
					for (let k = from, seen = 0; k >= 0 && k < bodyItems.length && seen < win; k += dir) {
						const c = bodyItems[k];
						if (c.type === "black" && !(c.text ?? "").trim()) continue;
						if (isBoundary(c)) break;
						seen++;
						if (isAbs(c)) c._mtkEngAbsorbed = true;
					}
				};
				walk(i - 1, -1); walk(i + 1, 1);
			}
		}
	}
'''
cc = replace_once(cc, A10a_OLD, A10a_NEW, "(10a) engagement trigger absorb (pre-pass)")
A10b_OLD = '''			if (it._mtkQuizAnchor) {
				const mq = tpl.interactive_builders?.mtk_quiz;
'''
A10b_NEW = '''			// ROUND 322: an engagement-trigger tag absorbed by the marker renders nothing
			if (it._mtkEngAbsorbed && this.#mtkQuizOmitCfg()) return out;
			if (it._mtkQuizAnchor) {
				const mq = tpl.interactive_builders?.mtk_quiz;
'''
if "it._mtkEngAbsorbed && this.#mtkQuizOmitCfg()" in cc: print("  = (10b) engagement trigger absorb (render): already applied")
else:
    assert cc.count(A10b_OLD) == 1, "(10b) anchor count != 1"
    cc = cc.replace(A10b_OLD, A10b_NEW, 1); print("  + (10b) engagement trigger absorb (render): applied")
A10c_OLD = '''				"shell_box_plain": true,
'''
A10c_NEW = '''				"shell_box_plain": true,
				"absorb_tags": ["engagement quiz button"],
				"absorb_window": 2,
'''
et10 = rd(ET)
if '"absorb_tags"' in et10: print("  = (10c) engagement trigger absorb (data): already applied")
else:
    assert et10.count(A10c_OLD) == 1, "(10c) anchor count != 1"
    et10 = et10.replace(A10c_OLD, A10c_NEW, 1); wr(ET, et10); print("  + (10c) engagement trigger absorb (data): applied")

wr(CC, cc)
print("done")
