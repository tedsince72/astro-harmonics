"""check_tl_events.py (independent checker, 22 Oct 2026): (a) every star-source event of a runner's TIMELINE H / J and LONG TIMELINE
H / J recomputed from POSITIONS with own code; none missing or extra; source / also, target value, value and score at the off, minutes,
applying / separating. Writes a pickle of the events for the engine / sky-equivalent checks.
usage: check_tl_events.py tables.xlsx [runner] [out.pickle]"""
import pickle, re, sys, collections
sys.path.insert(0, __import__('os').path.dirname(__file__))
from check_tl_common import *

path = sys.argv[1]
runner = sys.argv[2] if len(sys.argv) > 2 else 'P01'
outp = sys.argv[3] if len(sys.argv) > 3 else None
wb = openpyxl.load_workbook(path, read_only=True)
sky, ch = load_positions(wb, runner)
W = World(sky, ch)
B = tl_blocks(wb[runner])
stars = [s for s in STARS67 if s in ch['H'] and s in ch['J'] and s in sky]
print('stars', len(stars))
bad = []


def win(e):
    return e['t'] is not None and -30.0 <= e['t'] <= 60.0


def lng(e):
    return e['score'] is not None and e['score'] >= 90.0


def also_of(note):
    if not note:
        return []
    for part in str(note).split('; '):
        if part.startswith('also '):
            return part[5:].split(', ')
    return []


report = {}
dump = {}
for C in ('H', 'J'):
    ev, kept = star_events(W, C, stars)
    print(f'{C}: kept pair rows {kept}; events per source', {s: len(v) for s, v in ev.items()},
          'midpoints', sum(1 for v in ev.values() for e in v if e['kind'] == 'midpoint'))
    for blk, filt in ((f'TIMELINE {C}', win), (f'LONG TIMELINE {C}', lng)):
        rows = [r for r in B[blk] if r[3] and not str(r[3]).startswith('———') and r[4] and r[3] != 'source']
        rows = [r for r in rows if r[1] != 'exact (race-local)']
        table_rows = [r for r in rows if r[3] not in STAR_SRC]
        star_rows = [r for r in rows if r[3] in STAR_SRC]
        tkeys = {}
        for r in table_rows:
            k = row_key(r, W)
            if k is not None:
                tkeys[k] = r
        mine = collections.OrderedDict()   # key -> event (with also lists)
        tab_also = collections.defaultdict(list)
        tab_also_any = collections.defaultdict(list)
        for src in STAR_SRC:
            for e in ev[src]:
                k = e['key']
                ok = filt(e)
                if k in tkeys:
                    if ok and src not in tab_also[k]:
                        tab_also[k].append(src)
                    if src not in tab_also_any[k]:
                        tab_also_any[k].append(src)
                    continue
                if k in mine:
                    m = mine[k]
                    if src != m['src']:
                        if ok and src not in m['also']:
                            m['also'].append(src)
                        if src not in m['also_any']:
                            m['also_any'].append(src)
                    continue
                if ok:
                    mine[k] = dict(e, also=[], also_any=[])
        # pre-pass occurrences that failed before the event was added are 'also_any' too
        for src in STAR_SRC:
            for e in ev[src]:
                k = e['key']
                if k in mine and src != mine[k]['src'] and src not in mine[k]['also_any']:
                    mine[k]['also_any'].append(src)
        # compare
        seen = set()
        n_ok = 0
        for r in star_rows:
            k = row_key(r, W)
            if k not in mine:
                bad.append((blk, 'extra row (not in my events)', r[1:13]))
                continue
            if k in seen:
                bad.append((blk, 'duplicate row', r[1:13]))
            seen.add(k)
            e = mine[k]
            prob = []
            if r[3] != e['src']:
                prob.append(('source', r[3], e['src']))
            if r[4] != e['rel']:
                prob.append(('rel', r[4], e['rel']))
            if r[5] != e['plane']:
                prob.append(('plane', r[5], e['plane']))
            kind_sheet = r[6]
            if kind_sheet != e['kind']:
                prob.append(('kind', kind_sheet, e['kind']))
            if abs(float(r[8]) - e['tv']) > 1e-6:
                prob.append(('target value', r[8], e['tv']))
            if e['kind'] != 'midpoint':
                tt = target_text(e['tgt'], e['hit'], e['kind'])
                if r[7] != tt:
                    prob.append(('target text', r[7], tt))
            if abs(float(r[9]) - round(e['v0'], 6)) > 1.5e-6:
                prob.append(('value at the off', r[9], e['v0']))
            sc = None if e['score'] is None else round(e['score'], 2)
            if (r[10] is None) != (sc is None) or (sc is not None and abs(r[10] - sc) > 0.0051):
                prob.append(('score', r[10], sc))
            ap = 'applying' if e['t'] > 0 else 'separating'
            if not blk.startswith('LONG'):
                if abs(float(r[2]) - e['t']) > 0.051:
                    prob.append(('minutes', r[2], e['t']))
                if r[11] != ap:
                    prob.append(('app/sep', r[11], ap))
            else:
                m = re.search(r'\(([-+]?[\d.]+) (min|days)\)', str(r[20]))
                lt = float(m[1]) * (1440.0 if m[2] == 'days' else 1.0)
                tol = 0.051 if m[2] == 'min' else 0.006 * 1440
                if abs(lt - e['t']) > tol:
                    prob.append(('linear estimate', r[20], e['t']))
            al = also_of(r[12])
            if al != e['also']:
                prob.append(('also', al, e['also'], 'any-occurrence variant', e['also_any']))
            note_out = 'outside at the off' in str(r[12] or '')
            if not blk.startswith('LONG') and note_out != (not e['hit']):
                prob.append(('outside note', r[12], e['hit']))
            if prob:
                bad.append((blk, r[4], r[5], prob))
            else:
                n_ok += 1
        for k, e in mine.items():
            if k not in seen:
                bad.append((blk, 'MISSING on the sheet', e['src'], e['rel'], e['plane'], e['kind'], e['tv'], round(e['v0'], 6),
                            e['score'], e['t']))
        # star sources in 'also' of table rows
        for k, r in tkeys.items():
            al = [a for a in also_of(r[12]) if a in STAR_SRC]
            if al != tab_also[k]:
                bad.append((blk, 'table row also', r[3], r[4], r[5], al, tab_also[k], 'any', tab_also_any[k]))
        nt = sum(1 for k in tab_also if tab_also[k])
        c = collections.Counter(r[3] for r in star_rows)
        report[blk] = (len(rows), len(table_rows), dict(c), nt, n_ok)
        print(f'{blk}: rows {len(rows)} (table {len(table_rows)}, star {len(star_rows)}) per source {dict(c)}; mine {len(mine)}; '
              f'star rows matching every cell {n_ok}; table rows gaining a star "also": {nt}')
        dump[blk] = [dict({x: y for x, y in e.items()}, key=k) for k, e in mine.items()]
print('MISMATCHES', len(bad))
for b in bad[:80]:
    print('  ', b)
if outp:
    with open(outp, 'wb') as f:
        pickle.dump(dict(dump=dump, sky=sky, ch=ch), f)
