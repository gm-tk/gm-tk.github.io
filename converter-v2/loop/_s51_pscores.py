#!/usr/bin/env python3
"""_s51_pscores.py — the per-page skeleton scores of a module prefix, lowest first. argv: sk_final.json PREFIX"""
import json, sys
d = json.load(open(sys.argv[1]))["per_page"]
x = sorted((p for p in d if p["module"].startswith(sys.argv[2])), key=lambda p: p["scaffold"])
print(" ".join(f'{p["page"]}:{p["scaffold"] * 100:.0f}' for p in x))
