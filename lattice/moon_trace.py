"""moon_trace.py RACE OFF DUR_S - the Moon's star chords every 5 s, off-30 to off+30: in / exact / out, count at each minute."""
import sys
src=open('/home/claude/lattice/race_read.py').read().split("BODIES = [")[0]
exec(src)
ts=np.arange(t0-30,t0+30+1e-9,5/60); prev=None; life={}; cnt=[]
for t in ts:
    ch=chords_of(pos('Moon',t),S); cur={(mm,a,b):(typ,dv,d) for mm,a,b,d,typ,dv in ch}; cnt.append((t,len(cur)))
    for k,(typ,dv,d) in cur.items():
        L=life.setdefault(k,{'typ':typ,'on':[],'best':(9,None,None)})
        if dv<L['best'][0]: L['best']=(dv,t,d)
    if prev is not None:
        for k in cur.keys()-prev.keys(): life[k]['on'].append(['+',t])
        for k in prev.keys()-cur.keys(): life[k]['on'].append(['-',t])
    else:
        for k in cur: life[k]['on'].append(['+',t])
    prev=cur
print(f"{RACE} off {OFF} finish {hm(t1)} - MOON STAR CHORDS every 5 s")
print("count by minute: "+'  '.join(f"{t-t0:+.0f}:{n}" for t,n in cnt if abs((t-t0)-round(t-t0))<1e-6))
X=pos('Moon',t0); print(f"Moon at off RA {X[0]:.3f} Dec {X[1]:+.3f}")
for k,L in sorted(life.items(),key=lambda x:x[1]['best'][1]):
    dv,tb,d=L['best']; ev=' '.join(f"{s}{t-t0:+.2f}" for s,t in L['on'])
    held=any(True for s,t in L['on'])
    print(f"{k[0]:4s} {L['typ']:14s} {k[1]}/{k[2]:13s} exact {hm(tb)} ({tb-t0:+.2f}) dev {dv*100:.3f}%  {ev}")
