import sys; sys.path.insert(0,sys.argv[1]); import rc
exec(open(sys.argv[1]+'/nep1.py').read().split('d=rc.d')[0].split('import rc')[1])
d=rc.d;p=rc.pos
def sc(v,pl,k='deg'):
    b=rc.fm.best(v,pl,k); return (round(b['score'],2),str(b['target'])) if b else (None,None)
print("PART 1: Makemake / Chiron / Neptune both ways (T5-type S Jup→natal X and T7-type S X→natal Jupiter, same plane RA or Dec, both inside a family)")
for kind,key,win in RACES:
    rc.load(key) if kind=='sel' else rc.load_file(key)
    k=key if kind=='sel' else key.split('_')[3]
    out=[]
    for r in rc.RUN:
        for ch in ('HJ' if kind=='f' else 'H'):
            for X in ('Makemake','Chiron','Neptune'):
                for pl in ('RA','Dec'):
                    a=d(p(r,'S','Jupiter'),p(r,ch,X),pl); b=d(p(r,'S',X),p(r,ch,'Jupiter'),pl)
                    sa=sc(a,pl); sb=sc(b,pl)
                    if sa[0] is not None and sb[0] is not None:
                        out.append(f"   {'WIN ' if r==win else '    '}{r} {rc.N[r][:30]:30s} {ch} {X:8s} {pl:3s}: S Jup→{ch} {X} {a:.6f} → {sa[1]} [{sa[0]}] | S {X}→{ch} Jup {b:.6f} → {sb[1]} [{sb[0]}]")
    print(f"== {k} (n={len(rc.RUN)})"); print('\n'.join(out) if out else '   none')
