import json,glob,collections,sys,os,re
sys.path.insert(0,os.path.dirname(__file__))
from intervals import on_list,frac
D=os.path.dirname(__file__)
cnt=collections.defaultdict(collections.Counter); offl=[]; shared=collections.Counter()
for f in sorted(glob.glob('docs/jupiter/*/layer2/P*.json')):
    race=f.split('/')[2]; d=json.load(open(f)); r=os.path.basename(f)[:3]
    for it in d['items']:
        k=it['kind']
        if k=='shared':
            shared[(race,'<=0.15%' if it['err']<=0.15 else '>0.15%')]+=1; continue
        rs=it['ratios'] if 'ratios' in it else [it['ratio']]
        bad=[x for x in rs if not on_list(frac(x))]
        band=it.get('band') or ('set<=0.15%' if k=='set' else 'pairset<=0.05%')
        st='off' if bad else 'on'
        cnt[race][(k,band,st)]+=1
        if bad: offl.append((race,r,k,band,'off: '+','.join(bad),it['text']))
# layer3 splits (19) and item 23
for f in sorted(glob.glob('docs/jupiter/*/layer3/P*.json')):
    race=f.split('/')[2]; d=json.load(open(f)); r=os.path.basename(f)[:3]
    for it in d['items']:
        if it['m']==19:
            m=re.search(r'(parts|span/other) (\S+) \(([\d.]+)%\)',it['text'])
            x=m.group(2); st='on' if on_list(frac(x)) else 'off'
            cnt[race][('split19','<=0.25%',st)]+=1
            if st=='off': offl.append((race,r,'split19','<=0.25%','off: '+x,it['text']))
        if it['m']==23:
            rs=re.findall(r' (\d+(?:/\d+)?)(?= \|\||$)',it['text'])
            bad=[x for x in rs if not on_list(frac(x))]
            st='off' if bad else 'on'
            cnt[race][('both23','-',st)]+=1
            if bad: offl.append((race,r,'both23','-','off: '+','.join(bad),it['text']))
kinds=sorted({k[:2] for c in cnt.values() for k in c})
with open(os.path.join(D,'jr1_counts.txt'),'w') as o:
    tot=collections.Counter()
    for r in sorted(cnt):
        print(r,file=o)
        for kb in kinds:
            a,b=cnt[r][kb+('on',)],cnt[r][kb+('off',)]
            if a or b: print(f'   {kb[0]:8} {kb[1]:16} on {a:4}  off {b:4}',file=o)
        tot.update(cnt[r])
    print('TOTAL',file=o)
    for kb in kinds: print(f'   {kb[0]:8} {kb[1]:16} on {tot[kb+("on",)]:4}  off {tot[kb+("off",)]:4}',file=o)
    print('\nshared (item 13, ratio 1; old <=0.5%) by err:',file=o)
    t=collections.Counter()
    for (rc,b),v in shared.items(): t[b]+=v
    print(dict(t),file=o)
    for (rc,b),v in sorted(shared.items()): print('  ',rc,b,v,file=o)
with open(os.path.join(D,'jr1_offlist_all.txt'),'w') as o:
    for x in offl: print('\t'.join(x),file=o)
