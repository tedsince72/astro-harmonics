import json,glob,collections,sys,os,re
sys.path.insert(0,os.path.dirname(__file__))
from intervals import on_list,frac
from cr_audit_lib import ratios
D=os.path.dirname(__file__)
RI={11,13,14,15,16,17,18,19,22,23,24,26}
out=open(os.path.join(D,'cr_fieldonly_changes.txt'),'w')
print('race | item level | holders now -> holders if off-list ratios dropped (13/14: shared > 0.15% dropped) | note',file=out)
for rd in sorted(glob.glob('docs/classic/*/checklist')):
    race=rd.split('/')[2]
    before=collections.defaultdict(set); after=collections.defaultdict(set)
    n=0
    for f in sorted(glob.glob(rd+'/P*.json')):
        n+=1; r=os.path.basename(f)[:3]
        for i in json.load(open(f))['instances']:
            it=i['item']
            if it not in RI: continue
            w=i['what']; k=(it,i['level'])
            if it in (13,14):
                m=re.search(r'\(([\d.]+)%\)',w); ok= m is None or float(m.group(1))<=0.15
            else:
                rs=ratios(it,w)
                if rs is None: ok=True  # item 11 'number' -> not a ratio
                else: ok=all(on_list(frac(x)) for x in rs)
            before[k].add(r)
            if ok: after[k].add(r)
    for k in sorted(before):
        b,a=before[k],after[k]
        if b==a: continue
        note=[]
        if len(b)==1 and not a: note.append('ONLY claim disappears')
        if len(b)==1 and a: pass
        if len(a)==1 and len(b)>1: note.append('becomes ONLY '+min(a))
        if not a and len(b)>1: note.append('nobody left')
        print(f'{race} | {k[0]} {k[1]} | {len(b)}: {",".join(sorted(b))} -> {len(a)}: {",".join(sorted(a)) or "-"} | {"; ".join(note)}',file=out)
out.close()
