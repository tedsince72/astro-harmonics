import sys,glob,openpyxl
D=sys.argv[1]; sys.argv=['x','x']
exec(open('/tmp/claude-0/-home-claude-astro-harmonics/a6920965-38c7-5676-b509-936bc1207077/scratchpad/yk/scan.py').read().split('for f in sorted')[0])
for f in sorted(glob.glob(D+'/*.xlsx')):
    wb=openpyxl.load_workbook(f,data_only=True); S,H,J=load(wb,'TRANS'),load(wb,'P01'),load(wb,'P02')
    nm=f"{wb['P01'].cell(2,1).value[:20]}/{wb['P02'].cell(2,1).value[:18]}"
    out=[]
    for c,N in(('S',S),('H',H),('J',J)):
        for b,(ra,de) in N.items():
            if b=='Ketu': continue
            v=abs(de); w=round(v)
            if w>0 and abs(v-w)<=0.01: out.append(f"{c} {b} {de:+.4f}")
    print(f"{nm:40s} "+'; '.join(out))
