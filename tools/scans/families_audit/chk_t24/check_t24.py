import sys, math
for p in ['tools','tools/jup2','rebuild_kit']: sys.path.insert(0,'/Users/eddieplace/astro-harmonics/'+p)
import families as F, openpyxl
from collections import Counter
WB='../ascot_gc/race_batch_20120619_ascot_1430_jupiter_tables.xlsx'
wb=openpyxl.load_workbook(WB)
STARS=['Algol','Pleiades','Aldebaran','Capella','Sirius','Procyon','Regulus','Alkaid','Algorab','Spica','Arcturus','Alphecca','Antares','Vega','Deneb Algedi','Fomalhaut','Rigel','Betelgeuse','Polaris','Castor','Altair','Bellatrix','Galactic Centre']
BODIES=['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto','Rahu','Ketu']
pos={}
ws=wb['POSITIONS']
for r in range(5,ws.max_row+1):
    v=[c.value for c in ws[r]]
    if v[2] in ('S','H','J') and v[3]: pos[(v[2],v[3])]=(v[4],v[5],v[6])
FILL={'green':'00C6EFCE','yellow':'00FFEB9C','light':'00FFF8DC','':'00000000'}
def fmt(x): return f'{x:+.5f}'
# own scoring sample: squared / linear
def expected(v,plane):
    ev=F.evaluate(v,plane,'deg')
    if ev:
        b=ev[0]; col=F.colour(b['score'])
        if b['family']=='conj':
            txt=f"0 · conjunction ({plane} < {F.CONJ[plane]}) · {fmt(v)} · {b['score']:.2f}"
        else:
            txt=f"{b['target']} · {b['family']} · {fmt(b['off'])} · {b['score']:.2f}"
        return col,txt,b
    o=F.outside(v,plane,'deg')
    return '',f"nearest: {o['target']} · {o['family']} — outside ±{o['tol']:.3g} · {fmt(o['off'])}",None
mism=[]; report={}
indep=[0,0]
def check(sheet,chart,title):
    ws=wb[sheet]
    r0=next(r for r in range(1,ws.max_row+1) if ws.cell(r,1).value=='T24' and str(ws.cell(r,2).value or '').startswith(title))
    bodies=[b for b in BODIES if (chart,b) in pos and (chart=='S' or b!='Moon')]
    stars=[s for s in STARS if (chart,s) in pos]
    h1=[ws.cell(r0+1,c).value for c in range(1,3+2*len(bodies)+2)]
    exp_h1=['table','star']+sum([[b,None] for b in bodies],[])+[None]
    if h1!=exp_h1: mism.append((sheet,title,'header1',exp_h1,h1))
    merged={str(m) for m in ws.merged_cells.ranges}
    for i,b in enumerate(bodies):
        c=3+2*i; L=openpyxl.utils.get_column_letter
        if f'{L(c)}{r0+1}:{L(c+1)}{r0+1}' not in merged: mism.append((sheet,'merge',b))
        if [ws.cell(r0+2,c).value,ws.cell(r0+2,c+1).value]!=['RA','Dec']: mism.append((sheet,'h2',b))
    cnt=Counter(); n=0
    for j,s in enumerate(stars):
        r=r0+3+j
        if ws.cell(r,1).value!='T24' or ws.cell(r,2).value!=f'{chart} {s}': mism.append((sheet,r,'rowlabel',f'{chart} {s}',ws.cell(r,2).value))
        sa=pos[(chart,s)]
        for i,b in enumerate(bodies):
            ba=pos[(chart,b)]
            ra=abs(sa[1]-ba[1])%360; ra=360-ra if ra>180 else ra
            for k,(plane,v) in enumerate((('RA',ra),('Dec',abs(sa[2]-ba[2])))):
                cell=ws.cell(r,3+2*i+k); n+=1
                col,txt,b_=expected(v,plane)
                # independent score check
                if b_:
                    tol={'whole':0.02,'golden':0.03236,'conj':F.CONJ[plane]}.get(b_['family'])
                    if tol:
                        dev=abs(v-b_['tv']) if b_['family']!='conj' else v
                        mine=(10*(tol-dev)/tol)**2; indep[0]+=1
                        if abs(mine-b_['score'])>1e-6: indep[1]+=1
                got=cell.value
                if got is None or abs(got-round(v,6))>1e-9: mism.append((sheet,cell.coordinate,'value',round(v,6),got))
                gf=cell.fill.fgColor.rgb if cell.fill and cell.fill.fill_type else '00000000'
                if gf!=FILL[col]: mism.append((sheet,cell.coordinate,'fill',FILL[col],gf))
                gc=cell.comment.text if cell.comment else None
                if gc!=txt: mism.append((sheet,cell.coordinate,'comment',txt,gc))
                cnt[col or 'none']+=1
                if b_ and b_['family']=='conj': cnt['conj']+=1
    rend=r0+3+len(stars)
    if any(ws.cell(rend,c).value is not None for c in range(1,60)): mism.append((sheet,rend,'not blank after'))
    # extra columns beyond grid
    if ws.cell(r0+3,3+2*len(bodies)).value is not None: mism.append((sheet,'extra col'))
    report[title]=(len(stars),2*len(bodies),n,'Galactic Centre' in stars,dict(cnt))
check('SKY JUPITER','S','T24 SKY'); check('P01','H','T24 HORSE'); check('P01','J','T24 JOCKEY')
for k,v in report.items(): print(k,v)
print('indep score checks',indep)
print('mismatches',len(mism)); [print(m) for m in mism[:15]]
for c in 'SHJ': print(c,pos[(c,'Galactic Centre')], 'Ketu' , (c,'Ketu') in pos, 'Moon',(c,'Moon') in pos)
