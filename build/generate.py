# -*- coding: utf-8 -*-
"""
Spring Real Estate — static page generator.
Generates: 4 doelgroep-hubs, 21 business-unit pages, vacatures page.
Run:  python build/generate.py
Shared chrome (header/footer/mobile menu) is defined once here so every
page stays consistent and multilingual (NL/EN/ES via js/i18n.js).
"""
import os, json, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def he(s):  # escape text for HTML
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def esc(s):  # escape for attribute value
    return he(s).replace('"',"&quot;")
def trh(en, es):  # data-tr attributes for the i18n layer (body translations)
    a = ""
    if en or es:
        a = ' data-tr="1"'
        if en: a += f' data-en="{esc(en)}"'
        if es: a += f' data-es="{esc(es)}"'
    return a

# real per-unit website texts (NL/EN/ES) parsed from the aanleverdocument
_MAP = {1:"verhuur-commercieel",2:"aanhuur-kantoorruimte",3:"aanverkoop-beleggingsvastgoed",4:"serviced-offices",
        5:"taxaties-beleggingsvastgoed",6:"grootzakelijke-taxaties",7:"herbouwwaarde-verzekering",8:"vastgoeddata-marktinzichten",
        9:"asset-management",10:"commercieel-vastgoedbeheer",11:"residentieel-vastgoedbeheer",12:"design-build",
        13:"vastgoedadministratie",14:"financiele-administratie",15:"hr-advies",16:"recruitment-talent",
        17:"vastgoedmarketing",18:"strategic-advisory"}
CONTENT = {}
try:
    _raw = json.load(open(os.path.join(ROOT,"build","units_content.json"), encoding="utf-8"))
    for numstr, data in _raw.items():
        slug = _MAP.get(int(numstr))
        if not slug: continue
        CONTENT[slug] = {"nl":data["langs"].get("nl"), "en":data["langs"].get("en"),
                         "es":data["langs"].get("es"), "people":data.get("people")}
    if "aanverkoop-belegging" in CONTENT:
        CONTENT.setdefault("aankoop-beleggingsvastgoed", CONTENT["aanverkoop-belegging"])
except Exception as e:
    print("WARN: no units_content.json (", e, ")")

# Concept-teksten voor de units die niet in het aanleverdocument stonden,
# zodat ELKE business unit echte lopende tekst (intro + aanpak) krijgt.
EXTRA = {
 "bedrijfs-logistiek": {
   "h1":"Bedrijfsruimte & logistiek vastgoed huren",
   "tagline":"De juiste hal, loods of distributielocatie — strategisch gelegen.",
   "intro":"Op zoek naar bedrijfsruimte of een logistieke locatie? Spring vindt de juiste hal, loods of last-mile-locatie en onderhandelt scherpe huurvoorwaarden, met diepgaande kennis van de Nederlandse logistieke markt.",
   "approach":["We brengen uw logistieke eisen — vloerbelasting, vrije hoogte, laaddocks en bereikbaarheid — in kaart en koppelen die aan beschikbaar aanbod op de juiste knooppunten.",
               "Van shortlist en bezichtiging tot onderhandeling en oplevering begeleiden we het volledige traject, zodat u snel operationeel bent."],
   "usps":["Toegang tot logistiek aanbod op A-locaties en knooppunten","Onderhandeling over huurprijs, incentives en opleverniveau","Advies over vloerbelasting, vrije hoogte en docks","Korte lijnen met eigenaren en ontwikkelaars","Landelijke dekking met sterke regionale marktkennis"],
   "faq":[{"q":"Welke typen bedrijfsruimte begeleidt Spring?","a":"Van kleinschalige bedrijfsunits tot grote distributiecentra en last-mile-locaties door heel Nederland."},
          {"q":"Helpen jullie ook bij build-to-suit?","a":"Ja. We adviseren over nieuwbouw- en build-to-suit-trajecten in samenwerking met ontwikkelaars."},
          {"q":"In welke regio's zijn jullie actief?","a":"Landelijk, met sterke kennis van de logistieke hotspots en korte lijnen met lokale partijen."}]},
 "retail-winkelruimte": {
   "h1":"Winkelruimte & retaillocatie huren",
   "tagline":"Op de juiste plek voor uw doelgroep.",
   "intro":"Een succesvolle winkel begint bij de locatie. Spring vindt winkel- en horecaruimte op A1-, aanloop- of wijklocaties die passen bij uw formule, doelgroep en bezoekersstromen.",
   "approach":["We analyseren passantenstromen, branchering en demografie en selecteren locaties die aansluiten bij uw retailformule.",
               "We onderhandelen over huurprijs en voorwaarden en begeleiden u tot en met de opening van uw winkel."],
   "usps":["Inzicht in passantenstromen en branchering","Toegang tot A1-, aanloop- en wijklocaties","Onderhandeling over huur, incentives en bijdragen","Begeleiding voor pop-up, flagship én vaste vestiging","Sterke kennis van de lokale retailmarkt"],
   "faq":[{"q":"Begeleiden jullie ook horeca?","a":"Ja, naast retail begeleiden we ook de huur van horeca- en leisureruimte."},
          {"q":"Kan Spring helpen bij een pop-upstore?","a":"Zeker. We regelen ook kortlopende en flexibele huurovereenkomsten voor pop-up en flagship."},
          {"q":"Hoe vinden jullie de juiste locatie?","a":"Op basis van data over passanten, doelgroep en branchering, gecombineerd met lokale marktkennis."}]},
 "verkoop-commercieel": {
   "h1":"Bedrijfspand verkopen: verkoop van commercieel vastgoed",
   "tagline":"Verkoop tegen de beste marktprijs.",
   "intro":"Uw bedrijfspand verkopen vraagt om de juiste prijsstrategie en een sterk koperssnetwerk. Spring positioneert uw object scherp, benadert kopers actief en begeleidt de volledige verkoop tot aan de overdracht.",
   "approach":["We bepalen samen de optimale verkoopstrategie en vraagprijs op basis van actuele transactie- en marktdata.",
               "We presenteren uw object professioneel, benaderen gekwalificeerde kopers direct en onderhandelen tot een succesvolle transactie."],
   "usps":["Datagedreven waardebepaling en prijsstrategie","Actieve benadering van een sterk koperssnetwerk","Professionele presentatie met fotografie en dataroom","Begeleiding van bod tot notariële overdracht","Landelijke dekking met sterke regionale marktkennis"],
   "faq":[{"q":"Wat kost de verkoop van een bedrijfspand via Spring?","a":"We werken met heldere, vooraf afgesproken courtage en lichten dit toe in een vrijblijvend gesprek."},
          {"q":"Hoe bepalen jullie de vraagprijs?","a":"Op basis van een uitgebreide transactie- en marktdatabase, vergelijkbare objecten en het verwachte rendement."},
          {"q":"Verkopen jullie ook beleggingsobjecten?","a":"Ja, we begeleiden de verkoop van zowel eigenaar-gebruikerspanden als beleggingsvastgoed."}]},
 "aankoop-vastgoed": {
   "h1":"Aankoop van vastgoed & ontwikkellocaties",
   "tagline":"De juiste acquisitie als basis voor uw ontwikkeling.",
   "intro":"Een goede ontwikkeling begint bij de juiste aankoop. Spring identificeert ontwikkellocaties en te herpositioneren objecten, toetst de haalbaarheid en begeleidt de volledige acquisitie.",
   "approach":["We brengen uw ontwikkelambitie in kaart en zoeken gericht naar locaties en objecten met potentie.",
               "We toetsen haalbaarheid, voeren due diligence uit en onderhandelen tot een passende aankoop."],
   "usps":["Gerichte acquisitie van ontwikkellocaties en objecten","Haalbaarheids- en risicoanalyse vooraf","Due diligence en onderhandeling","Inzicht in bestemmings- en marktpotentie","Korte lijnen met gemeenten, eigenaren en beleggers"],
   "faq":[{"q":"Zoeken jullie ook off-market objecten?","a":"Ja. Via ons netwerk krijgen we regelmatig toegang tot objecten die niet openbaar worden aangeboden."},
          {"q":"Helpen jullie bij de haalbaarheidsanalyse?","a":"Zeker. We toetsen locatie, bestemming, kosten en marktpotentie voordat u zich vastlegt."},
          {"q":"Werken jullie samen met beleggers?","a":"Ja, we begeleiden zowel ontwikkelaars als beleggers bij acquisities."}]},
 "gebiedsontwikkeling": {
   "h1":"Gebiedsontwikkeling: van visie tot realisatie",
   "tagline":"Toekomstbestendige gebieden, samen ontwikkeld.",
   "intro":"Gebiedsontwikkeling vraagt om visie, draagvlak en regie. Spring begeleidt ontwikkelaars, gemeenten en corporaties van eerste gebiedsvisie tot gefaseerde realisatie van toekomstbestendige gebieden.",
   "approach":["We vertalen ambities naar een haalbare gebiedsvisie en betrekken de juiste stakeholders vroegtijdig.",
               "We bewaken samenhang, fasering en programma tot en met de realisatie en invulling van het gebied."],
   "usps":["Heldere gebiedsvisie met draagvlak","Stakeholder- en procesmanagement","Programmering, fasering en realisatieregie","Inzicht in markt, doelgroep en haalbaarheid","Ervaring met publiek-private samenwerking"],
   "faq":[{"q":"Voor wie werkt Spring bij gebiedsontwikkeling?","a":"Voor ontwikkelaars, gemeenten, corporaties en beleggers die samen een gebied willen ontwikkelen."},
          {"q":"Begeleiden jullie het hele traject?","a":"Ja, van visievorming en haalbaarheid tot fasering, programmering en realisatie."},
          {"q":"Hoe borgen jullie draagvlak?","a":"Door stakeholders vroeg te betrekken en het proces transparant en gestructureerd te voeren."}]},
 "vastgoedfinanciering": {
   "h1":"Vastgoedfinanciering: onafhankelijk financieringsadvies",
   "tagline":"De optimale financieringsstructuur voor uw vastgoed.",
   "intro":"De juiste financiering bepaalt mede uw rendement. Spring adviseert onafhankelijk over de optimale financieringsstructuur en onderhandelt namens u met financiers.",
   "approach":["We brengen uw financieringsbehoefte en risicoprofiel in kaart en bepalen de optimale structuur.",
               "We benaderen geschikte financiers, vergelijken voorstellen en onderhandelen scherpe voorwaarden."],
   "usps":["Onafhankelijk advies, geen binding aan één financier","Optimale financieringsstructuur en looptijd","Toegang tot een breed netwerk van banken en alternatieve financiers","Onderhandeling over rente en voorwaarden","Begeleiding tot en met closing"],
   "faq":[{"q":"Zijn jullie onafhankelijk?","a":"Ja. We adviseren onafhankelijk en behartigen uitsluitend uw belang richting financiers."},
          {"q":"Voor welke financieringen kan ik terecht?","a":"Voor acquisitie-, herfinancierings- en ontwikkelingsfinanciering van commercieel vastgoed."},
          {"q":"Werken jullie ook met alternatieve financiers?","a":"Ja, naast banken hebben we toegang tot een netwerk van alternatieve en private financiers."}]},
}
for _slug, _nl in EXTRA.items():
    CONTENT.setdefault(_slug, {"nl":_nl, "en":None, "es":None, "people":None})

