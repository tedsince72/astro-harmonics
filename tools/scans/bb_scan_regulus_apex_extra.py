"""Extra checks on bb_scan_regulus_apex at cut 50 (19 Nov 2026, read-only): sky T0 distribution favourite won / lost + permutation p;
natal T1 winner top of the field split favourite / non-favourite winners; races with some holder only. Chosen after the results."""
import sys, random, statistics as st
sys.argv=['x','50']; sys.path[:0]=['tools','tools/scans']
import io, contextlib
import bb_scan_regulus_apex as R
rows=[]
orig=R.main
# rebuild rows by copying main's loop
import os, json, itertools
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
for race, win in NG.RACES:
    p=f'reference/classic/race_batch_{race}_active.xlsx'
    if not os.path.exists(p): continue
    runners, tt, tp = EB.load(p)
    s0,s1=R.apex(tt,'S',EB.BODIES)
    nat={R.key(r['name'].get('H') or ''): sum(R.apex(r['dist'][ch],'N',EB.NATAL_BODIES)[1] for ch in ('H','J') if r['dist'].get(ch)) for r in runners.values()}
    rows.append((race,win,F.FAV.get(race),s0,s1,nat))
fw=[r[3] for r in rows if r[2] and r[2]==r[1]]; fl=[r[3] for r in rows if r[2] and r[2]!=r[1]]
print('S0 dist fav won',sorted(fw)); print('S0 dist fav lost',sorted(fl))
d=st.mean(fl)-st.mean(fw); allv=fw+fl; n=len(fw); c=0
for _ in range(20000):
    random.shuffle(allv); c+= st.mean(allv[n:])-st.mean(allv[:n])>=d
print('perm p (lost mean >= won mean + diff)',c/20000)
# natal T1: winner top, split favourite-winner vs other
for lab,sel in (('fav winners',lambda r:r[2]==r[1]),('non-fav winners',lambda r:r[2]!=r[1])):
    top=e=n=0
    for r in rows:
        if not sel(r): continue
        v=r[5]; w=v.get(R.key(r[1]))
        if w is None: continue
        n+=1; m=max(v.values()); top+=w==m; e+=sum(x==m for x in v.values())/len(v)
    print(lab,n,'top',top,'chance',round(e,1))
# favourites: those top in T1, won?
a=b=0
for r in rows:
    if not r[2]: continue
    v=r[5]; f=v.get(R.key(r[2]))
    if f is None: continue
    if f==max(v.values()): a+=1; b+= r[2]==r[1]
print('favs top T1',a,'won',b)
# today's races natal T1
for r in rows:
    if r[0].startswith('20261119'):
        v=r[5]; print(r[0], r[1], 'winner', v.get(R.key(r[1])), 'max', max(v.values()), sorted(v.items(), key=lambda x:-x[1])[:3])
print('--- races where some runner has >= 1 (T1 natal, cut 50)')
for lab,sel in (('all winners',lambda r:True),('fav winners',lambda r:r[2]==r[1]),('non-fav winners',lambda r:r[2]!=r[1])):
    top=e=n=0; hold=eh=0
    for r in rows:
        if not sel(r): continue
        v=r[5]; w=v.get(R.key(r[1]))
        if w is None or max(v.values())==0: continue
        n+=1; m=max(v.values()); top+=w==m; e+=sum(x==m for x in v.values())/len(v)
        hold+=w>0; eh+=sum(x>0 for x in v.values())/len(v)
    print(lab,n,'top',top,'chance',round(e,1),'| winner holds >=1',hold,'chance',round(eh,1))
