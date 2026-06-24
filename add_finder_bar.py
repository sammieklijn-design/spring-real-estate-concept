"""
add_finder_bar.py  (v3)
========================
- listings.html  → stap-voor-stap collapsible finder (blijft)
- index.html     → zoekbalk IN de hero (na de stats)
- alle andere    → site-search-bar wordt verwijderd, niets toegevoegd
- Bumpt CSS/JS versie naar v=25

NOOIT PowerShell voor HTML bestanden!
"""
import os, glob, re

REPO = os.path.dirname(os.path.abspath(__file__))
VERSION = '25'

# ── Zoekbalk in homepage hero (na .hero-stats) ──────────────────────────────

HERO_SEARCH = (
    '\n    <form class="hero-search" onsubmit="return false">\n'
    '      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>\n'
    '      <input type="text" class="hs-input" placeholder="Zoek een object, locatie of dienst&hellip;" aria-label="Zoeken">\n'
    '      <button type="submit" class="hs-btn">Zoeken</button>\n'
    '    </form>\n'
)

def remove_old_bars(text):
    """Verwijder eerder geplaatste site-search-bar en finder-bar van niet-listings."""
    # site-search-bar blok
    text = re.sub(
        r'<!-- ZOEKBALK -->\n<div class="site-search-bar">.*?</div>\n',
        '', text, flags=re.DOTALL
    )
    # finder-bar blok met script
    text = re.sub(
        r'<!-- FINDER BAR.*?</script>\n',
        '', text, flags=re.DOTALL
    )
    # oude vf-bar / obj-finder-bar
    text = re.sub(r'<div class="vf-bar">.*?</div>\s*\n', '', text, flags=re.DOTALL)
    text = re.sub(r'<div class="obj-finder-bar">.*?</div>\s*\n', '', text, flags=re.DOTALL)
    return text

def add_hero_search(text):
    """Voeg zoekbalk toe IN homepage hero na de stats div."""
    if 'hero-search' in text:
        return text
    # Zoek het einde van .hero-stats en voeg daarna de zoekbalk toe
    text = re.sub(
        r'(</div>\n    </div>\n  </div>\n</section>)(\s*\n<!-- ={8,} VASTGOEDZOEKER)',
        r'\1' + HERO_SEARCH.rstrip('\n') + r'\2',
        text, count=1
    )
    # Alternatief: zoek het hero-stats afsluiten direct voor </section>
    if 'hero-search' not in text:
        text = text.replace(
            'jaar ervaring</span></div>\n    </div>\n  </div>\n</section>',
            'jaar ervaring</span></div>\n    </div>' + HERO_SEARCH + '  </div>\n</section>',
            1
        )
    # Fallback met simpelere marker
    if 'hero-search' not in text:
        text = re.sub(
            r'(class="hero-stats">.*?</div>\n    </div>)(\n  </div>\n</section>)',
            r'\1' + HERO_SEARCH + r'\2',
            text, count=1, flags=re.DOTALL
        )
    return text

def process(path):
    fname = os.path.basename(path)

    with open(path, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    text = raw.decode('utf-8', errors='replace')

    # Verwijder alle eerder geplaatste zoekbalken behalve de listings stap-finder
    if fname != 'listings.html':
        text = remove_old_bars(text)

    # Op de homepage: zoekbalk in de hero
    if fname == 'index.html':
        text = add_hero_search(text)

    # CSS/JS versie bumpen
    text = re.sub(r'\?v=\d+', f'?v={VERSION}', text)

    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

html_files = glob.glob(os.path.join(REPO, '*.html'))
print(f'Verwerken {len(html_files)} bestanden...')
for path in sorted(html_files):
    process(path)

# Controle
with open(os.path.join(REPO, 'index.html'), encoding='utf-8') as f:
    si = f.read()
print('hero-search in index.html:           ', 'hero-search' in si)
print('site-search-bar in index.html:       ', 'site-search-bar' in si)

with open(os.path.join(REPO, 'listings.html'), encoding='utf-8') as f:
    sl = f.read()
print('finder-bar--stepper in listings.html:', 'finder-bar--stepper' in sl)
print('site-search-bar in listings.html:    ', 'site-search-bar' in sl)

with open(os.path.join(REPO, 'agents.html'), encoding='utf-8') as f:
    sa = f.read()
print('site-search-bar in agents.html:      ', 'site-search-bar' in sa)

print('\nKlaar!')
