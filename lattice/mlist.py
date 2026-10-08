"""mlist.py RACE TAB_H TAB_J M1DIR CROSSFILE OUTDIR
Method 1 lists for prediction (Eddie, 8 Oct 08:29 "yes, build the lists"). Kept WIDE: everything Method 1 found, nothing trimmed.
Input: the per-body Method 1 outputs (natnums.py + natchords.py at 12:00, files <TAB>_<Body>.txt in M1DIR) and cross.py output.
Output: <OUTDIR>/<name>_list.md for each chart and <horse>__<jockey>_combined.md."""
import sys, re, os, csv, math, collections
exec(open('/home/claude/lattice/families.py').read().split("CH = []")[0])   # STARS, iv, dist, ctype
RACE, TH, TJ, D, CROSS, OUT = sys.argv[1:7]
os.makedirs(OUT, exist_ok=True)
BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas', 'Juno', 'Vesta',
          'Eris', 'Sedna', 'Haumea', 'Makemake', 'Quaoar', 'Orcus', 'Gonggong', 'Transpluto', 'Rahu', 'Ketu']
OBL = 23.437
NUMRE = re.compile(r"^\s+to (.+?)\s{2,}([\d.]+) = (.+?)\s+\(([\d.]+), off ([+-][\d.]+)\)\s+(.+?)\s+\[00:00 ([\d.]+) · 24:00 ([\d.]+)\]")
POSRE = re.compile(r"natal (\S+) at 12h: RA ([\d.]+) Dec (-?[\d.]+)\s+\(00:00 RA ([\d.]+) Dec (-?[\d.]+); 24:00 RA ([\d.]+) Dec (-?[\d.]+)\)")
CHRE = re.compile(r"^\s+(RA|Dec|Flat|Sky)\s+(.+?)–(.+?)\s+base\s+([\d.]+) \| to (.+?)\s+([\d.]+) \| to (.+?)\s+([\d.]+)\s+(.+?)\s+([\d.]+)%\s+\[00:00 ([\d.]+)%\s+24:00 ([\d.]+)%\]")
META = list(csv.reader(open(f"/home/claude/ledger/allpos/{RACE}__META.csv")))
tabs = {r[0]: (r[1], r[3], r[4] if len(r) > 4 else '') for r in META if r and r[0].startswith('P') and r[0][1:].isdigit()}
def parse(tab):
    pos, nums, stc, boc = {}, [], [], []
    for b in BODIES:
        f = f"{D}/{tab}_{b}.txt"
        if not os.path.exists(f): continue
        meas = None; sect = None
        for ln in open(f, encoding='utf-8'):
            m = POSRE.search(ln)
            if m: pos[b] = tuple(float(x) for x in m.groups()[1:]); continue
            s = ln.strip()
            if s in ('RA:', 'Dec:', 'Flat:', 'Sky:', '|Dec|:'): meas = s[:-1]; sect = 'num'; continue
            if s.startswith('WITH THE STARS'): sect = 'star'; continue
            if s.startswith('WITH TWO OTHER NATAL'): sect = 'body'; continue
            if sect == 'num':
                m = NUMRE.match(ln)
                if m:
                    tgt = m.group(1).replace(' ★', '').strip()
                    nums.append(dict(body=b, meas=meas, to=tgt, star='★' in m.group(1), val=float(m.group(2)), lab=m.group(3).strip(),
                                     off=float(m.group(5)), when=m.group(6).strip()))
            elif sect in ('star', 'body'):
                m = CHRE.match(ln)
                if m:
                    g = m.groups()
                    rec = dict(body=b, meas=g[0], A=g[1].strip(), B=g[2].strip(), base=float(g[3]), dA=float(g[5]), dB=float(g[7]),
                               ratio=g[8].strip(), dev=float(g[9]), d0=float(g[10]), d24=float(g[11]))
                    (stc if sect == 'star' else boc).append(rec)
    return pos, nums, stc, boc
