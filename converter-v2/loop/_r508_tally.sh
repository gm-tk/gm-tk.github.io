#!/usr/bin/env bash
# ROUND 508 — hand-off labels and built widget roots, disk (OFF) vs the probe's ON pages
cd "$(dirname "$0")"
declare -A B A
for p in $(grep '\.html$' _r508_ON_pages.txt); do
  m=${p%%/*}; d=$(ls -d ../../01-Claude_Modules_/*/$m | head -1)
  for t in $(grep -o 'INTERACTIVE (un-built) #[0-9]*: [A-Za-z]*' $d/$(basename $p) </dev/null | sed 's/.*: //'); do B[box:$t]=$(( ${B[box:$t]:-0} + 1 )); done
  for t in $(grep -o 'INTERACTIVE (un-built) #[0-9]*: [A-Za-z]*' _r508_on/$p </dev/null | sed 's/.*: //'); do A[box:$t]=$(( ${A[box:$t]:-0} + 1 )); done
  for t in $(grep -o '<div class="\(dragAndDrop\|multiChoiceQuiz\|reorder\|radioQuiz\|dropQuiz\|typing\|selectionBox\|memoryGame\|wordFind\)[ "]' $d/$(basename $p) </dev/null | sed 's/<div class="//; s/[ "]$//'); do B[built:$t]=$(( ${B[built:$t]:-0} + 1 )); done
  for t in $(grep -o '<div class="\(dragAndDrop\|multiChoiceQuiz\|reorder\|radioQuiz\|dropQuiz\|typing\|selectionBox\|memoryGame\|wordFind\)[ "]' _r508_on/$p </dev/null | sed 's/<div class="//; s/[ "]$//'); do A[built:$t]=$(( ${A[built:$t]:-0} + 1 )); done
done
for k in $(printf '%s\n' "${!B[@]}" "${!A[@]}" | sort -u); do echo "$k ${B[$k]:-0} -> ${A[$k]:-0}"; done
