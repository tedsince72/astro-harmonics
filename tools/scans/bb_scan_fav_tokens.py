"""What do winning favourites have that losing favourites do not? (19 Nov 2026, Eddie: 'is there a distance, a pair, a family, a star
or maybe the moon or sun involved here?'; read-only, chosen after the results). Every result race with a known favourite
(bb_favs_outer_uranus.FAV) and a bybody xlsx. Per runner, every bybody line scoring >= CUT (L, S, O groups; conj / cp incl.), as tokens:
  pair    'S Y → N X' (N = natal, horse or jockey) / 'S A – S B' / 'R – N X' (royal natal line) / 'H X – J X', any plane
  fam     the line's family (count of lines per family)
  star    a royal star on the line
  sunmoon S Sun / S Moon on the line
  target  family + target number
Race level: the sky lines S A – S B >= CUT (any runner's O rows) as pair + family.
Compared: winning favourites, losing favourites, other winners (not the favourite). Token shown when held by >= 4 winning favourites.
Usage: python3 tools/scans/bb_scan_fav_tokens.py [CUT]"""
import sys, os, re
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 90
sys.argv = sys.argv[:1]; sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody_rules as E, bb_scan_negatives as NG, bb_favs_outer_uranus as F
ROYAL = ('Aldebaran', 'Regulus', 'Antares', 'Fomalhaut')


def toks(D):
    t = set(); fam = {}
    for X, d in D.items():
        for g in ('L', 'S', 'O'):
            for r in d[g]:
                if r.get('sc') is None or r['sc'] < CUT:
                    continue
                ln = r['line']; f = r['fam']
                gen = re.sub(r'\b[HJ] ', 'N ', ln)
                t.add(('pair', gen)); t.add(('pairfam', f'{gen} {f}'))
                t.add(('target', f'{f} {r["tgt"]}'))
                fam[f] = fam.get(f, 0) + 1
                for s in ROYAL:
                    if s in ln:
                        t.add(('star', s))
                if 'S Sun' in ln: t.add(('sunmoon', 'S Sun line'))
                if 'S Moon' in ln: t.add(('sunmoon', 'S Moon line'))
    for f, n in fam.items():
        t.add(('fam', f'{f} >= 3' if n >= 3 else f'{f} 1-2'))
    return t, fam


def sky(D):
    s = set()
    for X, d in D.items():
        for r in d['O']:
            if r.get('sc') is not None and r['sc'] >= CUT and r['line'].startswith('S ') and '–' in r['line']:
                a, b = sorted(x.strip()[2:] for x in r['line'].split('–'))
                s.add(f'S {a} – S {b} {r["fam"]}')
    return s


WF, LF, OW = [], [], []; SW, SL = [], []; FW, FL = [], []
for race, win in NG.RACES:
    p = f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx'
    if not os.path.exists(p):
        continue
    R = E.load(p)
    fav = next((r for r in R if race in F.FAV and F.FAV[race] in r), None)
    wr = next((r for r in R if win in r), None)
    if fav:
        t, fm = toks(R[fav]); (WF if fav == wr else LF).append(t); (FW if fav == wr else FL).append(fm)
        (SW if fav == wr else SL).append(sky(R[fav]))
    if wr and wr != fav:
        OW.append(toks(R[wr])[0])
print(f'# Favourite tokens, lines >= {CUT}: winning favourites {len(WF)}, losing favourites {len(LF)}, other winners {len(OW)}\n')
print('Chosen after the results; 9 winning favourites is a very small sample.\n')
keys = sorted({k for t in WF for k in t})
rows = []
for k in keys:
    w = sum(k in t for t in WF); l = sum(k in t for t in LF); o = sum(k in t for t in OW)
    if w >= 4:
        rows.append((w / len(WF) - l / max(1, len(LF)), k, w, l, o))
for kind in ('sunmoon', 'star', 'fam', 'pair', 'pairfam', 'target'):
    sel = sorted((r for r in rows if r[1][0] == kind), reverse=True)
    print(f'## {kind}\n\n| token | winning favs | losing favs | other winners |\n|---|---|---|---|')
    for d, k, w, l, o in sel[:15]:
        print(f'| {k[1]} | {w}/{len(WF)} | {l}/{len(LF)} ({100*l/len(LF):.0f} %) | {o}/{len(OW)} ({100*o/len(OW):.0f} %) |')
    print()
print('## Lines per family (average per favourite)\n\n| family | winning favs | losing favs |\n|---|---|---|')
for f in sorted({f for m in FW + FL for f in m}, key=str):
    print(f'| {f} | {sum(m.get(f, 0) for m in FW)/len(FW):.1f} | {sum(m.get(f, 0) for m in FL)/len(FL):.1f} |')
print('\n## Race-level sky lines (S A – S B) in favourite-won races, held in >= 3\n\n| sky line | fav won | fav lost |\n|---|---|---|')
ks = sorted({k for s in SW for k in s})
for k in sorted(ks, key=lambda k: -sum(k in s for s in SW)):
    w = sum(k in s for s in SW); l = sum(k in s for s in SL)
    if w >= 3:
        print(f'| {k} | {w}/{len(SW)} | {l}/{len(SL)} |')
