import json, glob, re, os, collections, sys
N48 = set(range(1,10)) | set(range(10,91,10)) | set(range(100,901,100)) | {1000} | set(range(11,18)) | set(range(110,171,10)) | set(range(1100,1601,100))
assert len(N48) == 48
LEV = ('strict','exact-in-race','exact-pre-off','near')
def n_of(t):
    m = re.fullmatch(r'(\d+)/9', t.strip()); return int(m.group(1)) if m else None
rows = []  # race, P, kind(single/part/root), m, desc, target, level
ratio9 = collections.Counter()
for f in sorted(glob.glob('/Users/eddieplace/astro-harmonics/docs/classic/*/jupiter/P[0-9][0-9].json')):
    race = f.split('/')[-3]; P = os.path.basename(f)[:-5]
    d = json.load(open(f))
    for h in d['hits']:
        if h['family'] == 'ninth':
            rows.append((race, P, 'single', h['m'], h['desc'], h['plane'], h['value'], h['target'], h['level']))
        elif h['family'] == 'ratio' and n_of(h['target']) is not None:
            ratio9[race] += 1
        for p in h.get('parts') or []:
            if p.get('family') == 'ninth':
                rows.append((race, P, 'part', h['m'] + '>' + p['m'], h['desc'] + ' || ' + p['desc'], p['plane'], p['value'], p['target'], p['level']))
        rn = h.get('root_number')
        if isinstance(rn, dict) and rn.get('family') == 'ninth':
            rows.append((race, P, 'root', h['m'], h['desc'], h.get('root_plane'), h.get('root_value'), rn['target'], rn['level']))
json.dump(rows, open(sys.argv[1], 'w'))
# counts
races = sorted({r[0] for r in rows} | set(ratio9))
for kind in ('single', 'part', 'root'):
    print(f'\n== {kind}: per race, level: total (in48/not48)')
    tot = collections.Counter()
    for race in races:
        c = collections.Counter(); c48 = collections.Counter()
        for r in rows:
            if r[0] == race and r[2] == kind:
                c[r[8]] += 1; c48[r[8]] += n_of(r[7]) in N48
                tot[r[8]] += 1; tot[r[8]+'48'] += n_of(r[7]) in N48
        print(f'{race:32s} ' + '  '.join(f'{l[:7]:7s} {c[l]:4d} ({c48[l]}/{c[l]-c48[l]})' for l in LEV))
    print(f'{"TOTAL":32s} ' + '  '.join(f'{l[:7]:7s} {tot[l]:4d} ({tot[l+"48"]}/{tot[l]-tot[l+"48"]})' for l in LEV))
print('\nratio-family hits with target n/9 (ratios, not ninths):', dict(ratio9))
