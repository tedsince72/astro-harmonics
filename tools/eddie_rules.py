#!/usr/bin/env python3
"""eddie_rules.py - stage 3 of Eddie's race read: run the rules. Never reads results.

Usage:  python3 tools/eddie_rules.py docs/eddie_read/<race>_eddie_read.json [more ...] [--rules docs/eddie_read/rules.json]
        [--out docs/eddie_read/rules]

For each race writes <race>_rules.md and <race>_rules.json: every rule in rules.json, the runners it selects, and the
cells that made each one qualify. Inputs: the stage 1 json (flags, pieces) and the race's tables workbook
(reference/classic/<workbook>, named in the json) for the register rules. Nothing is ranked or picked here; the
back-test (tools/eddie_backtest.py) is the only script that reads results.

Rules (Eddie, 7 Nov 2026: "create the rules for all of these"; text in rules.json):
  Set A  rules register R1-R42 (claude/isolation-log.md), computed by tools/race_rows.py rules_register from POSITIONS
         with families.py, exactly as written there: R25, R28, R1b, R7, R26, R40, R42, R1.
  Set B  from the stage 1 json:
         B1 every holder of the flag 'natal body on a strong line star' (a field filter)
         B2 the top score in that flag (ties: every runner on the top score)
         B3 version 4: 'hub landing' held by exactly one runner, else B2
         B4 most same-body cells scoring >= 50 (pieces layer 'same body', score >= 50), alone, lead >= 2
         B5 one natal body with same-body cells >= 50 in RA and in Dec on the same chart
         B6 one body with a same-body cell >= 50 on the horse chart and one on the jockey chart
A new rule: its entry in rules.json and a function in RULES below (takes the race context, returns {runner: [cells]}).
"""
import argparse
import contextlib
import io
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)


def race_key(path):
    b = os.path.basename(path)
    return b.replace('race_batch_', '').replace('_eddie_read.json', '')


# ---------------------------------------------------------------- set A (the register, via race_rows.py)
_REG = {}


def register(ctx):
    wb = ctx['workbook']
    if wb not in _REG:
        import race_rows
        with contextlib.redirect_stdout(io.StringIO()):
            _REG[wb] = race_rows.rules_register(wb)
    return _REG[wb]


def reg_rule(rid):
    def f(ctx):
        reg = register(ctx)
        out = defaultdict(list)
        for line in reg['out'].get(rid, []):
            R = line.strip().split(' ', 1)[0]
            pre = f"  {R} {reg['names'].get(R, '')[:30]}: "
            out[R].append(line[len(pre):] if line.startswith(pre) else line)
        assert sorted(out) == sorted(reg['picked'].get(rid, [])), rid
        return dict(out)
    return f


# ---------------------------------------------------------------- set B (stage 1 json)
def b1(ctx):
    out = defaultdict(list)
    for c in ctx['d']['flags'].get('natal body on a strong line star', []):
        out[c['runner']].append(c['text'])
    return dict(out)


def b2(ctx):
    cs = ctx['d']['flags'].get('natal body on a strong line star', [])
    if not cs:
        return {}
    top = max(round(c['score'], 6) for c in cs)
    out = defaultdict(list)
    for c in cs:
        if round(c['score'], 6) == top:
            out[c['runner']].append(c['text'] + ' (top score in the field)')
    return dict(out)


def b3(ctx):
    hl = ctx['d']['flags'].get('hub landing', [])
    holders = sorted({c['runner'] for c in hl})
    if len(holders) == 1:
        return {holders[0]: ['step 1, hub landing held alone: ' + c['text'] for c in hl]}
    return {R: ['step 2: ' + t for t in v] for R, v in b2(ctx).items()}


def same_body(ctx):
    """runner -> list of same-body pieces scoring >= 50."""
    sb = defaultdict(list)
    for p in ctx['d']['pieces']:
        if p['layer'] == 'same body' and p.get('score') is not None and p['score'] >= 50:
            sb[p['runner']].append(p)
    return sb


def sbtxt(p):
    tf = f"conj ({p['score']:.2f})" if p['family'] == 'conj' else f"{p['target']} {p['family']} ({p['score']:.2f})"
    return f"{p['source']} → {p['chart']} {p['body']} {p['plane']} {p['value']:.4f} {tf}"


