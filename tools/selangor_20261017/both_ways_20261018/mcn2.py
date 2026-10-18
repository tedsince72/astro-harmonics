import sys; sys.path.insert(0,sys.argv[1]); import rc
exec(open(sys.argv[1]+'/nep1.py').read().split('d=rc.d')[0].split('import rc')[1])
d=rc.d;p=rc.pos
ROY=['Aldebaran','Regulus','Antares','Fomalhaut']
def sc(v,pl,k='deg'):
    b=rc.fm.best(v,pl,k); return (round(b['score'],2),str(b['target'])) if b else None
def mid(J,x,y,pl):
    a=d(J,x,pl); b=d(J,y,pl); clos=min(a,b)/max(a,b)*100
    if pl=='Dec': off=J[1]-(x[1]+y[1])/2; tol=0.15
    elif pl=='Equator': off=abs(J[1])-(abs(x[1])+abs(y[1]))/2; tol=0.15
    else:
        m1=((x[0]+y[0])/2)%360; m2=(m1+180)%360
        off=min([((J[0]-m+540)%360)-180 for m in (m1,m2)],key=abs); tol=0.5
    if clos<90 or abs(off)>=tol: return None
    return round((10*(10-(100-clos))/10)**2*0.5+(10*(tol-abs(off))/tol)**2*0.5,2)
def t19(J,x,y,pl):
    if pl=='Equator' and not rc.straddle(J,x,y): return None
    if d(x,y,pl)<(1.5 if pl=='RA' else 0.3): return 'together'
    a=d(J,x,pl);b=d(J,y,pl);q=max(a,b)/min(a,b); s=sc(q,pl,'ratio'); m=mid(J,x,y,pl)
    out=[]
    if s: out.append(f"ratio {q:.6f} → {s[1]} [{s[0]}]")
    if m: out.append(f"midpoint {m}")
    return '; '.join(out) if out else None
W={'1345':[('Makemake','H')],'1515':[('Chiron','H')],'newcastle':[('Chiron','H'),('Chiron','J')],'worcester':[('Neptune','H'),('Neptune','J')]}
for kind,key,win in RACES:
    k=key if kind=='sel' else key.split('_')[3]
    if k not in W: continue
    rc.load(key) if kind=='sel' else rc.load_file(key)
    chs='HJ' if kind=='f' else 'H'
    X=W[k][0][0]
    print(f"\n######## {k} winner {win} {rc.N[win]} — {X}")
    SJ=p(win,'S','Jupiter')
    for R in ROY:
        print(f" --- {X} with {R}")
        for pl in ('RA','Dec','Equator'):
            v=d(p(win,'S',X),p(win,'S',R),pl); s=sc(v,pl)
            if pl=='Equator' and (p(win,'S',X)[1]>=0)==(p(win,'S',R)[1]>=0): eqnote=' (same side: = |Dec| diff)'
            else: eqnote=''
            r19=t19(SJ,p(win,'S',X),p(win,'S',R),pl)
            print(f"   SKY {pl:7s} d(S {X}, S {R}) {v:.6f} {('→ %s [%s]'%(s[1],s[0])) if s else '-'}{eqnote} | S Jup on S {X}–S {R}: {r19 or '-'}")
        for ch in chs:
            for pl in ('RA','Dec','Equator'):
                v=d(p(win,ch,X),p(win,ch,R),pl); s=sc(v,pl)
                r19=t19(SJ,p(win,ch,X),p(win,ch,R),pl)
                # field
                fd=[];f19=[]
                for r in rc.RUN:
                    if r==win: continue
                    for c2 in chs:
                        vv=d(p(r,c2,X),p(r,c2,R),pl); ss=sc(vv,pl)
                        if s and ss and ss[1]==s[1]: fd.append(f"{r}{c2} {ss[0]}")
                        rr=t19(p(r,'S','Jupiter'),p(r,c2,X),p(r,c2,R),pl)
                        if r19 and rr and rr!='together': f19.append(f"{r}{c2} {rr}")
                line=f"   {ch}   {pl:7s} d({ch} {X}, {ch} {R}) {v:.6f} {('→ %s [%s]'%(s[1],s[0])) if s else '-'}"
                if s: line+=f"  field same number: {', '.join(fd) or 'none'}"
                line+=f" | S Jup on {ch} {X}–{ch} {R}: {r19 or '-'}"
                if r19 and r19!='together': line+=f"  field: {', '.join(f19) or 'none'}"
                print(line)
