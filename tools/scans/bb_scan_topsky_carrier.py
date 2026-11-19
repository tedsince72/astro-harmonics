import sys,re,os
sys.path.insert(0,"tools/scans"); sys.argv=sys.argv[:1]; sys.path.insert(0,'tools'); sys.path.insert(0,'tools/scans')
from bb_ss_lines import ss_lines
import bb_sky_angles_races as A, bb_scan_negatives as NG
def key(c):
    m=re.match(r'S (\S+(?: \S+)?) – S (\S+(?: \S+)?) (RA|Dec)',c); return (frozenset((m.group(1),m.group(2))),m.group(3))
res={'top1':[], 'top3sole':[], 'top3all':[]}
for race,win in NG.RACES:
    o=ss_lines(race)
    if not o or not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'): continue
    try: L=sorted(A.lines(race),key=lambda x:-x[5])
    except Exception as e: continue
    car={}
    for r,cs in o.items():
        for c in cs: car.setdefault(key(c),set()).add(r)
    n=len(o)  # runners holding any rule
    import bb_cover8_where as W
    runners,_=W.holders(race); n=len(runners)
    # top1: carriers of the single strongest sky line
    k=(frozenset(L[0][:2]),L[0][2]); c1=car.get(k,set())
    res['top1'].append((race,win,c1,n))
    # top3: runners carrying ALL of the 3 strongest lines (as Monopolise)
    ks=[(frozenset(x[:2]),x[2]) for x in L[:3]]
    sets=[car.get(k,set()) for k in ks]
    allc=set.intersection(*sets) if sets else set()
    res['top3all'].append((race,win,allc,n))
for name,rows in res.items():
    picks=sum(len(c) for _,_,c,_ in rows); won=sum(any(win in r for r in c) for _,win,c,_ in rows)
    ch=sum(len(c)/n for _,_,c,n in rows)
    print(name,'races',len(rows),'races with a holder',sum(bool(c) for *_,c,_ in [(a,b,c,d) for a,b,c,d in rows]),'picks',picks,'won',won,'by chance %.1f'%ch)
    if name=='top3all':
        for race,win,c,n in rows:
            if c: print('   ',race,sorted(c),'WON' if any(win in r for r in c) else '')
