#!/usr/bin/env python3
"""trigger.py WORKBOOK TAB A B  (Eddie 11 Oct: 'why are these natal pairs triggered that day — what is in the sky?')
For a natal pair A–B in chart TAB (P01 horse / P02 jockey):
 1 its natal RA and Dec distances;
 2 SAME NUMBER in the race sky: sky pairs (moving body involved; no star–star) whose RA or Dec equals the natal RA or Dec value (±0.005);
 3 BOTH ENDS STRUCK: a sky body X whose distance to natal A and to natal B (RA or Dec) are both whole (±0.005) or ninths (±0.0005);
 4 SKY A–B itself and the movement of A and B since birth (sky − natal), with whole/ninth flags."""
import sys, openpyxl, itertools
F, TAB, A, B = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
wb = openpyxl.load_workbook(F, data_only=True)
BOD = ['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
def load(t):
    P = {}
    for r in list(wb[t].iter_rows(values_only=True))[1:]:
        b = r[1]
        if b in BOD: P[b] = (float(r[4]), float(r[8]))
        elif isinstance(b, str) and b.endswith('_B'): P[b[:-2] + '*'] = (float(r[4]), float(r[8]))
    return P
S, N = load('TRANS'), load(TAB); who = wb[TAB].cell(2, 1).value
st = lambda x: x.endswith('*'); rd = lambda a, b: abs((a[0] - b[0] + 180) % 360 - 180); dd = lambda a, b: abs(a[1] - b[1])
def lab(v):
    w = round(v); q = round(v * 9)
    if abs(v - w) <= 0.005 and w > 0: return f"{w}"
    if abs(v - q / 9) <= 0.0005 and q % 9: return f"{q}/9"
    return None
nr, nd = rd(N[A], N[B]), dd(N[A], N[B])
print(f"== {who}: natal {A}–{B}  RA {nr:.4f} ({lab(nr)})  Dec {nd:.4f} ({lab(nd)})")
print(f"\n2. same number in the race sky (±0.005), moving body involved:")
for x, y in itertools.combinations(S, 2):
    if (st(x) and st(y)) or {x, y} == {'Rahu', 'Ketu'}: continue
    for mm, v in (('RA', rd(S[x], S[y])), ('Dec', dd(S[x], S[y]))):
        for tm, t in (('RA', nr), ('Dec', nd)):
            if t >= 0.5 and abs(v - t) <= 0.005: print(f"   sky {x}–{y} {mm} {v:.4f}  = natal {tm} {t:.4f}  (off {abs(v-t):.4f})")
print(f"\n3. a sky body on whole/ninth to BOTH natal {A} and natal {B}:")
for x in S:
    if st(x): continue
    hits = {}
    for end in (A, B):
        for mm, v in (('RA', rd(S[x], N[end])), ('Dec', dd(S[x], N[end]))):
            l = lab(v)
            if l: hits.setdefault(end, []).append(f"{mm} {v:.4f}={l}")
    if len(hits) == 2: print(f"   sky {x}: → {A} " + ', '.join(hits[A]) + f" | → {B} " + ', '.join(hits[B]))
print(f"\n4. sky {A}–{B}: RA {rd(S[A], S[B]):.4f} ({lab(rd(S[A], S[B]))})  Dec {dd(S[A], S[B]):.4f} ({lab(dd(S[A], S[B]))})")
for e in (A, B):
    if st(e): continue
    mr = (S[e][0] - N[e][0] + 180) % 360 - 180; md = S[e][1] - N[e][1]
    print(f"   {e} moved since birth: RA {mr:+.4f} ({lab(abs(mr))})  Dec {md:+.4f} ({lab(abs(md))})")
