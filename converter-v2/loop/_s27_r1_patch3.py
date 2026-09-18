
import re
s = open("_s27_r1_videoicon3.py", encoding="utf-8").read()
s = s.replace("""gm = defaultdict(lambda: [0, 0]); pages_of = defaultdict(set)
for code, pg, gI, gP, cI, cP in rows:
    gm[code][0] += gI; gm[code][1] += gP; pages_of[code].add(pg)""",
"""gm = defaultdict(lambda: [0, 0]); pages_of = defaultdict(set)
for code, pg, gI, gP, cI, cP in rows:
    gm[code][0] += gI; gm[code][1] += gP; pages_of[code].add(pg)
# the MINING population = every gold video incl. the widget-embedded ones (the r200 rule mined all videos)
full = json.load(open(os.path.join(OUTPUTS, "_s27_r1_videoicon.json")))
gfull = {c: (sum(v["gi"].values()), sum(v["gp"].values())) for c, v in full.items()}""")
s = s.replace("""    a = defaultdict(lambda: [0, 0, 0])
    for code, (gI, gP) in gm.items():""", """    a = defaultdict(lambda: [0, 0, 0])
    for code, (gI, gP) in gfull.items():""")
s = s.replace("""    icon_series = {k for k, (sh, n, a, b) in S.items() if n >= n_series and sh >= s_icon_series}
    plain_series = {k for k, (sh, n, a, b) in S.items() if n >= n_series and sh <= s_plain_series} if carve else set()
    icon_st = {k for k, (sh, n, a, b) in ST.items() if n >= n_st and sh >= s_icon_st}""",
"""    icon_series = ICON_SERIES | {k for k, (sh, n, a, b) in S.items() if n >= n_series and sh >= s_icon_series}
    plain_series = ({k for k, (sh, n, a, b) in S.items() if n >= n_series and sh <= s_plain_series} - ICON_SERIES) if carve else set()
    icon_st = ICON_ST | {k for k, (sh, n, a, b) in ST.items() if n >= n_st and sh >= s_icon_st}""")
open("_s27_r1_videoicon3.py", "w", encoding="utf-8").write(s)
print("patched")
