#!/usr/bin/env python3
"""shapes.py RACE  - Jupiter-centred read, layer 3: every measure (1-36) and the star section, with Jupiter in it, per runner.
Reads docs/jupiter/RACE/positions.csv and layer2/P##.json (run ratios.py first). Writes layer3/P##.json + P##.txt.
No field view (layer 4), no judgement. Every item carries its exact numbers.

Terms: H = horse natal, J = jockey natal, S = race sky. "strike" = sky body Z (incl. sky Moon, no stars) to a natal point at a
whole/ninth in any plane (+-0.005 / +-0.0005). "moved" = sky X vs natal X at a whole/ninth in any plane (+-0.01 / +-0.0011).
Cross link = H a - J b, close RA < 1.5 or Dec < 0.3 (near RA < 2 or Dec < 0.6). Inside-one-chart pair counts when tagged in any plane
or RA < 1.5 or Dec < 0.6. Node = Rahu (Ketu folded; where Ketu matters - shared node, node on a link - its mirror is checked too).

Measures (instructions file, 12 Oct 2026): 1/2 cross link struck on both ends (2+ bodies / one body / split); 3 partner strike;
4 pair together in the sky; 5 both ends moved; 6 movement onto a cross link; 7 swap; 8 triangle struck at every corner by one sky body;
9/10 natal Jupiter pair struck both ends by one / 2+ sky bodies; 11 same number in both charts; 12 shared node; 13/14 shared pair
(+ cross-linked); 15-17 from layer 2; 18 same-body set joined to the web; 19 split; 20 midpoint; 21 soak; 22-24, 26 from layer 2;
23 Jupiter in sky/natal ratios in BOTH charts; 25 Jupiter Equator whole/ninth and derived Dec strikes; 27 return / contact;
28 RA AND Dec together (sky -> natal); 29 natal Jupiter pair RA AND Dec together; 30 tightest Jupiter cross link (runner value;
field rank in layer 4); 31 hub; 32 pair lit many ways; 33 node on the Jupiter links; 34-35 recurring (annotation);
36 same rider / pair again (needs past results - listed in layer 4 only as rider name). Stars: section ST."""
import sys, json, itertools
from jcore import *

RECURRING = {frozenset(['Jupiter', 'Vesta']): 'recurring pair Jupiter–Vesta (Ffos Las, Wincanton, Nottingham 15:30, Exeter)',
             frozenset(['Jupiter', 'Pluto']): 'recurring pair Jupiter–Pluto (York 15:45, Nottingham 17:50)'}
STARS = None


class Runner:
    def __init__(self, sky, R):
        self.S, self.H, self.J = sky, R['H'], R['J']
        self.C = {'S': self.S, 'H': self.H, 'J': self.J}
        self._cache = {}

    def p(self, pt):                     # 'H Jupiter' -> position
        c, b = pt.split(' ', 1)
        return self.C[c][b]

    def pl(self, a, b):
        k = (a, b)
        if k not in self._cache:
            self._cache[k] = self._cache[(b, a)] = planes(self.p(a), self.p(b))
        return self._cache[k]

    def strikes(self, Z, pt):
        """sky body Z -> natal point pt: tagged planes"""
        return tags_all(self.pl(f'S {Z}', pt), 'pair')

    def moved(self, pt):
        c, b = pt.split(' ', 1)
        if c == 'S' or b not in self.S or b == 'Moon' or self.C[c][b][2] != 'body':
            return []
        return tags_all(self.pl(f'S {b}', pt), 'move')


def natal_points(R, charts=('H', 'J'), stars=False):
    return [f'{c} {b}' for c in charts for b in (R.C[c]) if (stars or R.C[c][b][2] == 'body')]


