import sys; sys.path.insert(0,sys.argv[1]); import rc
exec(open(sys.argv[1]+'/nep1.py').read().split('d=rc.d')[0].split('import rc')[1])
d=rc.d;p=rc.pos
ROY=['Aldebaran','Regulus','Antares','Fomalhaut']
def b(v,pl,k='deg'):
    x=rc.fm.best(v,pl,k); return (x['target'],round(x['score'],2)) if x else None
TH=float(sys.argv[2]); ONLYWIN=sys.argv[3]=='win'
for kind,key,win in RACES:
    rc.load(key) if kind=='sel' else rc.load_file(key)
    k=key if kind=='sel' else key.split('_')[3]
    bodies=sorted({q[2] for q in rc.P if q[0]=='SKY' and q[1]=='S'} - {'Jupiter','Moon'}-set(ROY))
    bodies=[x for x in bodies if (win,'H',x) in rc.P]
    print(f"== {k} winner {win}")
    for r in ([win] if ONLYWIN else rc.RUN):
      for ch in ('HJ' if kind=='f' else 'H'):
        for X in bodies:
            for pl in ('RA','Dec'):
                for lab,A,B in (('T7 S%s→%sJup'%(X,ch),p(r,'S',X),p(r,ch,'Jupiter')),('T5 SJup→%s%s'%(ch,X),p(r,'S','Jupiter'),p(r,ch,X))):
                    tot=d(A,B,pl); bt=b(tot,pl)
                    if not bt or bt[1]<TH: continue
                    for R in ROY:
                        sr=p(r,'S',R); a=d(A,sr,pl); c=d(sr,B,pl)
                        if abs(a+c-tot)>0.01*tot: continue
                        ba,bc=b(a,pl),b(c,pl)
                        q=max(a,c)/min(a,c); bq=b(q,pl,'ratio'); bq2=b(tot/max(a,c),pl,'ratio')
                        if (ba and ba[1]>=50) or (bc and bc[1]>=50) or (bq and bq[1]>=50):
                            print(f"  {r}{' WIN' if r==win else ''} {lab} {pl} {tot:.6f} {bt} | S {R} between: {a:.6f} {ba} + {c:.6f} {bc} | parts ratio {q:.6f} {bq} | whole/larger {tot/max(a,c):.6f} {bq2}")
