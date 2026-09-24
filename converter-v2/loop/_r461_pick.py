#!/usr/bin/env python3
"""r461 PICK write: raise the in-flight marker + insert the Round 9 PICK section into LOOP_STATE.md (line edits only)."""
import io, os
P = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/LOOP_STATE.md"
s = io.open(P, encoding="utf-8", newline="").read()
old = s[s.index("- **No round in flight** (24 Sept 2026 ≈11:50, session 41 Round 8"):]
old = old[:old.index("\n") + 1]
new = ("- **ROUND 9 (engine r461) IN FLIGHT — NOT PROVEN** (24 Sept 2026 ≈12:00, session 41): THE AUDIO-IMAGE PHONICS GRID "
       "(KB 01E `[audio image]` → `div.audioImage > div#{audio}.audioImageOption > img`) — re-test of the r135 build parked "
       "default-off for its nesting (`Emit_Templates.elements.dual_language.audio_image`, `ContentConverter.#bilingualAudioImage`). "
       "Files: `data/Emit_Templates.json` (+ `ContentConverter.js` if the nesting needs a repair), `app/js/Config.js`. Data flag "
       "`audio_image.enabled`; env **`AUDIOIMG_OFF`**. LAST SHIPPED **r460** (260620.30); LAST FULL = r460; ledger scoped #0.\n")
s = s.replace(old, new, 1)
anchor = "## Session 41 — Round 8 (engine r460, build 260620.30)"
pick = ("## Session 41 — Round 9 PICK (engine r461) — THE AUDIO-IMAGE PHONICS GRID (the r135 park re-tested)\n"
        "- **Lane:** the loss ledger's largest low family (the r453 follow-up: TRR — 76 pages, mean 40.4 %, 49 pages at 10–39 %; "
        "`outputs/_s41_r9_skdiff.py`). The TRR112 3.0 diff (31 %): the gold's `div.audioImage > div#{name}.audioImageOption > "
        "img` grids are Claude's `audio.audioPlayer.icon` + `img` pairs; gold `div.audioImage` on **111 pages / 31 modules** (TRR 12, "
        "PWY1009 / 1008, FRFUN06, ENGC302, GENO901, XMES…), Claude 0. **Authority:** KB 01E `[audio image]` → the audioImage form "
        "(§1b rank 1) + the gold. The build exists (r135, `#bilingualAudioImage`) but was parked for nesting (a bare top-level row, "
        "−1.41 on TRR102) before the r135-v2 / r451 section nesting shipped. **Step 1:** flip the flag in memory, probe, pre-score; "
        "ship if the population rises, else repair the nesting (≤ 3 attempts) or decline.\n\n")
s = s.replace(anchor, pick + anchor, 1)
io.open(P + ".tmp", "w", encoding="utf-8", newline="").write(s)
assert os.path.getsize(P + ".tmp") > 90000; os.replace(P + ".tmp", P)
print("ok", len(s))
