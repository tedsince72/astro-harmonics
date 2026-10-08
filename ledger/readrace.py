#!/usr/bin/env python3
"""
readrace.py v1.2 - one race laid out for a full-detail read, built from the raw positions
(Eddie, 3 Oct 2026 07:40: "ok, great - lets do that"; plan agreed 2 Oct 21:16-21:21).

Read set: the first three home + the favourite(s) when outside the first three, in full detail;
the rest of the field briefly so "alone" can be checked against everyone.

Everything is computed here from positions (sky_motion.py SKY3, Pxx_POS, NATAL_HOURLY) with the
engine's own family scoring (active_vibrations.py). Fast points set aside, the Moon KEPT (sky and natal;
a natal-Moon item is flagged '~m' because the birth time is unknown).

Held how, for every 80+ sky pair a/b (same words as the detail sheets):
  N  natal a - natal b            X  sky a -> natal b (or sky b -> natal a)      S  sky a -> natal a
  an item counts at >= 40 (the sheets' hit level), either coordinate; N in any family, X and S only in
  the sky pair's family (as sheet sections 4-6);
  ** = sky pair's family + coordinate, * = family, other coordinate.
  TYPE 1   two or more of N / X / S on one chart        NATAL PAIR   N on its own
  LANDS    both sky bodies on the same natal body C (sky a -> C or natal a -> C, and the same for b),
           in the sky pair's family + coordinate, each >= 60 (as sheet section 8)
  LINK     the pair touched on BOTH charts of the partnership
  INSIDE   = Type 1 or natal pair; ALONE = no other partnership holds the pair inside
Raw: every item shows its value in degrees, distance from the family target (dev), and for X/S/lands
whether it is Applying or Separating AT the off (2 minutes either side); items on a fast natal body show
'c' (scores at every hour of the birth day) or 'p' (only some hours) with the % of hours.
Star rule: a natal star sits where the sky star is, so 'sky planet -> natal star' copies the sky pair
for every runner [copy] and 'sky star -> natal planet' repeats the natal pair [=N]; both are shown but
not counted towards Type 1 / inside.
Repeats: any contact on the chart whose raw value equals a key sky number (top 3 + busiest pairs)
within 0.01 deg; '!!' = within 0.0003 deg (dead-exact).

v1.1 (Eddie, 3 Oct 08:05: "the natal natal must hold the imprint / ability, the transit holds the energy
at that moment, any repeats across these 2 charts must be significant; transit to natal of lesser
importance but must still show things"): IMPRINT <-> MOMENT section - every natal-natal distance on each
chart that repeats a sky-sky distance of the top 12 pairs (same coordinate, within 0.005 deg), the bodies
that carry two or more race numbers, numbers held on BOTH horse and jockey as well as in the sky, and
how many such repeats chance alone would give (shown so a count is not over-read).
v1.2 (Eddie, 3 Oct 08:09-08:11): NATAL HOTSPOTS - "the transit to natal may reflect how busy that natal
body is in the natal natal chart ... an energetic hotspot for that runner". For each chart, each natal body's
number of natal-natal relationships at three levels (>= 50, >= 70, >= 90 - Eddie: 90 may be too high, see
which level the highlighted bodies sit at), star-star pairs and the natal Moon left out; compared with the
same body across the field; and which sky contacts (landings, sky->natal on the top 12, race-number
repeats) reach each hotspot.
Usage: python3 readrace.py --race RACE [--out FILE]
"""
import argparse
import collections
import csv
import itertools
import os
import sys

sys.path.insert(0, '/home/claude/ds')
import active_vibrations as av

HERE = '/home/claude/ledger'
POS = f'{HERE}/allpos'
SKYD = f'{HERE}/sky'
OUT = f'{HERE}/out'
DETAIL_TEST = '/home/claude/blind/detail'
FAST = {'Ascendant', 'Midheaven', 'Vertex', 'Part_of_Fortune', 'Part_of_Spirit'}
STARS = av.FIXED_STARS
ROYAL = {'Aldebaran', 'Regulus', 'Antares', 'Fomalhaut'}
NODES = {'Ketu', 'Rahu'}
FASTNATAL = {'Sun', 'Moon', 'Mercury', 'Venus', 'Mars'}
FAMS = [n for n, _ in av.VIBRATION_FAMILIES]
FN = av._FAMILY_FN
PHI = (1 + 5 ** 0.5) / 2
SQ2 = 2 ** 0.5
SIL = 1 + SQ2
ITEM, LAND = 40.0, 60.0


