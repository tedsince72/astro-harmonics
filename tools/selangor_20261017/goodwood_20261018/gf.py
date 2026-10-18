import sys; sys.path.insert(0,sys.argv[1]); import rc
rc.load_file('reference/classic/race_batch_20210827_goodwood_1853_jupiter_tables.xlsx')
d=rc.d;p=rc.pos;R=rc.RUN;WIN='P09'
def sc(v,pl,k='deg'):
    b=rc.fm.best(v,pl,k); return f"{b['target']} [{b['score']:.2f}]" if b else None
def mid(J,x,y,pl):
    a=d(J,x,pl); b=d(J,y,pl); clos=min(a,b)/max(a,b)*100
    if pl=='Dec': off=J[1]-(x[1]+y[1])/2; tol=0.15
    elif pl=='Equator': off=abs(J[1])-(abs(x[1])+abs(y[1]))/2; tol=0.15
    else:
        m1=((x[0]+y[0])/2)%360; m2=(m1+180)%360
        off=min([((J[0]-m+540)%360)-180 for m in (m1,m2)],key=abs); tol=0.5
    if clos<90 or abs(off)>=tol: return None
    return round((10*(10-(100-clos))/10)**2*0.5+(10*(tol-abs(off))/tol)**2*0.5,2)
def ratio(J,x,y,pl,tog=True):
    if pl=='Equator' and not rc.straddle(J,x,y): return None
    if tog and d(x,y,pl)<(1.5 if pl=='RA' else 0.3): return 'together'
    a=d(J,x,pl);b=d(J,y,pl);q=max(a,b)/min(a,b); s=sc(q,pl,'ratio'); m=mid(J,x,y,pl)
    o=[]
    if s: o.append(f"{q:.6f} {s}")
    if m: o.append(f"mid {m}")
    return '; '.join(o) or None
def show(lbl,f,chs):
    out=[]
    for r in R:
        for ch in chs:
            try: v=f(r,ch)
            except KeyError: v=None
            if v: out.append(f"{'*' if r==WIN else ''}{r}{ch} {v}")
    print(f"{lbl}: "+(' | '.join(out) or 'none'))
def dist(a,b,pl):
    def f(r,ch):
        A=p(r,*a(ch)) if callable(a) else p(r,*a); B=p(r,*b(ch)) if callable(b) else p(r,*b)
        v=d(A,B,pl); s=sc(v,pl); return f"{v:.6f} {s}" if s else None
    return f

H='H';J='J'
for ch,x,y,pl in [('H','Uranus','Juno','Dec'),('H','Ketu','Sedna','Dec'),('H','Venus','Sedna','Equator'),('H','Venus','Sedna','RA'),('H','Ceres','Quaoar','Dec'),('H','Pluto','Makemake','Equator'),
 ('H','Pluto','Antares','Dec'),('H','Mars','Neptune','Dec'),('H','Venus','Regulus','Equator'),('H','Mars','Makemake','Equator'),('H','Uranus','Neptune','Dec'),('H','Mercury','Regulus','Equator'),
 ('H','Sun','Mercury','Dec'),('H','Haumea','Fomalhaut','Dec'),
 ('J','Saturn','Aldebaran','Equator'),('J','Mars','Ceres','Dec'),('J','Mercury','Uranus','Dec'),('J','Saturn','Neptune','RA'),('J','Jupiter','Pallas','RA'),('J','Venus','Haumea','RA'),
 ('J','Rahu','Regulus','RA'),('J','Saturn','Sedna','Equator'),('J','Sun','Neptune','Dec'),('J','Jupiter','Uranus','Dec'),('J','Makemake','Transpluto','RA'),('J','Venus','Regulus','Dec')]:
    show(f"T19 {ch} {x}–{y} {pl}",lambda r,c,x=x,y=y,pl=pl: ratio(p(r,'S','Jupiter'),p(r,c,x),p(r,c,y),pl),'HJ')
for x,y,pl in [('Pleiades','Antares','RA'),('Pleiades','Regulus','RA'),('Regulus','Antares','RA'),('Regulus','Polaris','RA'),('Pleiades','Algorab','RA'),
  ('Capella','Fomalhaut','Dec'),('Pleiades','Betelgeuse','RA'),('Deneb Algedi','Polaris','Dec'),('Alphecca','Antares','Dec'),('Algorab','Castor','Dec'),('Algol','Sirius','RA')]:
    show(f"T21 {x}–{y} {pl}",lambda r,c,x=x,y=y,pl=pl: ratio(p(r,c,'Jupiter'),p(r,c,x),p(r,c,y),pl),'HJ')
