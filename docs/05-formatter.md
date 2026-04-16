# 5. How the Formatter Works


### OutputFormatter (js/formatter.js)

The formatter converts the parser's structured data into the plain text format currently used. In the future architecture, this class will be supplemented (or replaced) by the HTML converter.

### Output Format

- **Metadata block** — `=====` delimited header with module code, subject, course, writer, date
- **Content section** — starts with `--- CONTENT START ---`
- **Paragraphs** — plain text with formatting markers (`**bold**`, `*italic*`, `__underline__`)
- **Red text** — wrapped in `🔴[RED TEXT] content [/RED TEXT]🔴`
- **Hyperlinks** — `text [LINK: URL]` format
- **Lists** — `•` for bullets, `1.` for ordered, 2-space indent per level
- **Tables** — ASCII art with `┌─── TABLE ───` / `└─── END TABLE ───` delimiters, `║` column separator

---


---

[← Back to index](../CLAUDE.md)