def sep(p, q, mode):
    return av.angular_sep_ra(p[0], q[0]) if mode == 'RA' else av.angular_sep_dec(p[1], q[1])


def dev_deg(v, f):
    PP = [PHI ** p for p in (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)] + [10 * PHI ** p for p in (-1, 1, 2, 3, 4, 5, 6, 7)] + [100 * PHI ** p for p in (-1, 1)]
    if f == 'Whole Number':
        return abs(v - round(v))
    if f == 'Golden Ratio':
        m = v % PHI
        return min(m, PHI - m)
    if f == 'Phi Powers':
        return min(abs(v - t) for t in PP)
    if f == 'Ninths':
        return min(abs(v - t) for lo, hi, tol, t in av._NINTH_RANGES)
    if f == 'Sqrt2':
        m = v % SQ2
        return min(min(m, SQ2 - m), abs(v - 10 * SQ2), abs(v - 100 * SQ2))
    if f == 'Silver Ratio':
        m = v % SIL
        return min(min(m, SIL - m), abs(v - 10 * SIL))
    return v


def special(v):
    """name the clean number a sky distance sits on (within 0.003 deg), for the reader."""
    c = []
    k = round(v * 9)
    if k and abs(v - k / 9) < 0.003:
        c.append((abs(v - k / 9), f'{k // 9}' if k % 9 == 0 else f'{k}/9'))
    for p in range(-2, 12):
        for s, lab in ((1, ''), (10, '10'), (100, '100')):
            t = s * PHI ** p
            if abs(v - t) < 0.003:
                c.append((abs(v - t), f'{lab}φ^{p}' if p not in (1,) else f'{lab}φ'))
    for base, lab in ((SQ2, '√2'), (SIL, '(1+√2)'), (PHI, 'φ')):
        n = round(v / base)
        if n and abs(v - n * base) < 0.003:
            c.append((abs(v - n * base), f'{n}{lab}'))
    return min(c)[1] if c else ''


def clean(b):
    b = b.split('(')[0].strip()
    return {'PoF': 'Part_of_Fortune', 'PoS': 'Part_of_Spirit'}.get(b, b)


def short(b):
    return b + ('(R)' if b in ROYAL else '(s)' if b in STARS else '')


