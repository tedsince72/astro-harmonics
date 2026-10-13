import swisseph as swe, numpy as np, math
from eph import T, run, FL, EXTRA
swe.set_topo(-1.6247, 54.9832, 35)
def vec(ra,dec):
    r,d=math.radians(ra),math.radians(dec); return np.array([math.cos(d)*math.cos(r),math.cos(d)*math.sin(r),math.sin(d)])
def rot(jd):
    A=[];B=[]
    for b in range(0,10):
        f=swe.FLG_SWIEPH|swe.FLG_EQUATORIAL
        x,_=swe.calc_ut(jd,b,f); y,_=swe.calc_ut(jd,b,f|swe.FLG_J2000)
        A.append(vec(x[0],x[1])); B.append(vec(y[0],y[1]))
    A=np.array(A);B=np.array(B)
    U,S,Vt=np.linalg.svd(A.T@B); d=np.sign(np.linalg.det(U@Vt))
    R=(U@np.diag([1,1,d])@Vt).T
    return R
def back(v):
    ra=math.degrees(math.atan2(v[1],v[0]))%360; dec=math.degrees(math.asin(v[2])); return ra,dec
def sky(mins):
    jd=swe.julday(2022,1,2,13.5+mins/60)
    o=run(FL,mins)
    o['Pleiades_B']=tuple(swe.fixstar2_ut('Alcyone',jd,FL)[0][:2])
    for n,k in EXTRA.items():
        x,_=swe.calc_ut(jd, swe.AST_OFFSET+k, FL); o[n]=(x[0],x[1])
    R=rot(jd)
    cusps,ascmc=swe.houses_ex(jd,54.9832,-1.6247,b'P')
    eps=swe.calc_ut(jd,swe.ECL_NUT)[0][0]
    for n,l in (('Ascendant',ascmc[0]),('Midheaven',ascmc[1]),('Vertex',ascmc[3])):
        x=swe.cotrans((l,0,1),-eps); o[n]=back(R@vec(x[0],x[1]))
    for n,s in (('Part_of_Fortune',1),('Part_of_Spirit',-1)):
        a,m,su=o['Ascendant'],o['Moon'],o['Sun']
        o[n]=((a[0]+s*(m[0]-su[0]))%360, a[1]+s*(m[1]-su[1]))
    return o
if __name__=='__main__':
    o=sky(0)
    for n in o:
        if n in T and o[n]:
            d=(round(((o[n][0]-T[n][0]+180)%360)-180,6),round(o[n][1]-T[n][1],6))
            if max(map(abs,d))>1e-4: print('BAD',n,d)
    print('missing',[n for n in T if n not in o])
