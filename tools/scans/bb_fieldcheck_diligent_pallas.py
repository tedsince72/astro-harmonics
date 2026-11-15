import sys,re; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
exec(open('tools/scans/bb_fieldcheck_sky_line_royal_ends.py').read().split("def test(")[0])
def uni(r): return [k for k,t,s in (('sb',r['rt'],r['rs']),('x',r['xt'],r['xs'])) if t and str(t).startswith('1 ') and s is not None]
def U(b):  # royal row with a same-body unison (any royal row), 3+ such cells
    return sum(1 for c,R,r in b.star_rows() if 'sb' in uni(r))>=3
D=data['York16']
print('Pallas unisons (>=3 same-body unisons on royal rows) York16:', sorted(run for run,DD in D.items() if U(E.Body('Pallas',DD['Pallas']))))
def num(s):
    try: return float(s['tgt'])
    except: return None
def P2(b):  # one sky body Y on natal X (same chart) in both planes, targets with the same leading digits (33 / 33.3333)
    for c in 'HJ':
        for Y in set(re.match(r'S (.+) → ',o['line']).group(1) for o in b.O if re.match(rf'S .+ → {c} {re.escape(b.X)}$',o['line'] or '')):
            rows=[o for o in b.O if o['line']==f'S {Y} → {c} {b.X}' and o['fam'] and o['fam'] not in CJ]
            ra=[o for o in rows if o['plane']=='RA']; de=[o for o in rows if o['plane']=='Dec']
            for a in ra:
                for d in de:
                    x,y=num(a),num(d)
                    if x and y and str(x).replace('.','')[:2]==str(y).replace('.','')[:2] and int(x)==int(y): return True
    return False
def sky_xy(b):
    for s in b.O:
        m=re.match(r'S (.+) – S (.+)$',s['line'] or '')
        if m and b.X in m.groups():
            Y=[g for g in m.groups() if g!=b.X][0]
            if Y not in E.ROY and Y!='Moon' and s['fam'] and s['fam'] not in CJ: yield s,Y
def P3(b):  # royal line to X carried by the sky line S X – S Y (same target), and Y on natal X (S Y -> c X, any chart, not conj/cp)
    for c,R,r in b.star_rows(scoring=True):
        if r['fam'] in CJ: continue
        for s in b.same_on(r):
            m=re.match(r'S (.+) – S (.+)$',s['line'] or '')
            if not m or b.X not in m.groups() or s['fam'] in CJ: continue
            Y=[g for g in m.groups() if g!=b.X][0]
            if Y in E.ROY or Y=='Moon': continue
            if any(o['line'] in (f'S {Y} → H {b.X}',f'S {Y} → J {b.X}') and o['fam'] and o['fam'] not in CJ for o in b.O): return True
    return False
def P3o(b):  # P3, Y on natal X in the other chart from the royal line
    for c,R,r in b.star_rows(scoring=True):
        if r['fam'] in CJ: continue
        oc='J' if c=='H' else 'H'
        for s in b.same_on(r):
            m=re.match(r'S (.+) – S (.+)$',s['line'] or '')
            if not m or b.X not in m.groups() or s['fam'] in CJ: continue
            Y=[g for g in m.groups() if g!=b.X][0]
            if Y in E.ROY or Y=='Moon': continue
            if any(o['line']==f'S {Y} → {oc} {b.X}' and o['fam'] and o['fam'] not in CJ for o in b.O): return True
    return False
for v,f in [('P2 one sky body on natal X both planes, same number across families (33 / 33.33)',P2),
            ('P3 royal line carried by S X – S Y, Y on natal X',P3),('P3o P3, Y on natal X in the other chart',P3o)]:
    print('==',v); tot=exp=won=0
    for n,_ in races:
        h=[(run,X) for run,DD in data[n].items() for X,d in DD.items() if f(E.Body(X,d))]
        rn=sorted({r for r,_ in h}); w=W.get(n)
        if w: tot+=len(rn); exp+=len(rn)/len(data[n]); won+=any(w in r for r in rn)
        lab=', '.join(f"{r.split(' ',1)[1]} {X}" for r,X in h) if len(h)<=10 else f'{len(h)} bodies'
        print(f"  {n}: {len(rn)}/{len(data[n])}" + (f"; winner {'YES' if any(w in r for r in rn) else 'no'}" if w else '') + f" | {lab}")
    print(f'  winner races: {tot} picks, {won} won, {exp:.1f} by chance')
print('---- Pallas same-body unisons per runner, York16')
for run,DD in D.items():
    b=E.Body('Pallas',DD['Pallas']); print(run, [(r['line'],r['plane'],r['r'],r['rt']) for c,R,r in b.star_rows() if 'sb' in uni(r) and 'Antares' in r['line']])
