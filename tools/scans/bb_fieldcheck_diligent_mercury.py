import sys,re; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
races=[('Lingfield','20210402_lingfield_aw_1435'),('Haydock','20200608_haydock_1345'),('Beverley','20240608_beverley_1405'),('Catterick','20220406_catterick_1440'),('Chelmsford','20240118_chelmsford_aw_1320'),('York','20240515_york_1545'),('York16','20240515_york_1615')]
W={'Lingfield':'Pholas','Haydock':'Ishvara','Beverley':'Perfect Part','York':'Secret Satire','York16':'Diligent Resdev'}
CJ=('conj','contraparallel'); ROY=E.ROY
data={n:E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx') for n,r in races}
ok=lambda rs:[r for r in rs if r['fam'] and r['fam'] not in CJ]
def roy(b): return [(c,R,r) for c,R,r in b.star_rows(scoring=True) if r['fam'] not in CJ]
def prs(b,r): return [(s,A,B) for s,A,B in b.pairs_on(r) if b.X not in (A,B) and 'Moon' not in (A,B)]
def a(b,conj=True):
    for c,R,r in roy(b):
        for s,A,B in b.pairs_on(r):
            if R in (A,B):
                Y=B if A==R else A
                if Y in (b.X,'Moon'): continue
                n=[x for x in b.to_natal(Y,c) if x['fam']]
                if any((x['fam']=='conj')==conj or not conj for x in n): return True
    return False
def bb(b):
    for c,R,r in roy(b):
        for s in b.same_on(r):
            m=re.match(r'S (.+) – S (.+)$',s['line'] or '')
            if m and b.X in m.groups():
                Y=[g for g in m.groups() if g!=b.X][0]
                if Y in ROY and Y!=R and s['fam'] not in CJ: return True
    return False
def c(b):
    return any(ok(b.sky_y(A)) and ok(b.sky_y(B)) for cc,R,r in roy(b) for s,A,B in prs(b,r) if A not in ROY and B not in ROY)
V={'a royal line carried by S Y – S R (the same star), Y conj natal X in that chart':a,
'a2 as a, Y on natal X any family':lambda x:a(x,False),
'b royal line on the target of another royal star on sky X (S X – S R2)':bb,
'c royal line carried by a pair (no royal star) with both ends on sky X':c,
'a + b':lambda x:a(x) and bb(x),'a + c':lambda x:a(x) and c(x),'b + c':lambda x:bb(x) and c(x),'a2 + b':lambda x:a(x,False) and bb(x),'a2 + c':lambda x:a(x,False) and c(x),'a + b + c':lambda x:a(x) and bb(x) and c(x)}
for v,f in V.items():
    print('==',v)
    for n,_ in races:
        l=[f"{run.split(' ',1)[1]} {X}"+(' *' if W.get(n,'#') in run else '') for run,D in data[n].items() for X,d in D.items() if f(E.Body(X,d))]
        print(f'  {n} ({len(l)}): {", ".join(l) if len(l)<=14 else ", ".join(l[:14])+" ..."}')
