# Change Request — PageForge → HTML Convertor (consolidated)

**Scope.** One consolidated request covering all the Convertor-side changes that are still pending (none actioned yet). It states *what* must change — not where or how. Three areas: **(A)** red designer notes — a source-specific prefix per note, all rendered red **and** bold; **(B)** SPLIT MODE — one HTML file per prompt; **(C)** manual-stitch guidance comments.

---

## A. Red designer notes — prefix by source, rendered red + bold

Replace the single generic `RED FLAG:` prefix with **three source-specific prefixes**, chosen by where the note came from. All three render identically (see *Styling* below); only the prefix differs.

**1. Captured reviewer comment → `Note from {author}:` (kept verbatim).**
A red note derived from a native Word **comment** captured from the Writer's Template / Media List, authored by a whitelisted reviewer (copyright / editor / Creative-Services — Kate Scanlon, Nadia Stanton, Caroline Schwer, Simon Vita, Amanda Griffiths, Creative Services). PageForge already supplies these with the `Note from {author}:` lead, e.g. `Note from Creative Services: …`. Render that lead **verbatim** — do not reword it, drop the author, or replace it with any other prefix. (Recognised by the `Note from {whitelisted author}:` lead.)

**2. Writer's own note/instruction → `Writers Note:`.**
A red note derived from a comment or instruction the **writer** placed in the Writer's Template / Media List (writer-authored red text the project surfaces — i.e. one that does **not** carry a `Note from {author}:` lead). Where the project currently prefixes such a note `RED FLAG:`, prefix it **`Writers Note:`** instead.

**3. Issue detected by the Convertor → `Red Flag:`.**
Any issue the Convertor itself detects during conversion (an ambiguity, missing or unconfirmed information, a structure it cannot safely build, etc.) and surfaces into the HTML is prefixed **`Red Flag:`**.

**Styling (all three).** Every one of these notes must render **coloured red and in bold** (bold font weight), in the same visible style the project already uses for designer messages. They are always **visible** — never a hidden HTML comment, never student-facing. Only the source-specific prefix and the added bold weight are new.

---

## B. SPLIT MODE — generate exactly one HTML file per prompt

When the designer invokes SPLIT MODE, produce **one — and only one — HTML file per response**:

- First response: the **base** HTML file only.
- Each subsequent response (on the designer's next prompt): the **next single section/lesson file**, one at a time, in order.

Never emit more than one file in a single turn. Example — a single-page module with four embedded lessons: turn 1 → base; turn 2 → lesson 1; turn 3 → lesson 2; turn 4 → lesson 3; turn 5 → lesson 4 (one file each, on the designer's prompt). Each section file still contains **only** the exact HTML for that one slot — the content destined for the module's single `#body` at that lesson's position — exactly as the existing SPLIT MODE contract requires, and nothing else.

---

## C. Highly detailed manual-stitch guidance comments

The base file and every section file must include **very clear, highly detailed comments** telling a human developer exactly **how and where** to stitch the files together by hand — which splice point each section replaces, the order they go in, and where each section's insertable content begins and ends.

So these instructions can be removed automatically when the developer instead stitches via the PageForge web app, wrap **all** such guidance in a clearly delimited block:

```
<!-- PAGEFORGE-GUIDE-START -->
<!-- …highly detailed manual-stitch instructions… -->
<!-- PAGEFORGE-GUIDE-END -->
```

- In the **base** file: place a guide block at each splice point, explaining which section file fills it and in what order.
- In each **section** file: place a guide block (ideally *outside* the section's content markers, so a manual copy of the content doesn't drag the guidance along) stating which base splice point this section fills.

PageForge's Page Stitcher already **strips every `PAGEFORGE-GUIDE` block** during automated stitching, so the finalised unified HTML contains none of these manual instructions — they exist purely to help a developer who assembles the files by hand.

---

**Unchanged.** The section content itself, the `PAGEFORGE-SPLICE` / `PAGEFORGE-SECTION` markers, the lesson `<!-- N -->` delimiters, and the round-trip guarantee all remain exactly as in the existing Native Word-comment capture and SPLIT MODE / stitch contract.