def allday(c): return c['d0'] <= 0.15 and c['d24'] <= 0.15
def cdesc(c, who=True):
    ad = ' — held all day' if allday(c) else f" (00:00 {c['d0']:.3f}%, 24:00 {c['d24']:.3f}%)"
    return (f"{c['body'] + ' on ' if who else ''}{c['meas']} {c['A']}–{c['B']} {c['ratio']} {c['dev']:.3f}%{ad}"
            f"  [base {c['base']:.3f} | to {c['A']} {c['dA']:.3f} | to {c['B']} {c['dB']:.3f}]")
def ndesc(n, who=True):
    t = 'own Dec' if n['to'] == 'own' else ('to ' + n['to'] + (' ★' if n['star'] else ''))
    return f"{n['body'] + ' ' if who else ''}{n['meas']} {t} = {n['lab']} ({n['val']:.4f}, off {n['off']:+.4f}; {n['when']})"
def fam(lab):
    if '/9' in lab: return 'ninth'
    return 'whole' if lab.startswith('whole') else ('φⁿ' if 'φ^' in lab or re.search('φ[⁰¹²³⁴⁵⁶⁷⁸⁹]', lab) else ('φ' if 'φ' in lab else ('√2' if '√2' in lab else 'other')))
DATA = {t: parse(t) for t in (TH, TJ)}
def chart_list(tab):
    name, role, born = tabs[tab][1], tabs[tab][0], tabs[tab][2]
    pos, nums, stc, boc = DATA[tab]; L = []
    L.append(f"# Method 1 list — {name} ({role}, {tab} of {RACE}{', born ' + born if born else ''})")
    L.append("Birth chart at 12:00 (the midday rule). Kept wide: every number (±0.002°) and every chord (≤0.15%) found in Method 1. "
             "Natal Moon left out. ★ = a star. 'Held all day' = the chord stays within 0.15% from 00:00 to 24:00 on the birth day.\n")
    L.append("## 1. The bodies")
    L.append("| Body | RA | Dec | RA move /day | Dec move /day | Out of bounds | Numbers | Star chords | Body chords |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    cnt = lambda lst, b: sum(1 for x in lst if x['body'] == b)
    for b in BODIES:
        if b not in pos: continue
        ra, de, r0, d0, r24, d24 = pos[b]; dra = ((r24 - r0 + 180) % 360) - 180; dde = d24 - d0
        oob = f"YES {abs(de) - OBL:+.2f}" if abs(de) > OBL else ''
        L.append(f"| {b} | {ra:.3f} | {de:+.3f} | {dra:+.3f} | {dde:+.3f} | {oob} | {cnt(nums, b)} | {cnt(stc, b)} | {cnt(boc, b)} |")
    L.append("\n## 2. Body by body (everything)")
    for b in BODIES:
        if b not in pos: continue
        ra, de = pos[b][:2]
        L.append(f"\n### {b} — RA {ra:.3f}, Dec {de:+.3f}")
        nn = [n for n in nums if n['body'] == b]; ss = sorted([c for c in stc if c['body'] == b], key=lambda c: c['dev']); bb = sorted([c for c in boc if c['body'] == b], key=lambda c: c['dev'])
        L.append(f"- **Numbers ({len(nn)}):**" + ('' if nn else ' none'))
        for n in nn: L.append(f"  - {ndesc(n, False)}")
        L.append(f"- **Star chords ({len(ss)}):**" + ('' if ss else ' none'))
        for c in ss: L.append(f"  - {cdesc(c, False)}")
        L.append(f"- **Chords with two other natal bodies ({len(bb)}):**" + ('' if bb else ' none'))
        for c in bb: L.append(f"  - {cdesc(c, False)}")
    # strings
    L.append("\n## 3. Star strings and who holds them (the watch list for Methods 2 and 3)")
    L.append("Every star base (pair of stars, or a star and the Equator) with each natal body that makes a chord on it. Bases held by two or more bodies first, then the rest; all kept.")
    S = collections.defaultdict(list)
    for c in stc: S[(c['meas'], tuple(sorted((c['A'], c['B']))))].append(c)
    for k, v in sorted(S.items(), key=lambda kv: (-len({c['body'] for c in kv[1]}), min(c['dev'] for c in kv[1]))):
        L.append(f"- **{k[0]} {k[1][0]}–{k[1][1]}** ({len({c['body'] for c in v})}): " + '; '.join(f"{c['body']} {c['ratio']} {c['dev']:.3f}%{' all day' if allday(c) else ''}" for c in sorted(v, key=lambda c: c['dev'])))
    L.append("\n## 4. Figures between natal bodies (each counted once)")
    F = {}
    for c in boc:
        k = (c['meas'], frozenset((c['body'], c['A'], c['B'])))
        if k not in F or c['dev'] < F[k]['dev']: F[k] = c
    for (mm, fs), c in sorted(F.items(), key=lambda kv: kv[1]['dev']):
        mid = ''
        if c['ratio'].startswith('1:1:2'):
            d = {c['A']: c['dA'], c['B']: c['dB']}; mid = ' — MIDPOINT'
        L.append(f"- {mm} {'–'.join(sorted(fs))}: {c['ratio']} {c['dev']:.3f}%{' all day' if allday(c) else ''}{mid}")
    L.append("\n## 5. Midpoints (1:1:2) on star bases")
    mids = [c for c in stc if c['ratio'].startswith('1:1:2')]
    for c in sorted(mids, key=lambda c: c['dev']): L.append(f"- {cdesc(c)}")
    if not mids: L.append("- none")
    L.append("\n## 6. Stars and every body that reaches them (by chord or by number)")
    ST = collections.defaultdict(list)
    for c in stc:
        for s_ in (c['A'], c['B']):
            if s_ != 'Equator': ST[s_].append(f"{c['body']} chord {c['meas']} {c['A']}–{c['B']} {c['dev']:.3f}%")
    for n in nums:
        if n['star']: ST[n['to']].append(f"{n['body']} number {n['meas']} {n['lab']}")
    for s_, v in sorted(ST.items(), key=lambda kv: -len({x.split()[0] for x in kv[1]})):
        bodies = sorted({x.split()[0] for x in v})
        L.append(f"- **{s_}** — {len(bodies)} bodies ({', '.join(bodies)}): " + '; '.join(v))
    L.append("\n## 7. Numbers between natal bodies (each pair once)")
    seen = set()
    for n in sorted([n for n in nums if not n['star'] and n['to'] != 'own'], key=lambda n: (n['meas'], n['body'])):
        k = (n['meas'], frozenset((n['body'], n['to'])), n['lab'])
        if k in seen: continue
        seen.add(k); L.append(f"- {n['meas']} {n['body']}–{n['to']} = {n['lab']} ({n['val']:.4f}; {n['when']})")
    L.append("\n## 8. Dec numbers (the Dec lattice): own Dec, and Dec distances to stars and bodies")
    for n in sorted([n for n in nums if n['meas'] in ('Dec', '|Dec|')], key=lambda n: n['body']):
        L.append(f"- {ndesc(n)}")
    L.append("\n## 9. Number families")
    fc = collections.Counter(fam(n['lab']) for n in nums)
    L.append('- ' + ', '.join(f"{k} {v}" for k, v in fc.most_common()))
    num_by = collections.defaultdict(list)
    for n in nums: num_by[n['lab']].append(n)
    rep = {k: v for k, v in num_by.items() if len({x['body'] for x in v}) > 1}
    L.append("- The same number from more than one body: " + ('; '.join(f"{k} — " + ', '.join(f"{x['body']} {x['meas']} to {x['to']}" for x in v) for k, v in sorted(rep.items())) if rep else 'none'))
    return '\n'.join(L) + '\n'
def combined():
    h, j = tabs[TH][1], tabs[TJ][1]
    (ph, nh, sh, bh), (pj, nj, sj, bj) = DATA[TH], DATA[TJ]
    L = [f"# Method 1 combined list — {h} ({TH}) × {j} ({TJ}), {RACE}",
         "Both charts at 12:00. Kept wide. Natal Moon left out. Race-day items (same-body chords with the race sky) are in the race read, not here.\n"]
    L.append("## 1. Star strings held in both charts")
    Sh = collections.defaultdict(list); Sj = collections.defaultdict(list)
    for c in sh: Sh[(c['meas'], tuple(sorted((c['A'], c['B']))))].append(c)
    for c in sj: Sj[(c['meas'], tuple(sorted((c['A'], c['B']))))].append(c)
    both = sorted(set(Sh) & set(Sj), key=lambda k: min(c['dev'] for c in Sh[k] + Sj[k]))
    for k in both:
        L.append(f"- **{k[0]} {k[1][0]}–{k[1][1]}** — horse: " + '; '.join(f"{c['body']} {c['ratio']} {c['dev']:.3f}%" for c in sorted(Sh[k], key=lambda c: c['dev']))
                 + " | jockey: " + '; '.join(f"{c['body']} {c['ratio']} {c['dev']:.3f}%" for c in sorted(Sj[k], key=lambda c: c['dev'])))
    L.append(f"- ({len(both)} bases in both; horse {len(Sh)} bases, jockey {len(Sj)} bases)")
    L.append("\n## 2. The same star pair in a different measure (RA in one chart, Dec in the other, etc.)")
    ph_ = collections.defaultdict(set); pj_ = collections.defaultdict(set)
    for k in Sh: ph_[k[1]].add(k[0])
    for k in Sj: pj_[k[1]].add(k[0])
    for pr in sorted(set(ph_) & set(pj_)):
        if ph_[pr] & pj_[pr] == ph_[pr] | pj_[pr]: continue
        L.append(f"- {pr[0]}–{pr[1]}: horse {', '.join(sorted(ph_[pr]))} | jockey {', '.join(sorted(pj_[pr]))}")
    L.append("\n## 3. The same figure of natal bodies in both charts (same three bodies, same measure)")
    def figs(boc):
        F = {}
        for c in boc:
            k = (c['meas'], frozenset((c['body'], c['A'], c['B'])))
            if k not in F or c['dev'] < F[k]['dev']: F[k] = c
        return F
    Fh, Fj = figs(bh), figs(bj)
    sf = sorted(set(Fh) & set(Fj), key=lambda k: Fh[k]['dev'] + Fj[k]['dev'])
    for k in sf: L.append(f"- {k[0]} {'–'.join(sorted(k[1]))}: horse {Fh[k]['ratio']} {Fh[k]['dev']:.3f}% | jockey {Fj[k]['ratio']} {Fj[k]['dev']:.3f}%")
    if not sf: L.append("- none")
    L.append("\n## 4. The same number in both charts")
    lh = collections.defaultdict(list); lj = collections.defaultdict(list)
    for n in nh: lh[n['lab']].append(n)
    for n in nj: lj[n['lab']].append(n)
    for k in sorted(set(lh) & set(lj), key=lambda k: float(re.sub('[^0-9.]', '', k.split('/')[0]) or 0) if '/' in k else 0):
        L.append(f"- **{k}** — horse: " + ', '.join(f"{x['body']} {x['meas']} to {x['to']}" for x in lh[k]) + " | jockey: " + ', '.join(f"{x['body']} {x['meas']} to {x['to']}" for x in lj[k]))
    L.append("\n## 5. Stars reached in both charts (by chord or number)")
    def stars(nums, stc):
        S = collections.defaultdict(set)
        for c in stc:
            for s_ in (c['A'], c['B']):
                if s_ != 'Equator': S[s_].add(c['body'])
        for n in nums:
            if n['star']: S[n['to']].add(n['body'])
        return S
    Xh, Xj = stars(nh, sh), stars(nj, sj)
    for s_ in sorted(set(Xh) & set(Xj), key=lambda s_: -(len(Xh[s_]) + len(Xj[s_]))):
        L.append(f"- **{s_}** — horse {len(Xh[s_])} ({', '.join(sorted(Xh[s_]))}) | jockey {len(Xj[s_])} ({', '.join(sorted(Xj[s_]))})")
    L.append("\n## 6. Same body, horse and jockey — the natal-to-natal distances")
    L.append("| Body | RA | Dec | Flat | Sky | Numbers (±0.002) |")
    L.append("|---|---|---|---|---|---|")
    def numlab(x):
        o = []
        if x < 0.05: return o
        if abs(x - round(x)) <= 0.002 and round(x) > 0: o.append(f"whole {round(x)}")
        for k_, nm in ((PHI, 'φ'), (2 ** .5, '√2')):
            k = round(x / k_)
            if k > 0 and abs(x - k * k_) <= 0.002: o.append(f"{k}{nm}")
        k = round(x * 9)
        if abs(x - k / 9) <= 0.002 and k % 9: o.append(f"{k}/9")
        for n_ in range(-4, 13):
            if abs(x - PHI ** n_) <= 0.002: o.append(f"φ^{n_}")
        return o
    for b in BODIES:
        if b not in ph or b not in pj: continue
        A, B = ph[b][:2], pj[b][:2]
        vals = {mm: dist(A, B, mm) for mm in ('RA', 'Dec', 'Flat', 'Sky')}
        hits = '; '.join(f"{mm} {', '.join(numlab(v))}" for mm, v in vals.items() if numlab(v))
        par = ' PARALLEL' if abs(A[1] - B[1]) <= 0.1 else (' CONTRAPARALLEL' if abs(A[1] + B[1]) <= 0.1 else '')
        L.append(f"| {b} | {vals['RA']:.3f} | {vals['Dec']:.3f}{par} | {vals['Flat']:.3f} | {vals['Sky']:.3f} | {hits} |")
    L.append("\n## 7. Direct links between the two charts (cross.py: Dec parallels ≤0.1; numbers between every horse body and every jockey body)")
    L.append("```"); L += [ln.rstrip('\n') for ln in open(CROSS, encoding='utf-8')]; L.append("```")
    L.append("\n## 8. Cross-chart chords: a horse body, a jockey body and a star (all ≤0.15%; same body first, then tightest first)")
    hb = {b: ph[b][:2] for b in ph}; jb = {b: pj[b][:2] for b in pj}
    STP = {}
    for r in csv.DictReader(open(f"/home/claude/ledger/allpos/{RACE}__NATAL_HOURLY.csv")):
        if r['tab'] == TH and r['hour'] == '12' and r['body'].replace('_B', '') in STARS and r['ra']:
            STP[r['body'].replace('_B', '')] = (float(r['ra']), float(r['dec']))
    STP['Equator'] = (None, 0.0)
    out = []; nall = 0
    for a, A in hb.items():
        for b, B in jb.items():
            for s_, C in STP.items():
                for mm in ('RA', 'Dec', 'Flat', 'Sky'):
                    if s_ == 'Equator' and mm != 'Dec': continue
                    d = [dist(A, B, mm), dist(A, C, mm), dist(B, C, mm)]
                    if min(d) < 0.05: continue
                    rs = [max(d[0], d[1]) / min(d[0], d[1]), max(d[0], d[2]) / min(d[0], d[2]), max(d[1], d[2]) / min(d[1], d[2])]
                    dv = max(iv(x)[1] for x in rs)
                    if dv <= 0.0015: nall += 1
                    if dv <= 0.0015: out.append((dv, a, b, s_, mm, d))
    L.append(f"- {nall} cross-chart star chords at ≤0.15%, {sum(1 for x in out if x[0] <= 0.0002)} of them ≤0.02%. Same body in both charts marked ◆.")
    for dv, a, b, s_, mm, d in sorted(out, key=lambda x: (x[1] != x[2], x[0])):
        L.append(f"- {'◆ ' if a == b else ''}horse {a} – jockey {b} + {s_} {mm} {ctype(d)} {dv*100:.3f}%  [horse–jockey {d[0]:.3f} | horse–{s_} {d[1]:.3f} | jockey–{s_} {d[2]:.3f}]")
    return '\n'.join(L) + '\n'
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', re.sub(r'^\d+ ', '', s).lower()).strip('-')
for t in (TH, TJ):
    p = f"{OUT}/{slug(tabs[t][1])}_list.md"; open(p, 'w', encoding='utf-8').write(chart_list(t)); print(p)
p = f"{OUT}/{slug(tabs[TH][1])}__{slug(tabs[TJ][1])}_combined.md"; open(p, 'w', encoding='utf-8').write(combined()); print(p)
