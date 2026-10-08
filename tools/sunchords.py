"""sunchords RACE OFF DUR BODY: every chord BODY makes with the Layer-1 points (stars, equator, course lat) at the off, with distances, families, exact time."""
import sys
BODY=sys.argv[4]; sys.argv=sys.argv[:4]
src=open('/home/claude/lattice/layer1_tuned.py').read(); exec(src.split('# transit chords')[0])
FAMS={'PERFECT':['1','2','3/2','4/3','3','4'],'IMPERFECT':['5/4','6/5','5/3','8/5','5/2','8/3','9/4'],
 'DISSONANT':['√2','1+1/√2','9/8','16/9','9/5','15/8','16/15'],'SEPTIMAL':['7/4','7/3','7/2','7/5','7/6','8/7'],
 'HARMONIC':['5','6','7','8','9'],'HIGH':['11/5','11/6','11/3','11/8','11/4','13/5','13/8','13/4'],
 'PHI':['φ','φ²','φ³','1+√2','φ√5','2−1/φ','φ³+1','2/φ']}
F={k:f for f,ks in FAMS.items() for k in ks}
P0=pos(BODY,t0); print(f"{BODY} at the off: RA {P0[0]:.3f} Dec {P0[1]:.3f}")
out=[]
for a,c in itertools.combinations(RN,2):
    for mm in ('RA','Dec','Flat','Sky'):
        r=tri(P0,REF[a],REF[c],mm)
        if r and r[1]<=0.0015:
            d=[dist(REF[a],REF[c],mm),dist(P0,REF[a],mm),dist(P0,REF[c],mm)]
            rs=[max(d[0],d[1])/min(d[0],d[1]),max(d[0],d[2])/min(d[0],d[2]),max(d[1],d[2])/min(d[1],d[2])]
            fam=', '.join(f"{iv(x)[0]} {F.get(iv(x)[0],'?')}" for x in rs)
            x,xd,edge=exact_t(BODY,a,c,mm)
            out.append((mm,r[1],a,c,d,ctype(r[0]),fam,when(x,edge,BODY)))
for mm in ('RA','Dec','Flat','Sky'):
    L=sorted([o for o in out if o[0]==mm],key=lambda o:o[1])
    print(f"\n{mm}: {len(L)} chords")
    for mm_,dv,a,c,d,typ,fam,w in L:
        print(f"  {a}–{c:12s} base {d[0]:8.3f} | {BODY}–{a} {d[1]:8.3f} | {BODY}–{c} {d[2]:8.3f}  {typ:14s} {dv*100:.3f}%  [{fam}]  {w}")
# ---- the whole day: chords that come exact on the race day (Sun at its rate)
print(f"\nTHE WHOLE DAY (00:00–24:00): {BODY}'s chords that come exact during the race day")
day=[]
for a,c in itertools.combinations(RN,2):
    for mm in ('RA','Dec','Flat','Sky'):
        best=(9,None,None)
        for dd in np.arange(-t0/1440,(1440-t0)/1440+1e-9,10/1440):
            r=tri(moved(P0,BODY,dd),REF[a],REF[c],mm)
            if r and r[1]<best[0]: best=(r[1],dd,ctype(r[0]))
        if best[1] is None or best[0]>0.0015: continue
        x,xd,edge=exact_t(BODY,a,c,mm)
        if x is None or not (-t0/1440 <= x <= (1440-t0)/1440): continue
        P=moved(P0,BODY,x); d=[dist(REF[a],REF[c],mm),dist(P,REF[a],mm),dist(P,REF[c],mm)]
        day.append((x,mm,a,c,d,best[2],xd))
for x,mm,a,c,d,typ,xd in sorted(day):
    print(f"  {hm(t0+x*1440)}  {mm:4s} {a}–{c:12s} base {d[0]:8.3f} | to {a} {d[1]:8.3f} | to {c} {d[2]:8.3f}  {typ:14s} {xd*100:.3f}%")
