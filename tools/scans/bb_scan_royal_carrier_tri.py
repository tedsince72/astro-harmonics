"""Royal carrier triangle (20 Nov 2026, Eddie: 'back to Hollie Doyle and the triangle / how about this shape', from Newcastle AW
16:10 19 Nov 2026 Ezenli / Hollie Doyle: J Antares - J Orcus RA 111.111 (83.7), S Antares - S Ketu RA 62xphi (84.0),
S Ketu -> J Orcus Dec 8xphi (93.7); read-only, chosen after the result).
Shape, per chart c (H or J), royal star R, natal body X, sky body Y (not the Moon, not R):
  side 1  c R - c X       (natal royal line)       number family >= cut
  side 2  S R - S Y       (sky line from the star)  number family >= cut
  side 3  S Y -> c X      (sky body on natal X)     number family >= cut
  closing only ACROSS planes (a triangle closed in one plane is forced by geometry).
A runner holds it with >= 1 such triangle. Shapes are counted once per (chart, R, X): two Ys conjunct each other give the same
fact twice (Ezenli: S Haumea conj S Ketu in Dec makes S Haumea -> J Orcus 8xphi too).
  python3 tools/scans/bb_scan_royal_carrier_tri.py [cut] [--race RACE] [--jockey NAME]"""
import sys, os, re, io, contextlib
args = sys.argv[1:]
RACE = args[args.index('--race') + 1] if '--race' in args else None
JOCK = args[args.index('--jockey') + 1] if '--jockey' in args else None
nums = [a for a in args if re.fullmatch(r'[\d.]+', a)]
CUT = float(nums[0]) if nums else 80.0
sys.argv = sys.argv[:1]
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_runner_triangles as RT
    import bb_scan_regulus_apex as RA
RT.CUT = CUT
ROY = EB.ROYAL
SKYY = [b for b in EB.BODIES if b != 'Moon']
NAT = EB.NATAL_BODIES


def sides(get, keyf):
    out = {}
    for pl in ('RA', 'Dec'):
        f = RT.fam(get(pl), pl)
        if f:
            out[pl] = f
    return out


def shapes(r, tt):
    found = {}
    for ch in ('H', 'J'):
        d = r['dist'].get(ch)
        if not d:
            continue
        for R in ROY:
            for X in NAT:
                s1 = sides(lambda pl: EB.pair(d, 'N', pl, R, X), None)
                if not s1:
                    continue
                for Y in SKYY:
                    s2 = sides(lambda pl: EB.pair(tt, 'S', pl, R, Y), None)
                    s3 = sides(lambda pl: d.get(('S', pl, Y, X)), None)
                    if s2 and s3 and RT.closes([s1, s2, s3]):
                        found.setdefault((ch, R, X), []).append((Y, s1, s2, s3))
    return found


def jname(r):
    return re.sub(r'^\d+\s+', '', r['name'].get('J') or '')


def main():
    races = [(RACE, None)] if RACE else NG.RACES
    tot = dict(n=0, h=0, w=0, ch=0.0, fh=0, fw=0)
    print(f'# Royal carrier triangle, cut {CUT:g}\n')
    for race, win in races:
        p = f'reference/classic/race_batch_{race}_active.xlsx'
        if not os.path.exists(p):
            continue
        runners, tt, tp = EB.load(p)
        hold = {}
        for r in runners.values():
            if JOCK and jname(r) != JOCK:
                continue
            s = shapes(r, tt)
            if s:
                hold[RA.key(r['name'].get('H') or '')] = (r, s)
        n = len(runners)
        fav = F.FAV.get(race)
        tot['n'] += 1; tot['h'] += len(hold); tot['ch'] += len(hold) / n
        if win:
            tot['w'] += RA.key(win) in hold
        if fav and RA.key(fav) in hold:
            tot['fh'] += 1; tot['fw'] += fav == win
        if RACE or JOCK:
            print(f'## {race} ({n} ran){" winner " + win if win else ""}\n')
            for k, (r, s) in hold.items():
                tag = ' **won**' if win and RA.key(win) == k else ''
                print(f'- {r["name"]["H"]} / {jname(r)}{tag}: {len(s)} shape(s)')
                for (ch, R, X), ys in s.items():
                    yl = '; '.join(f'S {Y} ({"/".join(f"{pl} {f}" for pl, f in s2.items())} | {"/".join(f"{pl} {f}" for pl, f in s3.items())})'
                                   for Y, s1, s2, s3 in ys)
                    s1 = ys[0][1]
                    print(f'  - {ch} {R} - {ch} {X} ({"/".join(f"{pl} {f}" for pl, f in s1.items())}) carried by {yl}')
            if not hold:
                print('- none')
            print()
    print(f'Total: {tot["n"]} races, {tot["h"]} holders, {tot["w"]} won, {tot["ch"]:.1f} by chance; '
          f'favourites holding {tot["fh"]}, won {tot["fw"]}')


if __name__ == '__main__':
    main()
