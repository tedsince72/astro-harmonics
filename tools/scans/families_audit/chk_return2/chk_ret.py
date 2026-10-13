import sys, re, math
sys.argv=['x','P09']
exec(open('/private/tmp/claude-501/-Users-eddieplace-astro-harmonics/0a4b9192-0277-48b6-a3a8-817a486af8bb/scratchpad/chk_ret2/base.py').read())
RUNNERS=['P01','P03','P05','P07','P09','P11']; N=len(RUNNERS)
GREY='D9D9D9'
BODIES=['Sun','Mercury','Venus','Mars','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu',
        'Eris','Sedna','Haumea','Makemake','Orcus','Quaoar','Gonggong','Transpluto']
ROYAL=['Aldebaran','Regulus','Antares','Fomalhaut']

def set_runner(h):
    j='P%02d'%(int(h[1:])+1)
    POS['H']=load(h); POS['J']=load(j)
    for k in ('H','J'):
        ra,dec=POS[k]['Rahu']; POS[k]['KetuMirror']=((ra+180)%360,-dec)

def strip_inv(l): return re.sub(r'\s*\(inverted\)$','',l)

# ---------- pass 1: per runner, read sheet rows T12-T15, compute values, unisons, returns ----------
AUTO={}
def autoinfo(table,lab,plane):
    """d1 = d(S Jupiter, C Jupiter), d2 = d(C Jupiter, X) in plane; current runner must be set."""
    l=strip_inv(lab)
    if table in ('T12','T13'):
        n,d=l.split(' / '); d1n,d2n=d.split('–'); c=d1n.strip()[0]; x=d2n.strip()[2:].strip()
        assert d1n.strip()==c+' Jupiter' and d2n.strip()[0]==c, l
        a=planes(pt('S','Jupiter'),pt(c,'Jupiter')); b=planes(pt(c,'Jupiter'),pt(c,x))
        if plane not in a or plane not in b or b[plane]==0: return None
        return (a[plane]/b[plane]<0.0015, a[plane], b[plane])
    if table=='T14':
        m=re.match(r'\|Dec\| S Jupiter / \|Dec\| ([HJ]) Jupiter$',l)
        if not m: return None
        c=m.group(1); d1=abs(pt('S','Jupiter')[1]-pt(c,'Jupiter')[1]); d2=abs(pt(c,'Jupiter')[1])
        return (d1/d2<0.0015, d1, d2)
    return None
RET={}; ROWS={}; UNI={}; LABELS={}
for h in RUNNERS:
    set_runner(h)
    ws=wo[h]
    # return condition
    sj=pt('S','Jupiter')
    for ch in 'HJ':
        if 'Jupiter' not in POS[ch]: RET[(h,ch)]=None; continue
        q=pt(ch,'Jupiter'); rd=ra_sep(sj[0],q[0]); dd=abs(sj[1]-q[1])
        RET[(h,ch)]=(rd<1.5 or dd<0.3, rd, dd)
    rows=[]; PC={}; labs={}
    for r in range(1,ws.max_row+1):
        a=ws.cell(r,1).value
        if a=='table':
            PC={ws.cell(r,3+9*i).value:3+9*i for i in range(4) if ws.cell(r,3+9*i).value}; continue
        if not (isinstance(a,str) and a in ('T12','T13','T14','T15')): continue
        lab=ws.cell(r,2).value
        if lab is None: continue
        if all(ws.cell(r,c).value is None for c in range(3,40)):
            rows.append(('blank',r,a,lab)); continue
        labs.setdefault(a,[]).append(lab)
        mode,vals=compute(a,lab); _,vals5=compute(a,lab,True)
        for pl in vals:
            x=vals[pl]
            if mode=='ratio1': v,inv,labinv=x; v5=vals5[pl][0]
            else: v,inv=x; v5=vals5[pl][0]; labinv=None
            uni = abs(v/1-1)*100<0.15 and (10*(0.15-abs(v-1)*100)/0.15)**2>0
            k=(a,strip_inv(lab),pl)
            ai=autoinfo(a,lab,pl) if uni else None
            if uni: AUTO[(h,a,strip_inv(lab),pl)]=ai
            if uni and not (ai and ai[0]): UNI.setdefault(k,set()).add(h)
            rows.append(('cell',r,a,lab,pl,PC.get(pl),mode,v,inv,labinv,v5))
    ROWS[h]=rows; LABELS[h]=labs

