"""dmatch SCFILE: sky body's chords (at the off and through the whole day) matched to Messi natal (20:30) star strings (dett/*.txt)."""
import re,glob,os,collections,sys
S='/home/claude/tools'
pat=re.compile(r"^\s+(RA|Dec|Flat|Sky)\s+(.+?)–(.+?)\s+base.*?\s(\S+)\s+([\d.]+)%\s+\[00:00\s+(\S+)\s+24:00\s+(\S+)\]")
nat=collections.defaultdict(list)
for f in glob.glob(S+'/fnat/*.txt'):
    b=os.path.basename(f)[:-4]; sec=None
    for line in open(f):
        if line.startswith('WITH THE STARS'): sec='star'
        elif line.startswith('WITH TWO'): sec=None
        m=pat.match(line)
        if m and sec:
            mm,a,c,t,d,d0,d24=m.groups()
            allday = d0!='-' and d24!='-' and float(d0.rstrip('%'))<=0.15 and float(d24.rstrip('%'))<=0.15
            nat[(mm,frozenset([a.strip(),c.strip()]))].append(f"{b} {t} {d}%{' ALLDAY' if allday else ''}")
off=re.compile(r"^\s+(.+?)–(.+?)\s+base\s.*?\s([\d.]+)%\s+\[.*\]\s+(.*)$")
day=re.compile(r"^\s+(\d+:\d+:\d+)\s+(RA|Dec|Flat|Sky)\s+(.+?)–(.+?)\s+base.*?\s(\S+)\s+([\d.]+)%$")
mm=None; inday=False
print("AT THE OFF:")
for line in open(sys.argv[1]):
    if line.startswith('THE WHOLE DAY'): inday=True; print("WHOLE DAY:"); continue
    h=re.match(r"^(RA|Dec|Flat|Sky): ",line)
    if h: mm=h.group(1); continue
    if not inday:
        m=off.match(line)
        if m and mm:
            a,c,d,w=m.groups(); k=(mm,frozenset([a.strip(),c.strip()]))
            if k in nat: print(f"  {mm} {a.strip()}–{c.strip()} {d}% {w[-60:]} | {' ; '.join(nat[k])}")
    else:
        m=day.match(line)
        if m:
            t,m2,a,c,typ,d=m.groups(); k=(m2,frozenset([a.strip(),c.strip()]))
            if k in nat : print(f"  {t} {m2} {a.strip()}–{c.strip()} {typ} | {' ; '.join(x for x in nat[k])}")
