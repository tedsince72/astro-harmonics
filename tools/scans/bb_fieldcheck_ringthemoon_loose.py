"""Looser versions of J1 (Ring The Moon Juno; 17 Nov 2026; read-only, from the depth ladder json files).
J1: loop closed (depth >= 3), same-body line >= 90, one pair end E on both natal X (S E -> H X and S E -> J X, number family, >= 80).
Versions vary: loop (depth >= 3 closed, or >= 2 one end only), same-body cut, end cut, conj / cp end lines allowed.
Prints picks / won / by chance over the result races with a depth json."""
import sys, json, os, re
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_fieldcheck_ringthemoon as RM
SC = re.compile(r'\(([\d.]+)\)\s*$')
sc = lambda c: float(SC.search(c).group(1)) if SC.search(c) else 0.0
# name: (min depth, same-body cut, end cut (both charts), allow conj / cp, one end >= 90 needed)
V = {
    'J1 (as found)':            (3, 90, 80, False, False),
    'L1 same-body >= 80':       (3, 80, 80, False, False),
    'L2 ends >= 50':            (3, 90, 50, False, False),
    'L3 ends any score':        (3, 90, 0, False, False),
    'L4 conj / cp ends allowed':(3, 90, 80, True, False),
    'L5 loop not closed (>=2)': (2, 90, 80, False, False),
    'L6 same-body >= 80, ends >= 50': (3, 80, 50, False, False),
    'L7 same-body any, ends >= 80':   (3, 0, 80, False, False),
    'L8 >=2, same-body >= 80, ends >= 80': (2, 80, 80, False, False),
    'L9 >=2, same-body >= 50, ends >= 80, one >= 90': (2, 50, 80, False, True),
}


def holds(r, v):
    dmin, sbc, endc, cj, one90 = v
    for b in r['bodies']:
        if b['depth'] < dmin or not b['cells']:
            continue
        X, cs = b['body'], b['cells']
        if sc(cs[0]) < sbc:
            continue
        for c in cs:
            m = re.match(r'(\S+) on X: (.*)', c)
            if not m:
                continue
            good = [l for l in m.group(2).split('; ') if (cj or ('conj' not in l and 'contraparallel' not in l)) and sc(l) >= endc]
            h = [l for l in good if f'→ H {X}' in l]; j = [l for l in good if f'→ J {X}' in l]
            if h and j and (not one90 or any(sc(l) >= 90 for l in h + j)):
                return f"{X}: {cs[0]} | {m.group(1)}: {h[0]} ; {j[0]}"
    return None


def main():
    tot = {k: [0, 0, 0.0, []] for k in V}; n = 0
    for race, win in RM.RACES:
        f = f'docs/eddie_read/depth/{race}_depth.json'
        if not os.path.exists(f):
            continue
        n += 1
        rs = json.load(open(f))['runners']; N = len(rs)
        for r in rs:
            for k, v in V.items():
                t = holds(r, v)
                if t:
                    a = tot[k]; a[0] += 1; a[1] += win in r['runner']; a[2] += 1 / N
                    a[3].append(('*' if win in r['runner'] else '') + race[:16] + ' ' + r['runner'] + ' ' + t.split(':')[0])
    print(f'## {n} result races (picks / won / by chance); * = winner')
    for k, (p, w, c, ws) in tot.items():
        print(f'  {k}: {p} / {w} / {c:.1f}')
        if p <= 12:
            for x in ws: print('      ', x)


if __name__ == '__main__':
    main()
