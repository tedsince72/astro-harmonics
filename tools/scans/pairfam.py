import sys,glob,itertools,openpyxl
sys.path.insert(0,'/home/claude/astro-harmonics/tools'); import layer1_inventory as L
def run(f,show=None):
    wb=openpyxl.load_workbook(f,data_only=True); S,H,J=L.load(wb,'TRANS'),L.load(wb,'P01'),L.load(wb,'P02')
    cnt={0.00005:0,0.0005:0,0.002:0}; hits=[]
    for c,N in(('H',H),('J',J)):
        for a,b in itertools.combinations(L.BOD,2):
            if L.node_pair(a,b): continue
            for pl,fn in L.PLANES:
                nn=fn(N[a],N[b]); tt=fn(S[a],S[b])
                for lab,tn in ((f'sky {a}–{c} {b}',fn(S[a],N[b])),(f'{c} {a}–sky {b}',fn(N[a],S[b]))):
                    for base,bv in (('NN',nn),('TT',tt)):
                        if min(tn,bv)<0.5: continue
                        r=L.frac(max(tn,bv)/min(tn,bv))
                        if not r: continue
                        for k in cnt:
                            if r[1]<=k: cnt[k]+=1
                        if show and {a,b}==show: hits.append(f"{c} {pl:4s} {lab} {tn:.5f} vs {base} {bv:.5f} -> {r[0]} ({r[1]*100:.4f}%)")
    return wb['P01'].cell(2,1).value, cnt, hits
nm,cnt,hits=run('reference/classic/dettori_ascot_19960928/19960928_ascot_1435__P01.xlsx',{'Sun','Chiron'})
print(nm,{f'{k*100}%':v for k,v in cnt.items()})
for h in hits:
    if float(h.split('(')[-1].rstrip('%)'))<0.3: print('  ',h)
for f in sorted(glob.glob('reference/classic/newmarket_july_1745_20240816/*.xlsx'))[:3]:
    nm,cnt,_=run(f); print(nm,{f'{k*100}%':v for k,v in cnt.items()})
