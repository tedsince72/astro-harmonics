import sys; sys.path.insert(0,sys.argv[1]); import rc
rc.load_file('reference/classic/race_batch_20210825_musselburgh_1345_jupiter_tables.xlsx')
d=rc.d;p=rc.pos;R=rc.RUN;WIN='P07'
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
# T19 natal pairs (S Jupiter)
for ch,x,y,pl in [('H','Venus','Mars','Dec'),('H','Jupiter','Aldebaran','RA'),('H','Chiron','Antares','Equator'),('H','Vesta','Fomalhaut','Dec'),('H','Sedna','Antares','Dec'),
 ('H','Juno','Fomalhaut','RA'),('H','Transpluto','Aldebaran','RA'),('H','Mars','Chiron','RA'),('H','Jupiter','Pluto','Dec'),('H','Chiron','Orcus','Equator'),('H','Uranus','Haumea','Equator'),
 ('H','Sedna','Haumea','Dec'),('H','Haumea','Antares','Dec'),
 ('J','Uranus','Fomalhaut','Dec'),('J','Neptune','Antares','Dec'),('J','Orcus','Aldebaran','Equator'),('J','Saturn','Makemake','RA'),('J','Mercury','Sedna','Equator'),('J','Sun','Mars','RA'),
 ('J','Mercury','Orcus','Equator'),('J','Mars','Quaoar','RA'),('J','Venus','Haumea','Equator'),('J','Eris','Aldebaran','Equator'),('J','Jupiter','Chiron','RA')]:
    show(f"T19 {ch} {x}–{y} {pl}",lambda r,c,x=x,y=y,pl=pl: ratio(p(r,'S','Jupiter'),p(r,c,x),p(r,c,y),pl),'HJ')
# T21 natal Jupiter on star pairs
for x,y,pl in [('Aldebaran','Betelgeuse','Dec'),('Antares','Rigel','RA'),('Deneb Algedi','Bellatrix','RA'),('Regulus','Arcturus','Dec'),('Capella','Procyon','Equator'),
  ('Procyon','Polaris','RA'),('Algorab','Spica','RA'),('Algol','Bellatrix','Dec'),('Algol','Castor','Dec')]:
    show(f"T21 {x}–{y} {pl}",lambda r,c,x=x,y=y,pl=pl: ratio(p(r,c,'Jupiter'),p(r,c,x),p(r,c,y),pl),'HJ')
# T12/T13
for ch,x,pl,k in [('H','Pluto','Dec','T13'),('H','Mars','Dec','T13'),('J','Chiron','RA','T13'),('J','Mars','RA','T13'),('J','Sedna','Dec','T13')]:
    def f(r,c,x=x,pl=pl):
        if c!=ch: return None
        a=d(p(r,'S','Jupiter'),p(r,c,x),pl); b=d(p(r,c,'Jupiter'),p(r,c,x),pl); q=max(a,b)/min(a,b); s=sc(q,pl,'ratio'); return f"{q:.6f} {s}" if s else None
    show(f"{k} {ch} {x} {pl}",f,'HJ')
# T14 Jupiter |Dec|
for a,b in [('S','J'),('H','J'),('S','H')]:
    def f(r,c,a=a,b=b):
        if c!='H': return None
        A=abs(p(r,a,'Jupiter')[1]);B=abs(p(r,b,'Jupiter')[1]); q=max(A,B)/min(A,B); s=sc(q,'Equator','ratio'); return f"{q:.6f} {s}" if s else None
    show(f"T14 |Dec| {a}/{b} Jupiter",f,'H')
