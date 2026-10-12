import sys,glob,itertools,openpyxl
D=sys.argv[1]; sys.argv=['x','x']
exec(open('/tmp/claude-0/-home-claude-astro-harmonics/a6920965-38c7-5676-b509-936bc1207077/scratchpad/yk/scan.py').read().split('for f in sorted')[0])
for f in sorted(glob.glob(D+'/*.xlsx')):
    wb=openpyxl.load_workbook(f,data_only=True); S,H,J=load(wb,'TRANS'),load(wb,'P01'),load(wb,'P02')
    nm=f"{wb['P01'].cell(2,1).value[:20]}/{wb['P02'].cell(2,1).value[:18]}"
    a=[]
    for x in H:
        for y in J:
            if x==y or {x,y}=={'Rahu','Ketu'}: continue
            if (rd(H[x],J[y])<1.5 or dd(H[x],J[y])<0.3) and gc(S[x],S[y])<5: a.append(f"H{x}-J{y} xl {rd(H[x],J[y]):.2f}/{dd(H[x],J[y]):.2f} sky GC {gc(S[x],S[y]):.2f}")
    b=[]
    for x,y in itertools.combinations(BOD,2):
        if {x,y}=={'Rahu','Ketu'}: continue
        cl=lambda N:(rd(N[x],N[y])<1.5 or dd(N[x],N[y])<0.6)
        if cl(H) and cl(J): b.append(f"{x}-{y} H {rd(H[x],H[y]):.2f}/{dd(H[x],H[y]):.2f} J {rd(J[x],J[y]):.2f}/{dd(J[x],J[y]):.2f}")
    print(nm); print('   skyAlso:', a); print('   bothCharts:', b)
