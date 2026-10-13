import json, re, collections, sys
S = sys.argv[1]
rows = json.load(open(S + '/jr3_rows.json'))
N48 = set(range(1,10)) | set(range(10,91,10)) | set(range(100,901,100)) | {1000} | set(range(11,18)) | set(range(110,171,10)) | set(range(1100,1601,100))
R = [l.split(',') for l in open(S + '/ranges.txt').read().split()]
R = [tuple(map(float, r)) for r in R]
def sn(v):
    for lo, hi, tol, t in R:
        if lo <= v < hi: return max(0.0, 100.0 * (tol - abs(v - t)) / tol), t
    return 0.0, None
n = lambda t: int(t.split('/')[0])
singles = [r for r in rows if r[2] == 'single']
allS = [r for r in singles if all(p.startswith('S ') for p in [])]
# m codes of single ninth hits
print(collections.Counter(r[3] for r in singles))
bad = [r for r in singles if n(r[7]) not in N48 and r[8] != 'near']
print('non-48 single strict/I/P:', len(bad))
sc = [sn(r[6]) for r in bad]
print('of these, value inside one of the 48 ranges with score>0:', sum(1 for s,t in sc if s > 0), ' >=50:', sum(1 for s,t in sc if s >= 50), ' >=80:', sum(1 for s,t in sc if s >= 80))
print('target frequency (top 25):', collections.Counter(r[7] for r in bad).most_common(25))
with open(S + '/jr3_non48_single_SIP.txt', 'w') as fh:
    for r in sorted(bad, key=lambda r: (r[0], r[1], ['strict','exact-in-race','exact-pre-off'].index(r[8]))):
        s, t = sn(r[6])
        fh.write(f"{r[0]} {r[1]} {r[3]} {r[4]} {r[5]} {r[6]:.5f} -> {r[7]} [{r[8]}]" + (f"  (new-48 score {s:.1f} vs {t})" if s > 0 else '') + '\n')
badp = [r for r in rows if r[2] in ('part','root') and n(r[7]) not in N48 and r[8] != 'near']
with open(S + '/jr3_non48_parts_SIP.txt', 'w') as fh:
    for r in badp: fh.write(f"{r[0]} {r[1]} {r[2]} {r[3]} {r[4]} {r[5]} {r[6]} -> {r[7]} [{r[8]}]\n")
print('parts/root non-48 S/I/P lines:', len(badp), 'unique (race,P,part desc,target):', len({(r[0],r[1],r[4].split(' || ')[-1],r[5],r[7]) for r in badp}))
