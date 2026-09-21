"""_s31_r425_lead.py — round 425: the questions title rides INSIDE the alert's red span (the callout's embedded lead)."""
import io, os
JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2", "app", "js")
p = os.path.join(JS, "DocxExtractor.js"); s = io.open(p, encoding="utf-8", newline="").read()
old = """			push(TAG(ad.alert_tag ?? "alert") + (asLead ? t : ""), links);"""
new = """			push(asLead ? RED(`[${ad.alert_tag ?? "alert"}] ${t}`) : TAG(ad.alert_tag ?? "alert"), links);   // the lead INSIDE the span"""
assert s.count(old) == 1; s = s.replace(old, new); io.open(p, "w", encoding="utf-8", newline="").write(s); print("patched")
