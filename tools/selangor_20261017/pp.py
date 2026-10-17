import openpyxl,glob,itertools,math,sys,random,collections
import numpy as np
U='/root/.claude/uploads/a6920965-38c7-5676-b509-936bc1207077/'
PHI=(1+5**.5)/2
IV=[1,2,1.5,4/3,3,4,1.25,1.2,5/3,1.6,2.5,8/3,9/4,2**.5,1+2**-.5,9/8,16/9,9/5,15/8,16/15,7/4,7/3,7/2,7/5,7/6,8/7,5,6,7,8,9,11/5,11/6,11/3,11/8,11/4,13/5,13/8,13/4,PHI,PHI**2,PHI**3,1+2**.5]
IVa=np.array(IV)
def isiv(r): return np.any(np.abs(r[...,None]-IVa)<=0.0015*IVa,axis=-1)
W=lambda x:(x+180)%360-180
races={'12:15':'7566745e','12:45':'2673848e','13:15':'e96aa387','13:45':'afee33f2','14:15':'929b5b49','14:45':'8a883cbf'}
def load(pt,stars,m):
    # pt scalar coord (RA or Dec); stars dict name->(ra,dec)
    names=list(stars); v=np.array([stars[n][0] if m=='RA' else stars[n][1] for n in names])
    d=np.abs(W(v-pt)) if m=='RA' else np.abs(v-pt)
    cnt=0; who=[]
    for i,j in itertools.combinations(range(len(names)),2):
        d3=abs(W(v[i]-v[j])) if m=='RA' else abs(v[i]-v[j])
        a,b=d[i],d[j]
        if min(a,b)<=0.05 or d3<0.05: continue
        rs=np.array([max(a,b)/min(a,b),max(a,d3)/min(a,d3),max(b,d3)/min(b,d3)])
        if isiv(rs).all(): cnt+=1; who.append(f'{names[i]}–{names[j]}')
    return cnt,who
out=collections.defaultdict(list)
for hhmm in sys.argv[1:]:
    wb=openpyxl.load_workbook(glob.glob(U+races[hhmm]+'-*jupiter_tables.xlsx')[0],read_only=True)
    rows=[r for r in wb['POSITIONS'].iter_rows(values_only=True) if r and r[2] in('S','H') and r[4] in('body','star')]
    sky={r[3]:(r[5],r[6]) for r in rows if r[2]=='S'}
    sstars={k:v for k,v in sky.items() if [x for x in rows if x[2]=='S' and x[3]==k][0][4]=='star'}
    # background
    random.seed(1); bg={'RA':[], 'Dec':[]}
    for _ in range(600):
        bg['RA'].append(load(random.uniform(0,360),sstars,'RA')[0]); bg['Dec'].append(load(random.uniform(-35,90),sstars,'Dec')[0])
    th={m:np.percentile(bg[m],99) for m in bg}
    print(f'######## {hhmm}  background mean RA {np.mean(bg["RA"]):.1f} Dec {np.mean(bg["Dec"]):.1f}; 99% RA {th["RA"]:.0f} Dec {th["Dec"]:.0f}')
    for b,(ra,de) in sky.items():
        if b in sstars: continue
        for m,c in (('RA',ra),('Dec',de)):
            n,who=load(c,sstars,m)
            if n>=th[m]: print(f'  SKY {b} {m} {c:.3f}: {n}  {", ".join(who)}')
    runners=sorted({(r[0],r[1]) for r in rows if r[2]=='H'})
    for pid,name in runners:
        H={r[3]:(r[5],r[6],r[4]) for r in rows if r[2]=='H' and r[0]==pid}
        hst={k:(v[0],v[1]) for k,v in H.items() if v[2]=='star'}
        for b,(ra,de,kind) in H.items():
            if kind!='body': continue
            for m,c in (('RA',ra),('Dec',de)):
                n,who=load(c,hst,m)
                if n>=th[m]: print(f'  {pid} {name.split(" / ")[0]} H {b} {m} {c:.3f}: {n}  {", ".join(who)}')
