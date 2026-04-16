# 10. Tag Taxonomy & Normalisation


### Normalisation Algorithm

```
1. Strip red text markers: 🔴[RED TEXT] ... [/RED TEXT]🔴 → extract inner content
2. Identify square-bracket tags within extracted content
3. Trim whitespace from both ends of tag content
4. Compare case-insensitively against normalisation table
5. Extract trailing number or letter-number ID (e.g., "1A", "3", "5C")
6. Map to normalised form + extracted sub-identifier
```

### Complete Tag Normalisation Table

#### Page Structure Tags
| Writer Variants (case-insensitive) | Normalised Form |
|---|---|
| `title bar` | `title_bar` |
| `module introduction` | `module_introduction` |
| `lesson`, `lesson N` | `lesson` + number |
| `lesson overview` | `lesson_overview` |
| `lesson content` | `lesson_content` |
| `end page` | `end_page` |

#### Heading & Body Tags
| Writer Variants | Normalised |
|---|---|
| `h1`–`h5` | `heading` + level |
| `body`, `body text` | `body` |

#### Content Styling Tags
| Writer Variants | Normalised |
|---|---|
| `alert` | `alert` |
| `important` | `important` |
| `alert-wananga`, `alert wananga` | `alert_cultural_wananga` |
| `alert-talanoa`, `alert talanoa` | `alert_cultural_talanoa` |
| `alert-combined`, `alert combined` | `alert_cultural_combined` |
| `whakatauki` | `whakatauki` |
| `quote` | `quote` |
| `rhetorical question` | `rhetorical_question` |
| `full page translate`, `reo translate` | `reo_translate` |

#### Media Tags
| Writer Variants | Normalised |
|---|---|
| `image`, `image N` | `image` |
| `video`, `embed video`, `imbed video`, `insert video`, `embed film`, `imbed film`, `Interactive: Video: Title`, `audio animation video` | `video` |
| `audio` | `audio` |
| `audio image`, `audioimage`, `audioImage` | `audio_image` |
| `image zoom` | `image_zoom` |
| `image label` | `image_label` |

#### Activity Tags
| Writer Variants | Normalised |
|---|---|
| `activity NA`, `activity` | `activity` + ID |
| `activity heading`, `activity heading h3`, `activity heading H3`, `activity title` (with optional heading level H2-H5) | `activity_heading` + level |
| `end activity`, `end of activity` | `end_activity` |

#### Link/Button Tags
| Writer Variants | Normalised |
|---|---|
| `button` | `button` |
| `button- external link`, `button-external link`, `button - external`, `button-external` | `external_link_button` |
| `external link button` | `external_link_button` |
| `external link` | `external_link` |
| `go to journal` | `go_to_journal` |
| `download journal` | `download_journal` |
| `upload to dropbox` | `upload_to_dropbox` |
| `engagement quiz button` | `engagement_quiz_button` |
| `supervisor button` | `supervisor_button` |
| `modal button` | `modal_button` |
| `audio button` | `audio_button` |

#### Interactive Component Tags
| Writer Variants | Normalised |
|---|---|
| `drag and drop` + variants | `drag_and_drop` |
| `dropdown`, `drop down`, `dropdown N` | `dropdown` |
| `dropdown quiz paragraph`, `dropquiz` | `dropdown_quiz_paragraph` |
| `flip cards`, `flip card`, `flipcard`, `flipcards`, `flip card N`, `flipcard image` | `flip_card` |
| `accordion`, `accordion N` | `accordion` |
| `end accordions` | `end_accordions` |
| `click drop`, `clickdrop`, `drop click` | `click_drop` |
| `carousel`, `slide show`, `slideshow` | `carousel` |
| `rotating banner` | `rotating_banner` |
| `slide N` | `carousel_slide` |
| `tabs` | `tabs` |
| `tab N` | `tab` |
| `speech bubble` + any suffix | `speech_bubble` |
| `hint slider`, `hintslider`, `hint slider N`, `hintslider N` | `hint_slider` |
| `hint` | `hint` |
| `shape hover` | `shape_hover` |
| `shape N` | `shape` |
| `reorder` | `reorder` |
| `slider chart` | `slider_chart` |
| `slider` | `slider` |
| `memory game` | `memory_game` |
| `word drag` | `word_drag` |
| `typing self-check`, `typing quiz` | `typing_quiz` |
| `self check`, `self-check` | `self_check` |
| `word highlighter`, `word select` | `word_select` |
| `mcq`, `multi choice quiz`, `multichoice dropdown quiz`, `multi choice dropdown quiz`, `dropdown quiz` | `mcq` |
| `multi choice quiz survey` | `multichoice_quiz_survey` |
| `radio quiz`, `true false` | `radio_quiz` |
| `checklist` | `checklist` |
| `info trigger` + optional text, `hovertrigger`, `hover trigger` | `info_trigger` |
| `info trigger image` | `info_trigger_image` |
| `info audio trigger`, `audio trigger` | `audio_trigger` |
| `venn diagram` | `venn_diagram` |
| `timeline` | `timeline` |
| `self reflection` | `self_reflection` |
| `reflection slider` | `reflection_slider` |
| `stop watch`, `stopwatch` | `stop_watch` |
| `number line` | `number_line` |
| `crossword` | `crossword` |
| `word find`, `wordfind` | `word_find` |
| `bingo` | `bingo` |
| `clicking order` | `clicking_order` |
| `puzzle` | `puzzle` |
| `sketcher` | `sketcher` |
| `glossary` | `glossary` |
| `embed pdf` | `embed_pdf` |
| `embed padlet` | `embed_padlet` |
| `embed desmos`, `desmos graph` | `embed_desmos` |

### Red Text Handling Rules

Content in `🔴[RED TEXT]...[/RED TEXT]🔴` is writer instruction to CS/developers. NOT student-facing.

1. **Tag-only red text:** `🔴[RED TEXT] [H2] [/RED TEXT]🔴` → extract `[H2]` tag, process normally
2. **Tag + instruction:** `🔴[RED TEXT] [drag and drop column autocheck] They are in correct place [/RED TEXT]🔴` → extract tag, capture instruction for interactive reference document only (NOT rendered in HTML)
3. **Pure instruction:** `🔴[RED TEXT] CS: please make images small [/RED TEXT]🔴` → captured for reference but NOT rendered as HTML comments
4. **Whitespace-only:** `🔴[RED TEXT]   [/RED TEXT]🔴` → disregard entirely
5. **NEVER render red text as visible student content**
6. **NEVER render CS/writer instructions as `<!-- CS: ... -->` HTML comments** — they are internal workflow notes captured only in the interactive reference document

---


---

[← Back to index](../CLAUDE.md)
