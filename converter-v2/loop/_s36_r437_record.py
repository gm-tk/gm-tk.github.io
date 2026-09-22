#!/usr/bin/env python3
"""Session 36 Round 5 — the DECLINE record (no engine change): the Round-5 PICK section moves to the archive, the Declined-classes
entry and the Round-log line are written, the in-flight marker is cleared, the Follow-up line for CEDR302 is added, and the
next-session line is refreshed. Run under WSL: python3 _s36_r437_record.py"""
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")

# 1. the Round-log line
o = "- s36-r4 (engine r436, build 260620.09"; assert st.count(o) == 1
line = ("- s36-r5 (NO engine change — DECLINED on measurement, 23 Sept 01:25 → ≈01:50) · PICK PASS on the miner's module-menu rows #36 / #37 / #49: "
        "**THE MODULE MENU'S SECTION CONTENT IS A LIST** — menu-level the case looked overwhelming (the gold's overview-menu sections are list-dominant "
        "on 428 of 453 paired menus = 0.945, Claude matching on 397, 27 modules paragraph-dominant) but it FAILS at the line level, which is where the "
        "rule would operate: a bold-labelled menu line is `<p>` in the gold 147 times vs `<li>` 29 (`_s36_r5_menubold.py`), and corpus-wide the gold's "
        "own menu content is **9,732 li / 2,881 p = 0.772 list share against Claude's 0.743** — under three points apart, so a per-line rule overshoots "
        "the human by a quarter of the content. BUILT and probed to be sure: the four changed overview pages scored SCAFFOLD +0.0 each, RAW split "
        "(MXDI301 +7.6, XDLS906 −7.6 — its gold keeps 15 paragraphs beside 22 items). Engine change REVERTED (`MenuBuilder.js` byte-identical to HEAD; "
        "the 7-module probe 34 / 34 identical), the verdict recorded in `Emit_Templates.json` `menu._declined_r437_section_content_is_list` and under "
        "Declined classes · no regeneration, no gate run · plateau unchanged (a declined round predicts no move)\n")
st = st.replace(o, line + o)

# 2. the Declined-classes entry
o = "## Declined classes\n"; assert st.count(o) == 1
st = st.replace(o, o + ("- **Session 36 Round 5 (23 Sept ≈01:50) — THE MODULE MENU'S SECTION CONTENT IS A LIST (the miner's module-menu rows #36 / #37 / #49) "
    "— DECLINED on measurement; the engine change was built, probed and REVERTED.** Menu-level evidence (`_s36_r5_menuchild.py`, 453 paired overview menus "
    "with ≥ 3 content children on both sides): gold list-dominant 428 / paragraph-dominant 10 / tied 8 = **0.945**, Claude matching on 397, the gap 27 "
    "modules (CBI1004 / 1005, the CED family, CHI1003, ENGJ102, GER1002, GEWHA, HIS1002, MUS1004, MXDB301, MXDI301, MXEX301, MXFU302, TEDC401, "
    "XDLS902–906 / 909). Line-level evidence, which is what a rule needs: (1) `_s36_r5_menubold.py` — a bold-labelled menu line is `<p>` in the gold **147** "
    "times against `<li>` **29**; (2) the corpus's own menu content is **9,732 `li` to 2,881 `p` = 0.772**, and Claude already ships **0.743** — a gap of "
    "2.9 points, not a structural defect, so listing every line would drive Claude to ≈ 1.00 and overshoot the human by a quarter of the content; (3) the "
    "built probe: four changed overview pages, SCAFFOLD **+0.0 each**, RAW split (MXDI301 +7.6, XDLS906 −7.6 — that gold keeps 15 paragraphs beside its 22 "
    "items). The paragraph-heavy modules are carrying the writer's own prose, which the human keeps as prose. Never re-open without a DISCRIMINATOR at the "
    "line level (what makes one line an item and the next a paragraph); the menu-level dominance statistic is not one. Scripts: `_s36_r5_menuchild.py`, "
    "`_s36_r5_menubold.py`, `_s36_r5_overwhat2.log`; the reverted probe `_s36_r437_probe.cjs`.\n"))

# 3. the in-flight marker
lines = st.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **ROUND 437 IN FLIGHT — NOT PROVEN**")]
assert len(idx) == 1
lines[idx[0]] = ("- **No round in flight** (23 Sept 2026 ≈01:50, session 36 Round 5 DECLINED on measurement and REVERTED — `MenuBuilder.js` is byte-identical "
                 "to HEAD and a 7-module probe is 34 / 34 identical to disk; the corpus on disk IS the r436 state, LAST SHIPPED r436). The §3 step-1 rule "
                 "stands: the next PICK raises `ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited.")
