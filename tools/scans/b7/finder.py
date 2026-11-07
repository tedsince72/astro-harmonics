# For a race with a known result: stage 2 items held by the winner alone, and by the 1st + 2nd only (non-runners left out).
import json,re,sys,collections
race=sys.argv[1]; MIN=float(sys.argv[2]) if len(sys.argv)>2 else 50
R=json.load(open('docs/eddie_read/results/results.json'))[race]
d=json.load(open(f'docs/eddie_read/race_batch_{race}_layers.json'))
def sc(t):
    m=re.search(r'\(([\d.]+)\)\s*$',t); return float(m.group(1)) if m else 0.0
def horse(n): return n.split(' / ')[0].split(' ',1)[1].strip()
nr=set(R.get('nonrunners',[])); W=set(R['first']); S=set(R['second'])
hold=collections.defaultdict(dict)   # item -> horse -> [texts]
for p in d['report'].values():
    h=horse(p['name'])
    if h in nr: continue
    for b in p['bodies']:
        for c in b['cells']:
            if sc(c['text'])>=MIN: hold[('L4 '+c['layer'],)+tuple(c['key'])].setdefault(h,[]).append(c['text'])
    for k,v in p['cases'].items():
        for x in v:
            if k in ('4','5') and max(sc(t) for t in x['cells'])<MIN: continue
            lab=x['label'] if k!='4' else x['label']
            hold[(f'L3 case {k}',lab)].setdefault(h,[]).extend(x['cells'])
runners=[horse(p['name']) for p in d['report'].values() if horse(p['name']) not in nr]
print('runners',runners,'| 1st',W,'2nd',S)
for title,want in (('WINNER ALONE',W),('1st + 2nd ONLY',W|S)):
    print('=====',title)
    for k,m in sorted(hold.items()):
        if set(m)==want:
            print(' ',' | '.join(k))
            for h in sorted(m): print('     ',h,':','; '.join(sorted(set(m[h]))[:4]))
