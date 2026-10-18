import sys,io,contextlib; sys.path.insert(0,sys.argv[1]); import rc
rc.load_file('reference/classic/race_batch_20210822_worcester_1300_jupiter_tables.xlsx')
R=rc.RUN; p=rc.pos
for ch,x,y,pl in [('H','Procyon','Vega','Dec'),('H','Alkaid','Algorab','Equator'),('H','Regulus','Castor','Dec')]:
    print(f"\n## T21 {ch} {x}-{y} {pl}")
    for r in R: print(' ',r,rc.ratio3(p(r,ch,'Jupiter'),p(r,ch,x),p(r,ch,y),pl))
print("\n## T17 J Jup: J Saturn = J Uranus RA")
for r in R:
    for ch in 'HJ': print(' ',r,ch,rc.ratio3(p(r,ch,'Jupiter'),p(r,ch,'Saturn'),p(r,ch,'Uranus'),'RA'))
print("\n## T3 H Jup->J Vesta Dec / T8 S Vesta->J Jup Dec")
for r in R: print(' ',r, round(rc.d(p(r,'H','Jupiter'),p(r,'J','Vesta'),'Dec'),6), rc.fam(rc.d(p(r,'H','Jupiter'),p(r,'J','Vesta'),'Dec'),'Dec'))
# sky timeline star events
ws=rc.rows('SKY JUPITER'); on=False
for row in ws:
    t=rc.trim(row)
    if t and isinstance(t[0],str) and t[0].startswith('TIMELINE'): on=True
    if t and isinstance(t[0],str) and t[0].startswith('LONG TIMELINE'): break
    if on and t: print(' | '.join(str(c) for c in t[:12]))
