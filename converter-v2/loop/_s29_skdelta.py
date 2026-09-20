#!/usr/bin/env python3
"""_s29_skdelta.py — per-page skeleton delta between two _skeleton_compare.py --json states.
Usage: python3 _s29_skdelta.py OLD.json NEW.json [--affected FILE]
Prints the full-precision means / buckets of both, every mover (with its module), the up/down/pp-sum,
and — with --affected — whether any mover lies outside the affected module list."""
import json, sys
old = json.load(open(sys.argv[1]))
new = json.load(open(sys.argv[2]))
aff = set()
if '--affected' in sys.argv:
    aff = {l.strip() for l in open(sys.argv[sys.argv.index('--affected') + 1]) if l.strip()}

def stats(d):
    pp = d['per_page']; n = len(pp)
    sc = [p['scaffold'] for p in pp]
    return dict(pages=n, mean=100 * sum(sc) / n, raw=100 * d['raw_mean'],
                ge50=sum(1 for s in sc if s >= .5), ge75=sum(1 for s in sc if s >= .75), ge90=sum(1 for s in sc if s >= .9))

so, sn = stats(old), stats(new)
for lab, s in (('OLD', so), ('NEW', sn)):
    print('%s pairs %d  SCAFFOLD %.4f%%  RAW %.3f%%  >=50 %d  >=75 %d  >=90 %d' % (lab, s['pages'], s['mean'], s['raw'], s['ge50'], s['ge75'], s['ge90']))
print('delta SCAFFOLD %+.4fpp  RAW %+.3fpp  >=50 %+d  >=75 %+d  >=90 %+d' % (sn['mean'] - so['mean'], sn['raw'] - so['raw'], sn['ge50'] - so['ge50'], sn['ge75'] - so['ge75'], sn['ge90'] - so['ge90']))
om = {(p['module'], p['page']): p for p in old['per_page']}
nm = {(p['module'], p['page']): p for p in new['per_page']}
movers = []
for k in nm:
    if k in om and abs(nm[k]['scaffold'] - om[k]['scaffold']) > 1e-9:
        movers.append((k, 100 * (nm[k]['scaffold'] - om[k]['scaffold']), 100 * om[k]['scaffold'], 100 * nm[k]['scaffold']))
movers.sort(key=lambda m: -m[1])
up = [m for m in movers if m[1] > 0]; dn = [m for m in movers if m[1] < 0]
print('movers %d (up %d / down %d), pp-sum %+.1f' % (len(movers), len(up), len(dn), sum(m[1] for m in movers)))
outside = sorted({m[0][0] for m in movers} - aff) if aff else []
if aff:
    print('movers outside the affected set: %d %s' % (len(outside), outside[:10]))
print('new-only pages: %d  gone pages: %d' % (len(set(nm) - set(om)), len(set(om) - set(nm))))
for k, d, a, b in movers:
    print('  %-10s %-24s %6.1f -> %6.1f  (%+.1f)' % (k[0], k[1], a, b, d))
