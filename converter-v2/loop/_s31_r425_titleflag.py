"""_s31_r425_titleflag.py — round 425: the adapted XOTP pages take the MODULE title (skip the heading harvest).
Run under WSL from CONVERTER_V2/outputs: python3 _s31_r425_titleflag.py"""
import io, os
JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2", "app", "js")

def patch(name, old, new):
    p = os.path.join(JS, name)
    s = io.open(p, encoding="utf-8", newline="").read()
    assert s.count(old) == 1, (name, s.count(old))
    s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("patched", name)

patch("PageSplitter.js",
"""		for (const p of pages) {
			if (p.isOverview) continue;
			// ROUND 344 (D10-1 sibling""",
"""		for (const p of pages) {
			if (p.isOverview) continue;
			// ROUND 425 (the activity-table adapter): the adapted stream's pages carry the MODULE title as
			// their own — the gold's lesson h1 repeats the module title on every XOTP page — so the
			// heading harvest is skipped and the SkeletonBuilder fallback applies. Set by ModuleResolver
			// from `input_shapes.activity_table.adapter.page_title === "module"`; env ACTTABLEADAPT_OFF.
			if (run && run.pageTitleFromModule) continue;
			// ROUND 344 (D10-1 sibling""")

patch("ModuleResolver.js",
"""			run.noOverviewPage = atCfg.adapter.no_overview_page === true;   // the splitter's RR-4 folds the title bar into lesson 1
""",
"""			run.noOverviewPage = atCfg.adapter.no_overview_page === true;   // the splitter's RR-4 folds the title bar into lesson 1
			run.pageTitleFromModule = atCfg.adapter.page_title === "module";   // the splitter skips the heading harvest (round 425)
""")
