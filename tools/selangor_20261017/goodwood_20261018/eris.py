import sys; sys.path.insert(0,sys.argv[1]); import rc
rc.load_file('reference/classic/race_batch_20210827_goodwood_1853_jupiter_tables.xlsx')
d=rc.d;p=rc.pos;fam=rc.fam;W='P09'
PL=('RA','Dec','Equator')
def line(lbl,A,B):
    s=[]
    for pl in PL:
        v=d(A,B,pl)
        if pl=='Equator' and (A[1]>=0)==(B[1]>=0): continue
        s.append(f"{pl} {v:.6f} {fam(v,pl)}")
    print(f"  {lbl}: "+' | '.join(s))
print("== positions (RA, Dec)")
for c in 'SHJ':
    for b in ('Jupiter','Eris'): print(f"  {c} {b}: {p(W,c,b)[0]:.6f} {p(W,c,b)[1]:+.6f}")
print("== every Jupiter–Eris link, winner")
for a,b in [(('S','Jupiter'),('S','Eris')),(('H','Jupiter'),('H','Eris')),(('J','Jupiter'),('J','Eris')),(('S','Jupiter'),('H','Eris')),(('S','Eris'),('H','Jupiter')),
            (('S','Jupiter'),('J','Eris')),(('S','Eris'),('J','Jupiter')),(('H','Jupiter'),('J','Eris')),(('J','Jupiter'),('H','Eris')),(('H','Eris'),('J','Eris'))]:
    line(f"{a[0]} {a[1]} – {b[0]} {b[1]}",p(W,*a),p(W,*b))
print("== field: S Eris → natal Jupiter and S Jupiter → natal Eris, RA/Dec")
for r in rc.RUN:
    for ch in 'HJ':
        o=[]
        for pl in ('RA','Dec'):
            v=d(p(r,'S','Eris'),p(r,ch,'Jupiter'),pl); w=d(p(r,'S','Jupiter'),p(r,ch,'Eris'),pl); n=d(p(r,ch,'Jupiter'),p(r,ch,'Eris'),pl)
            o.append(f"{pl}: SEris→{ch}Jup {v:.6f} {fam(v,pl)} ; SJup→{ch}Eris {w:.6f} {fam(w,pl)} ; natal {n:.6f} {fam(n,pl)}")
        print(f"  {r}{ch} "+' || '.join(o))
print("== Eris with royal stars and other stars, hits only")
ST=['Aldebaran','Regulus','Antares','Fomalhaut','Algol','Pleiades','Capella','Sirius','Procyon','Alkaid','Algorab','Spica','Arcturus','Alphecca','Vega','Deneb Algedi','Rigel','Betelgeuse','Polaris','Castor','Altair','Bellatrix']
for c in 'SHJ':
    for st in ST:
        for pl in PL:
            A=p(W,c,'Eris');B=p(W,c,st)
            if pl=='Equator' and (A[1]>=0)==(B[1]>=0): continue
            v=d(A,B,pl); b=rc.fm.best(v,pl,'deg')
            if b and b['score']>=50: print(f"  {c} Eris – {c} {st} {pl} {v:.6f} → {b['target']} ({b['family']}) [{b['score']:.2f}]")
print("== stars between S Eris and H Jupiter (RA) and between S Jupiter and H Eris (Dec)")
for st in ST:
    for (A,B,pl,lbl) in [(p(W,'S','Eris'),p(W,'H','Jupiter'),'RA','S Eris→H Jup'),(p(W,'S','Jupiter'),p(W,'H','Eris'),'Dec','S Jup→H Eris'),(p(W,'S','Eris'),p(W,'H','Jupiter'),'Dec','S Eris→H Jup')]:
        s=p(W,'S',st); t=d(A,B,pl); a=d(A,s,pl); c=d(s,B,pl)
        if abs(a+c-t)<0.01*t:
            fa=rc.fm.best(a,pl,'deg'); fc=rc.fm.best(c,pl,'deg')
            if (fa and fa['score']>=50) or (fc and fc['score']>=50): print(f"  {lbl} {pl} via S {st}: {a:.6f} {fam(a,pl)} + {c:.6f} {fam(c,pl)} = {t:.6f}")
