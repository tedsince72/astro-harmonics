import swisseph as swe, numpy as np, math, os, openpyxl
swe.set_ephe_path(os.path.expanduser('~/astronomy-project/ephe'))
LAT,LON,ELEV=51.4119,-0.3712,20
swe.set_topo(LON,LAT,ELEV)
Y,M,D,H=2026,10,12,18.25   # 19:15 BST = 18:15 UTC
INP='/Users/eddieplace/astro-harmonics/reference/classic/race_batch_20261012_kempton_aw_1915.xlsx'
wb=openpyxl.load_workbook(INP,data_only=True)
T={r[1]:(r[4],r[8]) for r in wb['TRANS'].iter_rows(min_row=2,values_only=True) if r[3]=='transit_self'}
IDS={'Sun':0,'Moon':1,'Mercury':2,'Venus':3,'Mars':4,'Jupiter':5,'Saturn':6,'Uranus':7,'Neptune':8,'Pluto':9,'Rahu':swe.TRUE_NODE,'Chiron':swe.CHIRON,'Ceres':swe.CERES,'Pallas':swe.PALLAS,'Juno':swe.JUNO,'Vesta':swe.VESTA}
EXTRA={'Eris':136199,'Sedna':90377,'Haumea':136108,'Makemake':136472,'Gonggong':225088,'Orcus':90482,'Quaoar':50000}
FL=swe.FLG_SWIEPH|swe.FLG_EQUATORIAL|swe.FLG_TOPOCTR|swe.FLG_J2000
def sky(mins):
    jd=swe.julday(Y,M,D,H+mins/60); o={}
    for n,i in IDS.items():
        x,_=swe.calc_ut(jd,i,FL); o[n]=(x[0],x[1])
    for n,k in EXTRA.items():
        x,_=swe.calc_ut(jd,swe.AST_OFFSET+k,FL); o[n]=(x[0],x[1])
    try:
        x,_=swe.calc_ut(jd,swe.ISIS,FL); o['Transpluto']=(x[0],x[1])
    except Exception: pass
    return o
if __name__=='__main__':
    o=sky(0)
    for n in o:
        if n in T:
            d=(round(((o[n][0]-T[n][0]+180)%360)-180,6),round(o[n][1]-T[n][1],6))
            print(n,d)
    print('TRANS bodies',sorted(T))

def vec(ra,dec):
    r,d=math.radians(ra),math.radians(dec); return np.array([math.cos(d)*math.cos(r),math.cos(d)*math.sin(r),math.sin(d)])
def rot(jd):
    A=[];B=[]
    for b in range(0,10):
        f=swe.FLG_SWIEPH|swe.FLG_EQUATORIAL
        x,_=swe.calc_ut(jd,b,f); y,_=swe.calc_ut(jd,b,f|swe.FLG_J2000)
        A.append(vec(x[0],x[1])); B.append(vec(y[0],y[1]))
    A=np.array(A);B=np.array(B)
    U,S_,Vt=np.linalg.svd(A.T@B); d=np.sign(np.linalg.det(U@Vt))
    return (U@np.diag([1,1,d])@Vt).T
def back(v):
    return math.degrees(math.atan2(v[1],v[0]))%360, math.degrees(math.asin(v[2]))
STARMAP={'Pleiades':'Alcyone'}
def skyfull(mins):
    jd=swe.julday(Y,M,D,H+mins/60); o=sky(mins)
    for n in T:
        nm=n[:-2] if n.endswith('_B') else n
        if n.endswith('_B') or n in ('Aldebaran','Regulus','Antares','Fomalhaut'):
            try: o[n]=tuple(swe.fixstar2_ut(STARMAP.get(nm,nm),jd,FL)[0][:2])
            except Exception as e: print('star fail',n,e)
    R=rot(jd)
    cusps,ascmc=swe.houses_ex(jd,LAT,LON,b'P')
    eps=swe.calc_ut(jd,swe.ECL_NUT)[0][0]
    for n,l in (('Ascendant',ascmc[0]),('Midheaven',ascmc[1]),('Vertex',ascmc[3])):
        x=swe.cotrans((l,0,1),-eps); o[n]=back(R@vec(x[0],x[1]))
    for n,s in (('Part_of_Fortune',1),('Part_of_Spirit',-1)):
        a,m,su=o['Ascendant'],o['Moon'],o['Sun']
        o[n]=((a[0]+s*(m[0]-su[0]))%360, a[1]+s*(m[1]-su[1]))
    return o
