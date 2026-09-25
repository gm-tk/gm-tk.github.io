import json, collections
a = json.load(open("_r505_measure_on.json")); b = json.load(open("_r506_measure_on.json"))   # before = the shipped r505 state
side = lambda s: s.startswith("side-")
mv = gain = lose = colgain = collose = 0
for x, y in zip(a, b):
    if x["claude"] == y["claude"]: continue
    mv += 1
    ok0, ok1 = x["gold"] == x["claude"], y["gold"] == y["claude"]
    c0, c1 = side(x["gold"]) == side(x["claude"]), side(y["gold"]) == side(y["claude"])
    gain += ok1 and not ok0; lose += ok0 and not ok1; colgain += c1 and not c0; collose += c0 and not c1
    print(f"  {x['code']:9s} {x['tag'][:30]:30s} gold={x['gold']:18s} {x['claude']:18s} -> {y['claude']:18s} {x['text'][:34]!r}")
found = [r for r in b if r["gold"] not in ("absent", "no text")]
print(f"moved {mv}: exact-shape gain {gain} / lose {lose}; side-column agreement gain {colgain} / lose {collose}")
print(f"after: exact = {sum(r['gold'] == r['claude'] for r in found)} / {len(found)}; side-column agreement = {sum(side(r['gold']) == side(r['claude']) for r in found)} / {len(found)}")
a_found = [r for r in a if r["gold"] not in ("absent", "no text")]
print(f"before: exact = {sum(r['gold'] == r['claude'] for r in a_found)}; side-column agreement = {sum(side(r['gold']) == side(r['claude']) for r in a_found)}")
