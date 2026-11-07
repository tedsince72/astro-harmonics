import json,glob,sys
sys.path.insert(0,'/tmp/f1240'); from top2 import feats,horse,R
tot={}
def add(k,race,rows,sel,res):
    n=len(rows); t2={h.lower() for h in res['first']+res['second']}
    hit=sum(1 for h in sel if h in t2); exact= set(sel)==t2
    v=tot.setdefault(k,[0,0,0.0,0,0]); v[0]+=len(sel); v[1]+=hit; v[2]+=len(sel)*len(t2)/res['ran']; v[3]+=1 if sel else 0; v[4]+=exact
for fn in sorted(glob.glob('docs/eddie_read/*_layers.json')):
    race=fn.split('race_batch_')[1].replace('_layers.json','')
    if race=='20261106_aintree_1240' or race not in R: continue
    res=R[race]; d=json.load(open(fn)); nr={x.lower() for x in res.get('nonrunners',[])}
    rows=[(horse(p['name']),feats(p)) for p in d['report'].values()]; rows=[r for r in rows if r[0] not in nr]
    add('F1 S Sun on Sedna',race,rows,[h for h,f in rows if f['sun_sedna']],res)
    add('F2 Deneb Algedi on Venus+Quaoar',race,rows,[h for h,f in rows if f['DA_venus_quaoar']],res)
    v=sorted({f['n50 S Sun'] for h,f in rows},reverse=True)[:2]
    add('F3 top two counts of Sun cells',race,rows,[h for h,f in rows if f['n50 S Sun'] in v and v[0]-f['n50 S Sun']<= (v[0]-v[-1])],res)
print('filter: picks, of them 1st or 2nd, by chance, races fired, exact 1st+2nd')
for k,v in tot.items(): print(f'  {k}: {v[0]} picks, {v[1]} 1st/2nd, chance {v[2]:.1f}, fired {v[3]}, exact {v[4]}')
