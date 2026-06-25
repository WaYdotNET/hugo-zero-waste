#!/usr/bin/env python3
"""Raggruppa l'autotrace del logo WaYdotNET in 4 layer (emblem/wordmark/tagline/quote)
per fascia verticale (coordinata y, viewBox 1024x1024), preservando ogni elemento invariato.

Uso: python3 group-logo.py INPUT.svg OUTPUT.svg
Il calcolo della fascia usa un parser dei comandi path che IGNORA i flag degli archi
(altrimenti i flag 0/1 verrebbero scambiati per coordinate e falserebbero la classificazione).
"""
import re, sys


def cy_of(d):
    tok = re.compile(r'[MmLlHhVvCcSsQqTtAaZz]|-?\d*\.?\d+(?:e-?\d+)?')
    NARGS = {'m': 2, 'l': 2, 'h': 1, 'v': 1, 'c': 6, 's': 4, 'q': 4, 't': 2, 'a': 7, 'z': 0}
    toks = tok.findall(d); i = 0; ys = []; y = 0.0; sy = 0.0; cmd = None
    while i < len(toks):
        t = toks[i]
        if t.isalpha(): cmd = t; i += 1
        if cmd is None: i += 1; continue
        c = cmd.lower(); rel = cmd.islower(); n = NARGS[c]
        if c == 'z': y = sy; ys.append(y); continue
        args = toks[i:i + n]; i += n
        if len(args) < n: break
        a = [float(v) for v in args]
        if c == 'h': pass
        elif c == 'v': y = (y + a[0]) if rel else a[0]
        elif c == 'a': ny = a[6]; y = (y + ny) if rel else ny
        else: ny = a[n - 1]; y = (y + ny) if rel else ny
        if c == 'm': sy = y
        ys.append(y)
    return sum(ys) / len(ys) if ys else 0


def main(inp, outp):
    src = open(inp).read()
    svgopen = re.search(r'<svg[^>]*>', src).group(0)
    if 'role=' not in svgopen:
        svgopen = svgopen[:-1] + ' role="img" aria-label="WaYdotNET — Architect · Enable · Simplify">'
    pat = re.compile(r'<(path|ellipse|circle|rect)\b(.*?)/?>', re.S)
    groups = {k: [] for k in ['emblem', 'wordmark', 'tagline', 'quote']}
    for m in pat.finditer(src):
        tag, attrs, full = m.group(1), m.group(2), m.group(0)
        if tag == 'path':
            d = re.search(r'd="(.*?)"', attrs, re.S); cy = cy_of(d.group(1)) if d else 0
        else:
            tr = re.search(r'translate\(([\-\d.]+),([\-\d.]+)\)', attrs)
            if tr:
                cy = float(tr.group(2))
            else:
                mm = re.search(r'cy="([\-\d.]+)"', attrs) or re.search(r'\by="([\-\d.]+)"', attrs)
                cy = float(mm.group(1)) if mm else 0
        k = 'quote' if cy > 868 else 'tagline' if cy > 812 else 'wordmark' if cy > 650 else 'emblem'
        groups[k].append(full)
    out = [svgopen]
    for k in ['emblem', 'wordmark', 'tagline', 'quote']:
        out.append('<g id="%s" stroke-width="2" fill="none" stroke-linecap="butt">' % k)
        out += groups[k]
        out.append('</g>')
    out.append('</svg>')
    open(outp, 'w').write('\n'.join(out))
    print('scritto', outp, '— gruppi:', {k: len(v) for k, v in groups.items()})


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
