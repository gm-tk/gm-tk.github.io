import io
s = io.open("_s27_r6_goldboxes.py", encoding="utf-8", newline="").read()
s = s.replace("THE GOLD'S EXTRA ACTIVITY BOXES (529 lesson pages where the gold ships more top-level boxes than Claude)", "CLAUDE'S EXTRA ACTIVITY BOXES (287 lesson pages where Claude ships more top-level boxes than the gold) — the mirror of _s27_r6_goldboxes.py")
s = s.replace("For every gold top-level activity box whose first heading text is NOT the first heading of any Claude box on the paired page", "For every Claude top-level activity box whose first heading text is NOT the first heading of any gold box on the paired page")
s = s.replace("wsl: python3 _s27_r6_goldboxes.py", "wsl: python3 _s27_r6_claudeboxes.py")
# swap the roles in the main loop
s = s.replace("        if len(gb) <= len(cb): continue\n        cheads = {first_heading(b)[1] for b in cb}", "        if len(cb) <= len(gb): continue\n        cheads = {first_heading(b)[1] for b in gb}")
s = s.replace("        walk(ct.root, cw)\n        for b in gb:", "        walk(gt.root, cw)\n        for b in cb:")
s = s.replace('print(f"gold extra boxes on gold-more lesson pages: {TOT}")', 'print(f"claude extra boxes on claude-more lesson pages: {TOT}")')
s = s.replace('print("Claude\'s rendering of the box\'s heading:"', 'print("the gold\'s rendering of the box\'s heading:"')
s = s.replace('# Claude\'s headings anywhere + their context', '# the gold\'s headings anywhere + their context')
s = s.replace('# the writer\'s opener for the heading where the parsed WT has it.', '# the box\'s first non-heading text so the writer\'s opener can be traced.')
s = s.replace('if len(EX[key]) < 3: EX[key].append(f"{code}/{os.path.basename(cp)} #{b.attrs.get(\'number\',\'\')} «{h[:36]}»")',
              'if len(EX[key]) < 3: EX[key].append(f"{code}/{os.path.basename(cp)} #{b.attrs.get(\'number\',\'\')} «{h[:36]}» first=«{ftext(b)[:50]}»")')
io.open("_s27_r6_claudeboxes.py", "w", encoding="utf-8", newline="").write(s); print("ok")