# ----------------------------------------------------------------------
# DATA MODEL
# ----------------------------------------------------------------------
DOELGROEPEN = {
    "gebruiker":   {"num":"01","name":"Gebruiker","q":"Ik zoek een kantoor of werkplek",
        "intro":"Op zoek naar de juiste werkomgeving? Spring vindt, onderhandelt en richt in — van een eigen kantoor tot een flexibele werkplek."},
    "eigenaar":    {"num":"02","name":"Eigenaar","q":"Ik wil mijn vastgoed verkopen of verhuren",
        "intro":"Haal maximaal rendement uit uw object met scherpe marketing, het juiste netwerk en betrouwbare taxaties."},
    "investeerder":{"num":"03","name":"Investeerder","q":"Ik wil investeren in vastgoed",
        "intro":"Van acquisitie tot beheer: datagedreven advies over de volledige levenscyclus van uw belegging."},
    "ontwikkelaar":{"num":"04","name":"Ontwikkelaar","q":"Ik wil vastgoed ontwikkelen of optimaliseren",
        "intro":"Van acquisitie en concept tot oplevering en verhuur — met data en taxaties als kompas."},
}

# 18 officiële business units (Spring pitch), verdeeld over de 4 doelgroepen.
# u[2] = één of meer doelgroep-keys (spatie-gescheiden); ondersteunend = overkoepelend.
# Spanje is geen aparte unit: de internationale dekking + Spaans team staat op
# 'Aan- en verkoop beleggingsvastgoed' en 'Asset management'.
UNITS = [
 # GEBRUIKER
 ("aanhuur-kantoorruimte","Aanhuur kantoorruimte","gebruiker","Strategische zoektocht naar de juiste kantoorlocatie en de beste huurvoorwaarden.",
   ["Locatieanalyse & shortlist","Onderhandeling huurvoorwaarden","Begeleiding tot sleuteloverdracht"],["Scale-ups","Corporates","Zorg","Tech"]),
 ("serviced-offices","Serviced Offices & flexibele werkplekken","gebruiker","Instapklare werkplekken en flexibele contracten die met u meegroeien.",
   ["Flexibele contractvormen","Volledig gefaciliteerde kantoren","Snel schakelen bij groei"],["Startups","Projectteams","Internationale kantoren"]),
 ("design-build","Design & Build","gebruiker ontwikkelaar","Inrichting en optimalisatie van de werkplek, van concept tot oplevering.",
   ["Werkplekconcept & ontwerp","Projectmanagement realisatie","Duurzame inrichting"],["Corporates","Zorg","Onderwijs"]),
 # EIGENAAR
 ("verhuur-commercieel","Verhuur van commercieel vastgoed","eigenaar","Verhuur die beweging creëert in de markt.",
   ["Positionering & strategie","Actieve salesbenadering","Contractmanagement"],["Kantoren","Bedrijfsruimte","Retail"]),
 ("vastgoedmarketing","Vastgoedmarketing","eigenaar","Professionele presentatie en bereik bij precies de juiste doelgroep.",
   ["Fotografie & video","Online campagnes","Brochures & datarooms"],["Beleggers","Ontwikkelaars","Eigenaren"]),
 ("taxaties-beleggingsvastgoed","Taxaties van beleggingsvastgoed","eigenaar investeerder","Onafhankelijke, gevalideerde taxaties van beleggingsvastgoed.",
   ["Marktwaarde-taxaties","Gevalideerd & RICS-conform","Datagedreven onderbouwing"],["Banken","Beleggers","Accountants"]),
 ("grootzakelijke-taxaties","Grootzakelijke taxaties","eigenaar","Taxaties van technisch complexe en grootzakelijke objecten.",
   ["Complexe & unieke assets","Internationale expertise","Erkende rekenmodellen"],["Corporates","Industrie","Zorg"]),
 ("herbouwwaarde-verzekering","Herbouwwaarde- & verzekeringstaxaties","eigenaar","De juiste verzekerde waarde en onderbouwde herbouwwaarde.",
   ["Herbouwwaardebepaling","Verzekeringstaxatie","Periodieke herijking"],["Eigenaren","VvE's","Verzekeraars"]),
 # INVESTEERDER (+ ontwikkelaar waar relevant)
 ("aanverkoop-beleggingsvastgoed","Aan- en verkoop van beleggingsvastgoed","investeerder ontwikkelaar","Begeleiding bij zowel aan- als verkoop van beleggingsobjecten — in Nederland én Spanje.",
   ["Acquisitie & due diligence","Markttiming","Internationaal: NL & España"],["Beleggers","Family offices","Fondsen"]),
 ("vastgoeddata-marktinzichten","Vastgoeddata en marktinzichten","investeerder ontwikkelaar","Heldere marktinzichten als basis voor betere vastgoedbeslissingen.",
   ["Marktrapportages","Real-time dashboards","Acquisitietools"],["Beleggers","Ontwikkelaars","Adviseurs"]),
 ("asset-management","Asset management","investeerder","Actief beheer gericht op waardegroei en optimale exploitatie — in Nederland én Spanje.",
   ["Waardecreatie-plannen","Huurdersbeleid","Internationaal: NL & España"],["Beleggers","Fondsen","Institutioneel"]),
 ("commercieel-vastgoedbeheer","Commercieel vastgoedbeheer","investeerder","Technisch en commercieel beheer dat zorgen uit handen neemt.",
   ["Technisch beheer","Commercieel beheer","24/7 storingsdienst"],["Eigenaren","Beleggers","VvE's"]),
 ("residentieel-vastgoedbeheer","Residentieel vastgoedbeheer","investeerder","Beheer van woningen en residentiële portefeuilles.",
   ["Verhuur & mutaties","Onderhoud & service","Financiële rapportage"],["Beleggers","Particulieren","Corporaties"]),
 ("vastgoedadministratie","Vastgoedadministratie","investeerder","Sluitende administratie en rapportage, volledig ontzorgd.",
   ["Huuradministratie","Servicekostenafrekening","Maatwerkdashboards"],["Beleggers","Eigenaren","Fondsen"]),
 ("strategic-advisory","Strategic Advisory","investeerder ontwikkelaar","Strategisch advies over portefeuille, rendement en risicospreiding.",
   ["Portefeuillestrategie","Rendementsanalyse","Boardroom-advies"],["Family offices","Fondsen","Corporates"]),
 # ONDERSTEUNEND (overkoepelend)
 ("financiele-administratie","Financiële administratie","ondersteunend","Financiële administratie en rapportage voor vastgoedorganisaties.",
   ["Boekhouding","Rapportage","Jaarafsluiting"],["Beleggers","Ontwikkelaars","Eigenaren"]),
 ("hr-advies","HR-Advies","ondersteunend","HR-advies voor groeiende vastgoedorganisaties.",
   ["HR-strategie","Arbeidsvoorwaarden","Organisatieontwikkeling"],["Vastgoedbedrijven","Ontwikkelaars","Beleggers"]),
 ("recruitment-talent","Recruitment & Talent acquisition","ondersteunend","Werving en selectie van vastgoedtalent.",
   ["Search & selectie","Talent acquisition","Employer branding"],["Vastgoedbedrijven","Ontwikkelaars","Beleggers"]),
]

GROUP_NAMES = {"gebruiker":"Gebruiker","eigenaar":"Eigenaar","investeerder":"Investeerder",
               "ontwikkelaar":"Ontwikkelaar","ondersteunend":"Ondersteunend"}

def units_for(dg):
    # u[2] is a space-separated list of doelgroep keys; match membership
    return [u for u in UNITS if dg in u[2].split()]

# ----------------------------------------------------------------------
# ICONS
# ----------------------------------------------------------------------
def ic(p, sw="2"):
    return f'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}">{p}</svg>'
I_BLD = '<path d="M3 21h18M5 21V8l7-5 7 5v13"/>'
I_CHECK = '<path d="M5 12l5 5L20 6"/>'
I_ARR = '<path d="M5 12h14M13 6l6 6-6 6"/>'
def arrow(cls="arr"):
    return f'<svg class="{cls}" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4">{I_ARR}</svg>'

# ----------------------------------------------------------------------
# SHARED CHROME
# ----------------------------------------------------------------------
HEAD = """<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,500&family=Fraunces:ital,opsz,wght@1,9..144,400;1,9..144,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
</head>
<body>
"""

TOPBAR = """<div class="topbar"><div class="container">
  <div class="badges">
    <span class="badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l2.4 6.9H22l-6 4.3 2.3 7-6.3-4.4L5.7 20 8 13.2 2 8.9h7.6z"/></svg> 4,8 / 5 op Google</span>
    <span class="badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="9"/></svg> NVM &amp; VBO aangesloten</span>
    <span class="badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l8 4v6c0 5-3.5 8-8 10-4.5-2-8-5-8-10V6z"/></svg> 15+ jaar ervaring</span>
  </div>
  <div class="top-right">
    <a href="mailto:info@springrealestate.com">info@springrealestate.com</a>
    <div class="lang" id="lang"><button class="active" data-lang="nl">NL</button><button data-lang="en">EN</button><button data-lang="es">ES</button></div>
  </div>
</div></div>
"""