print('Jupiter return condition (S Jupiter vs natal Jupiter, RA<1.5 or Dec<0.3):')
for (h,ch),x in sorted(RET.items()):
    print('  ',h,ch, None if x is None else (x[0],round(x[1],5),round(x[2],5)))
print('unison keys (table,label,plane) -> runners:')
for k,s in sorted(UNI.items()): print('  ',k,sorted(s))

# ---------- label completeness ----------
lm=[]
for h in RUNNERS:
    L=LABELS[h]
    e12=['S Jupiter–S %s / %s Jupiter–%s %s'%(x,c,c,x) for c in 'HJ' for x in BODIES]
    e13=['S Jupiter–%s %s / %s Jupiter–%s %s'%(c,x,c,c,x) for c in 'HJ' for x in BODIES]
    if sorted(L.get('T12',[]))!=sorted(e12): lm.append((h,'T12',set(L.get('T12',[]))^set(e12)))
    if sorted(L.get('T13',[]))!=sorted(e13): lm.append((h,'T13',set(L.get('T13',[]))^set(e13)))
    t14=[strip_inv(x) for x in L.get('T14',[])]
    e14=['|Dec| S Jupiter / |Dec| H Jupiter','|Dec| S Jupiter / |Dec| J Jupiter','|Dec| H Jupiter / |Dec| J Jupiter']
    if sorted(t14)!=sorted(e14): lm.append((h,'T14',t14))
    t15=[strip_inv(x) for x in L.get('T15',[])]
    e15=[]
    for c in 'SHJ':
        xs=BODIES+(['Moon'] if c=='S' else [])+ROYAL
        e15+=['(%s Jupiter–%s %s) / (%s Jupiter–equator)'%(c,c,x,c) for x in xs]
        e15+=['(%s Jupiter–%s %s) / (%s Jupiter–%s %s)'%(c,c,ROYAL[i],c,c,ROYAL[j]) for i in range(4) for j in range(i+1,4)]
    if sorted(t15)!=sorted(e15): lm.append((h,'T15',set(t15)^set(e15)))
print('label completeness mismatches',lm)

# ---------- pass 2: cell checks, all runners ----------
def autoflag(h,table,lab,plane):
    ai=AUTO.get((h,table,strip_inv(lab),plane)); return bool(ai and ai[0])
