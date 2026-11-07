import json,re,glob,sys
R=json.load(open('docs/eddie_read/results/results.json'))
def sc(t):
    m=re.search(r'\(([\d.]+)\)\s*$',t); return float(m.group(1)) if m else 0.0
def horse(n): return n.split(' / ')[0].split(' ',1)[1].strip().lower()
def cen(c):
    if c['layer']=='top rows': return {c['text'].split(' →')[0]}
    return {s.split(' →')[0] for s in c['source_lines']}
def feats(p):
    f={}
    cells=[c for b in p['bodies'] for c in b['cells']]
    for C in ('S Sun','S Moon','S Jupiter'):
        f['n50 '+C]=len({c['text'] for c in cells if C in cen(c) and sc(c['text'])>=50})
    f['sun_sedna']=any(c['layer']=='top rows' and c['text'].startswith('S Sun →') and ' Sedna ' in c['text'] and sc(c['text'])>=50 for c in cells)
    da={b['body'] for b in p['bodies'] for c in b['cells'] if c['layer']=='star rows' and re.match(r'[HJ] Deneb Algedi →',c['text']) and sc(c['text'])>=50}
    f['DA_venus_quaoar']= {'Venus','Quaoar'}<=da
    return f
if __name__=='__main__':
    race=sys.argv[1]; d=json.load(open(f'docs/eddie_read/race_batch_{race}_layers.json'))
    res=R[race]; print(res['order'])
    for pk,p in d['report'].items(): print(pk,horse(p['name']),feats(p))
