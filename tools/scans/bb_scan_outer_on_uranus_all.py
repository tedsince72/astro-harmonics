"""Every slow outer sky body on natal Uranus, per body and version: holders / won / by chance / favourites (18 Nov 2026, read-only)."""
import sys; sys.path[:0]=['tools','tools/scans']
import eddie_bybody_rules as E, bb_fieldcheck_outer_uranus as O, bb_favs_outer_uranus as F
print(len(O.RACES), len(F.FAV))
OUT=['Neptune','Sedna','Quaoar','Pluto','Eris','Haumea','Makemake','Gonggong','Orcus','Uranus']
def ls(D,y): return O.lines(D,y) if 'Uranus' in D else []
R=E.load('docs/eddie_read/bybody/20211211_newcastle_aw_1420/20211211_newcastle_aw_1420_bybody.xlsx')
print('== this race: S outer -> natal Uranus (any score)')
for run,D in R.items():
    print(run, '; '.join(f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} {r['fam']} ({r['sc']})" for y in OUT for r in ls(D,y)) or '-')
# across races: per body, per version: holders/won/chance, fav holders/fav count
import collections
vers=[('any',50),('any',80),('whole',50),('whole',80)]
tot={(y,v):[0,0,0.0,0,0] for y in OUT+['SNQ'] for v in vers}
nfav=0
for race,win in O.RACES:
    R=E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx'); N=len(R)
    fav=next((r for r in R if race in F.FAV and F.FAV[race] in r),None); nfav+= fav is not None
    for run,D in R.items():
        for v in vers:
            for y in OUT+['SNQ']:
                ys=['Sedna','Neptune','Quaoar'] if y=='SNQ' else [y]
                h=any(r['sc']>=v[1] and (v[0]=='any' or r['fam']=='whole') for yy in ys for r in ls(D,yy))
                if h:
                    t=tot[(y,v)]; t[0]+=1; t[2]+=1/N; t[1]+= win in run; t[3]+= run==fav
                if run==fav: tot[(y,v)][4]+=0
print('== totals over',len(O.RACES),'races; favourites known',nfav)
for (y,v),(p,w,c,fh,_) in tot.items():
    if p: print(f"{y:9s} {v[0]:5s}>={v[1]}: {p:3d} holders / {w} won / {c:.1f} by chance; favourites holding {fh}")
