# 9. Template System Knowledge


### Template Levels (Year Levels)

Module code prefix indicates year level and determines the `template` attribute on the `<html>` tag:

| Code Suffix | Year Level | Template Attribute | Example |
|-------------|-----------|-------------------|---------|
| `101` | Years 1–3 | `template="1-3"` | OSAI101 |
| `201` | Years 4–6 | `template="4-6"` | OSAI201 |
| `301` | Years 7–8 | `template="7-8"` | OSAI301 |
| `401` | Years 9–10 | `template="9-10"` | OSAI401 |
| `501` / NCEA | NCEA | `template="NCEA"` | OSAI501 |

### HTML Tag Patterns

| Level | HTML Tag |
|-------|---------|
| Years 1–3 | `<html lang="en" level="" template="1-3" class="notranslate" translate="no" >` |
| Years 4–6 | `<html lang="en" level="" template="4-6" class="notranslate" translate="no" >` |
| Years 7–8 | `<html lang="en" level="" template="7-8" class="notranslate" translate="no" >` |
| Years 9–10 | `<html lang="en" level="" template="9-10" class="notranslate" translate="no">` |
| NCEA | `<html lang="en" level="" template="NCEA" class="notranslate " translate="no">` |

**Note:** `level=""` is ALWAYS empty. Do not populate it.

### Refresh Template Sub-Types

| Sub-Type | `template=` | `<body>` class | Navigation | Footer class |
|----------|-------------|---------------|------------|-------------|
| Standard | `1-3`/`4-6`/`7-8`/`9-10` | `container-fluid` | None | `footer-nav` |
| Bilingual | `1-3` | `container-fluid reoTranslate` | None | `footer-nav` |
| Fundamentals | `combo` | `fundamentals container-fluid` | `div.phases` | `footer-nav fundamentals-nav` |
| Inquiry | `combo` | `inquiry container-fluid` | `div.crumbs` | `footer-nav inquiry-nav` |
| Combo | `combo` | `container-fluid` | None | `footer-nav` |

### Document Shell (Refresh Baseline)

```html
<!doctype html>
<html lang="en" level="" template="..." class="notranslate" translate="no">
<head>
  <meta charset="utf-8" />
  <meta content="IE=edge" http-equiv="X-UA-Compatible" />
  <meta content="width=device-width, initial-scale=1" name="viewport" />
  <title>MODULE_CODE Module Title</title>
  <script type="text/javascript" src="https://tekura.desire2learn.com/shared/refresh_template/js/idoc_scripts.js"></script>
</head>
<body class="container-fluid">
  <div id="header">
    <div id="module-code"><h1>MODULE_CODE</h1></div>
    <h1><span>English Title </span></h1>
    <!-- Years 9-10/NCEA: add second h1 for Te Reo title -->
    <div id="module-head-buttons">
      <div id="module-menu-button" class="circle-button btn1" tooltip="Overview"></div>
    </div>
    <div id="module-menu-content" class="moduleMenu">
      <!-- Module menu content here -->
    </div>
  </div>
  <div id="body">
    <!-- All content rows here -->
  </div>
  <div id="footer">
    <ul class="footer-nav">
      <li><a href="" id="prev-lesson" target="_self"></a></li>
      <li><a href="" id="next-lesson" target="_self"></a></li>
      <li><a href="" class="home-nav" target="_parent"></a></li>
    </ul>
  </div>
</body>
</html>
```

### Key Structural Rules

1. **DOCTYPE:** Always lowercase `<!doctype html>`
2. **Void elements:** XHTML-style self-closing (`<meta ... />`, `<img ... />`, `<link ... />`)
3. **Grid:** ALL body content inside `<div class="row"><div class="col-md-8 col-12">` (default)
4. **Body headings:** `<h2>`–`<h5>` have NO `<span>` wrappers — spans only inside `<h1>` header titles
5. **Heading formatting:** Never wrap entire headings in italic/bold (usually .docx artefact)
6. **No inline CSS/JS:** Never add custom styles or scripts

### Page Structure

