# Every distance (RA, Dec, Flat, Sky; Dec to Equator) in TT, NN and TN that equals a target value (and 1/2, 2x, 3x) within TOL - Eddie's workbook
import sys,openpyxl,math,itertools
F,V,TOL=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]); wb=openpyxl.load_workbook(F,data_only=True)
BOD=['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto','Moon']
def load(t,natal):
    P={}
    for r in list(wb[t].iter_rows(values_only=True))[1:]:
        b=r[1]
        if b in BOD and not(natal and b=='Moon'): P[b]=(float(r[4]),float(r[8]))
        elif isinstance(b,str) and b.endswith('_B'): P[b[:-2]+'*']=(float(r[4]),float(r[8]))
    return P
def ms(a,b):
    dra=(a[0]-b[0]+180)%360-180; dd=a[1]-b[1]; r1,d1,r2,d2=map(math.radians,(a[0],a[1],b[0],b[1]))
    hv=math.sin((d2-d1)/2)**2+math.cos(d1)*math.cos(d2)*math.sin((r2-r1)/2)**2
    return {'RA':abs(dra),'Dec':abs(dd),'Flat':math.hypot(dra,dd),'Sky':math.degrees(2*math.asin(math.sqrt(hv)))}
T={'×1':V,'×½':V/2,'×2':2*V,'×3':3*V}
SKY=load('TRANS',0); NAT={wb[t].cell(2,1).value:load(t,1) for t in wb.sheetnames[1:]}
L=[]
def go(tag,P,Q,same):
    it=itertools.combinations(sorted(P),2) if same else itertools.product(sorted(P),sorted(Q))
    for a,b in it:
        if (a.endswith('*') and b.endswith('*')) or {a,b}=={'Rahu','Ketu'}: continue
        for mm,v in ms(P[a],(P if same else Q)[b]).items():
            for k,t in T.items():
                if abs(v-t)<=TOL: L.append((k,abs(v-t),tag,mm,a,b,v))
    if same:
        for a in P:
            if a!='Ketu':
                for k,t in T.items():
                    if abs(abs(P[a][1])-t)<=TOL: L.append((k,abs(abs(P[a][1])-t),tag,'Dec',a,'Equator',abs(P[a][1])))
go('TT sky',SKY,None,True)
for n,N in NAT.items(): go(f'NN {n}',N,None,True); go(f'TN sky→{n}',SKY,N,False)
print(f"target {V} (½ {V/2:.4f}, 2× {2*V:.4f}, 3× {3*V:.4f}) ±{TOL}")
for x in sorted(L,key=lambda x:(list(T).index(x[0]),x[1])): print(f"  {x[0]:3s} {x[1]:.4f}  {x[2]:22s} {x[3]:4s} {x[4]}–{x[5]:12s} {x[6]:.4f}{'  MOON' if 'Moon' in x[4:6] else ''}")
