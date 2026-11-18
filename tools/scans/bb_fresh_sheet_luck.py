"""Luck check for bb_fresh_sheet (18 Nov 2026): a random runner as the winner in every race, T times (env, default 200); the best p and the count of p < 0.001 for singles / pairs / triples vs the real winners. Read-only."""
import sys, random, itertools
T=int(__import__("os").environ.get("T","200"))
sys.path.insert(0,'tools/scans'); import bb_fresh_sheet as F, bb_scan_negatives as N
data=[]
for race,win in N.RACES:
    runners,hh=F.holders(race); data.append((runners,hh,next(r for r in runners if win in r)))
rules=sorted({x for _,hh,_ in data for s in hh.values() for x in s})
# precompute holder sets per combo
combos={k:[] for k in (1,2,3)}
for k in (1,2,3):
    for c in itertools.combinations(rules,k):
        cs=set(c); hold=[]
        for i,(runners,hh,w) in enumerate(data):
            for r,s in hh.items():
                if cs<=s: hold.append((i,r))
        if len(hold)>=3: combos[k].append(hold)
def best(winners):
    res={}
    for k,L in combos.items():
        b=1; cnt=0
        for hold in L:
            w=sum(1 for i,r in hold if winners[i]==r)
            if w<2: continue
            p=F.tail([1/len(data[i][0]) for i,_ in hold],w)
            b=min(b,p); cnt+= p<0.001
        res[k]=(b,cnt)
    return res
real=best([w for _,_,w in data]); print('real',real)
random.seed(1); out=[]
for t in range(T):
    out.append(best([random.choice(runners) for runners,_,_ in data]))
for k in (1,2,3):
    bs=sorted(o[k][0] for o in out); cs=[o[k][1] for o in out]
    print(k,'best p median',bs[len(bs)//2],'share beating real',sum(b<=real[k][0] for b in bs)/len(bs),'count p<0.001 mean',sum(cs)/len(cs),'real',real[k][1])
