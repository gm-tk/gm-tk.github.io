#!/usr/bin/env python3
"""Session 26 Round 3 (engine r389) — the built flipCard group closes its column.
Data: `body_region.row_breaks.after_built_widgets` (rules with class_match / templates / exclude_subjects; env FLIPBREAK_OFF).
Engine: `ContentConverter.#breaksAfterBuilt(html, run)` + the INLINE widget site breaks the row after a matching built widget.
LF preserved. Idempotent. Run under WSL: python3 _s26_r389_splice.py"""
import io, sys
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2"

# ---- data ----
P = ROOT + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"after_built_widgets"' not in s:
    old = ('\t\t\t"after_note": "Content following a closed callout/activity/widget always starts a fresh row (verified OSAI201_0.0, OSAH401_1.0)."\n'
           '\t\t},\n')
    assert s.count(old) == 1, s.count(old)
    new = ('\t\t\t"after_note": "Content following a closed callout/activity/widget always starts a fresh row (verified OSAI201_0.0, OSAH401_1.0).",\n'
           '\t\t\t"after_built_widgets": {\n'
           '\t\t\t\t"enabled": true,\n'
           '\t\t\t\t"env": "FLIPBREAK_OFF",\n'
           '\t\t\t\t"rules": [\n'
           '\t\t\t\t\t{\n'
           '\t\t\t\t\t\t"class_match": "\\\\bflipCardsContainer\\\\b",\n'
           '\t\t\t\t\t\t"templates": [\n'
           '\t\t\t\t\t\t\t"Standard"\n'
           '\t\t\t\t\t\t],\n'
           '\t\t\t\t\t\t"exclude_subjects": []\n'
           '\t\t\t\t\t}\n'
           '\t\t\t\t],\n'
           '\t\t\t\t"_doc": "ROUND 389 (the autonomous loop\'s session 26 Round 3 — the paired row-break census cut by the built widget\'s own signature, outputs/_s26_r389_divpair.py + _s26_r389_flipgold.py). The r51 flow_blocks rule keeps every built widget IN the section row and lets the next prose flow on after it; the gold does that for every built widget but ONE — after a built flipCard group (`div.row.flipCardsContainer`) the gold CLOSES the column and opens a new row for the prose (paired 23 / 5 = 0.82 on 26 pages / 20 modules; the gold-side census: the group is its column\'s LAST or only child 0.75 of 187 — English 0.87, Mathematics 0.93, ConnectED 0.82, Online Safety 0.82). Every other built widget (the reader\'s WIDGET kind) is a tie at 0.55 and keeps r51. A rule = class_match (a regex on the built html\'s open-tag class), templates (module_meta.template_type), exclude_subjects (module_meta.subject), an optional per-rule env. Fires only at the INLINE widget site (a top-level widget — inside an activity box the group never closes the box). The break BEFORE the group is NOT taken (the gold is a tie: FIRST-or-only 0.45), nor the col-md-12 width (0.31). OFF = the r388 output."\n'
           '\t\t\t}\n'
           '\t\t},\n')
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: after_built_widgets added")
else:
    print("data: already")

# ---- engine ----
P2 = ROOT + "/app/js/ContentConverter.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "#breaksAfterBuilt" not in s:
    # (1) the helper, placed right before #flowsAfter
    old_h = "\tstatic #flowsAfter(tag, run, boxOpen = \"\") {\n"
    assert s.count(old_h) == 1
    helper = (
        "\t// ROUND 389 (the autonomous loop's session 26 Round 3): the built flipCard group closes its column — the r51\n"
        "\t// flow_blocks rule keeps every built widget in the section row, but after a built flipCard group the gold\n"
        "\t// opens a NEW row for the prose that follows (paired 0.82; the group is its column's last child 0.75\n"
        "\t// gold-wide). Data body_region.row_breaks.after_built_widgets — a rule matches the built html's open-tag\n"
        "\t// class, the module's template_type and subject. Returns true when the inline widget site should breakRow().\n"
        "\tstatic #breaksAfterBuilt(html, run) {\n"
        "\t\tconst cfg = DataService.Data.EmitTemplates?.body_region?.row_breaks?.after_built_widgets;\n"
        "\t\tif (!cfg || cfg.enabled === false) return false;\n"
        "\t\tif (typeof process !== \"undefined\" && process.env && process.env[cfg.env ?? \"FLIPBREAK_OFF\"]) return false;\n"
        "\t\tconst m = String(html || \"\").match(/^\\s*<div class=\"([^\"]*)\"/);\n"
        "\t\tif (!m) return false;\n"
        "\t\tconst meta = DataService.Data.ModuleStructureIndex?.module_meta?.[String(run?.moduleCode || \"\")];\n"
        "\t\tif (!meta) return false;\n"
        "\t\tfor (const rule of (Array.isArray(cfg.rules) ? cfg.rules : [])) {\n"
        "\t\t\tif (!rule.class_match || !new RegExp(rule.class_match).test(m[1])) continue;\n"
        "\t\t\tif ((rule.templates ?? []).length && !(rule.templates ?? []).some((t) => String(t) === String(meta.template_type ?? \"\"))) continue;\n"
        "\t\t\tif ((rule.exclude_subjects ?? []).some((sub) => String(sub) === String(meta.subject ?? \"\"))) continue;\n"
        "\t\t\tif (rule.env && typeof process !== \"undefined\" && process.env && process.env[rule.env]) continue;\n"
        "\t\t\treturn true;\n"
        "\t\t}\n"
        "\t\treturn false;\n"
        "\t}\n\n"
    )
    s = s.replace(old_h, helper + old_h, 1)
    # (2) the INLINE site (the one followed by the ROUND 232 mtkTailI line; the owned site's twin is followed by a different line)
    T = "\t" * 6
    old_pre = T + "const mtkShellI = this.#mtkQuizShellBundle(bundle, it);   // ROUND 322 — see the owned site above (\"lead\" cannot occur inline)\n"
    assert s.count(old_pre) == 1, s.count(old_pre)
    s = s.replace(old_pre, T + "let _r389Break = false;   // ROUND 389 — the built flipCard group closes its column (see #breaksAfterBuilt)\n" + old_pre, 1)
    old_a = (T + "else if (!this.#mtkQuizBundleThin(bundle)) emit(this.#interactivePlaceholder(bundle, run));\n"
             + T + "const mtkTailI = this.#mtkQuizBundleTail(bundle, run, it);")
    assert s.count(old_a) == 1, s.count(old_a)
    new_a = (T + "else if (!this.#mtkQuizBundleThin(bundle)) { const _r389Html = this.#interactivePlaceholder(bundle, run); emit(_r389Html); _r389Break = this.#breaksAfterBuilt(_r389Html, run); }   // ROUND 389\n"
             + T + "const mtkTailI = this.#mtkQuizBundleTail(bundle, run, it);")
    s = s.replace(old_a, new_a, 1)
    old_b = T + "if (!rowCfg.flow_blocks && !stack.length && rowCfg.after.includes(\"interactive_placeholder\")) breakRow();\n"
    assert s.count(old_b) == 1, s.count(old_b)
    new_b = old_b + T + "if (_r389Break && !stack.length) breakRow();   // ROUND 389 — the built flipCard group closes its column\n"
    s = s.replace(old_b, new_b, 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: #breaksAfterBuilt + the inline site")
else:
    print("engine: already")
