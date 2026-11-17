"""Field check (17 Nov 2026, from Ffos Las 17:25 23 Mar 2022 Ring The Moon; read-only, from the depth ladder json files).
  T1  the runner alone with the most bodies at depth 3+ (Ring The Moon 4)
  T2  one sky pair closes step-3 loops on two or more bodies (Ring The Moon: S Mercury – S Gonggong Dec 4×φ on Juno and Neptune)
  J1  a closed loop (depth >= 3) whose same-body line scores >= 90 and one pair end lands on BOTH natal X (S E -> H X and S E -> J X,
      number family, no conj / cp, both >= 80) (Ring The Moon Juno: S Juno → H Juno RA 4×φ 96, pair S Mercury – S Gonggong Dec 4×φ,
      S Mercury → H Juno RA 41.4 silver 98.41 and → J Juno RA 177.778 ninth 83.74)
  J2  J1 with one of those end lines >= 90
Prints picks / won / by chance over the result races that have a depth json."""
import sys, json, os, re
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_fieldcheck_daphne as F
RACES = F.RACES + [('20220414_newmarket_1535', 'Eydon'), ('20220406_lingfield_aw_1425', 'Man On A Mission'),
                   ('20220323_ffos_las_1725', 'Ring The Moon')]
SC = re.compile(r'\(([\d.]+)\)\s*$')
sc = lambda c: float(SC.search(c).group(1)) if SC.search(c) else 0.0


def runner_tags(r):
    t = set(); pairs = {}
    for b in r['bodies']:
        if b['depth'] < 3:
            continue
        X, cs = b['body'], b['cells']
        for c in cs:
            m = re.match(r'pair (S \S+ – S \S+ \S+) ', c)
            if m:
                pairs.setdefault(m.group(1), set()).add(X)
        if not cs or sc(cs[0]) < 90:
            continue
        for c in cs:
            m = re.match(r'(\S+) on X: (.*)', c)
            if not m:
                continue
            good = [l for l in m.group(2).split('; ') if 'conj' not in l and 'contraparallel' not in l and sc(l) >= 80]
            if any(f'→ H {X}' in l for l in good) and any(f'→ J {X}' in l for l in good):
                t.add('J1')
                if any(sc(l) >= 90 for l in good):
                    t.add('J2')
    if any(len(v) >= 2 for v in pairs.values()):
        t.add('T2')
    return t


def main():
    tot = {k: [0, 0, 0.0, []] for k in ['T1', 'T2', 'J1', 'J2']}; n = 0
    for race, win in RACES:
        f = f'docs/eddie_read/depth/{race}_depth.json'
        if not os.path.exists(f):
            print('no depth json:', race); continue
        n += 1
        rs = json.load(open(f))['runners']; N = len(rs)
        mx = max(r['n3'] for r in rs)
        for r in rs:
            t = runner_tags(r)
            if r['n3'] == mx and sum(x['n3'] == mx for x in rs) == 1:
                t.add('T1')
            for k in t:
                v = tot[k]; v[0] += 1; v[1] += win in r['runner']; v[2] += 1 / N
                if win in r['runner']:
                    v[3].append(r['runner'])
    print(f'## Totals over {n} result races (picks / won / by chance)')
    for k, (p, w, c, ws) in tot.items():
        print(f'  {k}: {p} / {w} / {c:.1f}  {", ".join(ws)}')


if __name__ == '__main__':
    main()