ALLM={}; CELLS={}; HITS={}; RETLINES={}
for h in RUNNERS:
    set_runner(h); ws=wo[h]; mism=[]; cells=0; hits=[]
    # return lines
    rl=[]
    for r in range(1,ws.max_row+1):
        if ws.cell(r,1).value=='T13' and isinstance(ws.cell(r,2).value,str) and ws.cell(r,2).value.startswith('Jupiter return'):
            rl.append((r,ws.cell(r,2).value,[ws.cell(r,c).value for c in range(3,40) if ws.cell(r,c).value is not None]))
    for r in range(1,ws.max_row+1):
        v=ws.cell(r,2).value
        if isinstance(v,str) and 'return' in v.lower() and ws.cell(r,1).value!='T13': mism.append(('return text outside T13',r,v))
    exp_rl=[]
    for ch in 'HJ':
        x=RET[(h,ch)]
        if x and x[0]: exp_rl.append((ch,'Jupiter return: S–%s Jupiter RA %.5f Dec %.5f; a unison is automatic (grey) only where d(S Jupiter, %s Jupiter) / d(%s Jupiter, X) < 0.0015 in that plane'%(ch,x[1],x[2],ch,ch)))
    RETLINES[h]=(rl,exp_rl)
    if [x[1] for x in rl]!=[e[1] for e in exp_rl]: mism.append(('return lines',[x[1] for x in rl],[e[1] for e in exp_rl]))
    for x in rl:
        if x[2]: mism.append(('return line has extra cells',x))
    # position of return line: first line of that chart's T13 part
    for (r,txt,_) in rl:
        ch=txt.split('S–')[1][0]
        nxt=ws.cell(r+1,2).value
        if not (isinstance(nxt,str) and nxt.startswith('S Jupiter–%s Sun / %s Jupiter'%(ch,ch))): mism.append(('return line not directly before chart part',r,nxt))
        prv=ws.cell(r-1,2).value
        if isinstance(prv,str) and prv.startswith('S Jupiter–%s '%ch): mism.append(('return line not at start of part',r,prv))
    for row in ROWS[h]:
        if row[0]=='blank': continue
        _,r,table,label,plane,c0,mode,v,inv,labinv,v5=row
        C=lambda k: ws.cell(r,c0+k)
        sv,v5s,tgt,grp,off,sc,arr,also,scaled=[C(k).value for k in range(9)]
        col=fill(C(0)); scol=fill(C(8)); cells+=9
        def M(what,sheet,mine): mism.append((r,table,label[:70],plane,what,sheet,mine))
        if sv is None or abs(sv-v)>2e-6: M('value',sv,round(v,6))
        if has_S(label):
            if v5s is None or abs(v5s-v5)>2e-5: M('+5',v5s,round(v5,6))
        elif v5s is not None: M('+5 on natal row',v5s,None)
        if mode=='ratio1':
            if labinv!=inv: M('row (inverted) flag',labinv,inv)
            inv=False
        e=expected(v,'ratio',plane,inv)
        if e['ties']: M('TIE (note)',None,[x[:2] for x in e['ties']])
        if tgt!=e['target']: M('target',tgt,e['target'])
        if grp!=e['group']: M('group',grp,e['group'])
        uni=bool(e['best']) and e['best'][1]=='1'
        k=(table,strip_inv(label),plane)
        auto=uni and autoflag(h,table,label,plane)
        if e['target']:
            if off!=e['offset']: M('offset',off,e['offset'])
            if sc is None or abs(sc-e['score'])>0.011: M('score',sc,e['score'])
            b=e['best']
            if v5s is not None:
                d0,d1=abs(sv/b[4]-1),abs(v5s/b[4]-1)
                ea='-> toward' if d1<d0 else '<- away' if d1>d0 else '?='
                if arr!=ea: M('arrow',arr,ea)
            elif arr is not None: M('arrow w/o +5',arr,None)
            hits.append(dict(group=b[5],table=table,label=label,plane=plane,v=v,v5=v5s,iv=b[1],off=e['offset'],score=b[3],inv=inv,arr=arr,uni=uni,auto=auto,k=k))
        elif any(x is not None for x in (off,sc,arr)): M('offset/score/arrow present',(off,sc,arr),None)
        ecol=GREY if auto else e['colour']
        if col!=ecol: M('colour',col,ecol)
        ea=list(e['also'])
        if uni:
            ea.append('unison: automatic (Jupiter return), not counted' if auto else 'unison: field %d/%d'%(len(UNI.get(k,())),N))
        sh=[x.strip() for x in re.split(r';\s*|,\s(?=[^\]]*\[)',also)] if also else []
        sh=[x for x in sh if x]
        if sorted(sh)!=sorted(ea): M('also',also,ea)
        if scaled!=e['scaled']: M('scaled',scaled,e['scaled'])
        if scol!=e['scaled_colour']: M('scaled colour',scol,e['scaled_colour'])
    ALLM[h]=mism; CELLS[h]=cells; HITS[h]=hits

for h in RUNNERS:
    print(h,'T12-T15 cells compared',CELLS[h],'mismatches',len(ALLM[h]),'return lines',RETLINES[h][0] and [x[1] for x in RETLINES[h][0]])
    for m in ALLM[h][:40]: print('   ',m)

# ---------- RATIOS sheets ----------
for h in RUNNERS:
    wr=wo[h+' RATIOS']; got=[]; hdr=None; secs=[]
    for r in range(1,wr.max_row+1):
        row=[wr.cell(r,c).value for c in range(1,14)]
        if row[0] in GROUPS and row[1] is None: secs.append(row[0]); continue
        if row[0]=='group': hdr=row; continue
        if r==1 or row[0] is None: continue
        got.append((r,row,fill(wr.cell(r,5)),[c for c in range(1,13) if c!=5 and fill(wr.cell(r,c)) not in (None,'D9E1F2')]))
    exp=[]
    for g in GROUPS: exp+=sorted([x for x in HITS[h] if x['group']==g],key=lambda x:-x['score'])
    rm=[]; rc=0
    if hdr and hdr[11]!='unison field': rm.append(('header col12',hdr[11]))
    if any(x is not None for x in (hdr or [None]*13)[12:]): rm.append(('header extra cols',hdr[12:]))
    if len(got)!=len(exp): rm.append(('row count',len(got),len(exp)))
    expsecs=[g for g in GROUPS if any(x['group']==g for x in exp)]
    for i,(r,row,c5,extra) in enumerate(got[:len(exp)]):
        x=exp[i]; rc+=12
        elab=strip_inv(x['label'])+(' (inverted)' if (x['inv'] or x['label'].endswith('(inverted)')) else '')
        ev=[x['group'],x['table'],elab,x['plane'],None,None,x['iv'],NAMES.get(x['iv']),x['off'],None,x['arr'],
            ('automatic (Jupiter return), not counted' if x['auto'] else '%d/%d'%(len(UNI.get(x['k'],())),N)) if x['uni'] else None]
        for j in (0,1,2,3,6,7,8,10,11):
            if row[j]!=ev[j]: rm.append((r,'col%d'%(j+1),row[j],ev[j]))
        if abs(row[4]-x['v'])>2e-6: rm.append((r,'value',row[4],x['v']))
        if row[5]!=x['v5']: rm.append((r,'+5',row[5],x['v5']))
        if abs(row[9]-round(x['score'],2))>0.011: rm.append((r,'score',row[9],x['score']))
        ec=GREY if x['auto'] else colour(x['score'])
        if c5!=ec: rm.append((r,'colour',c5,ec))
        if extra: rm.append((r,'extra fills',extra))
        if row[12] is not None: rm.append((r,'col13',row[12]))
    print(h,'RATIOS rows',len(got),'expected',len(exp),'cells',rc,'sections',secs,'(expected',expsecs,') mismatches',len(rm)+(secs!=expsecs))
    for m in rm[:30]: print('   ',m)