class Race:
    def __init__(self, R):
        self.R = R
        self.S3 = {}
        for r in csv.DictReader(open(f'{SKYD}/{R}__SKY3.csv')):
            self.S3[r['body']] = {k: (float(r[f'ra_{k}']), float(r[f'dec_{k}'])) for k in ('m30', 'm2', '0', 'p2', 'p30')}
        self.sky = {b: v['0'] for b, v in self.S3.items()}
        self.meta = []
        for r in csv.reader(open(f'{POS}/{R}__META.csv')):
            if r and len(r) > 3 and r[0].startswith('P') and r[0][1:].isdigit():
                self.meta.append({'tab': r[0], 'role': r[1], 'cloth': r[2], 'name': r[3]})
        self.mrow = {r[0]: r[1] for r in csv.reader(open(f'{POS}/{R}__META.csv')) if len(r) > 1}
        self.natal = {m['tab']: {r['body']: (float(r['ra']), float(r['dec'])) for r in csv.DictReader(open(f'{POS}/{R}__{m["tab"]}_POS.csv')) if r['ra']} for m in self.meta}
        self.hourly = collections.defaultdict(lambda: collections.defaultdict(list))
        f = f'{POS}/{R}__NATAL_HOURLY.csv'
        if os.path.exists(f):
            for r in csv.DictReader(open(f)):
                if r['ra'] and r['dec']:
                    self.hourly[r['tab']][r['body']].append((float(r['ra']), float(r['dec'])))
        self.charts = collections.defaultdict(dict)  # cloth -> {'H': tab, 'J': tab}
        for m in self.meta:
            self.charts[m['cloth']]['H' if m['role'] == 'horse' else 'J'] = m['tab']
        self.names = collections.defaultdict(list)
        for m in self.meta:
            self.names[m['cloth']].append(m['name'].split(' ', 1)[1] if m['name'].split(' ', 1)[0] == m['cloth'] else m['name'])
        self.load_sky()

    def load_sky(self):
        rows = list(csv.DictReader(open(f'{OUT}/{self.R}__SKY.csv')))
        self.pairs = {}  # (a,b) -> dict(rank, best, entries=[(mode, fam, score, value, dev, motion, m30, p30)])
        for r in rows:
            if not r['rank80']:
                continue
            k = (r['a'], r['b'])
            d = self.pairs.setdefault(k, dict(rank=int(r['rank80']), best=float(r['pair_best']), entries=[]))
            if float(r['best_score']) >= 80:
                d['entries'].append((r['mode'], r['best_family'], float(r['best_score']), float(r['value']), float(r['dev_deg']), r['motion'],
                                     float(r['score_m30']), float(r['score_p30'])))
        cnt = collections.Counter()
        for a, b in self.pairs:
            cnt[a] += 1
            cnt[b] += 1
        self.count = cnt
        top = max(cnt.values())
        self.busiest = sorted(b for b, c in cnt.items() if c == top)
        nxt = sorted(set(cnt.values()), reverse=True)
        self.next = sorted(b for b, c in cnt.items() if len(nxt) > 1 and c == nxt[1]) if len(self.busiest) == 1 else []
        self.byrank = sorted(self.pairs, key=lambda k: self.pairs[k]['rank'])
        cnm = collections.Counter()
        for a, b in self.pairs:
            if 'Moon' not in (a, b):
                cnm[a] += 1
                cnm[b] += 1
        self.count_nm = cnm
        topn = max(cnm.values())
        self.busiest_nm = sorted(b for b, c in cnm.items() if c == topn)
        # BUSY = busiest with the Moon kept (Eddie 2 Oct) OR without the Moon (the definition used in the T25-T48 reads)
        self.busy = set(self.busiest) | set(self.busiest_nm)

    # ---------- held how
    def items_for(self, tab, a, b):
        """N/X/S items (best family per coordinate, >= ITEM) for sky pair a/b on one chart."""
        P = self.natal[tab]
        ents = self.pairs[(a, b)]['entries']
        fams = {(e[0], e[1]) for e in ents}
        famset = {e[1] for e in ents}
        out = []
        cands = [('N', a, b), ('X', a, b), ('X', b, a), ('S', a, a), ('S', b, b)]
        for kind, s, n in cands:
            if s in STARS and n in STARS:
                continue
            if kind == 'N' and (s not in P or n not in P):
                continue
            if kind != 'N' and (s not in self.sky or n not in P):
                continue
            for mode in ('RA', 'Dec'):
                if kind == 'N' and mode == 'RA' and {s, n} == NODES:
                    continue
                v = sep(P[s], P[n], mode) if kind == 'N' else sep(self.sky[s], P[n], mode)
                # as the sheets: a natal pair counts in any family; X and S only in the sky pair's family
                sc = {f: (FN[f](v, mode) if kind == 'N' or f in famset else 0.0) for f in FAMS}
                f = max(FAMS, key=lambda k: sc[k])
                if sc[f] < ITEM:
                    continue
                mark = '**' if (mode, f) in fams else '*' if f in famset else ''
                it = self.item(tab, kind, s, n, mode, v, f, sc[f], mark)
                # a natal star sits where the sky star is: sky planet -> natal star copies the sky pair for
                # every runner; sky star -> natal planet repeats the natal pair. Shown, not counted.
                if kind == 'X' and n in STARS:
                    it['flag'] = 'copy'
                elif kind == 'X' and s in STARS:
                    it['flag'] = '=N'
                out.append(it)
        return out

    def item(self, tab, kind, s, n, mode, v, f, score, mark):
        d = dict(kind=kind, s=s, n=n, mode=mode, v=v, f=f, score=score, mark=mark, dev=dev_deg(v, f), mv='', cert='')
        if kind in ('X', 'S', 'TN'):
            P = self.natal[tab]
            dm = dev_deg(sep(self.S3[s]['m2'], P[n], mode), f)
            dp = dev_deg(sep(self.S3[s]['p2'], P[n], mode), f)
            d['mv'] = 'A' if dp < dm - 1e-9 else 'S' if dp > dm + 1e-9 else ''
        fastb = [x for x in ((s, n) if kind in ('N', 'NN') else (n,)) if x in FASTNATAL]
        if fastb:
            H = self.hourly.get(tab, {})
            if kind in ('N', 'NN'):
                P0 = self.natal[tab]
                A, B = H.get(s), H.get(n)
                if A and not B:
                    B = [P0[n]] * len(A)
                if B and not A:
                    A = [P0[s]] * len(B)
                vals = [sep(p, q, mode) for p, q in zip(A, B)] if A and B else []
            else:
                B = H.get(n)
                vals = [sep(self.sky[s], q, mode) for q in B] if B else []
            if vals:
                ok = sum(FN[f](x, mode) >= ITEM for x in vals) / len(vals)
                d['cert'] = ('c' if ok == 1 else f'p{round(100 * ok)}%') + ('~m' if 'Moon' in fastb else '')
        return d

    def lands_for(self, tab, a, b):
        P = self.natal[tab]
        out = []
        for mode, f, score, *_ in self.pairs[(a, b)]['entries']:
            for C in P:
                if C in (a, b) or C in STARS and (a in STARS or b in STARS):
                    continue
                legs = []
                for s in (a, b):
                    best = None
                    if s in self.sky and not (s in STARS and C in STARS):
                        v = sep(self.sky[s], P[C], mode)
                        sc = FN[f](v, mode)
                        if sc >= LAND:
                            best = self.item(tab, 'TN', s, C, mode, v, f, sc, '**')
                    if s in P and not (s in STARS and C in STARS) and not (mode == 'RA' and {s, C} == NODES):
                        v = sep(P[s], P[C], mode)
                        sc = FN[f](v, mode)
                        if sc >= LAND and (best is None or sc > best['score']):
                            best = self.item(tab, 'NN', s, C, mode, v, f, sc, '**')
                    legs.append(best)
                if all(legs):
                    out.append(dict(C=C, mode=mode, f=f, legs=legs))
        return out

    def build(self):
        self.hold = collections.defaultdict(dict)    # cloth -> (a,b) -> {'H': items, 'J': items}
        self.land = collections.defaultdict(dict)    # cloth -> (a,b) -> {'H': lands, 'J': lands}
        for cloth, ch in self.charts.items():
            for k in self.byrank:
                for side, tab in ch.items():
                    it = self.items_for(tab, *k)
                    if it:
                        self.hold[cloth].setdefault(k, {})[side] = it
                    ld = self.lands_for(tab, *k)
                    if ld:
                        self.land[cloth].setdefault(k, {})[side] = ld
        self.inside = collections.defaultdict(set)   # (a,b) -> cloths holding inside (T1 or NP)
        for cloth in self.charts:
            for k, sides in self.hold[cloth].items():
                for side, it in sides.items():
                    if self.how(it):
                        self.inside[k].add(cloth)

    @staticmethod
    def how(items):
        # natal Moon: birth time unknown - an item on it counts only if it scores at every hour ('c')
        items = [i for i in items if not i.get('flag') and not (i['cert'].endswith('~m') and not i['cert'].startswith('c'))]
        kinds = {i['kind'] for i in items}
        if len(kinds) >= 2 or sum(1 for i in items if i['kind'] in ('X', 'S')) >= 2:
            return 'T1'
        if 'N' in kinds:
            return 'NP'
        return ''


