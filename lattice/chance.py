import random, itertools, math, sys
exec(open('families.py').read().split("CH = []")[0])
def count(P):
    n = collections.Counter()
    for a, b, c in itertools.combinations(range(len(P)), 3):
        for m in ('RA', 'Dec'):
            d = [dist(P[a], P[b], m), dist(P[a], P[c], m), dist(P[b], P[c], m)]
            if min(d) < 0.05: continue
            rs = [max(d[0], d[1]) / min(d[0], d[1]), max(d[0], d[2]) / min(d[0], d[2]), max(d[1], d[2]) / min(d[1], d[2])]
            if max(iv(x)[1] for x in rs) <= 0.0015: n[m] += 1
    return n
real = count([S[s] for s in N]); print('real stars', dict(real))
random.seed(1)
for label, gen in (('uniform random', lambda: [(random.uniform(0, 360), random.uniform(-30, 90)) for _ in N]),
                   ('stars jittered ±3°', lambda: [((S[s][0] + random.uniform(-3, 3)) % 360, S[s][1] + random.uniform(-3, 3)) for s in N])):
    R = [count(gen()) for _ in range(60)]
    for m in ('RA', 'Dec'):
        v = sorted(r[m] for r in R)
        print(f"{label:20s} {m}: mean {sum(v)/len(v):.1f}  min {v[0]}  max {v[-1]}  real {real[m]}  rank {sum(x>=real[m] for x in v)}/60 at or above")
