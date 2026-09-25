import json
a = json.load(open("_rhsalert_measure.json")); b = json.load(open("_r505_measure_on.json"))
assert len(a) == len(b)
gain = lose = mv = 0
for x, y in zip(a, b):
    if x["claude"] == y["claude"]: continue
    mv += 1
    ok0, ok1 = x["gold"] == x["claude"], y["gold"] == y["claude"]
    tag = "GAIN" if ok1 and not ok0 else ("LOSE" if ok0 and not ok1 else "moved")
    gain += tag == "GAIN"; lose += tag == "LOSE"
    print(f"  {tag:5s} {x['code']:9s} {x['tag'][:30]:30s} gold={x['gold']:18s} {x['claude']:18s} -> {y['claude']:18s} {x['text'][:36]!r}")
print(f"moved {mv}: gain {gain} / lose {lose}")
