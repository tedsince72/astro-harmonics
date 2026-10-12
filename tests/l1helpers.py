"""Helpers for Layer 1 expected-item files (tests/layer1_expect/<race>.py)."""
import json

def link(I,kind,a,b,pl=None,num=None,close=None):
    for l in I['links']:
        if l['kind']==kind and {l['a'],l['b']}=={a,b} or (l['kind']==kind and l['a']==a and l['b']==b):
            if num and l['nums'].get(pl,{}).get('num')!=num: continue
            if close and not l['close']: continue
            return True
    return False
def strike(I,sky,tgt,pl,num): return any(s['sky']==sky and s['target']==tgt and s['plane']==pl and s['num']==num for s in I['strikes'])
def move(I,c,b,pl,num): return any(m['chart']==c and m['body']==b and m['plane']==pl and m['num']==num for m in I['movement'])
def ratio(I,c,pair,pl,r): return any(x['chart']==c and x['pair']==pair and x['plane']==pl and x['ratio']==r for x in I['ratios'])
def same(I,b,pl,rs): return any(s['body']==b and s['plane']==pl and sorted(s['ratios'])==sorted(rs) for s in I['same_body'])
def eqpt(I,c,b,n): return any(p['chart']==c and p['body']==b and p['eq_num']==n for p in I['points'])
def eqr(I,b,pair,r,band): return any(e['body']==b and e['pair']==pair and e['ratio']==r and e['band']==band for e in I['eq_ratios'])
def shared(I,pair,pl): return any(s['pair']==pair and s['plane']==pl for s in I['shared'])
def pset(I,pair,pl): return any(s['pair']==pair and s['plane']==pl for s in I['pair_sets'])
def sky(race,pair,pl,num): return any(s['pair']==pair and s['plane']==pl and s['num']==num for s in json.load(open(f'docs/classic/{race}/layer1/sky.json')))

# order-insensitive pair matching (Layer 1 names pairs in BOD order, e.g. 'Uranus–Neptune', 'Chiron–Transpluto')
def _pm(p, q):
    a, b = p.split('–'); return p == q or f'{b}–{a}' == q
def ratio(I,c,pair,pl,r): return any(x['chart']==c and _pm(pair,x['pair']) and x['plane']==pl and x['ratio']==r for x in I['ratios'])
def shared(I,pair,pl): return any(_pm(pair,s['pair']) and s['plane']==pl for s in I['shared'])
def pset(I,pair,pl): return any(_pm(pair,s['pair']) and s['plane']==pl for s in I['pair_sets'])
def sky(race,pair,pl,num): return any(_pm(pair,s['pair']) and s['plane']==pl and s['num']==num for s in json.load(open(f'docs/classic/{race}/layer1/sky.json')))
def fam(I,c,pair,pl,r): return any(x['chart']==c and _pm(pair,x['pair']) and x['plane']==pl and x['ratio']==r for x in I['pair_family'])
def split(I,moved,to,pl): return any(x['moved']==moved and x['to']==to and x['plane']==pl for x in I['splits'])
def has_link(I,a,b,close=True):
    """any link (inside a chart or cross) between 'H X' / 'J Y' labels, either order"""
    return any({l['a'],l['b']}=={a,b} and (l['close'] or not close) for l in I['links'])
def linknum(I,a,b,pl,num): return any({l['a'],l['b']}=={a,b} and l['nums'].get(pl,{}).get('num')==num for l in I['links'])
# Planes: 'RA','Dec','Flat','GC' (the older tools' 'Sky' plane = 'GC'). Same-body planes also 'EqValue'. Charts 'H','J'; sky points chart 'S'.

# v1.4 helpers
def crossnear(I,a,b): return any(l['kind']=='cross' and {l['a'],l['b']}=={a,b} and l.get('near') for l in I['links'])
def contact(I,sky_,tgt,band=None): return any(x['sky']==sky_ and x['target']==tgt and (band is None or x['band']==band) for x in I['contacts'])
def hjr(I,pair,pl,r,band=None): return any(_pm(pair,x['pair']) and x['plane']==pl and x['ratio']==r and (band is None or x['band']==band) for x in I['hj_ratios'])
def skyclose(race,pair): return any(_pm(pair,x['pair']) for x in json.load(open(f'docs/classic/{race}/layer1/sky_close.json')))
def ratioband(I,c,pair,pl,r,band): return any(x['chart']==c and _pm(pair,x['pair']) and x['plane']==pl and x['ratio']==r and x['band']==band for x in I['ratios'])