def b4(ctx):
    sb = same_body(ctx)
    n = sorted(((len(sb.get(R, [])), R) for R in ctx['d']['runners']), reverse=True)
    if not n or n[0][0] == 0:
        return {}
    lead = n[0][0] - (n[1][0] if len(n) > 1 else 0)
    if lead < 2:
        return {}
    R = n[0][1]
    nxt = f"next {n[1][0]} ({ctx['d']['names'].get(n[1][1], n[1][1])})" if len(n) > 1 else 'no other runner'
    return {R: [f"{n[0][0]} same-body cells >= 50, {nxt}, lead {lead}"] + [sbtxt(p) for p in sb[R]]}


def b5(ctx):
    out = defaultdict(list)
    for R, ps in same_body(ctx).items():
        by = defaultdict(dict)
        for p in ps:
            by[(p['chart'], p['body'])].setdefault(p['plane'], p)
        for (ch, X), pl in sorted(by.items()):
            if 'RA' in pl and 'Dec' in pl:
                out[R].append(f"{ch} {X}: {sbtxt(pl['RA'])} | {sbtxt(pl['Dec'])}")
    return dict(out)


def b6(ctx):
    out = defaultdict(list)
    for R, ps in same_body(ctx).items():
        by = defaultdict(lambda: defaultdict(list))
        for p in ps:
            by[p['body']][p['chart']].append(p)
        for X, ch in sorted(by.items()):
            if ch.get('H') and ch.get('J'):
                out[R].append(f"{X}: " + '; '.join(sbtxt(p) for p in ch['H']) + ' | ' + '; '.join(sbtxt(p) for p in ch['J']))
    return dict(out)


RULES = {rid: reg_rule(rid) for rid in ('R25', 'R28', 'R1b', 'R7', 'R26', 'R40', 'R42', 'R1')}
RULES.update(B1=b1, B2=b2, B3=b3, B4=b4, B5=b5, B6=b6)


def run(json_path, rules):
    d = json.load(open(json_path))
    wb = os.path.join(ROOT, 'reference', 'classic', d['workbook'])
    if not os.path.exists(wb):
        wb = os.path.join(os.path.dirname(json_path), d['workbook'])
    ctx = dict(d=d, workbook=wb)
    res = []
    for r in rules:
        sel = RULES[r['id']](ctx)
        res.append(dict(id=r['id'], name=r['name'], selected=sorted(sel), cells={R: sel[R] for R in sorted(sel)}))
    return dict(race=race_key(json_path), workbook=d['workbook'], runners=d['runners'], names=d['names'], rules=res)


def write(o, out_dir, rules):
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.join(out_dir, f"{o['race']}_rules")
    json.dump(o, open(base + '.json', 'w'), indent=1, ensure_ascii=False)
    nm = o['names']
    L = [f"# Stage 3 rules: {o['race']}", '',
         f"Workbook {o['workbook']}. Runners {len(o['runners'])}. Results not read. Rule text: docs/eddie_read/rules.json.", '',
         '## Per rule', '']
    text = {r['id']: r['text'] for r in rules}
    for r in o['rules']:
        sel = ', '.join(nm.get(R, R) for R in r['selected']) or 'none'
        L.append(f"- **{r['id']} {r['name']}** ({len(r['selected'])} of {len(o['runners'])}): {sel}")
    L += ['', '## Per runner', '']
    for R in o['runners']:
        ids = [r['id'] for r in o['rules'] if R in r['selected']]
        L.append(f"- {nm.get(R, R)}: {', '.join(ids) if ids else 'none'}")
    L += ['', '## Cells', '']
    for r in o['rules']:
        L.append(f"### {r['id']} {r['name']}")
        L.append(f"_{text[r['id']]}_")
        if not r['selected']:
            L.append('- none')
        for R in r['selected']:
            L.append(f"- {nm.get(R, R)}")
            for c in r['cells'][R]:
                L.append(f"  - {c}")
        L.append('')
    open(base + '.md', 'w').write('\n'.join(L) + '\n')
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('json', nargs='+')
    ap.add_argument('--rules', default=os.path.join(ROOT, 'docs', 'eddie_read', 'rules.json'))
    ap.add_argument('--out', default=os.path.join(ROOT, 'docs', 'eddie_read', 'rules'))
    a = ap.parse_args()
    rules = json.load(open(a.rules))['rules']
    for r in rules:
        if r['id'] not in RULES:
            sys.exit(f"rule {r['id']} in rules.json has no function in tools/eddie_rules.py")
    for p in a.json:
        b = write(run(p, rules), a.out, rules)
        print(b + '.md')


if __name__ == '__main__':
    main()
