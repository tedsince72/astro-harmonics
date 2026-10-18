import sys; sys.path.insert(0,sys.argv[1]); import rc
rc.load_file('reference/classic/race_batch_20210827_goodwood_1853_jupiter_tables.xlsx')
d=rc.d;p=rc.pos;R=rc.RUN
def sc(v,pl,k='deg'):
    b=rc.fm.best(v,pl,k); return (round(b['score'],2),str(b['target'])) if b else None
def mid(J,x,y,pl):
    a=d(J,x,pl); b=d(J,y,pl); clos=min(a,b)/max(a,b)*100
    if pl=='Dec': off=J[1]-(x[1]+y[1])/2; tol=0.15
    elif pl=='Equator': off=abs(J[1])-(abs(x[1])+abs(y[1]))/2; tol=0.15
    else:
        m1=((x[0]+y[0])/2)%360; m2=(m1+180)%360
        off=min([((J[0]-m+540)%360)-180 for m in (m1,m2)],key=abs); tol=0.5
    if clos<90 or abs(off)>=tol: return None
    return round((10*(10-(100-clos))/10)**2*0.5+(10*(tol-abs(off))/tol)**2*0.5,2)
def t19(J,x,y,pl):
    if pl=='Equator' and not rc.straddle(J,x,y): return 'n/a'
    if d(x,y,pl)<(1.5 if pl=='RA' else 0.3): return 'together'
    a=d(J,x,pl);b=d(J,y,pl);q=max(a,b)/min(a,b); s=sc(q,pl,'ratio'); m=mid(J,x,y,pl)
    o=[]
    if s: o.append(f"{s[1]} [{s[0]}] ({q:.6f})")
    if m: o.append(f"mid {m}")
    return '; '.join(o)
PAIRS=[('Sun','Chiron','Dec'),('Mars','Pallas','Equator'),('Mars','Juno','Equator'),('Uranus','Regulus','Equator'),('Mercury','Ketu','RA'),('Ceres','Ketu','Dec'),
 ('Mercury','Transpluto','RA'),('Venus','Pluto','Dec'),('Orcus','Aldebaran','Equator'),('Venus','Rahu','Dec'),('Saturn','Chiron','Equator'),('Venus','Sedna','RA'),
 ('Saturn','Aldebaran','Equator'),('Pluto','Pallas','RA'),('Uranus','Neptune','RA'),('Ceres','Transpluto','Equator'),('Uranus','Antares','Equator'),('Makemake','Antares','RA'),
 ('Chiron','Makemake','Dec'),('Mercury','Mars','Equator'),('Ceres','Antares','RA'),('Uranus','Chiron','RA'),('Chiron','Fomalhaut','Equator'),('Mercury','Pallas','Equator'),
 ('Sun','Rahu','Equator'),('Mercury','Juno','Dec')]
print("== Same pair, natal (S Jupiter on natal X–Y, same plane)")
for x,y,pl in PAIRS:
    out=[]
    for r in R:
        for ch in 'HJ':
            try: v=t19(p(r,'S','Jupiter'),p(r,ch,x),p(r,ch,y),pl)
            except KeyError: v='(no natal %s)'%x; 
            if v and v!='n/a': out.append(f"{r}{ch} {v}")
    print(f" {x}–{y} {pl}: "+(' | '.join(out) or 'none'))
print("\n== Sky X → natal Jupiter (T7/T8) and S Jupiter → natal X (T5/T6), hits >= 70, bodies + royal stars")
bodies=sorted({k[2] for k in rc.P if k[0]=='SKY' and k[1]=='S'}-{'Jupiter'})
for r in R:
    for ch in 'HJ':
        a=[];b=[];both=[]
        for X in bodies:
            for pl in ('RA','Dec'):
                v=d(p(r,'S',X),p(r,ch,'Jupiter'),pl); s=sc(v,pl)
                if s and s[0]>=70: a.append(f"S {X}→{ch}Jup {pl} {v:.6f} {s[1]} [{s[0]}]")
                if (r,ch,X) in rc.P and X!='Moon':
                    w=d(p(r,'S','Jupiter'),p(r,ch,X),pl); t=sc(w,pl)
                    if t and t[0]>=70: b.append(f"SJup→{ch} {X} {pl} {w:.6f} {t[1]} [{t[0]}]")
                    if s and t and s[0]>=50 and t[0]>=50: both.append(f"{X} {pl} {t[0]}/{s[0]}")
        print(f" {r}{ch} {rc.N[r][:22]}\n    T7/8: "+'; '.join(a)+"\n    T5/6: "+'; '.join(b)+"\n    BOTH>=50: "+('; '.join(both) or 'none'))
