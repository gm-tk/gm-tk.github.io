import glob,re,io,collections,os
forms={'audio.audioPlayer.icon':r'<audio[^>]*class="[^"]*audioPlayer[^"]*icon','audio.audioPlayer(no icon)':r'<audio[^>]*class="audioPlayer"','audio other':r'<audio\b(?![^>]*audioPlayer)','div.audioImage':r'<div class="audioImage','span.audioTrigger':r'<span class="audioTrigger','div.audioSection':r'<div class="audioSection'}
for side,root in (("GOLD","01-Finalized_Modules_/Bilingual"),("CLAUDE","01-Claude_Modules_/Bilingual")):
    occ=collections.Counter(); pages=collections.defaultdict(set); mods=collections.defaultdict(set)
    for p in glob.glob(f'{root}/*/*.html'):
        h=io.open(p,encoding='utf-8',errors='replace').read(); mod=os.path.basename(os.path.dirname(p))
        for k,rx in forms.items():
            n=len(re.findall(rx,h))
            if n: occ[k]+=n; pages[k].add(p); mods[k].add(mod)
    print(side)
    for k in forms: print(f"   {k:28s} occ {occ[k]:4d} pages {len(pages[k]):3d} modules {len(mods[k]):3d} {sorted(mods[k])[:8] if k.startswith('div.audioImage') or k.startswith('span') else ''}")
for p in glob.glob('01-Finalized_Modules_/Bilingual/*/*.html'):
    h=io.open(p,encoding='utf-8',errors='replace').read(); i=h.find('class="audioImage')
    if i>0: print(p); print(re.sub(r'\s+',' ',h[i-300:i+600])); break
