"""Sky to sky, pair by pair, for the sqrt 2 / silver families (19 Nov 2026, Eddie: 'ok, what about sky to sky and certain pairs';
read-only). Families on the NEW targets only (what the bybody scoring does not count today; see bb_scan_sqrt2_multiples.py and
bb_scan_sqrt2_powers.py): sqrt 2 multiples (k x 1.41421, k not 1, 5, 10, 50, 100, ±0.0283), silver multiples (k x 2.41421, k not 1, 10,
±0.0483), sqrt 2 powers and silver powers (m x b^n, new targets, ±0.15 %). Sky lines S A - S B, bodies (Moon incl., Rahu - Ketu left
out), RA and Dec, scoring >= cut. Golden and phi powers (bybody's own) alongside as baselines.
Per race: cover hit / miss (cover of eight picks from the rule files), favourite won / lost (bb_favs_outer_uranus.FAV).
Per pair (A - B, family; planes pooled): races holding it, cover misses, favourites won. Lean labels (Claude's choice):
  cover: 'miss' = held in >= 3 races with a cover result and miss rate >= 0.7; 'hit' = >= 4 races, miss rate 0.
  favourite: 'won' = >= 2 favourite wins and win rate >= 0.5.
Fair check, leave one race out: labels from the other races, race score = hit-lean pairs held - miss-lean pairs held; mean score in
cover-hit vs cover-miss races; favourite score = won-lean pairs held, fav won vs lost. Chosen after the results.
  python3 tools/scans/bb_scan_sqrt2_skypairs.py [cut]   (default 90)"""
import sys, os, json, math, itertools, io, contextlib
from collections import defaultdict
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 90
sys.argv = sys.argv[:1]
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_regulus_apex as RA
R2, PHI = math.sqrt(2), (1 + 5 ** 0.5) / 2
SIL = 1 + R2
OLDT = [t for _f, _l, t, _tol in EB.TARGETS]
isnew = lambda t: all(abs(t - o) > 1e-6 for o in OLDT)


def powers(b):
    return sorted({round(m * b ** n, 9) for m in (1, 10, 100) for n in range(-20, 20) if n and 0.3 <= m * b ** n <= 180})


FAMS = {'sqrt2 mult': [(k * R2, 0.02 * R2) for k in range(1, 128) if k not in (1, 5, 10, 50, 100)],
        'silver mult': [(k * SIL, 0.02 * SIL) for k in range(1, 75) if k not in (1, 10)],
        'sqrt2 pow': [(t, 0.0015 * t) for t in powers(R2) if isnew(t)],
        'silver pow': [(t, 0.0015 * t) for t in powers(SIL) if isnew(t)],
        'golden': [(k * PHI, 0.0324) for k in range(1, 125)],
        'phi pow': [(t, tol) for f, _l, t, tol in EB.TARGETS if f == 'phi power']}
TESTS = ('sqrt2 mult', 'silver mult', 'sqrt2 pow', 'silver pow')


def score(v, fam):
    if v is None:
        return None
    b = None
    for t, tol in FAMS[fam]:
        d = abs(v - t)
        if d < tol:
            s = 100 * (tol - d) / tol
            b = s if b is None or s > b else b
    return b


def load():
    races = []
    for race, win in NG.RACES:
        p = f'reference/classic/race_batch_{race}_active.xlsx'
        if not os.path.exists(p):
            continue
        runners, tt, tp = EB.load(p)
        rf = f'docs/eddie_read/bybody_rules/{race}_bbrules.json'
        cover = None
        if os.path.exists(rf):
            J = json.load(open(rf))
            held = {r: set() for r in J['runners']}
            for rid, cs in J['rules'].items():
                for c in cs:
                    if not c.get('watch_only'):
                        held.setdefault(c['runner'], set()).add(rid)
            picks = {RA.key(r) for r in J['runners'] if any(set(c) <= held[r] for c in RA.C8)}
            cover = RA.key(win) in picks if picks else None
        fav = F.FAV.get(race)
        favwon = (RA.key(fav) == RA.key(win)) if fav else None
        lines = defaultdict(set)   # family -> {(A, B)}
        for pl in ('RA', 'Dec'):
            for a, b in itertools.combinations(EB.BODIES, 2):
                if {a, b} == {'Rahu', 'Ketu'}:
                    continue
                v = EB.pair(tt, 'S', pl, a, b)
                for f in FAMS:
                    s = score(v, f)
                    if s is not None and s >= CUT:
                        lines[f].add((a, b, pl))
        races.append(dict(race=race, cover=cover, favwon=favwon, lines=lines))
    return races


