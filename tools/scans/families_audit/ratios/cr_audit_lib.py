import re
F=r"(\d+(?:/\d+)?)"
def ratios(it,w):
    if it==11:
        m=re.match(r'ratio '+F+':',w); return [m.group(1)] if m else None
    if it==15:
        m=re.search(r'H:J '+F+', H:S '+F+', J:S '+F,w); return list(m.groups())
    if it in (16,17,18):
        m=re.search(r'-> '+F+' : '+F+' : '+F,w); return list(m.groups())
    if it==19:
        m=re.search(r'(?:parts|span/other) '+F+r' \(',w); return [m.group(1)]
    if it==23:
        return re.findall(r' '+F+r' [\d.]+%\)',w)
    if it in (22,24,26):
        m=re.findall(r'(?:sky/natal|natal/sky|[A-Z]{1,2}/[A-Z]{1,2}) '+F+r' \(',w); return m
    return None
