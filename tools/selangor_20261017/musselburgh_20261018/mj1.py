import sys,re; sys.path.insert(0,sys.argv[1])
from rc import *
load_file('reference/classic/race_batch_20210825_musselburgh_1345_jupiter_tables.xlsx')
NOTES='/root/.claude/uploads/9419e2bd-a69d-5277-b65b-c6f29372b0af/d1f5d41b-race_batch_20210825_musselburgh_1345_jupiter_tables_horse_jockey_notes'
t=open(NOTES,encoding='utf-8').read().replace('\r','')
cells=[c.strip() for c in t.replace('\n','\t').split('\t')]
codes=re.compile(r'^(T\d+R?|TIMELINE H|TIMELINE J|LONG TIMELINE H|LONG TIMELINE J)$')
recs=[];cur=None
for c in cells:
    if codes.match(c):
        if cur: recs.append(cur)
        cur=[c]
    elif cur is not None and c!='': cur.append(c)
recs.append(cur)
R=rows('P07')
def num(x):
    try: return float(x)
    except: return None
def match(rec):
    tab=rec[0]
    if tab.startswith('TIMELINE') or tab.startswith('LONG'): return 'tl'
    for i,r in enumerate(R,1):
        if r[0]!=tab: continue
        vals=[str(v) for v in r[1:5] if v is not None]
        if all(any(p==v for v in vals) for p in rec[1:3] if num(p) is None) :
            # check first numeric
            fn=next((num(p) for p in rec[1:] if num(p) is not None),None)
            rn=[v for v in r[1:] if isinstance(v,(int,float))]
            if fn is None or (rn and abs(rn[0]-fn)<1e-6): return (i,r)
    return None
bad=0
for k,rec in enumerate(recs,1):
    m=match(rec)
    if m is None: bad+=1; print('NO MATCH',k,rec[:4])
print('records',len(recs),'unmatched',bad)
