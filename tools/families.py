#!/usr/bin/env python3
"""families.py - the number families, Eddie's definitions (13 Oct 2026). The single reference for every tool from now on.
Eddie's own scoring functions in rebuild_kit/active_vibrations.py are imported (not copied) wherever they exist.

  whole      whole numbers 1-200, +-0.02                               score_whole (squared)
  golden     every multiple of phi, +-0.03236, zero multiple not scored score_phi_interval (squared)
  phi power  phi^-1, phi^1..10, 10 phi^-1..7, 100 phi^-1, 100 phi       score_phi_powers (squared); 1/phi^2 forms dropped
  ninth      the 48 _NINTH_RANGES (lower <= v < upper, own tol)          score_ninth (linear). Not n/9.
  sqrt2      1.414, 14.14, 141.4, 0.707, 7.07, 70.7 - no multiples       tol max(0.5 % of target, 0.025), squared as phi powers
  silver     2.414, 24.14, 0.414, 4.14, 41.4 - no multiples              same
  conj       conjunction: RA < 1.5 or Dec < 0.3 (RA / Dec values only)   squared, as score_conjunction, on these tolerances
  interval   ratio values only (larger / smaller): NOT any p/q - Eddie's musical interval list (INTERVALS below, groups Perfect,
             Imperfect, Dissonant, Septimal, Harmonic, High, Phi), squared on each interval's own tolerance (interval_tol, Eddie
             13 Oct 2026, revised same day): unison 1 %; a whole-number interval 1 % / k, k = the whole number or the LARGER
             number of the fraction (2 -> 0.5 %; 3, 3/2 -> 0.333 %; 4, 4/3 -> 0.25 %; 5, 5/4, 5/3, 5/2 -> 0.2 %), 0.15 % when
             k >= 6 (6/5 and up); Phi group, sqrt2 and 1+1/sqrt2 0.15 %. Ratio values are scored against the interval list only; distances
             (degrees) against the other families only.
             Area A (Eddie, 15 Oct 2026): the whole-number intervals and 3/2 (AREA_A: 1, 3/2, 2, 3, 4, 5, 6, 7, 8, 9) are scored on
             +-0.02 ABSOLUTE (|ratio - interval| < 0.02, as whole-number distances, squared; offset shown in absolute units, no %).
             Area "φ and √2" (Eddie, 15 Oct 2026; AREA_P: φ, φ², φ³, 1+√2, √2, 1+1/√2), 0.15 % as before.
             Area B = every other interval, tapered % tolerances as above (interval_tol). area(label) -> 'A' / 'P' / 'B'.
Outside every tolerance: outside() gives the nearest target and its offset, plain text (nearest by tightness: the smallest offset in
units of the target's own tolerance, ratios and degrees alike).
Scores: squared (10 (tol - dev) / tol)^2 for whole, golden, phi powers, sqrt2, silver, conjunction and intervals; linear
100 (tol - dev) / tol for ninths.
Planes RA, Dec, Flat, GC. Decimal scaling: v, 10 v and v/10 are each tested against every family but conj (scaled() - labelled x10 / /10;
/10 widens a tolerance 10x in degrees). Score 0-100; colour green >= 80, yellow 50-80, light yellow < 50 (inside the bounds).
Best family = the highest score. No birth-day certainty for now."""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'rebuild_kit'))
from active_vibrations import (PHI, score_whole, score_phi_interval, score_phi_powers, score_ninth,  # noqa: E402
                               _PHI_POWER_TARGETS, _NINTH_RANGES)

