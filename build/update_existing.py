# -*- coding: utf-8 -*-
"""Update the hand-written pages to the new nav (doelgroep structure +
Vacatures) and add the i18n layer, reusing the shared chrome from generate.py."""
import os, re, generate
ROOT = generate.ROOT

HEADER = generate.HEADER.strip()
FOOTER_BLOCK = generate.FOOTER.split('</footer>')[0] + '</footer>'

EXISTING = ["index.html","listings.html","listing-detail.html","about.html",
            "agents.html","resources.html","contact.html","locaties.html","diensten.html"]

DG_LINKS = {
    "diensten.html#gebruiker":"doelgroep-gebruiker.html",
    "diensten.html#eigenaar":"doelgroep-eigenaar.html",
    "diensten.html#investeerder":"doelgroep-investeerder.html",
    "diensten.html#ontwikkelaar":"doelgroep-ontwikkelaar.html",
}

for name in EXISTING:
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        print("skip (missing):", name); continue
    html = open(p, encoding="utf-8").read()
    # 1) swap header
    html = re.sub(r'<header class="header">.*?</header>', lambda m: HEADER, html, count=1, flags=re.S)
    # 2) swap footer element
    html = re.sub(r'<footer class="footer">.*?</footer>', lambda m: FOOTER_BLOCK, html, count=1, flags=re.S)
    # 3) body links to old diensten anchors -> doelgroep pages
    for old, new in DG_LINKS.items():
        html = html.replace(old, new)
    # 4) include i18n.js once
    if "js/i18n.js" not in html:
        html = html.replace('<script src="js/main.js"></script>',
                            '<script src="js/main.js"></script>\n<script src="js/i18n.js"></script>', 1)
    open(p, "w", encoding="utf-8").write(html)
    print("updated:", name)
