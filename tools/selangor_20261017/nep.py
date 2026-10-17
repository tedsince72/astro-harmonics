import openpyxl,glob,itertools,sys,collections
import numpy as np
U='/root/.claude/uploads/a6920965-38c7-5676-b509-936bc1207077/'
PHI=(1+5**.5)/2
IV=[1,2,1.5,4/3,3,4,1.25,1.2,5/3,1.6,2.5,8/3,9/4,2**.5,1+2**-.5,9/8,16/9,9/5,15/8,16/15,7/4,7/3,7/2,7/5,7/6,8/7,5,6,7,8,9,11/5,11/6,11/3,11/8,11/4,13/5,13/8,13/4,PHI,PHI**2,PHI**3,1+2**.5]
W=lambda x:(x+180)%360-180
def dev(r): return min(abs(r-v)/v for v in IV)
def chord(p,a,b):
    d1,d2,d3=abs(W(p-a)),abs(W(p-b)),abs(W(a-b))
    if min(d1,d2)<=0.05 or d3<0.05: return None
    ds=[dev(max(x,y)/min(x,y)) for x,y in ((d1,d2),(d1,d3),(d2,d3))]
    return max(ds) if max(ds)<=0.0015 else None
races={'12:15':'7566745e','12:45':'2673848e','13:15':'e96aa387','13:45':'afee33f2','14:15':'929b5b49','14:45':'8a883cbf'}
for hh in sys.argv[1:]:
    wb=openpyxl.load_workbook(glob.glob(U+races[hh]+'-*jupiter_tables.xlsx')[0],read_only=True)
    rows=[r for r in wb['POSITIONS'].iter_rows(values_only=True) if r and r[2] in('S','H') and r[4] in('body','star')]
    S={r[3]:r[5] for r in rows if r[2]=='S'}; Sst=[r[3] for r in rows if r[2]=='S' and r[4]=='star']
    nep=S['Neptune']
    bases=[(a,b,chord(nep,S[a],S[b])) for a,b in itertools.combinations(Sst,2)]
    bases=[x for x in bases if x[2] is not None]
    print(f'######## {hh}  sky Neptune RA {nep:.3f}: {len(bases)} star bases: '+', '.join(f'{a}–{b} ({c*100:.3f}%)' for a,b,c in bases))
    runners=sorted({(r[0],r[1].split(' / ')[0]) for r in rows if r[2]=='H'})
    per={}
    for pid,name in runners:
        H={r[3]:(r[5],r[4]) for r in rows if r[2]=='H' and r[0]==pid}
        hold=[]
        for a,b,_ in bases:
            for x,(ra,k) in H.items():
                if k!='body': continue
                c=chord(ra,H[a][0],H[b][0])
                if c is not None: hold.append((c,x,f'{a}–{b}'))
        per[name]=sorted(hold)
    # tightest per base
    best={}
    for name,h in per.items():
        for c,x,base in h:
            if base not in best or c<best[base][0]: best[base]=(c,name,x)
    for name,h in per.items():
        tops=[f'{x} on {base} {c*100:.3f}%'+(' [TIGHTEST]' if best[base][1]==name and best[base][2]==x else '') for c,x,base in h]
        print(f'  {name:22s} {len(h):2d} | '+'; '.join(tops[:8]))
