import sys; sys.path.insert(0,sys.argv[1]); import rc
rc.load_file('reference/classic/race_batch_20210825_musselburgh_1345_jupiter_tables.xlsx')
print({r:rc.N[r] for r in rc.RUN})
print(rc.wb.sheetnames[:12])
raw=[rc.trim(r) for r in rc.rows('SKY JUPITER')]
def norm(c):
    if c is None or c=='': return None
    try: return round(float(c),5)
    except: return str(c).strip()
notes=[l.rstrip('\n').split('\t') for l in open(sys.argv[2],encoding='utf-8')]
miss=0;tot=0
for i,n in enumerate(notes,1):
    cells=[norm(c) for c in n]
    if not any(cells): continue
    tot+=1
    # drop leading 'SKY'/'TIMELINE' tag col? try match with and without first col
    found=False
    for start in (0,1):
        want=[c for c in cells[start:] ]
        while want and want[-1] is None: want.pop()
        for r in raw:
            rr=[norm(c) for c in r]
            for off in range(0,3):
                seg=rr[off:off+len(want)]
                if len(seg)==len(want) and all(w is None or w==s for w,s in zip(want,seg)) and sum(w is not None for w in want)>=3:
                    found=True;break
            if found: break
        if found: break
    if not found: miss+=1; print('NO MATCH line',i,n[:6])
print('lines',tot,'unmatched',miss)
