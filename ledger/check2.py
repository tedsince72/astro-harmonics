import sys, itertools, collections
sys.path.insert(0,'/home/claude/ledger')
from readrace import Race, sep, FN, FAMS, STARS, NODES, FAST, FASTNATAL, results, dev_deg
def best(v,m):
    f=max(FAMS,key=lambda k:FN[k](v,m)); return f,FN[f](v,m)
R=sys.argv[1]; rc=Race(R); res=results(R)
order=sorted(rc.charts,key=lambda c:int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
allsky=[]
for k in rc.byrank:
    for m in ('RA','Dec'):
        v=sep(rc.sky[k[0]],rc.sky[k[1]],m)
        if best(v,m)[1]>=80: allsky.append((rc.pairs[k]['rank'],k,m,v))
print('RACE',R,'80+ sky entries',len(allsky))
print('\n1. IMPRINT<->MOMENT on ALL 80+ sky pairs (same coord, 0.003), natal certain bodies; and 2. CROSS-COORDINATE (natal RA = sky Dec etc.)')
for c in order:
    same=collections.Counter(); crossc=[]; bodies=collections.defaultdict(set); lst=[]
    for sd,tab in rc.charts[c].items():
        P=rc.natal[tab]
        for x,y in itertools.combinations(sorted(P),2):
            if (x in STARS and y in STARS) or 'Moon' in (x,y) or {x,y}&FASTNATAL: continue
            for m in ('RA','Dec'):
                if m=='RA' and {x,y}==NODES: continue
                v=sep(P[x],P[y],m)
                for rk,k,sm,sv in allsky:
                    if abs(v-sv)<=0.003:
                        if sm==m:
                            same[sd]+=1; lst.append(f"#{rk} {sd} {x}–{y} {m} {v:.4f}")
                            for b in (x,y):
                                if b not in STARS: bodies[b].add((sd,rk))
                        else: crossc.append(f"#{rk}({sm}) {sd} {x}–{y} {m} {v:.4f}")
    both=[b for b,s in bodies.items() if {sd for sd,_ in s}=={'H','J'}]
    print(f"  {res[c]['finish']} {rc.names[c][0]:18} same-coord H {same['H']} J {same['J']} | bodies on both charts: {', '.join(f'{b} '+','.join(f'{sd}#{rk}' for sd,rk in sorted(bodies[b])) for b in both) or '-'} | cross-coord {len(crossc)}")
    if c==order[0] or res[c]['sp'] in [min((res[x]['sp'] for x in order),key=lambda s:0)]: pass
    print('      '+'; '.join(sorted(lst,key=lambda t:int(t[1:].split()[0]))[:14]))
print('\n3. SELF contacts (sky body on its own natal body) >=90, certain natal bodies first; busy bodies marked B')
for c in order:
    out=[]
    for sd,tab in rc.charts[c].items():
        P=rc.natal[tab]
        for b in P:
            if b in STARS or b in FAST or b not in rc.sky: continue
            for m in ('RA','Dec'):
                v=sep(rc.sky[b],P[b],m); f,s=best(v,m)
                if s>=90:
                    A=dev_deg(sep(rc.S3[b]['p2'],P[b],m),f)<dev_deg(sep(rc.S3[b]['m2'],P[b],m),f)
                    out.append(f"{sd} {b}{'B' if b in rc.busy else ''}{'*' if b in FASTNATAL else ''} {m} {v:.4f} {f[:5]} {s:.0f} {'A' if A else 'S'}")
    print(f"  {res[c]['finish']} {rc.names[c][0]:18} {len(out)}: "+'; '.join(out))
print('\n4. The winner key contacts at -30 / off / +30 min (sky->natal): strengthening or fading')
