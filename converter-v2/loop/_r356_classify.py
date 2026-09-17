"""_r356_classify.py — classify every page the r356 ON probe changed: visible text LOST / GAINED / DUPLICATED vs the disk page,
hand-off boxes gained (reverts) / lost (builds). Reads _r356_on/<code>/<page> vs 01-Claude_Modules_/*/<code>/<page>."""
import io, os, re, glob, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ON = os.path.join(HERE, "_r356_on"); CL = os.path.join(HERE, "..", "..", "01-Claude_Modules_")
def vis(html):
    h = re.sub(r"<!--[\s\S]*?-->", " ", html); h = re.sub(r"<script[\s\S]*?</script>", " ", h)
    h = re.sub(r'<p class="cv2-note"[^>]*>[\s\S]*?</p>', " ", h)          # notes are chrome
    h = re.sub(r"<(br|/p|/li|/h\d|/td|/th|/div)[^>]*>", "\n", h); h = re.sub(r"<[^>]+>", " ", h)
    h = re.sub(r"&[a-z#0-9]+;", " ", h)
    lines = [re.sub(r"[^\w]+", " ", l).strip().lower() for l in h.split("\n")]
    return [l for l in lines if len(l.split()) >= 3]
tot = collections.Counter(); rows = []
for code in sorted(os.listdir(ON)):
    for page in sorted(os.listdir(os.path.join(ON, code))):
        if not page.endswith(".html"): continue
        disk = glob.glob(os.path.join(CL, "*", code, page))
        if not disk: continue
        a = io.open(disk[0], encoding="utf-8").read(); b = io.open(os.path.join(ON, code, page), encoding="utf-8").read()
        if a == b: continue
        A, B = vis(a), vis(b); ca, cb = collections.Counter(A), collections.Counter(B)
        lost = [l for l in ca if cb[l] < ca[l]]; gained = [l for l in cb if cb[l] > ca[l]]
        dup = [l for l in cb if cb[l] > 1 and ca[l] <= 1 and cb[l] > ca[l]]
        boxes_a = len(re.findall(r'class="cv2-interactive cv2-int-ref"', a)); boxes_b = len(re.findall(r'class="cv2-interactive cv2-int-ref"', b))
        imgs = len(re.findall(r'<img class="img-fluid"', b)) - len(re.findall(r'<img class="img-fluid"', a))
        kind = "REVERT" if boxes_b > boxes_a else ("BUILD" if boxes_b < boxes_a else "RESTORE")
        tot[kind] += 1; tot["lost"] += len(lost); tot["gained"] += len(gained); tot["dup"] += len(dup); tot["imgs"] += imgs
        rows.append(f"{kind:7} {code:8} {page:22} lost {len(lost):2} gained {len(gained):2} dup {len(dup):2} boxes {boxes_a}->{boxes_b} imgs {imgs:+d}  | {(gained or lost or [''])[0][:70]}")
        for l in dup: rows.append(f"      DUP: {l[:100]}")
        for l in lost: rows.append(f"      LOST: {l[:100]}")
print("\n".join(rows)); print("pages", len([r for r in rows if not r.startswith("      ")]), dict(tot))
