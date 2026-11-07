import json,re,sys
d=json.load(open(sys.argv[1]))
def sc(t):
    m=re.search(r'\(([\d.]+)\)\s*$',t); return float(m.group(1)) if m else 0.0
def centres(srcs): return sorted({s.split(' →')[0] for s in srcs})
for pk,p in d['report'].items():
    print('=====',p['name'])
    for L in p['landings']:
        sbs=max([sc(x) for x in L['same_body']] or [0])
        for kind in ('on_this_chart','other_chart_same_body','on_other_chart','body_lines'):
            for c in L[kind]:
                t=c['text'] if isinstance(c,dict) else c
                src=c.get('source_lines',[]) if isinstance(c,dict) else []
                if sc(t)>=50 and sbs>=50:
                    print(f'  SB {L["chart"]} {L["body"]} ({sbs}) <- [{kind}] {t} | centres {centres(src)} | {src}')
    # top rows only
    for b in p['bodies']:
        for c in b['cells']:
            if c['layer']=='top rows' and sc(c['text'])>=80: print('  TOP',c['text'],'|',c['field'])
