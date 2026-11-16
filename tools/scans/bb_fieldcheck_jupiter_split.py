"""Field check (16 Nov 2026, Eddie: 'I still think this is valid when they all score ... but check your ideas as well').
On Time (Newton Abbot 15:25 17 Jul 2022), Dec: S Jupiter -> H Jupiter 4.8284 3×φ, S Jupiter -> J Jupiter 6.4981 4×φ,
H Jupiter – J Jupiter 11.3265 7×φ (99.2); S Jupiter – S Sedna 6.4832 4×φ with S Sedna -> J Jupiter 12.9813 (sky Jupiter between);
S Ketu – S Orcus 6.4740 4×φ with S Ketu -> J Jupiter RA 33.3327. Read-only; from the _active.xlsx (eddie_bybody's loader and scorer,
non-conj family hits; the Moon never used). Versions, per runner (any plane, RA or Dec):
 E   Eddie: S Jupiter -> H Jupiter, S Jupiter -> J Jupiter and H Jupiter – J Jupiter all score in one plane
 Es  E with sky Jupiter between the natal Jupiters (the two legs add to H – J within 0.001)
 Ef  E with all three on the same family
 M1  sky Jupiter the midpoint of a natal Jupiter (H or J) and a sky body Y: d(S Jup, c Jup) and d(S Jup, S Y) on the same family + target,
     S Y -> c Jup = their sum within 0.05 (Y between-check), Y not Jupiter / Moon
 M2  M1 + a sky pair S A – S B (no Jupiter, no Moon, not Rahu – Ketu) on the same family + target and plane, with S A -> c Jup (or B)
     scoring in a family (any plane)
 M3  E + each sky leg's family + target carried by a sky pair S A – S B in that plane (no Jupiter, no Moon, neither end within the
     conjunction range of sky Jupiter in that plane)"""
import sys
sys.path.insert(0, 'tools'); import eddie_bybody as BY
sys.path.insert(0, 'tools/scans'); from bb_over100_tighten import RACES
RACES = RACES + [('Newton Abbot', '20220717_newton_abbot_1525', 'On Time')]
PTS = [p for p in BY.SKY_POINTS if p not in ('Jupiter', 'Moon')]


def fams(v, pl):
    return {(f, t): s for f, t, s in BY.hits(v, pl) if f != 'conj'} if v is not None else {}


def ra_d(a, b):
    x = abs(a - b) % 360
    return 360 - x if x > 180 else x


def sky_pairs(tt, pl, skip=()):
    out = []
    for i, a in enumerate(PTS):
        for b in PTS[i + 1:]:
            if {a, b} == {'Rahu', 'Ketu'} or a in skip or b in skip:
                continue
            v = BY.pair(tt, 'S', pl, a, b)
            for k, s in fams(v, pl).items():
                out.append((k, a, b, v, s))
    return out


def runner(r, tt, tp):
    out = {}
    if r['missing']:
        return out
    sj = {c: r['dist'][c] for c in 'HJ'}
    for pl in ('RA', 'Dec'):
        legs = {c: sj[c].get(('S', pl, 'Jupiter', 'Jupiter')) for c in 'HJ'}
        if pl == 'Dec':
            hj = abs(r['pos']['H']['Jupiter'] - r['pos']['J']['Jupiter'])
        else:
            hj = ra_d(r['ra']['H']['Jupiter'], r['ra']['J']['Jupiter'])
        fh, fj, fhj = fams(legs['H'], pl), fams(legs['J'], pl), fams(hj, pl)
        near = {p for p in PTS if (BY.pair(tt, 'S', pl, 'Jupiter', p) or 99) < BY.CONJ[pl]}
        pairs = sky_pairs(tt, pl)
        if fh and fj and fhj:
            txt = f"{pl}: S Jup→H Jup {legs['H']:.4f} {list(fh)} | S Jup→J Jup {legs['J']:.4f} {list(fj)} | H–J {hj:.4f} {list(fhj)}"
            out.setdefault('E', []).append(txt)
            if abs(legs['H'] + legs['J'] - hj) < 0.001:
                out.setdefault('Es', []).append(txt)
            if {k[0] for k in fh} & {k[0] for k in fj} & {k[0] for k in fhj}:
                out.setdefault('Ef', []).append(txt)
            car = {}
            for c, f in (('H', fh), ('J', fj)):
                car[c] = [f"S {a} – S {b} {v:.4f} {k[1]} ({s:.1f})" for k, a, b, v, s in pairs if k in f and a not in near and b not in near]
            if car['H'] and car['J']:
                out.setdefault('M3', []).append(txt + f" | carriers H: {car['H'][:2]} J: {car['J'][:2]}")
        for c in 'HJ':
            a = legs[c]
            fa = fams(a, pl)
            for Y in PTS:
                b = BY.pair(tt, 'S', pl, 'Jupiter', Y)
                fb = fams(b, pl)
                com = set(fa) & set(fb)
                if not com:
                    continue
                yc = sj[c].get(('S', pl, Y, 'Jupiter'))
                if yc is None or abs(yc - (a + b)) > 0.05:
                    continue
                for k in com:
                    t = f"{pl}: S Jup→{c} Jup {a:.4f} / S Jup–S {Y} {b:.4f} on {k[1]} {k[0]}, S {Y}→{c} Jup {yc:.4f}"
                    out.setdefault('M1', []).append(t)
                    for kk, A, B, v, s in pairs:
                        if kk != k or 'Jupiter' in (A, B):
                            continue
                        ends = [e for e in (A, B) if any(fams(sj[c].get(('S', p2, e, 'Jupiter')), p2) for p2 in ('RA', 'Dec'))]
                        if ends:
                            out.setdefault('M2', []).append(t + f" + S {A} – S {B} {v:.4f} ({s:.1f}), {ends} on {c} Jupiter")
    return out


KEYS = ['E', 'Es', 'Ef', 'M1', 'M2', 'M3']
tot = {k: [0, 0, 0.0] for k in KEYS}
for name, r, win in RACES:
    import glob, os
    f = f'reference/classic/race_batch_{r}_active.xlsx'
    f = f if os.path.exists(f) else sorted(glob.glob(f'/mnt/user-data/uploads/*race_batch_{r}_active.xlsx'))[0]
    R, tt, tp = BY.load(f); N = len(R)
    print(f'\n## {name} ({N} runners, winner {win})')
    held = {k: [] for k in KEYS}
    for cl, rr in sorted(R.items()):
        nm = rr['name'].get('H', '?')
        o = runner(rr, tt, tp)
        for k in KEYS:
            if o.get(k):
                held[k].append(nm)
                for t in o[k][:2]:
                    print(f'  [{k}] {cl} {nm}{" *WINNER*" if win in nm else ""}: {t}')
    for k in KEYS:
        h = held[k]; w = sum(1 for x in h if win in x)
        tot[k][0] += len(h); tot[k][1] += w; tot[k][2] += len(h) / N
    print('  holders: ' + ', '.join(f'{k} {len(held[k])}' for k in KEYS))
print('\n## Totals (picks / winners / by chance)')
for k, (p, w, c) in tot.items():
    print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')
