import sys; sys.path.insert(0,sys.argv[1]); import rc
exec(open(sys.argv[1]+'/nep1.py').read().split('d=rc.d')[0].split('import rc')[1])
for kind,key,win in RACES:
    rc.load(key) if kind=='sel' else rc.load_file(key)
    k=key if kind=='sel' else key.split('_')[3]
    ws=rc.rows('SKY JUPITER'); blk=None; out=[]
    for row in ws:
        t=rc.trim(row)
        if not t: continue
        if isinstance(t[0],str) and t[0].isupper() and len(t)==1: blk=t[0][:40]
        if isinstance(t[0],str) and ('SKY ROYAL' in t[0] or 'SKY PAIRS' in t[0] or t[0].startswith('TIMELINE') or t[0].startswith('LONG')): blk=t[0][:30]
        s=' | '.join(str(c) for c in t)
        if 'Neptune' in s and any(R in s for R in ('Aldebaran','Regulus','Antares','Fomalhaut')) and blk and ('ROYAL' in blk):
            out.append(s[:260])
    print(f"== {k}"); [print('  ',o) for o in out[:12]]
