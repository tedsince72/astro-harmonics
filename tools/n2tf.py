"""n2t.py BODY [NATALBODY]: Frankel natal (12:00, P01) to transit distances at KO, mid (21:43) and FT, with number check."""
import csv, math, sys
B=sys.argv[1]; NB=sys.argv[2] if len(sys.argv)>2 else B
SK={}
for r in csv.DictReader(open('/home/claude/ledger/sky/20120619_ascot_1434__SKYM.csv')):
    if r['body']==B: SK[int(r['minute'])]=(float(r['ra']),float(r['dec']))
H={}
for r in csv.DictReader(open('/home/claude/ledger/allpos/20120619_ascot_1434__NATAL_HOURLY.csv')):
    if r['tab']=='P01' and r['body']==NB and r['ra']: H[int(r['hour'])]=(float(r['ra']),float(r['dec']))
n=H[12]
def ra(x,y): d=abs(x-y)%360; return min(d,360-d)
def sky(p,q):
    r1,d1,r2,d2=map(math.radians,(p[0],p[1],q[0],q[1])); return math.degrees(math.acos(max(-1,min(1,math.sin(d1)*math.sin(d2)+math.cos(d1)*math.cos(d2)*math.cos(r1-r2)))))
phi=(1+5**.5)/2
def num(x,t=float(sys.argv[3]) if len(sys.argv)>3 else 0.002):
    o=[]
    if abs(x-round(x))<=t and round(x)>0: o.append(f"whole {round(x)}")
    if abs(x*9-round(x*9))<=t*9: o.append(f"{round(x*9)}/9")
    k=round(x/phi)
    if k>0 and abs(x-k*phi)<=t: o.append(f"{k}φ")
    k=round(x/2**.5)
    if k>0 and abs(x-k*2**.5)<=t: o.append(f"{k}√2")
    for e in range(-3,12):
        for c in (1,10):
            if abs(x-c*phi**e)<=t: o.append(f"{'10' if c==10 else ''}φ^{e}")
    return ', '.join(o)
print(f"natal {NB} 12:00 (00:00 {H[0][0]:.4f}/{H[0][1]:.4f}, 24:00 {H[max(H)][0]:.4f}/{H[max(H)][1]:.4f})  RA {n[0]:.4f} Dec {n[1]:.4f}")
for m,l in ((0,'14:34 off'),(2,'14:36 fin')):
    p=SK[m]; v={'RA':ra(p[0],n[0]),'Dec':abs(p[1]-n[1]),'Flat':math.hypot(ra(p[0],n[0]),p[1]-n[1]),'Sky':sky(p,n)}
    print(f"{l:5} transit {B} RA {p[0]:.4f} Dec {p[1]:.4f} | "+'  '.join(f"{k} {x:.4f}{' ['+num(x)+']' if num(x) else ''}" for k,x in v.items()))
