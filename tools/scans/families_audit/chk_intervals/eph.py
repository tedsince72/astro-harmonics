import swisseph as swe, openpyxl, os
swe.set_ephe_path(os.path.expanduser('~/astronomy-project/ephe'))
swe.set_topo(-1.6247, 54.9832, 35)
INP='/Users/eddieplace/astro-harmonics/reference/classic/race_batch_20220102_newcastle_aw_1330.xlsx'
wb=openpyxl.load_workbook(INP,data_only=True)
T={r[1]:(r[4],r[8]) for r in wb['TRANS'].iter_rows(min_row=2,values_only=True)}
IDS={'Sun':0,'Moon':1,'Mercury':2,'Venus':3,'Mars':4,'Jupiter':5,'Saturn':6,'Uranus':7,'Neptune':8,'Pluto':9,'Rahu':swe.TRUE_NODE,'Chiron':swe.CHIRON,'Ceres':swe.CERES,'Pallas':swe.PALLAS,'Juno':swe.JUNO,'Vesta':swe.VESTA}
def pos(name, jd, flags):
    if name.endswith('_B') or name in ('Aldebaran','Antares','Regulus','Fomalhaut'):
        st=name[:-2] if name.endswith('_B') else name
        x,_,_=swe.fixstar2_ut(st, jd, flags); return x[0],x[1]
    x,_=swe.calc_ut(jd, IDS[name], flags); return x[0],x[1]
def run(flags, mins=0):
    jd=swe.julday(2022,1,2,13.5+mins/60)
    out={}
    for n in list(IDS)+[k for k in T if k.endswith('_B')]:
        try: out[n]=pos(n,jd,flags)
        except Exception as e: out[n]=None
    return out
if __name__=="__main__" and False:
    base=swe.FLG_SWIEPH|swe.FLG_EQUATORIAL
    for lab,f in [('geo',base),('topo',base|swe.FLG_TOPOCTR),('geo+mean',base)]:
        o=run(f); bad=[(n,round(o[n][0]-T[n][0],5),round(o[n][1]-T[n][1],5)) for n in o if o[n] and (abs(((o[n][0]-T[n][0]+180)%360)-180)>1e-4 or abs(o[n][1]-T[n][1])>1e-4)]
        print(lab,len(o),'bad',bad[:12])

FL=swe.FLG_SWIEPH|swe.FLG_EQUATORIAL|swe.FLG_TOPOCTR|swe.FLG_J2000
EXTRA={'Eris':136199,'Sedna':90377,'Haumea':136108,'Makemake':136472,'Gonggong':225088,'Orcus':90482,'Quaoar':50000}
def sky(mins):
    jd=swe.julday(2022,1,2,13.5+mins/60)
    o=run(FL,mins)
    for n,k in EXTRA.items():
        try: x,_=swe.calc_ut(jd, swe.AST_OFFSET+k, FL); o[n]=(x[0],x[1])
        except Exception as e: o[n]=None
    try: x,_=swe.calc_ut(jd, swe.ISIS, FL); o['Transpluto']=(x[0],x[1])
    except Exception: o['Transpluto']=None
    # angles: ecliptic of date -> equatorial of date -> compare
    cusps,ascmc=swe.houses_ex(jd,54.9832,-1.6247,b'P')
    eps=swe.calc_ut(jd,swe.ECL_NUT)[0][0]
    sun=swe.calc_ut(jd,0)[0][0]; moon=swe.calc_ut(jd,1,swe.FLG_TOPOCTR)[0][0]
    asc,mc,vx=ascmc[0],ascmc[1],ascmc[3]
    def eq(lon):
        x=swe.cotrans((lon,0,1),-eps); return (x[0],x[1])
    o['Ascendant']=eq(asc); o['Midheaven']=eq(mc); o['Vertex']=eq(vx)
    o['Part_of_Fortune']=eq((asc+moon-sun)%360); o['Part_of_Spirit']=eq((asc+sun-moon)%360)
    return o
if __name__=="__main__" and False:
    o=sky(0)
    for n in o:
        if n in T and o[n]:
            d=(round(((o[n][0]-T[n][0]+180)%360)-180,5),round(o[n][1]-T[n][1],5))
            if max(map(abs,d))>1e-4: print('BAD',n,d)
    print('missing',[n for n in T if n not in o or o[n] is None])