def runner_shapes(sky, Rd, L2):
    R = Runner(sky, Rd)
    items = []

    def add(m, text, **kw):
        kw.update({'m': m, 'text': text}); items.append(kw)

    skyZ = [b for b in SKY_BODIES if b in sky]
    jup = ['H Jupiter', 'J Jupiter']

    # ---------- cross links through Jupiter (1-7, 30, 33)
    links = []
    for b in NATAL_BODIES:
        for a_pt, b_pt in (('H Jupiter', f'J {b}'), (f'H {b}', 'J Jupiter')):
            if a_pt == 'H Jupiter' and b_pt == 'J Jupiter' and links and any(l['a'] == 'H Jupiter' and l['b'] == 'J Jupiter' for l in links):
                continue
            v = R.pl(a_pt, b_pt); bd = band(v['RA'], v['Dec'])
            if bd:
                links.append({'a': a_pt, 'b': b_pt, 'RA': v['RA'], 'Dec': v['Dec'], 'GC': v['GC'], 'band': bd})
    for l in links:
        desc = f"{l['a']} – {l['b']} RA {l['RA']:.4f} Dec {l['Dec']:.4f} [{l['band']}]"
        add(1, f'cross link {desc}', key=f"link {l['a']}–{l['b']}", sub='link', band=l['band'], RA=l['RA'], Dec=l['Dec'],
            pair=sorted([l['a'].split()[1], l['b'].split()[1]]))
        # 2 both-ends strikes
        sa = {Z: R.strikes(Z, l['a']) for Z in skyZ}; sb = {Z: R.strikes(Z, l['b']) for Z in skyZ}
        both = [Z for Z in skyZ if sa[Z] and sb[Z]]
        if both:
            m = 1 if len(both) >= 2 else 2
            add(m, f"{desc} struck on both ends by {len(both)} sky bod{'ies' if len(both) > 1 else 'y'}: " +
                '; '.join(f'S {Z} ({tagstr(sa[Z])} | {tagstr(sb[Z])})' for Z in both),
                key=f"both-ends {l['a']}–{l['b']}", sub='both_ends', n=len(both), band=l['band'],
                pair=sorted([l['a'].split()[1], l['b'].split()[1]]))
        else:
            ea = [Z for Z in skyZ if sa[Z]]; eb = [Z for Z in skyZ if sb[Z]]
            if ea and eb:
                add(2, f"{desc} struck one body per end: {l['a']} by " + ', '.join(f'S {Z} ({tagstr(sa[Z])})' for Z in ea)
                    + f" | {l['b']} by " + ', '.join(f'S {Z} ({tagstr(sb[Z])})' for Z in eb),
                    key=f"split-strike {l['a']}–{l['b']}", sub='split_ends', band=l['band'],
                    pair=sorted([l['a'].split()[1], l['b'].split()[1]]))
        # 3 partner strike: sky y -> H x ; sky x -> J y
        x, y = l['a'].split()[1], l['b'].split()[1]
        for Z, tgt in ((y, l['a']), (x, l['b'])):
            if Z in sky:
                t = R.strikes(Z, tgt)
                if t:
                    add(3, f'partner strike on {desc}: S {Z} -> {tgt} {tagstr(t)}', key=f"partner S {Z}->{tgt}",
                        pair=sorted([x, y]))
        # 4 pair together in the sky
        if x != y and x in sky and y in sky:
            v = R.pl(f'S {x}', f'S {y}')
            if v['GC'] < 5 or contact(v['RA'], v['Dec']):
                add(4, f'{desc}: sky {x}–{y} together GC {v["GC"]:.4f} (RA {v["RA"]:.4f} Dec {v["Dec"]:.4f})',
                    key=f'sky-together {x}–{y}', pair=sorted([x, y]))
        # 5 / 6 movement
        ma, mb = R.moved(l['a']), R.moved(l['b'])
        if ma and mb:
            add(5, f'{desc}: both ends moved — {l["a"]} moved {tagstr(ma)} | {l["b"]} moved {tagstr(mb)}',
                key=f"both-moved {l['a']}–{l['b']}", pair=sorted([x, y]))
        for pt, mv in ((l['a'], ma), (l['b'], mb)):
            if mv:
                add(6, f'{desc}: {pt} moved {tagstr(mv)} (end of the link)', key=f'moved-onto {pt} [{l["a"]}–{l["b"]}]',
                    pair=sorted([x, y]))
        # 33 node on the Jupiter links
        if 'Rahu' in (x, y):
            add(33, f'node on a Jupiter cross link: {desc}', key=f"node-link {l['a']}–{l['b']}")
        if sa.get('Rahu') and sb.get('Rahu'):
            add(33, f'sky node strikes both ends of {desc}: ({tagstr(sa["Rahu"])} | {tagstr(sb["Rahu"])})', key=f"node-strike {l['a']}–{l['b']}")
    # Ketu side of node on Jupiter links
    for c_j, c_n in (('H', 'J'), ('J', 'H')):
        k = ketu(R.C[c_n]['Rahu']); v = planes(R.C[c_j]['Jupiter'], k); bd = band(v['RA'], v['Dec'])
        if bd:
            add(33, f'{c_j} Jupiter – {c_n} Ketu (node mirror) RA {v["RA"]:.4f} Dec {v["Dec"]:.4f} [{bd}]', key=f'node-link {c_j} Jupiter–{c_n} Ketu')
    # 30 tightest Jupiter cross link of this runner
    close_links = [l for l in links if l['band'] == 'close']
    if close_links:
        tRA = min(close_links, key=lambda l: l['RA']); tDe = min(close_links, key=lambda l: l['Dec'])
        add(30, f"tightest Jupiter cross link: RA {tRA['a']} – {tRA['b']} {tRA['RA']:.4f}; Dec {tDe['a']} – {tDe['b']} {tDe['Dec']:.4f}",
            key='tightest', minRA=tRA['RA'], minDec=tDe['Dec'], linkRA=f"{tRA['a']}–{tRA['b']}", linkDec=f"{tDe['a']}–{tDe['b']}")
    # 7 swap
    for b in NATAL_BODIES:
        if b == 'Jupiter':
            continue
        v1 = R.pl('H Jupiter', f'J {b}'); v2 = R.pl(f'H {b}', 'J Jupiter')
        if contact(v1['RA'], v1['Dec']) and contact(v2['RA'], v2['Dec']):
            add(7, f'swap Jupiter/{b}: H Jupiter – J {b} RA {v1["RA"]:.4f} Dec {v1["Dec"]:.4f}; H {b} – J Jupiter RA {v2["RA"]:.4f} Dec {v2["Dec"]:.4f}',
                key=f'swap Jupiter/{b}', pair=sorted(['Jupiter', b]))

    # ---------- 9/10, 29 natal Jupiter pairs inside one chart
    for c in ('H', 'J'):
        for b in NATAL_BODIES:
            if b == 'Jupiter':
                continue
            a_pt, b_pt = f'{c} Jupiter', f'{c} {b}'
            v = R.pl(a_pt, b_pt); t = tags_all(v, 'pair')
            if t and any(pl == 'RA' for pl, _, _ in t) and any(pl == 'Dec' for pl, _, _ in t):
                add(29, f'{c} Jupiter–{b} RA AND Dec together: {tagstr(t)}', key=f'radec-natal {c} Jupiter–{b}', pair=sorted(['Jupiter', b]))
            if not (t or contact(v['RA'], v['Dec'], INSIDE_CLOSE)):
                continue
            both = [Z for Z in skyZ if R.strikes(Z, a_pt) and R.strikes(Z, b_pt)]
            if both:
                pd = tagstr(t) if t else f"conj RA {v['RA']:.4f} Dec {v['Dec']:.4f}"
                add(10 if len(both) >= 2 else 9, f'{c} Jupiter–{b} ({pd}) struck on both ends by ' +
                    '; '.join(f'S {Z} ({tagstr(R.strikes(Z, a_pt))} | {tagstr(R.strikes(Z, b_pt))})' for Z in both),
                    key=f'natal-struck {c} Jupiter–{b}', n=len(both), pair=sorted(['Jupiter', b]))

    # ---------- 8 triangle with a Jupiter corner (natal corners H/J, pairwise whole numbers, one sky body on all three)
    pts = natal_points(R)
    def whole(a, b):
        return [(pl, v, tg) for pl, v, tg in tags_all(R.pl(a, b), 'pair') if tg.startswith('W')]
    for jp in jup:
        nb = [p for p in pts if p != jp and whole(jp, p)]
        for p1, p2 in itertools.combinations(nb, 2):
            w12 = whole(p1, p2)
            if not w12:
                continue
            Zs = [Z for Z in skyZ if R.strikes(Z, jp) and R.strikes(Z, p1) and R.strikes(Z, p2)]
            if Zs:
                add(8, f'triangle {jp} – {p1} – {p2} (sides {tagstr(whole(jp, p1))} / {tagstr(whole(jp, p2))} / {tagstr(w12)}) '
                       f'struck at every corner by ' + ', '.join(f'S {Z}' for Z in Zs),
                    key=f'triangle {"–".join(sorted([jp, p1, p2]))}')

    # ---------- 11 same number in both charts (Jupiter roots: Equator + natal Jupiter pairs)
    roots = {'H': {}, 'J': {}}
    for c in ('H', 'J'):
        e = tag(abs(R.C[c]['Jupiter'][1]), 'equator')
        if e:
            roots[c].setdefault(label(e), []).append(f'{c} Jupiter Equator {abs(R.C[c]["Jupiter"][1]):.5f}')
        for b in NATAL_BODIES:
            if b != 'Jupiter':
                for pl, v, tg in tags_all(R.pl(f'{c} Jupiter', f'{c} {b}'), 'pair'):
                    roots[c].setdefault(label(tg), []).append(f'{c} Jupiter–{b} {pl} {v:.5f}')
    for n in sorted(set(roots['H']) & set(roots['J']), key=lambda s: eval(s)):
        add(11, f'same number {n} in both charts: ' + '; '.join(roots['H'][n]) + ' || ' + '; '.join(roots['J'][n]), key=f'same-number {n}')

    # ---------- 12 shared node, with Jupiter on it
    for nm, jn in (('Rahu', R.J['Rahu']), ('Ketu', ketu(R.J['Rahu']))):
        g = gc(R.H['Rahu'], jn)
        if g < 3:
            onj = []
            for c in ('H', 'J'):
                for nn, npos in (('Rahu', R.C[c]['Rahu']), ('Ketu', ketu(R.C[c]['Rahu']))):
                    for cj in ('H', 'J'):
                        v = planes(R.C[cj]['Jupiter'], npos)
                        if contact(v['RA'], v['Dec']):
                            onj.append(f'{cj} Jupiter – {c} {nn} RA {v["RA"]:.4f} Dec {v["Dec"]:.4f}')
            add(12, f'shared node: H Rahu – J {nm} GC {g:.4f}' + ('; Jupiter on the node: ' + '; '.join(onj) if onj else '; no Jupiter on the node'),
                key='shared-node', jup=bool(onj))

    # ---------- 13/14 from layer 2 shared + cross link
    for it in L2:
        if it['kind'] == 'shared':
            x = it['x']; v1 = R.pl('H Jupiter', f'J {x}'); v2 = R.pl(f'H {x}', 'J Jupiter')
            cl = [f'H Jupiter – J {x} RA {v1["RA"]:.4f} Dec {v1["Dec"]:.4f}' if contact(v1['RA'], v1['Dec']) else '',
                  f'H {x} – J Jupiter RA {v2["RA"]:.4f} Dec {v2["Dec"]:.4f}' if contact(v2['RA'], v2['Dec']) else '']
            cl = [c for c in cl if c]
            if cl:
                add(14, f"{it['text']} AND cross-linked: " + '; '.join(cl), key=f"shared+cross Jupiter–{x} {it['plane']}", pair=sorted(['Jupiter', x]))

    # ---------- 18 same-body set joined to the web; 23 both charts in sky/natal ratio
    sets = [i for i in L2 if i['kind'] == 'set']
    if sets:
        web = [l for l in links if l['band'] == 'close'] + [i for i in L2 if i['kind'] in ('skynat', 'hj', 'family') and i.get('band') == 'tight']
        if web:
            add(18, f"Jupiter same-body set ({', '.join(s['plane'] for s in sets)}) and Jupiter on the web: "
                    f"{len([l for l in links if l['band'] == 'close'])} close cross link(s), "
                    f"{len([i for i in L2 if i['kind'] in ('skynat', 'hj', 'family') and i.get('band') == 'tight'])} tight ratio(s)", key='set-joined')
    sn = {c: [i for i in L2 if i['kind'] == 'skynat' and i['chart'] == c and i['band'] == 'tight'] for c in ('H', 'J')}
    if sn['H'] and sn['J']:
        add(23, 'Jupiter in tight sky/natal ratios in BOTH charts: H ' + '; '.join(f"{i['pair']} {i['plane']} {i['ratio']}" for i in sn['H'])
            + ' || J ' + '; '.join(f"{i['pair']} {i['plane']} {i['ratio']}" for i in sn['J']), key='skynat-both')
        same = {(i['ratio']) for i in sn['H']} & {(i['ratio']) for i in sn['J']}
        for r in sorted(same):
            add(11, f'same sky/natal ratio {r} in both charts on Jupiter pairs', key=f'same-ratio {r}')

    # ---------- 19 split (RA or Dec): moved X between natal X and natal Y, with Jupiter as X or Y
    nat = natal_points(R)
    def betweens(xpt, ypt, plane):
        nx, sx, ny = R.p(xpt), R.S[xpt.split()[1]], R.p(ypt)
        if plane == 'RA':
            d1, d2 = signed_ra(nx[0], sx[0]), signed_ra(sx[0], ny[0])
        else:
            d1, d2 = sx[1] - nx[1], ny[1] - sx[1]
        if d1 == 0 or d2 == 0 or (d1 > 0) != (d2 > 0) or abs(d1) + abs(d2) > 180:
            return None
        return abs(d1), abs(d2)
    for xpt in nat:
        xb = xpt.split()[1]
        if xb == 'Moon' or xb not in R.S:
            continue
        for plane in ('RA', 'Dec'):
            mv = R.pl(f'S {xb}', xpt)[plane]; mt = tag(mv, 'move')
            if not mt:
                continue
            for ypt in nat:
                if ypt == xpt or ('Jupiter' not in (xb, ypt.split()[1])):
                    continue
                bt = betweens(xpt, ypt, plane)
                if not bt:
                    continue
                m, o = bt
                for nm, a, b in (('parts', m, o), ('span/other', m + o, o)):
                    f = fit(a, b, allow1=True)
                    if f and f[2] <= R_SPLIT:
                        add(19, f'split {plane}: S {xb} moved {m:.5f} ({label(mt)}) from {xpt}, lies between {xpt} and {ypt}; '
                                f'other part {o:.5f}; {nm} {frac(f)} ({f[2]:.4f}%)', key=f'split {xpt}/{ypt} {plane}')

    # ---------- 20 midpoint: natal body at the midpoint of natal X and sky X (X = Jupiter, or the body at the midpoint = Jupiter)
    def mid_items(xpt):
        xb = xpt.split()[1]; nx, sx = R.p(xpt), R.S[xb]; res = []
        for plane in ('RA', 'Dec'):
            if plane == 'RA':
                d = signed_ra(nx[0], sx[0]); span = abs(d); mid = (nx[0] + d / 2) % 360
            else:
                span = abs(sx[1] - nx[1]); mid = (sx[1] + nx[1]) / 2
            if span < 0.5 or span >= 60:
                continue
            res.append((plane, span, mid))
        return res
    for xpt in nat:
        xb = xpt.split()[1]
        if xb == 'Moon' or xb not in R.S:
            continue
        for plane, span, mid in mid_items(xpt):
            for ypt in nat:
                if ypt == xpt:
                    continue
                if xb != 'Jupiter' and ypt.split()[1] != 'Jupiter':
                    continue
                yv = R.p(ypt)
                off = wrap_ra(yv[0], mid) if plane == 'RA' else abs(yv[1] - mid)
                if off <= 0.05:
                    strict = ypt[0] != xpt[0]
                    add(20, f'midpoint {plane}: {ypt} at the midpoint of {xpt} and S {xb} (span {span:.4f}{", wide" if span >= 20 else ""}; '
                            f'off {off:.4f}) [{"strict: other chart" if strict and span < 20 else ("other chart, wide" if strict else "same chart")}]',
                        key=f'midpoint {ypt} @ {xpt}/S {xb} {plane}', strict=strict and span < 20)

    # ---------- 21 soak: one value from a Jupiter to 4+ non-star partners across H, J, S
    for jp in ['S Jupiter'] + jup:
        groups = {}
        for c in ('S', 'H', 'J'):
            for b, v in R.C[c].items():
                pt = f'{c} {b}'
                if v[2] != 'body' or pt == jp:
                    continue
                for pl, val, tg in tags_all(R.pl(jp, pt), 'pair'):
                    groups.setdefault(label(tg), {}).setdefault(pt, f'{pt} {pl} {val:.5f}')
        for n, d in groups.items():
            if len(d) >= 4:
                add(21, f'soak {jp} value {n} from {len(d)} partners: ' + '; '.join(d.values()), key=f'soak {jp} {n}')

    # ---------- 25 Jupiter Equator whole/ninth and derived Dec strikes
    for c in ('S', 'H', 'J'):
        e = abs(R.C[c]['Jupiter'][1]); et = tag(e, 'equator')
        if et:
            der = []
            for c2 in ('S', 'H', 'J'):
                for b, v in R.C[c2].items():
                    if v[2] != 'body' or (c2 == c and b == 'Jupiter'):
                        continue
                    e2 = tag(abs(v[1]), 'equator'); dt = tag(abs(R.C[c]['Jupiter'][1] - v[1]), 'pair')
                    if e2 and dt:
                        der.append(f'{c} Jupiter–{c2} {b} Dec {abs(R.C[c]["Jupiter"][1] - v[1]):.5f} ({label(dt)}) from Equators {label(et)} and {label(e2)}')
            add(25, f'{c} Jupiter Equator {e:.5f} ({label(et)})' + ('; derived Dec strikes (not separate): ' + '; '.join(der) if der else ''),
                key=f'equator {c} Jupiter {label(et)}')

    # ---------- 27 return / contact; 28 RA AND Dec together
    for c in ('H', 'J'):
        v = R.pl('S Jupiter', f'{c} Jupiter')
        if v['RA'] < 0.3 and v['Dec'] < 1.2:
            add(27, f'return: S Jupiter on {c} Jupiter RA {v["RA"]:.4f} Dec {v["Dec"]:.4f}', key=f'return {c} Jupiter')
        for b, pos in R.C[c].items():
            if pos[2] != 'body':
                continue
            v = R.pl('S Jupiter', f'{c} {b}')
            if b != 'Jupiter' and contact(v['RA'], v['Dec']):
                add(27, f'contact: S Jupiter close to {c} {b} RA {v["RA"]:.4f} Dec {v["Dec"]:.4f}', key=f'contact S Jupiter->{c} {b}')
            t = tags_all(v, 'pair')
            if any(p == 'RA' for p, _, _ in t) and any(p == 'Dec' for p, _, _ in t):
                add(28, f'S Jupiter -> {c} {b} RA AND Dec: {tagstr(t)}', key=f'radec S Jupiter->{c} {b}')
        for Z in skyZ:
            if Z == 'Jupiter':
                continue
            v = R.pl(f'S {Z}', f'{c} Jupiter')
            if contact(v['RA'], v['Dec']):
                add(27, f'contact: S {Z} close to {c} Jupiter RA {v["RA"]:.4f} Dec {v["Dec"]:.4f}', key=f'contact S {Z}->{c} Jupiter')
            t = tags_all(v, 'pair')
            if any(p == 'RA' for p, _, _ in t) and any(p == 'Dec' for p, _, _ in t):
                add(28, f'S {Z} -> {c} Jupiter RA AND Dec: {tagstr(t)}', key=f'radec S {Z}->{c} Jupiter')

    # ---------- Jupiter movement (M) itself - listed for 31/32 and the field
    for c in ('H', 'J'):
        mv = R.moved(f'{c} Jupiter')
        if mv:
            add(6, f'{c} Jupiter moved {tagstr(mv)}', key=f'jupiter-moved {c}', sub='jupiter_moved')

    # ---------- ST stars
    for c in ('S', 'H', 'J'):
        for st, pos in R.C[c].items():
            if pos[2] != 'star':
                continue
            v = R.pl(f'{c} Jupiter', f'{c} {st}'); sb = star_band(v['RA'], v['Dec']); t = tags_all(v, 'pair')
            if sb:
                add('ST', f'{c} Jupiter {sb} {st} (own chart) RA {v["RA"]:.4f} Dec {v["Dec"]:.4f}', key=f'star {c} Jupiter {sb} {st}', star=st, on=sb)
            if t:
                add('ST', f'{c} Jupiter – {st} (own chart): {tagstr(t)}', key=f'starnum {c} Jupiter–{st}', star=st, nums=[label(x[2]) for x in t])
    # same star touched by Jupiter in two charts
    touch = {}
    for it in items:
        if it['m'] == 'ST':
            touch.setdefault(it['star'], set()).add(it['key'].split()[1])
    for st, cs in touch.items():
        if len(cs) >= 2:
            add('ST', f'{st} touched by Jupiter in {len(cs)} charts ({", ".join(sorted(cs))})', key=f'star-two-charts {st}', star=st)
    # sky Jupiter whole/ninth from a natal star that a natal Jupiter sits on
    for c in ('H', 'J'):
        for st, pos in R.C[c].items():
            if pos[2] == 'star':
                v = R.pl(f'{c} Jupiter', f'{c} {st}')
                if star_band(v['RA'], v['Dec']) == 'on':
                    t = tags_all(R.pl('S Jupiter', f'{c} {st}'), 'pair')
                    if t:
                        cp = tags_all(R.pl('S Jupiter', f'S {st}'), 'pair')
                        add('ST', f'S Jupiter -> {c} {st} (which {c} Jupiter is on): {tagstr(t)}' +
                            (f' — copies sky Jupiter–{st} ({tagstr(cp)})' if cp else ''), key=f'star-sky {c} {st}', star=st)
    # star at either end of a Jupiter link
    for l in links:
        for pt in (l['a'], l['b']):
            c = pt[0]
            for st, pos in R.C[c].items():
                if pos[2] == 'star':
                    v = planes(R.p(pt), pos)
                    if star_band(v['RA'], v['Dec']) == 'on':
                        add('ST', f"star at an end of {l['a']} – {l['b']}: {pt} on {st} RA {v['RA']:.4f} Dec {v['Dec']:.4f}",
                            key=f'star-end {pt} {st}', star=st)

    # ---------- 31 hub / 32 pair focus (kinds, after everything above)
    for jp in jup:
        c = jp[0]; kinds = set()
        if any(l['band'] == 'close' and jp in (l['a'], l['b']) for l in links): kinds.add('cross')
        if R.moved(jp): kinds.add('movement')
        if any(i['kind'] == 'skynat' and i['chart'] == c and i['band'] == 'tight' for i in L2): kinds.add('ratio')
        if sets: kinds.add('same body')
        if tag(abs(R.C[c]['Jupiter'][1]), 'equator') or any(i['kind'] == 'eq' and c in i['pair'] and i['band'] == 'tight' for i in L2): kinds.add('Equator')
        if any(i['kind'] == 'shared' for i in L2): kinds.add('shared')
        if any(it['m'] in (27, 28) and jp in it['text'] for it in items): kinds.add('position')
        if len(kinds) >= 3:
            add(31, f'hub {jp}: {len(kinds)} kinds — {", ".join(sorted(kinds))}', key=f'hub {jp}', kinds=sorted(kinds))
    focus = {}
    def lit(x, k):
        focus.setdefault(x, set()).add(k)
    for it in items:
        p = it.get('pair')
        if not p or 'Jupiter' not in p:
            continue
        x = p[1] if p[0] == 'Jupiter' else p[0]
        k = {1: 'cross', 2: 'struck', 3: 'partner', 4: 'sky', 5: 'moved', 6: 'moved', 7: 'cross', 9: 'struck', 10: 'struck', 14: 'shared'}.get(it['m'])
        if it['m'] == 1 and it.get('sub') == 'both_ends': k = 'struck'
        if k: lit(x, k)
    for i in L2:
        if i['kind'] == 'skynat' and i['band'] == 'tight': lit(i['x'], f"ratio {i['chart']}")
        if i['kind'] == 'shared': lit(i['x'], 'shared')
        if i['kind'] == 'pairset': lit(i['x'], 'set')
        if i['kind'] == 'hj' and i['band'] == 'tight': lit(i['x'], 'h:j')
        if i['kind'] == 'family' and i['band'] == 'tight': lit(i['x'], 'family')
    if sets: lit('Jupiter', 'same body')
    for x, ks in sorted(focus.items(), key=lambda kv: -len(kv[1])):
        add(32, f'pair Jupiter–{x}: {len(ks)} kind(s) — {", ".join(sorted(ks))}', key=f'focus Jupiter–{x}', nk=len(ks), kinds=sorted(ks))

    # ---------- 34/35 recurring (annotation)
    for x in focus:
        r = RECURRING.get(frozenset(['Jupiter', x]))
        if r:
            add(34, f'{r}: lit here by {", ".join(sorted(focus[x]))}', key=f'recurring Jupiter–{x}')
    for it in items:
        if it['m'] == 5 and it['key'] == 'both-moved H Eris–J Jupiter':
            add(35, 'recurring cross link H Eris – J Jupiter, both ends moved (Ziggy\'s Dream, Pixie Loc)', key='recurring H Eris–J Jupiter moved')
    return items


ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 'ST']


