"""List the cases of chosen BB rules under the T2 tolerances above 100 (tools/scans/bb_over100_tighten.py: ninth, φ power, √2,
silver ±0.05; opposition ±0.25), 8 result races: runner, body, every cell (line, plane, value, family, target, score; '>100' marks a
value above 100, '[was ...]' its as-built score). Usage: python3 tools/scans/bb_t2_cases.py BB13 BB48"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_over100_tighten as TT

ids = sys.argv[1:] or ['BB13', 'BB48']
fns = {rid: fn for rid, fn, _ in E.RULES if fn is not None}
out = []
for n, r, w in TT.RACES:
    raw = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx')
    t2 = TT.tighten(raw, TT.V['T2'])
    old = {(run, X, sec, x['line'], x['plane']): x['sc'] for run, bs in raw.items() for X, d in bs.items() for sec in 'LSO' for x in d[sec]}
    for rid in ids:
        for run, D in t2.items():
            for X, d in D.items():
                b = E.Body(X, d); b.all = D
                seen = set()
                for case in fns[rid](b):
                    if case.get('watch_only') or case['key'] in seen:
                        continue
                    seen.add(case['key'])
                    out.append(f"\n### {rid} — {n} — {run}{' (WINNER)' if w in run else ''} — {case.get('body', X)}")
                    done = set()
                    for c in case['cells']:
                        k = (c['line'], c['plane'], c['tgt'])
                        if k in done:
                            continue
                        done.add(k)
                        flag = ''
                        if E.num(c['v']) and c['v'] > 100:
                            was = next((v for (ru, xx, sec, l, p), v in old.items() if ru == run and l == c['line'] and p == c['plane']), None)
                            flag = f"  >100 [was {was}]" if was != c['sc'] else '  >100'
                        out.append(f"- {c['line']} {c['plane']} {c['v']:.4f} — {c['fam']} {c['tgt']} ({c['sc']}){flag}")
txt = '\n'.join(out)
print(txt)
open(f"docs/eddie_read/bybody_rules/t2_cases_{'_'.join(ids)}.md", 'w').write(f"# {' '.join(ids)} under T2 (tolerances above 100 tightened)\n" + txt + '\n')
