import re,collections,sys
exec(open('/home/claude/lattice/families.py').read().split("N = sorted(S)")[0].split("S = {}")[0]); ST=set(STARS)
txt=open(sys.argv[1]).read()+open(sys.argv[2]).read()
sec=None; D=collections.defaultdict(list)
for L in txt.splitlines():
    m=re.match(r"== (TT|NN|TN)(?: sky →)? ?(.*?)(?: natal.*)?: \d+",L)
    if m: sec=(m.group(1),m.group(2).strip()); continue
    m=re.match(r"\s+([\d.]+)\s+(RA|Dec)\s+(.+?)–(\S+(?: \S+)?)\s+=\s+(\d+)\s+([\d.]+)",L)
    if m and sec: D[sec].append((float(m.group(1)),m.group(2),m.group(3).strip(),m.group(4).strip(),int(m.group(5))))
names=sorted({k[1] for k in D if k[0]!='TT'},key=lambda n:n[:2])
print(f"{'chart':22s} {'TN new':>6s} {'9-mult':>6s} | Neptune hits (NN+TN new) | natal on Equator | body ladder (natal pt: TN Dec hits, + Equator) | double RA+Dec same sky→natal pair | 144")
for n in names:
    nn=D[('NN',n)]; tn=D[('TN',n)]
    new=[x for x in tn if x[2] not in ST and x[3] not in ST]
    m9=[x for x in new+[y for y in nn if not (y[2] in ST or y[3] in ST)] if x[4]%9==0]
    nep=[f"{x[1]} {x[2]}-{x[3]} {x[4]}" for x in nn+new if 'Neptune' in (x[2],x[3])]
    eq=[f"{x[2]} {x[4]}" for x in nn if x[3]=='Equator' and x[2] not in ST]
    lad=collections.defaultdict(list)
    for x in new:
        if x[1]=='Dec': lad[x[3]].append(f"{x[2]} {x[4]}")
    ladtxt='; '.join(f"{k}: {', '.join(v)}{' +Eq' if any(e.startswith(k+' ') for e in eq) else ''}" for k,v in lad.items() if len(v)>=2 or any(e.startswith(k+' ') for e in eq))
    pr=collections.defaultdict(set)
    for x in new: pr[(x[2],x[3])].add((x[1],x[4]))
    dbl=[f"{a}→{b} {sorted(v)}" for (a,b),v in pr.items() if {m for m,_ in v}=={'RA','Dec'}]
    s144=[f"{x[1]} {x[2]}-{x[3]}" for x in nn+tn if x[4]==144]
    print(f"{n:22s} {len(new):6d} {len(m9):6d} | {'; '.join(nep) or '-'} | {', '.join(eq) or '-'} | {ladtxt or '-'} | {'; '.join(dbl) or '-'} | {'; '.join(s144) or '-'}")
