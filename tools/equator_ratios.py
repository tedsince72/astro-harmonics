# equator_ratios.py WORKBOOK: |Dec| of each body in sky, horse, jockey, with S/H, S/J, H/J nearest p/q (q<=9). (Newcastle AW 12 Nov read, 11 Oct 2026)
import sys,openpyxl
from fractions import Fraction
wb=openpyxl.load_workbook(sys.argv[1],read_only=True,data_only=True)
def load(t):
    P={}
    for r in wb[t].iter_rows(min_row=2,values_only=True):
        if isinstance(r[1],str) and r[4] is not None and not r[1].endswith('_B') and r[1] not in ('Moon','Ketu'):
            try: P[r[1]]=abs(float(r[8]))
            except: pass
    return P
S,H,J=load('TRANS'),load('P01'),load('P02')
def best(x):
    f=Fraction(x).limit_denominator(9); return f, abs(float(f)/x-1)*100
def lab(v):
    w=round(v); q=round(v*9)
    if abs(v-w)<=0.005 and w: return f"={w}"
    if abs(v-q/9)<=0.0005 and q%9: return f"={q}/9"
    return ""
print("body        sky Eq      horse Eq    jockey Eq   S/H            S/J            H/J")
for b in S:
    if b not in H or b not in J: continue
    s,h,j=S[b],H[b],J[b]
    cells=[]
    for a,c in ((s,h),(s,j),(h,j)):
        f,e=best(a/c); cells.append(f"{str(f):>6s} {e:5.3f}%"+('*' if e<=0.05 and f.numerator<=30 else ' '))
    print(f"{b:10s} {s:9.4f}{lab(s):6s}{h:9.4f}{lab(h):6s}{j:9.4f}{lab(j):6s} "+"  ".join(cells))
