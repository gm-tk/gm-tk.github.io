#!/usr/bin/env python3
"""_measure_r338_extbutton_class.py — ROUND 338 measurement (session 7 Round 1 PICK, the class that survived).

KB 05D "Buttons": an INTERNAL destination renders <a href target=_blank><div class="button">…</div></a>, an
EXTERNAL one <div class="externalButton">. The gold follows it by HOST (measured here): relative paths, "#",
Google Drive / Docs (Te Kura's hosted files), the LMS (desire2learn) and the vimeo player are `button`; every
outside website is `externalButton`. Claude's round-326 anchor ships `button` for every [button]-family tag
regardless of destination.

This probe: every anchored button on every Claude page (pre-acks) whose href is an http(s) URL → host class
(internal / external by the data-style host list below) → Claude's div class → the gold's div class for the SAME
href on the same module (or, failing an href match, the same label). Reports per template / subject family the
share of external-host Claude `button`s the gold ships as `externalButton` — the solidify test — and the class
size in pages / modules. Also the converse (internal-host buttons the gold ships as externalButton) so the
host rule cannot disturb the dropbox / portfolio / quiz / journal buttons.

Usage (from CONVERTER_V2/outputs, WSL):  python3 _measure_r338_extbutton_class.py   → _r338_extbutton_class.json
"""
import os, re, json, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _corpus

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
META = json.load(open(os.path.join(ROOT, "pageforge-site", "converter-v2", "data", "Module_Structure_Index.json"), encoding="utf-8")).get("module_meta", {})

# the INTERNAL host list (Te Kura's own systems and hosted files) — the candidate data list
INTERNAL_HOST_RE = re.compile(r"^(?:[\w-]+\.)*(?:drive\.google\.com|docs\.google\.com|forms\.gle|desire2learn\.com|tekura\.school\.nz|mytekuraschool\.sharepoint\.com|mytekuraschool-my\.sharepoint\.com|player\.vimeo\.com|vimeo\.com)$", re.I)

BTN_RE = re.compile(r'<a\s+href="([^"]*)"[^>]*>\s*<div class="([^"]*)">([\s\S]*?)</div>\s*</a>', re.I)

def unent(s):
    return (s or "").replace("&amp;", "&").replace("&nbsp;", " ").replace("&#257;", "ā").replace("&#275;", "ē").replace("&#299;", "ī").replace("&#333;", "ō").replace("&#363;", "ū")

def norm_href(h):
    h = unent(h).strip().lower()
    h = re.sub(r"^https?://", "", h); h = re.sub(r"^www\.", "", h); h = re.sub(r"#.*$", "", h); h = re.sub(r"/+$", "", h)
    return h

def norm_text(s):
    s = re.sub(r"<[^>]+>", " ", unent(s)).lower()
    return re.sub(r"[^\w]+", " ", s).strip()

def host_of(href):
    h = unent(href).strip()
    if not re.match(r"^https?://", h, re.I): return None
    return re.sub(r"^https?://", "", h, flags=re.I).split("/")[0].split("?")[0].lower()

def host_class(href):
    h = host_of(href)
    if h is None: return "non-http"
    return "internal" if INTERNAL_HOST_RE.match(h) else "external"

def body_of(html):
    return re.split(r'<div[^>]*class="[^"]*acks[^"]*"', html, maxsplit=1, flags=re.I)[0]

def buttons_in(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    out = []
    for m in BTN_RE.finditer(body_of(html)):
        cls = m.group(2)
        if not re.search(r"\b(button|externalButton)\b", cls): continue
        out.append({"href": unent(m.group(1)).strip(), "cls": cls, "label": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(3))).strip()})
    return out

