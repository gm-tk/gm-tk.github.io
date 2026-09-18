#!/usr/bin/env python3
"""Session 26 Round 2 (engine r388) — a per-rule env toggle on `callouts.flow_after_tags.rules[]` so the alert rule
reverses ALONE (`ALERTFLOW_OFF`) while `WHFLOW_OFF` still reverses the whole family. Data + engine; LF preserved;
idempotent. Run under WSL: python3 _s26_r388_ruleenv.py"""
import io, sys
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2"
P = ROOT + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"env": "ALERTFLOW_OFF"' not in s:
    old = '\t\t\t\t\t"exclude_subjects": [],\n\t\t\t\t\t"exclude_class_match": "\\\\btop\\\\b",\n'
    new = ('\t\t\t\t\t"env": "ALERTFLOW_OFF",\n'
           '\t\t\t\t\t"exclude_subjects": [],\n'
           '\t\t\t\t\t"exclude_class_match": "\\\\btop\\\\b",\n')
    n = s.count(old)
    if n != 1:
        i = s.find('"exclude_class_match"')
        print("anchor count", n, "context:", repr(s[i - 80:i + 40])); sys.exit(1)
    s = s.replace(old, new, 1)
    old_doc = "exclude_class_match (a regex on the emitted box's open tag, e.g. the `top` modifier)."
    if s.count(old_doc) == 1:
        s = s.replace(old_doc, "exclude_class_match (a regex on the emitted box's open tag, e.g. the `top` modifier), env (an optional per-rule env toggle on top of the family env — the rule reverses alone; r388 `ALERTFLOW_OFF`).", 1)
    else:
        print("(rules_doc anchor not found — doc unchanged)")
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: ALERTFLOW_OFF added to rule 2")
else:
    print("data: already applied")

P2 = ROOT + "/app/js/ContentConverter.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "the rule's own toggle" not in s:
    old = '\t\t\tif (!(rule.tags ?? []).some((t) => String(t) === String(tag))) continue;\n'
    new = old + '\t\t\tif (rule.env && typeof process !== "undefined" && process.env && process.env[rule.env]) continue;   // the rule\'s own toggle (r388)\n'
    assert s.count(old) == 1, s.count(old)
    s = s.replace(old, new, 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: per-rule env check added")
else:
    print("engine: already applied")
