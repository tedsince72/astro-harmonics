import sys,re; sys.path.insert(0,sys.argv[1])
exec(open(sys.argv[1]+'/mj1.py').read().split("bad=0")[0])
MAP={'T1':[(2,4,7,'natal RA'),(10,12,15,'natal Dec'),(18,20,23,'SKY RA'),(27,29,32,'SKY Dec')]}
MAP['T2']=MAP['T1']
for t in ['T3','T4','T5','T7','T8','T12','T13']: MAP[t]=[(2,4,7,'RA'),(10,12,15,'Dec')]
out=[]
for rec in recs:
    m=match(rec)
    if not m or m=='tl': continue
    i,r=m; r=list(r)+[None]*70; tab=r[0]
    hits=[]
    if tab in MAP:
        for v,tg,s,lab in MAP[tab]:
            if isinstance(r[s],(int,float)): hits.append(f"{lab} {r[v]} → {r[tg]} [{r[s]}]")
        key=r[1]
    elif tab=='T19':
        key=f"{r[2]} {r[3]}"
        if isinstance(r[13],(int,float)): hits.append(f"ratio {r[10]} {str(r[11]).split(' ·')[0]} [{r[13]}] {r[14]}")
        if isinstance(r[21],(int,float)): hits.append(f"mid {r[21]}")
    elif tab in ('T21','T21R'):
        key=f"{r[1]} {r[2]}"
        for lab,(q,iv,s,mt) in {'H':(9,10,12,20),'J':(27,28,30,38),'S':(45,46,48,56)}.items():
            if isinstance(r[s],(int,float)): hits.append(f"{lab} {r[q]} {str(r[iv]).split(' ·')[0]} [{r[s]}]")
            if isinstance(r[mt],(int,float)): hits.append(f"{lab} mid {r[mt]}")
    elif tab=='T22':
        key=f"{r[1]} {r[2]}"
        for lab,(q,iv,s,mt) in {'H':(7,8,10,17),'J':(22,23,25,32)}.items():
            if isinstance(r[s],(int,float)): hits.append(f"{lab} {r[q]} {str(r[iv]).split(' ·')[0]} [{r[s]}]")
            if isinstance(r[mt],(int,float)): hits.append(f"{lab} mid {r[mt]}")
        for lab,(dv,fm_) in {'H leg':(5,6),'J leg':(20,21)}.items():
            if r[fm_] and 'no family' not in str(r[fm_]): hits.append(f"{lab} {r[dv]} {str(r[fm_])[:40]}")
    else:
        key=str(r[1:4]); hits.append(str(trim(r)[1:24]))
    out.append((tab,key,i,hits))
for tab,key,i,h in out:
    if h: print(f"{tab:4s} r{i} {key[:44]:44s} | "+' ; '.join(h))
print('rows without any hit:',sum(1 for o in out if not o[3]),'of',len(out))
