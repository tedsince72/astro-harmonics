import sys,re; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
races=[('Lingfield','20210402_lingfield_aw_1435'),('Haydock','20200608_haydock_1345'),('Beverley','20240608_beverley_1405'),('Catterick','20220406_catterick_1440'),('Chelmsford','20240118_chelmsford_aw_1320'),('York','20240515_york_1545'),('York16','20240515_york_1615')]
W={'Lingfield':'Pholas','Haydock':'Ishvara','Beverley':'Perfect Part','York':'Secret Satire','York16':'Diligent Resdev'}
CJ=('conj','contraparallel'); ROY=E.ROY
data={n:E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx') for n,r in races}
ok=lambda rs:[r for r in rs if r['fam'] and r['fam'] not in CJ]
num=lambda x:isinstance(x,(int,float))
def prs(b,r): return [(s,A,B) for s,A,B in b.pairs_on(r) if b.X not in (A,B) and 'Moon' not in (A,B)]
def A_(b):
    for R in ROY:
        for pl in ('RA','Dec'):
            if all(any(R2==R and r['plane']==pl and num(r['rs']) and str(r['rt']).startswith('1 ') for _,R2,r in b.star_rows(c)) for c in 'HJ'): return True
    return False
def ends(b,c,R):
    out=[]
    for _,R2,r in b.star_rows(c,scoring=True):
        if R2==R and r['fam'] not in CJ:
            for s,A,B in prs(b,r): out.append({A,B})
    return out
def B1(b): return any(ends(b,'H',R) and ends(b,'J',R) for R in ROY)
def shared(b):
    S=set()
    for R in ROY:
        for p in ends(b,'H',R):
            for q in ends(b,'J',R): S|=(p&q)-set(ROY)
    return S
def B2(b): return bool(shared(b))
def onall(b,Y): return ok(b.sky_y(Y)) and ok(b.to_natal(Y,'H')) and ok(b.to_natal(Y,'J'))
def B3(b): return any(onall(b,Y) for Y in shared(b))
V={'A same-body unison on the same royal star in both charts, same plane':A_,
'B1 the same royal star\'s line carried by a pair in both charts':B1,
'B2 B1, the H and J pairs share a body':B2,
'B3 B2, the shared body on sky X and on both natal X':B3,
'A + B1':lambda x:A_(x) and B1(x),'A + B2':lambda x:A_(x) and B2(x)}
for v,f in V.items():
    print('==',v)
    for n,_ in races:
        l=[f"{run.split(' ',1)[1]} {X}"+(' *' if W.get(n,'#') in run else '') for run,D in data[n].items() for X,d in D.items() if f(E.Body(X,d))]
        print(f'  {n} ({len(l)}): {", ".join(l) if len(l)<=14 else ", ".join(l[:14])+" ..."}')
print('---')
for n,who,X in [('Haydock','Ishvara','Mercury'),('York16','Diligent','Venus')]:
    D=data[n]; k=[k for k in D if who in k][0]; b=E.Body(X,D[k][X])
    for R in ROY:
        for c in 'HJ':
            for _,R2,r in b.star_rows(c,scoring=True):
                if R2==R and r['fam'] not in CJ and prs(b,r):
                    print(who,X,E.cell(r)); [print('    ',E.cell(s)) for s,A,B in prs(b,r)]
    print('  shared', shared(b), {Y:(bool(ok(b.sky_y(Y))),bool(ok(b.to_natal(Y,'H'))),bool(ok(b.to_natal(Y,'J')))) for Y in shared(b)})
print('== B2s: B2, the shared body on sky X')
for n,_ in races:
    l=[f"{run.split(' ',1)[1]} {X}"+(' *' if W.get(n,'#') in run else '') for run,D in data[n].items() for X,d in D.items() if any(ok(E.Body(X,d).sky_y(Y)) for Y in shared(E.Body(X,d)))]
    print(f'  {n} ({len(l)}): {", ".join(l)}')
