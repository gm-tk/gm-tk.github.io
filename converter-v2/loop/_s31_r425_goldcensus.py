#!/usr/bin/env python3
"""_s31_r425_goldcensus.py — round 425: the XOTP golds' page shapes (header h1s, menu shell, section headings,
alert form, activity-box inner row, acks placement, footer) so the adapter targets the FAMILY convention.
Run under WSL from CONVERTER_V2/outputs: python3 _s31_r425_goldcensus.py"""
import os, re, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = os.path.join(HERE, "..", "..", "01-Finalized_Modules_", "Standard")
CODES = [l.strip() for l in open(os.path.join(HERE, "_affected_r425.txt")) if l.strip()]
C = collections.Counter
stats = collections.defaultdict(C)
for code in CODES:
    for f in sorted(glob.glob(os.path.join(GOLD, code, "*.html"))):
        h = open(f, encoding="utf-8", errors="replace").read()
        hdr = h.split('id="body"')[0]
        body = h.split('id="body"')[1] if 'id="body"' in h else ""
        stats["header_h1_spans"][len(re.findall(r"<h1>\s*<span>", hdr))] += 1
        stats["chip"][bool(re.search(r'id="module-code"', hdr))] += 1
        m = re.search(r'moduleMenu">\s*<div class="row">\s*<div class="([^"]+)">\s*(<div class="item">)?', hdr)
        stats["menu_first_col"][(m.group(1), bool(m.group(2))) if m else None] += 1
        stats["menu_heading_tags"][tuple(sorted(set(re.findall(r'<(h\d)><span>', hdr.split("moduleMenu")[-1] if "moduleMenu" in hdr else ""))))] += 1
        stats["menu_ul"][len(re.findall(r"<ul>", hdr.split("moduleMenu")[-1] if "moduleMenu" in hdr else ""))] += 1
        # section headings in body (outside activity boxes / alerts): h2 with span?
        stats["body_h2_span"][len(re.findall(r"<h2>\s*<span>", body))] += 1
        stats["body_h2_plain"][len(re.findall(r"<h2>(?!\s*<span>)", body))] += 1
        # alert
        for a in re.finditer(r'<div class="(col-[^"]+)"[^>]*>\s*<div class="alert">\s*(<div class="row">)?\s*(<div class="col-12">)?\s*<(h\d)>', body):
            stats["alert_col"][a.group(1)] += 1
            stats["alert_inner_row"][bool(a.group(2))] += 1
            stats["alert_title"][a.group(4)] += 1
        for a in re.finditer(r'<div class="alert">(.*?)</div>\s*</div>', body, flags=re.S):
            stats["alert_list"][("ol" if "<ol>" in a.group(1) else "ul" if "<ul>" in a.group(1) else "none")] += 1
        # activity box: inner row?
        for a in re.finditer(r'<div class="activity[^"]*" number="[^"]*">\s*(<div class="row">)?', body):
            stats["activity_inner_row"][bool(a.group(1))] += 1
        stats["activity_count_per_page"][len(re.findall(r'<div class="activity[^"]*" number=', body))] += 1
        stats["acks_on_page"][(os.path.basename(f).split("_")[1], bool(re.search(r'class="acks', body)))] += 1
        stats["footer"][tuple(re.findall(r'<a[^>]*(?:id="([a-z-]+)"|class="([a-z-]+)")', body.split("footer")[-1]))[:3]] += 1
        stats["table_responsive"][len(re.findall(r'table-responsive', body))] += 1
        stats["h3_after_activity_open"][len(re.findall(r'number="[^"]*">\s*<h3>', body))] += 1
for k, v in stats.items():
    print(f"{k}: {dict(v)}")
