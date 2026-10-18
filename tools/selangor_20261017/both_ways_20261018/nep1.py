import sys; sys.path.insert(0,sys.argv[1]); import rc
RACES=[('sel','1215','P11'),('sel','1245','P01'),('sel','1315','P03'),('sel','1345','P17'),('sel','1415','P05'),('sel','1445','P03'),('sel','1515','P19'),('sel','1615','P09'),
 ('f','reference/classic/race_batch_20210802_newcastle_aw_1633_jupiter_tables.xlsx','P03'),('f','reference/classic/race_batch_20210822_worcester_1300_jupiter_tables.xlsx','P05')]
d=rc.d;p=rc.pos
def sc(v,pl):
    b=rc.fm.best(v,pl,'deg'); return (b['score'],str(b['target'])) if b else (None,None)
for kind,key,win in RACES:
    rc.load(key) if kind=='sel' else rc.load_file(key)
    chs='HJ' if kind=='f' else 'H'
    print(f"\n=== {key.split('/')[-1][:45]} winner {win} {rc.N[win]}  runners {len(rc.RUN)}")
    for r in rc.RUN:
        for ch in chs:
            out=[]
            for pl in ('RA','Dec','Equator'):
                a=d(p(r,'S','Jupiter'),p(r,ch,'Neptune'),pl); b=d(p(r,'S','Neptune'),p(r,ch,'Jupiter'),pl)
                sa=sc(a,pl); sb=sc(b,pl)
                if sa[0] is not None or sb[0] is not None:
                    out.append(f"{pl}: SJ→{ch}Nep {a:.6f} {sa[1]} {sa[0]} | SNep→{ch}Jup {b:.6f} {sb[1]} {sb[0]}")
            both=[o for o in out if o.count('None')==0]
            tag='WIN' if r==win else '   '
            if out: print(f" {tag} {r}{ch} "+' ; '.join(out)+('   <<RECIPROCAL' if both else ''))
