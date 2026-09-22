#!/usr/bin/env python3
"""Session 36 Round 1 PICK measurement — THE [Lesson Overview] MARKER'S OWN TRAILING TEXT, and the alert box that follows it.
Over every parsed Writers Template: find each `[Lesson Overview]` marker (red span) and look at (a) the black text that
follows it ON THE SAME LINE (the marker's blackAfter — the engine skips the marker item at render, so this text is lost),
and (b) whether the very next tagged line before `[Lesson content]` / the first heading is an `[Alert box]`.
For each case find where the gold put that text (menu region / body / absent) and where Claude put it (menu / body / absent),
by fuzzy-normalised prefix match against the paired page. Report per template family and per subject prefix.
Run under WSL: python3 _s36_r1_lomarker.py
"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
GOLD = ROOT + "/01-Finalized_Modules_"; CL = ROOT + "/01-Claude_Modules_"
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
RED = re.compile(r'\U0001f534\[RED TEXT\](.*?)\[/RED TEXT\]\U0001f534', re.S)
def strip_md(s): return re.sub(r'\*\*|__|\*', '', s)
def split_gold(g):
    for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
        i = g.find(mark)
        if i > 0: return g[:i], g[i:]
    return g, ""
def where(text, page_html, is_gold):
    """menu / body / absent for a text (normalised prefix of 40 chars)"""
    t = norm(text)[:40]
    if len(t) < 12: return "short"
    if is_gold: head, body = split_gold(page_html)
    else:
        i = page_html.find('<div id="body">'); head, body = (page_html[:i], page_html[i:]) if i > 0 else ("", page_html)
    hn = norm(head); bn = norm(body)
    if t in hn: return "menu"
    if t in bn: return "body"
    return "absent"
def find_pages(code):
    gdir = (glob.glob(GOLD + "/*/" + code + "/") or [None])[0]
    cdir = (glob.glob(CL + "/*/" + code + "/") or [None])[0]
    return gdir, cdir
def lesson_pages(gdir, cdir, n):
    """the gold page CODE_n.0.html and Claude CODE_n_0.html (or single-file)"""
    g = glob.glob(gdir + "*_%d.0.html" % n) if gdir else []
    c = glob.glob(cdir + "*_%d_0.html" % n) if cdir else []
    return (g[0] if g else None), (c[0] if c else None)
stats = collections.Counter(); byfam = collections.defaultdict(collections.Counter); bypre = collections.defaultdict(collections.Counter)
alert_stats = collections.Counter(); alert_byfam = collections.defaultdict(collections.Counter); alert_bypre = collections.defaultdict(collections.Counter)
examples = collections.defaultdict(list)
mods_with = set(); mods_alert = set()
for wt in sorted(glob.glob(GOLD + "/*/*/*Writers*parsed.txt")):
    fam = wt.split("/")[-3]; code = wt.split("/")[-2]; pre = re.match(r'[A-Z]+', code).group(0) if re.match(r'[A-Z]+', code) else code
    gdir, cdir = find_pages(code)
    if not cdir: continue
    txt = open(wt, encoding="utf-8", errors="replace").read()
    lines = txt.splitlines()
    lesson_n = 0
    for k, line in enumerate(lines):
        # count lesson boundaries: [LESSON N] / [Lesson N] / bare [LESSON]
        m = re.search(r'\[\s*lesson\s*(\d+)?\s*\]', line, re.I)
        if m and not re.search(r'lesson\s+(overview|content|title)', line, re.I):
            lesson_n = int(m.group(1)) if m.group(1) else lesson_n + 1
        lo = re.search(r'\[\s*lesson\s+overview\s*\]', line, re.I)
        if not lo: continue
        # text after the LAST red span on this line
        reds = list(RED.finditer(line))
        after = line[reds[-1].end():].strip() if reds else line[lo.end():].strip()
        after = strip_md(after)
        gp, cp = lesson_pages(gdir, cdir, lesson_n)
        gh = open(gp, encoding="utf-8", errors="replace").read() if gp else ""
        ch = open(cp, encoding="utf-8", errors="replace").read() if cp else ""
        if len(norm(after)) >= 12:
            gw = where(after, gh, True) if gh else "nopage"; cw = where(after, ch, False) if ch else "nopage"
            key = "gold=%s claude=%s" % (gw, cw)
            stats[key] += 1; byfam[fam][key] += 1; bypre[pre][key] += 1; mods_with.add(code)
            if len(examples[key]) < 6: examples[key].append("%s L%d: %s" % (code, lesson_n, after[:70]))
        # (b) the next tagged line after the marker, within 6 lines, before [Lesson content] / a heading
        for j in range(k + 1, min(k + 8, len(lines))):
            l2 = lines[j].strip()
            if not l2: continue
            if re.search(r'\[\s*lesson\s+content\s*\]|\[\s*h[1-5]\s*\]|\[\s*title bar', l2, re.I): break
            am = re.search(r'\[\s*alert(?:\s*box)?[^\]]*\]', l2, re.I)
            if am:
                reds2 = list(RED.finditer(l2))
                atext = strip_md(l2[reds2[-1].end():].strip() if reds2 else l2[am.end():].strip())
                if len(norm(atext)) < 12:
                    # the alert text may be on the following line
                    atext = strip_md(lines[j + 1].strip()) if j + 1 < len(lines) else ""
                gw = where(atext, gh, True) if gh else "nopage"; cw = where(atext, ch, False) if ch else "nopage"
                key = "gold=%s claude=%s" % (gw, cw)
                alert_stats[key] += 1; alert_byfam[fam][key] += 1; alert_bypre[pre][key] += 1; mods_alert.add(code)
                if len(examples["ALERT " + key]) < 6: examples["ALERT " + key].append("%s L%d: %s" % (code, lesson_n, atext[:70]))
                break
            if RED.search(l2) and not re.search(r'\[\s*(body|list|sub head)', l2, re.I): break   # another structural tag first
print("(a) [Lesson Overview] markers WITH trailing text on the marker line: %d (modules %d)" % (sum(stats.values()), len(mods_with)))
for k, v in stats.most_common(): print("   %-34s %4d" % (k, v))
print("   by template family:")
for fam, c in sorted(byfam.items()): print("      %-14s %s" % (fam, dict(c.most_common())))
print("   by prefix (top 25):")
for pre, c in sorted(bypre.items(), key=lambda kv: -sum(kv[1].values()))[:25]: print("      %-8s %s" % (pre, dict(c.most_common())))
print("\n(b) an [Alert box] as the first tagged line after the marker (before [Lesson content] / a heading): %d (modules %d)" % (sum(alert_stats.values()), len(mods_alert)))
for k, v in alert_stats.most_common(): print("   %-34s %4d" % (k, v))
print("   by template family:")
for fam, c in sorted(alert_byfam.items()): print("      %-14s %s" % (fam, dict(c.most_common())))
print("   by prefix (top 25):")
for pre, c in sorted(alert_bypre.items(), key=lambda kv: -sum(kv[1].values()))[:25]: print("      %-8s %s" % (pre, dict(c.most_common())))
print("\nexamples:")
for k, v in sorted(examples.items()):
    print("  " + k)
    for e in v: print("     " + e)