R2 = math.sqrt(2.0)
SILVER = 1.0 + R2
SQRT2_T = [('1.414', R2), ('14.14', 10 * R2), ('141.4', 100 * R2), ('0.707', R2 / 2), ('7.07', 10 * R2 / 2), ('70.7', 100 * R2 / 2)]
SILVER_T = [('2.414', SILVER), ('24.14', 10 * SILVER), ('0.414', SILVER - 2), ('4.14', 10 * (SILVER - 2)), ('41.4', 100 * (SILVER - 2))]
CONJ = {'RA': 1.5, 'Dec': 0.3}
# Eddie's musical interval list (13 Oct 2026; groups and ratios as given; names: musical names as in docs/sky_dig.md l.840 where given,
# otherwise the usual just-intonation names - Eddie to correct). (ratio label, value, name, group)
INTERVALS = [
    ('1', 1.0, 'unison', 'Perfect'), ('2', 2.0, 'octave', 'Perfect'), ('3/2', 1.5, 'fifth', 'Perfect'),
    ('4/3', 4 / 3, 'fourth', 'Perfect'), ('3', 3.0, 'twelfth', 'Perfect'), ('4', 4.0, 'double octave', 'Perfect'),
    ('5/4', 1.25, 'major third', 'Imperfect'), ('6/5', 1.2, 'minor third', 'Imperfect'), ('5/3', 5 / 3, 'major sixth', 'Imperfect'),
    ('8/5', 1.6, 'minor sixth', 'Imperfect'), ('5/2', 2.5, 'major tenth', 'Imperfect'), ('8/3', 8 / 3, 'octave + fourth', 'Imperfect'),
    ('9/4', 2.25, 'major ninth', 'Imperfect'),
    ('√2', R2, 'tritone', 'Dissonant'), ('1+1/√2', 1 + 1 / R2, '√2 division partner', 'Dissonant'), ('9/8', 1.125, 'major second', 'Dissonant'),
    ('16/9', 16 / 9, 'minor seventh', 'Dissonant'), ('9/5', 1.8, 'minor seventh (5-limit)', 'Dissonant'),
    ('15/8', 1.875, 'major seventh', 'Dissonant'), ('16/15', 16 / 15, 'minor second', 'Dissonant'),
    ('7/4', 1.75, 'harmonic seventh', 'Septimal'), ('7/3', 7 / 3, 'septimal minor tenth', 'Septimal'),
    ('7/2', 3.5, 'septimal (octave + harmonic seventh)', 'Septimal'), ('7/5', 1.4, 'septimal tritone', 'Septimal'),
    ('7/6', 7 / 6, 'septimal minor third', 'Septimal'), ('8/7', 8 / 7, 'septimal whole tone', 'Septimal'),
    ('5', 5.0, '5th harmonic', 'Harmonic'), ('6', 6.0, '6th harmonic', 'Harmonic'), ('7', 7.0, '7th harmonic', 'Harmonic'),
    ('8', 8.0, '8th harmonic', 'Harmonic'), ('9', 9.0, '9th harmonic', 'Harmonic'),
    ('11/5', 2.2, 'undecimal 11:5', 'High'), ('11/6', 11 / 6, 'undecimal 11:6', 'High'), ('11/3', 11 / 3, 'undecimal 11:3', 'High'),
    ('11/8', 1.375, 'undecimal 11:8', 'High'), ('11/4', 2.75, 'undecimal 11:4', 'High'), ('13/5', 2.6, 'tridecimal 13:5', 'High'),
    ('13/8', 1.625, 'tridecimal 13:8', 'High'), ('13/4', 3.25, 'tridecimal 13:4', 'High'),
    ('φ', PHI, 'golden ratio', 'Phi'), ('φ²', PHI ** 2, 'φ squared', 'Phi'), ('φ³', PHI ** 3, 'φ cubed', 'Phi'),
    ('1+√2', SILVER, 'silver ratio', 'Phi'),               # Eddie 13 Oct: Phi group = φ, φ², φ³, 1+√2 only (φ√5, 2−1/φ, φ³+1, 2/φ removed)
]
INTERVAL_BY_LABEL = {i[0]: i for i in INTERVALS}
GROUPS = ('Perfect', 'Imperfect', 'Dissonant', 'Septimal', 'Harmonic', 'High', 'Phi')
INTERVAL_TOL = 0.15                                    # percent: the floor; Phi group, √2, 1+1/√2
AREA_A = ('1', '3/2', '2', '3', '4', '5', '6', '7', '8', '9')   # Eddie 15 Oct 2026: area A "whole + 3/2"
A_TOL = 0.02                                           # area A: +-0.02 absolute, as whole-number distances


