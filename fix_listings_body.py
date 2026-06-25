import re, os, subprocess

ROOT = r'C:/Users/Gebruiker/spring-real-estate-concept'

# Get old clean listings.html from git
result = subprocess.run(['git', 'show', '1d553cf:listings.html'],
                        capture_output=True, encoding='utf-8', cwd=ROOT)
old = result.stdout

# Get current listings.html
with open(os.path.join(ROOT, 'listings.html'), encoding='utf-8') as f:
    current = f.read()

# From old: extract everything between kz-bar closing and talk-strip
# kz-bar ends with </div>\n\n<!-- ============ and talk-strip starts
old_body_m = re.search(
    r'(</div>\n</div>\n\n)(<!-- ============ LISTINGS|<!-- ============ MAP|<div class="listings-map-wrap)',
    old, re.DOTALL
)
old_footer_m = re.search(r'<section class="talk-strip">', old)

if old_body_m and old_footer_m:
    listings_content = old[old_body_m.start(2):old_footer_m.start()]
else:
    # fallback: get from map wrap to talk-strip
    listings_content = re.search(
        r'(<div class="listings-map-wrap">.*?)<section class="talk-strip">',
        old, re.DOTALL
    )
    listings_content = listings_content.group(1) if listings_content else ''

# From current: keep header + page-hero + kz-bar (up to kz-bar closing)
# kz-bar closing: </div>\n</div> right after kz-actions
current_kzbar_end = re.search(
    r'(      </button>\n    </div>\n  </div>\n</div>)\n',
    current
)
if not current_kzbar_end:
    # Alternative: find end of kz-bar div
    current_kzbar_end = re.search(r'(</div>\n</div>)\n\n(?:<div class="has-drop"|<section|<div class="listings)', current)

# From current: get footer (talk-strip onwards)
current_footer_m = re.search(r'\n<section class="talk-strip">', current)

if current_kzbar_end and current_footer_m:
    prefix = current[:current_kzbar_end.end(0)]
    footer = current[current_footer_m.start():]
    new = prefix + '\n' + listings_content + footer
    with open(os.path.join(ROOT, 'listings.html'), 'w', encoding='utf-8') as f:
        f.write(new)
    print('listings.html restored with map + listings grid')
else:
    print('Could not find markers, trying fallback...')
    # Fallback: take everything from old between </header> and talk-strip as body
    old_after_header = re.search(r'</header>(.*?)<section class="talk-strip">', old, re.DOTALL)
    current_after_header = re.search(r'</header>', current)
    current_footer = re.search(r'<section class="talk-strip">', current)
    if old_after_header and current_after_header and current_footer:
        new = (current[:current_after_header.end(0)] +
               old_after_header.group(1) +
               current[current_footer.start():])
        with open(os.path.join(ROOT, 'listings.html'), 'w', encoding='utf-8') as f:
            f.write(new)
        print('listings.html restored via fallback')
    else:
        print('ERROR: could not restore')
