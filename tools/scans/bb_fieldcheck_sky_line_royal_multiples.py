import sys,re; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
exec(open('tools/scans/bb_fieldcheck_sky_line_royal_ends.py').read().split("def test(")[0])   # races, data, royal, skylines, helpers
A=[1.5,2,3,4,5,6,7,8,9]
def on(a,b,targets):
    if not a or not b: return None
    r=max(a,b)/min(a,b)
    for t in targets:
        if abs(r-t)<0.02: return t
    return None
def ends(b,D):
    for s,Y in skylines(b):
        if Y in D: yield s,Y,royal(b),royal(E.Body(Y,D[Y]))
def M1(b,D,uni=False):
    T=([1] if uni else [])+A
    return any(on(r1['v'],r2['v'],T) for s,Y,RX,RY in ends(b,D) for r1 in RX for r2 in RY)
def M2(b,D):   # both royal lines a multiple (incl. 1) of the sky line
    T=[1]+A
    return any(any(on(r1['v'],s['v'],T) for r1 in RX) and any(on(r2['v'],s['v'],T) for r2 in RY) for s,Y,RX,RY in ends(b,D))
def M2b(b,D):  # M2 with at least one a true multiple (not 1)
    T=[1]+A
    for s,Y,RX,RY in ends(b,D):
        x=[on(r['v'],s['v'],T) for r in RX]; y=[on(r['v'],s['v'],T) for r in RY]
        x=[t for t in x if t]; y=[t for t in y if t]
        if x and y and (any(t!=1 for t in x) or any(t!=1 for t in y)): return True
    return False
def M3(b,D):   # M1 (royal lines a multiple, not 1) and the sky line in the family of one of them
    for s,Y,RX,RY in ends(b,D):
        for r1 in RX:
            for r2 in RY:
                if on(r1['v'],r2['v'],A) and s['fam'] in (r1['fam'],r2['fam']): return True
    return False
V={'M1 royal->X / royal->Y on 3/2, 2 ... 9':M1,'M1u M1 incl. unison 1':lambda b,D:M1(b,D,True),
'M2 royal->X and royal->Y each a multiple (1, 3/2, 2 ... 9) of the sky X–Y line':M2,'M2b M2, at least one not 1':M2b,
'M3 M1 and the sky line in the family of one royal line':M3}
for v,f in V.items():
    print('==',v)
    for n,_ in races:
        h=[(run,X) for run,D in data[n].items() for X,d in D.items() if f(E.Body(X,d),D)]
        rn=sorted({run for run,_ in h}); w=W.get(n)
        print(f'  {n}: {len(h)} bodies, {len(rn)}/{len(data[n])} runners' + (f"; winner {'YES' if any(w in r for r in rn) else 'no'}" if w else ''))
