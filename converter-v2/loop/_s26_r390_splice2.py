#!/usr/bin/env python3
"""r390 splice 2 — gate the promoted-closer family on the own-row call only (the probe's OFF leg showed EXIP901 / SCFUN01
moving: the r170 / r239 promotions made `end alert` count for `side alert` and `end shape n` for `interactive` everywhere).
`#explicitCloseAhead(bodyItems, i, canonTag, opts)` — opts.stopAtActivity / opts.promotedClosers, both false by default."""
import io
P2 = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/app/js/ContentConverter.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "opts.promotedClosers" not in s:
    old = "\tstatic #explicitCloseAhead(bodyItems, i, canonTag, stopAtActivity = false) {\n"
    assert s.count(old) == 1
    s = s.replace(old, "\tstatic #explicitCloseAhead(bodyItems, i, canonTag, opts = {}) {\n\t\tconst stopAtActivity = !!opts.stopAtActivity;   // ROUND 390: only the own-row (supervisor) span asks for these two\n", 1)
    old = "\t\tfor (const r of (DataService.Data.TagLexicon?._meta?.tag_promote?.rules ?? [])) {\n\t\t\tif (r && r.to === canonTag && r.from) family.add(`end ${r.from}`);\n\t\t}\n"
    assert s.count(old) == 1
    s = s.replace(old, "\t\tif (opts.promotedClosers) for (const r of (DataService.Data.TagLexicon?._meta?.tag_promote?.rules ?? [])) {\n\t\t\tif (r && r.to === canonTag && r.from) family.add(`end ${r.from}`);\n\t\t}\n", 1)
    old = "\t\t\t\t\t\t\t&& this.#explicitCloseAhead(bodyItems, i, primary.tag, _ecs.stop_at_activity !== false)) {\n"
    assert s.count(old) == 1
    s = s.replace(old, "\t\t\t\t\t\t\t&& this.#explicitCloseAhead(bodyItems, i, primary.tag, { stopAtActivity: _ecs.stop_at_activity !== false, promotedClosers: true })) {\n", 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: opts-gated")
else:
    print("already")
