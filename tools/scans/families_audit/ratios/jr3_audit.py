import json,glob,collections,sys,os
sys.path.insert(0,os.path.dirname(__file__))
from intervals import on_list,nearest
LV=('strict','exact-in-race','exact-pre-off','near')
cnt=collections.defaultdict(collections.Counter); offl=[]; tgt=collections.Counter()
for f in sorted(glob.glob('docs/classic/*/jupiter/P*.json')):
    race=f.split('/')[2]; d=json.load(open(f))
    for h in d['hits']:
        if h['unit']!='%': continue
        k=on_list(h['target_value']); st='on' if k else 'off'
        cnt[race][(h['level'],st)]+=1
        tgt[(h['target'],st)]+=1
        if not k:
            pct=100*(h['value']/h['target_value']-1)
            offl.append((race,os.path.basename(f)[:3],h['level'],h['m'],h['plane'],h['desc'],h['target'],round(h['value'],5),round(h['offset'],5) if h['offset'] is not None else None,h['family'],d.get('horse'),d.get('jockey')))
out=open(os.path.join(os.path.dirname(__file__),'jr3_counts.txt'),'w')
hdr='race'.ljust(28)+' '.join(f'{l[:9]+":on":>14}{l[:9]+":off":>15}' for l in LV)
print(hdr,file=out)
tot=collections.Counter()
for r in sorted(cnt):
    print(r.ljust(28)+' '.join(f'{cnt[r][(l,"on")]:>14}{cnt[r][(l,"off")]:>15}' for l in LV),file=out); tot.update(cnt[r])
print('TOTAL'.ljust(28)+' '.join(f'{tot[(l,"on")]:>14}{tot[(l,"off")]:>15}' for l in LV),file=out)
print('\nTargets (label, on/off): count',file=out)
for k,v in sorted(tgt.items(),key=lambda x:-x[1]): print(k,v,file=out)
out.close()
with open(os.path.join(os.path.dirname(__file__),'jr3_offlist_all.txt'),'w') as o:
    print('race\trunner\tlevel\tmeasure\tplane\tdesc\ttarget\tvalue\toffset%\tfamily\thorse\tjockey',file=o)
    for x in offl: print('\t'.join(map(str,x)),file=o)
with open(os.path.join(os.path.dirname(__file__),'jr3_offlist_blind_strict_exact.txt'),'w') as o:
    for x in offl:
        if x[0].endswith('_20261012') and x[2]!='near': print('\t'.join(map(str,x)),file=o)