st = "\n".join(lines)

# 4. the PICK section → the archive
i0 = st.index("## Session 36 — Round 5 (engine r437) — THE MODULE MENU'S SECTION CONTENT IS A LIST")
i1 = st.index("## Session 36 — Round 4 (engine r436, build 260620.09)")
r5 = st[i0:i1]
pointer = ("## Session 36 — Round 5 (no engine change — DECLINED on measurement) — THE MODULE MENU'S SECTION CONTENT IS A LIST — the PICK + the verdict are "
           "in LOOP_STATE_ARCHIVE.md 'Session 36 — Round 5 (DECLINED …)' and under Declined classes; the one-line summary is the s36-r5 Round-log line below.\n\n")
st = st[:i0] + pointer + st[i1:]
verdict = """**THE VERDICT (23 Sept ≈01:50).** Built behind `menu.section_content_is_list` / `MENULIST_OFF` (MenuBuilder's `flushText` prefixing the corpus bullet glyph to every buffered line once a section heading had been emitted in that column, so the existing list machinery rendered them; a `max_words` guard kept genuine prose as paragraphs). The five-module probe changed four overview pages and scored them **SCAFFOLD +0.0 each** with RAW split (MXDI301 +7.6, XDLS906 −7.6). The follow-up measurement settled it: the gold's own overview-menu content is **9,732 `li` to 2,881 `p` (0.772)** and Claude already ships **0.743** — the two are less than three points apart, so the 27 "paragraph-dominant" modules are not a defect class but modules whose writers supplied more prose, which the human keeps as prose. A per-line rule would push Claude to ≈ 1.00 list and overshoot the human by a quarter of the menu's content. REVERTED: `MenuBuilder.js` is byte-identical to HEAD (`git diff` empty) and a 7-module probe (MXDI301, MXEX301, XDLS906, TEDC401, GEWHA, CEDR302, BLL125) is **34 / 34 identical to disk**; the corpus was never regenerated. The verdict is recorded in `Emit_Templates.json` as `menu._declined_r437_section_content_is_list` — the data file is the place a later round will look — and under Declined classes here. What would re-open it: a DISCRIMINATOR at the line level (what makes one menu line an item and the next a paragraph), not the menu-level dominance statistic.
"""
assert "## Session 36 — Round 5 (DECLINED" not in ar
r5_head = "## Session 36 — Round 5 (DECLINED on measurement, no engine change, 23 Sept 01:25 → ≈01:50) — THE MODULE MENU'S SECTION CONTENT IS A LIST + the verdict\n\n"
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n" + r5_head + r5.split("\n", 1)[1].strip("\n") + "\n\n" + verdict)

# 5. the Follow-up line for CEDR302
o = "- **(r436) The REPEATED MODULE-OVERVIEW MENU"; assert st.count(o) == 1
st = st.replace(o, ("- **(r437) CEDR302's overview menu holds 89 elements** — 24 of them the gold places in inquiry panels, accordions and activity boxes "
                    "(`_s36_r5_overwhat2.log`): the menu/body boundary is never found on that page, so almost the whole module sits in "
                    "`#module-menu-content`. ONE module (below floor), but it is the last large single-page menu overrun left after r432 / r435 / r436 and "
                    "the biggest remaining single-page menu defect in the corpus. It is a CEDR Inquiry module — check it against the r428–r430 inquiry "
                    "fallback shells before treating it as its own class.\n" + o))

i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the "
               "\"Amended:\" line; the §7 diff check; `git status` CLEAN at the session-36 commits). No round in flight (r436 is LAST SHIPPED; the Round-5 "
               "candidate was declined and reverted — see Declined classes). **The ship ledger is at scoped #3 since the r433 FULL (5 of headroom).** The "
               "module-menu chrome region is now dispositioned end to end: r432 the implicit block, r435 the `[Body]` stop, r436 the continuation page, the "
               "repeated module-overview class DECLINED as a KB override, the section-content-is-list class DECLINED on measurement. The open leads: "
               "CEDR302's 89-element overview menu (one module, the Follow-up section's top line), the body's ROW COMPOSITION class (the r435 dips), the "
               "miner's 196 rows re-read on the r436 corpus, the KB queue, the widget census and the loss ledger. NEEDS CHRIS: the open lines of the "
               "\"Needs Chris\" section.\n")
wr(R + "LOOP_STATE.md", st)
print("record OK")
