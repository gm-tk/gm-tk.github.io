#!/usr/bin/env python3
"""ROUND 455 (DECLINED) — LOOP_STATE.md edits: clear the in-flight marker, the Declined-classes entry, the round-log line, the
follow-up pointer, and MOVE the round's PICK section to the archive. A .pre-r455-declined.bak is kept. Run under WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(P, P + ".pre-r455-declined.bak")
s = io.open(P, encoding="utf-8").read(); L = s.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
i = find("- **ROUND 455 IN FLIGHT — NOT PROVEN**"); j = find("- Before r455: **no round in flight**"); assert j == i + 1
L[i:j + 1] = ["- **No round in flight** (24 Sept 2026 09:30, session 41 Round 3 — r455 BUILT, PROBED, DECLINED and REVERTED: engine = HEAD caae7e0 (git clean), the in-memory corpus 3218 / 3218 byte-identical to disk; the work kept as `outputs/_r455_declined.patch`). LAST SHIPPED **r454** (260620.25); **LAST FULL = the r452 state**; ledger **scoped #2** since it."]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 41 Round 3 (24 Sept 09:22 → 09:30) — THE `Activity NX:` SECTION TABLE AS THE ACTIVITY BOX (KB 07B; engine r455 — BUILT, PROBED, DECLINED, REVERTED; `outputs/_r455_declined.patch` keeps the code) — below the 20-page body floor (19 pages / 4 modules: TRR102 / 103 / 106 / 116) and the §1d family-dialect exception is NOT met.** Three variants pre-scored (`outputs/_r455_prescore{,2,3}.log`): (a) box every label section — 13 up / 6 down, +114.2 pp-sum (TRR102's five lesson pages −3 to −17); (b) box only sections that gathered a widget — 10 up / 5 down, +45.4 (TRR103's widget-less sections, which its human DOES box, fell); (c) no box when the section's widget is a scanner-owned bundle — **14 up / 5 down, +121.9 pp-sum (≈ +0.049pp), ≥50 +5** (TRR102_4.0 −11.9, 2.0 −6.1, TRR116_5_0 −3.1, TRR103_1.0 −1.1, TRR116_8_0 −1.1). The human form is per-MODULE with no Writers-Template discriminator: TRR102 keeps every section's prose as a body row and boxes only the widget (4A / 4B / 4C); TRR106 / TRR116 box the whole section; TRR103 mixes both (1.0 widget-only, 2.0 / 3.0 whole section). KB 07B prescribes the section box and the gold agrees in the majority, so the (c) form is the right target — **re-open ONLY as a ride-along** with a TRR-lesson round already in scope (the patch applies to HEAD caae7e0), never alone under the floor.")
k = find("## Round log")
L.insert(k + 1, "- s41-r3 (engine r455 — BUILT, PROBED, DECLINED, REVERTED, 24 Sept 09:22 → 09:30) · THE `Activity NX:` SECTION TABLE AS THE ACTIVITY BOX (KB 07B; the r454 follow-up) · best variant 14 up / 5 down, +121.9 pp-sum (≈ +0.049pp), ≥50 +5 — but 19 pages / 4 modules is under the body floor and the family-dialect exception fails (TRR102's human boxes the widget alone; per-module, no discriminator) · reverted: engine = HEAD, 3218 / 3218 identical; `outputs/_r455_declined.patch` kept for a ride-along · see Declined classes.")
k = find("## Session 41 — Round 3 PICK (engine r455)") if any(l.startswith("## Session 41 — Round 3 PICK (engine r455)") for l in L) else None
if k is not None:
    e = k + 1
    while e < len(L) and not L[e].startswith("## "): e += 1
    block = L[k:e]
    io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 41 — Round 3 PICK (engine r455, DECLINED)\n\n" + "\n".join(block[1:]) + "\n")
    L[k:e] = ["## Session 41 — Round 3 (engine r455 — DECLINED, reverted) — THE `Activity NX:` SECTION BOX — the PICK is in LOOP_STATE_ARCHIVE.md 'Session 41 — Round 3 PICK (engine r455, DECLINED)'; the verdict is under Declined classes.", ""]
out = "\n".join(L); tmp = P + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, P)
print("LOOP_STATE.md", len(s.encode("utf-8")), "->", os.path.getsize(P))
