"""report.py - JR v3 field counts, flags, joins and pages (design sections 5B cut 4, 6, 5G)."""
import json, os
from core import LEVELS, SLOW, EQUATOR, STAR_NAMES

STRUCK = ('strict', 'exact-in-race', 'exact-pre-off')
GROUPS = [('C', 'C. TRANSIT TO NATAL'), ('D', 'D. RATIOS OF THE SAME RELATIONSHIP'), ('E', 'E. THREE-WAY MIDPOINTS'),
          ('B', 'B. NATAL TO NATAL — joined by the sky (cut 4)'), ('A', 'A. THE RACE SKY — joined by this runner')]


def fmt_eta(e):
    if e is None:
        return ''
    if abs(e) >= 600:
        return f'exact {e / 60:+.1f} h'
    return f'exact {e:+.1f} min'


def line(h, fc=None):
    if h.get('parts'):
        nums = ' + '.join(f"{p['plane']} {p['value']:.5f} -> {p['target']} ({p['family']}, off {p['offset']:+.5f}{'%' if p['unit'] == '%' else ''}, "
                          f"t {p['t']:.2f}, {p['level']}{', ' + p['as'] if p['as'] != 'n/a' else ''}{', ' + fmt_eta(p['eta']) if p['eta'] is not None else ''})"
                          if p['value'] is not None else
                          f"{p['desc']} [{p['level']}]" for p in h['parts'])
        core = f"{h['desc']}: {nums}"
        lev = f"{h['level']} | t {h['t']:.2f}"
    elif h['family'] == 'contact':
        core = h['desc']
        lev = f"{h['level']} | t {h['t']:.2f}"
    elif h['family'] == 'midpoint':
        core = f"{h['desc']} {h['plane']}: off {h['offset']:+.5f}"
        lev = f"{h['level']} | t {h['t']:.2f} | a/s {h['as']}{' ' + fmt_eta(h['eta']) if h['eta'] is not None else ''}"
    else:
        u = '%' if h['unit'] == '%' else ''
        val = f"{h['value']:.5f}"
        if h.get('num') is not None:
            val = f"{max(h['num'], h['den']):.5f} / {min(h['num'], h['den']):.5f} = {h['value']:.5f}"
        core = f"{h['desc']} {h['plane']} {val} -> {h['family']} {h['target']} off {h['offset']:+.5f}{u}"
        lev = f"{h['level']} | t {h['t']:.2f} | a/s {h['as']}{' ' + fmt_eta(h['eta']) if h['eta'] is not None else ''}"
    fl = f" [{','.join(h['flags'])}]" if h['flags'] else ''
    return f"[{h['m']}] {core}{fl} | {lev}" + (f' | {fc}' if fc else '')


def field_counts(per_runner):
    """key -> {level: set(runners)}"""
    K = {}
    for P, hs in per_runner.items():
        for h in hs:
            K.setdefault(h['key'], {l: set() for l in LEVELS})[h['level']].add(P)
    return K


def fc_text(K, key, n):
    d = K[key]
    tot = len(set().union(*d.values()))
    return f"field S{len(d['strict'])} I{len(d['exact-in-race'])} P{len(d['exact-pre-off'])} N{len(d['near'])} (holders {tot}/{n})"


def holders(K, key):
    return len(set().union(*K[key].values()))


def b_joined(h, hs):
    """cut 4: the same pair has a D1 hit, or a sky body strikes either end (C1, C3 = sky Jupiter on natal Jupiter, C2)."""
    natal = [p for p in h['pts'] if not p.startswith('S ')]
    struck = set()
    d1 = set()
    for g in hs:
        if g['level'] not in STRUCK:
            continue
        if g['m'] in ('C1', 'C3', 'C2') and not g.get('parts'):
            struck.add(g['pts'][1])
        if g['m'] == 'D1':
            c, x = g['pts'][3].split(' ', 1)
            d1.add((c, x))
    why = []
    for p in natal:
        if p in struck:
            why.append(f'{p} struck')
    if h['m'] in ('B1', 'B2'):
        for p in natal:
            c, x = p.split(' ', 1)
            if x not in ('Jupiter', EQUATOR) and (c, x) in d1:
                why.append(f'D1 on {c} Jupiter–{x}')
    return why


