import json,re,glob,itertools,collections
R=json.load(open('docs/eddie_read/results/results.json'))
def sc(t):
    m=re.search(r'\(([\d.]+)\)\s*$',t); return float(m.group(1)) if m else 0.0
def horse(n): return n.split(' / ')[0].split(' ',1)[1].strip().lower()
def cen(c):
    if c['layer'] in ('top rows','same body'): return {c['text'].split(' →')[0]}
    return {s.split(' →')[0] for s in c['source_lines']}
def star(c):
    m=re.match(r'[HJ] (.+?) →',c['text']); return m.group(1) if c['layer']=='star rows' and m else None
def chart(c):
    m=re.search(r'→ ([HJ]) ',c['text']); return m.group(1) if m else c['text'][0]
def feats(p):
    cells=[(b['body'],c) for b in p['bodies'] for c in b['cells']]
    f={}
    for C,nm in (('S Sun','Sun'),('S Moon','Moon'),('S Jupiter','Jup')):
        strong=[(X,c) for X,c in cells if C in cen(c) and sc(c['text'])>=50]
        st=collections.defaultdict(set)
        for X,c in strong:
            if star(c): st[star(c)].add(X)
        f[f'{nm}: a {nm}-line star on 2+ natal bodies']=any(len(v)>=2 for v in st.values())
        direct={X for X,c in strong if c['text'].startswith(C+' →')}
        viastar={X for X,c in strong if star(c)}
        f[f'{nm}: S {nm} and a {nm}-line star on one natal body']=bool(direct & viastar)
        both=collections.defaultdict(set)
        for X,c in strong: both[X].add(chart(c))
        f[f'{nm}: one natal body reached on both charts']=any(v>={'H','J'} for v in both.values())
        f[f'{nm}: S {nm} on one body both charts']=any({chart(c) for X2,c in strong if X2==X and c['text'].startswith(C+' →')}>={'H','J'} for X in direct)
        f[f'{nm}: a {nm}-route cell >= 90']=any(sc(c['text'])>=90 for X,c in strong)
    f['L3: same number in 3+ places']=any(len(x['cells'])>=3 for x in p['cases']['5'])
    f['L3: one body both planes']=len(p['cases']['2'])>0
    f['L3: no same body both charts']=len(p['cases']['1'])==0
    f['L1: a loose same body']=any('(loose)' in x for x in p['same_bodies'])
    f['L1: same body >= 80']=any(sc(x)>=80 for x in p['same_bodies'])
    f['L2: line star on a same body >= 50']=any(sc((c['text'] if isinstance(c,dict) else c))>=50 for L in p['landings'] for k in ('on_this_chart','on_other_chart') for c in L[k] if isinstance(c,dict) and c['layer']=='star rows')
    return f
races={}
for fn in sorted(glob.glob('docs/eddie_read/*_layers.json')):
    race=fn.split('race_batch_')[1].replace('_layers.json','')
    if race not in R: continue
    res=R[race]; nr={x.lower() for x in res.get('nonrunners',[])}
    d=json.load(open(fn))
    races[race]=(res,[(horse(p['name']),feats(p)) for p in d['report'].values() if horse(p['name']) not in nr])
K=list(races['20261106_aintree_1240'][1][0][1].keys())
res,rows=races['20261106_aintree_1240']
for h,f in rows: print(h,[k for k in K if f[k]])
target={'risky obsession','aqua bleu'}
out=[]
for n in (1,2,3):
    for combo in itertools.combinations(K,n):
        sel={h for h,f in rows if all(f[k] for k in combo)}
        if sel!=target: continue
        # minimal: no subset already isolates
        if any({h for h,f in rows if all(f[k] for k in sub)}==target for m in range(1,n) for sub in itertools.combinations(combo,m)): continue
        pk=t2=w=0; ch=0.0; fired=exact=0
        for race,(rs,rw) in races.items():
            if race=='20261106_aintree_1240': continue
            s=[h for h,f in rw if all(f[k] for k in combo)]
            T={x.lower() for x in rs['first']+rs['second']}; W={x.lower() for x in rs['first']}
            pk+=len(s); t2+=sum(h in T for h in s); w+=sum(h in W for h in s); ch+=len(s)*len(T)/rs['ran']; fired+=bool(s); exact+=set(s)==T
        out.append((t2-ch,combo,pk,t2,ch,w,fired,exact))
for o in sorted(out,reverse=True):
    print(f'{" + ".join(o[1])}\n    other 19 races: {o[2]} picks, {o[3]} 1st/2nd (chance {o[4]:.1f}), {o[5]} won, fired {o[6]}, exact 1st+2nd {o[7]}')
