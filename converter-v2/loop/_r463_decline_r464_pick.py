#!/usr/bin/env python3
"""r463 DECLINED record + Needs Chris #21 (the Merge-item lessons) + the r464 PICK / in-flight marker. Line edits only;
.pre-r463-decline.bak kept. Run under WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-r463-decline.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8"))
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
i = find("- **ROUND 11 (engine r463) IN FLIGHT — NOT PROVEN**"); marker11 = L[i]
L[i] = ("- **ROUND 12 (engine r464) IN FLIGHT — NOT PROVEN** (24 Sept 2026 ≈14:25, session 41): THE UNTAGGED `Merge item N` "
        "LESSON LINE — a recognition round: the writer's whole-paragraph `Merge item 7` (the lesson's content lives in merged "
        "material outside the document — CHI1003 / 1004 / 1005, JPN1004: 30 lesson pages) takes the r300 merge To-Do note "
        "(`asset_todo_notes`, the `merge` family) instead of shipping as a bare `<p>Merge item 7</p>`. Files: "
        "`app/js/ContentConverter.js`, `data/Emit_Templates.json`, `app/js/Config.js`. Data flag `asset_todo_notes.black_line`; "
        "env **`TODOMERGELINE_OFF`**. Before it: r463 DECLINED (reverted, tree clean at dd4abba). LAST SHIPPED **r461** "
        "(260620.31); LAST FULL = r460; ledger scoped #1; plateau 2 of 3.")
p0 = find("## Session 41 — Round 11 PICK (engine r463)"); p1 = p0 + 1
while p1 < len(L) and not L[p1].startswith("## "): p1 += 1
pick11 = L[p0:p1]
L[p0:p1] = ["## Session 41 — Round 12 PICK (engine r464) — THE UNTAGGED `Merge item N` LESSON LINE (a recognition round)",
            "- **Lane:** the loss ledger's family ranking (`_r461_sk_final.json` by family: TRR 0.428pp, MXFL 0.282, **CHI 0.225** "
            "at 26 pages / mean 33.1 %). **Triangulated:** CHI1003's WT lessons 1–8 are each `[LESSON N]` → `[Lesson content]` → "
            "the black line `Merge item N` and nothing else (the docx holds no embedded or linked part — `word/embeddings` empty); "
            "the gold lessons are full pages; Claude's are one `<p>Merge item 7</p>` (1,284 bytes). The same form: CHI1004 (8), "
            "CHI1005 (7), JPN1004 (7) — **30 lesson pages / 4 modules whose content is not in the input** (→ Needs Chris #21). "
            "The r300 `asset_todo_notes` merge family already turns a TAGGED `[Merge item N]` into the designer To-Do note; the "
            "untagged whole-paragraph line never reaches it. **Authority:** r300's own rule (KB 12 deferred-item red-note "
            "convention). **Prediction:** gate-neutral by design (one `p` becomes one note `p` on pages that are otherwise empty) — "
            "neither counts toward nor resets the plateau window.",
            ""]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 41 Round 11 (24 Sept ≈13:40 → 14:05) — THE TILE'S \"Year N\" LEARNING LEADS (engine r463 — BUILT, PROBED, "
         "DECLINED on the floor, REVERTED; `outputs/_r463_declined.patch`).** `tile_pages.year_lead` (a \"Year 3 Learning "
         "Intention\" / \"Year 3 Success Criteria\" label line opens its side of a `[Lesson Overview]` run): correct, but it moves "
         "ONE page (WJFUN116_0_0 +0.2) — the form is WJFUN116's alone (WJFUN112 has one label, WJFUN206's `[Lesson Overview]` + "
         "`[Learning Intentions]` TAG form is another single module). The 11 WJFUN modules with an empty 'Learning Intentions' "
         "menu pane each have their own authoring form; none reaches the 10-module chrome floor. Re-open only as one WJFUN "
         "family round that covers every form together.")
k = find("20. **24 Sept (session 41 Round 1, r453)**")
L.insert(k + 1, "21. **24 Sept (session 41 Round 12)** — **the `Merge item N` lessons: where is their content?** CHI1003, CHI1004, "
         "CHI1005 and JPN1004 write every lesson as `[Lesson content]` + one line `Merge item N` (30 lesson pages); the docx holds "
         "nothing else, but the human pages are full lessons (they had the merged material). The converter cannot build them: "
         "supply the merge items (or the stitched Writers Template) and the loop converts them; or record them as no-source pages "
         "(like the 7 no-source modules) so the gate stops counting them — **holds 30 pages (≈ 0.3pp of the skeleton mean)**. "
         "Recommendation: supply the source if it exists; otherwise exclude.")
k = find("## Round log")
L.insert(k + 1, "- s41-r11 (engine r463, 24 Sept ≈13:40 → ≈14:05) · THE TILE'S \"Year N\" LEARNING LEADS (WJFUN) · DECLINED on the "
         "floor (1 page, WJFUN116 +0.2; every empty-pane module has its own form) · reverted, tree clean · also measured: crossed "
         "page pairs (`_s41_r12_crosspair.py`: 9 two-cycles, 4 better swapped, +25 pp-sum — not an instrument round) · plateau "
         "unchanged 2 of 3.")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 41 — Round 11 PICK (engine r463, DECLINED) + what it found\n\n"
    + "\n".join(pick11).rstrip() + "\n" + marker11 + "\n- **Verdict:** DECLINED on the floor — see Declined classes (s41-r11). The "
    "files were restored (Emit_Templates from `outputs/_r462_ET_pre.json`, ContentConverter from `git show HEAD:`); `git status` clean.\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", n0, "->", os.path.getsize(S))
