import sys,re; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
exec(open('tools/scans/bb_fieldcheck_sky_line_royal_ends.py').read().split("def test(")[0])
def sky_on(b,Y):   # S Y – S X either order, scoring, not conj/cp
    return [s for s in b.O if s['line'] in (f'S {Y} – S {b.X}',f'S {b.X} – S {Y}') and s['fam'] and s['fam'] not in CJ]
def nat_on(b,Y):   # S Y -> c X scoring (conj / cp kept separately)
    return [s for s in b.O if s['line'] in (f'S {Y} → H {b.X}',f'S {Y} → J {b.X}') and s['fam']]
def nat_on_strict(b,Y): return [s for s in nat_on(b,Y) if s['fam'] not in CJ]
def lines(b):
    for c,R,r in b.star_rows(scoring=True):
        if r['fam'] in CJ: continue
        P=[(s,A,B) for s,A,B in b.pairs_on(r) if b.X not in (A,B) and 'Moon' not in (A,B)]
        yield r,P
def tied(b,Y,strict=False): return bool(sky_on(b,Y) or (nat_on_strict(b,Y) if strict else nat_on(b,Y)))
def N1(b,k=3,strict=False):
    for r,P in lines(b):
        good=[p for p in P if any(Y not in E.ROY and tied(b,Y,strict) for Y in p[1:])]
        if len(good)>=k: return True
    return False
def N2(b):   # >=2 carrier pairs, each with an end on sky X in the royal line's family
    for r,P in lines(b):
        good=[p for p in P if any(Y not in E.ROY and any(s['fam']==r['fam'] for s in sky_on(b,Y)) for Y in p[1:])]
        if len(good)>=2: return True
    return False
def N3(b):   # a carrier with one end on sky X and the other on natal X, + another carrier with an end on sky X in the royal family
    for r,P in lines(b):
        a=[p for p in P if (sky_on(b,p[1]) and nat_on(b,p[2])) or (sky_on(b,p[2]) and nat_on(b,p[1]))]
        f=[p for p in P if any(Y not in E.ROY and any(s['fam']==r['fam'] for s in sky_on(b,Y)) for Y in p[1:])]
        if a and any(q is not x for q in f for x in a): return True
    return False
V=[('N1 royal line carried by >=3 pairs, each with an end on sky X or natal X (conj/cp count)',lambda b:N1(b,3)),
   ('N1s N1, conj/cp ties not counted',lambda b:N1(b,3,True)),
   ('N1b >=2 such pairs',lambda b:N1(b,2)),
   ('N2 >=2 carrier pairs with an end on sky X in the royal line family',N2),
   ('N3 a carrier with one end on sky X, other on natal X + another carrier end on sky X in the royal family',N3)]
for v,f in V:
    print('==',v)
    for n,_ in races:
        h=[(run,X) for run,D in data[n].items() for X,d in D.items() if f(E.Body(X,d))]
        rn=sorted({r for r,_ in h}); w=W.get(n)
        lab=', '.join(f"{r.split(' ',1)[1]} {X}" for r,X in h) if len(h)<=10 else f'{len(h)} bodies'
        print(f"  {n}: {len(rn)}/{len(data[n])}" + (f"; winner {'YES' if any(w in r for r in rn) else 'no'}" if w else '') + f" | {lab}")
print('#### tighter')
def fam_sky(b,Y,f): return any(s['fam']==f for s in sky_on(b,Y))
def N2c(b):  # N2 and >=3 carriers on the line
    for r,P in lines(b):
        good=[p for p in P if any(Y not in E.ROY and fam_sky(b,Y,r['fam']) for Y in p[1:])]
        if len(good)>=2 and len(P)>=3: return True
    return False
def N4(b):   # N2 and some sky body -> natal X (not conj/cp) in the royal line's family
    for r,P in lines(b):
        good=[p for p in P if any(Y not in E.ROY and fam_sky(b,Y,r['fam']) for Y in p[1:])]
        if len(good)>=2 and any(s['fam']==r['fam'] for s in b.O if re.match(r'S .+ → [HJ] ',s['line'] or '') and s['line'].endswith(' '+b.X)): return True
    return False
def N5(b):   # N2 with the two tying lines on different targets of the family (as 55.5556 and 12.2222)
    for r,P in lines(b):
        t=set()
        for p in P:
            for Y in p[1:]:
                if Y in E.ROY: continue
                for s in sky_on(b,Y):
                    if s['fam']==r['fam']: t.add((p[0]['line'],str(s['tgt'])))
        if len({x for _,x in t})>=2 and len({l for l,_ in t})>=2: return True
    return False
for v,f in [('N2c N2 + >=3 carriers',N2c),('N4 N2 + a sky body -> natal X in the family',N4),('N5 N2, tying lines on 2+ targets',N5),('N2c+N4',lambda b:N2c(b) and N4(b))]:
    print('==',v); tot=0;exp=0;won=0
    for n,_ in races:
        h=[(run,X) for run,D in data[n].items() for X,d in D.items() if f(E.Body(X,d))]
        rn=sorted({r for r,_ in h}); w=W.get(n)
        if w: tot+=len(rn); exp+=len(rn)/len(data[n]); won+=any(w in r for r in rn)
        lab=', '.join(f"{r.split(' ',1)[1]} {X}" for r,X in h) if len(h)<=10 else f'{len(h)} bodies'
        print(f"  {n}: {len(rn)}/{len(data[n])}" + (f"; winner {'YES' if any(w in r for r in rn) else 'no'}" if w else '') + f" | {lab}")
    print(f'  winner races: {tot} picks, {won} won, {exp:.1f} by chance')
