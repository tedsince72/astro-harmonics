"""merc_natal.py RACE OFF DUR_S - transit Mercury – each chart's natal Mercury – star chords, off-30 to off+15, exact time."""
import sys
src=open('/home/claude/lattice/race_read.py').read().split("BODIES = [")[0]
exec(src)
META=list(csv.reader(open(f"{POSD}/{RACE}__META.csv")))
tabs={r[0]:(r[1],r[2],r[3]) for r in META if r and r[0].startswith('P') and r[0][1:].isdigit()}
NM={}
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour']=='12' and r['body']=='Mercury': NM[r['tab']]=(float(r['ra']),float(r['dec']))
fin={}
for p in ('/home/claude/pinpoint_blind_kit/reference/profiles.csv','/home/claude/scored/profiles_test_scored.csv'):
    for r in csv.DictReader(open(p)):
        if r['race']==RACE: fin[r['cloth']]=(r['finish'],r['sp'])
X0=pos('Mercury',t0); print(f"{RACE} off {OFF} finish {hm(t1)}\nTransit Mercury at off RA {X0[0]:.3f} Dec {X0[1]:+.3f}")
ts=np.arange(t0-30,t0+15+1e-9,5/60)
for tab,(role,cloth,nm) in sorted(tabs.items(),key=lambda x:(int(fin.get(x[1][1],('99',))[0] or 99),x[1][0]!='horse')):
    NP=NM[tab]; f=fin.get(cloth,('?','?'))
    print(f"\n[{f[0]}] {role} {nm} {f[1]}  natal Mercury RA {NP[0]:.3f} Dec {NP[1]:+.3f}")
    life={}
    for t in ts:
        X=pos('Mercury',t)
        for c in N:
            for mm in ('RA','Dec','Flat','Sky'):
                d=[dist(X,NP,mm),dist(X,S[c],mm),dist(NP,S[c],mm)]
                if min(d)<0.05: continue
                rs=[max(d[0],d[1])/min(d[0],d[1]),max(d[0],d[2])/min(d[0],d[2]),max(d[1],d[2])/min(d[1],d[2])]
                dv=max(iv(x)[1] for x in rs)
                if dv<=0.0015:
                    L=life.setdefault((mm,c),{'typ':ctype(d),'ts':[],'best':(9,0,None)}); L['ts'].append(t)
                    if dv<L['best'][0]: L['best']=(dv,t,d)
    for (mm,c),L in sorted(life.items(),key=lambda x:x[1]['best'][1]):
        dv,tb,d=L['best']; a,b=min(L['ts']),max(L['ts'])
        flag=' <<RACE' if t0-2<=tb<=t1 else ''
        print(f"   {mm:4s} {L['typ']:14s} {c:13s} in {a-t0:+6.2f} out {b-t0:+6.2f} exact {hm(tb)} ({tb-t0:+.2f}) dev {dv*100:.3f}%{flag}")