# distances
for lbl,a,b,pl,chs in [('T7 S Chiron→natal Jup',('S','Chiron'),lambda c:(c,'Jupiter'),'RA','HJ'),('T7 S Moon→natal Jup',('S','Moon'),lambda c:(c,'Jupiter'),'RA','HJ'),
  ('T1/2 natal Jup→Vesta',lambda c:(c,'Jupiter'),lambda c:(c,'Vesta'),'Dec','HJ'),('T1/2 natal Jup→Ketu',lambda c:(c,'Jupiter'),lambda c:(c,'Ketu'),'Dec','HJ'),
  ('T1/2 natal Jup→Mars',lambda c:(c,'Jupiter'),lambda c:(c,'Mars'),'RA','HJ'),('T1/2 natal Jup→Betelgeuse',lambda c:(c,'Jupiter'),lambda c:(c,'Betelgeuse'),'Dec','HJ'),
  ('T1/2 natal Jup→Rigel RA',lambda c:(c,'Jupiter'),lambda c:(c,'Rigel'),'RA','HJ'),('T1/2 natal Jup→Eris RA',lambda c:(c,'Jupiter'),lambda c:(c,'Eris'),'RA','HJ'),
  ('T1/2 natal Jup→Sirius RA',lambda c:(c,'Jupiter'),lambda c:(c,'Sirius'),'RA','HJ'),('T1/2 natal Jup→Capella RA',lambda c:(c,'Jupiter'),lambda c:(c,'Capella'),'RA','HJ'),
  ('T1/2 natal Jup→Saturn RA',lambda c:(c,'Jupiter'),lambda c:(c,'Saturn'),'RA','HJ'),
  ('T8 S Pluto→natal Jup RA',('S','Pluto'),lambda c:(c,'Jupiter'),'RA','HJ'),('T8 S Gonggong→natal Jup Dec',('S','Gonggong'),lambda c:(c,'Jupiter'),'Dec','HJ'),
  ('T22 leg S Aldebaran→natal Jup Dec',('S','Aldebaran'),lambda c:(c,'Jupiter'),'Dec','HJ')]:
    show(lbl,dist(a,b,pl),chs)
# cross
for lbl,a,b,pl in [('T3 H Jup→J Transpluto RA',('H','Jupiter'),('J','Transpluto'),'RA'),('T4 J Jup→H Saturn Dec',('J','Jupiter'),('H','Saturn'),'Dec'),
 ('T4 J Jup→H Haumea Dec',('J','Jupiter'),('H','Haumea'),'Dec'),('T4 J Jup→H Vesta RA',('J','Jupiter'),('H','Vesta'),'RA'),('T3 H Jup→J Chiron Dec',('H','Jupiter'),('J','Chiron'),'Dec'),
 ('T4 J Jup→H Pallas RA',('J','Jupiter'),('H','Pallas'),'RA'),('H Jup–J Jup RA',('H','Jupiter'),('J','Jupiter'),'RA'),('H Jup–J Jup Dec',('H','Jupiter'),('J','Jupiter'),'Dec')]:
    show(lbl,dist(a,b,pl),'H')
# T10/T11 midpoints
def m10(r,c):
    if c!='H': return None
    return mid(p(r,'H','Orcus'),p(r,'S','Jupiter'),p(r,'J','Orcus'),'Equator') if rc.straddle(p(r,'H','Orcus'),p(r,'S','Jupiter'),p(r,'J','Orcus')) else None
show("T10 S Jupiter / J Orcus | H Orcus Equator",m10,'H')
def m11(r,c):
    if c!='J': return None
    X=p(r,'J','Vesta');A=p(r,'S','Jupiter');B=p(r,'J','Jupiter')
    return mid(X,A,B,'Equator') if rc.straddle(X,A,B) else None
show("T11 S Jupiter / J Jupiter | J Vesta Equator",m11,'J')
def m17(r,c):
    if c!='H': return None
    J=p(r,'S','Jupiter');x=p(r,'H','Jupiter');y=p(r,'H','Transpluto')
    return mid(J,x,y,'Equator') if rc.straddle(J,x,y) else None
show("T17 S Jupiter: H Jupiter = H Transpluto Equator",m17,'H')
def vv(r,c):
    if c!='H': return None
    return ratio(p(r,'S','Jupiter'),p(r,'H','Vesta'),p(r,'J','Vesta'),'RA')
show("T19 H Vesta – J Vesta RA",vv,'H')