AREA_P = ('φ', 'φ²', 'φ³', '1+√2', '√2', '1+1/√2')     # Eddie 15 Oct 2026: area "φ and √2" (0.15 %), between A and B
AREAS = ('A', 'P', 'B')                                # area order: A, φ and √2, B


def area(lab):
    """'A' (whole + 3/2), 'P' (φ and √2) or 'B' (every other interval on the list)"""
    return 'A' if lab in AREA_A else 'P' if lab in AREA_P else 'B'


def interval_tol(lab):
    """area A (Eddie, 15 Oct 2026): 0.02 ABSOLUTE. Area B: tolerance in percent (Eddie, 13 Oct 2026, revised): whole-number interval
    1 % / k (k = the larger number of the fraction: 4/3 -> 4, 13/4 -> 13), 0.15 % when k >= 6; Phi group, √2 and 1+1/√2 0.15 %"""
    if lab in AREA_A:
        return A_TOL
    if INTERVAL_BY_LABEL[lab][3] == 'Phi' or '√' in lab:
        return INTERVAL_TOL
    k = max(int(x) for x in lab.split('/'))
    return 1.0 / k if k <= 5 else INTERVAL_TOL


TOL = {lab: interval_tol(lab) for lab, *_ in INTERVALS}
GREEN, YELLOW = 80.0, 50.0
DEG_FAMILIES = ('whole', 'golden', 'phi power', 'ninth', 'sqrt2', 'silver', 'conj')
ORDER = DEG_FAMILIES + ('interval',)


def _phi_power_label(t):
    for lab, f in (('', 1.0), ('10', 10.0), ('100', 100.0)):
        for p in range(-1, 11):
            if abs(t - f * PHI ** p) < 1e-9:
                return f"{lab + '×' if lab else ''}φ^{p}"
    return f'{t:.4f}'


def _const(v, targets):
    """sqrt2 / silver: squared score on tol max(0.5 % of target, 0.025), as score_phi_powers"""
    best = (0.0, None, None)
    for lab, t in targets:
        tol = max(t * 0.005, 0.025)
        d = abs(v - t)
        if d <= tol:
            s = (10.0 * (tol - d) / tol) ** 2
            if s > best[0]:
                best = (s, lab, t)
    return best


def score_family(v, fam, plane=None, kind='deg'):
    """-> (score, label, target value) for one family; score 0 = outside it."""
    if v is None or v <= 0 and fam != 'conj':
        return 0.0, None, None
    if fam == 'whole':
        t = float(round(v))
        return score_whole(v), f'{int(t)}', t
    if fam == 'golden':
        k = round(v / PHI)
        return score_phi_interval(v), f'{k}×φ', k * PHI
    if fam == 'phi power':
        s = score_phi_powers(v)
        if not s:
            return 0.0, None, None
        t = max(_PHI_POWER_TARGETS, key=lambda t: (10.0 * (max(t * 0.005, 0.025) - abs(v - t)) / max(t * 0.005, 0.025)) ** 2
                if abs(v - t) <= max(t * 0.005, 0.025) else -1)
        return s, _phi_power_label(t), t
    if fam == 'ninth':
        for lo, hi, tol, t in _NINTH_RANGES:
            if lo <= v < hi:
                return score_ninth(v), f'{t:g}', t
        return 0.0, None, None
    if fam == 'sqrt2':
        return _const(v, SQRT2_T)
    if fam == 'silver':
        return _const(v, SILVER_T)
    if fam == 'conj':
        if plane not in CONJ or v >= CONJ[plane]:
            return 0.0, None, None
        tol = CONJ[plane]
        return (10.0 * (tol - v) / tol) ** 2, 'conj', 0.0
    if fam == 'interval':
        best = (0.0, None, None)
        for lab, t, name, grp in INTERVALS:
            dev = abs(v - t) if lab in AREA_A else abs(v / t - 1) * 100
            tol = TOL[lab]
            if dev < tol:
                sc = (10.0 * (tol - dev) / tol) ** 2
                if sc > best[0]:
                    best = (sc, lab, t)
        return best
    raise ValueError(fam)


