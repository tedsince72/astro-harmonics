# B9/B10 shape from other sky bodies: S X -> natal body >= 50 and 2+ line stars (of the given centres) on that body, same chart.
import json,glob,collections,sys
R=json.load(open('docs/eddie_read/results/results.json'))
def picks(d,src,cents,nmin=2):
    ls={st for st,c in d['star_centre'].items() if set(c)&cents}
    dr,stv=collections.defaultdict(list),collections.defaultdict(set)
    for p in d['pieces']:
        if p.get('score') is None or p['score']<50: continue
        k=(p['runner'],p['chart'],p['body'])
        if p['layer']=='top rows' and src(p['source']) and p['source']!='S '+p['body']: dr[k].append(p['source'])
        if p['layer']=='star rows' and p['source'].startswith(p['chart']+' ') and p.get('star') in ls: stv[k].add(p['star'])
    return {k[0] for k in dr if len(stv[k])>=nmin}
def run(name,src,cents):
    tot=collections.Counter();ch=0.0;c2=0.0
    for fn in sorted(glob.glob('docs/eddie_read/*_eddie_read.json')):
        race=fn.split('race_batch_')[1].replace('_eddie_read.json','')
        if race not in R: continue
        rs=R[race]; d=json.load(open(fn))
        def h(P): return d['names'][P].split(' / ')[0].split(' ',1)[1].strip()
        sel=[h(P) for P in picks(d,src,cents) if h(P) not in rs.get('nonrunners',[])]
        W=set(rs['first']); T=W|set(rs['second'])
        tot['p']+=len(sel); tot['w']+=sum(x in W for x in sel); tot['t']+=sum(x in T for x in sel); tot['f']+=bool(sel)
        ch+=len(sel)/rs['ran']; c2+=len(sel)*len(T)/rs['ran']
    print(f"{name}: 20 races {tot['p']} picks in {tot['f']} races, {tot['w']} won (chance {ch:.1f}), 1st/2nd {tot['t']} ({c2:.1f})")
run('Moon + 2 Moon-line stars',lambda s:s=='S Moon',{'Moon'})
run('Jupiter + 2 line stars of any centre',lambda s:s=='S Jupiter',{'Jupiter','Sun','Moon'})
run('Sun + 2 line stars of any centre',lambda s:s=='S Sun',{'Jupiter','Sun','Moon'})
run('any other sky body (not Jupiter/Sun/Moon) + 2 line stars of any centre',lambda s:s.startswith('S ') and s not in ('S Jupiter','S Sun','S Moon'),{'Jupiter','Sun','Moon'})
run('any sky body + 2 line stars of any centre',lambda s:s.startswith('S '),{'Jupiter','Sun','Moon'})
def picks_sb(d,cents,nmin=2,smin=50):
    ls={st for st,c in d['star_centre'].items() if set(c)&cents}
    dr,stv=set(),collections.defaultdict(set)
    for p in d['pieces']:
        if p.get('score') is None: continue
        k=(p['runner'],p['chart'],p['body'])
        if p['layer']=='same body' and p['score']>=smin: dr.add(k)
        if p['layer']=='star rows' and p['score']>=50 and p['source'].startswith(p['chart']+' ') and p.get('star') in ls: stv[k].add(p['star'])
    return {k[0] for k in dr if len(stv[k])>=nmin}
for cents,lab in (({'Jupiter','Sun','Moon'},'any centre'),({'Jupiter','Sun'},'Jupiter / Sun')):
    tot=collections.Counter();ch=0.0
    for fn in sorted(glob.glob('docs/eddie_read/*_eddie_read.json')):
        race=fn.split('race_batch_')[1].replace('_eddie_read.json','')
        rs=R[race]; d=json.load(open(fn))
        h=lambda P:d['names'][P].split(' / ')[0].split(' ',1)[1].strip()
        sel=[h(P) for P in picks_sb(d,cents) if h(P) not in rs.get('nonrunners',[])]
        tot['p']+=len(sel); tot['w']+=sum(x in rs['first'] for x in sel); ch+=len(sel)/rs['ran']
    print(f"same body X (S X -> natal X >= 50) + 2 line stars of {lab} on X: {tot['p']} picks, {tot['w']} won (chance {ch:.1f})")
