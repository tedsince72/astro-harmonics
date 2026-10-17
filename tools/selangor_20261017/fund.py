import openpyxl, re, sys, collections
U='/root/.claude/uploads/a6920965-38c7-5676-b509-936bc1207077/'
races=[('12:15','7566745e'),('12:45','2673848e'),('13:15','e96aa387'),('13:45','afee33f2'),('14:15','929b5b49'),('14:45','8a883cbf'),
('15:15','792f2545'),('15:45','49a23bd4'),('16:15','4f275ecf'),('16:45','61dc3d7a'),('17:15','692f0455'),('17:45','a6b9a230')]
import glob
AREA_A={'1','3/2','2','3','4','5','6','7','8','9'}
lre=re.compile(r'→ (.+?) \((\d+\.\d+)\) \[(T\d+)')
def isJ(l): return bool(re.search(r'(^|[ /|→])J ',l))
only=sys.argv[1:] 
for hhmm,pre in races:
    if only and hhmm not in only: continue
    f=glob.glob(U+pre+'-*jupiter_tables.xlsx')[0]
    wb=openpyxl.load_workbook(f,read_only=True)
    rows=list(wb['THREADS'].iter_rows(values_only=True))
    hdr=[r for r in rows if r and r[0]=='body'][0]
    runners=[(i,str(h).split(' / ')[0]) for i,h in enumerate(hdr) if h and str(h).startswith('P')]
    data=collections.defaultdict(dict)  # runner -> body -> list(lines)
    for r in rows:
        if not r or not r[0] or r is hdr or r[0]=='body': continue
        for i,name in runners:
            if i>=len(r) or not r[i]: continue
            L=[l for l in str(r[i]).split('\n') if lre.search(l) and not isJ(l)]
            if L: data[name][r[0]]=L
    fund=collections.defaultdict(list); cnt=collections.Counter()
    for name in data:
        for body,L in data[name].items():
            P=[(l,)+lre.search(l).groups() for l in L]
            t5=[p for p in P if p[3]=='T5']; t7=[p for p in P if p[3]=='T7']
            t5=[p for p in t5 if p[1]!='conj']; t7=[p for p in t7 if p[1]!='conj']
            if t5 and t7:
                a=max(t5,key=lambda p:float(p[2])); b=max(t7,key=lambda p:float(p[2]))
                fund[name].append(('RECIP',body,min(float(a[2]),float(b[2])),[a[0],b[0]])); cnt[('RECIP',body)]+=1
            ra=[p for p in P if p[3] in('T12','T13') and p[1] in AREA_A and float(p[2])>=70]
            for p in ra:
                fund[name].append(('RATIO-A',body,float(p[2]),[p[0]])); cnt[('RATIO-A',body,p[1])]+=1
            tabs={p[3] for p in P if p[1]!='conj'}
            if len(tabs)>=3:
                fund[name].append(('THREAD',body,len(tabs),[p[0] for p in P])); cnt[('THREAD',body)]+=1
    print(f'######## {hhmm}  ({len(runners)} runners)')
    for i,name in runners:
        F=fund.get(name,[])
        kinds=sorted({k for k,*_ in F})
        print(f'== {name}   kinds={kinds} n={len(F)}')
        for k,body,s,ls in F:
            key=(k,body) if k!='RATIO-A' else (k,body,lre.search(ls[0]).group(1))
            print(f'   {k:7s} {body:10s} [{s}] holders {cnt[key]}/{len(runners)}')
            for l in ls: print('        ',l)
