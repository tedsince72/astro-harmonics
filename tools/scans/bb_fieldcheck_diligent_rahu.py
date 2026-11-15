import sys,re; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
exec(open('tools/scans/bb_fieldcheck_sky_line_royal_ends.py').read().split("def test(")[0])
def rat(r): return [(k,t,s) for k,t,s in (('sb',r['rt'],r['rs']),('x',r['xt'],r['xs'])) if t and t!='no target' and s is not None]
def skyR(b,R): return [s for s in b.O if s['line'] in (f'S {R} – S {b.X}',f'S {b.X} – S {R}') and s['fam'] and s['fam'] not in CJ]
def rows(b,c,R): return [r for cc,RR,r in b.star_rows(scoring=True) if cc==c and RR.endswith(R) and r['fam'] not in CJ]
def carried_natal(b,r):  # a carrier pair of r with an end on natal X (S Y -> H/J X)
    for s,A,B in b.pairs_on(r):
        for Y in (A,B):
            if Y in E.ROY or Y in (b.X,'Moon'): continue
            if any(o['line'] in (f'S {Y} → H {b.X}',f'S {Y} → J {b.X}') and o['fam'] and o['fam'] not in CJ for o in b.O): return True
    return False
def A(b,sky=True,ratio=True,carry=False):
    for R in E.ROY:
        if sky and not skyR(b,R): continue
        H=rows(b,'H',R); J=rows(b,'J',R)
        if ratio: H=[r for r in H if rat(r)]; J=[r for r in J if rat(r)]
        if not H or not J: continue
        if carry and not any(carried_natal(b,r) for r in H+J): continue
        return True
    return False
def T10(b):  # crossed or same-body ratio on 10 (decade copy of the royal line)
    return any(t.startswith('10 ') for c,R,r in b.star_rows(scoring=True) if r['fam'] not in CJ for k,t,s in rat(r))
V=[('A1 same royal star R: S R – S X scores, H R – H X and J R – J X score, each with a ratio on target',lambda b:A(b)),
   ('A2 A1 without the sky line',lambda b:A(b,sky=False)),
   ('A0 S R – S X + both natal R lines score (no ratio needed)',lambda b:A(b,ratio=False)),
   ('A3 A1 + a carrier of one royal line has an end on natal X',lambda b:A(b,carry=True)),
   ('T10 a scoring royal line with a ratio on 10',T10)]
for v,f in V:
    print('==',v); tot=exp=won=0
    for n,_ in races:
        h=[(run,X) for run,D in data[n].items() for X,d in D.items() if f(E.Body(X,d))]
        rn=sorted({r for r,_ in h}); w=W.get(n)
        if w: tot+=len(rn); exp+=len(rn)/len(data[n]); won+=any(w in r for r in rn)
        lab=', '.join(f"{r.split(' ',1)[1]} {X}" for r,X in h) if len(h)<=10 else f'{len(h)} bodies'
        print(f"  {n}: {len(rn)}/{len(data[n])}" + (f"; winner {'YES' if any(w in r for r in rn) else 'no'}" if w else '') + f" | {lab}")
    print(f'  winner races: {tot} picks, {won} won, {exp:.1f} by chance')
print('#### T10 variants')
def Tn(b,ns,scoring=True):
    return any(any(t.split(' ')[0] in ns for k,t,s in rat(r)) for c,R,r in b.star_rows(scoring=scoring) if not scoring or r['fam'] not in CJ)
def Tdet(b):
    return [(E.cell(r),k,t,s) for c,R,r in b.star_rows(scoring=True) if r['fam'] not in CJ for k,t,s in rat(r) if t.startswith('10 ')]
for v,f in [('T10u ratio on 10, royal line need not score',lambda b:Tn(b,{'10'},False)),
            ('T11-20 scoring royal line, ratio on a whole 11-20',lambda b:Tn(b,{str(i) for i in range(11,21)})),
            ('T5-9 scoring royal line, ratio on 5..9',lambda b:Tn(b,{'5','6','7','8','9'}))]:
    print('==',v); tot=exp=won=0
    for n,_ in races:
        rn=sorted({run for run,D in data[n].items() for X,d in D.items() if f(E.Body(X,d))}); w=W.get(n)
        if w: tot+=len(rn); exp+=len(rn)/len(data[n]); won+=any(w in r for r in rn)
        print(f"  {n}: {len(rn)}/{len(data[n])}" + (f"; winner {'YES' if any(w in r for r in rn) else 'no'}" if w else ''))
    print(f'  winner races: {tot} picks, {won} won, {exp:.1f} by chance')
for n,who in [('Haydock','Ishvara'),('Beverley','Perfect Part'),('York','Secret Satire'),('York16','Diligent')]:
    D=data[n][[k for k in data[n] if who in k][0]]
    for X,d in D.items():
        for x in Tdet(E.Body(X,d)): print(n,who,X,x)
