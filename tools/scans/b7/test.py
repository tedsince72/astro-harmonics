import json,re,glob,sys
R=json.load(open('docs/eddie_read/results/results.json'))
def sc(t):
    m=re.search(r'\(([\d.]+)\)\s*$',t); return float(m.group(1)) if m else 0.0
def horse(n): return n.split(' / ')[0].split(' ',1)[1].strip().lower()
def feats(p):
    f={}
    f['no_case1']=len(p['cases']['1'])==0
    f['no_case3']=len(p['cases']['3'])==0
    f['nH_sb']=sum(1 for x in p['same_bodies'] if '→ H' in x)
    f['n_sb']=len(p['same_bodies'])
    # D: same body >=50 and S Jupiter -> that body (either chart) >=80
    sbb={re.match(r'S (\S+(?: \S+)?) →',x).group(1) for x in p['same_bodies'] if sc(x)>=50}
    D=False;E=0
    for b in p['bodies']:
        for c in b['cells']:
            t=c['text']
            if c['layer']=='top rows' and t.startswith('S Jupiter →') and sc(t)>=80 and b['body'] in sbb: D=True
            if c['layer']=='top rows' and re.match(r'S \S+.* → J Jupiter',t) and sc(t)>=80: E+=1
    f['D']=D; f['E_Jjup80']=E
    return f
tot={}
for fn in sorted(glob.glob('docs/eddie_read/*_layers.json')):
    race=fn.split('race_batch_')[1].replace('_layers.json','')
    if race not in R: continue
    win={w.lower() for w in R[race]['first']}
    d=json.load(open(fn)); rows=[]
    for pk,p in d['report'].items():
        rows.append((horse(p['name']) in win, feats(p)))
    n=len(rows)
    out=[]
    for k in ['no_case1','no_case3','D']:
        sel=[w for w,f in rows if f[k]]; out.append(f'{k}:{sum(sel)}/{len(sel)}')
        tot.setdefault(k,[0,0,0.0]); tot[k][0]+=sum(sel); tot[k][1]+=len(sel); tot[k][2]+=len(sel)/n
    for k,fn2 in [('fewest_H_sb',lambda f:f['nH_sb']),('fewest_sb',lambda f:f['n_sb'])]:
        m=min(fn2(f) for w,f in rows); sel=[w for w,f in rows if fn2(f)==m]
        out.append(f'{k}:{sum(sel)}/{len(sel)}'); tot.setdefault(k,[0,0,0.0]); tot[k][0]+=sum(sel); tot[k][1]+=len(sel); tot[k][2]+=len(sel)/n
    m=max(f['E_Jjup80'] for w,f in rows); sel=[w for w,f in rows if f['E_Jjup80']==m and m>0]
    out.append(f'most_Jjup80:{sum(sel)}/{len(sel)}'); tot.setdefault('most_Jjup80',[0,0,0.0]); tot['most_Jjup80'][0]+=sum(sel); tot['most_Jjup80'][1]+=len(sel); tot['most_Jjup80'][2]+=len(sel)/n
    print(race,n,' '.join(out))
print('TOTAL (wins / picks / by chance)')
for k,v in tot.items(): print(f'  {k}: {v[0]} of {v[1]}, chance {v[2]:.1f}')
