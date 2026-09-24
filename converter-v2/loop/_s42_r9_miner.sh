#!/usr/bin/env bash
# Session 42 Round 9 — the scoped miner over one family (codes file as $1, output tag as $2). WSL.
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
python3 _diff_miner.py $(cat $O/$1) > $O/_s42_r9_miner_$2.log 2>&1
cp $O/_diff_miner_scoped.md $O/_s42_r9_miner_$2.md
tail -1 $O/_s42_r9_miner_$2.log
