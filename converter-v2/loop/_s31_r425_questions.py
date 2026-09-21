"""_s31_r425_questions.py — round 425: the adapter's Questions row — the title as the alert's lead, the list numbered.
Run under WSL from CONVERTER_V2/outputs: python3 _s31_r425_questions.py"""
import io, os
JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2", "app", "js")

def patch(name, old, new, count=1):
    p = os.path.join(JS, name)
    s = io.open(p, encoding="utf-8", newline="").read()
    assert s.count(old) == count, (name, s.count(old), old[:60])
    s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("patched", name)

patch("DocxExtractor.js",
"""			push(TAG(ad.alert_tag ?? "alert"), links);
			push(TAG("H3") + t, links);
			emitBody(qs, links);
			push(TAG("End alert"), links);
""",
"""			// the title rides the alert tag as its embedded lead (the callout's own lead element — the family's
			// alert variant fixes it at h3) unless questions_title_as_lead is false; the extractor marks every
			// cell list "• " (a cell carries no numFmt), so questions_list "numbered" restores the writer's
			// decimal list (verified in the docx: numId → decimal) and renderBlackText builds the <ol>
			const asLead = ad.questions_title_as_lead !== false;
			push(TAG(ad.alert_tag ?? "alert") + (asLead ? t : ""), links);
			if (!asLead) push(TAG("H3") + t, links);
			const numbered = ad.questions_list === "numbered";
			emitBody(numbered ? qs.map((l) => String(l).replace(/^\\s*\\u2022\\s+/, "1. ")) : qs, links);
			push(TAG("End alert"), links);
""")

patch("ModuleResolver.js",
"""			run.pageTitleFromModule = atCfg.adapter.page_title === "module";   // the splitter skips the heading harvest (round 425)
""",
"""			run.pageTitleFromModule = atCfg.adapter.page_title === "module";   // the splitter skips the heading harvest (round 425)
			run.activityBoxBare = atCfg.adapter.activity_box === "bare";   // ActivitiesBuilder: the box holds its content directly (round 425)
			run.lessonTitleRepeatsModule = atCfg.adapter.lesson_title_repeats_module === true;   // SkeletonBuilder: the second lesson h1 (round 425)
""")
