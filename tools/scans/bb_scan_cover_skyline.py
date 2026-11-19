import sys,re,os,json
sys.argv=sys.argv[:1]; sys.path.insert(0,'tools'); sys.path.insert(0,'tools/scans')
import bb_scan_negatives as NG
from bb_cover8 import C
rows=[]
for race,win in NG.RACES:
    p=f'docs/eddie_read/bybody_rules/{race}_bbrules.json'
    if not os.path.exists(p): continue
    d=json.load(open(p))['rules']
    held={}
    for k,hs in d.items():
        for h in hs:
            if h.get('watch_only'): continue
            held.setdefault(h['runner'],{}).setdefault(k,[]).extend(h['cells'])
    for r,rs in held.items():
        its=[c for c in C if all(x in rs for x in c)]
        if not its: continue
        mx=0
        for c in its:
            for x in c:
                for cell in rs[x]:
                    m=re.match(r'S (\S+(?: \S+)?) – S (\S+(?: \S+)?) (RA|Dec) .*\(([\d.]+)\)$',cell)
                    if m and 'Moon' not in m.groups()[:2]: mx=max(mx,float(m.group(4)))
        rows.append((race,r,win in r,mx))
for lo,hi in ((0,50),(50,80),(80,90),(90,101)):
    R=[x for x in rows if lo<=x[3]<hi]
    print(f'cover picks, best S–S line in their cover-item cells {lo}-{hi}: {len(R)} picks, {sum(x[2] for x in R)} won')
print('Newmarket:',[x for x in rows if 'newmarket_1413' in x[0]])
names=[r for r,_ in NG.RACES]; i=names.index('20261116_wolverhampton_aw_1800')
after=set(names[i:])
print('races since the cover was fixed:',len(after))
for lo,hi in ((0,90),(90,101)):
    R=[x for x in rows if lo<=x[3]<hi and x[0] in after]
    print(f'  {lo}-{hi}: {len(R)} picks, {sum(x[2] for x in R)} won  ', [(x[0][9:],x[1][3:],'W' if x[2] else '') for x in R])
