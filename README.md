# Spring Real Estate — website concept

Visueel concept voor de nieuwe website van **Spring Real Estate**, gebouwd als
statische HTML/CSS/JS-site op basis van het **Katana**-Webflow-template en de
**Spring brand bible**. Bedoeld als visuele referentie/prototype dat per pagina
verder uitgewerkt en uiteindelijk in Webflow nagebouwd kan worden.

> **Powered by People. Backed by Tech.**

## Uitgangspunten
- **Doelgroepgestuurd**: bezoekers worden begeleid vanuit hun vraag —
  Gebruiker · Eigenaar · Investeerder · Ontwikkelaar.
- **23 business units** komen terug op de site (sectie + footer).
- **Grote, prominente zoekbalk** op de homepage (Katana-stijl), bedoeld om ook
  op andere pagina's terug te komen.
- **3 talen**: NL · EN · ES (taalschakelaar rechtsboven; concept-implementatie).
- Visuele stijl: licht & luchtig met donkere fotografische hero/secties,
  Spring-groen accent, afgeronde hoeken, Raleway.

## Huisstijl (uit het brandbook)
| Token | Hex | Gebruik |
|-------|-----|---------|
| Hoofdgroen | `#7CA73F` | Primaire kleur, buttons, accenten |
| Lijnengroen | `#89B647` | Lijnen / hover-accenten |
| Stipgroen | `#C3D88A` | Secundaire button, logo-punt |
| Hoofdgrijs | `#2B2B29` | Bodytekst / donkere secties |
| Lichtgrijs | `#AFAEB2` | Subtiele tekst / kaders |
| Wit / Zwart | `#FFFFFF` / `#000000` | Basis |

Lettertype: **Raleway** (Google Fonts). Buttons altijd met afgeronde hoeken.

## Structuur
```
spring-site-concept/
├── index.html              # Homepage
├── doelgroep-*.html        # 4 doelgroep-hubs (gebruiker/eigenaar/investeerder/ontwikkelaar)
├── unit-*.html             # 23 business-unit-pagina's
├── vacatures.html          # Vacatures
├── listings.html / listing-detail.html
├── about / agents / resources / contact / locaties .html
├── diensten.html           # diensten-overzicht (legacy hub)
├── css/styles.css          # Design system + alle secties
├── js/main.js              # Nav, mobiel menu, zoek-tabs
├── js/i18n.js              # 3 talen (NL/EN/ES) voor de navigatie/UI
├── build/generate.py       # Genereert doelgroep- + unit- + vacaturepagina's
├── build/update_existing.py# Zet bestaande pagina's op de nieuwe nav + i18n
├── images/                 # Logo + foto's
└── _assets/                # Bronmateriaal (brandbook, PDF's) — niet in git
```

### Informatiearchitectuur (doelgroepgestuurd)
`Doelgroep-hub → diensten → business-unit-pagina`. Elke business-unit-pagina
bevat de vaste blokken uit het aanleverdocument: expertises, sectoren, cijfers,
"zo werken wij", cases, team, reviews, FAQ, download (lead magnet),
kennisartikelen en certificeringen.

### Pagina's (her)genereren
```bash
python build/generate.py        # 4 doelgroepen + 23 units + vacatures
python build/update_existing.py # nav/i18n op de hand-gebouwde pagina's
```

## Lokaal bekijken
```bash
# vanuit de projectmap
python -m http.server 4321
# open http://localhost:4321
```

## Status / pagina's
- [x] **Homepage** (`index.html`) — hero + zoekbalk, doelgroepen, USP's,
      locatiekaart, team, reviews, 23 units, resources, footer
- [x] **Diensten** (`diensten.html`) — 4 doelgroepen, CTA boven de vouw,
      terugkerende zoekbalk, sticky categorie-navigatie
- [x] **Listings / Aanbod** (`listings.html`) — filter-rail, zoekbalk, grid,
      filter-chips, sortering, paginering
- [x] **Listing-detail** (`listing-detail.html`) — galerij, specs, locatie,
      sticky sidebar met contactformulier + adviseur
- [x] **About Us** (`about.html`) — verhaal, kernwaarden, stats, tijdlijn
- [x] **Agents / Team** (`agents.html`) — persoonskaarten + filter
- [x] **Resources / Blog** (`resources.html`) — uitgelicht + grid + categorieën
- [x] **Contact** (`contact.html`) — formulier, kantoren, kaart
- [x] **Locaties** (`locaties.html`) — Utrecht / Amsterdam / Valencia (anchors)
- [ ] Vertalingen NL/EN/ES koppelen aan de taalschakelaar (nu front-end concept)
- [ ] Echte content, foto's en formulier-afhandeling

## Bron-input
- `Aanpassingen Katana Template.pdf` — aanpassingen per pagina
- `Concuerrentenanalyse Spring.xlsx` — concurrentie / mee te nemen elementen
- `Brandbook Spring Real Estate DEF` — huisstijl
- Referentie-template: https://katana-real-estate.webflow.io
- Oude site: https://www.springrealestate.com/en/
