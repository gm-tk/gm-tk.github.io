import json, collections
rows = [r for r in json.load(open("_rhsalert_measure.json")) if r["gold"] not in ("absent", "no text")]
side = lambda s: s.startswith("side-")
miss = [r for r in rows if not side(r["claude"]) and r["template"] != "Inquiry"]
print(f"non-Inquiry tags where Claude builds NO side column: {len(miss)}  (gold side {sum(side(r['gold']) for r in miss)})")
for k, v in collections.Counter((r["spelling"], r["claude"]) for r in miss).most_common(40): print(f"  {v:3d}  {k[0]:40s} claude={k[1]}")
print("\nby module:", ", ".join(f"{k} {v}" for k, v in collections.Counter(r["code"] for r in miss).most_common(40)))
print("\nthe misses (non-Inquiry), gold shape / claude shape / page / text:")
for r in sorted(miss, key=lambda r: (r["claude"], r["code"])):
    print(f"  {r['code']:9s} {r['tag'][:34]:34s} gold={r['gold']:18s}@{str(r['gold_page'])[:16]:16s} claude={r['claude']:6s}@{str(r['claude_page'])[:16]:16s} {r['text'][:40]!r}")
