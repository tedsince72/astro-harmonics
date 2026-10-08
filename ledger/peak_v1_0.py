"""contacts that PEAK at the off: sky->natal (certain natal body), score >=90 at the off, at least as high as at
+/-2 min, and lower at both -30 and +30 (so the contact culminates at the race time)."""
import sys; sys.path.insert(0,'/home/claude/ledger')
from readrace import Race, sep, FN, FAMS, STARS, FAST, FASTNATAL, results
R=sys.argv[1]; rc=Race(R); res=results(R)
order=sorted(rc.charts,key=lambda c:int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
topb={b for k in rc.byrank[:12] for b in k}
print('PEAKING AT THE OFF –',R)
for c in order:
    out=[]
    for sd,tab in rc.charts[c].items():
        P=rc.natal[tab]
        for s in rc.sky:
            if s in FAST or s in STARS or s=='equator': continue
            for n in P:
                if n in STARS or n in FASTNATAL: continue
                for m in ('RA','Dec'):
                    v=sep(rc.sky[s],P[n],m)
                    f=max(FAMS,key=lambda k:FN[k](v,m)); s0=FN[f](v,m)
                    if s0<90: continue
                    sc={k:FN[f](sep(rc.S3[s][k],P[n],m),m) for k in ('m30','m2','p2','p30')}
                    if s0>=sc['m2']-1e-9 and s0>=sc['p2']-1e-9 and sc['m30']<s0-5 and sc['p30']<s0-5:
                        out.append(f"{sd} {s}{'*' if s in topb else ''}→{n}{'B' if n in rc.busy else ''} {m} {v:.4f} {f[:6]} {sc['m30']:.0f}/{s0:.0f}/{sc['p30']:.0f}")
    print(f"  {res[c]['finish']:>3} {rc.names[c][0]:18} {res[c]['sp']:>5} {len(out)}: "+'; '.join(out))
