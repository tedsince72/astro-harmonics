# A natal body reached by a sky centre directly and by that centre's line stars, same chart.
import json,re,glob,collections,sys
R=json.load(open('docs/eddie_read/results/results.json'))
def sc(t):
    m=re.search(r'\(([\d.]+)\)\s*$',t); return float(m.group(1)) if m else 0.0
def horse(n): return n.split(' / ')[0].split(' ',1)[1].strip()
def hits(p,C,dmin,smin,nstars):
    out=[]
    for b in p['bodies']:
        for ch in 'HJ':
            direct=[c['text'] for c in b['cells'] if c['layer']=='top rows' and c['text'].startswith(f'{C} → {ch} {b["body"]} ') and sc(c['text'])>=dmin]
            stars=collections.defaultdict(list)
            for c in b['cells']:
                m=re.match(rf'{ch} (.+?) → {ch} ',c['text'])
                if c['layer']=='star rows' and m and sc(c['text'])>=smin and any(s.startswith(C+' →') for s in c['source_lines']):
                    stars[m.group(1)].append(c['text'])
            if direct and len(stars)>=nstars: out.append((ch,b['body'],direct,dict(stars)))
    return out
VAR=[('S Jupiter',50,50,2),('S Jupiter',50,50,1),('S Jupiter',80,80,1),('S Sun',50,50,2),('S Sun',80,80,1),('either',50,50,2)]
for C,dm,sm,ns in VAR:
    tot=collections.Counter(); ch=0.0; c2=0.0; show=[]
    for fn in sorted(glob.glob('docs/eddie_read/*_layers.json')):
        race=fn.split('race_batch_')[1].replace('_layers.json','')
        rs=R[race]; nr=set(rs.get('nonrunners',[])); d=json.load(open(fn))
        sel=[]
        for p in d['report'].values():
            h=horse(p['name'])
            if h in nr: continue
            cs=['S Jupiter','S Sun'] if C=='either' else [C]
            hh=[x for c0 in cs for x in hits(p,c0,dm,sm,ns)]
            if hh: sel.append(h); 
            if hh and race.endswith('fontwell_1435'): show.append((h,hh))
        W=set(rs['first']); T=W|set(rs['second'])
        part='in' if race=='20261106_fontwell_1435' else 'test'
        if part=='in': inrace=sel; continue
        tot['p']+=len(sel); tot['w']+=sum(h in W for h in sel); tot['t']+=sum(h in T for h in sel); tot['f']+=bool(sel)
        ch+=len(sel)/rs['ran']; c2+=len(sel)*len(T)/rs['ran']
    print(f'{C} direct>={dm}, {ns}+ line stars >={sm}: Fontwell picks {inrace} | other 19 races: {tot["p"]} picks in {tot["f"]} races, {tot["w"]} won ({ch:.1f}), 1st/2nd {tot["t"]} ({c2:.1f})')
    if C=='S Jupiter' and ns==2:
        for h,hh in show:
            for x in hh: print('    ',h,x)
