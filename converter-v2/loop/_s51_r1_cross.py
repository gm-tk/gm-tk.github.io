import re, collections
seq = {}
for l in open("_s51_r1_actseq.tsv"):
    if l.startswith("#"): continue
    k, code, page, at, sh, g, c = l.rstrip("\n").split("\t")
    seq[(code, page)] = (k, g, c)
cnt = collections.Counter(); ex = collections.defaultdict(list)
for l in open("_s51_r1_numnorm.log"):
    code, lab, ren = l.rstrip("\n").split("\t")[:3]
    page = f"{code}_{lab.replace('.', '_')}.html"
    chain = len(ren.split(", "))
    k = seq.get((code, page), ("EQUAL?", "", ""))
    cls = k[0] + (" chain" if chain >= 2 else " single")
    cnt[cls] += 1; ex[cls].append(f"{page} | {ren} | gold {k[1]} | claude {k[2]}")
for c, n in cnt.most_common(): print(n, c)
for c in ("MISSING1 chain", "OTHER chain", "SHIFTED chain", "EXTRA1 chain", "EQUAL? chain"):
    print("==", c); print("\n".join(x[:170] for x in ex[c][:12]))
