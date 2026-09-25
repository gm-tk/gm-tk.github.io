"""_s50_r7_animchar.py — session 50 Round 7 PICK: every `[Insert animated character]` red tag in the Writers Templates — does the
module's gold carry a Vimeo player on the page that holds the text right before the tag (and right after it)? Does the gold ever show
the writer's 'Animation Script' link? Run under WSL from CONVERTER_V2/outputs/."""
import os, re, glob, collections
G = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_"
C = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Claude_Modules_"
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()
stats = collections.Counter(); ex = []
for wt in glob.glob(f"{G}/*/*/*_parsed.txt"):
    if re.search(r"/[^/+]* Media List_parsed\.txt$", wt): continue
    code = wt.split("/")[-2]
    lines = open(wt, encoding="utf-8", errors="ignore").read().split("\n")
    golds = {p: open(p, encoding="utf-8", errors="ignore").read() for p in glob.glob(os.path.join(os.path.dirname(wt), "*.html"))}
    for i, ln in enumerate(lines):
        if not re.search(r"\[\s*insert\s+animated\s+character", ln, re.I): continue
        stats["tags"] += 1
        prev = next((re.sub(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴", " ", l) for l in reversed(lines[:i]) if re.sub(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴", " ", l).strip()), "")
        key = norm(prev)[:60]
        page = next((p for p, h in golds.items() if key and key[:40] in norm(re.sub(r"<[^>]+>", " ", h))), None)
        if not page: stats["prev text not found in gold"] += 1; continue
        h = golds[page]; t = norm(re.sub(r"<[^>]+>", " ", h)); at = t.find(key[:40])
        # the gold markup right after the preceding text
        raw_at = h.lower().find(key[:25].split()[0]) if key else -1
        vimeo_page = "player.vimeo.com" in h
        stats["gold page has vimeo" if vimeo_page else "gold page NO vimeo"] += 1
        m = re.search(re.escape(prev.strip()[-30:]).replace("\\ ", r"\s+"), h) if prev.strip() else None
        near = h[m.end(): m.end() + 900] if m else ""
        stats["vimeo within 900 chars after" if "player.vimeo.com" in near else "no vimeo right after"] += 1
        stats["gold shows 'Animation Script'" if "animation script" in h.lower() else "gold hides 'Animation Script'"] += 1
        if len(ex) < 6: ex.append(f"{code}: {os.path.basename(page)} vimeo_page={vimeo_page} near={'player.vimeo.com' in near}")
print(dict(stats)); print("\n".join(ex))
cl = glob.glob(f"{C}/*/*/*.html")
print("Claude pages with 'Writers Note: [Insert animated character]':", sum(1 for p in cl if "Writers Note: [Insert animated character]" in open(p, encoding="utf-8", errors="ignore").read()))
