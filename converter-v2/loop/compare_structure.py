"""compare_structure.py — structural comparison: Claude output vs human-finished HTML.

WHAT THIS MEASURES (the things the brief's diff step cares about):
For every module present in 01-Claude_Modules_, pair its pages with the human
pages in 01-Finalized_Modules_ (document order) and, for every content element
whose TEXT matches between the two (so developer rewording never pollutes the
structural score), compare the element's ANCESTOR WRAPPER CHAIN
(#body > div.row > div.col-* > [callout/activity] > element):

  exact_chain   — the full wrapper chain agrees
  wrapper_set   — same wrappers, different order/duplication
  MISMATCH CATEGORIES (the over-nesting bug classes):
    claude_extra_container  — Claude nested it inside a callout/activity the
                              human kept it OUT of  ← the reported bug
    claude_missing_container— the human wrapped it, Claude didn't
    row_wrap_missing        — human has row/col wrapping, Claude doesn't
    other_chain_diff        — remaining differences (incl. column class)

Also: per-page row-count ratio (Claude rows / human content rows), and the
ACKS CONTENT comparison — position-independent per the locked placement
policy: acks are harvested from EVERY page on both sides (humans put them on
the last page historically), deduped, then matched by exact-or-fuzzy token
overlap. Claude's ❗ ackTodo lines are counted separately, never as content.

EXCLUDED REGIONS (per the brief): interactive-owned subtrees on both sides
(Claude's .cv2-interactive; human subtrees matching the wrapper catalogue's
widget classes) and red-flag <p>s.

USAGE:  python3 compare_structure.py            (all converted modules)
        python3 compare_structure.py OSAH401 …  (specific modules)
Writes structural_comparison.json + prints the aggregate.
"""
import json
import _corpus  # round128: nesting-aware corpus paths
import os
import re
import sys
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.abspath(__file__))
CLAUDE = os.path.join(BASE, "..", "..", "..", "01-Claude_Modules_")
HUMAN = os.path.join(BASE, "..", "..", "..", "01-Finalized_Modules_")
DATA = os.path.join(BASE, "..", "..", "data")

# ---- interactive wrapper classes (data-driven exclusion list) --------------
wrap = json.load(open(os.path.join(DATA, "Interactive_Wrapper_Catalogue.json")))
INTERACTIVE_CLASSES = set()
for i in wrap["interactives"]:
    for c in i.get("classes", []):
        INTERACTIVE_CLASSES.add(c)
    for v in i.get("variants", []):
        for c in v.get("classes", []):
            INTERACTIVE_CLASSES.add(c)
INTERACTIVE_CLASSES |= {"question", "dropContainer", "dragContainer", "clickDropContent",
                        "flipCardsContainer", "bubble-basic", "engagementTrigger",
                        "cv2-interactive"}
# the catalogue's variant class lists carry generic LAYOUT classes too
# (col-*, row, ratio, …) — those must never poison the widget skip-list,
# or every column div gets skipped and no content is compared at all
INTERACTIVE_CLASSES = {c for c in INTERACTIVE_CLASSES
                       if not c.startswith("col-")
                       and c not in {"row", "button", "buttonS", "buttonT", "img-fluid",
                                     "table", "ratio", "ratio-16x9", "videoSection",
                                     "img-thumbnail", "d-block", "w-100"}}

CALLOUT_CLASSES = {"alert", "important", "whakatauki", "wananga", "quoteText", "activity"}
CONTENT_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "ul", "ol", "img", "iframe", "table", "audio"}
# elements HTML allows to go unclosed — they must never enter the depth stack
VOID_TAGS = {"img", "br", "meta", "link", "input", "hr", "source", "wbr", "area", "base", "col", "embed", "track"}


def norm_text(s):
    s = re.sub(r"\s+", " ", s).strip().lower()
    return re.sub(r"[^a-z0-9āēīōū ]", "", s)


# round 72 — whitelisted Word-comment notes render as "<Author>: <text>" (class
# cv2-comment). Like the CS / RED FLAG notes they are Claude-only (the human strips
# EVERY comment), so they are excluded from the structural text match. The six display
# names, lowercased — source of truth: data/Comment_Authors.json.
# round 219 — the ledger note scheme (CL-0010) renders comments "Note from <Author>: …",
# so the "note from" lead is excluded too; the bare author names stay for a
# NOTESCHEME_OFF (legacy-form) corpus. Parity: keep both, never drop either.
CV2_COMMENT_AUTHORS = ("note from", "kate scanlon", "nadia stanton", "caroline schwer",
                       "simon vita", "amanda griffiths", "creative services")


