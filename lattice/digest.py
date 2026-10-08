import re,sys
K=sys.argv[1]; WIN=sys.argv[2]  # e.g. '[1]'
files=[('L1',f'T1_{K}.txt'),('Nodes',f'TN_{K}.txt'),('L2',f'TL2_{K}.txt'),('L3',f'TL3_{K}.txt'),('L4',f'TL4_{K}.txt')]
for lay,f in files:
    print(f'===== {lay}'); cur=None
    for l in open(f):
        if l.startswith('['): cur=' '.join(l.split()[:5]); 
        elif 'TRANSIT CHORDS HELD' in l: break
        elif l.strip().startswith('base'): base=re.sub(r'\s+',' ',l.strip())
        elif l.strip().startswith('natal'): nat=re.sub(r'\s+',' ',l.strip())
        elif l.strip().startswith('transit') and cur:
            dn=float(re.search(r'dev ([\d.]+)%',nat).group(1)); dt=float(re.search(r'dev ([\d.]+)%',l).group(1))
            tl=re.sub(r'\s+',' ',l.strip())
            m=re.search(r'exact ([\d.]+) min (before|after)',tl); near = m and float(m.group(1))<=15
            mh=re.search(r'Moon held at [\d:]+ \(([+-][\d.]+)\)',tl); near = near or (mh is not None)
            full='UNISON' in base and 'SAME BODY' in base
            win=cur.startswith(WIN)
            if (win and (max(dn,dt)<=0.02 or (('UNISON' in base or 'SAME BODY' in base) and max(dn,dt)<=0.06) or (near and dn<=0.05))) or (full and near):
                print(f"{cur[:30]} | {base[5:100]}\n      {nat[:95]}\n      {tl[:160]}")
