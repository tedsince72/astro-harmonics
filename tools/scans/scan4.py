import sys,glob,itertools,openpyxl,re
D=sys.argv[1]; O=sys.argv[2] if len(sys.argv)>2 else None; sys.argv=['x','x']
exec(open('/tmp/claude-0/-home-claude-astro-harmonics/a6920965-38c7-5676-b509-936bc1207077/scratchpad/yk/scan.py').read().split('for f in sorted')[0])
def strikes(S,P,skip=('Ketu',)):
    return [f'{s} {pl} {on(v)}' for s in S if s not in skip for pl,v in(('RA',rd(S[s],P)),('Dec',dd(S[s],P)),('GC',gc(S[s],P))) if v>=0.5 and on(v)]
for f in sorted(glob.glob(D+'/*.xlsx')):
    wb=openpyxl.load_workbook(f,data_only=True); S,H,J=load(wb,'TRANS'),load(wb,'P01'),load(wb,'P02')
    nm=f"{wb['P01'].cell(2,1).value[:20]}/{wb['P02'].cell(2,1).value[:18]}"
    out=[]
    for x in H:
        for y in J:
            if not(rd(H[x],J[y])<1.5 or dd(H[x],J[y])<0.3): continue
            a,b=strikes(S,H[x]),strikes(S,J[y])
            pa=[s for s in a if s.split()[0]==y]; pb=[s for s in b if s.split()[0]==x]
            tag=('BOTHSTRUCK ' if a and b else '')+('PARTNER ' if pa or pb else '')
            if tag: out.append(f"  {tag}H {x}-J {y} ({rd(H[x],J[y]):.3f}/{dd(H[x],J[y]):.3f}) Hend {len(a)} Jend {len(b)} partner {pa+pb}")
    eq=[]
    for b in BOD:
        if b=='Ketu': continue
        h,j=abs(H[b][1]),abs(J[b][1])
        if min(h,j)<0.5: continue
        e,fr=frac(max(h,j)/min(h,j))
        if e<=0.0001: eq.append(f'{b} {fr} {e*100:.4f}%')
    out.append('  EQ H/J <=0.01%: '+'; '.join(eq))
    print(nm); print('\n'.join(out))
