import json,glob,collections,sys,os,re
sys.path.insert(0,os.path.dirname(__file__))
from intervals import on_list,frac
D=os.path.dirname(__file__)
F=r'(\d+(?:/\d+)?)'
def ratios(it,w):
    if it==11:
        m=re.match(r'ratio '+F+':',w); return [m.group(1)] if m else None
    if it==15:
        m=re.search(r'H:J '+F+', H:S '+F+', J:S '+F,w); return list(m.groups())
    if it in (16,17,18):
        m=re.search(r'-> '+F+' : '+F+' : '+F,w); return list(m.groups())
    if it==19:
        m=re.search(r'(?:parts|span/other) '+F+r' \(',w); return [m.group(1)]
    if it==23:
        return re.findall(r' '+F+r' [\d.]+%\)',w)
    if it in (22,24,26):
        m=re.findall(r'(?:sky/natal|natal/sky|[A-Z]{1,2}/[A-Z]{1,2}) '+F+r' \(',w); return m
    return None
cnt=collections.defaultdict(collections.Counter); off=[]; shared=collections.Counter(); bad_parse=collections.Counter()
for f in sorted(glob.glob('docs/classic/*/checklist/P*.json')):
    race=f.split('/')[2]; r=os.path.basename(f)[:3]
    for i in json.load(open(f))['instances']:
        it=i['item']; w=i['what']
        if it in (13,14):
            m=re.search(r'\(([\d.]+)%\)',w)
            if m: shared[(it,i['level'],'<=0.15%' if float(m.group(1))<=0.15 else '>0.15%')]+=1
            continue
        rs=ratios(it,w)
        if rs is None: continue
        if not rs: bad_parse[it]+=1; continue
        b=[x for x in rs if not on_list(frac(x))]
        cnt[(it,i['level'])]['off' if b else 'on']+=1
        cnt[(it,i['level'],'blind' if race.endswith('_20261012') else 'other')]['off' if b else 'on']+=1
        if b: off.append((race,r,str(it),i['level'],'off: '+','.join(b),w))
with open(os.path.join(D,'cr_counts.txt'),'w') as o:
    print('item level           on    off   (all 50 CR races)',file=o)
    for k in sorted(k for k in cnt if len(k)==2): print(f'{k[0]:4} {k[1]:8} {cnt[k]["on"]:7} {cnt[k]["off"]:6}',file=o)
    print('\nsplit blind(_20261012) vs other:',file=o)
    for k in sorted(k for k in cnt if len(k)==3): print(f'{k[0]:4} {k[1]:8} {k[2]:6} {cnt[k]["on"]:7} {cnt[k]["off"]:6}',file=o)
    print('\nitems 13/14 shared pairs (ratio 1) by % apart vs new 0.15%:',file=o)
    for k,v in sorted(shared.items()): print(k,v,file=o)
    print('unparsed:',dict(bad_parse),file=o)
with open(os.path.join(D,'cr_offlist_all.txt'),'w') as o:
    for x in off: print('\t'.join(x),file=o)
