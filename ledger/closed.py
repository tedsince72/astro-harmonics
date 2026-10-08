"""closed loop: natal body B carries the number of sky pair #k (natal-natal / HxJ, certain) AND pair #k lands on B
(either chart) - imprint and moment on the same pair and the same body."""
import sys, collections; sys.path.insert(0,'/home/claude/ledger')
from readrace import Race, sep, STARS, NODES, FASTNATAL, results
R=sys.argv[1]; rc=Race(R); rc.build(); res=results(R)
order=sorted(rc.charts,key=lambda c:int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
def hr(tab,b): return rc.hourly[tab].get(b) or [rc.natal[tab][b]]*25
out=[]
for c in order:
    th,tj=rc.charts[c]['H'],rc.charts[c]['J']; H=rc.natal[th]; J=rc.natal[tj]; hits=[]
    for k in rc.byrank[:12]:
        rk=rc.pairs[k]['rank']
        landed={ld['C'] for sides in [rc.land[c].get(k,{})] for ls in sides.values() for ld in ls}
        if not landed: continue
        for m,f,s,v0,*_ in rc.pairs[k]['entries']:
            for sc in (0.1,1,10):
                t=v0*sc
                for tag,A,B,ta,tb in (('H',H,H,th,th),('J',J,J,tj,tj),('HxJ',H,J,th,tj)):
                    for x in A:
                        for y in B:
                            if tag!='HxJ' and x>=y: continue
                            if (x in STARS and y in STARS) or 'Moon' in (x,y): continue
                            if {x,y}&FASTNATAL:
                                AA,BB=hr(ta,x),hr(tb,y)
                                vv=[sep(p,q,m) for p in AA for q in BB] if tag=='HxJ' else [sep(p,q,m) for p,q in zip(AA,BB)]
                                if max(vv)-min(vv)>0.02: continue
                            v=sep(A[x],B[y],m)
                            if abs(v-t)<=0.005*max(1,sc):
                                for b in (x,y):
                                    if b in landed: hits.append(f"#{rk} → {b} (carries {tag} {x}–{y} {m} {v:.4f}{'' if sc==1 else ' x'+str(sc)})")
    print(f"  {res[c]['finish']:>3} {rc.names[c][0]:18} {res[c]['sp']:>6}: "+('; '.join(sorted(set(hits))) or '-'))
