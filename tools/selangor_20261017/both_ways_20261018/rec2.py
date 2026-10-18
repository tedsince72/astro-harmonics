import sys; sys.path.insert(0,sys.argv[1]); import rc
exec(open(sys.argv[1]+'/nep1.py').read().split('d=rc.d')[0].split('import rc')[1])
d=rc.d;p=rc.pos;fam=rc.fam
ROY=['Aldebaran','Regulus','Antares','Fomalhaut']
REC={'1345':['Makemake'],'1515':['Chiron'],'newcastle':['Chiron'],'worcester':['Neptune']}
for kind,key,win in RACES:
    rc.load(key) if kind=='sel' else rc.load_file(key)
    k=key if kind=='sel' else ('newcastle' if 'newcastle' in key else 'worcester')
    Xs=['Neptune']+[x for x in REC.get(k,[]) if x!='Neptune']
    chs='HJ' if kind=='f' else 'H'
    print(f"\n===== {k} winner {win} {rc.N[win]}")
    SJ=p(win,'S','Jupiter')
    for X in Xs:
        print(f" -- {X}")
        for pl in ('RA','Dec','Equator'):
            v=d(SJ,p(win,'S',X),pl)
            if pl=='Equator' and not rc.straddle(SJ,p(win,'S',X)): pass
            print(f"   sky S Jup–S {X} {pl} {v:.6f} {fam(v,pl)}")
        for R in ROY:
            for pl in ('RA','Dec','Equator'):
                v=d(p(win,'S',X),p(win,'S',R),pl)
                line=f"   sky S {X}–S {R} {pl} {v:.6f} {fam(v,pl)} || S Jup on S {X}–S {R}: "+rc.ratio3(SJ,p(win,'S',X),p(win,'S',R),pl)
                print(line)
                for ch in chs:
                    print(f"      natal T19 S Jup on {ch} {X}–{ch} {R} {pl}: "+rc.ratio3(SJ,p(win,ch,X),p(win,ch,R),pl))