```
Overview page (-00):
  Header: #module-code has full MODULE_CODE
  h1 spans: Module code prefix stripped, English + Te Reo split on double-space
           (NO trailing space inside span — Phase 13)
  Module menu: Full tabbed (Overview + Information tabs) with routed content
    - Tooltip on #module-menu-content only (NOT on #module-menu-button)
    - Content before [MODULE INTRODUCTION] → tab panes
    - Content after [MODULE INTRODUCTION] → <div id="body">
  Title element: MODULE_CODE English Title
                 (NO decimal lesson number — Phase 13)
  Footer: next-lesson + home-nav only

Lesson page (-01, -02, etc.):
  Header: #module-code format depends on template (Phase 15):
          4-6: decimal (1.0, 2.0, etc.)
          1-3, 7-8, 9-10, NCEA: zero-padded (01, 02, 03)
  h1 span: LESSON-specific title (first [H2] in body, "Lesson N:" prefix stripped)
           — Phase 13; extracted via HtmlConverter._extractLessonTitle()
           and passed to the skeleton as pageData.lessonTitle.
           Falls back to the module title with a console warning if missing.
           NO trailing space inside span.
  Te Reo h1: suppressed on 1-3 / 4-6 / 7-8 / bilingual lesson pages (titles
           array is ["english"]); emitted on 9-10 and NCEA lesson pages
           (titles array is ["english", "tereo"]).
  Module menu: Simplified (no tabs), populated from [Lesson Overview] content
    - NO tooltip attribute on #module-menu-button (Phase 13; tooltipOn: null)
    - Content between [Lesson Overview] and [Lesson Content] → module menu
    - Two-tier structure (Phase 13):
        <h5>{sectionHeading from config}</h5>
        <p>{writer's intro text verbatim, e.g. "We are learning:"}</p>
        <ul><li>bullet items...</li></ul>
      sectionHeadings come from template config; writer intro text is
      preserved verbatim (reversing the prior "labels from config" rule).
    - List items have italic stripped, description paragraph included
    - [Lesson Content] marks start of body content
  Title element: MODULE_CODE English Title
                 (NO decimal lesson number — Phase 13)
  Footer: prev + next + home (middle pages), prev + home (final page)

Years 9-10/NCEA: DUAL h1 titles (English + Te Reo) on EVERY page
```

### Module Menu Structure (Lesson Pages) — Phase 13 Two-Tier

Lesson-page module menus now use a two-tier structure. The section heading
(an `<h5>`) comes from template config; the intro paragraph (a `<p>`) is
taken verbatim from the writer's own text. This reverses the earlier rule
that substituted config label text for the writer's intro.

**Section headings** (new — from `moduleMenu.lessonPage.sectionHeadings`):

| Template Level | Learning section `<h5>` | Success section `<h5>` |
|----------------|-------------------------|------------------------|
| 1-3, 4-6, 7-8, 9-10, NCEA | `Learning Intentions` | `How will I know if I've learned it?` |

**Intro paragraphs** (now verbatim from writer text — fallback `labels` in
`moduleMenu.lessonPage.labels` used only when no writer paragraph is
detected):

| Template Level | Learning intro `<p>` (fallback) | Success intro `<p>` (fallback) |
|----------------|----------------------------------|---------------------------------|
| 1-3, 4-6 | `We are learning:` | `You will show your understanding by:` |
| 7-8, 9-10, NCEA | `We are learning:` | `I can:` |

**Critical (Phase 13 reversal):** Intro text is now preserved VERBATIM from
the writer's paragraph (whatever phrasing they used — "We are learning:",
"I can:", "You will show your understanding by:", "Success Criteria", etc.).
The section heading above it is the only text sourced from template config.

### Footer Navigation

Link ordering differs by page type (Phase 15):

| Page Position | Navigation Links (in order) |
|--------------|-----------------|
| Overview (-00) | `next-lesson`, then `home-nav` |
| Middle lesson pages | `home-nav`, then `prev-lesson`, then `next-lesson` |
| Final lesson page | `home-nav`, then `prev-lesson` |

Navigation hrefs: `MODULE_CODE-XX.html` (e.g., `OSAI201-00.html`, `OSAI201-01.html`)

---


---

[← Back to index](../CLAUDE.md)
