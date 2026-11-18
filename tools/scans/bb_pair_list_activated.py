"""Pair list split by sky activation (18 Nov 2026, Eddie: 'a new list of positive / neutral / negative pairs when activated or not,
including the royal stars (and noting the higher performing families)'; read-only).
Items held by a runner (each counted once per runner):
  sky-on-natal  S Y -> natal X (H or J) scoring >= cut in any family (as bb_scan_sky_on_natal), key (Y, X, act):
                act = 'activated' when the sky pair S Y - S X scores (conj or a number family), else 'not activated'
  royal         natal royal line c R - c X in a number family >= cut, key (R, X, grp): grp = 'sky-linked' (carried by a sky pair on
                the same family + target, or S R - S X scores) or 'no sky line'
Label over the result races (bb_scan_sky_on_natal.label: positive = won >= 2 and >= 2 x chance; negative = chance >= 1.5 and won <= chance / 3;
else neutral). Families: per kind, activation group and family of the line, holdings / won / by chance (each holding 1 / field size).
Fair check: each runner's net (positive - negative items) with labels from the OTHER races; winner top / bottom of its race vs chance.
  python3 tools/scans/bb_pair_list_activated.py [cut]   -> docs/eddie_read/bybody/pair_list_activated_<cut>.md"""
import sys
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 90
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_sky_on_natal as S
import bb_scan_negatives as NEG
import bb_scan_royal_activated as RA
NO = ('conj', 'contraparallel', 'opposition')


def items(D):
    sky = set()
    for X, d in D.items():
        for r in d['O']:
            ln = r['line']
            if r.get('sc') is not None and ln.startswith('S ') and ' – ' in ln and r['fam'] not in ('contraparallel', 'opposition'):
                sky.add(frozenset(s[2:] for s in ln.split(' – ')))
    out = {}
    for X, d in D.items():
        for r in d['L'] + d['O']:
            ln = r['line']
            if r.get('sc') is None or r['sc'] < CUT or not ln.startswith('S ') or '→' not in ln:
                continue
            y = ln.split('→')[0][2:].strip(); x = ln.split('→')[1].strip()[2:]
            k = ('sky-on-natal', y, x, 'activated' if frozenset((y, x)) in sky else 'not activated')
            if k not in out or r['sc'] > out[k][1]:
                out[k] = (r['fam'], r['sc'], f"{ln} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']})")
    for grp, txt in RA.lines(D, CUT):
        ln = txt.split(' RA ')[0].split(' Dec ')[0]
        a, b = [s[2:] for s in ln.split(' – ')]
        k = ('royal', a, b, 'no sky line' if grp == 'neither' else 'sky-linked')
        fam = next(r['fam'] for r in D[b]['L'] if f"{r['line']} {r['plane']} {r['tgt']} ({r['sc']})" == txt)
        sc = float(txt.rsplit('(', 1)[1][:-1])
        if k not in out or sc > out[k][1]:
            out[k] = (fam, sc, txt)
    return out


def tally(data, skip=None):
    st = {}
    for race, win, R in data:
        if race == skip:
            continue
        N = len(R)
        for run, it in R.items():
            for k in it:
                x = st.setdefault(k, [0, 0, 0.0]); x[0] += 1; x[1] += win in run; x[2] += 1 / N
    return st


def main():
    data = [(race, win, {run: items(D) for run, D in E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx').items()})
            for race, win in NEG.RACES]
    st = tally(data)
    out = [f'# Pair list split by sky activation, any family >= {CUT:g} ({len(data)} result races; in-sample labels)', '',
           'positive = won >= 2 and >= 2 x chance; negative = chance >= 1.5 and won <= chance / 3; neutral = the rest. '
           'Holdings / won / by chance. Chosen after the results; holdings are not independent.', '']
    fam = {}
    for race, win, R in data:
        N = len(R)
        for run, it in R.items():
            for k, (f, sc, _) in it.items():
                x = fam.setdefault((k[0], k[3], f), [0, 0, 0.0]); x[0] += 1; x[1] += win in run; x[2] += 1 / N
    out += ['## Families (kind, sky, family: holdings / won / by chance, won ÷ chance)', '']
    for key in sorted(fam, key=lambda q: (q[0], q[1], -fam[q][1] / max(fam[q][2], 1e-9))):
        h, w, c = fam[key]
        out.append(f'- {key[0]}, {key[1]}, {key[2]}: {h} / {w} / {c:.1f}  ({w / c:.2f})' if c else '')
    for lab in ('positive', 'negative'):
        for kind in ('sky-on-natal', 'royal'):
            for act in (('activated', 'not activated') if kind == 'sky-on-natal' else ('sky-linked', 'no sky line')):
                rows = [(k, v) for k, v in st.items() if k[0] == kind and k[3] == act and S.label(v[1], v[2]) == lab]
                rows.sort(key=lambda q: (-(q[1][1] / q[1][2]) if lab == 'positive' else q[1][1] / q[1][2], -q[1][0]))
                out += ['', f'## {lab.upper()} - {kind}, {act} ({len(rows)})', '']
                for k, (h, w, c) in rows:
                    nm = f'S {k[1]} → {k[2]}' if kind == 'sky-on-natal' else f'{k[1]} – {k[2]}'
                    out.append(f'- {nm}: {h} / {w} / {c:.1f}')
    neu = {}
    for k, v in st.items():
        if not S.label(v[1], v[2]):
            x = neu.setdefault((k[0], k[3]), [0, 0, 0, 0.0]); x[0] += 1; x[1] += v[0]; x[2] += v[1]; x[3] += v[2]
    out += ['', '## NEUTRAL (count of pairs; their holdings / won / by chance)', '']
    for k, (n, h, w, c) in sorted(neu.items()):
        out.append(f'- {k[0]}, {k[1]}: {n} pairs; {h} / {w} / {c:.1f}')
    # fair check
    top = bot = 0; ct = cb = 0.0
    for race, win, R in data:
        s2 = tally(data, skip=race)
        net = {run: sum((S.label(s2[k][1], s2[k][2]) == 'positive') - (S.label(s2[k][1], s2[k][2]) == 'negative')
                        for k in it if k in s2) for run, it in R.items()}
        hi, lo = max(net.values()), min(net.values())
        tops = [r for r in net if net[r] == hi]; bots = [r for r in net if net[r] == lo]
        top += sum(win in r for r in tops) / len(tops); bot += sum(win in r for r in bots) / len(bots)
        ct += 1 / len(R); cb += 1 / len(R)
    out += ['', f'## Fair check (labels from the other races): winner top by net {top:.1f} of {len(data)} (chance {ct:.1f}), '
            f'bottom {bot:.1f} (chance {cb:.1f}); ties split']
    txt = '\n'.join(x for x in out if x is not None) + '\n'
    open(f'docs/eddie_read/bybody/pair_list_activated_{CUT:g}.md', 'w').write(txt)
    print(txt[:200]); print(out[-1])


if __name__ == '__main__':
    main()
