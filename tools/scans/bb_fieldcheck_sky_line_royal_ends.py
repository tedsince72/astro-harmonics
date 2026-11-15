import sys,re; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
races=[('Lingfield','20210402_lingfield_aw_1435'),('Haydock','20200608_haydock_1345'),('Beverley','20240608_beverley_1405'),('Catterick','20220406_catterick_1440'),('Chelmsford','20240118_chelmsford_aw_1320'),('York','20240515_york_1545'),('York16','20240515_york_1615')]
W={'Lingfield':'Pholas','Haydock':'Ishvara','Beverley':'Perfect Part','York':'Secret Satire','York16':'Diligent Resdev'}
CJ=('conj','contraparallel'); ROY=E.ROY
data={n:E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx') for n,r in races}
def royal(b): return [r for c,R,r in b.star_rows(scoring=True) if r['fam'] not in CJ]
def skylines(b):
    out=[]
    for s in b.O:
        m=re.match(r'S (.+) – S (.+)$',s['line'] or '')
        if m and b.X in m.groups() and s['fam'] and s['fam'] not in CJ:
            Y=[g for g in m.groups() if g!=b.X][0]
            if Y not in ROY and Y!='Moon': out.append((s,Y))
    return out
def fam(r): return r['fam']
def tgt(r): return (r['fam'],str(r['tgt']))
def test(b,D,kind):
    for s,Y in skylines(b):
        if Y not in D: continue
        RX=royal(b); RY=royal(E.Body(Y,D[Y]))
        if kind=='L1':   # royal to X on the sky line's target, royal to Y same family as the sky line
            if any(tgt(r)==tgt(s) for r in RX) and any(fam(r)==fam(s) for r in RY): return True
        if kind=='L1b':  # same, royal to Y on its own different target of that family
            if any(tgt(r)==tgt(s) for r in RX) and any(fam(r)==fam(s) and tgt(r)!=tgt(s) for r in RY): return True
        if kind=='L2':   # royal to X and royal to Y on the same target as each other; sky X–Y same family
            if any(tgt(r1)==tgt(r2) and fam(r1)==fam(s) for r1 in RX for r2 in RY): return True
        if kind=='L4':   # royal to X and royal to Y both in the sky line's family
            if any(fam(r)==fam(s) for r in RX) and any(fam(r)==fam(s) for r in RY): return True
    return False
V={'L1 royal->X on the sky X–Y target; royal->Y same family':'L1','L1b L1, royal->Y on a different target of that family':'L1b',
'L2 royal->X = royal->Y (same target); sky X–Y same family':'L2','L4 royal->X and royal->Y both in the sky X–Y family':'L4'}
for v,k in V.items():
    print('==',v)
    for n,_ in races:
        l=[f"{run.split(' ',1)[1]} {X}"+(' *' if W.get(n,'#') in run else '') for run,D in data[n].items() for X,d in D.items() if test(E.Body(X,d),D,k)]
        rn=len({run for run,D in data[n].items() for X,d in D.items() if test(E.Body(X,d),D,k)}); fl=len(data[n])
        print(f'  {n} ({len(l)} bodies, {rn}/{fl} runners): {", ".join(l) if len(l)<=12 else ", ".join(l[:12])+" ..."}')
print('--- L2 detail')
for n,who,X in [('Beverley','Perfect Part','Sun'),('Beverley','Perfect Part','Makemake'),('York16','Diligent','Rahu')]:
    D=data[n][[k for k in data[n] if who in k][0]]; b=E.Body(X,D[X])
    for s,Y in skylines(b):
        if Y not in D: continue
        RX=royal(b); RY=royal(E.Body(Y,D[Y]))
        for r1 in RX:
            for r2 in RY:
                if tgt(r1)==tgt(r2) and fam(r1)==fam(s): print(who,X,'|',E.cell(s),'|',E.cell(r1),'|',E.cell(r2))
