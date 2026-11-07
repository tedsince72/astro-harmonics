import json,re,glob,itertools,collections,sys
R=json.load(open('docs/eddie_read/results/results.json'))
def sc(t):
    m=re.search(r'\(([\d.]+)\)\s*$',t); return float(m.group(1)) if m else 0.0
def horse(n): return n.split(' / ')[0].split(' ',1)[1].strip().lower()
MIN=float(sys.argv[1]) if len(sys.argv)>1 else 50
tot=collections.Counter(); chance=0.0
for fn in sorted(glob.glob('docs/eddie_read/*_layers.json')):
    race=fn.split('race_batch_')[1].replace('_layers.json','')
    if race not in R: continue
    rs=R[race]; nr={x.lower() for x in rs.get('nonrunners',[])}
    d=json.load(open(fn)); best=collections.defaultdict(dict)   # key -> runner -> (score, text)
    for p in d['report'].values():
        h=horse(p['name'])
        if h in nr: continue
        for b in p['bodies']:
            for c in b['cells']:
                k=tuple(c['key']); v=sc(c['text'])
                if k not in best or h not in best[k] or v>best[k][h][0]: best[k][h]=(v,c['text'])
    pair=collections.defaultdict(list)
    for k,m in best.items():
        if len(m)==2 and all(v>=MIN for v,t in m.values()):
            pair[tuple(sorted(m))].append((k,m))
    T={x.lower() for x in rs['first']+rs['second']}; W={x.lower() for x in rs['first']}
    if not pair: print(race,'no pair'); continue
    mx=max(len(v) for v in pair.values()); top=[pq for pq,v in pair.items() if len(v)==mx]
    n=len({h for h in (horse(p['name']) for p in d['report'].values()) if h not in nr})
    for pq in top:
        hit=len(set(pq)&T)
        tot['pairs']+=1; tot[f'{hit} of 1st/2nd']+=1; tot['exact']+= set(pq)==T; tot['has winner']+=bool(set(pq)&W)
    chance+=len(top)*2*len(T)/n/ (len(top) and 1)
    print(race, f'{n} ran, top pair(s) {mx} shared keys:', ['+'.join(pq) for pq in top], '| 1st/2nd', sorted(T))
    if race=='20261106_aintree_1240':
        for pq in top:
            for k,m in pair[pq]: print('     ',k,[t for v,t in m.values()])
print(dict(tot))