def evaluate(v, plane=None, kind='deg'):
    """every family with a score > 0, best first -> [{'family', 'score', 'target', 'tv', 'off', 'pct', 'colour', 'name', 'group'}].
    kind 'deg' (distances, degrees): whole ... conj; kind 'ratio' / 'eqratio': the interval list only."""
    out = []
    for fam in (DEG_FAMILIES if kind == 'deg' else ('interval',)):
        s, lab, t = score_family(v, fam, plane, kind)
        if s > 0:
            pct = fam == 'interval' and lab not in AREA_A     # area A offsets are absolute (Eddie 15 Oct)
            off = (v / t - 1) * 100 if pct else v - t
            name, grp = (INTERVAL_BY_LABEL[lab][2:] if fam == 'interval' else ('', ''))
            out.append({'family': fam, 'score': s, 'target': lab, 'tv': t, 'off': off, 'pct': pct, 'colour': colour(s),
                        'name': name, 'group': grp})
    return sorted(out, key=lambda d: (-d['score'], ORDER.index(d['family'])))


def outside(v, plane=None, kind='deg'):
    """no family scores: the nearest target anyway, by tightness (Eddie, 13 Oct): the target with the smallest offset in units of its
    own tolerance, ratios and degrees alike (conjunction left out) ->
    {'family', 'target', 'tv', 'off', 'pct', 'tol', 'name', 'group'} or None. Plain text in the tables: no score, no colour."""
    if v is None or v <= 0:
        return None
    if kind != 'deg':
        cands = [('interval', lab, t, TOL[lab], name, grp) for lab, t, name, grp in INTERVALS]
    else:
        k = round(v / PHI)
        cands = [('whole', f'{round(v)}', float(round(v)), 0.02, '', ''), ('golden', f'{k}×φ', k * PHI, 0.03236, '', '')]
        cands += [('phi power', _phi_power_label(t), t, max(t * 0.005, 0.025), '', '') for t in _PHI_POWER_TARGETS]
        cands += [('ninth', f'{t:g}', t, tol, '', '') for lo, hi, tol, t in _NINTH_RANGES]
        cands += [(f, lab, t, max(t * 0.005, 0.025), '', '') for f, ts in (('sqrt2', SQRT2_T), ('silver', SILVER_T)) for lab, t in ts]
        cands = [c for c in cands if c[2] > 0]
    ispct = lambda c: c[0] == 'interval' and c[1] not in AREA_A          # area A ratios: absolute (Eddie 15 Oct)
    rel = lambda c: abs(v / c[2] - 1) * 100 / c[3] if ispct(c) else abs(v - c[2]) / c[3]
    c = min(cands, key=rel)
    f, lab, t, tol, name, grp = c
    pct = ispct(c)
    return {'family': f, 'target': lab, 'tv': t, 'off': (v / t - 1) * 100 if pct else v - t, 'pct': pct, 'tol': tol,
            'name': name, 'group': grp, 'score': None, 'colour': ''}


def best(v, plane=None, kind='deg'):
    ev = evaluate(v, plane, kind)
    return ev[0] if ev else None


def scaled(v, plane=None, kind='deg'):
    """decimal scaling: the best family of 10 v and of v / 10 (each with 'scale' 'x10' / '/10'), best first"""
    out = []
    for lab, f in (('x10', 10.0), ('/10', 0.1)):
        b = next((d for d in evaluate(v * f, plane, kind) if d['family'] != 'conj'), None)   # conjunction is not scaled
        if b:
            out.append(dict(b, scale=lab, scaled_value=v * f))
    return sorted(out, key=lambda d: -d['score'])


def colour(s):
    return 'green' if s >= GREEN else 'yellow' if s >= YELLOW else 'light' if s > 0 else ''


if __name__ == '__main__':
    for x in sys.argv[1:]:
        v = float(x)
        print(x, 'deg', evaluate(v, 'Dec'), scaled(v, 'Dec'))
        print(x, 'ratio', evaluate(v, kind='ratio'), scaled(v, kind='ratio'))