class Page(HTMLParser):
    """Collects #body content elements (+ wrapper chains), rows, and acks."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.in_body = None      # depth of <div id="body">, None outside
        self.skip_depth = None   # inside an interactive subtree
        self.elements = []
        self.cur = None
        self.rows = 0
        self.acks = []           # ack entry texts
        self.ack_todos = 0
        self.in_acks = None
        self.ack_p = None
        self.cur_ack = []

    # ---- start tags ---------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        eid = a.get("id") or ""

        # ---- void elements: never pushed; img/iframe captured as content ----
        if tag in VOID_TAGS:
            if (tag == "img" and self.in_body is not None
                    and self.skip_depth is None and self.in_acks is None
                    and self.cur is None):
                src = os.path.basename((a.get("src") or "").split("?")[0])
                self.elements.append({"tag": "img", "text": norm_text(src) or "img",
                                      "chain": self._chain(len(self.stack))})
            return

        depth = len(self.stack)
        self.stack.append((tag, classes))

        if eid == "body" and tag == "div":
            self.in_body = depth
            return

        # ---- acks harvesting (anywhere in the file) -------------------------
        if "acks" in classes and self.in_acks is None:
            self.in_acks = depth
            return
        if self.in_acks is not None:
            if tag == "p":
                if "ackTodo" in classes:
                    self.ack_todos += 1
                    self.ack_p = -depth      # negative = todo line, skip text
                else:
                    self.ack_p = depth
                    self.cur_ack = []
            return

        if self.in_body is None:
            return

        # ---- interactive-owned subtree skip ---------------------------------
        if self.skip_depth is None and any(c in INTERACTIVE_CLASSES for c in classes):
            self.skip_depth = depth
            return
        if self.skip_depth is not None:
            return

        if tag == "div" and "row" in classes:
            self.rows += 1

        if tag in CONTENT_TAGS and self.cur is None:
            self.cur = {"tag": tag, "chain": self._chain(depth), "depth": depth, "text": []}
            if tag in ("iframe", "audio"):
                src = os.path.basename((a.get("src") or "").split("?")[0])
                self.cur["text"] = [src or tag]
                self._close_cur()

    def _chain(self, depth):
        """Wrapper chain from #body down to (not incl.) the element."""
        chain = []
        for (t, cl) in self.stack[(self.in_body or 0) + 1:depth]:
            if t != "div":
                continue
            if "row" in cl:
                chain.append("row")
            elif any(c.startswith("col-") for c in cl):
                chain.append("col")
            elif any(c in CALLOUT_CLASSES for c in cl):
                chain.append(sorted(c for c in cl if c in CALLOUT_CLASSES)[0])
            elif "videoSection" in cl or "ratio" in cl:
                chain.append("videoSection")
        return tuple(chain)

    # ---- end tags -----------------------------------------------------------
    def handle_endtag(self, tag):
        if tag in VOID_TAGS or not self.stack:
            return
        # tolerate stray closes: only pop when the tag matches something open
        if not any(t == tag for t, _ in self.stack):
            return
        while self.stack:
            t, _ = self.stack.pop()
            depth = len(self.stack)
            if self.cur is not None and depth <= self.cur["depth"]:
                self._close_cur()
            if self.ack_p is not None and depth <= abs(self.ack_p):
                if self.ack_p > 0:
                    text = norm_text(" ".join(self.cur_ack))
                    if text:
                        self.acks.append(text)
                self.ack_p = None
            if self.skip_depth is not None and depth <= self.skip_depth:
                self.skip_depth = None
            if self.in_acks is not None and depth <= self.in_acks:
                self.in_acks = None
            if self.in_body is not None and depth <= self.in_body:
                self.in_body = None
            if t == tag:
                break

    def handle_data(self, data):
        if self.ack_p is not None and self.ack_p > 0:
            self.cur_ack.append(data)
        elif self.cur is not None:
            self.cur["text"].append(data)

    def _close_cur(self):
        text = norm_text(" ".join(self.cur["text"]))
        # exclude Claude's converter-added notes from the structural text match: the
        # human strips ALL of them, so they never have a counterpart. Round 57 split the
        # one "RED FLAG:" prefix by SOURCE into "RED FLAG:" (converter diagnostic) and
        # "CS:" (writer->Creative-Services note) — both are still Claude-only notes, so
        # both prefixes are excluded here (norm_text strips the colon -> "red flag" / "cs ").
        # Round 219 — the ledger note scheme (CL-0010/CL-0013) renames the prefixes to
        # "Writers Note:" / "Red Flag:" / "Designer/Developer To Do:" (norm_text folds
        # the last to "designerdeveloper to do" — the slash is stripped). "red flag"
        # already covers the new "Red Flag:"; the legacy "cs " stays for a
        # NOTESCHEME_OFF corpus. Parity rule: ADD new prefixes here, never drop legacy.
        if (text and not text.startswith("red flag") and not text.startswith("cs ")
                and not text.startswith("writers note")
                and not text.startswith("designerdeveloper to do")
                and not text.startswith(CV2_COMMENT_AUTHORS) and len(text) >= 3):
            self.elements.append({"tag": self.cur["tag"], "text": text,
                                  "chain": self.cur["chain"]})
        self.cur = None