def main():
    race = sys.argv[1]
    sky, run = load_race(race)
    for P in sorted(run):
        L2 = json.load(open(f'docs/jupiter/{race}/layer2/{P}.json'))['items']
        items = runner_shapes(sky, run[P], L2)
        for i in L2:
            if 'key' not in i:
                i['key'] = {'eq': lambda i: f"eq-ratio {i['pair']} {i['ratio']}", 'set': lambda i: f"same-body {i['plane']}",
                            'skynat': lambda i: f"skynat {i['chart']} {i['pair']} {i['plane']} {i['ratio']}",
                            'hj': lambda i: f"hj {i['pair']} {i['plane']} {i['ratio']}", 'shared': lambda i: f"shared {i['pair']} {i['plane']}",
                            'pairset': lambda i: f"pairset {i['pair']} {i['plane']}",
                            'family': lambda i: f"family {i['chart']} {i['pair']} {i['plane']} {i['ratio']}"}[i['kind']](i)
        allit = items + L2
        dump(f'docs/jupiter/{race}/layer3/{P}.json', {'runner': run[P]['name'], 'jockey': run[P]['jockey'], 'items': allit})
        with open(f'docs/jupiter/{race}/layer3/{P}.txt', 'w') as fh:
            fh.write(f'{P} {run[P]["name"]} — Jupiter read, every measure (layer 3)\n')
            for m in ORDER:
                its = [i for i in allit if i['m'] == m]
                if its:
                    fh.write(f'\n[{m}]\n')
                    for i in its:
                        fh.write(f"  {i['text']}\n")
        print(P, run[P]['name'], len(allit), 'items')


if __name__ == '__main__':
    main()
