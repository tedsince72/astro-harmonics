import sys,re; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
exec(open('tools/scans/bb_fieldcheck_sky_line_royal_ends.py').read().split("def test(")[0])
def ok(r): return r['fam'] and r['fam'] not in CJ
def hj(b): return [r for r in b.L if r['line']==f'H {b.X} – J {b.X}' and ok(r)]
def moon(b): return [o for o in b.O if o['line'] in (f'S Moon → H {b.X}',f'S Moon → J {b.X}') and ok(o)]
def same(a,c): return a['fam']==c['fam'] and str(a['tgt'])==str(c['tgt'])
def M1(b): return any(same(h,m) for h in hj(b) for m in moon(b))
def SUN(b): return any(same(h,o) for h in hj(b) for o in b.O if o['line'] in (f'S Sun → H {b.X}',f'S Sun → J {b.X}') and ok(o))
def ANY(b,Y=None): return any(same(h,o) for h in hj(b) for o in b.O if re.match(rf'S (.+) → [HJ] {re.escape(b.X)}$',o['line'] or '') and ok(o) and (Y is None or o['line'].startswith(f'S {Y} ')))
def RS(b):  # sky royal on sky X and the Sun on natal X, same target
    sr=[o for o in b.O if re.match(rf'S (Aldebaran|Antares|Fomalhaut|Regulus) – S {re.escape(b.X)}$',o['line'] or '') and ok(o)]
    su=[o for o in b.O if o['line'] in (f'S Sun → H {b.X}',f'S Sun → J {b.X}') and ok(o)]
    return any(same(a,c) for a in sr for c in su)
V=[('M1 S Moon -> natal X on the target of H X – J X',M1),('M1sun same with the Sun',SUN),('control: any sky body -> natal X on the H X – J X target',ANY),
   ('RS sky royal on sky X and the Sun on natal X, same target',RS),('M1+RS',lambda b:M1(b) and RS(b))]
for v,f in V:
    print('==',v); tot=exp=won=0
    for n,_ in races:
        h=[(run,X) for run,D in data[n].items() for X,d in D.items() if X not in ('Rahu','Ketu') and f(E.Body(X,d))]
        rn=sorted({r for r,_ in h}); w=W.get(n)
        if w: tot+=len(rn); exp+=len(rn)/len(data[n]); won+=any(w in r for r in rn)
        lab=', '.join(f"{r.split(' ',1)[1]} {X}" for r,X in h) if len(h)<=10 else f'{len(h)} bodies'
        print(f"  {n}: {len(rn)}/{len(data[n])}" + (f"; winner {'YES' if any(w in r for r in rn) else 'no'}" if w else '') + f" | {lab}")
    print(f'  winner races: {tot} picks, {won} won, {exp:.1f} by chance')
print('---- RS details')
for n,who,X in [('Haydock','Ishvara','Juno'),('Haydock','Ventura Flame','Venus'),('Catterick','Beluga Gold','Mars'),('York16','True Promise','Vesta'),('York16','Diligent','Vesta'),('York16','Misemerald','Vesta'),('Chelmsford','Good Time Ahead','Sun')]:
    D=data[n][[k for k in data[n] if who in k][0]]; b=E.Body(X,D[X])
    sr=[o for o in b.O if re.match(rf'S (Aldebaran|Antares|Fomalhaut|Regulus) – S {re.escape(b.X)}$',o['line'] or '') and ok(o)]
    su=[o for o in b.O if o['line'] in (f'S Sun → H {b.X}',f'S Sun → J {b.X}') and ok(o)]
    for a in sr:
        for c in su:
            if same(a,c): print(n,who,X,'RS |',E.cell(a),'|',E.cell(c))
    for h in hj(b):
        for m in moon(b):
            if same(h,m): print(n,who,X,'M1 |',E.cell(h),'|',E.cell(m))
