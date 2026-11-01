"""edge scan: scores within 0.005 of 50, sky-score ties at 2 dp (own model)"""
import sys
import openpyxl
import lib as L
for f in sys.argv[1:]:
    wa = openpyxl.load_workbook(f); errs = []
    pos, kind = L.positions(wa)
    sky = {sec: L.sky_cells(wa, pos, kind, c, sh, errs) for sec, c, sh in L.SECTIONS}
    near = [(sec, s.rel, s.plane, s.score) for sec in sky for s in sky[sec] if abs(s.score - 50) < 0.005]
    ties = [(sec, a.rel, a.plane, b.rel, b.plane) for sec in sky for i, a in enumerate(sky[sec]) for b in sky[sec][i+1:] if round(a.score, 2) == round(b.score, 2)]
    tn = 0
    for p in [s for s in wa.sheetnames if s[:1] == 'P' and s[1:].isdigit()]:
        for side in 'HJ':
            tn += sum(1 for t in L.t24_cells(wa, pos, p, side, errs) if abs(t.score - 50) < 0.005)
    print(f, 'sky near 50:', near, '| T24 near 50:', tn, '| sky 2-dp ties:', ties, '| errs', len(errs))
