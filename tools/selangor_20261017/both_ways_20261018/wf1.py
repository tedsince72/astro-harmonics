import sys; sys.path.insert(0,sys.argv[1]); import rc
rc.load_file('reference/classic/race_batch_20210822_worcester_1300_jupiter_tables.xlsx')
R=rc.RUN; d=rc.d; p=rc.pos; fam=rc.fam
print({r:rc.N[r] for r in R})
def dist(lbl,a,b,pl):
    print(f"\n## {lbl} {pl}")
    for r in R:
        try: A=p(*a(r)) if callable(a) else p(r,*a); B=p(*b(r)) if callable(b) else p(r,*b)
        except KeyError as e: print(r,'missing',e); continue
        v=d(A,B,pl); print(f"  {r} {v:.6f} {fam(v,pl)}")
def t19(lbl,ch,x,y,pl):
    print(f"\n## T19 S Jup: {ch} {x} – {ch} {y} {pl}")
    for r in R:
        print(f"  {r} "+rc.ratio3(p(r,'S','Jupiter'),p(r,ch,x),p(r,ch,y),pl))
def t12(ch,x,pl,kind='T12'):
    print(f"\n## {kind} {ch} {x} {pl}")
    for r in R:
        sj=p(r,'S','Jupiter'); nj=p(r,ch,'Jupiter'); nx=p(r,ch,x)
        a=d(sj,p(r,'S',x),pl) if kind=='T12' else d(sj,nx,pl); b=d(nj,nx,pl)
        q=max(a,b)/min(a,b); print(f"  {r} {a:.6f}/{b:.6f} = {q:.6f} {fam(q,pl,'ratio')}")
def t21(ch,x,y,pl):
    print(f"\n## T21 {ch} Jup: {x} – {y} {pl}")
    for r in R: print(f"  {r} "+rc.ratio3(p(r,ch,'Jupiter'),p(r,ch,x),p(r,ch,y),pl))
def t22(st,pl):
    print(f"\n## T22 {st} {pl}")
    for r in R:
        s=p(r,'S',st)
        for ch in 'HJ':
            a=d(s,p(r,'S','Jupiter'),pl); b=d(s,p(r,ch,'Jupiter'),pl); q=max(a,b)/min(a,b)
            print(f"  {r}{ch} leg {b:.6f} {fam(b,pl)} | ratio {q:.6f} {fam(q,pl,'ratio')}")
H=[('H','Venus','Juno','RA'),('H','Rahu','Eris','RA'),('H','Sun','Eris','RA'),('H','Quaoar','Regulus','Equator'),('H','Mars','Ketu','RA'),
   ('H','Venus','Neptune','Equator'),('H','Jupiter','Haumea','Equator'),('H','Sun','Neptune','Equator'),('H','Mars','Aldebaran','Dec'),
   ('H','Ceres','Vesta','RA'),('H','Jupiter','Ketu','Dec'),('H','Rahu','Transpluto','Equator'),('H','Juno','Haumea','Equator'),
   ('H','Pallas','Makemake','RA'),('H','Mercury','Antares','Dec'),('H','Mercury','Vesta','Equator'),
   ('J','Venus','Quaoar','Dec'),('J','Sun','Ceres','Equator'),('J','Sun','Transpluto','Equator'),('J','Chiron','Quaoar','RA'),
   ('J','Rahu','Transpluto','RA'),('J','Vesta','Eris','Equator'),('J','Uranus','Aldebaran','Equator'),('J','Rahu','Transpluto','Equator'),('H','Rahu','Transpluto','RA')]
for c in H: t19('',*c)
t12('H','Ketu','Dec'); t12('J','Ceres','Dec'); t12('J','Pluto','RA','T13'); t12('H','Ketu','Dec','T13')
for nm,a,b,pl in [('T5 S Jup→H Transpluto',('S','Jupiter'),lambda r:(r,'H','Transpluto'),'RA'),('T5 S Jup→H Uranus',('S','Jupiter'),lambda r:(r,'H','Uranus'),'Dec'),
  ('T6 S Jup→J Haumea',('S','Jupiter'),lambda r:(r,'J','Haumea'),'RA'),('T6 S Jup→J Ketu',('S','Jupiter'),lambda r:(r,'J','Ketu'),'RA'),
  ('T7 S Neptune→H Jup',('S','Neptune'),lambda r:(r,'H','Jupiter'),'Dec'),('T7 S Sedna→H Jup',('S','Sedna'),lambda r:(r,'H','Jupiter'),'RA'),('T7 S Juno→H Jup',('S','Juno'),lambda r:(r,'H','Jupiter'),'RA'),
  ('T8 S Vesta→J Jup',('S','Vesta'),lambda r:(r,'J','Jupiter'),'Dec'),('T8 S Chiron→J Jup',('S','Chiron'),lambda r:(r,'J','Jupiter'),'Dec'),('T8 S Mercury→J Jup',('S','Mercury'),lambda r:(r,'J','Jupiter'),'RA'),
  ('T8 S Moon→J Jup',('S','Moon'),lambda r:(r,'J','Jupiter'),'RA'),('T22 leg S Regulus→J Jup',('S','Regulus'),lambda r:(r,'J','Jupiter'),'Dec'),
  ('T2 J Jup→J Regulus',lambda r:(r,'J','Jupiter'),lambda r:(r,'J','Regulus'),'Dec'),('T1 H Jup→H Quaoar',lambda r:(r,'H','Jupiter'),lambda r:(r,'H','Quaoar'),'RA'),
  ('T1 H Jup→H Rigel',lambda r:(r,'H','Jupiter'),lambda r:(r,'H','Rigel'),'RA'),('T1 H Jup→H Polaris',lambda r:(r,'H','Jupiter'),lambda r:(r,'H','Polaris'),'RA'),
  ('T3 H Jup→J Pallas',lambda r:(r,'H','Jupiter'),lambda r:(r,'J','Pallas'),'RA'),('T4 J Jup→H Gonggong',lambda r:(r,'J','Jupiter'),lambda r:(r,'H','Gonggong'),'RA'),
  ('T4 J Jup→H Juno',lambda r:(r,'J','Jupiter'),lambda r:(r,'H','Juno'),'RA'),('T4 J Jup→H Uranus',lambda r:(r,'J','Jupiter'),lambda r:(r,'H','Uranus'),'Dec')]:
    dist(nm,a,b,pl)
for ch,x,y,pl in [('H','Regulus','Algorab','Equator'),('J','Regulus','Algorab','RA'),('H','Regulus','Algorab','RA'),('J','Regulus','Algorab','Equator'),('H','Sirius','Fomalhaut','Dec'),('H','Regulus','Antares','Equator'),
  ('H','Procyon','Spica','RA'),('J','Spica','Alphecca','Equator'),('J','Aldebaran','Polaris','Dec'),('J','Spica','Castor','Equator')]: t21(ch,x,y,pl)
t22('Regulus','RA'); t22('Regulus','Dec')