def fmt_item(i):
    arrow = '–' if i['kind'] in ('N', 'NN') else '→'
    lab = {'N': 'N', 'X': 'X', 'S': 'S', 'TN': 'sky', 'NN': 'natal'}[i['kind']]
    if i['kind'] == 'S':
        body = f"{short(i['s'])} self"
    else:
        body = f"{short(i['s'])}{arrow}{short(i['n'])}"
    extra = ' '.join(x for x in (i['mv'], i['cert'], f"[{i['flag']}]" if i.get('flag') else '') if x)
    return f"{lab} {body} {i['mode']} {i['v']:.4f} {i['f']} {i['score']:.0f}{i['mark']} dev {i['dev']:.4f}" + (f' {extra}' if extra else '')


def results(R):
    res = {}
    for f in ('/home/claude/reads/profiles.csv', '/home/claude/scored/profiles_test_scored.csv'):
        for r in csv.DictReader(open(f)):
            if r['race'] == R:
                res[r['cloth']] = r
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--race', required=True)
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    R = a.race
    rc = Race(R)
    rc.build()
    res = results(R)
    sur = {r['race']: r for r in csv.DictReader(open(f'{HERE}/surprise_96.csv'))}[R]
    L = []
    p = L.append
    p(f"{sur['label']}  {R}  ({rc.mrow.get('race_local_time', '')})   surprise #{sur['order']} of 96, winner/fav odds ×{sur['ratio']}")
    fin = sorted(res.values(), key=lambda r: (not r['finish'].isdigit(), int(r['finish']) if r['finish'].isdigit() else 99))
    p('RESULT: ' + ' · '.join(f"{r['finish']} {r['partnership'].split('  /')[0]} {r['sp']}" for r in fin))
    # ---------- sky
    p('')
    p(f"SKY – busiest (80+ pairs, fast points aside, Moon kept): {', '.join(f'{b} {rc.count[b]}' for b in rc.busiest)}"
      + (f"; next {', '.join(f'{b} {rc.count[b]}' for b in rc.next)}" if rc.next else '')
      + f" | without the Moon: {', '.join(f'{b} {rc.count_nm[b]}' for b in rc.busiest_nm)}   (BUSY = either)")
    busy_pairs = [k for k in rc.byrank if set(k) & rc.busy]
    show = rc.byrank[:12] + [k for k in busy_pairs if k not in rc.byrank[:12]][:6]
    for k in show:
        d = rc.pairs[k]
        tags = []
        if set(k) & rc.busy:
            tags.append('BUSY')
        elif set(k) & set(rc.next):
            tags.append('next')
        if set(k) & ROYAL:
            tags.append('royal')
        ents = '; '.join(f"{m} {v:.4f} {f} {s:.1f} dev {dv:.4f}" + (f" ={special(v)}" if special(v) else '') + f" {mv or '-'} ({m30:.0f}→{p30:.0f})"
                         for m, f, s, v, dv, mv, m30, p30 in d['entries'])
        holders = len(rc.inside[k])
        p(f"  #{d['rank']:<3} {short(k[0])}/{short(k[1])}  {ents}  [{' '.join(tags)}] inside: {holders}")
    # ---------- read set
    keyset = list(dict.fromkeys(rc.byrank[:3] + busy_pairs[:3]))
    keynums = []
    for k in keyset:
        for m, f, s, v, *_ in rc.pairs[k]['entries']:
            keynums.append((f"#{rc.pairs[k]['rank']} {k[0]}/{k[1]}", v, m))
    def odds(r):
        t = r['sp'].strip().rstrip('FJC').strip()
        return 1.0 if t.lower() in ('evens', 'evs') else float(t.split('/')[0]) / float(t.split('/')[1])
    lo = min(odds(r) for r in res.values())
    favs = [c for c, r in res.items() if abs(odds(r) - lo) < 1e-9]   # joint favourites both in the read set
    top3 = [r['cloth'] for r in fin[:3]]
    readset = top3 + [c for c in favs if c not in top3]
    land_counts = {c: sum(len(ls) for k in rc.land[c] for ls in rc.land[c][k].values()) for c in rc.charts}
    med = sorted(land_counts.values())[len(land_counts) // 2]
    p('')
    p(f"landings per runner: {', '.join(f'{c}:{n}' for c, n in sorted(land_counts.items(), key=lambda x: int(x[0])))} (median {med})")
    for c in readset:
        r = res.get(c, {})
        p('')
        p(f"=== {r.get('finish', '?')}  {c} {' / '.join(rc.names[c])}  {r.get('sp', '')}{'  FAV' if c in favs else ''}  – landings {land_counts[c]}")
        ks = sorted(set(rc.hold[c]) | set(rc.land[c]), key=lambda k: rc.pairs[k]['rank'])
        for k in ks:
            d = rc.pairs[k]
            sides = rc.hold[c].get(k, {})
            hows = {sd: rc.how(it) for sd, it in sides.items()}
            inside = any(hows.values())
            lands = rc.land[c].get(k, {})
            interesting = d['rank'] <= 12 or set(k) & rc.busy or (inside and c in rc.inside[k] and len(rc.inside[k]) == 1)
            if not interesting or not (inside or lands or len(sides) == 2):
                continue
            others = len(rc.inside[k] - {c})
            tag = []
            if set(k) & rc.busy:
                tag.append('BUSY')
            if set(k) & ROYAL:
                tag.append('royal')
            if inside:
                tag.append('ALONE' if others == 0 else f'shared({others})')
            if len(sides) == 2:
                tag.append('link')
            p(f"  #{d['rank']} {short(k[0])}/{short(k[1])} {d['best']:.1f}  [{' '.join(tag)}]")
            for sd in ('H', 'J'):
                if sd in sides:
                    p(f"      {sd} {hows[sd] or 'touch'}: " + ' | '.join(fmt_item(i) for i in sides[sd]))
            for sd in ('H', 'J'):
                for ld in lands.get(sd, []):
                    others_l = sum(1 for cc in rc.charts if cc != c and any(x['C'] == ld['C'] for xs in rc.land[cc].get(k, {}).values() for x in xs))
                    p(f"      {sd} LANDS on {short(ld['C'])}: " + ' & '.join(fmt_item(i) for i in ld['legs']) + (f'  shared({others_l})' if others_l else '  alone'))
        # receiving bodies
        recv = collections.defaultdict(list)
        for k, sides in rc.land[c].items():
            for sd, ls in sides.items():
                for ld in ls:
                    recv[(sd, ld['C'])].append(k)
        rb = sorted(recv.items(), key=lambda kv: -len(kv[1]))
        if rb and len(rb[0][1]) >= 2:
            p('  RECEIVERS: ' + '; '.join(f"{sd} {C} ×{len(ks)} (" + ', '.join(f"#{rc.pairs[k]['rank']}{'B' if set(k) & rc.busy else ''}" for k in sorted(ks, key=lambda k: rc.pairs[k]['rank'])) + ')'
                                       for (sd, C), ks in rb if len(ks) >= 2))
        # repeats of key numbers
        reps = []
        for sd, tab in rc.charts[c].items():
            P = rc.natal[tab]
            for lab, val, mode in keynums:
                for x, y in itertools.combinations(sorted(P), 2):
                    if x in STARS and y in STARS:
                        continue
                    v = sep(P[x], P[y], mode)
                    if abs(v - val) <= 0.01:
                        reps.append((abs(v - val), f"{sd} natal {x}–{y} {mode} {v:.4f} ({v - val:+.4f}) = {lab}" + (' star' if {x, y} & STARS else '')))
                for s in rc.sky:
                    if s in FAST:
                        continue
                    for y in P:
                        if y in STARS:
                            continue
                        v = sep(rc.sky[s], P[y], mode)
                        if abs(v - val) <= 0.01:
                            dm = abs(sep(rc.S3[s]['m2'], P[y], mode) - val)
                            dp = abs(sep(rc.S3[s]['p2'], P[y], mode) - val)
                            reps.append((abs(v - val), f"{sd} sky {s}→natal {y} {mode} {v:.4f} ({v - val:+.4f}) {'A' if dp < dm else 'S'} = {lab}" + (' star' if s in STARS else '')))
        reps.sort()
        if reps:
            p('  REPEATS: ' + ' | '.join(('!! ' if d <= 0.0003 else '') + t for d, t in reps[:8]) + (f' (+{len(reps) - 8} more)' if len(reps) > 8 else ''))
    # ---------- natal hotspots
    LEV = (50, 70, 90)
    hot = {}
    for c in rc.charts:
        for sd, tab in rc.charts[c].items():
            P = rc.natal[tab]
            cnt = {b: [0, 0, 0] for b in P if b not in STARS and b != 'Moon'}
            for x, y in itertools.combinations(sorted(P), 2):
                if (x in STARS and y in STARS) or 'Moon' in (x, y):
                    continue
                for m in ('RA', 'Dec'):
                    if m == 'RA' and {x, y} == NODES:
                        continue
                    v = sep(P[x], P[y], m)
                    sc = max(FN[f](v, m) for f in FAMS)
                    for i, lv in enumerate(LEV):
                        if sc >= lv:
                            for b in (x, y):
                                if b in cnt:
                                    cnt[b][i] += 1
            hot[(c, sd)] = cnt
    fieldavg = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    nch = len(hot)
    for cnt in hot.values():
        for b, v in cnt.items():
            for i in range(3):
                fieldavg[b][i] += v[i] / nch
    def touches(c, sd, b):
        t = []
        for k, sides in rc.land[c].items():
            for ld in sides.get(sd, []):
                if ld['C'] == b:
                    mv = ''.join(l['mv'] or 'n' for l in ld['legs'])
                    t.append(f"lands #{rc.pairs[k]['rank']}{'B' if set(k) & rc.busy else ''} {mv}")
        tab = rc.charts[c][sd]
        for k in rc.byrank[:12]:
            for s_ in k:
                if s_ in rc.sky and b in rc.natal[tab] and s_ != b:
                    for m in ('RA', 'Dec'):
                        v = sep(rc.sky[s_], rc.natal[tab][b], m)
                        f = max(FAMS, key=lambda ff: FN[ff](v, m))
                        if FN[f](v, m) >= 80 and not (s_ in STARS):
                            t.append(f"sky {s_}→ {m} {f} {FN[f](v, m):.0f}")
        return sorted(set(t))
    p('')
    p('NATAL HOTSPOTS – natal–natal relationships per body at >=50 / >=70 / >=90 (field average for that body in brackets); what the sky does to it')
    for c in readset:
        r = res.get(c, {})
        p(f"  {r.get('finish', '?')} {c} {' / '.join(rc.names[c])} {r.get('sp', '')}")
        for sd in ('H', 'J'):
            if (c, sd) not in hot:
                continue
            cnt = hot[(c, sd)]
            # rank by count at >= 70, then >= 90
            top = sorted(cnt, key=lambda b: (-cnt[b][1], -cnt[b][2], -cnt[b][0]))[:6]
            parts = []
            for b in top:
                fa = fieldavg[b]
                tt = touches(c, sd, b)
                parts.append(f"{b} {cnt[b][0]}/{cnt[b][1]}/{cnt[b][2]} ({fa[0]:.0f}/{fa[1]:.0f}/{fa[2]:.1f})" + (f" ← {'; '.join(tt)}" if tt else ''))
            p(f"    {sd}: " + ' | '.join(parts))
    # ---------- imprint <-> moment
    TOL = 0.005
    top12 = rc.byrank[:12]
    skyvals = []
    for k in top12:
        for m in ('RA', 'Dec'):
            v = sep(rc.sky[k[0]], rc.sky[k[1]], m)
            sc = max(FN[f](v, m) for f in FAMS)
            if sc >= 80:
                skyvals.append((rc.pairs[k]['rank'], k, m, v))
    # sky pairs sitting on the same number (e.g. #1 and #5 both 160/9) are one race number
    numid = {}
    for rk, k, m, v in sorted(skyvals, key=lambda t: t[3]):
        hit = [n for (m2, v2), n in numid.items() if m2 == m and abs(v2 - v) <= 0.01]
        numid[(m, v)] = hit[0] if hit else f"{m} {v:.3f}"
    rk_num = {rk: numid[(m, v)] for rk, k, m, v in skyvals}
    def natal_vals(tab):
        P = rc.natal[tab]
        H = rc.hourly.get(tab, {})
        out = []
        for x, y in itertools.combinations(sorted(P), 2):
            if x in STARS and y in STARS:
                continue
            for m in ('RA', 'Dec'):
                if m == 'RA' and {x, y} == NODES:
                    continue
                out.append((x, y, m, sep(P[x], P[y], m)))
        return out
    imp = {}
    nvals_n = 0
    for c in rc.charts:
        imp[c] = []
        for sd, tab in rc.charts[c].items():
            nv = natal_vals(tab)
            nvals_n = max(nvals_n, len(nv))
            for x, y, m, v in nv:
                for rk, k, sm, sv in skyvals:
                    if sm == m and abs(v - sv) <= TOL:
                        fastb = [b for b in (x, y) if b in FASTNATAL]
                        unc = ''
                        if fastb:
                            Hh = rc.hourly.get(tab, {})
                            A = Hh.get(x) or [rc.natal[tab][x]] * 25
                            B = Hh.get(y) or [rc.natal[tab][y]] * 25
                            vals = [sep(p, q, m) for p, q in zip(A, B)]
                            unc = f' (moves {max(vals) - min(vals):.2f} over the birth day{" – Moon" if "Moon" in fastb else ""})'
                        imp[c].append(dict(sd=sd, x=x, y=y, m=m, v=v, rk=rk, k=k, d=v - sv, same=set(k) == {x, y}, unc=unc))
    # chance: values per chart x sky values x window / spread of values
    per_sky = {m: sum(1 for s in skyvals if s[2] == m) for m in ('RA', 'Dec')}
    exp = (nvals_n / 2) * (per_sky['RA'] * 2 * TOL / 180 + per_sky['Dec'] * 2 * TOL / 60)
    p('')
    p(f"IMPRINT ↔ MOMENT – natal–natal distances repeating a top-12 sky distance (same coordinate, ±{TOL}°); chance ≈ {exp:.1f} per chart")
    for c in sorted(rc.charts, key=lambda x: (x not in readset, int(x))):
        r = res.get(c, {})
        L_ = sorted(imp[c], key=lambda d: (d['rk'], abs(d['d'])))
        bod = collections.defaultdict(set)
        for d in L_:
            if not d['unc'] or 'Moon' not in d['unc']:
                for b in (d['x'], d['y']):
                    if b not in STARS:
                        bod[(d['sd'], b)].add(d['rk'])
        multi = {kb: rks for kb, rks in bod.items() if len({rk_num[x] for x in rks}) >= 2}
        # the same natal body carrying race numbers on BOTH charts (horse and jockey)
        hb = {b for (sd, b) in bod if sd == 'H'}
        jb = {b for (sd, b) in bod if sd == 'J'}
        cross = sorted(b for b in hb & jb if len({rk_num[x] for x in bod[('H', b)] | bod[('J', b)]}) >= 1)
        distinct = {(d['sd'], d['x'], d['y'], d['m'], rk_num[d['rk']]) for d in L_}
        sides = {d['sd'] for d in L_}
        both = sorted({d['rk'] for d in L_ if d['sd'] == 'H'} & {d['rk'] for d in L_ if d['sd'] == 'J'})
        p(f"  {r.get('finish', '?'):>3} {c} {' / '.join(rc.names[c])} {r.get('sp', '')}: {sum(1 for x in distinct if x[0] == 'H')} horse, {sum(1 for x in distinct if x[0] == 'J')} jockey (distinct numbers)"
          + (f" | same body on BOTH charts: {', '.join(b + ' (' + ', '.join('#' + str(x) for x in sorted(bod[('H', b)] | bod[('J', b)])) + ')' for b in cross)}" if cross else '')
          + (f" | same number on BOTH charts: {', '.join('#' + str(x) for x in both)}" if both else '')
          + (f" | one body carrying 2+ different race numbers: {'; '.join(f'{sd} {b} (' + ', '.join('#' + str(x) for x in sorted(rks)) + ')' for (sd, b), rks in multi.items())}" if multi else ''))
        if c in readset:
            for d in L_:
                p(f"      #{d['rk']} {d['k'][0]}/{d['k'][1]} {d['m']}: {d['sd']} natal {short(d['x'])}–{short(d['y'])} {d['v']:.4f} ({d['d']:+.4f})"
                  + (' SAME BODIES' if d['same'] else '') + d['unc'])
    # ---------- rest of field
    p('')
    p('REST OF FIELD (pairs in the top 12 or on the busiest body held INSIDE; ALONE marked)')
    for c in sorted(rc.charts, key=lambda x: int(x)):
        if c in readset:
            continue
        r = res.get(c, {})
        held = []
        for k in rc.byrank:
            if c in rc.inside[k] and (rc.pairs[k]['rank'] <= 12 or set(k) & rc.busy):
                held.append(f"#{rc.pairs[k]['rank']}{'B' if set(k) & rc.busy else ''}{' ALONE' if len(rc.inside[k]) == 1 else ''}")
        p(f"  {r.get('finish', '?'):>3} {c} {' / '.join(rc.names[c])} {r.get('sp', '')} – landings {land_counts[c]}; inside: {', '.join(held) or '-'}")
    # ---------- checklist
    p('')
    p('CHECKLIST (take-stock lines, 2 Oct)')
    for c in readset:
        r = res.get(c, {})
        alone_key = [k for k in rc.byrank if rc.inside[k] == {c} and (rc.pairs[k]['rank'] <= 3 or set(k) & rc.busy)]
        t1s = [rc.pairs[k]['best'] for k in rc.hold[c] for it in rc.hold[c][k].values() if rc.how(it) == 'T1' and c in rc.inside[k]]
        own_t1 = [rc.pairs[k]['best'] for k in rc.hold[c] for it in rc.hold[c][k].values() if rc.how(it) == 'T1' and rc.inside[k] == {c}]
        key_inside = [k for k in rc.byrank if c in rc.inside[k] and (rc.pairs[k]['rank'] <= 3 or set(k) & rc.busy)]
        all_shared = key_inside and all(len(rc.inside[k]) > 1 for k in key_inside)
        recvB = collections.Counter()
        for k, sides in rc.land[c].items():
            if set(k) & rc.busy:
                for ls in sides.values():
                    for ld in ls:
                        recvB[ld['C']] += 1
        own = f"{len(own_t1)} (best {max(own_t1):.1f})" if own_t1 else 'none'
        p(f"  {r.get('finish', '?')} {c} {rc.names[c][0]}: (1) top-3/busy pair inside ALONE: "
          + (', '.join(f"#{rc.pairs[k]['rank']} {k[0]}/{k[1]}" for k in alone_key) or 'no')
          + f"; quiet {'yes' if land_counts[c] <= med else 'no'} ({land_counts[c]} vs {med}) | (3) own Type 1s held alone: {own}")
        p(f"        key holdings inside: {len(key_inside)}{' – ALL SHARED' if all_shared else ''}; (4) busy-body pairs received: "
          + (', '.join(f'{C} ×{n}' for C, n in recvB.most_common(3)) or 'none'))
    txt = '\n'.join(L) + '\n'
    if a.out:
        open(a.out, 'w').write(txt)
    print(txt)


if __name__ == '__main__':
    main()