def a_joins(a, hs):
    """A hit joined by this runner: same value or same pair in its natal charts (B1/B2 same form, plane, target; or D1 on X)."""
    why = []
    xs = [p.split(' ', 1)[1] for p in a['pts'] if p != 'S Jupiter']
    for g in hs:
        if g['level'] not in STRUCK:
            continue
        gx = [p.split(' ', 1)[1] for p in g['pts'] if not p.endswith(' Jupiter')]
        if a['m'] == 'A1' and g['m'] == 'B1' and g['plane'] == a['plane'] and g['target'] == a['target'] and gx == xs:
            why.append(f"{g['pts'][0]} same value")
        if a['m'] == 'A2' and g['m'] == 'B2' and g['plane'] == a['plane'] and g['target'] == a['target'] and sorted(gx) == sorted(xs) \
                and ('equator' in xs) == ('equator' in gx):
            why.append(f"{g['pts'][0]} same ratio")
        if g['m'] == 'D1' and g['plane'] == a['plane'] and [x for x in xs if x != EQUATOR] and \
                g['pts'][1].split(' ', 1)[1] in xs:
            why.append(f"D1 on {g['pts'][1].split(' ', 1)[1]} {g['plane']}")
    return sorted(set(why))


def write_all(out, race, n_note, sky_lines, sky_h, runners, per_runner, durtxt):
    os.makedirs(out, exist_ok=True)
    n = len(per_runner); half = n / 2
    K = field_counts(per_runner)
    # flags: age = natal-only slow-body hit held by >= half the field
    for P, hs in per_runner.items():
        for h in hs:
            if h['m'].startswith('B'):
                others = [p.split(' ', 1)[1] for p in h['pts'] if not p.endswith(' Jupiter')]
                if all(o in SLOW or o in STAR_NAMES or o == EQUATOR for o in others) and holders(K, h['key']) >= half and 'age' not in h['flags']:
                    h['flags'].append('age')

    pages = {}
    for P, hs in per_runner.items():
        R = runners[P]
        show = {g: [] for g, _ in GROUPS}
        for h in hs:
            g = h['m'][0]
            if g == 'B':
                why = b_joined(h, hs)
                if not why:
                    continue
                h['joined_by'] = why
            # JR v3: strict / exact-in-race / exact-pre-off only; a near hit only as a part of a combined hit or chain
            # (combined with one near part = near, shown); both-near chains -> full file only
            if h['level'] not in STRUCK and not (h.get('parts') and 'both-near' not in h['flags']):
                continue
            show[g].append(h)
        for a in sky_h:
            if a['level'] in STRUCK:
                why = a_joins(a, hs)
                if why:
                    show['A'].append(dict(a, joined_by=why))
        pages[P] = show
        L = [f"{P} {R['cloth']} {R['horse']} / {R['jockey']} — JR v3 runner page ({race})",
             f"   Jupiter: S RA {sky_lines['SJ'][0]:.5f} Dec {sky_lines['SJ'][1]:+.5f} | H RA {R['H']['Jupiter'][0]:.5f} Dec {R['H']['Jupiter'][1]:+.5f} | "
             f"J RA {R['J']['Jupiter'][0]:.5f} Dec {R['J']['Jupiter'][1]:+.5f}",
             f'   {durtxt}', '   levels: strict / exact-in-race / exact-pre-off / near; t = |offset| / strict tolerance; '
             f'field S/I/P/N = runners holding the same hit at each level, of {n}.',
             '   shown: strict / exact-in-race / exact-pre-off; near only as a part of a combined hit or chain (then the line is near).',
             '   chains (CH, RA/Dec): field = runners sharing the root (same sky pair, same plane), by level. Everything else: P##_full.txt. No scores.', '']
        for g, title in GROUPS:
            L.append(title)
            rows = sorted(show[g], key=lambda h: h['t'])
            for h in rows:
                extra = ''
                if h.get('joined_by'):
                    extra = f" | joined: {'; '.join(h['joined_by'])}"
                fc = fc_text(K, h['key'], n) if g != 'A' else 'same sky for every runner'
                L.append('   ' + line(h, fc) + extra)
            if not rows:
                L.append('   -')
            L.append('')
        open(f'{out}/{P}.txt', 'w').write('\n'.join(L))
        F = [f"{P} {R['cloth']} {R['horse']} / {R['jockey']} — JR v3 FULL (every hit incl. near, common and unjoined natal)", '']
        for h in sorted(hs, key=lambda h: (h['m'], h['t'])):
            F.append('   ' + line(h, fc_text(K, h['key'], n)) + (' | B joined: ' + '; '.join(b_joined(h, hs)) if h['m'][0] == 'B' and b_joined(h, hs) else ''))
        open(f'{out}/{P}_full.txt', 'w').write('\n'.join(F) + '\n')
        for h in hs:
            h['field'] = {l: sorted(K[h['key']][l]) for l in LEVELS}
        json.dump({'runner': P, 'cloth': R['cloth'], 'horse': R['horse'], 'jockey': R['jockey'], 'hits': hs},
                  open(f'{out}/{P}.json', 'w'), indent=1, default=str)

    # race page
    L = [f'== {race} — JR v3 transit-Jupiter reader, race page. {n} runner(s). Blind: no results opened. No scores, no totals.',
         f"   S Jupiter RA {sky_lines['SJ'][0]:.5f} Dec {sky_lines['SJ'][1]:+.5f}; {durtxt}", f'   {n_note}', '']
    for P, R in runners.items():
        L.append(f"   {P} {R['cloth']} {R['horse']} / {R['jockey']}: H Jupiter Dec {R['H']['Jupiter'][1]:+.5f}, J Jupiter Dec {R['J']['Jupiter'][1]:+.5f}")
    L += ['', "A. SKY JUPITER'S OWN RELATIONSHIPS (strict, exact-in-race, exact-pre-off; near in sky_full.txt), sorted by t"]
    for h in sorted([h for h in sky_h if h['level'] in STRUCK], key=lambda h: h['t']):
        L.append('   ' + line(h))
    L.append(f"   (near: {sum(1 for h in sky_h if h['level'] == 'near')} in sky_full.txt)")
    # chain roots (JR v3)
    roots = {}
    for P, hs in per_runner.items():
        for h in hs:
            if h['m'] == 'CH':
                lst = roots.setdefault(h['key'], [])
                sig = (P, h['natal'], tuple(round(x['value'], 5) for x in h['parts']))
                if sig not in [(q, g['natal'], tuple(round(x['value'], 5) for x in g['parts'])) for q, g in lst]:
                    lst.append((P, h))
    L += ['', 'CHAIN ROOTS (RA, Dec): two sky bodies on the same natal Jupiter in one plane; root = the sky pair (identity, not a filter).',
          '   field by level (S/I/P/N) incl. both-near chains (full file only); sorted by number of holders']
    for k, lst in sorted(roots.items(), key=lambda kv: (holders(K, kv[0]), kv[0])):
        h0 = lst[0][1]
        rn = h0['root_number']
        rtxt = f"root is a number: {rn['family']} {rn['target']} ({rn['level']})" if rn else 'root not a number'
        L.append(f"   {h0['root']} {h0['root_plane']} {h0['root_value']:.5f} ({rtxt}) | {fc_text(K, k, n)} | " +
                 '; '.join(f"{P} {h['natal']} {h['parts'][0]['value']:.5f} / {h['parts'][1]['value']:.5f} [{h['level']}{', both-near' if 'both-near' in h['flags'] else ''}]"
                           for P, h in lst))
    if not roots:
        L.append('   -')
    L += ['', f'RUNNERS: hits on the runner pages held by fewer than half the field (< {half:g}), sorted by t']
    for P, show in pages.items():
        R = runners[P]
        L.append(f"\n   {P} {R['cloth']} {R['horse']} / {R['jockey']}")
        rows = [h for g, _ in GROUPS if g != 'A' for h in show[g] if holders(K, h['key']) < half]
        for h in sorted(rows, key=lambda h: h['t']):
            L.append('     ' + line(h, fc_text(K, h['key'], n)))
        if not rows:
            L.append('     -')
    open(f'{out}/field.txt', 'w').write('\n'.join(L) + '\n')
    S = [f'{race} — A, every sky-Jupiter hit incl. near', ''] + ['   ' + line(h) for h in sorted(sky_h, key=lambda h: (h['m'], h['t']))]
    open(f'{out}/sky_full.txt', 'w').write('\n'.join(S) + '\n')
    json.dump(sky_h, open(f'{out}/sky.json', 'w'), indent=1, default=str)
