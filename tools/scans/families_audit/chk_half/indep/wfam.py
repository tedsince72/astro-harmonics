"""Wording rule (Eddie, 24 Oct 2026), own code on fam.py: a value with no family hit whose nearest target is inside that family's
OLD tolerance (old score > 0 on that target) but fails the 4-digit match -> 'not a 4-digit match'; otherwise the old 'outside' text."""
from fam import *          # noqa
from fam import fams, outside, colour, offs, CONJ, NINTHS, dmatch, sq


def old_inside(v, fam, t, tol):
    """old score > 0 on that target (old tolerance), True / False"""
    if fam == 'golden':
        return abs(v - t) < 0.03236
    if fam in ('phi power', 'sqrt2', 'silver'):
        return abs(v - t) <= tol and sq(tol, abs(v - t)) > 0
    if fam == 'ninth':
        for lo, hi, nt, tt in NINTHS:
            if tt == t and nt == tol:
                return lo <= v < hi and 100.0 * (nt - abs(v - tt)) / nt > 0
        raise ValueError(t)
    return False                       # whole, half: no digit rule


def nearest_form(v):
    """('notdigit' | 'outside', fam, lab, t, tol)"""
    fam, lab, t, tol = outside(v, True)
    if old_inside(v, fam, t, tol):
        if dmatch(v, t):
            return 'HIT', fam, lab, t, tol     # inside and 4-digit: a family hit, no nearest text expected
        return 'notdigit', fam, lab, t, tol
    return 'outside', fam, lab, t, tol


def target_text(v, plane, new=True):
    f = fams(v, plane, True)
    if f:
        s, fam, lab, t = f[0]
        return f'{lab} ({fam})', offs(v - t), round(s, 2), colour(s), f
    o = outside(v, True)
    if not o:
        return None, None, None, '', f
    form, fam, lab, t, tol = nearest_form(v)
    if form == 'notdigit':
        return f'{lab} {fam} — not a 4-digit match ({offs(v - t)})', offs(v - t), None, '', f
    return f'{lab} ({fam}) — outside ±{tol:.3g}', offs(v - t), None, '', f


def t24_comment(v, plane, new=True):
    f = fams(v, plane, True)
    if f:
        s, fam, lab, t = f[0]
        if fam == 'conj':
            return f'0 · conjunction ({plane} < {CONJ[plane]}) · {offs(v)} · {s:.2f}', colour(s), f
        return f'{lab} · {fam} · {offs(v - t)} · {s:.2f}', colour(s), f
    form, fam, lab, t, tol = nearest_form(v)
    if form == 'notdigit':
        return f'nearest: {lab} {fam} — not a 4-digit match ({offs(v - t)})', '', f
    return f'nearest: {lab} · {fam} — outside ±{tol:.3g} · {offs(v - t)}', '', f
