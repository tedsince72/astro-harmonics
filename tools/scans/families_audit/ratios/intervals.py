import math
phi=(1+5**0.5)/2; r2=2**0.5
LIST={'1':1,'2':2,'3/2':1.5,'4/3':4/3,'3':3,'4':4,
'5/4':1.25,'6/5':1.2,'5/3':5/3,'8/5':1.6,'5/2':2.5,'8/3':8/3,'9/4':2.25,
'sqrt2':r2,'1+1/sqrt2':1+1/r2,'9/8':9/8,'16/9':16/9,'9/5':1.8,'15/8':15/8,'16/15':16/15,
'7/4':1.75,'7/3':7/3,'7/2':3.5,'7/5':1.4,'7/6':7/6,'8/7':8/7,
'5':5,'6':6,'7':7,'8':8,'9':9,
'11/5':2.2,'11/6':11/6,'11/3':11/3,'11/8':11/8,'11/4':2.75,'13/5':2.6,'13/8':13/8,'13/4':3.25,
'phi':phi,'phi^2':phi**2,'phi^3':phi**3,'1+sqrt2':1+r2,'phi*sqrt5':phi*5**0.5,'2-1/phi':2-1/phi,'phi^3+1':phi**3+1,'2/phi':2/phi}
def norm(v):
    v=abs(v)
    return 1/v if 0<v<1 else v
def on_list(v,rel=1e-7):
    v=norm(v)
    for k,x in LIST.items():
        if abs(v/x-1)<rel: return k
    return None
def nearest(v):
    v=norm(v); k=min(LIST,key=lambda k:abs(v/LIST[k]-1)); return k,100*(v/LIST[k]-1)
def frac(s):
    s=s.strip()
    if ':' in s: a,b=s.split(':'); return float(a)/float(b)
    if '/' in s: a,b=s.split('/'); return float(a)/float(b)
    return float(s)
