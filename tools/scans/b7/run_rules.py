# Runs tools/eddie_rules.py; where a race's tables workbook is not on this machine, set A (register) selections and
# cells are taken unchanged from the committed rules json of that race (they depend on the workbook only).
import sys, os, json, subprocess, glob
ROOT='/home/claude/astro-harmonics'; sys.path.insert(0, ROOT+'/tools')
import eddie_rules as E
SETA=('R25','R28','R1b','R7','R26','R40','R42','R1')
orig_run=E.run
def run(json_path, rules):
    d=json.load(open(json_path)); wb=os.path.join(ROOT,'reference','classic',d['workbook'])
    if os.path.exists(wb): return orig_run(json_path, rules)
    key=E.race_key(json_path)
    old=json.loads(subprocess.check_output(['git','-C',ROOT,'show',f'HEAD:docs/eddie_read/rules/{key}_rules.json']))
    oldr={r['id']:r for r in old['rules']}
    saved={rid:E.RULES[rid] for rid in SETA}
    for rid in SETA: E.RULES[rid]=(lambda r: (lambda ctx: dict(r['cells'])))(oldr[rid])
    try: o=orig_run(json_path, rules)
    finally: E.RULES.update(saved)
    print('  set A from committed json:', key)
    return o
E.run=run
rules=json.load(open(ROOT+'/docs/eddie_read/rules.json'))['rules']
for p in sorted(glob.glob(ROOT+'/docs/eddie_read/*_eddie_read.json')):
    print(E.write(E.run(p, rules), ROOT+'/docs/eddie_read/rules', rules)+'.md')
