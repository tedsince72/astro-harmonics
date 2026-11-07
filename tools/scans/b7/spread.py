import json,re,glob,collections
Rs=json.load(open('docs/eddie_read/results/results.json'))
def sc(t):
    m=re.search(r'\(([\d.]+)\)\s*$',t); return float(m.group(1)) if m else 0.0
def horse(n): return n.split(' / ')[0].split(' ',1)[1].strip()
def spread(p,MIN):
    st=collections.defaultdict(set)
    for b in p['bodies']:
        for c in b['cells']:
            m=re.match(r'([HJ]) (.+?) →',c['text'])
            if c['layer']=='star rows' and m and sc(c['text'])>=MIN: st[(m.group(1),m.group(2))].add(b['body'])
    return max([len(v) for v in st.values()] or [0]), max(st.items(),key=lambda kv:len(kv[1]),default=None)
for MIN in (50,80):
    tot=collections.Counter(); ch=0.0; c2=0.0
    for fn in sorted(glob.glob('docs/eddie_read/*_layers.json')):
        race=fn.split('race_batch_')[1].replace('_layers.json','')
        rs=Rs[race]; nr=set(rs.get('nonrunners',[])); d=json.load(open(fn))
        v={horse(p['name']):spread(p,MIN) for p in d['report'].values() if horse(p['name']) not in nr}
        mx=max(x[0] for x in v.values()); sel=[h for h,x in v.items() if x[0]==mx]
        W=set(rs['first']); T=W|set(rs['second'])
        if race.endswith('1315') and race.startswith('20261106'): print(f'  13:15 (>= {MIN}):',{h:(x[0],x[1][0] if x[1] else None) for h,x in v.items()})
        if race in ('20261106_aintree_1315',): continue
        tot['picks']+=len(sel); tot['won']+=sum(h in W for h in sel); tot['12']+=sum(h in T for h in sel); ch+=len(sel)/rs['ran']; c2+=len(sel)*len(T)/rs['ran']
    print(f'one natal star on the most natal bodies (>= {MIN}), other 19 races: {tot["picks"]} picks, {tot["won"]} won (chance {ch:.1f}), 1st/2nd {tot["12"]} ({c2:.1f})')
