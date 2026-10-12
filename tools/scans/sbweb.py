import sys,glob,itertools,openpyxl,re
D=sys.argv[1]; O=sys.argv[2]; sys.argv=['x','x']
exec(open('/tmp/claude-0/-home-claude-astro-harmonics/a6920965-38c7-5676-b509-936bc1207077/scratchpad/yk/scan.py').read().split('for f in sorted')[0])
for f in sorted(glob.glob(D+'/*.xlsx')):
    t=re.search(r'__(P\d+)',f).group(1)
    sb=set()
    txt=open(f'{O}/{t}_same_body.txt').read().split('within 0.15%')[1].split('best set')[0]
    for l in txt.splitlines():
        p=l.split()
        if len(p)>2: sb.add('Rahu' if p[1] in('Rahu','Ketu') else p[1])
    wb=openpyxl.load_workbook(f,data_only=True); S,H,J=load(wb,'TRANS'),load(wb,'P01'),load(wb,'P02')
    nm=f"{wb['P01'].cell(2,1).value[:20]}/{wb['P02'].cell(2,1).value[:18]}"
    E={}
    def add(a,b): E.setdefault(a,set()).add(b); E.setdefault(b,set()).add(a)
    for c,N in(('H',H),('J',J)):
        for x,y in itertools.combinations(N,2):
            if {x,y}=={'Rahu','Ketu'}: continue
            for pl,f_ in(('RA',rd),('Dec',dd),('GC',gc)):
                sv,nv=f_(S[x],S[y]),f_(N[x],N[y])
                if min(sv,nv)<0.5: continue
                e,fr=frac(max(sv,nv)/min(sv,nv))
                if fr and fr!='1' and e<=0.00005: add((c,x),(c,y))
    for x in H:
        for y in J:
            if rd(H[x],J[y])<1.5 or dd(H[x],J[y])<0.3: add(('H',x),('J',y))   # all cross links this time
    seen=set(); best=(0,[])
    for n in E:
        if n in seen: continue
        st=[n]; comp=set()
        while st:
            m=st.pop()
            if m in comp: continue
            comp.add(m); st+=list(E[m])
        seen|=comp
        hit=sorted({('Rahu' if b in('Rahu','Ketu') else b) for _,b in comp}&sb)
        if len(hit)>best[0]: best=(len(hit),hit,len(comp))
    print(f"{nm:40s} sameBody {sorted(sb)}  joined-in-one-component {best[0]} {best[1]} comp size {best[2] if best[0] else 0}")
