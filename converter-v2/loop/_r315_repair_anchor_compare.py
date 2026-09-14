"""ROUND 315 (loop Round 2) — repair anchor_compare.py's two HTML parsers (Tree, ATree) so HTML void
elements (<br>, <img>, <meta>, ...) never enter the tag stack, whichever form they arrive in.

WHY: html.parser fires handle_starttag for a plain `<br>` with NO matching handle_endtag, but
handle_startendtag (= start + end) for `<br />`. Both parsers pushed every start tag and popped on
every end tag, so a plain void left a phantom stack entry and a permanently inflated depth: the
widget-skip never released, the wrapper chain drifted, and ATree dropped any <p> holding a <br>
(its </p> met "br" on the stack top). Every Claude page and 76% of the gold pages were parsed that
way until round 315 moved the corpus to the KB's XHTML form and the skeleton gate's PAIRING
(_discrepancy_audit.pairs -> anchor_compare.parse -> Tree) changed on a byte-inert change.
Anchored, unique-match, idempotent. Run from anywhere: python3 _r315_repair_anchor_compare.py
"""
import os, re
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests", "anchor_compare.py")
b = open(P, "rb").read()

def rep(old, new):
    global b
    o = old.encode("utf-8"); n = new.encode("utf-8")
    ins = n[:-len(o)] if n.endswith(o) else n   # an insert whose "new" ends with its own anchor
    if b.count(ins) == 1 and (n.endswith(o) or b.count(o) == 0):
        print("already applied:", old[:48].strip()); return
    assert b.count(o) == 1, (old[:60], b.count(o))
    b = b.replace(o, n)

VOID_BLOCK = (
    "# ROUND 315 (loop Round 2): HTML void elements. html.parser fires handle_starttag for a plain\n"
    "# <br>/<img> with NO matching handle_endtag, but handle_startendtag (start + end) for <br />.\n"
    "# Both trees below pushed every start tag and popped on every end tag, so a plain void left a\n"
    "# phantom stack entry and a permanently inflated depth: the widget-skip never released, the\n"
    "# wrapper chain drifted, and ATree dropped any <p> holding a <br> (its </p> met \"br\" on the\n"
    "# stack top). Voids are now never pushed and their (synthetic) end tags ignored, so <br> and\n"
    "# <br /> parse identically -- exposed when round 315 moved the corpus to the KB's XHTML form.\n"
    "VOID_TAGS = {\"img\", \"br\", \"meta\", \"link\", \"input\", \"hr\", \"source\", \"wbr\", \"area\", \"base\", \"col\", \"embed\", \"track\"}\n"
)
rep("STRUCT = {\"div\", \"section\", \"ul\", \"ol\", \"table\", \"tr\", \"tbody\", \"thead\", \"dl\"}\n",
    VOID_BLOCK + "STRUCT = {\"div\", \"section\", \"ul\", \"ol\", \"table\", \"tr\", \"tbody\", \"thead\", \"dl\"}\n")

# ATree.handle_starttag / handle_endtag
rep("    def handle_starttag(self, tag, attrs):\n        a = dict(attrs)\n        cl = (a.get(\"class\") or \"\").split()\n        rid = a.get(\"id\")\n        name = None\n",
    "    def handle_starttag(self, tag, attrs):\n        if tag in VOID_TAGS:\n            return                      # ROUND 315: a void never enters the stack\n        a = dict(attrs)\n        cl = (a.get(\"class\") or \"\").split()\n        rid = a.get(\"id\")\n        name = None\n")
rep("    def handle_endtag(self, tag):\n        self.depth -= 1\n        if self._node is not None and self.stack and self.stack[-1][1] == tag",
    "    def handle_endtag(self, tag):\n        if tag in VOID_TAGS:\n            return                      # ROUND 315: the synthetic end of a self-closed void\n        self.depth -= 1\n        if self._node is not None and self.stack and self.stack[-1][1] == tag")

# Tree.handle_starttag / handle_endtag
rep("                self.skip_depth = self.depth\n        self.stack.append((tag, cls))\n        self.depth += 1\n",
    "                self.skip_depth = self.depth\n        if tag in VOID_TAGS:\n            return                      # ROUND 315: counted in the inventory, never on the stack\n        self.stack.append((tag, cls))\n        self.depth += 1\n")
rep("    def handle_endtag(self, tag):\n        self.depth -= 1\n        if self.stack:\n            self.stack.pop()\n        if self.skip_depth is not None and self.depth <= self.skip_depth:\n            self.skip_depth = None\n",
    "    def handle_endtag(self, tag):\n        if tag in VOID_TAGS:\n            return                      # ROUND 315: the synthetic end of a self-closed void\n        self.depth -= 1\n        if self.stack:\n            self.stack.pop()\n        if self.skip_depth is not None and self.depth <= self.skip_depth:\n            self.skip_depth = None\n")
open(P, "wb").write(b)
print("anchor_compare.py repaired")
