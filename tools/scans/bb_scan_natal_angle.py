"""Natal-to-natal angle (18 Nov 2026, Eddie: 'it is worth looking at these races from a natal to natal angle as well'; read-only).
Per runner (horse + jockey charts added), natal pairs c X – c Y (natal bodies, no Moon, + royal stars; no royal – royal, not the
chart's own Rahu – Ketu), planes RA / Dec, number families only (bb_scan_natal_pairs.nums). Sky pairs: sky bodies + royal stars,
no Moon, no royal – royal, not sky Rahu – Ketu; number families or conj (bb_scan_sky_both_natal.score).
  nat90   natal pair lines scoring >= 90
  same_n  natal >= 80 and the same pair in the sky (same plane) on the same family + target, sky >= 50
  same_a  natal >= 90 and the same pair in the sky (either plane) scoring >= 80 on any number / conj
  share1  natal >= 90 and a sky pair >= 80 sharing exactly one body, same family + target
  anysky  natal >= 90 and any sky pair >= 80 on the same family + target
  tight   natal >= 80 and a sky pair >= 80 (any bodies) within 0.01 of the natal value, same family + target
  both    sky pair >= 80 whose two bodies are both in natal pairs >= 90 (bb_scan_sky_both_natal; same + cross)
Winner's place in each race: top (ties shared), bottom (ties shared), vs chance; for the 19 races the cover misses and all races.
Usage: python3 tools/scans/bb_scan_natal_angle.py [--show]"""
import sys, itertools, os, openpyxl
ARGS = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
import bb_scan_negatives as N
from bb_scan_uranus_pairs import dist
from bb_scan_natal_pairs import nums, P, NAT, SKYP
from bb_scan_sky_both_natal import score
ROY = set(B.ROYAL)
MISS = {'Graces Quest', 'Hamish', 'Arvico Bleu', 'Present Moment', 'Sir Chauvelin', 'Not Available', 'First Flow', 'Nicholas T',
        'Venturous', 'New Age Dawning', 'Two For Gold', 'Silva Eclipse', 'Olympe De Gouges', 'River Bray', 'Daphne Moon',
        'Domandlouis', 'Cafe Sydney', 'Novakai'}
KEYS = ['nat90', 'same_n', 'same_a', 'share1', 'anysky', 'tight', 'both']


def pairs(points):
    for X, Y in itertools.combinations(points, 2):
        if {X, Y} == {'Rahu', 'Ketu'} or (X in ROY and Y in ROY):
            continue
        yield X, Y


def sky_lines(tp, tr):
    out = []  # (frozenset, plane, value, best(fam, tgt) or None, score, numhits)
    for X, Y in pairs([x for x in SKYP if x != 'Moon']):
        for pl in ('RA', 'Dec'):
            a, b = P(tp, tr, X, pl), P(tp, tr, Y, pl)
            if a is None or b is None:
                continue
            v = dist(a, b, pl); s = score(v, pl)
            out.append((frozenset((X, Y)), pl, v, s, nums(v, pl)))
    return out


def runner_counts(pos, ra, sky):
    c = dict.fromkeys(KEYS, 0); nat90 = set(); show = []
    sky80 = [(p, pl, v, s) for p, pl, v, s, h in sky if s and s[1] >= 80]
    bykey = {}
    for p, pl, v, s, h in sky:
        for f, t, sc in h:
            if sc >= 50:
                bykey.setdefault((f, t), []).append((p, pl, v, sc))
    for X, Y in pairs(NAT + B.ROYAL):
        p = frozenset((X, Y))
        for pl in ('RA', 'Dec'):
            a, b = P(pos, ra, X, pl), P(pos, ra, Y, pl)
            if a is None or b is None:
                continue
            v = dist(a, b, pl); h = nums(v, pl)
            if not h:
                continue
            f, t, sc = h[0]
            if sc >= 90:
                c['nat90'] += 1; nat90.add(p)
            if sc < 80:
                continue
            k = (f, t); on = bykey.get(k, [])
            if any(q == p and qpl == pl for q, qpl, qv, qs in on):
                c['same_n'] += 1; show.append(f'same_n {X} – {Y} {pl} {v:.4f} {t}')
            on80 = [x for x in on if x[3] >= 80]
            if any(abs(qv - v) < 0.01 for q, qpl, qv, qs in on80):
                c['tight'] += 1
                q = min(on80, key=lambda x: abs(x[2] - v))
                show.append(f"tight {X} – {Y} {pl} {v:.4f} = S {' – S '.join(sorted(q[0]))} {q[1]} {q[2]:.4f} {t}")
            if sc < 90:
                continue
            if any(q == p for q, *_ in sky80):
                c['same_a'] += 1
            if any(len(q & p) == 1 for q, *_ in on80):
                c['share1'] += 1
            if on80:
                c['anysky'] += 1
    bodies = set().union(*nat90) if nat90 else set()
    c['both'] = sum(1 for q, *_ in {(q,) for q, pl, v, s in sky80} if q <= bodies)
    return c, show


def race(race):
    path = f'reference/classic/race_batch_{race}_active.xlsx'
    if not os.path.exists(path):
        return None
    runners, tt, tp = B.load(path)
    tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
    sky = sky_lines(tp, tr); rows = []
    for cl, r in sorted(runners.items()):
        tot = dict.fromkeys(KEYS, 0); sh = []
        for ch in 'HJ':
            if not r['pos'].get(ch):
                continue
            c, s = runner_counts(r['pos'][ch], r['ra'][ch], sky)
            for k in KEYS: tot[k] += c[k]
            sh += [ch + ' ' + x for x in s]
        rows.append((r['name'].get('H'), tot, sh))
    return rows


def place(rows, win, k):
    vals = [t[k] for n, t, s in rows]; w = next(t[k] for n, t, s in rows if n and win in n)
    hi, lo = max(vals), min(vals); n = len(vals)
    top = (w == hi) / vals.count(hi) if hi > lo else 0; bot = (w == lo) / vals.count(lo) if hi > lo else 0
    return top, bot, (1 / n if hi > lo else 0), (1 / n if hi > lo else 0)


def main():
    res = {}
    for r, win in N.RACES:
        rows = race(r)
        if rows: res[r] = (win, rows)
    for name, sel in (('the 19 races the cover misses', [r for r in res if res[r][0] in MISS]), ('all races', list(res))):
        print(f'## {name} ({len(sel)} with an _active.xlsx)\n')
        print('| measure | winner top (ties shared) | chance | winner bottom | chance |\n|---|---|---|---|---|')
        for k in KEYS:
            a = [place(res[r][1], res[r][0], k) for r in sel]
            print(f'| {k} | {sum(x[0] for x in a):.1f} | {sum(x[2] for x in a):.1f} | {sum(x[1] for x in a):.1f} | {sum(x[3] for x in a):.1f} |')
        print()
    print('## Each of the 19 races: runner counts (winner marked *)\n')
    for r in res:
        win, rows = res[r]
        if win not in MISS: continue
        print(f'### {r} ({win})\n')
        print('| runner | ' + ' | '.join(KEYS) + ' |\n|---|' + '---|' * len(KEYS))
        for n, t, s in rows:
            print(f"| {'*' if n and win in n else ''}{n} | " + ' | '.join(str(t[k]) for k in KEYS) + ' |')
        if '--show' in ARGS:
            w = next(x for x in rows if x[0] and win in x[0])
            for line in w[2]: print('    ' + line)
        print()


if __name__ == '__main__':
    main()
