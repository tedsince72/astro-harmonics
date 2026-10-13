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
  ratio      simple p/q (p <= 30, q <= 9, p/q not a whole number, not 1) for ratio values only; linear on its own tolerance
             (0.005 %; Equator ratios 0.01 %)
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
FRACS = sorted({(p // math.gcd(p, q), q // math.gcd(p, q)) for q in range(2, 10) for p in range(1, 31)
                if p % q and p > q})
RATIO_TOL = {'ratio': 0.005, 'eqratio': 0.01}          # percent
GREEN, YELLOW = 80.0, 50.0
ORDER = ('whole', 'golden', 'phi power', 'ninth', 'sqrt2', 'silver', 'conj', 'ratio')


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
    """-> (score, label, target value) for one family; score 0 = outside it. kind 'deg' or 'ratio' / 'eqratio'."""
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
        if kind != 'deg' or plane not in CONJ or v >= CONJ[plane]:
            return 0.0, None, None
        tol = CONJ[plane]
        return (10.0 * (tol - v) / tol) ** 2, 'conj', 0.0
    if fam == 'ratio':
        if kind not in RATIO_TOL:
            return 0.0, None, None
        tol = RATIO_TOL[kind]
        best = (0.0, None, None)
        for p, q in FRACS:
            off = abs(v / (p / q) - 1) * 100
            if off < tol and 100.0 * (tol - off) / tol > best[0]:
                best = (100.0 * (tol - off) / tol, f'{p}/{q}', p / q)
        return best
    raise ValueError(fam)


def evaluate(v, plane=None, kind='deg'):
    """every family with a score > 0, best first -> [{'family', 'score', 'target', 'tv', 'off', 'pct', 'colour'}]"""
    out = []
    for fam in ORDER:
        s, lab, t = score_family(v, fam, plane, kind)
        if s > 0:
            pct = fam == 'ratio'
            off = (v / t - 1) * 100 if pct else v - t
            out.append({'family': fam, 'score': s, 'target': lab, 'tv': t, 'off': off, 'pct': pct, 'colour': colour(s)})
    return sorted(out, key=lambda d: (-d['score'], ORDER.index(d['family'])))


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
        print(x, evaluate(v, 'Dec'), scaled(v, 'Dec'))
