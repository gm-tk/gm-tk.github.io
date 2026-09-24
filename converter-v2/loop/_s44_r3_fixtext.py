import io
p = "_r480_finalise.py"; s = io.open(p, encoding="utf-8").read()
reps = [
 ("**Measured and declined inside the round:** (B) the marker table's data rows as ONE hand-off (`data_rows_handoff`, the code kept, OFF) — +41.7 pp-sum on TRR116 but the gold prints those activity sentences as ordinary paragraphs; and (b)",
  "**Built but not shipped this round:** (B) the marker table's data rows as ONE hand-off (`data_rows_handoff`, the code in place, OFF) — pre-scored +41.7 pp-sum on TRR116 on top of (A); its own gate effect was not separated (the −80 below is the boxing's), so it is queued as its own round. **Measured and declined:** (b)"),
 ("Measured and DECLINED s44-r3: (b) the reo = eng identical pair (the gold ships it once 111 / twice 132); (B) the marker table's data rows as one hand-off (+41.7 pp-sum but compare_structure exact −80 — the gold prints those sentences as paragraphs; `data_rows_handoff` kept OFF).",
  "Measured and DECLINED s44-r3: (b) the reo = eng identical pair (the gold ships it once 111 / twice 132). NEXT: (B) the marker table's data rows as one hand-off — built in r480, OFF (`data_rows_handoff`), pre-scored +41.7 pp-sum on TRR116 — measure its own gate effect and ship it as its own round."),
 ("(c) the audio-word line `p.center-text.sassoonI-text` (98 in 4 modules, 84 of them TRR111 — one module's dialect, below floor); (B) the `[Activity: Embedded]` table's data rows as ONE hand-off (+41.7 pp-sum on TRR116, but compare_structure exact −80 — the gold prints the activity sentences as ordinary paragraphs beside its widget; code kept, `act_label_box.data_rows_handoff` false). Re-open (B) only with a split of the data rows the gold keeps as paragraphs vs the ones inside its widget.\")",
  "(c) the audio-word line `p.center-text.sassoonI-text` (98 in 4 modules, 84 of them TRR111 — one module's dialect, below floor).\")"),
 ("inside r480's PICK, three sub-classes of the TRR1 lesson lane DECLINED on measurement:", "inside r480's PICK, two sub-classes of the TRR1 lesson lane DECLINED on measurement:"),
 ("(+0.0779pp with (B)); (B) then declined on the cs gate (−80 either way — the −80 is the pool shrink of the boxing itself, (B) was not its cause). Shipped (A)",
  "(+0.0779pp with (B)); the scoped ship's cs exact −80 was the pool shrink of the boxing itself (it stayed −80 with (B) off), so (B) — whose own effect was not separated — is left OFF for its own round. Shipped (A)"),
]
for a, b in reps:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
io.open(p, "w", encoding="utf-8", newline="\n").write(s); print("finalise text fixed")
