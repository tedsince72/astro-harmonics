"""check_longstar.py (Eddie, 22 Oct 2026, LONG STAR TIMELINE): BEFORE.xlsx AFTER.xlsx [STARS...]
- every LONG STAR TIMELINE (sky) / LONG STAR TIMELINE H / J block = the rows of the matching LONG TIMELINE block whose relationship is between
  Jupiter and stars only (own test: a star name, no body name), identical cells, same order, SEPARATING / APPLYING sections with their counts,
  title counts, every row >= 90;
- every other row of every sheet of AFTER = BEFORE (values, fills, comments), in order.
Prints the counts per block (separating / applying) and the mismatches."""
import sys, re, openpyxl

BODIES = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas', 'Juno', 'Vesta',
          'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto', 'Rahu', 'Ketu', 'equator']
STARS = ['Algol', 'Pleiades', 'Aldebaran', 'Capella', 'Sirius', 'Procyon', 'Regulus', 'Alkaid', 'Algorab', 'Spica', 'Arcturus', 'Alphecca',
         'Antares', 'Vega', 'Deneb Algedi', 'Fomalhaut', 'Rigel', 'Betelgeuse', 'Polaris', 'Castor', 'Altair', 'Bellatrix', 'Galactic Centre',
         'Hamal', 'Pollux', 'Praesepe', 'Denebola', 'Zubenelgenubi', 'Zubeneschamali', 'Kaus Australis', 'Nunki', 'Deneb', 'Sadalsuud',
         'Sadalmelik', 'Scheat', 'Markab', 'Alpheratz', 'Algenib', 'Difda', 'Mirach', 'Menkar', 'Phact', 'Adhara', 'Wezen', 'Menkent',
         'Unukalhai', 'Rasalhague', 'Ankaa', 'Al Rescha', 'Mirfak', 'El Nath', 'Meissa', 'Alnilam', 'Murzim', 'Alhena', 'Acubens', 'Alphard',
         'Alkes', 'Zosma', 'Vindemiatrix', 'Diadem', 'Ras Algethi', 'Aculeus', 'Acumen', 'Facies', 'Rukbat', 'Sualocin', 'Orion Nebula Cluster']
STW = re.compile(r'\b(' + '|'.join(re.escape(x) for x in sorted(STARS, key=len, reverse=True)) + r')\b')
BOW = re.compile(r'\b(' + '|'.join(BODIES) + r')\b')
isstar = lambda rel: bool(STW.search(rel)) and not BOW.search(STW.sub('', rel))
LS = re.compile(r'^LONG STAR TIMELINE( [HJ])?')


def sig(r):
    return tuple((c.value, c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.comment.text if c.comment else None) for c in r)


def rows(ws):
    return [r for r in ws.iter_rows() if any(c.value is not None for c in r)]


def blocks(rs, tid):
    """-> {'SEPARATING': [sig], 'APPLYING': [sig]}, section counts, title"""
    sec, out, cnt, title = None, {'SEPARATING': [], 'APPLYING': []}, {}, None
    for r in rs:
        a = r[0].value
        if isinstance(a, str) and a.startswith(tid + ' ('):
            title = a
        if a != tid:
            continue
        d = r[3].value
        if isinstance(d, str) and d.startswith('———'):
            sec = d.split()[1].rstrip(':')
            cnt[sec] = int(re.search(r'(\d+) events', d).group(1))
            continue
        out[sec].append(r)
    return out, cnt, title


def main(fb, fa):
    wb, wa = openpyxl.load_workbook(fb), openpyxl.load_workbook(fa)
    bad = []
    for sh in wa.sheetnames:
        ra, rb = rows(wa[sh]), rows(wb[sh])
        # every row outside the LONG STAR blocks = before
        keep, inblk = [], False
        for r in ra:
            a = r[0].value
            if isinstance(a, str) and LS.match(a):
                continue                                   # title, section and event rows of the new blocks
            if a == 'table' and inblk:
                inblk = False
                continue                                   # the new blocks' header row
            keep.append(r)
            inblk = False
        # header rows: drop those directly after a LONG STAR title
        keep2, prev = [], None
        for r in ra:
            a = r[0].value
            if a == 'table' and prev is not None and isinstance(prev, str) and LS.match(prev):
                prev = a; continue
            prev = a
            if isinstance(a, str) and LS.match(a):
                continue
            keep2.append(r)
        if [sig(r) for r in keep2] != [sig(r) for r in rb]:
            n = sum(1 for x, y in zip(keep2, rb) if sig(x) != sig(y)) + abs(len(keep2) - len(rb))
            bad.append((sh, f'{n} other rows differ'))
        for C in ('', ' H', ' J'):
            lt, ls = f'LONG TIMELINE{C}', f'LONG STAR TIMELINE{C}'
            if not any(r[0].value == lt or (isinstance(r[0].value, str) and r[0].value.startswith(lt + ' (')) for r in ra):
                continue
            L, _, _ = blocks(ra, lt)
            S, cnt, title = blocks(ra, ls)
            if title is None:
                bad.append((sh, ls, 'missing')); continue
            n = {}
            for sec in ('SEPARATING', 'APPLYING'):
                want = [[c.value for c in r][1:] for r in L[sec] if isinstance(r[4].value, str) and isstar(r[4].value)]
                got = [[c.value for c in r][1:] for r in S[sec]]
                fw = [sig(r)[1:] for r in L[sec] if isinstance(r[4].value, str) and isstar(r[4].value)]
                fg = [sig(r)[1:] for r in S[sec]]
                if want != got or fw != fg:
                    bad.append((sh, ls, sec, len(want), len(got)))
                if cnt.get(sec) != len(got):
                    bad.append((sh, ls, sec, 'count', cnt.get(sec), len(got)))
                low = [g for g in got if g[9] is None or g[9] < 90]
                if low:
                    bad.append((sh, ls, sec, 'under 90', low[:1]))
                n[sec] = len(got)
            if not title.endswith(f": {n['SEPARATING'] + n['APPLYING']} events, {n['SEPARATING']} separating, {n['APPLYING']} applying"):
                bad.append((sh, ls, 'title', title[-60:]))
            print(f"{sh:12s} {ls:21s} {n['SEPARATING'] + n['APPLYING']:3d} ({n['SEPARATING']} / {n['APPLYING']})")
    print('mismatches:', len(bad))
    for x in bad[:10]:
        print('  ', x)
    return not bad


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
