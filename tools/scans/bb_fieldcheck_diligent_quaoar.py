import sys,re,math; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
exec(open('tools/scans/bb_fieldcheck_sky_line_royal_ends.py').read().split("def test(")[0])
from fractions import Fraction
def ok(o): return o['fam'] and o['fam'] not in CJ
def sky_on(b,Y): return [s for s in b.O if s['line'] in (f'S {Y} – S {b.X}',f'S {b.X} – S {Y}') and ok(s)]
def nat_on(b,Y): return [s for s in b.O if s['line'] in (f'S {Y} → H {b.X}',f'S {Y} → J {b.X}') and ok(s)]
def mult(o):
    if o['fam']=='whole': return Fraction(int(o['tgt']))
    if o['fam']=='golden':
        try: return Fraction(int(str(o['tgt']).split('×')[0]))
        except: return None
    return None
def Q1(b):  # two different royal stars on sky X, same family (whole / golden), multipliers in ratio 2 or 3 (n and 2n / 3n)
    rs=[o for o in b.O if ok(o) and re.match(rf'S (Aldebaran|Antares|Fomalhaut|Regulus) – S {re.escape(b.X)}$',o['line'] or '')]
    for i,a in enumerate(rs):
        for c in rs[i+1:]:
            if a['line']!=c['line'] and a['fam']==c['fam'] and mult(a) and mult(c):
                r=max(mult(a),mult(c))/min(mult(a),mult(c))
                if r in (2,3): return True
    return False
def Q1b(b):  # two different royal stars on sky X, same family (any target)
    rs=[o for o in b.O if ok(o) and re.match(rf'S (Aldebaran|Antares|Fomalhaut|Regulus) – S {re.escape(b.X)}$',o['line'] or '')]
    return any(a['line']!=c['line'] and a['fam']==c['fam'] for i,a in enumerate(rs) for c in rs[i+1:])
def carriers(b,r):
    return [(s,A,B) for s,A,B in b.pairs_on(r) if b.X not in (A,B) and 'Moon' not in (A,B)]
def tied_end(b,p,sky=True,nat=True):
    return [Y for Y in p[1:] if Y not in E.ROY and ((sky and sky_on(b,Y)) or (nat and nat_on(b,Y)))]
def Q2(b,k=2):  # a same-body line S X -> c X carried by >= k pairs, each with an end on sky X or natal X
    for c in 'HJ':
        for r in b.same_body(c):
            if r['fam'] in CJ: continue
            if sum(1 for p in carriers(b,r) if tied_end(b,p))>=k: return True
    return False
def Q3(b):  # Q2 (>=2) with one carrier end on sky X AND on natal X (Pluto here)
    for c in 'HJ':
        for r in b.same_body(c):
            if r['fam'] in CJ: continue
            P=[p for p in carriers(b,r) if tied_end(b,p)]
            if len(P)>=2 and any(sky_on(b,Y) and nat_on(b,Y) for p in P for Y in p[1:] if Y not in E.ROY): return True
    return False
V=[('Q1 two royal stars on sky X, same family, multipliers n and 2n / 3n',Q1),('Q1b two royal stars on sky X, same family',Q1b),
   ('Q2 same-body line carried by >=2 pairs, each with an end on sky / natal X',Q2),('Q2c same, >=3',lambda b:Q2(b,3)),
   ('Q3 Q2 with one carrier end on sky X and on natal X',Q3),('Q1+Q3',lambda b:Q1(b) and Q3(b))]
for v,f in V:
    print('==',v); tot=exp=won=0
    for n,_ in races:
        h=[(run,X) for run,D in data[n].items() for X,d in D.items() if f(E.Body(X,d))]
        rn=sorted({r for r,_ in h}); w=W.get(n)
        if w: tot+=len(rn); exp+=len(rn)/len(data[n]); won+=any(w in r for r in rn)
        lab=', '.join(f"{r.split(' ',1)[1]} {X}" for r,X in h) if len(h)<=10 else f'{len(h)} bodies'
        print(f"  {n}: {len(rn)}/{len(data[n])}" + (f"; winner {'YES' if any(w in r for r in rn) else 'no'}" if w else '') + f" | {lab}")
    print(f'  winner races: {tot} picks, {won} won, {exp:.1f} by chance')