HEADER = """<header class="header"><div class="container">
  <a href="index.html" class="logo" aria-label="Spring Real Estate"><span class="logo-main">Spr<span class="dot"></span>ing</span><span class="logo-sub">real estate</span></a>
  <nav class="nav">
    <div class="has-drop"><button><span data-i18n="nav.diensten">Diensten</span> <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>
      <div class="drop">
        <a href="doelgroep-gebruiker.html"><span class="d-ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6"/></svg></span><span><span class="d-t" data-i18n="dd.gebruiker">Gebruiker</span><span class="d-d" data-i18n="dd.gebruiker.d">Ik zoek een kantoor of werkplek</span></span></a>
        <a href="doelgroep-eigenaar.html"><span class="d-ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/></svg></span><span><span class="d-t" data-i18n="dd.eigenaar">Eigenaar</span><span class="d-d" data-i18n="dd.eigenaar.d">Ik wil verkopen of verhuren</span></span></a>
        <a href="doelgroep-investeerder.html"><span class="d-ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l6-6 4 4 8-8M21 7v6M21 7h-6"/></svg></span><span><span class="d-t" data-i18n="dd.investeerder">Investeerder</span><span class="d-d" data-i18n="dd.investeerder.d">Ik wil investeren in vastgoed</span></span></a>
        <a href="doelgroep-ontwikkelaar.html"><span class="d-ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 20h20M4 20V8l5-3v15M14 20V4l6 4v12"/></svg></span><span><span class="d-t" data-i18n="dd.ontwikkelaar">Ontwikkelaar</span><span class="d-d" data-i18n="dd.ontwikkelaar.d">Ik wil ontwikkelen of optimaliseren</span></span></a>
      </div>
    </div>
    <a href="listings.html" data-i18n="nav.listings">Listings</a>
    <a href="about.html" data-i18n="nav.about">About Us</a>
    <a href="agents.html" data-i18n="nav.agents">Agents</a>
    <a href="resources.html" data-i18n="nav.resources">Resources</a>
    <a href="vacatures.html" data-i18n="nav.vacatures">Vacatures</a>
  </nav>
  <div class="header-cta">
    <a href="listings.html" class="h-search" aria-label="Zoeken in het aanbod"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg></a>
    <div class="h-lang"><button class="active" data-lang="nl">NL</button><button data-lang="en">EN</button><button data-lang="es">ES</button></div>
    <a href="contact.html" class="btn btn--primary" data-i18n="nav.contact">Contact</a>
    <button class="burger" id="burger" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</div></header>
"""

TALK_BLOCK = """
<section class="section talk-band"><div class="container">
  <div class="talk-card">
    <div class="talk-photo"><img src="images/photo-2.jpg" alt="Spring adviseur"></div>
    <div class="talk-body">
      <span class="eyebrow" data-i18n="talk.eyebrow">Persoonlijk contact</span>
      <h2 class="disp" data-tr="1" data-en="Talk to an &lt;em&gt;agent&lt;/em&gt;" data-es="Habla con un &lt;em&gt;asesor&lt;/em&gt;">Praat met een <em>adviseur</em></h2>
      <p class="lead" data-i18n="talk.p">Liever direct sparren? Onze specialisten helpen u graag verder &mdash; vrijblijvend en in uw taal.</p>
      <div class="talk-actions">
        <a href="tel:+31302001020" class="btn btn--primary"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg> +31 30 200 10 20</a>
        <a href="contact.html" class="btn btn--ghost" data-i18n="talk.plan">Plan een gesprek</a>
      </div>
    </div>
  </div>
</div></section>
"""

FOOTER = TALK_BLOCK + """<footer class="footer"><div class="container">
  <div class="top">
    <div>
      <div class="logo logo--light"><span class="logo-main">Spr<span class="dot"></span>ing</span><span class="logo-sub">real estate</span></div>
      <p style="margin-top:16px; max-width:30ch" data-i18n="foot.tagline">Powered by People. Backed by Tech. D&eacute; partner in commercieel vastgoed in Nederland &amp; Spanje.</p>
      <div class="badges">
        <span class="badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l2.4 6.9H22l-6 4.3 2.3 7-6.3-4.4L5.7 20 8 13.2 2 8.9h7.6z"/></svg> 4,8/5 Google</span>
        <span class="badge"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l8 4v6c0 5-3.5 8-8 10-4.5-2-8-5-8-10V6z"/></svg> NVM / VBO</span>
      </div>
    </div>
    <div><h4 data-i18n="foot.doelgroepen">Doelgroepen</h4><ul>
      <li><a href="doelgroep-gebruiker.html" data-i18n="dd.gebruiker">Gebruiker</a></li>
      <li><a href="doelgroep-eigenaar.html" data-i18n="dd.eigenaar">Eigenaar</a></li>
      <li><a href="doelgroep-investeerder.html" data-i18n="dd.investeerder">Investeerder</a></li>
      <li><a href="doelgroep-ontwikkelaar.html" data-i18n="dd.ontwikkelaar">Ontwikkelaar</a></li>
    </ul></div>
    <div><h4 data-i18n="foot.navigatie">Navigatie</h4><ul>
      <li><a href="listings.html" data-i18n="nav.listings">Listings / Aanbod</a></li>
      <li><a href="about.html" data-i18n="nav.about">About Us</a></li>
      <li><a href="agents.html" data-i18n="nav.agents">Agents / Team</a></li>
      <li><a href="sectoren.html">Sectoren</a></li>
      <li><a href="cases.html">Klantverhalen</a></li>
      <li><a href="resources.html" data-i18n="nav.resources">Resources &amp; Blog</a></li>
      <li><a href="vacatures.html" data-i18n="nav.vacatures">Vacatures</a></li>
      <li><a href="contact.html" data-i18n="nav.contact">Contact</a></li>
    </ul></div>
    <div><h4 data-i18n="foot.locaties">Locaties</h4><ul>
      <li><a href="locatie-utrecht.html">Utrecht</a></li>
      <li><a href="locatie-amsterdam.html">Amsterdam</a></li>
      <li><a href="locatie-valencia.html">Valencia (ES)</a></li>
      <li><a href="locatie-estepona.html">Estepona (ES)</a></li>
    </ul></div>
    <div class="news"><h4 data-i18n="foot.nieuwsbrief">Nieuwsbrief</h4><p style="font-size:.9rem" data-i18n="foot.nieuwsbrief.p">Marktinzichten &amp; nieuw aanbod in uw inbox.</p><form onsubmit="return false"><input type="email" placeholder="Uw e-mailadres" data-i18n-ph="foot.email"><button class="btn btn--primary" style="width:100%" data-i18n="foot.inschrijven">Inschrijven</button></form></div>
  </div>
  <div class="bottom"><span data-i18n="foot.rights">&copy; 2026 Spring Real Estate. Alle rechten voorbehouden.</span><div class="links"><a href="#">Privacyverklaring</a><a href="#">Cookies</a><a href="#">Algemene voorwaarden</a><span style="color:#6f7166">Concept o.b.v. Katana-template</span></div></div>
</div></footer>

<div class="mobile-menu" id="mobileMenu">
  <div class="mm-head"><div class="logo logo--light"><span class="logo-main">Spr<span class="dot"></span>ing</span><span class="logo-sub">real estate</span></div><button class="mm-close" id="mmClose">&times;</button></div>
  <nav>
    <a href="doelgroep-gebruiker.html" data-i18n="dd.gebruiker">Gebruiker</a>
    <a href="doelgroep-eigenaar.html" data-i18n="dd.eigenaar">Eigenaar</a>
    <a href="doelgroep-investeerder.html" data-i18n="dd.investeerder">Investeerder</a>
    <a href="doelgroep-ontwikkelaar.html" data-i18n="dd.ontwikkelaar">Ontwikkelaar</a>
    <a href="listings.html" data-i18n="nav.listings">Listings</a>
    <a href="about.html" data-i18n="nav.about">About Us</a>
    <a href="agents.html" data-i18n="nav.agents">Agents</a>
    <a href="resources.html" data-i18n="nav.resources">Resources</a>
    <a href="vacatures.html" data-i18n="nav.vacatures">Vacatures</a>
  </nav>
  <div class="mm-cta"><a href="contact.html" class="btn btn--primary" data-i18n="nav.contact">Contact</a><div class="lang mm-lang" style="justify-content:center"><button class="active" data-lang="nl">NL</button><button data-lang="en">EN</button><button data-lang="es">ES</button></div></div>
</div>

<script src="js/main.js"></script>
<script src="js/i18n.js"></script>
</body>
</html>
"""

def li_checks(items):
    return "".join(f'<li>{ic(I_CHECK,"2.4")} {x}</li>' for x in items)

