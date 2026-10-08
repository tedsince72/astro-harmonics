"""numcheck RACE OFF DUR BODY [TOL]: is the body's Dec / RA, or its RA and Dec distance to each star, itself a special number?
families: kφ, φ^n, k√2, k/9 (ninths), whole numbers. TOL absolute degrees (default 0.002). Prints the chance rate."""
import sys
BODY=sys.argv[4]; TOL=float(sys.argv[5]) if len(sys.argv)>5 else 0.002; sys.argv=sys.argv[:4]
src=open('/home/claude/lattice/layer1_tuned.py').read(); exec(src.split('# transit chords')[0])
PHI=(1+5**.5)/2; R2=2**.5
def special(x):
    out=[]
    k=round(x/PHI)
    if k>0 and abs(x-k*PHI)<=TOL: out.append(f"{k}φ ({k*PHI:.4f})")
    for n in range(2,12):
        if abs(x-PHI**n)<=TOL: out.append(f"φ^{n} ({PHI**n:.4f})")
        if abs(x-10*PHI**n)<=TOL: out.append(f"10φ^{n} ({10*PHI**n:.4f})")
    k=round(x/R2)
    if k>0 and abs(x-k*R2)<=TOL: out.append(f"{k}√2 ({k*R2:.4f})")
    k=round(x*9)
    if k%9 and abs(x-k/9)<=TOL: out.append(f"{k}/9 ({k/9:.4f})")
    k=round(x)
    if k>0 and abs(x-k)<=TOL: out.append(f"whole {k}")
    return out
def scan(t):
    P=pos(BODY,t); vals=[('Dec (from Equator)',abs(P[1])),('RA',P[0])]
    for s in RN:
        if s in ('Equator','CourseLat'): continue
        vals.append((f'RA to {s}',dist(P,REF[s],'RA'))); vals.append((f'Dec to {s}',dist(P,REF[s],'Dec')))
    vals.append(('Dec to CourseLat',dist(P,REF['CourseLat'],'Dec')))
    return vals
vals=scan(t0); n=len(vals)
# chance: per value, P(hit) ~ 2*TOL*(1/φ + 1/√2 + 8/9 + 1)  (ninths not whole: 8 per unit)
pp=2*TOL*(1/PHI+1/R2+1); p9=2*TOL*8; print(f"{BODY} at the off: {n} values tested, tolerance ±{TOL}°, chance hits expected: φ/√2/whole ≈ {n*pp:.2f}, ninths ≈ {n*p9:.2f}")
v1=dict(scan(t1))
for lab,x in vals:
    s=special(x)
    if s: print(f"   {lab:22s} {x:10.4f}  = {', '.join(s)}   (finish {v1[lab]:.4f})")
