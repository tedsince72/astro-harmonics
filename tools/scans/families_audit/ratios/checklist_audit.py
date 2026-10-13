import sys,os,collections
sys.path.insert(0,os.path.dirname(__file__))
from intervals import on_list,frac
from checklist_cites import C
on=off=0; rows=[]; byitem=collections.Counter()
for l in C.strip().splitlines():
    a=l.split('|'); it,ln,race=a[:3]; rs=a[-1].split(','); what='|'.join(a[3:-1])
    bad=[x for x in rs if not on_list(frac(x))]
    for x in rs:
        if on_list(frac(x)): on+=1
        else: off+=1
    byitem[(it,'entries_off' if bad else 'entries_on')]+=1
    rows.append((it,ln,race,what,','.join(rs),'OFF: '+','.join(bad) if bad else 'on'))
D=os.path.dirname(__file__)
with open(os.path.join(D,'checklist_offlist.txt'),'w') as o:
    print('item\tline\trace\twhat\tratios\tverdict',file=o)
    for r in rows: print('\t'.join(r),file=o)
    print(f'\nratio values cited: on list {on}, off list {off}',file=o)
    for k in sorted(set(i for i,_ in byitem),key=str): print(k,'entries on',byitem[(k,'entries_on')],'off',byitem[(k,'entries_off')],file=o)
print(on,off,len(rows))
for k in sorted(set(i for i,_ in byitem),key=str): print(k,'on',byitem[(k,'entries_on')],'off',byitem[(k,'entries_off')])
