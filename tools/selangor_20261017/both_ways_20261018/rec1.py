import sys; sys.path.insert(0,sys.argv[1]); import rc
exec(open(sys.argv[1]+'/nep1.py').read().split('d=rc.d')[0].split('import rc')[1])
d=rc.d;p=rc.pos
ROY=['Aldebaran','Regulus','Antares','Fomalhaut']
def sc(v,pl):
    b=rc.fm.best(v,pl,'deg'); return (round(b['score'],2),str(b['target'])) if b else (0,None)
TH=float(sys.argv[2])
for kind,key,win in RACES:
    rc.load(key) if kind=='sel' else rc.load_file(key)
    chs='HJ' if kind=='f' else 'H'
    bodies=sorted({k[2] for k in rc.P if k[0]=='SKY' and k[1]=='S'} - {'Jupiter','Moon'})
    holders={}
    for r in rc.RUN:
        for ch in chs:
            for X in bodies:
                if (r,ch,X) not in rc.P: continue
                for pl in ('RA','Dec'):
                    a=d(p(r,'S','Jupiter'),p(r,ch,X),pl); b=d(p(r,'S',X),p(r,ch,'Jupiter'),pl)
                    sa=sc(a,pl); sb=sc(b,pl)
                    if sa[0]>=TH and sb[0]>=TH:
                        holders.setdefault(r,[]).append(f"{ch} {X} {pl}: SJ→{X} {a:.6f} {sa[1]} [{sa[0]}] | S{X}→Jup {b:.6f} {sb[1]} [{sb[0]}]")
    name=key.split('/')[-1][:40]
    print(f"\n=== {name} winner {win}; runners with a reciprocal >= {TH}: {len(holders)}/{len(rc.RUN)}")
    for r in rc.RUN:
        if r in holders: print(f"  {'WIN' if r==win else '   '} {r} " + ' ; '.join(holders[r]))
