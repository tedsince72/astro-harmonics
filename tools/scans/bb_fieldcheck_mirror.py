"""Field check (16 Nov 2026, Eddie: 'I actually meant this' - Society Red's Venus mirror, Ripon 15:25 16 Jun 2022, won 16/1). Read-only;
winners named below, no results file read. 13 result races, from the bybody xlsx.
Society Red H Venus (Dec): S Venus -> H Venus contraparallel 0.0141 (95.31); sky Venus conj sky Uranus 0.0330 (88.99) and conj
S Aldebaran 0.0333 (88.89); S Uranus -> H Venus cp 0.0471 (84.3); H Aldebaran - H Venus cp 0.0469 (84.37).
'mirror' = the same-body line S X -> c X conj or contraparallel in Dec (body X, chart c; no natal Moon).
 M1   mirror >= 90                     M1b  mirror >= 80
 M2   M1 + a sky body Y (not the Moon, not X) conj / cp sky X in Dec (any score)
 M3   M1 + a royal star conj / cp sky X in Dec
 M4   M1 + both (Society Red)
 M5   M2 with S Y -> c X conj / cp too (the sky body carries the mirror to natal X)
 M6   M3 with c R - c X conj / cp (the royal star's natal line carries it; near-automatic: stars barely move)
 M2b, M3b, M4b  as M2-M4 on M1b (mirror >= 80)"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_split import RACES
CJ = ('conj', 'contraparallel'); ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
KEYS = ['M1', 'M1b', 'M2', 'M3', 'M4', 'M5', 'M6', 'M2b', 'M3b', 'M4b']
dec_cj = lambda r: r['plane'].startswith('Dec') and r['fam'] in CJ and r['sc'] is not None


def cases(X, d, bodies):
    out = []
    for c in 'HJ':
        mir = [r for r in d['L'] if r['line'] == f'S {X} → {c} {X}' and dec_cj(r)]
        if not mir:
            continue
        m = max(r['sc'] for r in mir)
        ys, rs, yc, rc = [], [], [], []
        for o in d['O']:
            if not dec_cj(o): continue
            ln = o['line']
            if ' – ' in ln and ln.endswith(f'– S {X}'):
                Y = ln.split(' – ')[0][2:]
                if Y in ROY: rs.append(o)
                elif Y in bodies and Y not in ('Moon', X): ys.append(o)
        for o in d['S'] + d['O']:
            if dec_cj(o) and o['line'].endswith(f'→ {c} {X}') and ' → ' in o['line']:
                yc.append(o['line'][2:].split(' → ')[0])
        for r in d['L']:
            if dec_cj(r) and r['line'].endswith(f'– {c} {X}') and r['line'].split(' – ')[0][2:] in ROY:
                rc.append(r['line'].split(' – ')[0][2:])
        Ys = {o['line'].split(' – ')[0][2:] for o in ys}; Rs = {o['line'].split(' – ')[0][2:] for o in rs}
        t = set()
        for hi, suf in ((90, ''), (80, 'b')):
            if m < hi: continue
            t.add('M1' + suf)
            if Ys: t.add('M2' + suf)
            if Rs: t.add('M3' + suf)
            if Ys and Rs: t.add('M4' + suf)
            if not suf:
                if Ys & set(yc): t.add('M5')
                if Rs & set(rc): t.add('M6')
        t &= set(KEYS)
        if t:
            out.append((t, f"{c} {X}: mirror {m}; sky bodies on S {X}: {sorted(Ys)}; royal on S {X}: {sorted(Rs)}; "
                           f"carried to {c} {X}: {sorted(Ys & set(yc))} / royal {sorted(Rs & set(rc))}"))
    return out


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        held = {k: [] for k in KEYS}; ex = []
        for run, D in data.items():
            tg = set()
            for X, d in D.items():
                for t, s in cases(X, d, set(D) | {'Rahu', 'Ketu'}):
                    tg |= t
                    if 'M2' in t or 'M3' in t: ex.append(f'{run} {s}')
            for k in tg: held[k].append(run)
        for k in KEYS:
            hh = held[k]; tot[k][0] += len(hh); tot[k][1] += sum(win in x for x in hh); tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
        for x in ex: print('    ', x)
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k, (p, w, c) in tot.items(): print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')


if __name__ == '__main__':
    main()
