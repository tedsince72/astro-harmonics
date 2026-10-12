import sys,openpyxl,itertools
sys.argv=['x','x']
exec(open('/tmp/claude-0/-home-claude-astro-harmonics/a6920965-38c7-5676-b509-936bc1207077/scratchpad/yk/scan.py').read().split('for f in sorted')[0])
wb=openpyxl.load_workbook('reference/classic/newmarket_july_1745_20240816/newmarket_july_1745_20240816__P01.xlsx',data_only=True)
S,H,J=load(wb,'TRANS'),load(wb,'P01'),load(wb,'P02')
G=['Sun','Venus','Uranus','Pluto','Chiron','Rahu','Ketu','Vesta','Mercury','Jupiter']
for b in G: print(f"{b:8s} S {S[b][0]:9.4f} {S[b][1]:+8.4f}  H {H[b][0]:9.4f} {H[b][1]:+8.4f}  J {J[b][0]:9.4f} {J[b][1]:+8.4f}")
print('H Rahu-J Ketu RA',rd(H['Rahu'],J['Ketu']),'Dec',dd(H['Rahu'],J['Ketu']),' H Rahu-J Rahu RA',rd(H['Rahu'],J['Rahu']))
print('H Chiron-J Chiron RA',rd(H['Chiron'],J['Chiron']),'Dec',dd(H['Chiron'],J['Chiron']))
print('cross links all:')
for x in H:
    for y in J:
        if rd(H[x],J[y])<1.5 or dd(H[x],J[y])<0.3: print(f"   H {x}-J {y} RA {rd(H[x],J[y]):.3f} Dec {dd(H[x],J[y]):.3f}")
print('H Uranus-J Venus GC',gc(H['Uranus'],J['Venus']),' sky Uranus-Venus RA/Dec/GC',rd(S['Uranus'],S['Venus']),dd(S['Uranus'],S['Venus']),gc(S['Uranus'],S['Venus']))
for a,b in[('Venus','Pluto'),('Mercury','Pluto'),('Sun','Vesta'),('Chiron','Rahu'),('Uranus','Ketu'),('Uranus','Rahu'),('Venus','Uranus'),('Pluto','Rahu')]:
    print(f"{a}-{b}: H RA {rd(H[a],H[b]):.4f} Dec {dd(H[a],H[b]):.4f} | J RA {rd(J[a],J[b]):.4f} Dec {dd(J[a],J[b]):.4f} | S RA {rd(S[a],S[b]):.4f} Dec {dd(S[a],S[b]):.4f}")
print('moves: J Pluto Dec', dd(S['Pluto'],J['Pluto']),'sky Pluto-J Venus Dec',dd(S['Pluto'],J['Venus']), 'H Uranus moved', rd(S['Uranus'],H['Uranus']),dd(S['Uranus'],H['Uranus']),gc(S['Uranus'],H['Uranus']),'J Venus moved',rd(S['Venus'],J['Venus']),dd(S['Venus'],J['Venus']),gc(S['Venus'],J['Venus']))
print('sky bodies striking H Uranus / J Venus (whole/ninth RA/Dec/GC):')
for tgt,N,b in(('H Uranus',H,'Uranus'),('J Venus',J,'Venus'),('H Chiron',H,'Chiron'),('J Chiron',J,'Chiron')):
    hits=[]
    for s in S:
        for pl,v in(('RA',rd(S[s],N[b])),('Dec',dd(S[s],N[b])),('GC',gc(S[s],N[b]))):
            if v>=0.5 and on(v): hits.append(f'{s} {pl} {on(v)} ({v:.4f})')
    print('  ',tgt,':',hits)
