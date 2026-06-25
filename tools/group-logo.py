#!/usr/bin/env python3
"""Raggruppa l'autotrace del logo WaYdotNET in 4 layer (emblem/wordmark/tagline/quote)
per fascia verticale (coordinata y, viewBox 1024x1024), preservando ogni elemento invariato.

Uso: python3 group-logo.py INPUT.svg OUTPUT.svg
Il calcolo della fascia usa un parser dei comandi path che IGNORA i flag degli archi
(altrimenti i flag 0/1 verrebbero scambiati per coordinate e falserebbero la classificazione).
"""
import re, sys


_TOK = re.compile(r'[MmLlHhVvCcSsQqTtAaZz]|-?\d*\.?\d+(?:e-?\d+)?')
_NARGS = {'m': 2, 'l': 2, 'h': 1, 'v': 1, 'c': 6, 's': 4, 'q': 4, 't': 2, 'a': 7, 'z': 0}


def path_points(d):
    """Punti (x, y) lungo il path, ignorando i flag degli archi."""
    toks = _TOK.findall(d); i = 0; pts = []; x = y = 0.0; sx = sy = 0.0; cmd = None
    while i < len(toks):
        t = toks[i]
        if t.isalpha(): cmd = t; i += 1
        if cmd is None: i += 1; continue
        c = cmd.lower(); rel = cmd.islower(); n = _NARGS[c]
        if c == 'z': x, y = sx, sy; pts.append((x, y)); continue
        args = toks[i:i + n]; i += n
        if len(args) < n: break
        a = [float(v) for v in args]
        if c == 'h': x = (x + a[0]) if rel else a[0]
        elif c == 'v': y = (y + a[0]) if rel else a[0]
        elif c == 'a': nx, ny = a[5], a[6]; x = (x + nx) if rel else nx; y = (y + ny) if rel else ny
        else: nx, ny = a[n - 2], a[n - 1]; x = (x + nx) if rel else nx; y = (y + ny) if rel else ny
        if c == 'm': sx, sy = x, y
        pts.append((x, y))
    return pts


def cy_of(d):
    pts = path_points(d)
    ys = [p[1] for p in pts]
    return sum(ys) / len(ys) if ys else 0


def is_white_fill(attrs):
    """True se l'elemento è un riempimento bianco. Il logo originale è trasparente:
    tutti i bianchi dell'autotrace (sfondo a tutta tela + disco/spazi interni) vanno
    rimossi, così l'avorio della pagina traspare dietro le forme inchiostrate."""
    return bool(re.search(r'fill="(#fff|#ffffff|white|#FFF)"', attrs))


def main(inp, outp):
    src = open(inp).read()
    svgopen = re.search(r'<svg[^>]*>', src).group(0)
    if 'role=' not in svgopen:
        svgopen = svgopen[:-1] + ' role="img" aria-label="WaYdotNET — Architect · Enable · Simplify">'
    pat = re.compile(r'<(path|ellipse|circle|rect)\b(.*?)/?>', re.S)
    groups = {k: [] for k in ['emblem', 'wordmark', 'tagline', 'quote']}
    dropped = 0
    for m in pat.finditer(src):
        tag, attrs, full = m.group(1), m.group(2), m.group(0)
        if is_white_fill(attrs):
            dropped += 1; continue  # scarta i riempimenti bianchi (logo trasparente)
        if tag == 'path':
            d = re.search(r'd="(.*?)"', attrs, re.S)
            cy = cy_of(d.group(1)) if d else 0
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
    print('scritto', outp, '— gruppi:', {k: len(v) for k, v in groups.items()}, '— sfondo bianco scartato:', dropped)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
