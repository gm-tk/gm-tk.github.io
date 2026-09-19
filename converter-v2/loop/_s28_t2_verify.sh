#!/usr/bin/env bash
# SESSION 28 / TASK 2 — prove the V1 parser message change: re-parse the 12 XOTP Writers Templates + controls (PMT101 / PNR107 /
# TRR102 Media List — genuine no-[TITLE BAR] documents that must KEEP the warning; SCCH301 / WJFUN105 — normal documents that
# must be byte-identical) into a scratch dir and diff against the corpus _parsed.txt. WSL, from anywhere.
cd "$(dirname "$0")" || exit 1
ROOT=../..
S=_s28_t2_parsed; mkdir -p $S
G=$ROOT/01-Finalized_Modules_
pairs=(
  "Standard/XOTPB08" "Standard/XOTPB09" "Standard/XOTPB10" "Standard/XOTPB11" "Standard/XOTPB12" "Standard/XOTPB13"
  "Standard/XOTPG01" "Standard/XOTPG03" "Standard/XOTPG04" "Standard/XOTPG05" "Standard/XOTPG06" "Standard/XOTPO01"
  "Bilingual/PMT101" "Bilingual/PNR107" "Standard/SCCH301" "Fundamentals/WJFUN105"
)
for p in "${pairs[@]}"; do
  c=${p##*/}
  for kind in "Writers Template" "Media List" "Writers Template + Media List"; do
    in="$G/$p/$c $kind.docx"; [ -f "$in" ] || continue
    ref="$G/$p/$c ${kind}_parsed.txt"
    out="$S/$c ${kind}_parsed.txt"
    node parse_docx.cjs "$in" "$out" > /dev/null 2>&1 || { echo "$c $kind: PARSE FAILED"; continue; }
    if cmp -s "$out" "$ref"; then echo "$c [$kind]: byte-identical to the corpus parsed txt"; else
      echo "$c [$kind]: differs — $(diff "$ref" "$out" | grep -c '^[<>]') line(s):"; diff "$ref" "$out" | grep '^[<>]' | cut -c1-150; fi
  done
done
# the TRR102 Media List (a no-[TITLE BAR] control)
in="$G/Bilingual/TRR102/TRR102 Media List.docx"; out="$S/TRR102 Media List_parsed.txt"; ref="$G/Bilingual/TRR102/TRR102 Media List_parsed.txt"
[ -f "$in" ] && { node parse_docx.cjs "$in" "$out" > /dev/null 2>&1; cmp -s "$out" "$ref" && echo "TRR102 [Media List]: byte-identical" || { echo "TRR102 [Media List]: differs"; diff "$ref" "$out" | grep '^[<>]' | cut -c1-150; }; }
