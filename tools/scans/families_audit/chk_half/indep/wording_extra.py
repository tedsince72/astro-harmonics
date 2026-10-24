"""Extra for check_wording.py: (1) shapes of every text mentioning 'outside' / '4-digit' that is not a distance nearest-target form
(numbers -> #), so no distance text escapes; (2) per-block counts of the two forms (column A id); (3) 'not a 4-digit' in the before
workbook. usage: wording_extra.py <after2.xlsx> <after.xlsx>"""
import sys, re, collections, openpyxl
FAM = r'(whole|half|golden|phi power|ninth|sqrt2|silver)'
FORMS = [re.compile(p) for p in (rf'^(\S+) \({FAM}\) — outside ±(\S+)$', rf'^nearest: (\S+) · {FAM} — outside ±(\S+) · ([+-]\d+\.\d{{5}})$',
         rf'^(\S+) \({FAM}\) — outside$', r'^(\S+) ([+-]\d+\.\d{5}) \(outside ±(\S+)\)$',
         rf'^(nearest: )?(\S+) {FAM} — not a 4-digit match \(([+-]\d+\.\d{{5}})\)$')]
RATIO_FIELD = re.compile(r'^FIELD (12|13|14|21|22|23)R?$')
LOOSE = re.compile(r'outside|4-digit')
wb = openpyxl.load_workbook(sys.argv[1])
shapes = collections.Counter(); ex = {}; blocks = collections.Counter()
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            for where, s in (('cell', c.value if isinstance(c.value, str) else None), ('comment', c.comment.text.split('\n')[0] if c.comment else None)):
                if not s or not LOOSE.search(s):
                    continue
                isform = any(p.match(s) for p in FORMS) and not RATIO_FIELD.match(ws.title)
                if isform:
                    a = ws.cell(c.row, 1).value
                    blk = ws.title if ws.title.startswith('FIELD') else f"{'SKY' if ws.title == 'SKY JUPITER' else 'P##'} {a}"
                    blocks[(blk, where, 'not 4-digit' if '4-digit' in s else 'outside')] += 1
                    continue
                k = (ws.title if ws.title.startswith('FIELD') or ws.title == 'SKY JUPITER' else 'P##', where, re.sub(r'[-+]?\d[\d.]*', '#', s)[:70])
                shapes[k] += 1; ex.setdefault(k, (ws.title, c.coordinate, s[:120]))
print(sys.argv[1])
print('  other texts with outside / 4-digit (not distance nearest-target forms), shapes:')
for k, n in shapes.most_common():
    print(f'   {n:6d} {k}  e.g. {ex[k]}')
print('  forms per block:')
for k, n in sorted(blocks.items()):
    print(f'   {k} {n}')
wb0 = openpyxl.load_workbook(sys.argv[2]); n0 = 0
for ws in wb0.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if (isinstance(c.value, str) and '4-digit' in c.value) or (c.comment and '4-digit' in c.comment.text):
                n0 += 1
print('  "4-digit" texts in the before workbook:', n0)
