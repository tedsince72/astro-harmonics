import sys, openpyxl, itertools
ARGS=sys.argv[1:]
sys.path.insert(0,'tools'); sys.path.insert(0,'tools/scans'); sys.argv=sys.argv[:1]
import eddie_bybody as B
from bb_scan_uranus_pairs import dist
from bb_scan_natal_pairs import nums, P, NAT, SKYP
race=ARGS[0]; NC=float(ARGS[1]); SC=float(ARGS[2]); show=len(ARGS)>3
path=f'reference/classic/race_batch_{race}_active.xlsx'
runners,tt,tp=B.load(path); tr=B.ra_positions(openpyxl.load_workbook(path,read_only=True)['TRANS_POS'])
def sc(a,b,pl):
    if a is None or b is None: return None
    v=dist(a,b,pl); h=nums(v,pl); return h[0] if h else None
sky=set()
for a,b in itertools.combinations([x for x in SKYP if x!='Moon'],2):
    if {a,b}=={'Rahu','Ketu'}: continue
    if any((h:=sc(P(tp,tr,a,pl),P(tp,tr,b,pl),pl)) and h[2]>=SC for pl in ('RA','Dec')): sky.add(frozenset((a,b)))
for cl,r in sorted(runners.items()):
    nm=r['name'].get('H'); out=[]
    for ch in ('H','J'):
        pos,ra=r['pos'].get(ch,{}),r.get('ra',{}).get(ch,{}); nat=set()
        for X,Y in itertools.combinations(NAT,2):
            if {X,Y}=={'Rahu','Ketu'}: continue
            if any((h:=sc(P(pos,ra,X,pl),P(pos,ra,Y,pl),pl)) and h[2]>=NC for pl in ('RA','Dec')): nat.add(frozenset((X,Y)))
        bodies=set().union(*nat) if nat else set()
        links=[e for e in sky if e<=bodies and e not in nat]
        # longest alternating-ish path: graph with natal+links edges, count connected component containing >=2 sky links
        g={}
        for e in nat|set(links):
            a,b=tuple(e); g.setdefault(a,set()).add(b); g.setdefault(b,set()).add(a)
        seen=set(); comps=[]
        for s in g:
            if s in seen: continue
            st=[s]; comp=set()
            while st:
                x=st.pop()
                if x in comp: continue
                comp.add(x); st+= list(g[x]-comp)
            seen|=comp; comps.append(comp)
        best=max((sum(1 for e in links if e<=c) for c in comps),default=0)
        out.append(f'{ch}: natal {len(nat)}, sky links {len(links)}, most sky links in one connected group {best}')
        if show: out.append('   links: '+', '.join(sorted('–'.join(sorted(e)) for e in links)))
    print(nm,'|',' | '.join(o for o in out if not o.startswith('   '))); [print(o) for o in out if o.startswith('   ')]