def tally(races, fam, skip=None):
    T = defaultdict(lambda: [0, 0, 0, 0, 0])   # pair -> [races, with cover result, misses, with fav, fav won]
    for i, r in enumerate(races):
        if i == skip:
            continue
        for p in {(a, b) for a, b, _pl in r['lines'][fam]}:
            t = T[p]
            t[0] += 1
            if r['cover'] is not None:
                t[1] += 1
                t[2] += r['cover'] is False
            if r['favwon'] is not None:
                t[3] += 1
                t[4] += r['favwon']
    return T


def labels(T):
    cov, fav = {}, set()
    for p, (n, nc, m, nf, w) in T.items():
        if nc >= 3 and m / nc >= 0.7:
            cov[p] = -1
        elif nc >= 4 and m == 0:
            cov[p] = 1
        if w >= 2 and nf and w / nf >= 0.5:
            fav.add(p)
    return cov, fav


def main():
    races = load()
    nc = [r for r in races if r['cover'] is not None]
    nf = [r for r in races if r['favwon'] is not None]
    base_m = sum(r['cover'] is False for r in nc) / len(nc)
    base_w = sum(r['favwon'] for r in nf) / len(nf)
    print(f'# Sky to sky, pair by pair: sqrt 2 / silver families (new targets), cut {CUT:g}\n')
    print(f'{len(races)} result races; {len(nc)} with a cover result ({sum(r["cover"] is False for r in nc)} misses, base miss rate '
          f'{base_m:.2f}); {len(nf)} with a favourite ({sum(r["favwon"] for r in nf)} won, base {base_w:.2f}). Chosen after the results.\n')
    for fam in TESTS + ('golden', 'phi pow'):
        T = tally(races, fam)
        print(f'## {fam}\n')
        rows = sorted(T.items(), key=lambda x: -x[1][0])
        cov, fav = labels(T)
        lean = [(p, t) for p, t in rows if p in cov or p in fav]
        print(f'{len(T)} pairs score somewhere; races with a line: {sum(1 for r in races if r["lines"][fam])}. '
              f'Leaning pairs (all races, in-sample): cover miss {sum(v < 0 for v in cov.values())}, cover hit '
              f'{sum(v > 0 for v in cov.values())}, favourite won {len(fav)}.\n')
        print('| pair | races | cover misses / with result (expected) | fav won / with fav (expected) | lean |\n|---|---|---|---|---|')
        for p, (n, ncv, m, nfv, w) in lean:
            tag = ', '.join(x for x in (('miss' if cov.get(p) == -1 else 'hit' if cov.get(p) == 1 else ''),
                                        'fav won' if p in fav else '') if x)
            print(f'| S {p[0]} – S {p[1]} | {n} | {m} / {ncv} ({ncv * base_m:.1f}) | {w} / {nfv} ({nfv * base_w:.1f}) | {tag} |')
        # leave one out
        sc_hit, sc_miss, f_won, f_lost = [], [], [], []
        for i, r in enumerate(races):
            cov_i, fav_i = labels(tally(races, fam, skip=i))
            ps = {(a, b) for a, b, _pl in r['lines'][fam]}
            s = sum(cov_i.get(p, 0) for p in ps)
            if r['cover'] is True:
                sc_hit.append(s)
            elif r['cover'] is False:
                sc_miss.append(s)
            fs = sum(p in fav_i for p in ps)
            if r['favwon'] is True:
                f_won.append(fs)
            elif r['favwon'] is False:
                f_lost.append(fs)
        mean = lambda x: sum(x) / len(x) if x else 0
        neg_hit = sum(s < 0 for s in sc_hit); neg_miss = sum(s < 0 for s in sc_miss)
        print(f'\nLeave one race out: cover score mean {mean(sc_hit):.2f} in hit races ({len(sc_hit)}), {mean(sc_miss):.2f} in miss '
              f'races ({len(sc_miss)}); score < 0 in {neg_miss} miss races and {neg_hit} hit races. Favourite score (won-lean pairs held) '
              f'mean {mean(f_won):.2f} when the favourite won ({len(f_won)}), {mean(f_lost):.2f} when it lost ({len(f_lost)}); '
              f'>= 1 in {sum(x >= 1 for x in f_won)} won / {sum(x >= 1 for x in f_lost)} lost.\n')


if __name__ == '__main__':
    main()
