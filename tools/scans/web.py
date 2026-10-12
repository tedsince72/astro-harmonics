import sys,glob,itertools,openpyxl
exec(open('/tmp/claude-0/-home-claude-astro-harmonics/a6920965-38c7-5676-b509-936bc1207077/scratchpad/yk/scan.py').read().split('for f in sorted')[0])
for f in sorted(glob.glob(sys.argv[1]+'/*.xlsx')):
    wb=openpyxl.load_workbook(f,data_only=True); S,H,J=load(wb,'TRANS'),load(wb,'P01'),load(wb,'P02')
    nm=f"{wb['P01'].cell(2,1).value[:20]}/{wb['P02'].cell(2,1).value[:18]}"
    E={}
    def add(a,b,l): E.setdefault(a,{})[b]=l; E.setdefault(b,{})[a]=l
    for c,N in(('H',H),('J',J)):
        for x,y in itertools.combinations(N,2):
            if {x,y}=={'Rahu','Ketu'}: continue
            for pl,f_ in(('RA',rd),('Dec',dd),('GC',gc)):
                sv,nv=f_(S[x],S[y]),f_(N[x],N[y])
                if min(sv,nv)<0.5: continue
                e,fr=frac(max(sv,nv)/min(sv,nv))
                if fr and fr!='1' and e<=0.00005: add((c,x),(c,y),f'{pl} {fr}')
    rn=set(E)
    for x in H:
        for y in J:
            if ('H',x) in rn and ('J',y) in rn and (rd(H[x],J[y])<1.5 or dd(H[x],J[y])<0.3): add(('H',x),('J',y),f'XL RA{rd(H[x],J[y]):.2f} Dec{dd(H[x],J[y]):.2f}')
    seen=set(); comps=[]
    for n in E:
        if n in seen: continue
        st=[n]; comp=set()
        while st:
            m=st.pop()
            if m in comp: continue
            comp.add(m); st+=list(E[m])
        seen|=comp; comps.append(comp)
    comps.sort(key=len,reverse=True); big=comps[0] if comps else set()
    print(f"{nm:40s} nodes {len(E):2d} biggest {len(big):2d} crosses-charts {'Y' if len({c for c,_ in big})==2 else 'n'}: "+' '.join(sorted(f'{c}{b}' for c,b in big)))
