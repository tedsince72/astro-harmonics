#!/usr/bin/env python3
"""Depth ladder (Eddie, 15 Nov 2026): how far each runner's chains go, body by body. Data only - no pick, no score cut-off.

Usage:  python3 tools/eddie_depth.py <race>_bybody.xlsx [--out DIR]   (default DIR docs/eddie_read/depth)
        -> DIR/<race>_depth.md and DIR/<race>_depth.json

Reads the bybody workbook only (tools/eddie_bybody.py output). Never a csv, never a result.
Steps fixed 15 Nov 2026, before any race outside the three origin races was read with it. Per runner, per body X; each step needs
the one before (a ladder); Moon never counts (pair end or repeat); a conjunction / contraparallel target never counts as a repeat.
  0  a same-body line S X -> H X or S X -> J X scores (has a family; conj / contraparallel included).
  1  a sky pair S A - S B on that line's target ('Sky lines on the same target'), A and B not X, not the Moon.
  2  one end of that pair is also on X: S E - S X, S E -> H X or S E -> J X (any plane, any score).
  3  the other end is on X too (the loop closes).
  4  a further line on X (another sky body Y, not A, B, X, the Moon: S Y - S X / S Y -> H X / J X; or a natal royal star line
     on X) repeats a family + target already in the loop (the same-body line, the pair, the two ends' lines). The Sun counts.
  5  a second loop on X: another step-3 loop (a different pair, or the other chart's same-body line), or a royal-star loop
     (a royal star R on sky X, S R - S X, and R's natal line on X in either chart with a family or with a same-body /
     crossed ratio on a target).
A body's depth = the highest step it reaches. Per runner: the deepest body (all bodies at it), and the count of bodies at
3 or more. Field lines: who reaches the race's top step ('only' / 'also'), and per step how many runners reach it.
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eddie_bybody_rules as E  # noqa: E402

CJ = ('conj', 'contraparallel')


def _ends_on(b, e):
    """Lines putting sky body e on X: S e - S X, S e -> H X, S e -> J X."""
    return b.sky_y(e) + b.to_natal(e, 'H') + b.to_natal(e, 'J')


def _ft(r):
    return (r['fam'], r['tgt'])


def _loops(b):
    """Every step-1..3 chain on body X: list of dicts (chart, line, pair, ends, step, cells)."""
    out = []
    for c in 'HJ':
        for sb in b.same_body(c):
            for s, A, B in b.pairs_on(sb):
                if b.X in (A, B) or 'Moon' in (A, B):
                    continue
                la, lb = _ends_on(b, A), _ends_on(b, B)
                step = 3 if la and lb else 2 if la or lb else 1
                out.append({'chart': c, 'sb': sb, 'pair': s, 'A': A, 'B': B, 'la': la, 'lb': lb, 'step': step})
    return out


def _repeats(b, lp):
    """Step 4: lines on X (not the loop's own points) on a family + target already in the loop."""
    loop_cells = [lp['sb'], lp['pair']] + lp['la'] + lp['lb']
    keys = {_ft(r) for r in loop_cells if r['fam'] and r['fam'] not in CJ}
    used = {b.X, lp['A'], lp['B'], 'Moon'}
    seen = {(r['line'], r['plane']) for r in loop_cells}
    out = []
    for o in b.O:
        m = re.match(r'S (.+?) (?:–|→) ', o['line'])
        if not m or m.group(1) in used or (o['line'], o['plane']) in seen:
            continue
        if o['fam'] not in CJ and _ft(o) in keys:
            out.append(o)
    for _, R, r in b.star_rows(scoring=True):
        if (r['line'], r['plane']) not in seen and r['fam'] not in CJ and _ft(r) in keys:
            out.append(r)
    return out


def _royal_loops(b):
    out = []
    for R in E.ROY:
        sky = b.sky_y(R)
        if not sky:
            continue
        nat = [r for c in 'HJ' for r in b.lines(f'{c} {R} – {c} {b.X}')
               if r['fam'] or (E.num(r.get('rs')) and r.get('rt') not in (None, 'no target'))
               or (E.num(r.get('xs')) and r.get('xt') not in (None, 'no target'))]
        if nat:
            out.append({'R': R, 'sky': sky, 'nat': nat})
    return out


def body_depth(b):
    """(depth, detail) for one body."""
    if not (b.same_body('H') or b.same_body('J')):
        return -1, {}
    loops = _loops(b)
    if not loops:
        return 0, {'lines': b.same_body('H') + b.same_body('J')}
    best = max(lp['step'] for lp in loops)
    if best < 3:
        lp = max(loops, key=lambda x: x['step'])
        return best, {'loop': lp}
    closed = [lp for lp in loops if lp['step'] == 3]
    rep = [(lp, _repeats(b, lp)) for lp in closed]
    rep4 = [(lp, r) for lp, r in rep if r]
    if not rep4:
        return 3, {'loop': closed[0], 'loops': closed}
    roy = _royal_loops(b)
    second = len({(lp['chart'], lp['pair']['line'], lp['pair']['plane']) for lp in closed}) >= 2
    if second or roy:
        return 5, {'loop': rep4[0][0], 'repeat': rep4[0][1], 'loops': closed, 'royal': roy}
    return 4, {'loop': rep4[0][0], 'repeat': rep4[0][1], 'loops': closed}


def _txt_loop(lp):
    t = [f"{E.cell(lp['sb'])}", f"pair {E.cell(lp['pair'])}"]
    for e, ls in ((lp['A'], lp['la']), (lp['B'], lp['lb'])):
        if ls:
            t.append(f'{e} on X: ' + '; '.join(E.cell(r) for r in ls))
    return t


def describe(depth, d):
    out = []
    if depth <= 0:
        return out
    out += _txt_loop(d['loop'])
    if depth >= 4:
        out.append('repeat: ' + '; '.join(E.cell(r) for r in d['repeat']))
    if depth >= 5:
        k0 = (d['loop']['chart'], d['loop']['pair']['line'], d['loop']['pair']['plane'])
        seen = {k0}
        for lp in d['loops']:
            k = (lp['chart'], lp['pair']['line'], lp['pair']['plane'])
            if k in seen:
                continue
            seen.add(k)
            out.append('second loop: ' + ' | '.join(_txt_loop(lp)))
        for rl in d['royal']:
            out.append(f"royal loop {rl['R']}: " + '; '.join(E.cell(r) for r in rl['sky']) + ' | ' +
                       '; '.join(E.cell(r) + (f" [{E.ratio_txt(r, 'same')}]" if E.num(r.get('rs')) and r.get('rt') not in (None, 'no target') else '')
                                 + (f" [{E.ratio_txt(r, 'crossed')}]" if E.num(r.get('xs')) and r.get('xt') not in (None, 'no target') else '')
                                 for r in rl['nat']))
    return out


def run(path):
    data = E.load(path)
    race = os.path.basename(path).replace('_bybody.xlsx', '')
    runners = []
    for run_, D in data.items():
        bodies = []
        for X, d in D.items():
            dep, det = body_depth(E.Body(X, d))
            if dep >= 0:
                bodies.append({'body': X, 'depth': dep, 'cells': describe(dep, det)})
        top = max((x['depth'] for x in bodies), default=-1)
        runners.append({'runner': run_, 'top': top, 'top_bodies': [x['body'] for x in bodies if x['depth'] == top],
                        'n3': sum(1 for x in bodies if x['depth'] >= 3), 'bodies': bodies})
    race_top = max((r['top'] for r in runners), default=-1)
    per_step = {k: sorted(r['runner'] for r in runners if r['top'] >= k) for k in range(6)}
    return {'race': race, 'race_top': race_top, 'at_top': [r['runner'] for r in runners if r['top'] == race_top],
            'per_step': per_step, 'runners': runners}


def write(res, out):
    os.makedirs(out, exist_ok=True)
    base = os.path.join(out, res['race'] + '_depth')
    with open(base + '.json', 'w') as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    L = [f"# Depth ladder — {res['race']}", '', '```', __doc__[__doc__.index('Steps fixed'):].rstrip(), '```', '',
         '## Field', '']
    at = res['at_top']
    L.append(f"Top step in the race: {res['race_top']} — " + (f"{at[0]} only" if len(at) == 1 else 'also: ' + ', '.join(at)))
    for k in range(6):
        L.append(f"- step {k}+: {len(res['per_step'][k])} of {len(res['runners'])}")
    L += ['', '| runner | deepest | bodies at the deepest | bodies at 3+ |', '|---|---|---|---|']
    for r in res['runners']:
        L.append(f"| {r['runner']} | {r['top']} | {', '.join(r['top_bodies'])} | {r['n3']} |")
    L.append('')
    for r in res['runners']:
        L += [f"## {r['runner']}", '']
        for x in sorted(r['bodies'], key=lambda x: -x['depth']):
            if x['depth'] < 3:
                continue
            others = [q['runner'] for q in res['runners'] if q is not r and any(y['body'] == x['body'] and y['depth'] >= x['depth'] for y in q['bodies'])]
            L.append(f"### {x['body']} — step {x['depth']} ({'only' if not others else 'also: ' + ', '.join(others)})")
            L += ['- ' + c for c in x['cells']] + ['']
        low = sorted(x['body'] for x in r['bodies'] if x['depth'] < 3)
        L += [f"Below step 3: {', '.join(f'{x}' for x in low) or 'none'}", '']
    with open(base + '.md', 'w') as f:
        f.write('\n'.join(L) + '\n')
    return base + '.md'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('bybody')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(HERE), 'docs', 'eddie_read', 'depth'))
    a = ap.parse_args()
    res = run(a.bybody)
    print(f"{res['race']}: top step {res['race_top']} ({', '.join(res['at_top'])}) -> {write(res, a.out)}")


if __name__ == '__main__':
    main()
