#!/usr/bin/env python3
"""field.py RACE  - Jupiter-centred read, layer 4: the field view. Reads layer3/P##.json for every runner (no results).
Writes docs/jupiter/RACE/field.txt:
  A. per measure: which runners hold it (k of n; RARE = fewer than half the field), each runner's lines with numbers
  B. per runner: details held by fewer than half the field (same key = same bodies / same kind)
  C. 30 tightest Jupiter cross link, field ranked (RA and Dec)
  D. Jupiter with itself across charts (the frozen 12 Oct watch line, recomputed here from the same definition:
     Equator ratio tight, same-body set, Jupiter moved, close cross link H Jupiter – J Jupiter) - shown, not changed
  E. riders (for 36, same rider / pair again - needs past results, not judged here)
Counts are background only."""
import sys, json, glob, os

ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
         34, 35, 'ST']
NAMES = {1: 'Jupiter cross links (and links struck on both ends by 2+ sky bodies)', 2: 'cross link struck both ends (one body / one per end)',
         3: 'partner strike', 4: 'cross-link pair together in the sky', 5: 'both ends of a cross link moved', 6: 'movement onto a cross link / Jupiter moved',
         7: 'swap', 8: 'triangle struck at every corner', 9: 'natal Jupiter pair struck both ends by one sky body',
         10: 'natal Jupiter pair struck both ends by 2+ sky bodies', 11: 'same number / ratio in both charts', 12: 'shared node',
         13: 'shared natal pair', 14: 'shared pair also cross-linked', 15: 'pair set H:J:S', 16: 'same-body set of Jupiter',
         17: 'same-body set 4:5:9 split', 18: 'same-body set joined to the web', 19: 'split', 20: 'midpoint', 21: 'soak',
         22: 'sky/natal ratio of a Jupiter pair', 23: 'Jupiter in sky/natal ratios in both charts', 24: 'h:j and pair family ratios',
         25: 'Jupiter Equator whole/ninth (+ derived)', 26: 'Jupiter Equator ratios', 27: 'return / contact', 28: 'RA AND Dec together (sky -> natal)',
         29: 'natal Jupiter pair RA AND Dec together', 30: 'tightest Jupiter cross link', 31: 'Jupiter as hub', 32: 'Jupiter pair lit many ways',
         33: 'node on the Jupiter links', 34: 'recurring pair (annotation)', 35: 'recurring cross link (annotation)', 'ST': 'Jupiter and the stars'}


def main():
    race = sys.argv[1]
    base = f'docs/jupiter/{race}'
    R = {}
    for f in sorted(glob.glob(f'{base}/layer3/P*.json')):
        R[os.path.basename(f)[:-5]] = json.load(open(f))
    n = len(R); half = n / 2
    L = [f'== {race} — Jupiter-centred read, field view (layer 4). {n} runners. RARE = held by fewer than half the field (< {half:g}).',
         '   Blind: no results opened. Counts are background only.', '']
    for P, d in R.items():
        L.append(f'   {P} {d["runner"]}')
    # keys -> holders
    keyhold = {}
    for P, d in R.items():
        for it in d['items']:
            keyhold.setdefault(it['key'], set()).add(P)

    # A. per measure
    L += ['', 'A. PER MEASURE']
    for m in ORDER:
        hold = [P for P, d in R.items() if any(i['m'] == m for i in d['items'])]
        if m in (30, 32):
            continue
        tagr = ' — RARE' if hold and len(hold) < half else ''
        L.append(f'\n[{m}] {NAMES[m]}: held by {len(hold)} of {n}{tagr}' + (f" ({', '.join(hold)})" if hold else ''))
        for P in hold:
            for it in [i for i in R[P]['items'] if i['m'] == m]:
                k = len(keyhold[it['key']])
                L.append(f"   {P}  {it['text']}  {{{k}/{n}{' rare' if k < half else ''}}}")
    # 32 compact
    L.append(f'\n[32] {NAMES[32]} (per runner, pairs with 2+ kinds)')
    for P, d in R.items():
        f = [i for i in d['items'] if i['m'] == 32 and i['nk'] >= 2]
        L.append(f"   {P}  " + ('; '.join(i['text'].replace('pair ', '') for i in f) if f else '-'))

    # B. rare details per runner
    L += ['', 'B. DETAILS HELD BY FEWER THAN HALF THE FIELD (per runner; 32 and 30 left out)']
    for P, d in R.items():
        rare = [i for i in d['items'] if i['m'] not in (30, 32) and len(keyhold[i['key']]) < half]
        L.append(f"\n   {P} {d['runner']}")
        seen = set()
        for i in sorted(rare, key=lambda i: ORDER.index(i['m'])):
            if (i['m'], i['text']) in seen:
                continue
            seen.add((i['m'], i['text']))
            L.append(f"     [{i['m']}] {i['text']}  {{{len(keyhold[i['key']])}/{n}}}")
        if not rare:
            L.append('     -')

    # C. tightest cross link
    L += ['', 'C. [30] TIGHTEST JUPITER CROSS LINK (close band), field ranked']
    T = [(P, i) for P, d in R.items() for i in d['items'] if i['m'] == 30]
    for pl, k, lk in (('RA', 'minRA', 'linkRA'), ('Dec', 'minDec', 'linkDec')):
        L.append(f'   by {pl}:')
        for P, i in sorted(T, key=lambda t: t[1][k]):
            L.append(f"     {P} {i[lk]} {pl} {i[k]:.4f}")
    none = [P for P in R if P not in {t[0] for t in T}]
    if none:
        L.append(f"   no close Jupiter cross link: {', '.join(none)}")

    # D. Jupiter with itself across charts (watch line definition, 12 Oct)
    L += ['', 'D. JUPITER WITH ITSELF ACROSS CHARTS (12 Oct watch-line definition; shown, not changed)']
    kinds = {'E': lambda i: i['m'] == 26 and i.get('band') == 'tight',
             'B': lambda i: i['m'] in (16, 17),
             'M': lambda i: i['m'] == 6 and i.get('sub') == 'jupiter_moved',
             'X': lambda i: i['m'] == 1 and i.get('sub') == 'link' and i['key'] == 'link H Jupiter–J Jupiter' and i.get('band') == 'close'}
    held = {k: [P for P, d in R.items() if any(fn(i) for i in d['items'])] for k, fn in kinds.items()}
    for k, nm in (('E', 'Jupiter Equator ratio (tight)'), ('B', 'Jupiter same-body set'), ('M', 'Jupiter moved onto a whole/ninth'),
                  ('X', 'close cross link H Jupiter – J Jupiter')):
        L.append(f"   [{k}] {nm}: held by {len(held[k])} of {n}{' — RARE' if held[k] and len(held[k]) < half else ''}"
                 + (f" ({', '.join(held[k])})" if held[k] else ''))
    for P, d in R.items():
        mine = [k for k in kinds if P in held[k] and len(held[k]) < half]
        lines = [i['text'] for i in d['items'] if any(fn(i) for fn in kinds.values())]
        L.append(f"   {P} {'HOLDS ' + ','.join(mine) if mine else '-':10s} " + ' | '.join(lines))

    # E. riders
    L += ['', 'E. [36] RIDERS (same rider / pair again needs past results; not judged here)']
    for P, d in R.items():
        L.append(f"   {P} {d['jockey']}")
    txt = '\n'.join(L) + '\n'
    open(f'{base}/field.txt', 'w').write(txt)
    print(f'{race}: field view -> {base}/field.txt')


if __name__ == '__main__':
    main()
