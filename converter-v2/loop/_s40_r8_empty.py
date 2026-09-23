"""SESSION 40 ROUND 8 (24 Sept 2026) — the §3 PICK measurement: what are body_compare's EMPTY hand-off boxes?

body_compare.py counts a `.cv2-interactive` placeholder as EMPTY when its member text (banner, cv2-note /
cv2-comment paragraphs, the reference labels and the ▼ / ▲ glyphs excluded) is under 40 characters. The body
gate carries 200 such pages (the `empty` figure of "body 57 / 5 / 200 / 260"). This probe re-uses the gate's own
parser, records each placeholder's source span, and dumps every empty one: page, banner type, member chars,
the note text and the raw HTML (first 700 chars) — so the class can be split by what the box actually holds.

Run under WSL from reference/tests:  python3 ../../outputs/_s40_r8_empty.py > ../../outputs/_s40_r8_empty.log
Writes ../../outputs/_s40_r8_empty.json (one row per empty placeholder).
"""
import json, os, re, sys, collections
sys.path.insert(0, os.getcwd())
import body_compare as bc
import _corpus

TAG_RE = re.compile(r"<[^>]+>")


class Spans(bc.Body):
    def __init__(self):
        super().__init__()
        self.spans = {}

    def handle_starttag(self, tag, attrs):
        before = self.cv2_key
        super().handle_starttag(tag, attrs)
        if self.cv2_key is not None and self.cv2_key != before:
            self.spans[self.cv2_key] = [self.getpos(), None]

    def handle_endtag(self, tag):
        before = self.cv2_key
        super().handle_endtag(tag)
        if before is not None and self.cv2_key is None and before in self.spans:
            self.spans[before][1] = self.getpos()


def offsets(src):
    starts, n = [0], 0
    for line in src.split("\n"):
        n += len(line) + 1
        starts.append(n)
    return starts


def main():
    mods = sorted(d for d in _corpus.gate_mods(bc.CLAUDE) if os.path.isdir(_corpus.mdir(bc.CLAUDE, d)))
    rows = []
    pages_with = set()
    for mod in mods:
        cdir = _corpus.mdir(bc.CLAUDE, mod)
        hdir = _corpus.mdir(bc.HUMAN, mod)
        if not os.path.isdir(hdir):
            continue
        for cf in sorted(f for f in os.listdir(cdir) if f.endswith(".html")):
            path = os.path.join(cdir, cf)
            src = open(path, encoding="utf8", errors="ignore").read()
            p = Spans()
            try:
                p.feed(src)
            except Exception:
                continue
            offs = offsets(src)
            for k, chars in p.cv2_text.items():
                if chars >= 40:
                    continue
                sp = p.spans.get(k)
                html = ""
                if sp and sp[1]:
                    a = offs[sp[0][0] - 1] + sp[0][1]
                    b = offs[sp[1][0] - 1] + sp[1][1]
                    html = src[a:b + 6]
                text = re.sub(r"\s+", " ", TAG_RE.sub(" ", html)).strip()
                notes = re.findall(r'<p[^>]*class="[^"]*cv2-(?:note|comment)[^"]*"[^>]*>(.*?)</p>', html, re.S)
                rows.append({"page": f"{mod}/{cf}", "module": mod, "banner": p.cv2_banner.get(k, ""),
                             "chars": chars, "notes": [re.sub(r"\s+", " ", TAG_RE.sub(" ", n)).strip()[:200] for n in notes],
                             "text": text[:400], "html": html[:700]})
                pages_with.add(f"{mod}/{cf}")
    json.dump(rows, open("../../outputs/_s40_r8_empty.json", "w"), indent=1)
    print(f"empty placeholders {len(rows)} on {len(pages_with)} pages / {len(set(r['module'] for r in rows))} modules")
    by_banner = collections.Counter(r["banner"].split("+")[0].strip() or "(none)" for r in rows)
    print("by banner type:", by_banner.most_common(25))
    by_prefix = collections.Counter(re.match(r"[A-Z]+", r["module"]).group(0) for r in rows)
    print("by module prefix:", by_prefix.most_common(25))
    by_chars = collections.Counter(min(r["chars"] // 10 * 10, 30) for r in rows)
    print("by member chars (bucket of 10):", sorted(by_chars.items()))
    has_note = sum(1 for r in rows if r["notes"])
    print(f"with a cv2-note / cv2-comment: {has_note}")
    for r in rows[:: max(1, len(rows) // 40)][:40]:
        print("---", r["page"], "|", r["banner"], "| chars", r["chars"])
        print("   TEXT:", r["text"][:300])


if __name__ == "__main__":
    main()
