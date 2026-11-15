import sys,re; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
races=[('Lingfield','20210402_lingfield_aw_1435'),('Haydock','20200608_haydock_1345'),('Beverley','20240608_beverley_1405'),('Catterick','20220406_catterick_1440'),('Chelmsford','20240118_chelmsford_aw_1320'),('York','20240515_york_1545'),('York16','20240515_york_1615')]
W={'Lingfield':'Pholas','Haydock':'Ishvara','Beverley':'Perfect Part','York':'Secret Satire','York16':'Diligent Resdev'}
CJ=('conj','contraparallel'); ROY=E.ROY
data={n:E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx') for n,r in races}
def selfpairs(b):
    """(royal row, pair row, Y): royal natal line to X on the target of a sky line S X – S Y (Y not royal, not Moon)"""
    out=[]
    for c,R,r in b.star_rows(scoring=True):
        if r['fam'] in CJ: continue
        for s in b.same_on(r):
            m=re.match(r'S (.+) – S (.+)$',s['line'] or '')
            if m and b.X in m.groups():
                Y=[g for g in m.groups() if g!=b.X][0]
                if Y not in ROY and Y!='Moon' and s['fam'] not in CJ: out.append((c,R,r,s,Y))
    return out
def a(b,D): return bool(selfpairs(b))
def mutual(b,D,diffR=False):
    for c,R,r,s,Y in selfpairs(b):
        if Y not in D: continue
        bY=E.Body(Y,D[Y])
        for c2,R2,r2,s2,X2 in selfpairs(bY):
            if X2==b.X and s2['line']==s['line'] and s2['plane']==s['plane'] and (not diffR or R2!=R): return True
    return False
V={'a a royal line to X carried by the sky line S X – S Y':a,
'b a, and the same sky line carries a royal line to Y (in Y\'s sheet)':mutual,
'b2 b, a different royal star on Y':lambda b,D:mutual(b,D,True)}
for v,f in V.items():
    print('==',v)
    for n,_ in races:
        l=[f"{run.split(' ',1)[1]} {X}"+(' *' if W.get(n,'#') in run else '') for run,D in data[n].items() for X,d in D.items() if f(E.Body(X,d),D)]
        print(f'  {n} ({len(l)}): {", ".join(l) if len(l)<=16 else ", ".join(l[:16])+" ..."}')
