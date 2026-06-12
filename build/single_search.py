# -*- coding: utf-8 -*-
"""Vervang de meerdelige .search--light formulieren door één zoekbalk."""
import re, os, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SINGLE = ('<form class="search search--light search--single" onsubmit="return false">'
  '<label class="seg"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>'
  '<input type="text" placeholder="Zoek op plaats, adres, type of trefwoord…" data-i18n-ph="search.phloc" aria-label="Zoeken"></label>'
  '<button class="search-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg> <span data-i18n="search.btn">Zoeken</span></button></form>')
pat = re.compile(r'<form class="search search--light"[^>]*>.*?</form>', re.S)
n = 0
for f in glob.glob(os.path.join(ROOT, '*.html')):
    s = open(f, encoding='utf-8').read()
    if pat.search(s) and 'search--single' not in pat.search(s).group(0):
        s2 = pat.sub(SINGLE, s)
        if s2 != s:
            open(f, 'w', encoding='utf-8').write(s2); n += 1; print('single search:', os.path.basename(f))
print('done', n)
