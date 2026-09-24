#!/usr/bin/env python3
"""Session 45 Round 1 — write the PICK (engine r486) + the in-flight marker in LOOP_STATE.md (§3 step 1, BEFORE any code). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r486-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈03:25, session 44 Round 11")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 486 IN FLIGHT — NOT PROVEN** (session 45 Round 1, 25 Sept ≈05:55): KB 01F / 05D THE WRITER'S `[quote]` IS "
         "`p.quoteText` + `p.quoteAck` (no wrapper div). Files: `app/js/ContentConverter.js` (`#calloutOpen` strict path + a new "
         "`#quoteKbForm`), `data/Emit_Templates.json` `callouts.by_tag.quote.kb_p_form` {enabled, env `QUOTEFORM_OFF`}. Affected: the "
         "modules whose WT carries a quote-family tag (≈ 17; the in-memory probe decides).")
p = [i for i, l in enumerate(L) if l.startswith("## Session 44 — Round 11 PICK (engine r485)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 45 — Round 1 PICK (engine r486) — KB 01F THE WRITER'S QUOTE IS p.quoteText + p.quoteAck (IN FLIGHT)",
 "- **Lane:** the loss ledger's largest low family not recently laned (HIS1: 77 pages, 49.8 %, 1.55pp — `_s45_r1_his1.log`, the "
 "`_s44_famdiff.py` view): its rows are the D13-5 journal button (decided — the HIS golds are NAMED overrides), the body row "
 "composition (the r435 follow-up), `span.infoTrigger`, and **`p.quoteText` / `p.quoteAck` MISSING** (23 + 20 lines). KB-first: "
 "**01F's tag table maps `quote` → `<p class=\"quoteText\">\"Quote\"</p><p class=\"quoteAck\">Attribution</p>`** (05D 'Quote Text' "
 "the same) — a KB row nobody had captured (`KB_AMALGAMATION_STATUS.md` has no quote row).",
 "- **Measured (`_s45_r1_quote.py`, `_s45_r1_quote2.py`):** gold 290+ `p.quoteText` / 221 `p.quoteAck` on 125 pages / 67 dirs, "
 "NEVER a div; Claude 45 `div.quoteText` boxes on 25 pages (the `callouts.by_tag.quote` template `<div class=\"quoteText\">` "
 "wrapping the gathered `<p>`s; the attribution glued into the quote's own `<p>`). Writer quote tags: `[quote]` 29, `[quote link]` 7, "
 "`[quotation]` 4 (+ singles) in 17 modules. Where the gold styles a tagged quote it is `p.quoteText` (+ `p.quoteAck`) — "
 "EXBP901 / OSAI301 / 401 / 501 / ENGJ402 / OSAH401; TWHA906's two go in a whakatauki box and ENGS101 / SSCI104 / XDLS906 plain "
 "(NAMED overrides — level 1). **The UNTAGGED quote (the gold's larger population) is NOT derivable corpus-wide:** a WT line "
 "opening with a quote mark is `p.quoteText` in the gold 41 / 399 = 0.10 (plain p 0.26, absent 0.21, li 0.11); only HIS reaches "
 "0.68 (26 / 38) — a family-dialect candidate for its own round (Follow-up).",
 "- **Authority:** level 1 — KB 01F (the normalised tag → HTML table) + 05D, the gold agreeing wherever it styles the tag. "
 "The fix: the quote box's `<p>`s become `p.quoteText`; the attribution — a trailing ` – Name` / `” Name.` / `By …` tail of the "
 "LAST paragraph, or a last paragraph that is itself a dash / Source / By line — becomes its own `p.quoteAck`; no wrapper div. "
 "Predicts a small skeleton move up on ≈ 18 paired pages (each quote: `div.quoteText` + `p` → the gold's `p.quoteText` + "
 "`p.quoteAck`); a KB-rule round — neither counts toward nor resets the plateau unless it moves ≥ 0.02pp.",
]
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(L)); os.replace(S + ".tmp", S)
print("ok", os.path.getsize(S))
