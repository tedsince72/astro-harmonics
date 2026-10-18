import sys,io,contextlib; sys.path.insert(0,sys.argv[1]); import rc
exec(open(sys.argv[1]+'/nep1.py').read().split('d=rc.d')[0].split('import rc')[1])
sys.argv=[sys.argv[0],sys.argv[1],sys.argv[1]]
with contextlib.redirect_stdout(io.StringIO()): from pr3 import mid
d=rc.d;p=rc.pos
def r3(J,x,y,pl):
    if pl=='Equator' and not rc.straddle(J,x,y): return None
    a=d(J,x,pl);b=d(J,y,pl); q=max(a,b)/min(a,b); bb=rc.fm.best(q,pl,'ratio')
    return (q, (bb['target'],round(bb['score'],2)) if bb else None)
for kind,key,win in RACES:
    rc.load(key) if kind=='sel' else rc.load_file(key)
    k=key if kind=='sel' else key.split('_')[3]
    out=[]
    for R in ('Antares','Fomalhaut','Aldebaran','Regulus'):
        for pl in ('RA','Dec','Equator'):
            hs=[]
            for r in rc.RUN:
                for ch in ('HJ' if kind=='f' else 'H'):
                    x=r3(p(r,'S','Jupiter'),p(r,ch,'Neptune'),p(r,ch,R),pl)
                    if x and x[1] and x[1][1]>=50: hs.append(f"{'*' if r==win else ''}{r}{ch} {x[1][0]} {x[1][1]}")
            if hs: out.append(f"  Neptune–{R} {pl}: "+', '.join(hs))
    print(f"== {k} (winner {win}, n={len(rc.RUN)})"); print('\n'.join(out) if out else '  none')
