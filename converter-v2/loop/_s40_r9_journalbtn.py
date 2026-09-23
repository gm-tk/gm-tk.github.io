"""SESSION 40 ROUND 9 (24 Sept 2026) — the §3 PICK measurement: the r447 follow-up "journal buttons INSIDE a widget bundle keep
the green button". For every Claude page, every `div.button` whose text is a journal label: record the nearest ancestor that
is a hand-off box (cv2-interactive), a built widget (a class from the skeleton's WIDGET_MARKERS), an activity box, or none;
and whether the label is D13-5's pure go-to-journal form. Also counts the gold's forms (h4.goJournal vs div.button) on the
paired module, for the per-module comparison.
Run under WSL from reference/tests:  python3 ../../outputs/_s40_r9_journalbtn.py > ../../outputs/_s40_r9_journalbtn.log
"""
import os, re, sys, collections
from html.parser import HTMLParser
sys.path.insert(0, os.getcwd())
import _corpus
from _structural_skeleton import WIDGET_MARKERS

CLAUDE = "../../../01-Claude_Modules_"
PURE = re.compile(r"^(?:go\s+to\s+)?(?:your\s+|the\s+)?(?:learning\s+)?journals?\.?$", re.I)
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "audio", "area", "col", "embed", "param", "track", "wbr"}


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.hits, self.buf = [], [], None

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        cls = set((dict(attrs).get("class") or "").split())
        self.stack.append((tag, cls))
        if tag == "div" and cls == {"button"}:
            self.buf = [len(self.stack), []]

    def handle_data(self, d):
        if self.buf:
            self.buf[1].append(d)

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        if self.buf and len(self.stack) == self.buf[0]:
            text = re.sub(r"\s+", " ", "".join(self.buf[1])).strip()
            if "journal" in text.lower():
                where = "free"
                for t, c in reversed(self.stack[:-1]):
                    if "cv2-interactive" in c:
                        where = "handoff"; break
                    if c & WIDGET_MARKERS:
                        where = "built:" + sorted(c & WIDGET_MARKERS)[0]; break
                    if "activity" in c:
                        where = "activity"; break
                self.hits.append((text, where))
            self.buf = None
        while self.stack:
            t, _ = self.stack.pop()
            if t == tag:
                break


def main():
    tally = collections.Counter()
    pure_where = collections.Counter()
    mods = collections.defaultdict(collections.Counter)
    for fam in sorted(os.listdir(CLAUDE)):
        fdir = os.path.join(CLAUDE, fam)
        if not os.path.isdir(fdir):
            continue
        for mod in sorted(os.listdir(fdir)):
            mdir = os.path.join(fdir, mod)
            if not os.path.isdir(mdir):
                continue
            for f in sorted(os.listdir(mdir)):
                if not f.endswith(".html"):
                    continue
                p = P()
                p.feed(open(os.path.join(mdir, f), encoding="utf8", errors="ignore").read())
                for text, where in p.hits:
                    pure = bool(PURE.match(text))
                    tally[(pure, where)] += 1
                    if pure:
                        pure_where[where] += 1
                        mods[mod][where] += 1
    print("journal div.button by (pure label, where):")
    for (pure, where), n in sorted(tally.items(), key=lambda x: -x[1]):
        print(f"  pure={pure!s:5s} {where:28s} {n}")
    print("pure by where:", dict(pure_where))
    print(f"pure: {sum(pure_where.values())} sites / {len(mods)} modules")
    for mod, c in sorted(mods.items(), key=lambda x: -sum(x[1].values()))[:25]:
        print(f"  {mod}: {dict(c)}")


if __name__ == "__main__":
    main()