# ---------- FIELD 12-15, all runner columns ----------
CELLV={}
for h in RUNNERS:
    for row in ROWS[h]:
        if row[0]=='cell': CELLV[(h,row[2],strip_inv(row[3]),row[4])]=row
fm=[]; fc=0; frows={}
for t in (12,13,14,15):
    wf=wo['FIELD %d'%t]; plane=None; cols={}
    seen=set()
    for r in range(1,wf.max_row+1):
        a=wf.cell(r,1).value
        if a in ('RA','Dec','Flat','GC','Equator') and isinstance(wf.cell(r,2).value,str) and wf.cell(r,2).value.startswith('P01'):
            plane=a; cols={wf.cell(r,c).value[:3]:c for c in range(2,wf.max_column+1) if isinstance(wf.cell(r,c).value,str) and re.match(r'^P\d\d ',wf.cell(r,c).value)}
            if sorted(cols)!=RUNNERS: fm.append((t,r,'runner columns',sorted(cols)))
            continue
        if plane is None or not a: continue
        for h,c in cols.items():
            sv=wf.cell(r,c).value; st=wf.cell(r,c+1).value; col=fill(wf.cell(r,c)); fc+=3
            key=(h,'T%d'%t,strip_inv(a),plane); seen.add(key)
            if key not in CELLV:
                if sv is not None or st is not None: fm.append((t,r,h,a,plane,'present but no runner cell',sv,st))
                continue
            set_runner(h)
            mode,vals=compute('T%d'%t,a); x=vals[plane]; v=x[0]
            if sv is None or abs(sv-v)>2e-6: fm.append((t,r,h,a,plane,'value',sv,v)); continue
            e=expected(v,'ratio',plane,False); b=e['best']
            if b is None: es=None
            else:
                es='%s %s [%.1f] [%s]'%(b[1],offs(b),b[3],b[5])
                if b[1]=='1':
                    auto=autoflag(h,'T%d'%t,a,plane)
                    es+=(' automatic (Jupiter return), not counted' if auto else ' field %d/%d'%(len(UNI.get(('T%d'%t,strip_inv(a),plane),())),N))
            if st!=es: fm.append((t,r,h,a,plane,'string',st,es))
            ec=e['colour']
            if b is not None and b[1]=='1' and autoflag(h,'T%d'%t,a,plane): ec=GREY
            if (col not in ec) if isinstance(ec,tuple) else (col!=ec): fm.append((t,r,h,a,plane,'colour',col,ec))
            if isinstance(ec,tuple): frows.setdefault('auto colour used',set()).add(col)
    missing=[k for k in CELLV if k[1]=='T%d'%t and k not in seen]
    if missing: fm.append((t,'cells on runner sheets missing from FIELD',len(missing),missing[:5]))
print('FIELD 12-15 cells compared',fc,'mismatches',len(fm),'FIELD colour of automatic unison cells:',frows)
for m in fm[:40]: print('   ',m)
print('interval names:',NAMES)
print('ALL unisons (h,table,label,plane) -> (auto,d1,d2,d1/d2):')
for k,ai in sorted(AUTO.items()):
    print('  ',k, None if ai is None else (ai[0],round(ai[1],6),round(ai[2],6),'%.6g'%(ai[1]/ai[2])))
print('unisons with no autoinfo (T14 H/J, T15):',[k for k,v in AUTO.items() if v is None])

