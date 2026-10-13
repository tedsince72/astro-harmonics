import glob,re,sys,os
sys.path.insert(0,os.path.dirname(__file__))
from intervals import on_list,frac
out=open(os.path.join(os.path.dirname(__file__),'watch_audit.txt'),'w')
for f in sorted(glob.glob('docs/classic/*/checklist/watch_jupiter.txt')):
    race=f.split('/')[2]
    for l in open(f):
        m=re.match(r'\s+(P\d\d) (.+?)\s{2,}HOLDS (\S+)\s+(.*)$',l.rstrip())
        if not m: continue
        p,name,codes,rest=m.groups(); codes=codes.split(',')
        ents=[e.strip() for e in rest.split(' | ')]
        verdict={}
        for e in ents:
            c=e[1]
            if c=='E':
                r=re.search(r'(?:S/H|S/J|H/J|J/H|H/S|J/S) (\S+) \(',e.split(') ',1)[0]+') ') or re.findall(r'[SHJ]/[SHJ] (\d+(?:/\d+)?) \(',e)
                rs=re.findall(r'[SHJ]/[SHJ] (\d+(?:/\d+)?) \(',e)
            elif c=='B':
                rs=re.findall(r'(\d+(?:/\d+)?)(?= :| \(worst)',e)
            else: rs=None
            if rs is None: verdict[c]=('n/a',e)
            else:
                bad=[x for x in rs if not on_list(frac(x))]
                verdict.setdefault(c,[]).append(('OFF '+','.join(bad) if bad else 'on',e))
        keep=[]
        for c in codes:
            v=verdict.get(c)
            if c in('E','B'):
                if any(s=='on' for s,_ in v): keep.append(c)
            else: keep.append(c)
        flag='' if keep else '  <== holds ONLY via off-list E/B'
        print(race,p,name.strip(),'HOLDS',','.join(codes),'| after:',','.join(keep) or '-',flag,file=out)
        for c in ('E','B'):
            for s,e in (verdict.get(c) or []):
                print('      ',s,'|',e,file=out)
out.close()