def t12(ch,x,pl):
    def f(r,c):
        if c!=ch: return None
        a=d(p(r,'S','Jupiter'),p(r,'S',x),pl); b=d(p(r,c,'Jupiter'),p(r,c,x),pl); q=max(a,b)/min(a,b); s=sc(q,pl,'ratio'); return f"{q:.6f} {s}" if s else None
    return f
show("T12 J Juno RA",t12('J','Juno','RA'),'HJ'); show("T12 J Makemake Dec",t12('J','Makemake','Dec'),'HJ')
for lbl,a,b,pl in [('T1 natal Jup→Polaris RA',lambda c:(c,'Jupiter'),lambda c:(c,'Polaris'),'RA'),('T1 natal Jup→Deneb Algedi RA',lambda c:(c,'Jupiter'),lambda c:(c,'Deneb Algedi'),'RA'),
  ('T1 natal Jup→Aldebaran Dec',lambda c:(c,'Jupiter'),lambda c:(c,'Aldebaran'),'Dec'),('T1 natal Jup→Chiron RA',lambda c:(c,'Jupiter'),lambda c:(c,'Chiron'),'RA'),
  ('T2 natal Jup→Pallas RA',lambda c:(c,'Jupiter'),lambda c:(c,'Pallas'),'RA'),('T2 natal Jup→Mercury Dec',lambda c:(c,'Jupiter'),lambda c:(c,'Mercury'),'Dec'),
  ('T2 natal Jup→Eris Dec',lambda c:(c,'Jupiter'),lambda c:(c,'Eris'),'Dec'),('T2 natal Jup→Ketu RA',lambda c:(c,'Jupiter'),lambda c:(c,'Ketu'),'RA'),
  ('T5 SJup→natal Quaoar Dec',('S','Jupiter'),lambda c:(c,'Quaoar'),'Dec'),('T5 SJup→natal Eris Dec',('S','Jupiter'),lambda c:(c,'Eris'),'Dec'),
  ('T7 S Uranus→natal Jup RA',('S','Uranus'),lambda c:(c,'Jupiter'),'RA'),('T8 S Makemake→natal Jup RA',('S','Makemake'),lambda c:(c,'Jupiter'),'RA'),
  ('T8 S Chiron→natal Jup Dec',('S','Chiron'),lambda c:(c,'Jupiter'),'Dec'),('T8 S Transpluto→natal Jup RA',('S','Transpluto'),lambda c:(c,'Jupiter'),'RA'),
  ('T8 S Neptune→natal Jup RA',('S','Neptune'),lambda c:(c,'Jupiter'),'RA')]:
    show(lbl,dist(a,b,pl),'HJ')
for lbl,a,b,pl in [('T3 H Jup→J Pluto RA',('H','Jupiter'),('J','Pluto'),'RA'),('T3 H Jup→J Orcus RA',('H','Jupiter'),('J','Orcus'),'RA'),('T4 J Jup→H Orcus Dec',('J','Jupiter'),('H','Orcus'),'Dec'),
  ('T4 J Jup→H Rahu RA',('J','Jupiter'),('H','Rahu'),'RA'),('T3 H Jup→J Uranus RA',('H','Jupiter'),('J','Uranus'),'RA')]:
    show(lbl,dist(a,b,pl),'H')
def m10(r,c):
    if c!='H': return None
    return mid(p(r,'J','Juno'),p(r,'S','Jupiter'),p(r,'H','Juno'),'Dec')
show("T10 J Juno midpoint of S Jupiter and H Juno, Dec",m10,'H')
def m10b(r,c):
    if c!='H': return None
    return mid(p(r,'H','Mercury'),p(r,'S','Jupiter'),p(r,'J','Mercury'),'Dec')
show("T10 H Mercury midpoint of S Jupiter and J Mercury, Dec",m10b,'H')
for ch,x,y in [('H','Mercury','Eris'),('J','Venus','Rahu'),('J','Ketu','Sedna'),('H','Mercury','Vesta'),('H','Pluto','Sedna')]:
    def f(r,c,x=x,y=y,ch=ch):
        if c!=ch: return None
        J=p(r,c,'Jupiter');res=[]
        for pl in ('RA','Dec','Equator'):
            if pl=='Equator' and not rc.straddle(J,p(r,c,x),p(r,c,y)): continue
            if d(p(r,c,x),p(r,c,y),pl)<(1.5 if pl=='RA' else 0.3): continue
            m=mid(J,p(r,c,x),p(r,c,y),pl)
            if m: res.append(f"{pl} {m}")
        return ', '.join(res) or None
    show(f"T17 {ch} Jupiter: {x} = {y}",f,'HJ')
def hj(r,c):
    if c!='H': return None
    return ratio(p(r,'S','Jupiter'),p(r,'H','Juno'),p(r,'J','Juno'),'Dec')
show("T19 H Juno – J Juno Dec",hj,'H')