def main():
    rows = []
    gold_index = {}   # code -> list of gold buttons (all pages)
    for code in _corpus.mods(CLAUDE):
        cdir = _corpus.mdir(CLAUDE, code)
        if not os.path.isdir(cdir): continue
        gdir = _corpus.mdir(GOLD, code)
        gbtns = []
        if os.path.isdir(gdir):
            for f in sorted(os.listdir(gdir)):
                if f.lower().endswith(".html"):
                    for b in buttons_in(os.path.join(gdir, f)): b["file"] = f; gbtns.append(b)
        gold_index[code] = gbtns
        meta = META.get(code, {})
        for f in sorted(os.listdir(cdir)):
            if not f.lower().endswith(".html"): continue
            for b in buttons_in(os.path.join(cdir, f)):
                hc = host_class(b["href"])
                if hc == "non-http": continue
                hN = norm_href(b["href"]); lN = norm_text(b["label"])
                g = None
                for gb in gbtns:
                    if hN and norm_href(gb["href"]) == hN: g = gb; break
                if g is None and lN:
                    for gb in gbtns:
                        if norm_text(gb["label"]) == lN and host_class(gb["href"]) == hc: g = gb; break
                gform = None if g is None else ("externalButton" if re.search(r"\bexternalButton\b", g["cls"]) else "button")
                rows.append({"code": code, "file": f, "template": meta.get("template_type", "?"), "subject": meta.get("subject", "?"),
                             "prefix": meta.get("prefix", re.sub(r"\d.*$", "", code)), "host": host_of(b["href"]), "host_class": hc,
                             "claude_cls": "externalButton" if re.search(r"\bexternalButton\b", b["cls"]) else "button", "claude_full_cls": b["cls"],
                             "label": b["label"][:80], "href": b["href"][:160], "gold": gform, "gold_file": None if g is None else g["file"], "gold_label": None if g is None else g["label"][:80]})
    json.dump({"rows": rows}, open(os.path.join(HERE, "_r338_extbutton_class.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def tally(label, rs):
        n = len(rs); pages = len({r["code"] + "/" + r["file"] for r in rs}); mods = len({r["code"] for r in rs})
        c = collections.Counter(r["gold"] for r in rs)
        found = c["externalButton"] + c["button"]
        print(f"{label:52s} n={n:4d} pages={pages:4d} mods={mods:3d} | gold externalButton {c['externalButton']:4d} / button {c['button']:4d} / not found {c[None]:4d} | ext share of found {(c['externalButton']/found) if found else 0:.3f}")

    print("== Claude anchored buttons with an http(s) href, by host class × Claude's class ==")
    for hc in ("external", "internal"):
        for cc in ("button", "externalButton"):
            tally(f"  host {hc:8s} · Claude {cc}", [r for r in rows if r["host_class"] == hc and r["claude_cls"] == cc])
    print("\n== THE CLASS: external-host buttons Claude ships as `button` — by template ==")
    cls = [r for r in rows if r["host_class"] == "external" and r["claude_cls"] == "button"]
    for t in ("Standard", "Inquiry", "Fundamentals", "Bilingual", "?"):
        rs = [r for r in cls if r["template"] == t]
        if rs: tally(f"  {t}", rs)
    print("\n== by subject family (≥ 5) ==")
    bys = collections.defaultdict(list)
    for r in cls: bys[r["subject"]].append(r)
    for s, rs in sorted(bys.items(), key=lambda x: -len(x[1])):
        if len(rs) >= 5: tally(f"  {s}", rs)
    print("\n== by external host (≥ 4) ==")
    byh = collections.defaultdict(list)
    for r in cls: byh[r["host"]].append(r)
    for h, rs in sorted(byh.items(), key=lambda x: -len(x[1])):
        if len(rs) >= 4: tally(f"  {h}", rs)
    print("\n== the converse: INTERNAL-host buttons — by host (the rule must leave these alone) ==")
    byh = collections.defaultdict(list)
    for r in rows:
        if r["host_class"] == "internal": byh[r["host"]].append(r)
    for h, rs in sorted(byh.items(), key=lambda x: -len(x[1])):
        tally(f"  {h}", rs)
    print("\n== Claude labels on the class (top 12) ==")
    for l, n in collections.Counter(r["label"] for r in cls).most_common(12): print(f"  {n:4d}  {l}")
    print("\n== gold label vs Claude label on the class where the gold has the button (href-matched) ==")
    same = diff = 0; ex = []
    for r in cls:
        if r["gold"] is None: continue
        if norm_text(r["gold_label"]) == norm_text(r["label"]): same += 1
        else:
            diff += 1
            if len(ex) < 12: ex.append(f'{r["code"]}/{r["file"]}: "{r["label"]}" → gold "{r["gold_label"]}"')
    print(f"  same {same} / different {diff}")
    for e in ex: print("   ", e)

if __name__ == "__main__":
    main()
