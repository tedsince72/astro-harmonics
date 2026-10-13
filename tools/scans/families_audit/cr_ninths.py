import glob, re, os, collections, sys
N48 = set(range(1,10)) | set(range(10,91,10)) | set(range(100,901,100)) | {1000} | set(range(11,18)) | set(range(110,171,10)) | set(range(1100,1601,100))
PAT = [re.compile(r'\d\.\d{4,5} \((\d+)/9[),]'), re.compile(r'\d\.\d{4,5} = (\d+)/9\b(?! \(\d+\.\d+%)'),
       re.compile(r'moved (?:RA|Dec|Flat|GC) \((\d+)/9\)'), re.compile(r'number (\d+)/9:')]
def tags(line):
    ns = []
    for p in PAT: ns += [int(x) for x in p.findall(line)]
    return ns
out = open(sys.argv[1], 'w')
T = collections.Counter()
print(f"{'race':32s} {'P-lines w/ ninth':>17s} {'any non48':>10s} {'only48':>7s} | field.txt lines w/ninth / non48 | watch M entries ninth / non48")
for d in sorted(glob.glob('/Users/eddieplace/astro-harmonics/docs/classic/*/checklist')):
    race = d.split('/')[-2]; c = collections.Counter()
    for f in sorted(glob.glob(d + '/P[0-9][0-9].txt')):
        for line in open(f):
            ns = tags(line)
            if not ns: continue
            c['l'] += 1
            bad = sorted({n for n in ns if n not in N48})
            if bad: c['b'] += 1; out.write(f"{race} {os.path.basename(f)[:3]} [{', '.join(f'{n}/9' for n in bad)}] {line.strip()[:240]}\n")
            else: c['o'] += 1
    f = d + '/field.txt'
    if os.path.exists(f):
        for line in open(f):
            ns = tags(line)
            if ns:
                c['fl'] += 1
                if any(n not in N48 for n in ns): c['fb'] += 1; out.write(f"{race} field [{', '.join(sorted({f'{n}/9' for n in ns if n not in N48}))}] {line.strip()[:240]}\n")
    f = d + '/watch_jupiter.txt'
    if os.path.exists(f):
        for line in open(f):
            for m in re.finditer(r'Jupiter moved (RA|Dec|Flat|GC) [\d.]+ \((\d+)/9\)', line):
                c['wm'] += 1; n = int(m.group(2))
                if n not in N48: c['wb'] += 1; out.write(f"{race} WATCH-M {m.group(0)}  <- {line.split()[0]}\n")
    T.update(c)
    print(f"{race:32s} {c['l']:17d} {c['b']:10d} {c['o']:7d} | {c['fl']:5d} / {c['fb']:5d} | {c['wm']:3d} / {c['wb']:3d}" + ('' if os.path.exists(d + '/watch_jupiter.txt') else '  (no watch file)'))
print(f"{'TOTAL':32s} {T['l']:17d} {T['b']:10d} {T['o']:7d} | {T['fl']:5d} / {T['fb']:5d} | {T['wm']:3d} / {T['wb']:3d}")
