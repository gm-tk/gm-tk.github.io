# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-24 15:51 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 7fd11eb; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 64 paired pages / 12 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 4.4 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 10354 — by direction {'SUBSTITUTED': 713, 'EXTRA': 4606, 'MISSING': 4531, 'MOVED': 504}
- by region: {'title': 44, 'header': 3, 'module-menu': 22, 'footer': 30, 'acks': 34, 'activity': 5791, 'body': 4398, 'root': 32}
- classes: 578 — CANDIDATE 12, below floor 558, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| crumbs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: 
- **crumbs** by template: 
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:head-buttons` | 11 | 3 | 0.36 | 0.36 | — | BELOW FLOOR |
| F2 | MISSING | `header:chip=module-code` | 11 | 3 | 0.36 | 0.36 | — | BELOW FLOOR |
| F3 | EXTRA | `header:chip=decimal-number` | 11 | 3 | 0.64 | 0.36 | — | BELOW FLOOR |
| F4 | MISSING | `header:title-h1-count=2` | 14 | 2 | 1.00 | 1.00 | — | BELOW FLOOR |
| F5 | EXTRA | `header:title-h1-count=1` | 14 | 2 | 0.00 | 1.00 | — | BELOW FLOOR |
| F6 | EXTRA | `footer:links=prev-lesson,home-nav` | 7 | 7 | 0.08 | 0.92 | — | BELOW FLOOR |
| F7 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 7 | 6 | 0.70 | 0.70 | — | BELOW FLOOR |
| F8 | MISSING | `footer:link=next-lesson` | 6 | 6 | 0.89 | 0.89 | — | BELOW FLOOR |
| F9 | EXTRA | `footer:link=prev-lesson` | 3 | 2 | 0.78 | 0.22 | — | BELOW FLOOR |
| F10 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 2 | 2 | 0.70 | 0.30 | — | BELOW FLOOR |
| F11 | EXTRA | `footer:present` | 2 | 1 | 0.97 | 0.03 | — | BELOW FLOOR |
| F12 | EXTRA | `footer:ul=footer-nav` | 2 | 1 | 0.97 | 0.03 | — | BELOW FLOOR |
| F13 | EXTRA | `footer:link=home-nav` | 2 | 1 | 0.97 | 0.03 | — | BELOW FLOOR |
| F14 | EXTRA | `footer:link=next-lesson` | 1 | 1 | 0.89 | 0.11 | — | BELOW FLOOR |
| F15 | MISSING | `footer:links=next-lesson,home-nav` | 1 | 1 | 0.19 | 0.19 | — | BELOW FLOOR |
| F16 | MISSING | `footer:link=prev-lesson` | 1 | 1 | 0.78 | 0.78 | — | BELOW FLOOR |
| F17 | EXTRA | `footer:links=next-lesson,home-nav` | 1 | 1 | 0.19 | 0.81 | — | BELOW FLOOR |
| F18 | MISSING | `footer:inside-body` | 1 | 1 | 0.02 | 0.02 | — | BELOW FLOOR |


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | MISSING | `span>span.sassoonI-text` | `span.sassoonI-text` | `—` | 15 | 4 | 0.23 of 64 | — | 0.80 | — | BELOW FLOOR |
| 2 | title | MISSING | `div#header` | `h1>span` | `—` | 14 | 2 | 1.00 of 64 | — | 0.29 | yes | BELOW FLOOR |
| 3 | header | MISSING | `div#header` | `p` | `—` | 3 | 1 | 0.05 of 64 | — | 0.00 | yes | BELOW FLOOR |
| 4 | module-menu | MISSING | `div#header` | `div#module-head-buttons` | `—` | 11 | 3 | 0.36 of 64 | — | structure | yes | BELOW FLOOR |
| 5 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 6 | 6 | 0.89 of 64 | — | structure | yes | BELOW FLOOR |
| 6 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 6 | 6 | 0.97 of 64 | — | structure | yes | BELOW FLOOR |
| 7 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav` | 3 | 2 | 0.03 of 64 | — | structure | yes | BELOW FLOOR |
| 8 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a#prev-lesson` | 1 | 1 | 0.22 of 64 | — | structure | yes | BELOW FLOOR |
| 9 | footer | MISSING | `ul.footer-nav` | `li>a#prev-lesson` | `—` | 1 | 1 | 0.78 of 64 | — | structure | yes | BELOW FLOOR |
| 10 | footer | MISSING | `div#body` | `div#footer` | `—` | 1 | 1 | 0.02 of 64 | — | structure | yes | BELOW FLOOR |
| 11 | activity | MISSING | `a` | `div.button` | `—` | 31 | 11 | 0.34 of 64 | — | 0.27 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 12 | activity | EXTRA | `div.col-12` | `—` | `p` | 37 | 10 | 0.66 of 64 | template=Bilingual c=0.66 n=37 | structure | — | CANDIDATE |
| 13 | activity | MISSING | `div.activity.interactive[number=*]` | `div.row` | `—` | 29 | 10 | 0.36 of 64 | — | 0.61 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 14 | activity | EXTRA | `p>b` | `—` | `b` | 25 | 10 | 0.89 of 64 | template=Bilingual c=0.89 n=25 | structure | — | CANDIDATE |
| 15 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 25 | 10 | 0.95 of 64 | template=Bilingual c=0.95 n=25 | structure | — | CANDIDATE |
| 16 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 27 | 9 | 1.00 of 64 | template=Bilingual c=1.00 n=27 | structure | — | CANDIDATE |
| 17 | activity | MISSING | `div.col-12` | `p` | `—` | 25 | 9 | 0.30 of 64 | — | 0.43 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 18 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 21 | 9 | 0.77 of 64 | ptype=lesson c=0.94 n=21 | structure | — | CANDIDATE |
| 19 | activity | MISSING | `div.col-12` | `div.row` | `—` | 19 | 9 | 0.27 of 64 | — | 0.97 | — | BELOW FLOOR |
| 20 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 30 | 8 | 0.83 of 64 | template=Bilingual c=0.83 n=30 | structure | — | CANDIDATE |
| 21 | activity | MOVED | `div.col-12` | `p` | `p` | 21 | 8 | 0.27 of 64 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 22 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 16 | 8 | 0.47 of 64 | — | structure | — | BELOW FLOOR |
| 23 | activity | EXTRA | `div.col-12` | `—` | `audio.audioPlayer.icon` | 25 | 7 | 1.00 of 64 | template=Bilingual c=1.00 n=25 | structure | yes | CANDIDATE |
| 24 | activity | MOVED | `div.col-12` | `h3` | `h3` | 20 | 7 | 0.31 of 64 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 25 | activity | EXTRA | `div.col-12` | `—` | `h3` | 18 | 7 | 0.41 of 64 | — | structure | — | BELOW FLOOR |
| 26 | activity | MISSING | `div.col-12` | `h3` | `—` | 17 | 7 | 0.42 of 64 | — | 0.71 | — | BELOW FLOOR |
| 27 | activity | SUBSTITUTED | `div.col-12` | `p` | `p>b` | 16 | 7 | 0.77 of 64 | — | structure | — | BELOW FLOOR |
| 28 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity.interactive[number=*]` | 13 | 7 | 0.73 of 64 | — | structure | yes | BELOW FLOOR |
| 29 | activity | MOVED | `div.col-12` | `p` | `p` | 10 | 7 | 0.23 of 64 | — | structure | — | BELOW FLOOR |
| 30 | activity | MISSING | `div.activity.alertPadding[number=*]` | `div.row` | `—` | 9 | 7 | 0.27 of 64 | — | 0.11 | yes | BELOW FLOOR |
| 31 | activity | MISSING | `div.activity.alertPadding.dropbox[number` | `div.row` | `—` | 8 | 7 | 0.28 of 64 | — | 0.25 | yes | BELOW FLOOR |
| 32 | activity | MOVED | `ul` | `li` | `li` | 10 | 6 | 0.27 of 64 | — | structure | — | BELOW FLOOR |
| 33 | activity | MOVED | `div.col-12` | `p>b` | `p>b` | 8 | 6 | 0.19 of 64 | — | structure | — | BELOW FLOOR |
| 34 | activity | MISSING | `div.row` | `div.col-12` | `—` | 9 | 5 | 0.48 of 64 | — | 0.55 | — | BELOW FLOOR |
| 35 | activity | MISSING | `div.col-12` | `p>b` | `—` | 7 | 5 | 0.34 of 64 | — | 0.36 | — | BELOW FLOOR |
| 36 | activity | MISSING | `div.activity[number=*]` | `div.row` | `—` | 7 | 5 | 0.14 of 64 | — | 0.29 | yes | BELOW FLOOR |
| 37 | activity | MISSING | `div.col-12` | `ul` | `—` | 6 | 5 | 0.11 of 64 | — | 0.61 | — | BELOW FLOOR |
| 38 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `h3` | 6 | 5 | 0.27 of 64 | — | structure | yes | BELOW FLOOR |
| 39 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `h3` | 5 | 5 | 0.28 of 64 | — | structure | yes | BELOW FLOOR |
| 40 | activity | SUBSTITUTED | `div.col-12` | `div.row` | `p` | 10 | 4 | 0.55 of 64 | — | structure | — | BELOW FLOOR |
| 41 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `WIDGET` | 6 | 4 | 0.73 of 64 | — | structure | yes | BELOW FLOOR |
| 42 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `h3` | 6 | 4 | 0.73 of 64 | — | structure | yes | BELOW FLOOR |
| 43 | activity | EXTRA | `p` | `—` | `b` | 5 | 4 | 0.91 of 64 | — | structure | — | BELOW FLOOR |
| 44 | activity | SUBSTITUTED | `div.col-12` | `p>b` | `p` | 5 | 4 | 0.55 of 64 | — | structure | — | BELOW FLOOR |
| 45 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding.dropbox[number=*]` | `h3` | 4 | 4 | 0.30 of 64 | — | structure | yes | BELOW FLOOR |
| 46 | activity | MOVED | `div.col-12` | `h3` | `h3` | 9 | 3 | 0.12 of 64 | — | structure | — | BELOW FLOOR |
| 47 | activity | MISSING | `p>b` | `b` | `—` | 6 | 3 | 0.05 of 64 | — | 0.93 | — | BELOW FLOOR |
| 48 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `p` | 6 | 3 | 0.77 of 64 | — | structure | — | BELOW FLOOR |
| 49 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 5 | 3 | 1.00 of 64 | — | structure | — | BELOW FLOOR |
| 50 | activity | EXTRA | `div.col-12` | `—` | `div.audioImage` | 5 | 3 | 0.86 of 64 | — | structure | — | BELOW FLOOR |
| 51 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.alertActivity` | 5 | 3 | 0.77 of 64 | — | structure | yes | BELOW FLOOR |
| 52 | activity | SUBSTITUTED | `div.col-12` | `div.row` | `audio.audioPlayer.icon` | 4 | 3 | 0.55 of 64 | — | structure | yes | BELOW FLOOR |
| 53 | activity | EXTRA | `div.col-12` | `—` | `div.row` | 3 | 3 | 0.45 of 64 | — | structure | — | BELOW FLOOR |
| 54 | activity | MISSING | `div.col-12` | `div.ratio.ratio-16x9.videoSection` | `—` | 3 | 3 | 0.17 of 64 | — | structure | yes | BELOW FLOOR |
| 55 | activity | MOVED | `div.col-12` | `p>b` | `p>b` | 3 | 3 | 0.19 of 64 | — | structure | — | BELOW FLOOR |
| 56 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding.dropbox[number=*]` | `div.activity.interactive[number=*]` | 3 | 3 | 0.30 of 64 | — | structure | yes | BELOW FLOOR |
| 57 | activity | SUBSTITUTED | `ul` | `li` | `li` | 3 | 3 | 0.34 of 64 | — | structure | — | BELOW FLOOR |
| 58 | activity | SUBSTITUTED | `div.col-12` | `h3` | `audio.audioPlayer.icon` | 3 | 3 | 0.77 of 64 | — | structure | yes | BELOW FLOOR |
| 59 | activity | MISSING | `span.audioTrigger` | `img.audioText.img-fluid` | `—` | 7 | 2 | 0.11 of 64 | — | structure | — | BELOW FLOOR |
| 60 | activity | MOVED | `ul` | `li>b` | `li>b` | 6 | 2 | 0.09 of 64 | — | structure | — | BELOW FLOOR |
| 61 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `p>b` | 6 | 2 | 0.73 of 64 | — | structure | yes | BELOW FLOOR |
| 62 | activity | SUBSTITUTED | `div.col-12` | `h3` | `img.img-fluid` | 5 | 2 | 0.77 of 64 | — | structure | — | BELOW FLOOR |
| 63 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity.interactive[number=*]` | 5 | 2 | 0.28 of 64 | — | structure | yes | BELOW FLOOR |
| 64 | activity | MISSING | `b>span.sassoonI-text` | `span.sassoonI-text` | `—` | 3 | 2 | 0.03 of 64 | — | 1.00 | — | BELOW FLOOR |
| 65 | activity | MISSING | `div.col-12` | `div.audioImage` | `—` | 3 | 2 | 0.12 of 64 | — | structure | — | BELOW FLOOR |
| 66 | activity | MOVED | `div.col-12.col-md-8` | `p` | `p` | 3 | 2 | 0.09 of 64 | — | structure | — | BELOW FLOOR |
| 67 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.dropbox[number=*]` | `WIDGET` | 3 | 2 | 0.11 of 64 | — | structure | yes | BELOW FLOOR |
| 68 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 2 | 2 | 0.25 of 64 | — | structure | — | BELOW FLOOR |
| 69 | activity | MISSING | `div.row` | `div.col.paddingR` | `—` | 2 | 2 | 0.02 of 64 | — | 1.00 | yes | BELOW FLOOR |
| 70 | activity | MISSING | `div.col-12` | `a` | `—` | 2 | 2 | 0.45 of 64 | — | 0.50 | — | BELOW FLOOR |
| 71 | activity | MISSING | `div.row` | `div.col-12.col-md-8` | `—` | 2 | 2 | 0.20 of 64 | — | 0.50 | — | BELOW FLOOR |
| 72 | activity | MISSING | `div.activity.alertPadding.interactive[nu` | `div.row` | `—` | 2 | 2 | 0.02 of 64 | — | 0.50 | yes | BELOW FLOOR |
| 73 | activity | MISSING | `div.activity.dropbox[number=*]` | `div.row` | `—` | 2 | 2 | 0.12 of 64 | — | 0.50 | yes | BELOW FLOOR |
| 74 | activity | MISSING | `div.activity.interactive[number=*]` | `WIDGET` | `—` | 2 | 2 | 0.05 of 64 | — | structure | yes | BELOW FLOOR |
| 75 | activity | MOVED | `div.col-12.col-md-8` | `p>b` | `p>b` | 2 | 2 | 0.05 of 64 | — | structure | — | BELOW FLOOR |
| 76 | activity | MOVED | `div.col-12.col-md-12` | `p>b` | `p>b` | 2 | 2 | 0.03 of 64 | — | structure | yes | BELOW FLOOR |
| 77 | activity | MOVED | `div.col-12.col-md-12` | `p` | `p` | 2 | 2 | 0.06 of 64 | — | structure | yes | BELOW FLOOR |
| 78 | activity | SUBSTITUTED | `div.col-12` | `h3` | `div.table-responsive` | 2 | 2 | 0.77 of 64 | — | structure | — | BELOW FLOOR |
| 79 | activity | SUBSTITUTED | `div.activity.alertPadding.interactive[nu` | `div.row` | `WIDGET` | 2 | 2 | 0.17 of 64 | — | structure | yes | BELOW FLOOR |
| 80 | activity | SUBSTITUTED | `div.col-12.col-md-12` | `div.activity.interactive[number=*]` | `div.activity.interactive[number=*]` | 2 | 2 | 0.11 of 64 | — | structure | yes | BELOW FLOOR |
| 81 | activity | SUBSTITUTED | `div.activity.dropbox[number=*]` | `div.row` | `div#footer` | 2 | 2 | 0.12 of 64 | — | structure | yes | BELOW FLOOR |
| 82 | activity | SUBSTITUTED | `a` | `div.button` | `div.row` | 2 | 2 | 0.55 of 64 | — | structure | yes | BELOW FLOOR |
| 83 | activity | SUBSTITUTED | `a` | `div.button` | `div.col-12.col-md-8` | 2 | 2 | 0.55 of 64 | — | structure | yes | BELOW FLOOR |
| 84 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `WIDGET` | 2 | 2 | 0.28 of 64 | — | structure | yes | BELOW FLOOR |
| 85 | activity | SUBSTITUTED | `div.col-12` | `ul` | `p` | 2 | 2 | 0.41 of 64 | — | structure | — | BELOW FLOOR |
| 86 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `h4` | 2 | 2 | 0.73 of 64 | — | structure | yes | BELOW FLOOR |
| 87 | activity | SUBSTITUTED | `div.col-12` | `a` | `p>b` | 2 | 2 | 0.45 of 64 | — | structure | — | BELOW FLOOR |
| 88 | activity | SUBSTITUTED | `div.row` | `div.col-12.col-md-12` | `div.col-12` | 2 | 2 | 0.20 of 64 | — | structure | yes | BELOW FLOOR |
| 89 | activity | SUBSTITUTED | `ul` | `li` | `li>b` | 2 | 2 | 0.34 of 64 | — | structure | — | BELOW FLOOR |
| 90 | activity | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-6.offset-md-0` | 2 | 2 | 0.12 of 64 | — | structure | yes | BELOW FLOOR |
| 91 | activity | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `div.audioImage` | `div.audioImage` | 2 | 2 | 0.12 of 64 | — | structure | yes | BELOW FLOOR |
| 92 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `div.activity.interactive[number=*]` | 2 | 2 | 0.27 of 64 | — | structure | yes | BELOW FLOOR |
| 93 | activity | SUBSTITUTED | `div.col-12` | `p` | `WIDGET` | 2 | 2 | 0.77 of 64 | — | structure | — | BELOW FLOOR |
| 94 | activity | SUBSTITUTED | `div.col-12` | `div.audioImage` | `audio.audioPlayer.icon` | 2 | 2 | 0.14 of 64 | — | structure | yes | BELOW FLOOR |
| 95 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `audio.audioPlayer.icon` | 2 | 2 | 0.77 of 64 | — | structure | yes | BELOW FLOOR |
| 96 | activity | MISSING | `div.col-12` | `p.center-text.sassoonI-text` | `—` | 6 | 1 | 0.09 of 64 | — | 1.00 | — | BELOW FLOOR |
| 97 | activity | SUBSTITUTED | `div.col-12` | `h3` | `h3` | 4 | 1 | 0.77 of 64 | — | structure | — | BELOW FLOOR |
| 98 | activity | MISSING | `a` | `div.button.externalButton` | `—` | 3 | 1 | 0.05 of 64 | — | 1.00 | yes | BELOW FLOOR |
| 99 | activity | MISSING | `div.row` | `div.col-12.col-md-6.paddingR` | `—` | 3 | 1 | 0.03 of 64 | — | structure | yes | BELOW FLOOR |
| 100 | activity | MISSING | `div.row` | `div.col-12.col-md-6.paddingL` | `—` | 3 | 1 | 0.03 of 64 | — | structure | yes | BELOW FLOOR |
| 304 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 39 | 12 | 0.88 of 64 | series=TRR11 c=0.97 n=24 | structure | — | CANDIDATE |
| 306 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h3` | 30 | 11 | 0.83 of 64 | template=Bilingual c=0.83 n=30 | structure | — | CANDIDATE |
| 307 | body | EXTRA | `div.col-12.col-md-8` | `—` | `img.img-fluid` | 30 | 11 | 1.00 of 64 | template=Bilingual c=1.00 n=30 | structure | — | CANDIDATE |
| 308 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>b` | 31 | 9 | 0.95 of 64 | template=Bilingual c=0.95 n=31 | structure | — | CANDIDATE |
| 314 | body | EXTRA | `div#body` | `—` | `WIDGET` | 21 | 6 | 1.00 of 64 | template=Bilingual c=1.00 n=21 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #12 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 37 / modules 10 / lines 488; consensus (all) 0.66 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 10m/37p c=0.66
- by subject: Te Marautanga o Aotearoa TMoA 10m/37p c=0.66
- by era: Refresh 10m/37p c=0.66
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR102** TRR102_1_0.html ↔ TRR102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Say the sound, then click to check if you are right.»`
- **TRR106** TRR106_1_0.html ↔ TRR106_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Listen to the words below.»`
- **TRR108** TRR108_1_0.html ↔ TRR108_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «☒ Pānui»`
- modules: TRR102, TRR106, TRR108, TRR109, TRR110, TRR111, TRR112, TRR113, TRR114, TRR116

### #14 · activity · EXTRA · `p>b` › gold `—` vs Claude `b` — CANDIDATE
- pages 25 / modules 10 / lines 53; consensus (all) 0.89 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 10m/25p c=0.89
- by subject: Te Marautanga o Aotearoa TMoA 10m/25p c=0.89
- by era: Refresh 10m/25p c=0.89
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR102** TRR102_1_0.html ↔ TRR102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Whakaahuatia ngā oropuare.»`
- **TRR106** TRR106_1_0.html ↔ TRR106_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «ū roa»`
- **TRR108** TRR108_1_0.html ↔ TRR108_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «He aha tā tātou ako ai?»`
- modules: TRR102, TRR106, TRR108, TRR109, TRR110, TRR111, TRR112, TRR113, TRR114, TRR116

### #15 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 25 / modules 10 / lines 170; consensus (all) 0.95 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 10m/25p c=0.95
- by subject: Te Marautanga o Aotearoa TMoA 10m/25p c=0.95
- by era: Refresh 10m/25p c=0.95
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR102** TRR102_4_0.html ↔ TRR102_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Where is ‘A’?»`
- **TRR103** TRR103_1_0.html ↔ TRR103_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Where is ‘e’?»`
- **TRR108** TRR108_1_0.html ↔ TRR108_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Tōia te oro ki te orokati e tika ana.»`
- modules: TRR102, TRR103, TRR108, TRR109, TRR110, TRR111, TRR112, TRR113, TRR114, TRR116

### #16 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `img.img-fluid` — CANDIDATE
- pages 27 / modules 9 / lines 151; consensus (all) 1.00 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 9m/27p c=1.00
- by subject: Te Marautanga o Aotearoa TMoA 9m/27p c=1.00
- by era: Refresh 9m/27p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR102** TRR102_4_0.html ↔ TRR102_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **TRR108** TRR108_1_0.html ↔ TRR108_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **TRR109** TRR109_2_0.html ↔ TRR109_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- modules: TRR102, TRR108, TRR109, TRR110, TRR111, TRR112, TRR113, TRR114, TRR116

### #18 · activity · SUBSTITUTED · `div.col-12` › gold `p` vs Claude `p` — CANDIDATE
- pages 21 / modules 9 / lines 93; consensus (all) 0.77 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 9m/21p c=0.77
- by subject: Te Marautanga o Aotearoa TMoA 9m/21p c=0.77
- by era: Refresh 9m/21p c=0.77
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR102** TRR102_1_0.html ↔ TRR102_1.0.html (structure, derivable=True)
  - gold: `p  «He nui ngā oro katoa I tō tatou taiao.»`
  - Claude: `p  «Did you know that every word in te reo Maori ends with a vowel?»`
- **TRR103** TRR103_1_0.html ↔ TRR103_1.0.html (structure, derivable=True)
  - gold: `p  «Me whakatā tātou. Anei tētahi waiata oropuare hei waiata tahi mā tātou. Whakarongo ki te waiata, ka ako ana koe i te wai»`
  - Claude: `p  «Ko te tikanga o te kupu ko ‘some’. ēkara – Some eagles.»`
- **TRR106** TRR106_1_0.html ↔ TRR106_1.0.html (structure, derivable=True)
  - gold: `p  «Kua mātakitaki, kua ako hoki tātou i te maha o ngā waiata ō ēnei akoranga oropuare.»`
  - Claude: `p  «Do you have a favourite?»`
- modules: TRR102, TRR103, TRR106, TRR109, TRR110, TRR111, TRR112, TRR113, TRR116

### #20 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 30 / modules 8 / lines 70; consensus (all) 0.83 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 8m/30p c=0.83
- by subject: Te Marautanga o Aotearoa TMoA 8m/30p c=0.83
- by era: Refresh 8m/30p c=0.83
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR108** TRR108_1_0.html ↔ TRR108_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **TRR109** TRR109_1_0.html ↔ TRR109_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **TRR110** TRR110_1_0.html ↔ TRR110_1_0_ea.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: TRR108, TRR109, TRR110, TRR111, TRR112, TRR113, TRR114, TRR116

### #23 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `audio.audioPlayer.icon` — CANDIDATE
- pages 25 / modules 7 / lines 247; consensus (all) 1.00 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 7m/25p c=1.00
- by subject: Te Marautanga o Aotearoa TMoA 7m/25p c=1.00
- by era: Refresh 7m/25p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:383 — <audio preload="none" class="audioPlayer" title="...">
  - KB: INDEX.md:166 — - **`14_SUBJECT_GLOBAL_PARAMETERS/14C_LANGUAGES_AV_ASSET_REGISTRY.md`** (17 KB) — The complete Languages Audiovisual Package asset registry, absorbed 
  - KB: INDEX.md:167 — - Sections: 14C — Languages Audiovisual Package: the complete asset registry · 1. Delivery forms (the supplied markup shapes) · 2. Language icons · 3.
- **TRR109** TRR109_1_0.html ↔ TRR109_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `audio.audioPlayer.icon`
- **TRR110** TRR110_1_0.html ↔ TRR110_1_0_ea.html (structure, derivable=True)
  - gold: `—`
  - Claude: `audio.audioPlayer.icon`
- **TRR111** TRR111_1_0.html ↔ TRR111_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `audio.audioPlayer.icon`
- modules: TRR109, TRR110, TRR111, TRR112, TRR113, TRR114, TRR116

### #304 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 39 / modules 12 / lines 316; consensus (all) 0.88 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 12m/39p c=0.88
- by subject: Te Marautanga o Aotearoa TMoA 12m/39p c=0.88
- by era: Refresh 12m/39p c=0.88
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR102** TRR102_1_0.html ↔ TRR102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Sir James Hēnare»`
- **TRR103** TRR103_1_0.html ↔ TRR103_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Tā Hemi Hēnare»`
- **TRR106** TRR106_1_0.html ↔ TRR106_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Sir James Hēnare»`
- modules: TRR102, TRR103, TRR106, TRR107, TRR108, TRR109, TRR110, TRR111, TRR112, TRR113, TRR114, TRR116

### #306 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `h3` — CANDIDATE
- pages 30 / modules 11 / lines 59; consensus (all) 0.83 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 11m/30p c=0.83
- by subject: Te Marautanga o Aotearoa TMoA 11m/30p c=0.83
- by era: Refresh 11m/30p c=0.83
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR102** TRR102_0_0.html ↔ TRR102_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Introduction»`
- **TRR103** TRR103_0_0.html ↔ TRR103_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «TRR103 The vowels: Ee | Ngā Oropuare: Ee»`
- **TRR106** TRR106_1_0.html ↔ TRR106_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Proverb»`
- modules: TRR102, TRR103, TRR106, TRR107, TRR108, TRR109, TRR110, TRR111, TRR112, TRR113, TRR116

### #307 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `img.img-fluid` — CANDIDATE
- pages 30 / modules 11 / lines 111; consensus (all) 1.00 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 11m/30p c=1.00
- by subject: Te Marautanga o Aotearoa TMoA 11m/30p c=1.00
- by era: Refresh 11m/30p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR102** TRR102_1_0.html ↔ TRR102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **TRR103** TRR103_1_0.html ↔ TRR103_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **TRR106** TRR106_1_0.html ↔ TRR106_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- modules: TRR102, TRR103, TRR106, TRR107, TRR108, TRR109, TRR110, TRR111, TRR112, TRR113, TRR116

### #308 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 31 / modules 9 / lines 136; consensus (all) 0.95 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 9m/31p c=0.95
- by subject: Te Marautanga o Aotearoa TMoA 9m/31p c=0.95
- by era: Refresh 9m/31p c=0.95
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR102** TRR102_1_0.html ↔ TRR102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «a e i o u»`
- **TRR103** TRR103_2_0.html ↔ TRR103_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «He wā pai tēnei ki te parakatihi tuhi me te hanga hoki i a .»`
- **TRR106** TRR106_1_0.html ↔ TRR106_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Mēnā he ingoa te kupu, ingoa tangata, ingoa wāhi, ingoa mōkai rānei, me whakamahi i au, i a i te tīmatanga.»`
- modules: TRR102, TRR103, TRR106, TRR109, TRR110, TRR111, TRR112, TRR113, TRR116

### #314 · body · EXTRA · `div#body` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 21 / modules 6 / lines 45; consensus (all) 1.00 of 64 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Bilingual 6m/21p c=1.00
- by subject: Te Marautanga o Aotearoa TMoA 6m/21p c=1.00
- by era: Refresh 6m/21p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **TRR102** TRR102_1_0.html ↔ TRR102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **TRR103** TRR103_1_0.html ↔ TRR103_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **TRR106** TRR106_1_0.html ↔ TRR106_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: TRR102, TRR103, TRR106, TRR107, TRR110, TRR116
