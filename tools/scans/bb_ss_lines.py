import json,re,sys,glob,os
def ss_lines(race):
    p=f'docs/eddie_read/bybody_rules/{race}_bbrules.json'
    if not os.path.exists(p): return None
    d=json.load(open(p)); out={}
    for k,hs in d['rules'].items():
        for h in hs:
            if h.get('watch_only'): continue
            for c in h['cells']:
                m=re.match(r'S (\S+(?: \S+)?) – S (\S+(?: \S+)?) (RA|Dec) .*\(([\d.]+)\)$',c)
                if m and 'Moon' not in (m.group(1),m.group(2)):
                    out.setdefault(h['runner'],{})[c]=float(m.group(4))
    return out
if __name__=='__main__':
    race=sys.argv[1]; o=ss_lines(race)
    for r,cs in sorted(o.items()):
        v=sorted(cs.values(),reverse=True)
        print(r,'S–S lines',len(v),'>=90',sum(x>=90 for x in v),'max',v[0] if v else None)
        for c,s in sorted(cs.items(),key=lambda x:-x[1])[:3]: print('   ',c)
