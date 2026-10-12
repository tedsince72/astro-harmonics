import sys,glob,itertools,openpyxl
sys.path.insert(0,'/tmp/claude-0/-home-claude-astro-harmonics/a6920965-38c7-5676-b509-936bc1207077/scratchpad/yk')
exec(open('/tmp/claude-0/-home-claude-astro-harmonics/a6920965-38c7-5676-b509-936bc1207077/scratchpad/yk/scan.py').read().split('for f in sorted')[0])
for f in sorted(glob.glob(sys.argv[1]+'/*.xlsx')):
    wb=openpyxl.load_workbook(f,data_only=True); S,H,J=load(wb,'TRANS'),load(wb,'P01'),load(wb,'P02')
    nm=f"{wb['P01'].cell(2,1).value[:20]}/{wb['P02'].cell(2,1).value[:18]}"
    R={'H':{},'J':{}}
    for c,N in(('H',H),('J',J)):
        for x,y in itertools.permutations(N,2):
            if {x,y}=={'Rahu','Ketu'}: continue
            for pl,f_ in(('RA',rd),('Dec',dd),('GC',gc)):
                sv,nv=f_(S[x],S[y]),f_(N[x],N[y])
                if min(sv,nv)<0.5: continue
                e,fr=frac(max(sv,nv)/min(sv,nv))
                if fr and fr!='1' and e<=0.00005: R[c].setdefault(x,set()).add(f'{y} {pl} {fr}')
    both=sorted(set(R['H'])&set(R['J']))
    cl=[(x,y) for x in H for y in J if (rd(H[x],J[y])<1.5 or dd(H[x],J[y])<0.3) and x in R['H'] and y in R['J']]
    print(f"{nm:40s} ratioBodies H{len(R['H'])} J{len(R['J'])} inBoth={both}  XL-with-ratio-ends={[(x,y,round(rd(H[x],J[y]),3),round(dd(H[x],J[y]),3)) for x,y in cl]}")
