"""Time tests/jupiter_tables_check.py test by test (Eddie, 31 Oct 2026).
usage: python3 tests/time_suite.py [--full] [--log <file>]
Runs the suite unbuffered with the given options, timestamps every line, and charges the wall clock between one test header
('Test 12 ...' / 'test 53: ...') and the next to that test (time before the first header = 'setup'). Prints every test's time, the
slowest 15 and the total, and the suite's own last line ('n/m passed')."""
import re, subprocess, sys, time

args = [a for a in sys.argv[1:] if a != '--log']
log = None
if '--log' in sys.argv:
    log = open(sys.argv[sys.argv.index('--log') + 1], 'w')
    args = [a for a in args if a != sys.argv[sys.argv.index('--log') + 1]]
t0 = time.time()
cur, start, spent, order, last = 'setup', t0, {}, ['setup'], ''
p = subprocess.Popen([sys.executable, '-u', 'tests/jupiter_tables_check.py'] + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
for ln in p.stdout:
    now = time.time()
    if log:
        log.write(f'{now - t0:8.1f}  {ln}')
        log.flush()
    m = re.match(r'^[Tt]est (\d+)\b', ln)
    if m:
        spent[cur] = spent.get(cur, 0) + now - start
        cur, start = f'test {int(m.group(1))}', now
        if cur not in order:
            order.append(cur)
    if ln.strip():
        last = ln.strip()
p.wait()
end = time.time()
spent[cur] = spent.get(cur, 0) + end - start
total = end - t0
print('per test (s):')
for k in order:
    print(f'  {k:10s} {spent[k]:8.1f}')
print('slowest 15:')
for k, v in sorted(spent.items(), key=lambda kv: -kv[1])[:15]:
    print(f'  {k:10s} {v:8.1f} s  ({100 * v / total:4.1f} %)')
print(f'total {total:.1f} s ({total / 60:.1f} min); suite: {last}; exit {p.returncode}')
sys.exit(p.returncode)
