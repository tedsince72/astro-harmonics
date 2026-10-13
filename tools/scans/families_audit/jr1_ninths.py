import json, glob, re, os, collections, sys
N48 = set(range(1,10)) | set(range(10,91,10)) | set(range(100,901,100)) | {1000} | set(range(11,18)) | set(range(110,171,10)) | set(range(1100,1601,100))
TAG = re.compile(r'\.\d{5} \((\d+)/9\)')
EQ = re.compile(r'from Equators (\S+) and (\S+)')
out = open(sys.argv[1], 'w'); tot = collections.Counter(); bym = collections.Counter(); tags_tot = collections.Counter()
print(f"{'race':32s} items_w_ninth  all48  any_non48   tags(48/non48)")
for race_dir in sorted(glob.glob('/Users/eddieplace/astro-harmonics/docs/jupiter/*/layer3')):
    race = race_dir.split('/')[-2]; c = collections.Counter()
    for f in sorted(glob.glob(race_dir + '/P[0-9][0-9].json')):
        P = os.path.basename(f)[:-5]
        for it in json.load(open(f))['items']:
            ns = [int(x) for x in TAG.findall(it['text'])]
            for a, b in EQ.findall(it['text']):
                ns += [int(x.split('/')[0]) for x in (a, b) if '/' in x]
            if not ns: continue
            c['items'] += 1; c['t48'] += sum(n in N48 for n in ns); c['tno'] += sum(n not in N48 for n in ns)
            bad = sorted({n for n in ns if n not in N48})
            if bad:
                c['bad'] += 1; bym[it['m']] += 1
                out.write(f"{race} {P} m{it['m']} [{', '.join(f'{n}/9' for n in bad)}] {it['text']}\n")
            else: c['all48'] += 1
    tot.update(c)
    print(f"{race:32s} {c['items']:8d} {c['all48']:8d} {c['bad']:8d}       {c['t48']}/{c['tno']}")
print(f"{'TOTAL':32s} {tot['items']:8d} {tot['all48']:8d} {tot['bad']:8d}       {tot['t48']}/{tot['tno']}")
print('non-48 items by m:', dict(bym.most_common()))