def parse_page(path):
    p = Page()
    p.feed(open(path, encoding="utf8", errors="ignore").read())
    return p


def page_sort_key(name):
    m243 = re.search(r"_(\d+)_(\d+(?:_\d+)*)\.html$", name)   # ROUND 243: the library-form name CODE_L_S.html
    if m243:                                                    # (both sides may carry it now)
        return float(f"{m243.group(1)}.{m243.group(2).split('_')[0]}")
    nums = re.findall(r"(\d+(?:\.\d+)?)", name.rsplit("-", 1)[-1].rsplit("_", 1)[-1])
    return float(nums[0]) if nums else 0


def fuzzy_in(needle, hay_set, hay_tokens):
    if needle in hay_set:
        return True
    nt = set(needle.split())
    if len(nt) < 4:
        return False
    return any(len(nt & ht) / len(nt) >= 0.7 for ht in hay_tokens)


def compare_module(mod):
    cdir = _corpus.mdir(CLAUDE, mod)
    hdir = _corpus.mdir(HUMAN, mod)
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=page_sort_key)
    # ROUND 440 (D13-6): the gold listing goes through compare_gold_pages.txt (_corpus.gold_pages; GOLDPAGES_OFF=1 = all).
    hpages = sorted(_corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=page_sort_key)
    if not cpages or not hpages:
        return None

    res = {"module": mod, "pages": f"{len(cpages)}/{len(hpages)}",
           "matched": 0, "exact_chain": 0, "wrapper_set": 0,
           "claude_extra_container": 0, "claude_missing_container": 0,
           "row_wrap_missing": 0, "other_chain_diff": 0,
           "examples": [], "rows_ratio": None, "content_match_share": 0}

    # acks: EVERY page on both sides (humans used the last page historically)
    claude_acks, human_acks = [], []
    ack_todos = 0
    cparsed = [parse_page(os.path.join(cdir, f)) for f in cpages]
    hparsed = [parse_page(os.path.join(hdir, f)) for f in hpages]
    for p in cparsed:
        claude_acks += p.acks
        ack_todos += p.ack_todos
    for p in hparsed:
        human_acks += p.acks
    claude_acks = list(dict.fromkeys(claude_acks))
    human_acks = list(dict.fromkeys(human_acks))

    fam = lambda t: "h" if t.startswith("h") else t
    ratios = []
    total_c_elems = 0
    for ci in range(min(len(cpages), len(hpages))):
        cp, hp = cparsed[ci], hparsed[ci]
        if hp.rows:
            ratios.append(cp.rows / hp.rows)
        hindex = {}
        for e in hp.elements:
            hindex.setdefault((fam(e["tag"]), e["text"][:80]), []).append(e)
        total_c_elems += len(cp.elements)
        for e in cp.elements:
            matches = hindex.get((fam(e["tag"]), e["text"][:80]))
            if not matches:
                continue
            h = matches[0]
            res["matched"] += 1
            cch, hch = e["chain"], h["chain"]
            if cch == hch:
                res["exact_chain"] += 1
                continue
            if set(cch) == set(hch):
                res["wrapper_set"] += 1
                continue
            cset, hset = set(cch), set(hch)
            extra = (cset - hset) & CALLOUT_CLASSES
            missing = (hset - cset) & CALLOUT_CLASSES
            if extra:
                res["claude_extra_container"] += 1
                kind = f"claude wrapped in {sorted(extra)}; human did not"
            elif missing:
                res["claude_missing_container"] += 1
                kind = f"human wrapped in {sorted(missing)}; claude did not"
            elif "row" in hset and "row" not in cset:
                res["row_wrap_missing"] += 1
                kind = "human row/col wrapped; claude bare"
            else:
                res["other_chain_diff"] += 1
                kind = f"chain differs: claude {list(cch)} vs human {list(hch)}"
            if len(res["examples"]) < 5:
                res["examples"].append({"page": cpages[ci], "tag": e["tag"],
                                        "text": e["text"][:60],
                                        "claude": list(cch), "human": list(hch),
                                        "kind": kind})

    res["content_match_share"] = round(res["matched"] / total_c_elems, 3) if total_c_elems else 0
    res["rows_ratio"] = round(sum(ratios) / len(ratios), 2) if ratios else None

    ca_set, ha_set = set(claude_acks), set(human_acks)
    ca_tok = [set(a.split()) for a in claude_acks]
    ha_tok = [set(a.split()) for a in human_acks]
    res["acks"] = {
        "human_entries_found_in_claude":
            f"{sum(1 for a in human_acks if fuzzy_in(a, ca_set, ca_tok))}/{len(human_acks)}",
        "claude_entries_found_in_human":
            f"{sum(1 for a in claude_acks if fuzzy_in(a, ha_set, ha_tok))}/{len(claude_acks)}",
        "claude_todo_lines": ack_todos,
    }
    return res


