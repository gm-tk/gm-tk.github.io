#!/usr/bin/env python3
"""ROUND 357 (loop session 19, Round 1) — the anchored data + engine splice.

(1) data/Style_Anchor_Registry.json (TAB-indented, LF — edited line-wise, never json.dumps'd, CLAUDE.md §16):
    _meta.template_deltas (the new tier's flag + doc) and _how_to_edit.template_override;
    PNR base_rules.module_code {full-code, padded-number}; SCFUN base_rules.module_code {full-code, padded-number};
    CEDT2 delta.module_code {absent, decimal}; CEDT3 delta.module_code {full-code, decimal};
    EXPFUN base_rules.module_code {absent, decimal} + template_deltas.Standard.module_code {full-code, decimal};
    OSSC base_rules.module_code.lesson padded-number; CEDK5 delta.module_code {absent, decimal};
    CEDO1 template_deltas.Inquiry.module_code {absent, decimal}; BLL1 template_deltas.Inquiry.module_code {absent, padded-number}.
(2) app/js/ModuleResolver.js — the template_deltas overlay after the level delta (env TMPLDELTA_OFF).
Idempotent: every edit tests for its own inserted PREFIX first (the r315 lesson). Validates: json.loads with a
duplicate-key guard, tabs-only indentation on every touched line, node --check on the engine.
"""
import os, re, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
REG = os.path.join(ROOT, "pageforge-site", "converter-v2", "data", "Style_Anchor_Registry.json")
MR = os.path.join(ROOT, "pageforge-site", "converter-v2", "app", "js", "ModuleResolver.js")

raw = open(REG, encoding="utf-8", newline="").read()
assert "\r\n" not in raw, "registry must be LF"
L = raw.split("\n")
T = "\t"


def find(pred, start=0, end=None):
    for i in range(start, end if end is not None else len(L)):
        if pred(L[i]):
            return i
    raise SystemExit(f"anchor not found from {start}: {pred.__doc__ or pred}")


def anchor(text, start=0):
    return find(lambda s, t=text: s.strip() == t or s.strip().startswith(t), start)


def set_pattern(anchor_text, field, overview, lesson, within=60):
    """Replace the two value lines of `field` (a {overview, lesson} pattern) inside the tier that starts at anchor_text."""
    a = anchor(anchor_text)
    f = find(lambda s: s.strip() == f'"{field}": {{', a, a + within)
    ov, le = L[f + 1], L[f + 2]
    assert '"overview":' in ov and '"lesson":' in le, (anchor_text, ov, le)
    ind = ov[:len(ov) - len(ov.lstrip("\t"))]
    L[f + 1] = f'{ind}"overview": "{overview}",'
    L[f + 2] = f'{ind}"lesson": "{lesson}"'
    return f


def insert_after(idx, lines):
    L[idx + 1:idx + 1] = lines


def pattern_block(depth, field, overview, lesson, trailing_comma):
    d = T * depth
    return [f'{d}"{field}": {{', f'{d}{T}"overview": "{overview}",', f'{d}{T}"lesson": "{lesson}"', f'{d}}}' + ("," if trailing_comma else "")]


def template_deltas_block(depth, template, overview, lesson, trailing_comma):
    d = T * depth
    return ([f'{d}"template_deltas": {{', f'{d}{T}"{template}": {{'] + pattern_block(depth + 2, "module_code", overview, lesson, False)
            + [f'{d}{T}}}', f'{d}}}' + ("," if trailing_comma else "")])


