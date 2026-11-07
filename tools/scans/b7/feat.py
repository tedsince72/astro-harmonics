import json,re,sys,collections
d=json.load(open(sys.argv[1]))
def sc(t):
    m=re.search(r'\(([\d.]+)\)\s*$',t); return float(m.group(1)) if m else None
for pk,p in d['report'].items():
    print('=====',pk,p['name'])
    sb=p['same_bodies']; s=[sc(x) for x in sb]
    print(' L1 same bodies',len(sb),'scored',sum(1 for x in s if x is not None),'>=50',sum(1 for x in s if x and x>=50),'H',sum(1 for x in sb if '→ H' in x),'J',sum(1 for x in sb if '→ J' in x))
    for x in sb:
        if sc(x) and sc(x)>=50: print('   ',x)
    # landings
    nl=collections.Counter()
    for L in p['landings']:
        n=len(L['on_this_chart'])+len(L['on_other_chart'])+len(L['other_chart_same_body'])+len(L['body_lines'])
        nl[L['chart']+' '+L['body']]=n
    print(' L2 landings per same body',dict(nl))
    for c,v in p['cases'].items():
        only=[x for x in v if x['field']=='only']
        print(' L3 case',c,'n',len(v),'only',len(only),[x['label'] for x in only])
    # L4: cells per layer, only
    lay=collections.Counter();lo=collections.Counter();hi=collections.Counter()
    for b in p['bodies']:
        for c in b['cells']:
            lay[c['layer']]+=1
            if c['field']=='only': lo[c['layer']]+=1
            v=sc(c['text'])
            if v and v>=80: hi[c['layer']]+=1
    print(' L4 cells',dict(lay)); print(' L4 only',dict(lo)); print(' L4 >=80',dict(hi))