def main():
    mods = sys.argv[1:] or sorted(
        m for m in _corpus.gate_mods(CLAUDE)   # r343: minus compare_exclusions.txt
        if os.path.isdir(_corpus.mdir(CLAUDE, m)) and os.path.isdir(_corpus.mdir(HUMAN, m)))
    results = []
    for m in mods:
        marker = _corpus.mdir(CLAUDE, m, "_run.json")
        if os.path.exists(marker) and json.load(open(marker)).get("error"):
            continue
        try:
            r = compare_module(m)
            if r:
                results.append(r)
        except Exception as e:  # surface, never absorb
            results.append({"module": m, "error": str(e)})

    json.dump(results, open(os.path.join(BASE, "structural_comparison.json"), "w"),
              indent=1, ensure_ascii=False)

    ok = [r for r in results if "error" not in r]
    tot = lambda k: sum(r[k] for r in ok)
    matched = tot("matched")
    total_elems = sum(round(r["matched"] / r["content_match_share"]) for r in ok if r["content_match_share"])
    print(f"modules compared: {len(ok)} (comparator errors: {len(results) - len(ok)})")
    print(f"claude content elements: ~{total_elems} | text-matched against human: {matched}"
          f" ({matched / total_elems:.1%} — unmatched = developer rewording/restructuring)")
    if matched:
        print(f"  exact wrapper chain:        {tot('exact_chain'):6d}  ({tot('exact_chain') / matched:.1%})")
        print(f"  same wrappers, diff order:  {tot('wrapper_set'):6d}  ({tot('wrapper_set') / matched:.1%})")
        print(f"  claude EXTRA container:     {tot('claude_extra_container'):6d}  ({tot('claude_extra_container') / matched:.1%})  ← over-nesting")
        print(f"  claude MISSING container:   {tot('claude_missing_container'):6d}  ({tot('claude_missing_container') / matched:.1%})")
        print(f"  row wrap missing:           {tot('row_wrap_missing'):6d}  ({tot('row_wrap_missing') / matched:.1%})")
        print(f"  other chain diffs:          {tot('other_chain_diff'):6d}  ({tot('other_chain_diff') / matched:.1%})")
    ratios = [r["rows_ratio"] for r in ok if r["rows_ratio"]]
    if ratios:
        print(f"rows ratio (claude/human content rows) avg: {sum(ratios) / len(ratios):.2f}")
    hf = [tuple(map(int, r["acks"]["human_entries_found_in_claude"].split("/"))) for r in ok]
    cf = [tuple(map(int, r["acks"]["claude_entries_found_in_human"].split("/"))) for r in ok]
    med = lambda xs: sorted(xs)[len(xs) // 2] if xs else 0
    hshare = [a / b for a, b in hf if b]
    cshare = [a / b for a, b in cf if b]
    print(f"acks content (per-module MEDIAN — pooled totals are skewed by legacy giants):")
    print(f"  human entries found in claude: median {med(hshare):.1%}"
          f"  (pooled {sum(a for a, b in hf)}/{sum(b for a, b in hf)})")
    print(f"  claude entries found in human: median {med(cshare):.1%}"
          f"  (pooled {sum(a for a, b in cf)}/{sum(b for a, b in cf)})"
          f" | claude ❗ todo lines: {sum(r['acks']['claude_todo_lines'] for r in ok)}")
    worst = sorted(ok, key=lambda r: -r["claude_extra_container"])[:8]
    print("worst over-nesting:", [(r["module"], r["claude_extra_container"]) for r in worst if r["claude_extra_container"]])


if __name__ == "__main__":
    main()