# ----------------------------------------------------------------------
# DOELGROEP HUB PAGE
# ----------------------------------------------------------------------
DG_WHY = {
 "gebruiker":[("Snel de juiste ruimte","We kennen de markt op straatniveau en koppelen uw eisen aan het beste beschikbare aanbod."),
              ("Onderhandeld op uw voorwaarden","Scherpe huurprijs, incentives en flexibele voorwaarden — wij behartigen uw belang."),
              ("Instapklaar opgeleverd","Van zoektocht tot inrichting: één partner regelt het hele traject.")],
 "eigenaar":[("Maximaal rendement","Datagedreven waardebepaling en een scherpe positionering van uw object."),
             ("Actieve salesaanpak","Wij benaderen kopers en huurders direct en creëren beweging in de markt."),
             ("Betrouwbare taxaties","Onafhankelijke, gevalideerde taxaties volgens de hoogste normen.")],
 "investeerder":[("De hele levenscyclus","Van acquisitie en beheer tot exit — strategisch advies in elke fase."),
                 ("Onderbouwd met data","Actuele markt- en transactiedata als fundament onder elke beslissing."),
                 ("Volledig ontzorgd","Asset management, beheer en administratie onder één dak.")],
 "ontwikkelaar":[("Van acquisitie tot oplevering","Begeleiding over de volledige ontwikkeling, met data en taxaties als kompas."),
                 ("Haalbaarheid vooraf","We toetsen locatie, bestemming en markt voordat u zich vastlegt."),
                 ("Marktinzicht als kompas","Research en advies die uw plan onderbouwen en versterken.")],
}
DG_QUOTE = {
 "gebruiker":"De grootste fout bij het zoeken naar ruimte is alleen naar de huurprijs kijken. Wij kijken naar groei, flexibiliteit en uw totale huisvestingsstrategie.",
 "eigenaar":"Een succesvol verhuur- of verkooptraject draait om de juiste prijs én een actieve benadering van de markt. Daar sturen we op.",
 "investeerder":"Rendement begint bij de juiste data en een scherpe strategie — en wordt geborgd door goed beheer.",
 "ontwikkelaar":"Een goede ontwikkeling begint bij de juiste acquisitie en een onderbouwd plan. Wij denken vanaf dag één mee.",
}
def render_doelgroep(key):
    d = DOELGROEPEN[key]
    units = units_for(key)
    cards = ""
    for j,(slug,name,_dg,tag,exp,sec) in enumerate(units):
        img = PHOTOS[j % 3]
        cards += f'''<a class="kat-card" href="unit-{slug}.html"><img src="{img}" alt=""><span class="ktag">{d['name']}</span><span class="kbody"><h3>{name}</h3><p>{tag}</p></span><span class="karr"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">{I_ARR}</svg></span></a>'''
    why_cards = "".join(f'<div class="value"><div class="ic">{ic(I_CHECK,"2.4")}</div><h3>{t}</h3><p>{x}</p></div>' for t,x in DG_WHY[key])
    onder = units_for("ondersteunend")
    onder_html = ""
    if key in ("investeerder","ontwikkelaar"):
        chips = "".join(f'<a class="unit" href="unit-{s}.html"><span class="u-dot"></span>{n}</a>' for s,n,_,_,_,_ in onder)
        onder_html = f'''<section class="section--tight section--soft"><div class="container">
          <div class="sec-head"><div class="t"><span class="eyebrow">Ondersteunend</span><h2 class="disp">Overkoepelende <em>expertise</em></h2></div></div>
          <div class="units-grid">{chips}</div>
        </div></section>'''
    html = HEAD.format(title=f"{d['name']} — Spring Real Estate",
                       desc=f"Spring Real Estate voor de {d['name'].lower()}: {d['q'].lower()}.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / Diensten / {d['name']}</div>
    <span class="eyebrow">Doelgroep {d['num']}</span>
    <h1>{d['name']} — <em style="color:var(--green);font-style:italic;font-weight:500">{d['q'].lower()}</em></h1>
    <p class="lead">{d['intro']}</p>
    <div class="ph-cta"><a href="#diensten" class="btn btn--primary">Bekijk diensten</a><a href="contact.html" class="btn btn--ghost">Plan een gesprek</a></div>
    <form class="search search--light search--single" onsubmit="return false">
      <label class="seg"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
        <input type="text" placeholder="Zoek op plaats, adres, type of trefwoord…" data-i18n-ph="search.phloc" aria-label="Zoeken"></label>
      <button class="search-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg> <span data-i18n="search.btn">Zoeken</span></button>
    </form>
  </div>
</section>

<section class="section"><div class="container"><div class="two-col">
  <div class="prose">
    <span class="eyebrow">Voor de {d['name'].lower()}</span>
    <h2 class="disp">{d['q']}? <em>Wij helpen u verder</em></h2>
    <p>{d['intro']}</p>
    <p>Of het nu om één vraag gaat of om een complex traject: u krijgt één aanspreekpunt met het hele Spring-ecosysteem erachter — commercieel én residentieel, in Nederland en Spanje.</p>
    <a href="#diensten" class="btn btn--primary" style="margin-top:6px">Bekijk de diensten</a>
  </div>
  <div class="media-tall"><img src="images/photo-1.jpg" alt="{d['name']}"></div>
</div></div></section>

<section class="section--tight section--soft"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Waarom Spring</span><h2 class="disp">Waarom de {d['name'].lower()} voor <em>Spring</em> kiest</h2></div></div>
  <div class="values-grid">{why_cards}</div>
</div></section>

<section class="section" id="diensten">
  <div class="container">
    <div class="sec-head"><div class="t"><span class="eyebrow">Onze diensten</span><h2 class="disp">Kies een <em>business unit</em></h2><p class="lead">Klik op een dienst voor de volledige business-unit-pagina met experts, cases en antwoorden.</p></div></div>
    <div class="kat-grid">{cards}</div>
  </div>
</section>
{onder_html}
<section class="section dark-sec"><div class="container">
  <div class="center" style="max-width:62ch;margin:0 auto">
    <span class="eyebrow" style="color:var(--green-soft)">Onze visie</span>
    <p class="disp disp--light" style="font-size:clamp(1.5rem,3vw,2.3rem);line-height:1.3"><em>"{DG_QUOTE[key]}"</em></p>
    <p class="muted" style="margin-top:16px">— Spring Real Estate</p>
  </div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Sectoren</span><h2 class="disp">Expertise in <em>elke sector</em></h2><p class="lead">Van kantoren en logistiek tot retail, zorg en residentieel vastgoed.</p></div><a href="sectoren.html" class="btn btn--ghost">Alle sectoren</a></div>
  <div class="units-grid">
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>Kantoren</a>
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>Logistiek &amp; bedrijfsruimte</a>
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>Retail &amp; winkels</a>
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>Zorgvastgoed</a>
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>Residentieel</a>
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>Hospitality</a>
  </div>
</div></section>

<section class="section--tight"><div class="container"><div class="cta">
  <h2>Niet zeker welke dienst u nodig heeft?</h2>
  <p>Onze adviseurs denken graag met u mee — vrijblijvend en vanuit uw vraag.</p>
  <div class="btns"><a href="contact.html" class="btn btn--light btn--lg">Plan een gesprek</a><a href="listings.html" class="btn btn--lg" style="background:rgba(255,255,255,.16);color:#fff;border-color:rgba(255,255,255,.4)">Bekijk het aanbod</a></div>
</div></div></section>
'''
    html += FOOTER
    return html

# ----------------------------------------------------------------------
# BUSINESS UNIT PAGE
# ----------------------------------------------------------------------
PHOTOS = ["images/photo-1.jpg","images/photo-2.jpg","images/hero.jpg"]

def render_unit(idx, u):
    slug,name,dg,tag,exp,sec = u
    pdg = dg.split()[0]  # primaire doelgroep voor crumb/links
    dgname = GROUP_NAMES[pdg]
    dglink = f"doelgroep-{pdg}.html" if pdg!="ondersteunend" else "doelgroep-investeerder.html"
    ph = PHOTOS[idx % 3]; ph2 = PHOTOS[(idx+1) % 3]
    sectors = "".join(f'<div class="sector">{ic(I_CHECK,"2.4")} {s}</div>' for s in sec)
    crumb_dg = "" if pdg=="ondersteunend" else f'<a href="{dglink}">{dgname}</a> / '
    title_low = name.lower()

    c = CONTENT.get(slug)
    nl = c["nl"] if c else None
    en = (c.get("en") if c else None) or {}
    es = (c.get("es") if c else None) or {}

    # hero (real H1 + tagline when available)
    if nl and nl.get("h1"):
        hero_h1 = f'<h1{trh(en.get("h1"), es.get("h1"))}>{he(nl["h1"])}</h1>'
        hero_tag = f'<p class="lead"{trh(en.get("tagline"), es.get("tagline"))}>{he(nl.get("tagline") or tag)}</p>'
    else:
        hero_h1 = f'<h1>{he(name)}</h1>'; hero_tag = f'<p class="lead">{he(tag)}</p>'

    # expertises (real USP list as check-cards, else generic)
    if nl and nl.get("usps"):
        enu = en.get("usps") or []; esu = es.get("usps") or []
        exp_cards = "".join(
            f'<div class="svc"><div class="svc-ic">{ic(I_CHECK,"2.4")}</div><p{trh(enu[i] if i<len(enu) else "", esu[i] if i<len(esu) else "")}>{he(x)}</p></div>'
            for i,x in enumerate(nl["usps"]))
    else:
        exp_cards = "".join(f'<div class="svc"><div class="svc-ic">{ic(I_BLD)}</div><h3>{e}</h3><p>Concrete begeleiding en uitvoering binnen {title_low}.</p></div>' for e in exp)

    # approach section (intro + paragraphs)
    approach_html = ""
    if nl and (nl.get("intro") or nl.get("approach")):
        rows = []
        if nl.get("intro"): rows.append((nl["intro"], en.get("intro"), es.get("intro")))
        ap = nl.get("approach") or []; ena = en.get("approach") or []; esa = es.get("approach") or []
        for i,p in enumerate(ap):
            rows.append((p, ena[i] if i<len(ena) else "", esa[i] if i<len(esa) else ""))
        body = "".join(f'<p{trh(e2,s2)}>{he(p)}</p>' for p,e2,s2 in rows)
        approach_html = f'''
<section class="section--tight" id="aanpak"><div class="container">
  <div class="prose" style="max-width:780px">
    <span class="eyebrow">Onze aanpak</span>
    <h2 class="disp">Zo pakken we het <em>aan</em></h2>
    {body}
  </div>
</div></section>'''

    # FAQ (real, else generic)
    if nl and nl.get("faq"):
        enf = en.get("faq") or []; esf = es.get("faq") or []
        fi = []
        for i,qa in enumerate(nl["faq"]):
            ef = enf[i] if i<len(enf) else {}; sf = esf[i] if i<len(esf) else {}
            op = " open" if i==0 else ""
            fi.append(f'<details class="faq-item"{op}><summary><span{trh(ef.get("q"),sf.get("q"))}>{he(qa["q"])}</span><span class="pl">+</span></summary><div class="ans"{trh(ef.get("a"),sf.get("a"))}>{he(qa["a"])}</div></details>')
        faq_html = "".join(fi)
    else:
        faq_html = (f'<details class="faq-item" open><summary>Wat kost {title_low} bij Spring?<span class="pl">+</span></summary><div class="ans">De kosten hangen af van uw situatie en doelstelling. Na een kennismaking ontvangt u een transparant voorstel op maat.</div></details>'
                    f'<details class="faq-item"><summary>Hoe snel kunnen jullie starten?<span class="pl">+</span></summary><div class="ans">Doorgaans plannen we binnen enkele werkdagen een kennismaking en starten we direct na akkoord.</div></details>'
                    f'<details class="faq-item"><summary>In welke regio&#39;s zijn jullie actief?<span class="pl">+</span></summary><div class="ans">We werken vanuit Utrecht, Amsterdam en Valencia en zijn actief in heel Nederland en Spanje.</div></details>')

    # team from real involved people, else generic
    ppl = (c.get("people") if c else None) or []
    if ppl:
        tc = []
        for i,pp in enumerate(ppl[:4]):
            parts = [x.strip() for x in re.split(r'—|·', pp) if x.strip()]
            nm = parts[0] if parts else "Adviseur"
            role = parts[1] if len(parts) > 1 else "Spring Real Estate"
            mail = parts[2] if len(parts) > 2 else "#"
            tc.append(f'<div class="agent"><div class="ph"><img src="{PHOTOS[i%3]}" alt=""></div><div class="body"><div class="name">{he(nm)}</div><div class="role">{he(role)}</div><div class="socials"><a href="#" aria-label="LinkedIn">in</a><a href="mailto:{mail}" aria-label="E-mail">@</a></div></div></div>')
        team_html = "".join(tc)
    else:
        team_html = (f'<div class="agent"><div class="ph"><img src="{ph}" alt=""></div><div class="body"><div class="name">Daan van der Meer</div><div class="role">Senior Adviseur</div><div class="socials"><a href="#">in</a><a href="#">@</a></div></div></div>'
                     f'<div class="agent"><div class="ph"><img src="{ph2}" alt=""></div><div class="body"><div class="name">Sofia Mart&iacute;n</div><div class="role">Adviseur</div><div class="socials"><a href="#">in</a><a href="#">@</a></div></div></div>'
                     f'<div class="agent"><div class="ph"><img src="{PHOTOS[(idx+2)%3]}" alt=""></div><div class="body"><div class="name">Lars Bakker</div><div class="role">Specialist</div><div class="socials"><a href="#">in</a><a href="#">@</a></div></div></div>')
    # gerelateerde diensten (cross-sell binnen dezelfde doelgroep)
    sibs = [x for x in UNITS if pdg in x[2].split() and x[0] != slug]
    if len(sibs) < 3:
        sibs = [x for x in UNITS if x[0] != slug]
    related_html = "".join(f'<a class="unit" href="unit-{s[0]}.html"><span class="u-dot"></span>{s[1]}</a>' for s in sibs[:6])

    def _propcard(ptype, title, addr, price, meta, img):
        return (f'<a class="prop-card" href="listing-detail.html"><div class="ph"><span class="tag">Beschikbaar</span>'
                f'<img src="images/{img}" alt=""></div><div class="body"><span class="ptype">{ptype}</span>'
                f'<h3>{title}</h3><span class="addr">{addr}</span><div class="meta"><span class="price">{price}</span>'
                f'<span style="margin-left:auto">{meta}</span></div></div></a>')
    def _agent(nm, role, img):
        return (f'<div class="agent"><div class="ph"><img src="images/{img}" alt=""></div><div class="body">'
                f'<div class="name">{nm}</div><div class="role">{role}</div>'
                f'<div class="socials"><a href="#">in</a><a href="#">@</a></div></div></div>')
    # beschikbare ruimtes/opties bij kantoor- en serviced-office-units
    office_html = ""
    if slug == "serviced-offices":
        office_html = ('<section class="section--soft" id="beschikbaar"><div class="container">'
          '<div class="sec-head"><div class="t"><span class="eyebrow">Beschikbare werkplekken</span><h2 class="disp">Direct <em>beschikbaar</em></h2><p class="lead">Een greep uit onze serviced offices en flexibele werkplekken.</p></div><a href="listings.html" class="btn btn--ghost">Heel het aanbod</a></div>'
          '<div class="cards-grid">'
          + _propcard("Serviced office", "WTC · Zuidas", "Amsterdam", "€1.250 <small>/maand</small>", "8 werkplekken", "photo-1.jpg")
          + _propcard("Flexwerkplekken", "Stadhouderskade", "Utrecht", "€350 <small>/werkplek</small>", "open &amp; vast", "photo-2.jpg")
          + _propcard("Private office", "Paseo de la Alameda", "Valencia", "€1.100 <small>/maand</small>", "12 werkplekken", "hero.jpg")
          + '</div></div></section>')
    elif slug == "aanhuur-kantoorruimte":
        office_html = ('<section class="section--soft" id="beschikbaar"><div class="container">'
          '<div class="sec-head"><div class="t"><span class="eyebrow">Beschikbare kantoorruimte</span><h2 class="disp">Direct <em>beschikbaar</em></h2><p class="lead">Een greep uit de actuele kantoorruimte in ons aanbod.</p></div><a href="listings.html" class="btn btn--ghost">Heel het aanbod</a></div>'
          '<div class="cards-grid">'
          + _propcard("Kantoorruimte", "Gustav Mahlerlaan 2999", "Amsterdam · Zuidas", "€720 <small>/m²/jaar</small>", "vanaf 1.250 m²", "photo-1.jpg")
          + _propcard("Kantoorruimte", "Stadhouderskade 12", "Utrecht · Centrum", "€295 <small>/m²/jaar</small>", "vanaf 480 m²", "photo-2.jpg")
          + _propcard("Kantoorruimte", "Strawinskylaan 3051", "Amsterdam · Zuidas", "€540 <small>/m²/jaar</small>", "vanaf 900 m²", "hero.jpg")
          + '</div></div></section>')
    # Spaans team + aparte tekst bij de Spanje-units
    spain_html = ""
    if slug in ("aanverkoop-beleggingsvastgoed", "asset-management"):
        spain_html = ('<section class="section dark-sec" id="espana"><div class="container">'
          '<div class="two-col" style="align-items:center">'
          '<div class="prose">'
          '<span class="eyebrow" style="color:var(--green-soft)">Ook in Spanje</span>'
          '<h2 class="disp disp--light">Deze dienst ook aan de <em>Costa del Sol</em></h2>'
          f'<p class="lead">Onze dienstverlening is internationaal — en voor {title_low} hebben we ook een eigen team in Spanje. Vanuit Valencia en Estepona begeleiden onze specialisten Nederlandse investeerders op de Spaanse markt: met lokale marktkennis, een Nederlands aanspreekpunt en dezelfde Spring-aanpak.'
          ' <span data-tr="1" data-en="Our service is international — and for this discipline we have a dedicated team in Spain, in Valencia and Estepona, guiding Dutch investors in the Spanish market." data-es="Nuestro servicio es internacional — y para esta disciplina contamos con un equipo propio en España, en Valencia y Estepona, que acompaña a inversores neerlandeses en el mercado español."></span></p>'
          '<a href="locatie-estepona.html" class="btn btn--secondary" style="margin-top:6px">Bekijk kantoor Estepona</a>'
          '</div>'
          '<div class="team-grid" style="grid-template-columns:1fr 1fr">'
          + _agent("Sofia Mart&iacute;n", "Investment Advisor · Valencia", "photo-1.jpg")
          + _agent("Carlos Ferrer", "Asset Manager · Estepona", "photo-2.jpg")
          + '</div>'
          '</div></div></section>')

    html = HEAD.format(title=f"{name} — Spring Real Estate",
                       desc=f"{name}: {tag} Spring Real Estate begeleidt {dgname.lower()}s in commercieel vastgoed.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / {crumb_dg}{name}</div>
    <span class="eyebrow">Business unit</span>
    {hero_h1}
    {hero_tag}
    <div class="ph-cta"><a href="#contact" class="btn btn--primary">Neem contact op</a><a href="#cases" class="btn btn--ghost">Bekijk cases</a></div>
    <form class="search search--light search--single" onsubmit="return false">
      <label class="seg"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
        <input type="text" placeholder="Zoek op plaats, adres, type of trefwoord…" data-i18n-ph="search.phloc" aria-label="Zoeken"></label>
      <button class="search-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg> <span data-i18n="search.btn">Zoeken</span></button>
    </form>
  </div>
</section>

<nav class="bu-toc">
  <div class="container">
    <a href="#aanpak">Aanpak</a><a href="#expertises">Expertises</a><a href="#werkwijze">Zo werken wij</a><a href="#cijfers">Cijfers</a>
    <a href="#cases">Cases</a><a href="#team">Team</a><a href="#reviews">Reviews</a><a href="#faq">FAQ</a><a href="#kennis">Kennis</a>
  </div>
</nav>

<section class="logos-band"><div class="section--tight" style="padding-top:34px;padding-bottom:34px"><div class="container">
  <div class="logos-cap">Vertrouwd door opdrachtgevers &amp; partners</div>
  <div class="logos-row">
    <span class="clogo">MERIN</span><span class="clogo">a.s.r.&nbsp;<small>real estate</small></span><span class="clogo">BPD</span>
    <span class="clogo">Vesteda</span><span class="clogo">Heimstaden</span><span class="clogo">Bouwinvest</span>
  </div>
</div></div></section>

{approach_html}
<section class="section" id="expertises">
  <div class="container">
    <div class="sec-head"><div class="t"><span class="eyebrow">Diensten &amp; expertises</span><h2 class="disp">Wat wij doen binnen <em>{title_low}</em></h2></div></div>
    <div class="usp-grid">{exp_cards}</div>
  </div>
</section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Sectoren &amp; branches</span><h2>Voor wie we <em>werken</em></h2></div></div>
  <div class="sector-grid">{sectors}</div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="panel" style="text-align:center">
    <p class="disp" style="font-size:clamp(1.4rem,3vw,2.2rem);max-width:62ch;margin:0 auto;line-height:1.3"><em>"Binnen {title_low} draait alles om de juiste match tussen vraag en aanbod — onderbouwd met data en geleverd door mensen die uw markt kennen."</em></p>
    <p class="muted" style="margin-top:18px;font-weight:600">{ROSTER[idx % len(ROSTER)][1]} · {ROSTER[idx % len(ROSTER)][2]}</p>
  </div>
</div></section>

<section class="section dark-sec" id="cijfers"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow" style="color:var(--green-soft)">Cijfers</span><h2 style="color:#fff">Bewezen <em>resultaat</em></h2></div></div>
  <div class="stats-band" style="background:transparent;border:1px solid rgba(255,255,255,.12)"><div class="grid">
    <div><b>200+</b><span>transacties</span></div><div><b>15+</b><span>jaar ervaring</span></div>
    <div><b>98%</b><span>klanttevredenheid</span></div><div><b>3</b><span>locaties</span></div>
  </div></div>
</div></section>

<section class="section--soft" id="werkwijze"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Zo werken wij</span><h2 class="disp">Onze <em>aanpak</em> in 4 stappen</h2></div></div>
  <div class="bu-steps">
    <div class="bu-step"><div class="n"></div><h3>Kennismaken</h3><p>We brengen uw vraag en situatie scherp in kaart.</p></div>
    <div class="bu-step"><div class="n"></div><h3>Analyse &amp; advies</h3><p>Datagedreven advies en een concreet plan van aanpak.</p></div>
    <div class="bu-step"><div class="n"></div><h3>Uitvoering</h3><p>Wij voeren uit en houden u continu op de hoogte.</p></div>
    <div class="bu-step"><div class="n"></div><h3>Oplevering &amp; nazorg</h3><p>Resultaat opgeleverd, met nazorg waar nodig.</p></div>
  </div>
</div></section>

<section class="section--tight" id="cases"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Business cases</span><h2>Recente <em>resultaten</em></h2></div><a href="resources.html" class="btn btn--ghost">Alle cases</a></div>
  <div class="case-grid">
    <a class="case" href="#"><div class="ph"><img src="{ph}" alt=""></div><div class="body"><div class="res">+18% rendement</div><h3>Herpositionering kantoorobject</h3><p class="muted" style="font-size:.9rem">Amsterdam Zuidas</p></div></a>
    <a class="case" href="#"><div class="ph"><img src="{ph2}" alt=""></div><div class="body"><div class="res">3 weken</div><h3>Snelle invulling leegstand</h3><p class="muted" style="font-size:.9rem">Utrecht</p></div></a>
    <a class="case" href="#"><div class="ph"><img src="{PHOTOS[(idx+2)%3]}" alt=""></div><div class="body"><div class="res">€4,9 mln</div><h3>Aankoop beleggingsobject</h3><p class="muted" style="font-size:.9rem">Valencia</p></div></a>
  </div>
</div></section>

<section class="section dark-sec" id="team"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow" style="color:var(--green-soft)">Het team</span><h2 style="color:#fff">Uw <em>experts</em></h2></div><a href="agents.html" class="btn btn--secondary">Heel het team</a></div>
  <div class="team-grid">{team_html}</div>
</div></section>

<section class="section" id="reviews"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Reviews</span><h2>Wat klanten <em>zeggen</em></h2></div></div>
  <div class="rev-grid">
    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Spring dacht echt mee en leverde sneller resultaat dan verwacht."</p><div class="who"><span class="av">JV</span><span><b>Jeroen V.</b><br><span>{sec[0]}</span></span></div></div>
    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Transparant, deskundig en datagedreven advies."</p><div class="who"><span class="av">MK</span><span><b>Marit K.</b><br><span>{sec[1] if len(sec)>1 else 'Belegger'}</span></span></div></div>
    <div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"Een betrouwbare partner voor {name.lower()}."</p><div class="who"><span class="av">RG</span><span><b>Rafael G.</b><br><span>Ondernemer</span></span></div></div>
  </div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="download-card">
    <div><span class="eyebrow" style="color:var(--green-soft)">Gratis download</span><h3>Whitepaper: {name}</h3><p>Laat uw e-mail achter en ontvang ons praktische rapport direct in uw inbox.</p></div>
    <form onsubmit="return false"><input type="email" placeholder="Uw e-mailadres"><button class="btn btn--primary">Download</button></form>
  </div>
</div></section>

<section class="section--soft" id="faq"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Veelgestelde vragen</span><h2 class="disp">FAQ over <em>{title_low}</em></h2></div></div>
  <div class="split">
    <div class="faq-list">{faq_html}</div>
    <div class="aside-card aside-dark">
      <h3>Nog een vraag?</h3>
      <p style="color:#bcbeb2;font-size:.94rem">Onze specialisten beantwoorden 'm graag persoonlijk — vrijblijvend.</p>
      <a href="contact.html" class="btn btn--primary" style="width:100%;margin-top:8px">Stel uw vraag</a>
      <a href="tel:+31302001020" class="btn btn--ghost" style="width:100%;margin-top:10px;color:#fff;border-color:rgba(255,255,255,.3)">+31 30 200 10 20</a>
    </div>
  </div>
</div></section>

<section class="section--tight" id="kennis"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Kennis &amp; certificeringen</span><h2>Onderbouwd &amp; <em>gecertificeerd</em></h2></div></div>
  <div class="cert-row" style="margin-bottom:26px">
    <span class="cert">{ic(I_CHECK,"2.4")} NVM Business</span><span class="cert">{ic(I_CHECK,"2.4")} VBO</span>
    <span class="cert">{ic(I_CHECK,"2.4")} RICS</span><span class="cert">{ic(I_CHECK,"2.4")} BREEAM expertise</span>
  </div>
  <div class="blog-grid">
    <a class="post" href="resources.html"><div class="ph"><img src="{ph}" alt=""></div><div class="body"><span class="cat">Kennisartikel</span><h3>Trends in {name.lower()} voor 2026</h3><span class="date">12 juni 2026 · 5 min</span></div></a>
    <a class="post" href="resources.html"><div class="ph"><img src="{ph2}" alt=""></div><div class="body"><span class="cat">Marktinzicht</span><h3>Zo bepaalt u de juiste strategie</h3><span class="date">3 juni 2026 · 6 min</span></div></a>
    <a class="post" href="resources.html"><div class="ph"><img src="{PHOTOS[(idx+2)%3]}" alt=""></div><div class="body"><span class="cat">Begrippen</span><h3>Belangrijke termen uitgelegd</h3><span class="date">28 mei 2026 · 4 min</span></div></a>
  </div>
</div></section>

{office_html}
{spain_html}
<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Gerelateerde diensten</span><h2 class="disp">Ook <em>interessant</em></h2></div><a href="{dglink}" class="btn btn--ghost">Alle diensten</a></div>
  <div class="units-grid">{related_html}</div>
</div></section>

<section class="section--tight" id="contact"><div class="container"><div class="cta">
  <h2>Vragen over {name.lower()}?</h2>
  <p>Onze specialisten staan voor u klaar — bel, mail of plan een afspraak.</p>
  <div class="btns"><a href="contact.html" class="btn btn--light btn--lg">Neem contact op</a><a href="listings.html" class="btn btn--lg" style="background:rgba(255,255,255,.16);color:#fff;border-color:rgba(255,255,255,.4)">Bekijk aanbod</a></div>
</div></div></section>
'''
    html += FOOTER
    return html

# ----------------------------------------------------------------------
# VACATURES PAGE
# ----------------------------------------------------------------------
VACS = [
 ("Senior Real Estate Advisor","Amsterdam · Zuidas","Fulltime","Acquisitie & advies"),
 ("Investment Analyst","Utrecht","Fulltime","Investments"),
 ("Vastgoedmarketeer","Utrecht","32–40 uur","Marketing"),
 ("Taxateur RT","Amsterdam","Fulltime","Taxaties"),
 ("Asociado Comercial","Valencia (ES)","Fulltime","España"),
 ("Stage: Vastgoeddata & onderzoek","Utrecht","Stage","Data"),
]
def render_vacatures():
    rows = ""
    for t,loc,typ,team in VACS:
        rows += f'''<a class="vac" href="contact.html">
          <div><h3>{t}</h3><div class="vmeta">
            <span><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="10" r="3"/><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/></svg> {loc}</span>
            <span><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg> {typ}</span>
            <span><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{I_BLD}</svg> {team}</span>
          </div></div>
          <span class="btn btn--primary">Bekijk vacature</span>
        </a>'''
    html = HEAD.format(title="Vacatures — Spring Real Estate", desc="Werken bij Spring Real Estate. Bekijk onze vacatures in Utrecht, Amsterdam en Valencia.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / Vacatures</div>
    <span class="eyebrow" data-i18n="nav.vacatures">Vacatures</span>
    <h1>Werken bij <em style="color:var(--green);font-style:italic;font-weight:500">Spring</em></h1>
    <p class="lead">Vastgoed met hoofd &eacute;n hart. We groeien en zoeken mensen die het verschil maken — in Utrecht, Amsterdam, Valencia en Estepona.</p>
    <div class="ph-cta"><a href="#vacatures" class="btn btn--primary">Bekijk vacatures</a><a href="contact.html" class="btn btn--ghost">Open sollicitatie</a></div>
    <form class="search search--light search--single" onsubmit="return false">
      <label class="seg"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>
        <input type="text" placeholder="Zoek een functie of team…" aria-label="Zoek een vacature"></label>
      <button class="search-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg> <span data-i18n="search.btn">Zoeken</span></button>
    </form>
  </div>
</section>

<section class="section--tight"><div class="container">
  <div class="hero-stats" style="display:flex;gap:clamp(28px,5vw,56px);flex-wrap:wrap;justify-content:center;text-align:center">
    <div class="stat-pop"><b style="font-size:2rem;font-weight:800;display:block;color:var(--green)">40+</b><span class="muted">collega&#39;s</span></div>
    <div class="stat-pop"><b style="font-size:2rem;font-weight:800;display:block;color:var(--green)">3</b><span class="muted">vestigingen · NL &amp; ES</span></div>
    <div class="stat-pop"><b style="font-size:2rem;font-weight:800;display:block;color:var(--green)">18</b><span class="muted">business units</span></div>
    <div class="stat-pop"><b style="font-size:2rem;font-weight:800;display:block;color:var(--green)">15+</b><span class="muted">jaar groei</span></div>
  </div>
</div></section>

<section class="section--soft"><div class="container"><div class="two-col">
  <div class="media-tall"><img src="images/photo-1.jpg" alt="Werken bij Spring"></div>
  <div class="prose">
    <span class="eyebrow">Werken bij Spring</span>
    <h2 class="disp">Groei mee met een <em>ambitieuze</em> vastgoedgroep</h2>
    <p>Bij Spring werk je in kleine, slagvaardige teams met korte lijnen en veel eigen verantwoordelijkheid. Je krijgt de ruimte om te ondernemen, ondersteund door de beste data en tools in de markt.</p>
    <p>Of je nu start of al jaren ervaring hebt: je groeit mee met een groep die commercieel &eacute;n residentieel vastgoed onder &eacute;&eacute;n dak brengt, in Nederland en Spanje.</p>
    <a href="#vacatures" class="btn btn--primary">Bekijk vacatures</a>
  </div>
</div></div></section>

<section class="section"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Arbeidsvoorwaarden</span><h2 class="disp">Wat je bij ons <em>krijgt</em></h2></div></div>
  <div class="values-grid">
    <div class="value"><div class="ic">{ic(I_CHECK,"2.4")}</div><h3>Marktconform salaris &amp; bonus</h3><p>Een eerlijk salaris met een prestatieafhankelijke bonusregeling.</p></div>
    <div class="value"><div class="ic">{ic(I_CHECK,"2.4")}</div><h3>Opleiding &amp; groei</h3><p>Ruim opleidingsbudget en een persoonlijk ontwikkelplan.</p></div>
    <div class="value"><div class="ic">{ic(I_CHECK,"2.4")}</div><h3>Hybride werken</h3><p>Flexibel werken vanuit kantoor, thuis of een van onze vestigingen.</p></div>
    <div class="value"><div class="ic">{ic(I_CHECK,"2.4")}</div><h3>Auto / mobiliteit</h3><p>Mobiliteitsregeling die past bij jouw rol en situatie.</p></div>
    <div class="value"><div class="ic">{ic(I_CHECK,"2.4")}</div><h3>Internationale kansen</h3><p>Werk en groei mee over de grens — van Utrecht tot Valencia.</p></div>
    <div class="value"><div class="ic">{ic(I_CHECK,"2.4")}</div><h3>Teamspirit &amp; events</h3><p>Borrels, uitjes en een hecht team dat successen samen viert.</p></div>
  </div>
</div></section>

<section class="section--tight section--tint"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Sollicitatieproces</span><h2 class="disp">Zo verloopt je <em>sollicitatie</em></h2></div></div>
  <div class="bu-steps">
    <div class="bu-step"><div class="n"></div><h3>Solliciteer</h3><p>Stuur je cv en motivatie — binnen 5 werkdagen hoor je van ons.</p></div>
    <div class="bu-step"><div class="n"></div><h3>Kennismaking</h3><p>Een open gesprek over jou, je ambities en het team.</p></div>
    <div class="bu-step"><div class="n"></div><h3>Verdiepend gesprek</h3><p>We gaan dieper in op de rol en je vakkennis.</p></div>
    <div class="bu-step"><div class="n"></div><h3>Aanbod &amp; start</h3><p>Een passend aanbod en een warm welkom in het team.</p></div>
  </div>
</div></section>

<section class="section dark-sec"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow" style="color:var(--green-soft)">Hear from our leaders</span><h2 class="disp" style="color:#fff">De mensen achter <em>Spring</em></h2><p class="lead">Een mix van jong en ervaren talent — luister naar wat onze mensen drijft.</p></div></div>
  <div class="rev-grid">
    <div class="review" style="background:var(--dark-2);border-color:rgba(255,255,255,.1)"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p style="color:#e7e9e0">"Bij Spring krijg je vanaf dag één verantwoordelijkheid en de ruimte om te ondernemen."</p><div class="who"><span class="av">SM</span><span><b style="color:#fff">Sofia Mart&iacute;n</b><br><span style="color:#a9ab9f">Investment Advisor · Valencia</span></span></div></div>
    <div class="review" style="background:var(--dark-2);border-color:rgba(255,255,255,.1)"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p style="color:#e7e9e0">"Data en mensenwerk komen hier echt samen. Dat maakt ons advies sterker."</p><div class="who"><span class="av">LB</span><span><b style="color:#fff">Lars Bakker</b><br><span style="color:#a9ab9f">Asset Manager · Utrecht</span></span></div></div>
    <div class="review" style="background:var(--dark-2);border-color:rgba(255,255,255,.1)"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p style="color:#e7e9e0">"We groeien snel, maar houden de korte lijnen en de teamspirit."</p><div class="who"><span class="av">DM</span><span><b style="color:#fff">Daan van der Meer</b><br><span style="color:#a9ab9f">Senior Advisor · Amsterdam</span></span></div></div>
  </div>
</div></section>

<section class="section" id="vacatures"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Open posities</span><h2 class="disp">Onze <em>vacatures</em></h2></div><a href="contact.html" class="btn btn--ghost">Open sollicitatie</a></div>
  <div class="vac-list">{rows}</div>
</div></section>

<section class="section--soft"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Veelgestelde vragen</span><h2 class="disp">Vragen over <em>solliciteren</em></h2></div></div>
  <div class="faq-list">
    <details class="faq-item" open><summary>Kan ik een open sollicitatie sturen?<span class="pl">+</span></summary><div class="ans">Zeker. Staat er geen passende vacature tussen? Stuur je cv en motivatie en we kijken graag of er een match is.</div></details>
    <details class="faq-item"><summary>Bieden jullie stages en werkstudentplekken?<span class="pl">+</span></summary><div class="ans">Ja, we hebben regelmatig plek voor stagiairs en werkstudenten — onder meer bij vastgoeddata en marketing.</div></details>
    <details class="faq-item"><summary>Hoe snel hoor ik na mijn sollicitatie iets?<span class="pl">+</span></summary><div class="ans">Doorgaans binnen vijf werkdagen. We houden je gedurende het hele proces persoonlijk op de hoogte.</div></details>
  </div>
</div></section>

<section class="section--tight"><div class="container"><div class="cta">
  <h2>Geen passende vacature?</h2>
  <p>We maken graag kennis. Stuur een open sollicitatie — wie weet groeien we samen.</p>
  <div class="btns"><a href="contact.html" class="btn btn--light btn--lg">Open sollicitatie</a><a href="#vacatures" class="btn btn--lg" style="background:rgba(255,255,255,.16);color:#fff;border-color:rgba(255,255,255,.4)">Bekijk vacatures</a></div>
</div></div></section>
'''
    html += FOOTER
    return html

# ----------------------------------------------------------------------
# PERSON PROFILE PAGES (CBRE-style)
# ----------------------------------------------------------------------
# (slug, name, role, location, years, specialisme, photo, sectoren[])
ROSTER = [
 ("daan-van-der-meer","Daan van der Meer","Senior Real Estate Advisor","Amsterdam · Zuidas","15+ jaar",
   "Kantoorhuisvesting en verhuur op de Zuidas","photo-2.jpg",["Scale-ups","Corporates","Tech"]),
 ("sofia-martin","Sofia Mart&iacute;n","Investment Advisor","Valencia · Espa&ntilde;a","10+ jaar",
   "Beleggingen en internationale acquisities in Spanje","photo-1.jpg",["NL-investeerders","Family offices","Ontwikkelaars"]),
 ("lars-bakker","Lars Bakker","Asset Manager","Utrecht","12+ jaar",
   "Asset management en waardecreatie van portefeuilles","hero.jpg",["Beleggers","Fondsen","Institutioneel"]),
 ("emma-de-vries","Emma de Vries","Head of Marketing &amp; Communications","Utrecht","8+ jaar",
   "Vastgoedmarketing, campagnes en communicatie","photo-1.jpg",["Eigenaren","Ontwikkelaars"]),
 ("thomas-jansen","Thomas Jansen","Taxateur RT","Amsterdam","14+ jaar",
   "Taxaties van beleggings- en grootzakelijk vastgoed","photo-2.jpg",["Banken","Beleggers","Accountants"]),
 ("nina-aydin","Nina Aydin","Strategic Advisor","Amsterdam","9+ jaar",
   "Strategisch advies en marktinzichten","hero.jpg",["Family offices","Fondsen","Corporates"]),
]
def render_profile(p):
    slug,name,role,loc,years,spec,photo,sectors = p
    mail = slug.replace("-",".") + "@springrealestate.com"
    sect = "".join(f'<div class="sector">{ic(I_CHECK,"2.4")} {s}</div>' for s in sectors)
    html = HEAD.format(title=f"{name} — Spring Real Estate", desc=f"{name}, {role} bij Spring Real Estate. {spec}.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / <a href="agents.html">Agents</a> / {name}</div>
    <span class="eyebrow">Ons team</span>
    <h1>{name}</h1>
    <p class="lead">{role} · {loc}</p>
    <div class="ph-cta">
      <a href="mailto:{mail}" class="btn btn--primary">E-mail {name.split(' ')[0]}</a>
      <a href="tel:+31302001020" class="btn btn--ghost">+31 30 200 10 20</a>
      <a href="#" class="btn btn--ghost">LinkedIn</a>
    </div>
  </div>
</section>

<section class="section"><div class="container">
  <div class="two-col">
    <div class="media-tall"><img src="images/{photo}" alt="{name}"></div>
    <div class="prose">
      <span class="eyebrow">Professional experience</span>
      <h2 class="disp">Over <em>{name.split(' ')[0]}</em></h2>
      <p>{name} is {role.split('·')[0].strip().lower()} bij Spring Real Estate in {loc.split('·')[0].strip()}, met {years} ervaring. {name.split(' ')[0]} is gespecialiseerd in {spec.lower()} en werkt datagedreven samen met klanten aan de beste oplossing.</p>
      <p>"De beste resultaten ontstaan waar marktkennis en persoonlijk contact samenkomen. Ik denk met u mee over de lange termijn — niet alleen over de transactie van vandaag."</p>
      <a href="contact.html" class="btn btn--primary" style="margin-top:6px">Plan een afspraak</a>
    </div>
  </div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Specialisme</span><h2 class="disp">Wie {name.split(' ')[0]} <em>bedient</em></h2></div></div>
  <div class="sector-grid">{sect}</div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Recent werk</span><h2 class="disp">Gerelateerd <em>aanbod</em></h2></div><a href="listings.html" class="btn btn--ghost">Heel het aanbod</a></div>
  <div class="cards-grid">
    <a class="prop-card" href="listing-detail.html"><div class="ph"><span class="tag">Te huur</span><img src="images/photo-1.jpg" alt=""></div><div class="body"><span class="ptype">Kantoorruimte</span><h3>Gustav Mahlerlaan 2999</h3><span class="addr">Amsterdam · Zuidas</span><div class="meta"><span class="price">€720 <small>/m²/jaar</small></span></div></div></a>
    <a class="prop-card" href="listing-detail.html"><div class="ph"><span class="tag">Te koop</span><img src="images/photo-2.jpg" alt=""></div><div class="body"><span class="ptype">Beleggingsobject</span><h3>Stadhouderskade 12</h3><span class="addr">Utrecht · Centrum</span><div class="meta"><span class="price">€4,9 mln <small>k.k.</small></span></div></div></a>
    <a class="prop-card" href="listing-detail.html"><div class="ph"><span class="tag">Te huur</span><img src="images/hero.jpg" alt=""></div><div class="body"><span class="ptype">Serviced office</span><h3>Paseo de la Alameda 7</h3><span class="addr">Valencia · España</span><div class="meta"><span class="price">€1.450 <small>/maand</small></span></div></div></a>
  </div>
</div></section>
'''
    html += FOOTER
    return html

# ----------------------------------------------------------------------
# LOCATION PAGES (eigen pagina per kantoor)
# ----------------------------------------------------------------------
LOCATIES = {
 "utrecht":   {"name":"Utrecht","flag":"\U0001F1F3\U0001F1F1","tag":"Hoofdkantoor","addr":"Stadhouderskade 12 · 3531 BJ Utrecht","count":"8",
   "intro":"Vanuit ons hoofdkantoor in Utrecht bedienen we heel Nederland. Centraal gelegen en uitstekend bereikbaar — de thuisbasis van onze taxatie-, asset management- en marketingteams."},
 "amsterdam": {"name":"Amsterdam","flag":"\U0001F1F3\U0001F1F1","tag":"Zuidas","addr":"Gustav Mahlerlaan 2999 · 1082 MK Amsterdam","count":"12",
   "intro":"Op de Zuidas, in het zakelijke hart van Nederland, zit ons team voor kantoorhuisvesting, serviced offices en investments — dicht bij onze opdrachtgevers."},
 "valencia":  {"name":"Valencia","flag":"\U0001F1EA\U0001F1F8","tag":"España","addr":"Paseo de la Alameda 7 · 46023 Valencia","count":"7",
   "intro":"Onze vaste basis in Spanje. Vanuit Valencia begeleiden we Nederlandse investeerders en gebruikers bij acquisities en huisvesting op de Spaanse markt."},
 "estepona":  {"name":"Estepona","flag":"\U0001F1EA\U0001F1F8","tag":"España · Costa del Sol","addr":"Avenida Litoral 12 · 29680 Estepona","count":"6",
   "intro":"Aan de Costa del Sol begeleiden we vanuit Estepona investeringen en huisvesting in Zuid-Spanje — van residentieel tot commercieel vastgoed, met lokale kennis en een Nederlands aanspreekpunt."},
}
def render_locatie(key):
    L = LOCATIES[key]
    team3 = "".join(
        f'<div class="agent"><div class="ph"><img src="images/{p[6]}" alt=""></div><div class="body"><div class="name">{p[1]}</div><div class="role">{p[2]}</div><div class="socials"><a href="profile-{p[0]}.html">in</a><a href="#">@</a></div></div></div>'
        for p in ROSTER[:3])
    html = HEAD.format(title=f"{L['name']} — Spring Real Estate", desc=f"Spring Real Estate {L['name']}: {L['addr']}. Aanbod, team en contact in {L['name']}.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / <a href="locaties.html">Locaties</a> / {L['name']}</div>
    <span class="eyebrow">{L['flag']} {L['tag']}</span>
    <h1>Spring in <em style="color:var(--green);font-style:italic;font-weight:500">{L['name']}</em></h1>
    <p class="lead">{L['addr']}</p>
    <div class="ph-cta"><a href="listings.html" class="btn btn--primary">Aanbod in {L['name']}</a><a href="contact.html" class="btn btn--ghost">Route &amp; contact</a></div>
  </div>
</section>

<section class="section"><div class="container"><div class="two-col">
  <div class="prose"><span class="eyebrow">Over deze locatie</span><h2 class="disp">Lokaal sterk in <em>{L['name']}</em></h2><p>{L['intro']}</p>
    <div class="stat-pop" style="display:flex;gap:34px;margin-top:18px"><div><b style="font-size:1.9rem;font-weight:800;display:block;color:var(--green)">{L['count']}</b><span class="muted">objecten beschikbaar</span></div><div><b style="font-size:1.9rem;font-weight:800;display:block;color:var(--green)">15+</b><span class="muted">jaar in de regio</span></div></div>
  </div>
  <div class="loc-map" style="aspect-ratio:4/3;border-radius:var(--r-lg);overflow:hidden;position:relative;background:linear-gradient(135deg,#e9efe0,#dfe7d2);border:1px solid var(--line)">
    <svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" style="position:absolute;inset:0;width:100%;height:100%"><rect width="400" height="300" fill="#e6ecdb"/><path d="M0 170 Q120 150 240 175 T400 160" stroke="#c7d3ad" stroke-width="2" fill="none"/><path d="M90 0 L110 300" stroke="#d3ddbf" stroke-width="2"/></svg>
    <span class="pin2" style="position:absolute;left:50%;top:46%;transform:translate(-50%,-100%)"><span class="dot" style="display:block;width:30px;height:30px;border-radius:50% 50% 50% 0;background:var(--green);transform:rotate(-45deg);border:3px solid #fff;box-shadow:0 6px 14px -4px rgba(0,0,0,.4)"></span></span>
  </div>
</div></div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Kantoorimpressie</span><h2 class="disp">Zo ziet ons kantoor in <em>{L['name']}</em> eruit</h2></div></div>
  <div class="cards-grid">
    <div style="border-radius:var(--r);overflow:hidden;aspect-ratio:4/3"><img src="images/photo-1.jpg" alt="Kantoor {L['name']}" style="width:100%;height:100%;object-fit:cover"></div>
    <div style="border-radius:var(--r);overflow:hidden;aspect-ratio:4/3"><img src="images/photo-2.jpg" alt="Kantoor {L['name']}" style="width:100%;height:100%;object-fit:cover"></div>
    <div style="border-radius:var(--r);overflow:hidden;aspect-ratio:4/3"><img src="images/hero.jpg" alt="Kantoor {L['name']}" style="width:100%;height:100%;object-fit:cover"></div>
  </div>
</div></section>

<section class="section dark-sec"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow" style="color:var(--green-soft)">Het team in {L['name']}</span><h2 class="disp" style="color:#fff">Uw <em>aanspreekpunt</em></h2></div><a href="agents.html" class="btn btn--secondary">Heel het team</a></div>
  <div class="team-grid">{team3}</div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Aanbod</span><h2 class="disp">Beschikbaar in <em>{L['name']}</em></h2></div><a href="listings.html" class="btn btn--ghost">Bekijk alles</a></div>
  <div class="cards-grid">
    <a class="prop-card" href="listing-detail.html"><div class="ph"><span class="tag">Te huur</span><img src="images/photo-1.jpg" alt=""></div><div class="body"><span class="ptype">Kantoorruimte</span><h3>{L['name']} · centraal</h3><span class="addr">{L['name']}</span><div class="meta"><span class="price">€595 <small>/m²/jaar</small></span></div></div></a>
    <a class="prop-card" href="listing-detail.html"><div class="ph"><span class="tag">Te koop</span><img src="images/photo-2.jpg" alt=""></div><div class="body"><span class="ptype">Beleggingsobject</span><h3>{L['name']} · zakendistrict</h3><span class="addr">{L['name']}</span><div class="meta"><span class="price">€3,8 mln <small>k.k.</small></span></div></div></a>
    <a class="prop-card" href="listing-detail.html"><div class="ph"><span class="tag">Te huur</span><img src="images/hero.jpg" alt=""></div><div class="body"><span class="ptype">Serviced office</span><h3>{L['name']} · flex</h3><span class="addr">{L['name']}</span><div class="meta"><span class="price">€1.250 <small>/maand</small></span></div></div></a>
  </div>
</div></section>
'''
    html += FOOTER
    return html

# ----------------------------------------------------------------------
# SECTOREN / INDUSTRIES PAGE
# ----------------------------------------------------------------------
SECTOREN = [
 ("Kantoren","Huisvesting, verhuur en belegging in kantoorvastgoed."),
 ("Logistiek &amp; bedrijfsruimte","Distributiecentra, hallen en last-mile-locaties."),
 ("Retail &amp; winkels","Winkel- en horecaruimte op de juiste locatie."),
 ("Zorgvastgoed","Vastgoedoplossingen voor zorgaanbieders en investeerders."),
 ("Residentieel","Woningen en residenti&euml;le beleggingsportefeuilles."),
 ("Hospitality &amp; leisure","Hotels, horeca en vrijetijdsvastgoed."),
 ("Onderwijs &amp; publiek","Vastgoed voor onderwijs en (semi)publieke sector."),
 ("Data centers &amp; industrie","Specialistisch vastgoed voor tech en industrie."),
]
def render_sectoren():
    cards = "".join(f'''<a class="dienst-card" href="listings.html"><span class="dc-ic">{ic(I_BLD)}</span><h3>{n}</h3><p>{d}</p><span class="link-arrow">Bekijk sector {arrow()}</span></a>''' for n,d in SECTOREN)
    html = HEAD.format(title="Sectoren — Spring Real Estate", desc="De sectoren waarin Spring Real Estate actief is: kantoren, logistiek, retail, zorg, residentieel en meer.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero"><div class="container">
  <div class="crumbs"><a href="index.html">Home</a> / Sectoren</div>
  <span class="eyebrow">Sectoren &amp; specialismen</span>
  <h1>Expertise per <em style="color:var(--green);font-style:italic;font-weight:500">sector</em></h1>
  <p class="lead">Een brede vastgoedgroep — commercieel &eacute;n residentieel. We kennen de dynamiek van elke markt waarin u actief bent.</p>
</div></section>
<section class="section"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Onze sectoren</span><h2 class="disp">Waar we het <em>verschil</em> maken</h2></div></div>
  <div class="dienst-grid">{cards}</div>
</div></section>
'''
    html += FOOTER
    return html

# ----------------------------------------------------------------------
# CASES / KLANTVERHALEN PAGE
# ----------------------------------------------------------------------
CASES = [
 ("+18% rendement","Herpositionering kantoorobject","Asset management","Amsterdam","photo-1.jpg"),
 ("3 weken","Snelle invulling van leegstand","Verhuur","Utrecht","photo-2.jpg"),
 ("€4,9 mln","Aankoop beleggingsobject","Investments","Valencia","hero.jpg"),
 ("12.000 m²","Build-to-suit logistiek","Design &amp; Build","Tilburg","photo-2.jpg"),
 ("98% bezetting","Portefeuille-optimalisatie","Asset management","Randstad","photo-1.jpg"),
 ("€720/m²","Verhuur turn-key kantoor","Verhuur","Amsterdam","hero.jpg"),
]
def render_cases():
    cards = "".join(f'''<a class="case" href="#"><div class="ph"><img src="images/{img}" alt=""></div><div class="body"><div class="res">{res}</div><h3>{title}</h3><p class="muted" style="font-size:.9rem">{sector} · {loc}</p></div></a>''' for res,title,sector,loc,img in CASES)
    html = HEAD.format(title="Klantverhalen &amp; cases — Spring Real Estate", desc="Klantverhalen en business cases van Spring Real Estate — bewezen resultaat in commercieel en residentieel vastgoed.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero"><div class="container">
  <div class="crumbs"><a href="index.html">Home</a> / Klantverhalen</div>
  <span class="eyebrow">Klantverhalen &amp; cases</span>
  <h1>Bewezen <em style="color:var(--green);font-style:italic;font-weight:500">resultaat</em></h1>
  <p class="lead">Echte projecten, echte resultaten. Filter op sector of doelgroep en ontdek hoe we waarde cre&euml;ren.</p>
</div></section>
<section class="section"><div class="container">
  <div class="team-filter">
    <a href="#" class="active">Alle</a><a href="#">Verhuur</a><a href="#">Investments</a><a href="#">Asset management</a><a href="#">Design &amp; Build</a>
  </div>
  <div class="case-grid">{cards}</div>
</div></section>
'''
    html += FOOTER
    return html

# ----------------------------------------------------------------------
# WRITE
# ----------------------------------------------------------------------
def write(name, html):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(html)
    return name

def main():
    written = []
    for key in DOELGROEPEN:
        written.append(write(f"doelgroep-{key}.html", render_doelgroep(key)))
    for i,u in enumerate(UNITS):
        written.append(write(f"unit-{u[0]}.html", render_unit(i,u)))
    written.append(write("vacatures.html", render_vacatures()))
    for p in ROSTER:
        written.append(write(f"profile-{p[0]}.html", render_profile(p)))
    for key in LOCATIES:
        written.append(write(f"locatie-{key}.html", render_locatie(key)))
    written.append(write("sectoren.html", render_sectoren()))
    written.append(write("cases.html", render_cases()))
    print(f"Generated {len(written)} pages:")
    for w in written: print("  "+w)

if __name__ == "__main__":
    main()
