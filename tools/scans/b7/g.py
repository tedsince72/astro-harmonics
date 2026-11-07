import json,re,glob,collections
Rs=json.load(open('docs/eddie_read/results/results.json'))
def sc(t):
    m=re.search(r'\(([\d.]+)\)\s*$',t.strip()); return float(m.group(1)) if m else 0.0
def horse(n): return n.split(' / ')[0].split(' ',1)[1].strip()
def topline(d,C):
    L=[l for l in d['sky']['lines'] if l.startswith(C+' →')]; return max(L,key=sc) if L else None
FILT={}
def f_topline(C):
    def f(d,p):
        t=topline(d,C)
        return any(sc(x.split(' = ')[0])>=50 and x.split(' = ')[1].strip()==t for c in p['cases']['3'] for x in c['cells'])
    return f
for C in ('S Moon','S Sun','S Jupiter'): FILT[f'natal cell >= 50 on the number of the top {C} line']=f_topline(C)
def f_any_top(d,p): return any(f_topline(C)(d,p) for C in ('S Moon','S Sun','S Jupiter'))
FILT['... top line of any centre']=f_any_top
def sunstar_venus(d,p):
    return any(c['layer']=='star rows' and sc(c['text'])>=50 and any(s.startswith('S Sun →') for s in c['source_lines']) for b in p['bodies'] if b['body']=='Venus' for c in b['cells'])
FILT['a Sun-line star on natal Venus >= 50']=sunstar_venus
for name,f in FILT.items():
    tot=collections.Counter(); ch=collections.Counter()
    per=[]
    for fn in sorted(glob.glob('docs/eddie_read/*_layers.json')):
        race=fn.split('race_batch_')[1].replace('_layers.json','')
        rs=Rs[race]; nr=set(rs.get('nonrunners',[])); d=json.load(open(fn))
        sel=[horse(p['name']) for p in d['report'].values() if horse(p['name']) not in nr and f(d,p)]
        W=set(rs['first']); T=W|set(rs['second'])
        part='in' if race in ('20261106_aintree_1240','20261106_aintree_1315') else 'test'
        tot[part+' picks']+=len(sel); tot[part+' won']+=sum(h in W for h in sel); tot[part+' 1/2']+=sum(h in T for h in sel)
        tot[part+' exact12']+= set(sel)==T; ch[part+' w']+=len(sel)/rs['ran']; ch[part+' 2']+=len(sel)*len(T)/rs['ran']
        if part=='in': per.append((race[-4:],sel))
    print(name); print('   12:40 / 13:15:',per)
    print(f"   other 18 races: {tot['test picks']} picks, {tot['test won']} won (chance {ch['test w']:.1f}), {tot['test 1/2']} 1st/2nd (chance {ch['test 2']:.1f}), exact 1st+2nd {tot['test exact12']}")
