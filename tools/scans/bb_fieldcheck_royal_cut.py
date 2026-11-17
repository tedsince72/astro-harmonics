"""Field check (17 Nov 2026, from Haydock 17:18 7 May 2022 Aldhaja Rahu): a royal natal line c R - c X whose same-body or crossed ratio
is on a whole 10-20 ('N 1/N cut') scoring >= 90 (the line itself need not score; Aldhaja J Regulus - J Rahu Dec 11.801637 crossed against
S Rahu -> J Rahu RA 129.806599 = 10.999033 on 11, 98.24). Versions:
  W0  the cut ratio >= 90 (any royal line)
  W0s the same, the royal line scoring in a number family itself
  W2  W0 + the same star on X in the same chart, other plane, in a family carried by a sky pair >= 90 (Aldhaja RA 17x phi by S Gonggong - S Aldebaran 95.93)
  W3  W0 + the same star on X in the other chart with a family or a ratio >= 50 (Aldhaja H Regulus - H Rahu RA 16/9 71.9)
  W4  W2 + W3
Read-only; prints holders per race and totals (picks / winners / by chance)."""
import os, sys, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'scans'))
import eddie_bybody_rules as R
import bb_fieldcheck_hj_carry as HC
RACES = HC.RACES + [('20220509_musselburgh_1550', 'John Kirkup'), ('20220507_haydock_1718', 'Aldhaja')]
ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
NO = ('conj', 'contraparallel', 'opposition')
CUT = re.compile(r'^(\d+) 1/\1 cut')


def cut_ok(t, s):
    m = CUT.match(str(t or ''))
    return bool(m) and 10 <= int(m.group(1)) <= 20 and s is not None and s >= 90


def star(line):
    return line.split(' – ')[0].split(' ', 1)[1]


def cases(X, d):
    out = []
    roy = [x for x in d['L'] if ' – ' in x['line'] and star(x['line']) in ROY]
    for r in roy:
        hits = [(k, t, s) for k, t, s in (('same-body', r['rt'], r['rs']), ('crossed', r['xt'], r['xs'])) if cut_ok(t, s)]
        if not hits:
            continue
        ch, st = r['line'][0], star(r['line'])
        tags = {'W0'}
        if r['fam'] and r['fam'] not in NO and r['sc'] is not None:
            tags.add('W0s')
        other = [x for x in roy if x['line'] == r['line'] and x['plane'] != r['plane'] and x['fam'] and x['fam'] not in NO]
        if any(s.get('match') == f"{o['line']} {o['plane']}" and ' – ' in s['line'] and '→' not in s['line'] and 'Moon' not in s['line']
               and s['sc'] is not None and s['sc'] >= 90 for o in other for s in d['S']):
            tags.add('W2')
        oc = 'J' if ch == 'H' else 'H'
        if any(x['line'] == f'{oc} {st} – {oc} {X}' and ((x['fam'] and x['fam'] not in NO) or (x['rs'] or 0) >= 50 or (x['xs'] or 0) >= 50)
               for x in roy):
            tags.add('W3')
        if {'W2', 'W3'} <= tags:
            tags.add('W4')
        out.append((tags, f"{r['line']} {r['plane']} {r['v']:.6f} " + '; '.join(f'{k} {t} ({s})' for k, t, s in hits)))
    return out


def main():
    keys = ['W0', 'W0s', 'W2', 'W3', 'W4']
    tot = {k: [0, 0, 0.0] for k in keys}
    for race, win in RACES:
        p = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', race, f'{race}_bybody.xlsx')
        if not os.path.exists(p):
            continue
        data = R.load(p); N = len(data)
        held = {k: set() for k in keys}
        print(f'## {race} ({N} runners, winner {win})')
        for run, D in data.items():
            for X, d in D.items():
                for tags, txt in cases(X, d):
                    for k in tags:
                        held[k].add(run)
                    print(f"  {run} {X} [{' '.join(k for k in keys if k in tags)}]: {txt}")
        for k in keys:
            tot[k][0] += len(held[k]); tot[k][1] += sum(win in r for r in held[k]); tot[k][2] += len(held[k]) / N
    print('\n## Totals (picks / winners / by chance)')
    for k in keys:
        print(f'  {k}: {tot[k][0]} picks, {tot[k][1]} won, {tot[k][2]:.1f} by chance')


if __name__ == '__main__':
    main()
