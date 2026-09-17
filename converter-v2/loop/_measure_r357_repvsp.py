"""Session 17 PICK probe: the `┌ N× repeated: ⇐ p` substitution sites — what block does the gold repeat where Claude has one <p>?"""
import os, sys, re, difflib, collections
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests")); sys.path.insert(0, TESTS)
import _corpus, _skeleton_compare as S
from _discrepancy_audit import pairs, CLAUDE
codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
shapes=collections.Counter(); pg=collections.defaultdict(set); ex=collections.defaultdict(list)
for code in codes:
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code)))
    if tmpl!='Standard': continue
    for _, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary', os.path.basename(hp)+os.path.basename(cp), re.I): continue
        try: _, a, b = S.match(cp, hp, scaffold=True)
        except Exception: continue
        sm = difflib.SequenceMatcher(None, b, a, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "replace" or (i2-i1)!=(j2-j1): continue
            for k in range(i2-i1):
                gl=b[i1+k].strip(); cl=a[j1+k].strip()
                if gl.startswith('┌') and 'repeated:' in gl and cl=='p':
                    gblock=" > ".join(x.strip() for x in b[i1+k+1:i1+k+4]); cblock=" > ".join(x.strip() for x in a[j1+k+1:j1+k+4])
                    key=(gl, gblock[:60]); shapes[key]+=1; pg[key].add(os.path.basename(cp))
                    if len(ex[key])<3: ex[key].append((os.path.basename(cp), cblock[:60]))
for k,v in shapes.most_common(15): print(v, len(pg[k]), k, ex[k][:2])
