"""ROUND 318 splice (loop Round 5) — KB constraint 83: no loading="lazy" on an image inside a moving-or-draggable interactive.
Anchored, unique-match edits in bytes mode (LF files, tabs preserved). Idempotent (prefix test)."""
ROOT = r"C:/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/"
HF = ROOT + "app/js/HtmlFormatter.js"
ET = ROOT + "data/Emit_Templates.json"

def edit(path, pairs):
    b = open(path, "rb").read()
    for old, new in pairs:
        o = old.encode("utf-8"); n = new.encode("utf-8")
        ins = n[:-len(o)] if n.endswith(o) else (n[len(o):] if n.startswith(o) else n)
        if b.count(ins) == 1 and (n.endswith(o) or n.startswith(o) or b.count(o) == 0):
            print("already applied:", path.split("/")[-1], old[:40].strip()); continue
        cnt = b.count(o)
        assert cnt == 1, f"{path}: anchor count {cnt} != 1 for anchor starting {old[:60]!r}"
        b = b.replace(o, n)
    open(path, "wb").write(b)
    print("edited", path.split("/")[-1], len(pairs), "edit(s)")

# ---------------------------------------------------------------- data block (formatter, before xhtml_voids)
DATA_OLD = '\t\t"xhtml_voids": {\n\t\t\t"enabled": true,\n'
DATA_NEW = ('\t\t"lazy_free_hosts": {\n'
 '\t\t\t"enabled": true,\n'
 '\t\t\t"env": "LAZYHOST_OFF",\n'
 '\t\t\t"attribute": "loading=\\"lazy\\"",\n'
 '\t\t\t"host_classes": [\n'
 '\t\t\t\t"rotateBanner", "bannerContainer", "bannerItem",\n'
 '\t\t\t\t"carousel",\n'
 '\t\t\t\t"dragAndDrop", "drag", "drop", "ddContainer", "ddColumn",\n'
 '\t\t\t\t"clickDrop", "clickDropContent",\n'
 '\t\t\t\t"flipCard", "front", "back", "flipImage",\n'
 '\t\t\t\t"memoryGame", "memCard", "cardHidden",\n'
 '\t\t\t\t"canvasContainer"\n'
 '\t\t\t],\n'
 '\t\t\t"_round318_note": "ROUND 318 (the autonomous loop\'s Round 5, 2026-09-15 \\u2014 KB constraint 83 / CL-0083: NEVER add loading=\\"lazy\\" to an image inside a moving-or-draggable interactive \\u2014 lazy loading defers the image until the browser judges it near the viewport, which breaks any interactive whose images move; the KB names the rotating banner, carousel, drag and drop, click drop (incl. .clickDropContent), flip card, memory game and sketcher, in both image modes, real images and placehold.co placeholders alike; every OTHER image keeps the attribute). Round 240\'s MediaBuilder.FinishImg adds the attribute to every image it builds and cannot know its host, so the rule lives here as a whole-document pass in HtmlFormatter.Indent, run before the line walk: a void-aware tag walk keeps an open-element stack and strips `attribute` from any <img> whose open ancestor carries one of host_classes (the KB\'s own list; the inner names \\u2014 drag, drop, front, back, item-level classes \\u2014 sit inside their outer hosts anyway, and .clickDropContent is the click-drop panel\'s SIBLING, so it is listed in its own right). MEASURED (outputs/_measure_r318_lazyhosts.py, the same walk on every page): Claude 2424 lazy images inside hosts on 228 pages / 146 modules (carousel 1000, flipCard 1114, clickDrop 224, banner 86); the gold AGREES with the KB inside hosts \\u2014 11730 images without the attribute vs 3574 with (76.6%) \\u2014 and is era-mixed outside them, where the r240 forward rule stands. Gate-neutral (`loading` is not a KEEP_ATTR). Env toggle LAZYHOST_OFF reverts to the round-317 form byte-for-byte."\n'
 '\t\t},\n'
 + DATA_OLD)

# ---------------------------------------------------------------- HtmlFormatter (a) the pass, before #voidPass's doc block
HF_A_OLD = ('\t/**\n'
 '\t * ROUND 315 (loop Round 2 \u2014 KB constraint 28): the XHTML void pass, or null\n')
