"""SESSION 40 ROUND 8 (24 Sept 2026) — the §3 MEASURE step: the Bilingual template's widget bundles.

BilingualBuilder.bilingualSection renders a consumed widget bundle as ONE `cv2-interactive bilingual-unbuilt`
box holding `contentTable(firstMember.block)` — the bundle's FIRST member only. When that member is the
writer's `[Activity: Embedded] …` tag line (not a table) the box is an EMPTY `<table>`; either way every later
member (the bilingual heading / instruction table, the data table) renders nothing on the page.

This probe reads every Bilingual module's `_interactives.txt` worklist, takes each bundle's BILINGUAL ROW cells
(a cell carrying an [H2]/[H3]/[H4]/[Body] tag), and checks each cell's text against the Claude page the entry
names and against the module's gold pages (HTML comments stripped — a commented-out gold block is not shipped).

Run under WSL:  python3 _s40_r8_bilwidget.py > _s40_r8_bilwidget.log
"""
import html as H, os, re, collections

ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
CL = f"{ROOT}/01-Claude_Modules_/Bilingual"
GO = f"{ROOT}/01-Finalized_Modules_/Bilingual"
TAG = re.compile(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴")
CELLTAG = re.compile(r"\[(H[2-5]|Body|body|BODY)\]")


def norm(s):
    s = H.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("**", "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[^\w' ]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def page_text(path, strip_comments=False):
    s = open(path, encoding="utf8", errors="ignore").read()
    if strip_comments:
        s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    m = re.search(r"<body[^>]*>(.*)</body>", s, re.S)
    return norm(m.group(1) if m else s)


def entries(wl):
    txt = open(wl, encoding="utf8", errors="ignore").read()
    for blk in re.split(r"\nINTERACTIVE \d+ of \d+\n", txt)[1:]:
        f = re.search(r"^File: (\S+)", blk, re.M)
        t = re.search(r"^Type: (.*)$", blk, re.M)
        body = blk.split("\nContent:\n", 1)[1] if "\nContent:\n" in blk else ""
        first = next((ln for ln in body.split("\n") if ln.strip()), "")
        cells = []
        for ln in body.split("\n"):
            if not ln.startswith("│"):
                continue
            for c in ln[1:].split("║"):
                tags = " ".join(TAG.findall(c))
                if not CELLTAG.search(tags):
                    continue
                txt_c = norm(TAG.sub(" ", c))
                if len(txt_c) >= 12:
                    cells.append(txt_c)
        yield (f.group(1) if f else None), (t.group(1).strip() if t else "?"), first, cells


def main():
    tot = collections.Counter()
    per_mod = {}
    first_kind = collections.Counter()
    for mod in sorted(os.listdir(CL)):
        wl = f"{CL}/{mod}/{mod}_interactives.txt"
        if not os.path.isfile(wl):
            continue
        gdir = f"{GO}/{mod}"
        gold = " || ".join(page_text(f"{gdir}/{g}", True) for g in sorted(os.listdir(gdir)) if g.endswith(".html")) if os.path.isdir(gdir) else ""
        cache = {}
        c = collections.Counter()
        for page, typ, first, cells in entries(wl):
            c["bundles"] += 1
            first_kind["table" if first.startswith("┌") else "tag/para"] += 1
            if not page or not os.path.isfile(f"{CL}/{mod}/{page}"):
                continue
            if page not in cache:
                cache[page] = page_text(f"{CL}/{mod}/{page}")
            ct = cache[page]
            if cells:
                c["bundles_with_bilingual_rows"] += 1
            for cell in cells:
                inC, inG = cell in ct, bool(gold) and cell in gold
                c["cells"] += 1
                c["claude"] += inC
                c["gold"] += inG
                c["gold_not_claude"] += (inG and not inC)
        per_mod[mod] = c
        tot.update(c)
    print("first member of a bundle:", dict(first_kind))
    print("TOTAL", dict(tot))
    for mod, c in per_mod.items():
        print(f"  {mod}: bundles {c['bundles']} with-rows {c['bundles_with_bilingual_rows']} cells {c['cells']} "
              f"claude {c['claude']} gold {c['gold']} gold-not-claude {c['gold_not_claude']}")


if __name__ == "__main__":
    main()
