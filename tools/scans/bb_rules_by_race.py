"""Per BB rule, per race: holders / field, W when the winner holds it, (o) = the rule's origin race.
"Later races" = races read after the rule was made (order Lingfield, Haydock, Beverley, York 15:45, York 16:15); Catterick never counts there.
Winners are the known ones written in CLAUDE.md (no results file read). Chelmsford AW 13:20 2024 left out (no winner on record here).
Writes docs/eddie_read/bybody_rules/rules_by_race.md."""
import json, sys
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield 14:35 2021', '20210402_lingfield_aw_1435', 'Pholas'),
         ('Haydock 13:45 2020', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley 14:05 2024', '20240608_beverley_1405', 'Perfect Part'),
         ('York 15:45 2024', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15 2024', '20240515_york_1615', 'Diligent Resdev'),
         ('Catterick 14:40 2022', '20220406_catterick_1440', 'Wotever Next')]
def num(i): return int(''.join(c for c in i[2:] if c.isdigit()))
def origin(i):
    k = num(i)
    return 0 if k <= 17 else 1 if k <= 31 else 2 if k <= 40 else 3 if k <= 50 else 4
ids = [r for r, _, _ in E.RULES]; body = {r: b for r, _, b in E.RULES}
data = []
for n, r, w in races:
    N = len(E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'))
    J = json.load(open(f'docs/eddie_read/bybody_rules/{r}_bbrules.json'))['rules']
    data.append((n, N, w, J))
hdr = ['Rule', 'Body'] + [n for n, *_ in races] + ['Later races: picks', 'winners', 'by chance', 'Winner alone']
out = ['| ' + ' | '.join(hdr) + ' |', '|' + '---|' * len(hdr)]
tot = [0, 0, 0.0]
for i in ids:
    cells = []; P = Wn = 0; C = 0.0; alone = []
    for k, (n, N, w, J) in enumerate(data):
        h = {x['runner'] for x in J.get(i, [])}
        won = any(w in x for x in h)
        o = (k == origin(i))
        c = '–' if not h else f"{len(h)}/{N}{' **W**' if won else ''}"
        if o: c += ' (o)'
        cells.append(c)
        if won and len(h) == 1: alone.append(' '.join(n.split(' ')[:2]) if n.startswith('York') else n.split(' ')[0] + (' (o)' if o else ''))
        if k > origin(i) and k < 5 and h: P += len(h); Wn += won; C += len(h) / N
    tot[0] += P; tot[1] += Wn; tot[2] += C
    out.append(f"| {i} | {body[i]} | " + ' | '.join(cells) + f" | {P} | {Wn} | {C:.1f} | {', '.join(alone) or '–'} |")
out.append(f"\nAll rules, later races (read after the rule was made; Catterick not counted, its winner was known): {tot[0]} picks, {tot[1]} winners, {tot[2]:.1f} by chance.")
open('docs/eddie_read/bybody_rules/rules_by_race.md', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
