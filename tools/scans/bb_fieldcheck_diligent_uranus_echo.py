import sys,re; sys.path.insert(0,'tools')
import eddie_bybody_rules as E
exec(open('tools/scans/bb_fieldcheck_sky_line_royal_ends.py').read().split("def test(")[0])
def N(t):
    m=re.match(r'(\d+) ',t or ''); return int(m.group(1)) if m else None
def cases(b,kind):
    out=[]
    for c,R,r in b.star_rows():
        for typ,rt,base in (('sb',r['rt'],r['sbv']),('x',r['xt'],r['xbv'])):
            n=N(rt)
            if not n or n<2: continue
            if kind=='E3' and typ!='x': continue
            planes=[r['plane']] if kind=='E3' else ['RA','Dec']
            for p in planes:
                for s in b.same_body(c,p):
                    if s['fam']=='whole' and int(s['tgt'])==n:
                        if kind=='E2' and not (r['fam'] and r['fam'] not in CJ): continue
                        if kind=='E4' and not b.same_on(s): continue
                        out.append((r,typ,n,s))
    return out
for kind,desc in [('E1','royal row ratio (same-body or crossed) on whole N >= 2, and S X -> c X (same chart, any plane) on whole N'),
                  ('E2','E1 + the royal line itself scores'),
                  ('E3','crossed ratio on N, and the same-body line in the royal row plane on whole N'),
                  ('E4','E1 + a sky line on the same target carries the same-body line')]:
    print('==',kind,desc)
    for n,_ in races:
        h=[(run,X) for run,D in data[n].items() for X,d in D.items() if cases(E.Body(X,d),kind)]
        rn=sorted({r for r,_ in h}); w=W.get(n)
        lab=', '.join(f"{r.split(' ',1)[1]} {X}" for r,X in h) if len(h)<=10 else f'{len(h)} bodies'
        print(f"  {n}: {len(rn)}/{len(data[n])} runners" + (f"; winner {'YES' if any(w in r for r in rn) else 'no'}" if w else '') + f" | {lab}")
D=data['York16'][[k for k in data['York16'] if 'Diligent' in k][0]]
for kind in ('E1','E3','E4'):
    for r,typ,n,s in cases(E.Body('Uranus',D['Uranus']),kind): print(kind,'Diligent Uranus:',r['line'],r['plane'],typ,n,'|',E.cell(s))
print('---')
for n,who,X in [('York16','Misemerald','Uranus'),('York16','Ribble Radiant','Neptune'),('Haydock','Birkenhead','Orcus'),('Beverley','Maw Lam','Neptune'),('Beverley','Invincible Annice','Gonggong'),('Beverley','Mademoiselle','Chiron')]:
    D=data[n][[k for k in data[n] if who in k][0]]; b=E.Body(X,D[X])
    for r,typ,nn,s in cases(b,'E1'):
        print(n,who,X,'|',E.cell(r),r['plane'],typ,(r['r'] if typ=='sb' else r['xr']),nn,'|',E.cell(s),'| carried by', [E.cell(t) for t in b.same_on(s)][:2])
