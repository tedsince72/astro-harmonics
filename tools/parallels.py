"""parallels RACE OFF DUR: for every runner, natal points whose Dec (or RA) the sky's bodies sit on at the off (within 0.03 deg); slow-body 'crossings'."""
import sys
src=open('/home/claude/lattice/layer1_tuned.py').read(); exec(src.split('# transit chords')[0])
NATP=collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour']=='12' and r['ra'] and r['body'] in BODIES and r['body']!='Moon': NATP[r['tab']][r['body']]=(float(r['ra']),float(r['dec']))
SKYB=[b for b in BODIES]
SP={b:pos(b,t0) for b in SKYB}
TOL=float(sys.argv[4]) if len(sys.argv)>4 else 0.03
for tab,(role,cloth,nm) in order:
    f=fin.get(cloth,('?','?'))
    hits=[]
    for nb,(ra,de) in NATP[tab].items():
        for sb,(sra,sde) in SP.items():
            dd=abs(sde-de); dr=abs(((sra-ra+180)%360)-180)
            rate=RATE[sb]
            if dd<=TOL:
                tt=(de-sde)/rate[1]*1440/24 if rate[1] else None   # minutes (rate per hour? RATE in deg/day*?)
                hits.append(f"Dec  sky {sb:10s} {sde:8.3f} ~ natal {nb:10s} {de:8.3f}  diff {dd:.3f}")
            if dr<=TOL: hits.append(f"RA   sky {sb:10s} {sra:8.3f} ~ natal {nb:10s} {ra:8.3f}  diff {dr:.3f}")
    print(f"[{f[0]}] {role:6s} {nm:26s} {f[1]:>5s}  {len(hits)}")
    for h in hits: print('      '+h)
