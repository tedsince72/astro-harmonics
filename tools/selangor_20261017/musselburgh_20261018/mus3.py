import sys; sys.path.insert(0,sys.argv[1]); import rc
rc.load_file('reference/classic/race_batch_20210825_musselburgh_1345_jupiter_tables.xlsx')
d=rc.d;p=rc.pos;R=rc.RUN;fam=rc.fam
ROY=['Aldebaran','Regulus','Antares','Fomalhaut']
for X in ('Chiron','Quaoar','Makemake','Neptune'):
    print(f"\n== {X}: S Jup→natal {X} | S {X}→natal Jup, every runner, RA / Dec")
    for r in R:
        for ch in 'HJ':
            s=[]
            for pl in ('RA','Dec'):
                a=d(p(r,'S','Jupiter'),p(r,ch,X),pl); b=d(p(r,'S',X),p(r,ch,'Jupiter'),pl)
                s.append(f"{pl}: {a:.6f} {fam(a,pl)} | {b:.6f} {fam(b,pl)}")
            print(f"  {r}{ch} "+' ;; '.join(s))
print("\n== royal between S Chiron and H Jupiter RA (P07)")
A=p('P07','S','Chiron');B=p('P07','H','Jupiter')
for pl in ('RA','Dec'):
    tot=d(A,B,pl)
    for Rr in ROY:
        s=p('P07','S',Rr); a=d(A,s,pl); c=d(s,B,pl)
        print(f"  {pl} {Rr}: {a:.6f} {fam(a,pl)} + {c:.6f} {fam(c,pl)} = {a+c:.6f} vs {tot:.6f} {'BETWEEN' if abs(a+c-tot)<0.01*tot else ''}")
print("\n== Chiron with royal stars: sky, P07 H, P07 J (distances)")
for Rr in ROY:
    for pl in ('RA','Dec','Equator'):
        vs=[d(p('P07',c,'Chiron'),p('P07',c,Rr),pl) for c in 'SHJ']
        print(f"  {Rr} {pl}: S {vs[0]:.6f} {fam(vs[0],pl)} | H {vs[1]:.6f} {fam(vs[1],pl)} | J {vs[2]:.6f} {fam(vs[2],pl)}")
print("\n== positions")
for c,b in [('S','Jupiter'),('S','Chiron'),('H','Jupiter'),('H','Chiron'),('J','Jupiter'),('J','Chiron'),('S','Algorab'),('S','Quaoar'),('H','Quaoar'),('S','Regulus'),('S','Fomalhaut')]:
    print(f"  {c} {b}: RA {p('P07',c,b)[0]:.6f} Dec {p('P07',c,b)[1]:+.6f}")
