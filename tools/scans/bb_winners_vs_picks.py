import json,sys; sys.path.insert(0,'tools'); import eddie_bybody_rules as E
races=[('Lingfield','20210402_lingfield_aw_1435','Pholas'),('Haydock','20200608_haydock_1345','Ishvara'),('Beverley','20240608_beverley_1405','Perfect Part'),('York','20240515_york_1545','Secret Satire')]
ids=[r for r,_,_ in E.RULES]
rows=[]; tot={}
for n,r,w in races:
    D=E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N=len(D)
    J=json.load(open(f'docs/eddie_read/bybody_rules/{r}_bbrules.json'))['rules']
    for i in ids:
        h={x['runner'] for x in J.get(i,[])}
        tot.setdefault(i,[]).append((n,len(h),N,any(w in x for x in h)))
print('fields',[(n,len(E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'))) for n,r,_ in races])
out=['| Rule | Body | Lingfield | Haydock | Beverley | York | Races with picks | Winners picked | Picks | By chance |','|---|---|---|---|---|---|---|---|---|---|']
body=dict((r,b) for r,_,b in E.RULES)
for i in ids:
    t=tot[i]; cells=[]
    for n,h,N,wn in t: cells.append('–' if h==0 else f"{h}/{N}{' **W**' if wn else ''}")
    pk=sum(h for _,h,_,_ in t); wins=sum(wn for *_,wn in t); ch=sum(h/N for _,h,N,_ in t); rc=sum(h>0 for _,h,_,_ in t)
    out.append(f"| {i} | {body[i]} | "+' | '.join(cells)+f" | {rc} | {wins} | {pk} | {ch:.1f} |")
open('docs/eddie_read/bybody_rules/winners_vs_picks.md','w').write('\n'.join(out)+'\n'); print('\n'.join(out))
order=['Lingfield','Haydock','Beverley','York']
def grp(i):
    k=int(''.join(ch for ch in i[2:] if ch.isdigit()))
    return 0 if k<=17 else 1 if k<=31 else 2 if k<=40 else 3
for label,rng in [('BB1-BB17 (from Lingfield)',0),('BB18-BB31 (from Haydock)',1),('BB32-BB40 (from Beverley)',2)]:
    P=W=C=0; per={}
    for i in ids:
        if grp(i)!=rng or i=='BB34': continue
        for n,h,N,wn in tot[i]:
            if order.index(n)>rng: P+=h;W+=wn;C+=h/N; per.setdefault(n,[0,0,0]); per[n][0]+=h;per[n][1]+=wn;per[n][2]+=h/N
    print(label,'later races: picks',P,'winners',W,'chance %.1f'%C, {k:(a,b,round(c,1)) for k,(a,b,c) in per.items()})