done = []
# ---- (1a) _meta.template_deltas + _how_to_edit.template_override
if not any('"template_deltas": {' in s and s.startswith(T * 2 + '"') for s in L[:80]):
    i = anchor('"module_code_to_level": {')
    doc = ("ROUND 357 (the autonomous loop's session-19 Round 1, 2026-09-17 — the diff miner's first chrome class, DIFF_QUEUE F15 / F14: the "
           "#module-code chip's PRESENCE). A FIFTH, optional cascade tier at a base or a level: {\\\"<template_type>\\\": {field: value}} — "
           "Standard / Inquiry / Fundamentals / Bilingual, the 01-Finalized_Modules_ folder names — overlaid AFTER the level delta (so it "
           "outranks it) when the module's template type is known from Module_Structure_Index.module_meta (the same index the evidence floor "
           "reads); a module the index does not know gets NO template delta and keeps the level's value, exactly as before this round. WHY: a "
           "mined level can hold two template families the human built differently — the BLL1 level is the seven INQUIRY parents (BLL110 … "
           "BLL170: no chip in 6 of their 7 golds) plus their 56 STANDARD children (a chip on every page); CEDO1 is CEDO102 (Inquiry, no chip) "
           "beside CEDO105 (Standard, chip); the EXPFUN base is five Inquiry modules (no chip) beside EXPFUN07 (Standard, chip). Pattern fields "
           "resolve as WHOLE objects here too; unknown literals are skipped as in every tier. Measured: outputs/_measure_r357_chip.py.")
    block = [T * 2 + '"template_deltas": {', T * 3 + '"enabled": true,', T * 3 + '"env": "TMPLDELTA_OFF",',
             T * 3 + '"source": "Module_Structure_Index.module_meta.<code>.template_type",', T * 3 + f'"_doc": "{doc}"', T * 2 + '},']
    L[i:i] = block
    done.append("meta.template_deltas")
if not any('"template_override":' in s for s in L[:90]):
    i = anchor('"level_override":')
    L[i + 1:i + 1] = [T * 3 + '"template_override": "Edit <subject>.bases.<base>.template_deltas.<TemplateType>.<field> or <subject>.bases.<base>.levels.<level>.template_deltas.<TemplateType>.<field> — overlaid after the level delta for modules whose Module_Structure_Index template_type matches (round 357).",']
    done.append("meta._how_to_edit.template_override")

# ---- (1b) PNR base_rules {} -> module_code
a = anchor('"PNR": {')
if L[a + 2].strip() == '"base_rules": {},':
    L[a + 2:a + 3] = [T * 4 + '"base_rules": {'] + pattern_block(5, "module_code", "full-code", "padded-number", False) + [T * 4 + '},']
    done.append("PNR.base_rules.module_code")

# ---- (1c) SCFUN base_rules: add module_code after acknowledgements
a = anchor('"SCFUN": {')
f = find(lambda s: s.strip() == '"acknowledgements": "yes",', a, a + 20)
if not any('"module_code": {' in s for s in L[a:f + 12]):
    insert_after(f, pattern_block(5, "module_code", "full-code", "padded-number", True))
    done.append("SCFUN.base_rules.module_code")

# ---- (1d) CEDT2 / CEDT3 deltas
if L[set_pattern('"CEDT2": {', "module_code", "absent", "decimal") + 1].endswith('"absent",'):
    done.append("CEDT2.delta.module_code")
if L[set_pattern('"CEDT3": {', "module_code", "full-code", "decimal") + 1].endswith('"full-code",'):
    done.append("CEDT3.delta.module_code")

# ---- (1e) EXPFUN base_rules + template_deltas.Standard
set_pattern('"EXPFUN": {', "module_code", "absent", "decimal"); done.append("EXPFUN.base_rules.module_code")
a = anchor('"EXPFUN": {')
lv = find(lambda s: s.strip() == '"levels": {', a, a + 60)
if not any('"template_deltas": {' in s for s in L[a:lv]):
    L[lv:lv] = template_deltas_block(4, "Standard", "full-code", "decimal", True)
    done.append("EXPFUN.template_deltas.Standard.module_code")

# ---- (1f) OSSC base_rules.module_code.lesson
set_pattern('"OSSC": {', "module_code", "full-code", "padded-number"); done.append("OSSC.base_rules.module_code.lesson")

