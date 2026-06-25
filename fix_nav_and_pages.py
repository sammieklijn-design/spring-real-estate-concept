import re, glob, os

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'
CHV = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'

NEW_NAV = f'''    <div class="has-drop"><button><span>Aanbod</span> {CHV}</button>
      <div class="drop">
        <a href="listings.html"><span><span class="d-t">Alle objecten</span><span class="d-d">Kantoor, bedrijf en belegging</span></span></a>
        <a href="locatie-amsterdam.html"><span><span class="d-t">Amsterdam</span><span class="d-d">7 objecten beschikbaar</span></span></a>
        <a href="locatie-utrecht.html"><span><span class="d-t">Utrecht</span><span class="d-d">5 objecten beschikbaar</span></span></a>
        <a href="locatie-valencia.html"><span><span class="d-t">Valencia &amp; Estepona</span><span class="d-d">4 objecten beschikbaar</span></span></a>
      </div>
    </div>
    <div class="has-drop"><button><span>Resources</span> {CHV}</button>
      <div class="drop">
        <a href="resources.html"><span><span class="d-t">Alle resources</span><span class="d-d">Analyses, trends en inzichten</span></span></a>
        <a href="begrippen.html"><span><span class="d-t">Begrippengids</span><span class="d-d">Vastgoedjargon uitgelegd</span></span></a>
      </div>
    </div>
    <div class="has-drop"><button><span>Team</span> {CHV}</button>
      <div class="drop">
        <a href="agents.html"><span><span class="d-t">Ons team</span><span class="d-d">35+ specialisten</span></span></a>
        <a href="about.html"><span><span class="d-t">Over Spring</span><span class="d-d">Wie wij zijn en wat we doen</span></span></a>
        <a href="cases.html"><span><span class="d-t">Cases</span><span class="d-d">Resultaten voor onze klanten</span></span></a>
      </div>
    </div>
    <div class="has-drop"><button><span>Vacatures</span> {CHV}</button>
      <div class="drop">
        <a href="vacatures.html"><span><span class="d-t">Bekijk vacatures</span><span class="d-d">Alle openstaande functies</span></span></a>
        <a href="contact.html"><span><span class="d-t">Open sollicitatie</span><span class="d-d">Stuur je cv direct op</span></span></a>
      </div>
    </div>
  </nav>'''

# Pattern: after the Diensten has-drop closing tags, match all nav links to </nav>
NAV_PAT = re.compile(
    r'(      </div>\n    </div>\n)'
    r'((?:    <a href="(?:listings|about|agents|resources|vacatures)\.html"[^\n]*\n)+)'
    r'(  </nav>)',
    re.DOTALL
)

files = glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True)
nav_count = 0
for f in files:
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    new = NAV_PAT.sub(r'\1' + NEW_NAV, txt)
    if new != txt:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        nav_count += 1

print(f'Nav updated in {nav_count} files')

# --- Vacatures.html: move #vacatures section to right after hero ---
vac_file = os.path.join(ROOT, 'vacatures.html')
with open(vac_file, encoding='utf-8') as f:
    txt = f.read()

# Extract the #vacatures section
vac_m = re.search(r'\n(<section class="section" id="vacatures">[\s\S]*?</section>)\n', txt)
if vac_m:
    vac_section = vac_m.group(1)
    # Remove it from original position
    txt2 = txt[:vac_m.start()] + '\n' + txt[vac_m.end():]
    # Insert right after page-hero closing </section>
    txt2 = txt2.replace('</section>\n\n<section class="section--tight"><div class="container">\n  <div class="hero-stats"',
                        '</section>\n\n' + vac_section + '\n\n<section class="section--tight"><div class="container">\n  <div class="hero-stats"',
                        1)
    with open(vac_file, 'w', encoding='utf-8') as f:
        f.write(txt2)
    print('Vacatures section moved up')
else:
    print('Could not find vacatures section')

# --- CSS version bump v27 -> v28 ---
css_files = glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True)
css_count = 0
for f in css_files:
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    new = txt.replace('styles.css?v=27', 'styles.css?v=28')
    if new != txt:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        css_count += 1
print(f'CSS version bumped in {css_count} files')
