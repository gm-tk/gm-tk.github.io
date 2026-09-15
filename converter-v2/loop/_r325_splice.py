#!/usr/bin/env python3
"""ROUND 325 — phase-scoped activity numbering on Fundamentals phase pages (the r217 / r266 recorded
follow-up). Anchored, idempotent engine + data edits (env R325_ROOT overrides the target tree).

  (1) data  Emit_Templates.activity_wrapper.phase_numbering {enabled, env PHASENUM_OFF}
  (2) engine ContentConverter phasebreak handler: the phase ordinal becomes the page's activity-number
      prefix on ANY page with no lesson number of its own (not only the level-pages dialect)
"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("R325_ROOT") or os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
CC = os.path.join(ROOT, "app", "js", "ContentConverter.js")
ET = os.path.join(ROOT, "data", "Emit_Templates.json")
def rd(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
def step(src, key, old, new, label):
    if key in src: print(f"  = {label}: already applied"); return src
    n = src.count(old); assert n == 1, f"{label}: anchor count {n} != 1"
    print(f"  + {label}: applied"); return src.replace(old, new, 1)

et = rd(ET)
D_OLD = '\t\t"standalone_widget_box": {\n\t\t\t"enabled": true,\n'
D_NEW = ('\t\t"phase_numbering": {\n'
    '\t\t\t"_doc": "ROUND 325 (the autonomous loop\'s session-3 Round 12, 2026-09-15 — the r217 / r266 recorded follow-up \'fundamentals number by PHASE\'). On a page with NO lesson number of its own (the single-file Fundamentals modules), the human numbers every activity box {phase}{letter} — the letter sequence restarting in each phase panel (measured over every Fundamentals gold page with numbered boxes, outputs/_measure_r325_phasenumbers.py: 53 of 101 pages follow the rule exactly, the rest are the same rule with the human\'s own gaps / duplicates / sub-page continuations; 788 gold boxes vs Claude\'s 397, of which 111 unnumbered and 45 bare digits). Round 266 derived the ordinal only for the level-pages dialect (run._levelMenu); this generalises it: every phasebreak on a lesson-number-less page advances the page\'s activity-number prefix, so the existing rules fire — a writer\'s bare-digit id renumbers to {phase}{letter} (round 88), a writer LETTER id is kept, and the round-217 synthetic standalone-widget box asserts (it was withheld where no number was derivable). Simulated before coding: position-wise number matches against the gold 66 → 133 over the 51 phase-panel modules. Env PHASENUM_OFF reverts byte-for-byte.",\n'
    '\t\t\t"enabled": true,\n'
    '\t\t\t"env": "PHASENUM_OFF"\n'
    '\t\t},\n' + D_OLD)
et = step(et, '"phase_numbering"', D_OLD, D_NEW, "(1) data activity_wrapper.phase_numbering")
wr(ET, et)

cc = rd(CC)
E_OLD = ('\t\t\t\tif (run._levelMenu) {\n'
         '\t\t\t\t\tthis.#pageLessonNumber = (typeof this.#pageLessonNumber === "number")\n'
         '\t\t\t\t\t\t? this.#pageLessonNumber + 1 : 1;\n'
         '\t\t\t\t}\n')
E_NEW = ('\t\t\t\t// ROUND 325 (the r217 / r266 follow-up): the same phase ordinal on EVERY page that has\n'
         '\t\t\t\t// no lesson number of its own — the single-file Fundamentals modules — so the bare-digit\n'
         '\t\t\t\t// renumber (r88) and the synthetic standalone box (r217) fire {phase}{letter} there too.\n'
         '\t\t\t\t// Data activity_wrapper.phase_numbering; env PHASENUM_OFF.\n'
         '\t\t\t\tconst _pnCfg = tpl.activity_wrapper?.phase_numbering;\n'
         '\t\t\t\tconst _pnOn = !!_pnCfg && _pnCfg.enabled !== false\n'
         '\t\t\t\t\t&& !(typeof process !== "undefined" && process.env && process.env[_pnCfg.env ?? "PHASENUM_OFF"])\n'
         '\t\t\t\t\t&& page.lessonNumber == null;\n'
         '\t\t\t\tif (run._levelMenu || _pnOn) {\n'
         '\t\t\t\t\tthis.#pageLessonNumber = (typeof this.#pageLessonNumber === "number")\n'
         '\t\t\t\t\t\t? this.#pageLessonNumber + 1 : 1;\n'
         '\t\t\t\t}\n')
cc = step(cc, "const _pnCfg = tpl.activity_wrapper?.phase_numbering;", E_OLD, E_NEW, "(2) phasebreak ordinal on every lesson-number-less page")

# ---------------------------------------------------------------- (3) a writer bare digit wins over the scanner dedupe
A3a_OLD = '''						emit(...ActivitiesBuilder.activityOpen(actOwner, stack, run, false, bundle.activityId, forceInt, bSupNote, this.#pageLessonNumber, this.#lessonLetterMap, actOwner === saOwner || actOwner === lvOwner));
'''
A3a_NEW = '''						emit(...ActivitiesBuilder.activityOpen(actOwner, stack, run, false, this.#phaseBareId(actOwner, bundle.activityId, tpl), forceInt, bSupNote, this.#pageLessonNumber, this.#lessonLetterMap, actOwner === saOwner || actOwner === lvOwner));
'''
cc = step(cc, "this.#phaseBareId(actOwner, bundle.activityId, tpl)", A3a_OLD, A3a_NEW, "(3a) owned site bare id")
A3b_OLD = '''						emit(...ActivitiesBuilder.activityOpen(it, stack, run, true, it._r307PanelId ?? it._activityIdOverride ?? null, false, supNote, this.#pageLessonNumber, this.#lessonLetterMap));
'''
A3b_NEW = '''						emit(...ActivitiesBuilder.activityOpen(it, stack, run, true, this.#phaseBareId(it, it._r307PanelId ?? it._activityIdOverride ?? null, tpl), false, supNote, this.#pageLessonNumber, this.#lessonLetterMap));
'''
cc = step(cc, "this.#phaseBareId(it, it._r307PanelId", A3b_OLD, A3b_NEW, "(3b) opener site bare id")
A3c_OLD = '''	static #buttonLabelTrim(label, tpl) {
'''
A3c_NEW = '''	/**
	 * ROUND 325 — under PHASE numbering a writer's BARE-DIGIT id wins over the scanner's
	 * collision letter: the InteractiveScanner de-dupes repeated ids module-wide ("[Activity 1]"
	 * in phases 1, 2, 3 → "1", "1A", "1B") and activityOpen KEEPS a lettered id, so ENFUN02's
	 * phase-2 box shipped "1A" instead of "2A". With the phase ordinal live the writer's own
	 * bare digit is passed instead and the round-88 renumber makes it {phase}{letter}.
	 * Data activity_wrapper.phase_numbering.writer_digit_over_dedupe; env PHASENUM_OFF.
	 */
	static #phaseBareId(it, override, tpl) {
		const cfg = tpl?.activity_wrapper?.phase_numbering;
		if (!cfg || cfg.enabled === false || cfg.writer_digit_over_dedupe === false) return override;
		if (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "PHASENUM_OFF"]) return override;
		if (typeof this.#pageLessonNumber !== "number") return override;   // only a phase-derived ordinal
		const writer = String(it?.parse?.numbers?.[0] ?? "").toUpperCase();
		if (/^\\d+$/.test(writer) && override != null && /^\\d+[A-Z]$/.test(String(override))
			&& String(override).slice(0, -1) === writer) return writer;
		return override;
	}

	static #buttonLabelTrim(label, tpl) {
'''
cc = step(cc, "static #phaseBareId(it, override, tpl) {", A3c_OLD, A3c_NEW, "(3c) #phaseBareId helper")
A3d_OLD = '''			"enabled": true,
			"env": "PHASENUM_OFF"
		},
'''
A3d_NEW = '''			"enabled": true,
			"env": "PHASENUM_OFF",
			"writer_digit_over_dedupe": true
		},
'''
et3 = rd(ET); et3 = step(et3, '"writer_digit_over_dedupe"', A3d_OLD, A3d_NEW, "(3d) data writer_digit_over_dedupe"); wr(ET, et3)

# ---------------------------------------------------------------- (4) the ordinal follows the panels
A4_OLD = '''				if (run._levelMenu || _pnOn) {
					this.#pageLessonNumber = (typeof this.#pageLessonNumber === "number")
						? this.#pageLessonNumber + 1 : 1;
				}
				parts.push(it.kind === "lesson" ? FUND_LESSON_SENTINEL : FUND_PHASETEXT_SENTINEL);
'''
A4_NEW = '''				// the ordinal follows the PANELS: PanelsBuilder drops an empty segment between two
				// sentinels, so a phasebreak whose previous segment made no panel does not advance
				const _pnPrevEmpty = _pnOn && !run._levelMenu && page._pnSegStart != null
					&& parts.slice(page._pnSegStart).join("").trim() === "";
				if (run._levelMenu || (_pnOn && !_pnPrevEmpty)) {
					this.#pageLessonNumber = (typeof this.#pageLessonNumber === "number")
						? this.#pageLessonNumber + 1 : 1;
				}
				parts.push(it.kind === "lesson" ? FUND_LESSON_SENTINEL : FUND_PHASETEXT_SENTINEL);
				page._pnSegStart = parts.length;
'''
cc = step(cc, "const _pnPrevEmpty = _pnOn", A4_OLD, A4_NEW, "(4) ordinal follows the panels")

# ---------------------------------------------------------------- (5) synthetic box unnumbered on phase pages
A5_OLD = '''						emit(...ActivitiesBuilder.activityOpen(actOwner, stack, run, false, this.#phaseBareId(actOwner, bundle.activityId, tpl), forceInt, bSupNote, this.#pageLessonNumber, this.#lessonLetterMap, actOwner === saOwner || actOwner === lvOwner));
'''
A5_NEW = '''						// ROUND 325: on a PHASE-numbered page the human leaves its invented boxes UNNUMBERED
						// (TEFUN04 gold 1A,-,-,-,1B) — the synthetic box takes no letter there
						const _pnPhasePage = typeof this.#pageLessonNumber === "number" && !run._levelMenu
							&& (tpl.activity_wrapper?.phase_numbering?.synthetic_unnumbered !== false);
						emit(...ActivitiesBuilder.activityOpen(actOwner, stack, run, false, this.#phaseBareId(actOwner, bundle.activityId, tpl), forceInt, bSupNote, this.#pageLessonNumber, this.#lessonLetterMap, (actOwner === saOwner && !_pnPhasePage) || actOwner === lvOwner));
'''
cc = step(cc, "const _pnPhasePage = typeof this.#pageLessonNumber", A5_OLD, A5_NEW, "(5a) synthetic box unnumbered on phase pages")
A5d_OLD = '''			"env": "PHASENUM_OFF",
			"writer_digit_over_dedupe": true
		},
'''
A5d_NEW = '''			"env": "PHASENUM_OFF",
			"writer_digit_over_dedupe": true,
			"synthetic_unnumbered": false
		},
'''
et5 = rd(ET); et5 = step(et5, '"synthetic_unnumbered"', A5d_OLD, A5d_NEW, "(5b) data synthetic_unnumbered"); wr(ET, et5)
wr(CC, cc)
print("done")
