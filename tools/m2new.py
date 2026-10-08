import re,sys,collections
OLD0, OLD1 = 14*3600+38*60+41, 14*3600+44*60+49
OFF, FIN = 14*3600+40*60+41, 14*3600+44*60+49
def sec(t): h,m,s=map(int,t.split(':')); return h*3600+m*60+s
rows=[]; cnt=collections.Counter(); cntall=collections.Counter()
for L in ('L1','Nodes','L2','L3','L4'):
    chart=None; base=None; nat=None
    for ln in open(f'{L}.txt',encoding='utf-8'):
        m=re.match(r'^\[(\d+)\] (HORSE|JOCKEY)\s+(.+?)\s{2,}',ln)
        if m: chart=(m.group(1),m.group(2),m.group(3)); continue
        if ln.startswith('   base '): base=ln.strip(); continue
        if 'natal ' in ln and 'dev' in ln: nat=ln.strip(); continue
        if 'transit' in ln and 'Moon' in ln and chart:
            t=re.search(r'\((\d+:\d\d:\d\d)\)\s*$',ln) or re.search(r'Moon held at (\d+:\d\d:\d\d)',ln)
            if not t: continue
            s=sec(t.group(1))
            if OLD0<=s<=OLD1: continue
            dn=float(re.search(r'dev ([\d.]+)%',nat).group(1)); dm=float(re.search(r'dev ([\d.]+)%',ln).group(1))
            cntall[chart[2]]+=1
            if max(dn,dm)<=0.02: cnt[chart[2]]+=1
            if chart[0]=='1': rows.append((max(dn,dm),L,s,chart[1],base,nat,ln.strip()))
print("NEW Moon strikes (outside 14:38:41–14:44:49) per chart: all tuned / both sides ≤0.02%")
for k in cntall: print(f"  {k:24s} {cntall[k]:4d} / {cnt[k]:3d}")
def hm(s): return f"{s//3600}:{(s//60)%60:02d}:{s%60:02d}"
def zone(s): return 'before off' if s<OFF else ('IN RACE' if s<=FIN else 'after finish')
print("\nWINNING PAIR — new Moon strikes, tightest first (max of natal / Moon dev)")
for d,L,s,who,b,n,t in sorted(rows):
    if d>0.05: continue
    print(f"[{L} {who} {hm(s)} {zone(s)} {d:.3f}%] {b}\n      {n}\n      {t}")