# ---- (1g) CEDK5 delta: add module_code after page_model
a = anchor('"CEDK5": {')
pm = find(lambda s: s.strip() == '"page_model": "multi-file"', a, a + 12)
if not any('"module_code": {' in s for s in L[a:pm + 6]):
    L[pm] = L[pm] + ","
    insert_after(pm, pattern_block(7, "module_code", "absent", "decimal", False))
    done.append("CEDK5.delta.module_code")

# ---- (1h) CEDO1 + BLL1: template_deltas.Inquiry before "delta"
for tier, lesson in (('"CEDO1": {', "decimal"), ('"BLL1": {', "padded-number")):
    a = anchor(tier)
    dl = find(lambda s: s.strip() == '"delta": {', a, a + 80)
    if not any('"template_deltas": {' in s for s in L[a:dl]):
        L[dl:dl] = template_deltas_block(6, "Inquiry", "absent", lesson, True)
        done.append(f"{tier.split(chr(34))[1]}.template_deltas.Inquiry.module_code")

new = "\n".join(L)
# validation: duplicate keys, tabs-only indentation, parse
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

# ---- (2) ModuleResolver.js
src = open(MR, encoding="utf-8", newline="").read()
assert "\r\n" not in src
MARK = "// TEMPLATE DELTAS (ROUND 357"
if MARK not in src:
    anchor_js = "\t\t\t// EVIDENCE FLOOR (rule 2 above)."
    assert src.count(anchor_js) == 1, src.count(anchor_js)
    block = "\n".join([
        "\t\t\t// TEMPLATE DELTAS (ROUND 357 — the autonomous loop's session-19 Round 1, the diff",
        "\t\t\t// miner's first chrome class: the #module-code chip's presence). A registry level can",
        "\t\t\t// hold modules of TWO template families — the BLL1 level is seven INQUIRY parents",
        "\t\t\t// (BLL110 … BLL170, no chip in 6 of their 7 golds) plus 56 STANDARD children (a chip",
        "\t\t\t// on every page) — and one level delta cannot say both. `template_deltas` is a fifth,",
        "\t\t\t// optional tier at a base or a level: {\"<template_type>\": {field: value}}, overlaid",
        "\t\t\t// AFTER the level delta when the module's template type is known from",
        "\t\t\t// Module_Structure_Index.module_meta (the same index the evidence floor reads). A",
        "\t\t\t// module the index does not know gets no template delta — the level's value stands,",
        "\t\t\t// exactly as before this round. Pattern fields resolve as whole objects; unknown",
        "\t\t\t// literals are skipped (#overlayRules). Data flag: StyleRegistry._meta.template_deltas",
        "\t\t\t// .enabled. Env toggle: TMPLDELTA_OFF (the level's value stands for every module).",
        "\t\t\tconst td = REG._meta?.template_deltas;",
        "\t\t\tconst tdOn = td && td.enabled !== false",
        "\t\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env.TMPLDELTA_OFF);",
        "\t\t\tif (tdOn) {",
        "\t\t\t\tconst tt = DataService.Data.ModuleStructureIndex?.module_meta?.[code]?.template_type;",
        "\t\t\t\tif (tt) {",
        "\t\t\t\t\tlet applied = 0;",
        "\t\t\t\t\tfor (const tier of [base.template_deltas?.[tt], level?.template_deltas?.[tt]]) {",
        "\t\t\t\t\t\tif (!tier) continue;",
        "\t\t\t\t\t\tskippedUnknown += this.#overlayRules(rules, tier, ufOn ? uf : null);",
        "\t\t\t\t\t\tapplied++;",
        "\t\t\t\t\t}",
        "\t\t\t\t\tif (applied) path.push(`template ${tt}`);",
        "\t\t\t\t}",
        "\t\t\t}",
        "",
    ])
    src = src.replace(anchor_js, block + anchor_js)
    open(MR, "w", encoding="utf-8", newline="").write(src)
    print("ModuleResolver.js: template_deltas overlay spliced")
else:
    print("ModuleResolver.js: already spliced")
r = subprocess.run(["node", "--check", MR], capture_output=True, text=True)
print("node --check:", "OK" if r.returncode == 0 else r.stderr[:400])
