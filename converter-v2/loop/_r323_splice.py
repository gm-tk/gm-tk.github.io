#!/usr/bin/env python3
"""ROUND 323 — the trailing full stop on a button label (KB row 55's text defect). Anchored, idempotent
engine + data edits (env R323_ROOT overrides the target tree for the reproducibility test).

  (1) data  Emit_Templates.buttons.label_trailing_stop {enabled, env BTNSTOP_OFF, strip_pattern, keep_pattern}
  (2) engine ContentConverter.#element generic [button] site: label = this.#buttonLabelTrim(label, tpl) before the fill
  (3) engine static #buttonLabelTrim helper
"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("R323_ROOT") or os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
CC = os.path.join(ROOT, "app", "js", "ContentConverter.js")
ET = os.path.join(ROOT, "data", "Emit_Templates.json")
def rd(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
def step(src, key, old, new, label):
    if key in src: print(f"  = {label}: already applied"); return src
    n = src.count(old); assert n == 1, f"{label}: anchor count {n} != 1"
    print(f"  + {label}: applied"); return src.replace(old, new, 1)

# (1) data — after buttons.button_linked
et = rd(ET)
D_OLD = '\t\t"button_linked": {\n\t\t\t"form": "<a href=\\"{url}\\" target=\\"_blank\\"><div class=\\"button\\">{label}</div></a>"\n\t\t},\n'
D_NEW = D_OLD + ('\t\t"label_trailing_stop": {\n'
    '\t\t\t"_doc": "ROUND 323 (the autonomous loop\'s session-3 Round 10, 2026-09-15 — KB row 55\'s recorded text defect). A writer types the button label as a sentence — \'[button] Learning journal.\', \'[button] Upload to dropbox.\', \'[button] Check answers.\' — and the full stop rode into the label. The KB\'s canonical labels (constraint 55 \'Go to dropbox\' / \'Go to portfolio\', 14.11 \'Upload to Dropbox\', constraint 75 \'Go to website\', CL-0038 \'Go to quiz\') carry no terminal punctuation, and the gold agrees: 9 of 5,553 gold buttons end in a full stop (sentence-like labels) against 441 of 3,052 Claude buttons on 221 pages / 90 modules (outputs/_measure_r323_buttonstop.py). ONE trailing full stop is stripped from the label at the generic [button]-family emit (the only seam that fills a writer\'s label into a button form); an ellipsis and an abbreviation (e.g. / i.e. / etc.) keep theirs; \'?\' \'!\' \':\' are never touched (the gold keeps them: 64 / 17 / 10). Env BTNSTOP_OFF reverts byte-for-byte.",\n'
    '\t\t\t"enabled": true,\n'
    '\t\t\t"env": "BTNSTOP_OFF",\n'
    '\t\t\t"strip_pattern": "\\\\.$",\n'
    '\t\t\t"keep_pattern": "(\\\\.\\\\.|\\\\b(?:e\\\\.g|i\\\\.e|etc|vs|approx|no|pp?|cf))\\\\.$"\n'
    '\t\t},\n')
et = step(et, '"label_trailing_stop"', D_OLD, D_NEW, "(1) data buttons.label_trailing_stop")
wr(ET, et)

cc = rd(CC)
# (2) the generic site: trim just before the fill
E2_OLD = ('\t\t\t\tif (dlLabel) { label = dlLabel; form = dlCfg.form; }\n'
          '\t\t\t}\n'
          '\t\t\tout.push(Utils.FillTemplate(form, {\n'
          '\t\t\t\tlabel: Utils.EscapeHtml(label), url: Utils.EscapeHtml(url),\n')
E2_NEW = ('\t\t\t\tif (dlLabel) { label = dlLabel; form = dlCfg.form; }\n'
          '\t\t\t}\n'
          '\t\t\t// ROUND 323 (KB row 55): the writer\'s sentence full stop is not part of the label\n'
          '\t\t\tlabel = this.#buttonLabelTrim(label, tpl);\n'
          '\t\t\tout.push(Utils.FillTemplate(form, {\n'
          '\t\t\t\tlabel: Utils.EscapeHtml(label), url: Utils.EscapeHtml(url),\n')
cc = step(cc, "label = this.#buttonLabelTrim(label, tpl);", E2_OLD, E2_NEW, "(2) generic button site trim")
# (3) the helper — before #mtkQuizOmitCfg
E3_OLD = '\tstatic #mtkQuizOmitCfg() {\n'
E3_NEW = ('\t/**\n'
          '\t * ROUND 323 (KB row 55\'s text defect) — a button label never ends in a full stop: the\n'
          '\t * writer typed the label as a sentence ("[button] Upload to dropbox.") and the stop rode\n'
          '\t * into the label (441 Claude buttons vs 9 gold). ONE trailing full stop is stripped;\n'
          '\t * an ellipsis or an abbreviation (keep_pattern) keeps it; "?" "!" ":" are never touched.\n'
          '\t * Data buttons.label_trailing_stop; env BTNSTOP_OFF.\n'
          '\t */\n'
          '\tstatic #buttonLabelTrim(label, tpl) {\n'
          '\t\tconst cfg = tpl?.buttons?.label_trailing_stop;\n'
          '\t\tif (!cfg || cfg.enabled === false || !label) return label;\n'
          '\t\tif (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "BTNSTOP_OFF"]) return label;\n'
          '\t\tconst s = String(label).trim();\n'
          '\t\tif (!new RegExp(cfg.strip_pattern ?? "\\\\.$").test(s)) return label;\n'
          '\t\tif (cfg.keep_pattern && new RegExp(cfg.keep_pattern, "i").test(s)) return label;\n'
          '\t\treturn s.replace(new RegExp(cfg.strip_pattern ?? "\\\\.$"), "").trim();\n'
          '\t}\n\n'
          '\tstatic #mtkQuizOmitCfg() {\n')
cc = step(cc, "static #buttonLabelTrim(label, tpl) {", E3_OLD, E3_NEW, "(3) #buttonLabelTrim helper")
wr(CC, cc)
print("done")