HF_A_NEW = ('\t/**\n'
 '\t * ROUND 318 (loop Round 5 \u2014 KB constraint 83): strips loading="lazy" from every\n'
 '\t * <img> that sits INSIDE a moving-or-draggable interactive (data host_classes:\n'
 '\t * banner, carousel, drag-and-drop, click-drop + its content panel, flip card,\n'
 '\t * memory game, sketcher). A whole-document, void-aware tag walk: an open\n'
 '\t * element pushes (with the host class it carries, if any), a close tag pops\n'
 '\t * to its match, and an <img> met while any stacked ancestor is a host loses\n'
 '\t * the attribute. Images outside a host keep it (the round-240 forward rule).\n'
 '\t * Returns the html unchanged when off (data flag, env LAZYHOST_OFF, no data).\n'
 '\t */\n'
 '\tstatic #lazyFreeHosts(html) {\n'
 '\t\tif (typeof process !== "undefined" && process.env && process.env.LAZYHOST_OFF) return html;\n'
 '\t\tlet cfg;\n'
 '\t\ttry { cfg = DataService.Data.EmitTemplates.formatter?.lazy_free_hosts; } catch (e) { return html; }\n'
 '\t\tif (!cfg || !cfg.enabled || !Array.isArray(cfg.host_classes) || !cfg.host_classes.length) return html;\n'
 '\t\tif (cfg.env && typeof process !== "undefined" && process.env && process.env[cfg.env]) return html;\n'
 '\t\tconst hosts = new Set(cfg.host_classes);\n'
 '\t\tconst attr = cfg.attribute ?? \'loading="lazy"\';\n'
 '\t\tconst tagRe = /<(\\/?)([a-zA-Z][\\w-]*)((?:"[^"]*"|\'[^\']*\'|[^>"\'])*)>/g;\n'
 '\t\tconst stack = [];   // [tagName, isHost]\n'
 '\t\tlet out = "", last = 0, inHost = 0, m;\n'
 '\t\twhile ((m = tagRe.exec(html)) !== null) {\n'
 '\t\t\tconst closing = m[1] === "/", name = m[2].toLowerCase(), attrs = m[3];\n'
 '\t\t\tif (closing) {\n'
 '\t\t\t\tfor (let i = stack.length - 1; i >= 0; i--) {\n'
 '\t\t\t\t\tif (stack[i][0] === name) {\n'
 '\t\t\t\t\t\tfor (let k = stack.length - 1; k >= i; k--) if (stack[k][1]) inHost--;\n'
 '\t\t\t\t\t\tstack.length = i; break;\n'
 '\t\t\t\t\t}\n'
 '\t\t\t\t}\n'
 '\t\t\t\tcontinue;\n'
 '\t\t\t}\n'
 '\t\t\tif (name === "img") {\n'
 '\t\t\t\tif (inHost > 0 && attrs.includes(attr)) {\n'
 '\t\t\t\t\tout += html.slice(last, m.index) + m[0].replace(new RegExp("\\\\s*" + attr.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&")), "");\n'
 '\t\t\t\t\tlast = m.index + m[0].length;\n'
 '\t\t\t\t}\n'
 '\t\t\t\tcontinue;\n'
 '\t\t\t}\n'
 '\t\t\tif (HtmlFormatter.#VOID.has(name) || /\\/\\s*$/.test(attrs)) continue;   // a void never opens\n'
 '\t\t\tconst cm = /\\bclass="([^"]*)"/.exec(attrs);\n'
 '\t\t\tconst isHost = !!cm && cm[1].split(/\\s+/).some((c) => hosts.has(c));\n'
 '\t\t\tstack.push([name, isHost]);\n'
 '\t\t\tif (isHost) inHost++;\n'
 '\t\t}\n'
 '\t\treturn last ? out + html.slice(last) : html;\n'
 '\t};\n'
 '\n'
 + HF_A_OLD)

# ---------------------------------------------------------------- HtmlFormatter (b) the hook, before the void pass
HF_B_OLD = ('\t\t// ROUND 315 (KB constraint 28): lowercase doctype + XHTML self-closing voids,\n'
 '\t\t// applied per line after the block breaking so every void tag is seen once.\n'
 '\t\tconst vp = HtmlFormatter.#voidPass();\n')
HF_B_NEW = ('\t\t// ROUND 318 (KB constraint 83): no loading="lazy" inside a moving interactive \u2014\n'
 '\t\t// a whole-document walk, before the per-line passes (see #lazyFreeHosts).\n'
 '\t\thtml = HtmlFormatter.#lazyFreeHosts(html);\n'
 '\n'
 + HF_B_OLD)

edit(ET, [(DATA_OLD, DATA_NEW)])
edit(HF, [(HF_A_OLD, HF_A_NEW), (HF_B_OLD, HF_B_NEW)])
print("done")
