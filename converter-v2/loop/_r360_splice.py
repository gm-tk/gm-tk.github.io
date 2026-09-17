#!/usr/bin/env python3
"""ROUND 360 (loop session 19, Round 4 — the footer link set follows the KB's sub-type forms) — the anchored, tab-preserving
Style_Anchor_Registry.json splice (no engine change). Idempotent; json duplicate-key guard; tabs-only indentation.

  ARFUN / ENFUN / TEFUN base_rules  + footer_links {overview: home, lesson: prev+next+home, final: prev+home}   (06 §3.3)
  MXFUN base_rules                  footer_links {prev+next+home, —, —} (a no-evidence object, skipped whole) → the same
  CEDK base_rules ({})              + footer_links {prev+next+home, prev+next+home, prev+home}                  (06 §3.4)
  EXPFUN base_rules                 footer_links {—, prev+next+home, …} → {prev+next+home, prev+next+home, prev+home}
  BLL1.template_deltas.Inquiry      + footer_links {prev+next+home, prev+next+home, prev+home}  (the existing r357 block)
  BLL2                              + template_deltas.Inquiry.footer_links (new block)
  CEDO / CEDR / CEDW bases          + template_deltas.Inquiry.footer_links (new blocks; their Standard members untouched)
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
REG = os.path.join(ROOT, "pageforge-site", "converter-v2", "data", "Style_Anchor_Registry.json")
raw = open(REG, encoding="utf-8", newline="").read(); assert "\r\n" not in raw
L = raw.split("\n"); T = "\t"
HOME = ("home", "prev+next+home", "prev+home"); INQ = ("prev+next+home", "prev+next+home", "prev+home")


def find(pred, start, end):
    for i in range(start, min(end, len(L))):
        if pred(L[i]):
            return i
    return -1


def anchor(text):
    i = find(lambda s, t=text: s.strip() == t, 0, len(L)); assert i >= 0, text; return i


def fl_block(depth, vals, trailing):
    d = T * depth
    return [f'{d}"footer_links": {{', f'{d}{T}"overview": "{vals[0]}",', f'{d}{T}"lesson": "{vals[1]}",', f'{d}{T}"final": "{vals[2]}"', f'{d}}}' + ("," if trailing else "")]


def set_or_insert_in_base_rules(base, vals):
    """footer_links inside <base>.base_rules: replace the existing block's values, or insert one."""
    a = anchor(f'"{base}": {{')
    br = find(lambda s: s.strip() == '"base_rules": {' or s.strip() == '"base_rules": {},', a, a + 6); assert br > 0, base
    if L[br].strip() == '"base_rules": {},':
        L[br:br + 1] = [T * 4 + '"base_rules": {'] + fl_block(5, vals, False) + [T * 4 + '},']
        return "inserted (was {})"
    lv = find(lambda s: s.strip() == '"levels": {', br, br + 400)
    f = find(lambda s: s.strip() == '"footer_links": {', br, lv)
    if f > 0:
        ind = L[f + 1][:len(L[f + 1]) - len(L[f + 1].lstrip(T))]
        L[f + 1] = f'{ind}"overview": "{vals[0]}",'; L[f + 2] = f'{ind}"lesson": "{vals[1]}",'; L[f + 3] = f'{ind}"final": "{vals[2]}"'
        assert L[f + 4].strip().startswith("}"), (base, L[f + 4])
        return "replaced"
    # insert as the first key of base_rules
    L[br + 1:br + 1] = fl_block(5, vals, True)
    return "inserted"


def add_template_delta(anchor_text, depth, vals, existing_ok=True):
    """template_deltas.Inquiry.footer_links at a base (depth 4) or a level (depth 6)."""
    a = anchor(anchor_text)
    # within the object: an existing template_deltas block?
    end = find(lambda s: s.strip() in ('"levels": {', '"delta": {'), a, a + 400)
    td = find(lambda s: s.strip() == '"template_deltas": {', a, end if end > 0 else a + 400)
    if td > 0:
        inq = find(lambda s: s.strip() == '"Inquiry": {', td, td + 30); assert inq > 0, anchor_text
        if find(lambda s: s.strip() == '"footer_links": {', inq, inq + 30) > 0:
            return "already"
        # insert after the "Inquiry": { line
        L[inq + 1:inq + 1] = fl_block(depth + 2, vals, True)
        return "added to the existing Inquiry delta"
    ins = end; assert ins > 0, anchor_text
    d = T * depth
    L[ins:ins] = [f'{d}"template_deltas": {{', f'{d}{T}"Inquiry": {{'] + fl_block(depth + 2, vals, False) + [f'{d}{T}}}', f'{d}}},']
    return "new template_deltas block"


done = {}
for b in ("ARFUN", "ENFUN", "TEFUN", "MXFUN"):
    done[b] = set_or_insert_in_base_rules(b, HOME)
for b in ("CEDK", "EXPFUN"):
    done[b] = set_or_insert_in_base_rules(b, INQ)
done["BLL1"] = add_template_delta('"BLL1": {', 6, INQ)
done["BLL2"] = add_template_delta('"BLL2": {', 6, INQ)
for b in ("CEDO", "CEDR", "CEDW"):
    done[b] = add_template_delta(f'"{b}": {{', 4, INQ)

new = "\n".join(L)
def no_dupes(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise SystemExit(f"duplicate key in {keys}")
    return dict(pairs)
json.loads(new, object_pairs_hook=no_dupes)
for ln in L:
    lead = ln[:len(ln) - len(ln.lstrip())]
    if " " in lead:
        raise SystemExit(f"space indentation introduced: {ln[:60]!r}")
open(REG, "w", encoding="utf-8", newline="").write(new)
print("registry edits:", done)
