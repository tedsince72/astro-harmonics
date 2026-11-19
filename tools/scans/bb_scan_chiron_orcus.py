"""Chiron – Orcus and Rahu – Fomalhaut natal pairs >= 90 in either / both charts over every result race (19 Nov 2026, Eddie; read-only)."""
import sys; sys.argv=['x']; sys.path.insert(0,'tools'); sys.path.insert(0,'tools/scans')
import bb_scan_natal_angle as A, eddie_bybody as B, bb_scan_negatives as NG, openpyxl, os
from bb_scan_natal_pairs import nums, P
from bb_scan_uranus_pairs import dist
pairs=[('Chiron','Orcus'),('Rahu','Fomalhaut')]
T={(p,m):[0,0,0.0,[]] for p in pairs for m in ('either','both')}
for rc,win in NG.RACES:
    path=f'reference/classic/race_batch_{rc}_active.xlsx'
    if not os.path.exists(path): continue
    runners,tt,tp=B.load(path); n=len(runners)
    for cl,r in runners.items():
        name=r['name'].get('H'); w=bool(name and win in name)
        for X,Y in pairs:
            ch=set()
            for c in 'HJ':
                if not r['pos'].get(c): continue
                for pl in ('RA','Dec'):
                    a,b=P(r['pos'][c],r['ra'][c],X,pl),P(r['pos'][c],r['ra'][c],Y,pl)
                    if a is None or b is None: continue
                    h=nums(dist(a,b,pl),pl)
                    if h and h[0][2]>=90: ch.add(c)
            for m,ok in (('either',len(ch)>=1),('both',len(ch)==2)):
                if ok: t=T[((X,Y),m)]; t[0]+=1;t[1]+=w;t[2]+=1/n; w and t[3].append(name)
for k,v in T.items(): print(k,v[0],v[1],round(v[2],1),v[3])
