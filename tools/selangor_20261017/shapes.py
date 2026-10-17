import openpyxl,re,glob,sys
U='/root/.claude/uploads/a6920965-38c7-5676-b509-936bc1207077/'
races=[('12:15','7566745e'),('12:45','2673848e'),('13:15','e96aa387'),('13:45','afee33f2'),('14:15','929b5b49'),('14:45','8a883cbf'),
('15:15','792f2545'),('15:45','49a23bd4'),('16:15','4f275ecf'),('16:45','61dc3d7a'),('17:15','692f0455'),('17:45','a6b9a230')]
lre=re.compile(r'(RA|Dec|Equator) [-+]?[\d.]+ → (.+?) \((\d+\.\d+)\) \[(T\d+)')
isJ=lambda l: bool(re.search(r'(^|[ /|→])J ',l))
for hhmm,pre in races:
    wb=openpyxl.load_workbook(glob.glob(U+pre+'-*jupiter_tables.xlsx')[0],read_only=True)
    rows=list(wb['THREADS'].iter_rows(values_only=True)); hdr=[r for r in rows if r and r[0]=='body'][0]
    runners=[(i,str(h).split(' / ')[0]) for i,h in enumerate(hdr) if h and str(h).startswith('P')]
    M=[];S=[]
    for r in rows:
        if not r or not r[0] or r is hdr: continue
        for i,name in runners:
            if i>=len(r) or not r[i]: continue
            P=[(l,)+lre.search(l).groups() for l in str(r[i]).split('\n') if lre.search(l) and not isJ(l) and 'conj' not in l]
            d=[p for p in P if p[4] in('T5','T7') and float(p[3])>=90]
            q=[p for p in P if p[4] in('T12','T13') and float(p[3])>=70]
            if d and q: M.append((name,r[0],max(d,key=lambda p:float(p[3]))[0],max(q,key=lambda p:float(p[3]))[0]))
            t7={}
            for p in P:
                if p[4]=='T7' and p[1] in('RA','Dec') and float(p[3])>=70:
                    if p[1] not in t7 or float(p[3])>float(t7[p[1]][3]): t7[p[1]]=p
            if len(t7)==2: S.append((name,r[0],t7['RA'][0],t7['Dec'][0]))
    print(f'## {hhmm} ({len(runners)} runners)  M: {len(M)} runners-bodies, {len({m[0] for m in M})} runners | S: {len(S)}, {len({s[0] for s in S})} runners')
    if hhmm in sys.argv or '-v' in sys.argv:
        for m in M: print('   M',m[0],'|',m[1],'|',m[2],'||',m[3])
        for s in S: print('   S',s[0],'|',s[1],'|',s[2],'||',s[3])
