# 7. Current Output Format


The plain text output follows this structure (see `OSAI201_parsed.txt` for a full example):

```
=====================================
MODULE METADATA
=====================================
Module Code: OSAI201
Subject: Online Safety
Course: AI Digital Citizenship
=====================================

--- CONTENT START ---

🔴[RED TEXT] [TITLE BAR]  [/RED TEXT]🔴OSAI AI Digital Citizenship  Kirirarautanga Matihiko AI

🔴[RED TEXT] [H1]  [/RED TEXT]🔴**Tirohanga Whānui | Overview**

🔴[RED TEXT] [H2]  [/RED TEXT]🔴**Learning Intentions**
...
```

### Key Format Conventions

| Element | Format in Output |
|---------|-----------------|
| Square-bracket tags | Inside red text markers: `🔴[RED TEXT] [TAG] [/RED TEXT]🔴` |
| Bold text | `**text**` |
| Italic text | `*text*` |
| Bold + Italic | `***text***` |
| Underline | `__text__` |
| Hyperlinks | `__link text__ [LINK: URL]` |
| Bullet lists | `• item` with 2-space indent per level |
| Tables | `┌─── TABLE ───` / `└─── END TABLE ───` with `║` separators |
| Cell line breaks | `/` within table cells |
| Red text (writer instructions) | `🔴[RED TEXT] content [/RED TEXT]🔴` |
| Images | `[IMAGE: filename]` inside runs |

---


---

[← Back to index](../CLAUDE.md)
