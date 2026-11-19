"""Read-only scan (19 Nov 2026, Eddie after Newmarket 14:13 29 Oct 2022; chosen after the result): the sky race score's own lines
(bb_sky_race_score) - which runners' rule cells carry them, and cover picks split by the score lines inside their cover-item cells.
Usage: python3 tools/scans/bb_scan_skyscore_picks.py [--race <race>]"""
import sys, os, re, json
ARGS = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_sky_race_score as S, bb_scan_negatives as NG
from bb_cover8 import C


def key(a, b, p): return (frozenset((a, b)), p)


def score_lines(race):
    out = {}
    for w in S.score(race)[3]:
        m = re.match(r'([+-]) S (\S+(?: \S+)?) – S (\S+(?: \S+)?) (RA|Dec) ', w)
        out.setdefault(key(m.group(2), m.group(3), m.group(4)), []).append(m.group(1))
    return out


def held(race):
    d = json.load(open(f'docs/eddie_read/bybody_rules/{race}_bbrules.json'))['rules']; h = {}
    for k, hs in d.items():
        for x in hs:
            if not x.get('watch_only'):
                h.setdefault(x['runner'], {}).setdefault(k, []).extend(x['cells'])
    return h


def lines_in(cells, sl):
    got = set()
    for c in cells:
        m = re.match(r'S (\S+(?: \S+)?) – S (\S+(?: \S+)?) (RA|Dec) ', c)
        if m and key(*m.groups()) in sl:
            got.add(key(*m.groups()))
    pl = sum(sl[k].count('+') for k in got); mi = sum(sl[k].count('-') for k in got)
    return pl, mi, got


def race_rows(race):
    sl = score_lines(race); rows = []
    for r, rs in held(race).items():
        its = [c for c in C if all(x in rs for x in c)]
        cov = [cell for c in its for x in c for cell in rs[x]]
        allc = [cell for cs in rs.values() for cell in cs]
        rows.append((r, bool(its), lines_in(cov, sl)[:2], lines_in(allc, sl)[:2]))
    return rows


if __name__ == '__main__':
    if '--race' in ARGS:
        r = ARGS[ARGS.index('--race') + 1]
        print(S.score(r)[:3])
        for x in race_rows(r): print(x)
        sys.exit()
    names = [r for r, _ in NG.RACES]; after = set(names[names.index('20261116_wolverhampton_aw_1800'):])
    T = {}
    for race, win in NG.RACES:
        if not os.path.exists(f'docs/eddie_read/bybody_rules/{race}_bbrules.json') or \
           not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'):
            continue
        try:
            rows = race_rows(race)
        except Exception:
            continue
        for r, pick, cov, allc in rows:
            if not pick: continue
            for name, (p, m) in (('cover cells', cov), ('all rule cells', allc)):
                lab = '+ only' if p and not m else '- only' if m and not p else 'both' if p and m else 'none'
                for per in ('all', 'since fixed' if race in after else None):
                    if per: T.setdefault((name, per, lab), []).append(win in r)
    for (name, per, lab), v in sorted(T.items()):
        print(f'{name:15} {per:12} {lab:7} picks {len(v):3} won {sum(v)}')
