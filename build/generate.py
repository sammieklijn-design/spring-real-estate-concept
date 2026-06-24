# -*- coding: utf-8 -*-
"""
Spring Real Estate — static page generator.
Generates: 4 doelgroep-hubs, 21 business-unit pages, vacatures page.
Run:  python build/generate.py
Shared chrome (header/footer/mobile menu) is defined once here so every
page stays consistent and multilingual (NL/EN/ES via js/i18n.js).
"""
import os, json, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from listings_data import LISTINGS

def he(s):  # escape text for HTML
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def esc(s):  # escape for attribute value
    return he(s).replace('"',"&quot;")
def _initials(name):
    parts = [w for w in re.sub(r'&[a-z]+;', '', name).split() if w[:1].isupper()]
    return ((parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper()) if parts else "S"
def phinner(name, photo):
    """portretfoto indien beschikbaar, anders een nette initialen-avatar (geen foto)."""
    if photo:
        return f'<img src="{photo}" alt="{esc(name)}">'
    return f'<span class="ph-initials">{_initials(name)}</span>'
def trh(en, es):  # data-tr attributes for the i18n layer (body translations)
    a = ""
    if en or es:
        a = ' data-tr="1"'
        if en: a += f' data-en="{esc(en)}"'
        if es: a += f' data-es="{esc(es)}"'
    return a

# ----------------------------------------------------------------------
# UI-LABEL VERTALINGEN (NL -> EN, ES) voor de gegenereerde pagina's.
# localize() injecteert de data-tr/data-en/data-es attributen in elk
# element waarvan de volledige inhoud exact een NL-sleutel is. Zo worden
# alle 35 gegenereerde pagina's vanuit één plek drietalig.
# ----------------------------------------------------------------------
UI_TR = {
 # knoppen / generieke labels
 "Bekijk diensten": ("View services","Ver servicios"),
 "Plan een gesprek": ("Book a consultation","Reserva una consulta"),
 "Bekijk het aanbod": ("View listings","Ver inmuebles"),
 "Bekijk aanbod": ("View listings","Ver inmuebles"),
 "Heel het aanbod": ("All listings","Todos los inmuebles"),
 "Bekijk alles": ("View all","Ver todo"),
 "Alle sectoren": ("All sectors","Todos los sectores"),
 "Alle cases": ("All cases","Todos los casos"),
 "Alle diensten": ("All services","Todos los servicios"),
 "Heel het team": ("Meet the team","Todo el equipo"),
 "Neem contact op": ("Get in touch","Contáctanos"),
 "Bekijk cases": ("View cases","Ver casos"),
 "Download": ("Download","Descargar"),
 "Route &amp; contact": ("Directions &amp; contact","Cómo llegar y contacto"),
 "LinkedIn": ("LinkedIn","LinkedIn"),
 # eyebrows
 "Ondersteunend": ("Support","Soporte"),
 "Cijfers": ("Figures","Cifras"),
 "Ook in Spanje": ("Also in Spain","También en España"),
 "Onze visie": ("Our vision","Nuestra visión"),
 "Professional experience": ("Professional experience","Experiencia profesional"),
 "Hear from our leaders": ("Hear from our leaders","Escucha a nuestros líderes"),
 "Bewezen <em>resultaat</em>": ("Proven <em>results</em>","<em>Resultados</em> probados"),
 "Niet zeker welke dienst u nodig heeft?": ("Not sure which service you need?","¿No sabes qué servicio necesitas?"),
 "Geen passende vacature?": ("No suitable vacancy?","¿No encuentras una vacante adecuada?"),
 "Aanpak": ("Approach","Enfoque"),
 "Expertises": ("Expertise","Especialidades"),
 "Zo pakken we het <em>aan</em>": ("How we <em>approach it</em>","Cómo lo <em>abordamos</em>"),
 "Groei mee met een <em>ambitieuze</em> vastgoedgroep": ("Grow with an <em>ambitious</em> real estate group","Crece con un grupo inmobiliario <em>ambicioso</em>"),
 "Deze dienst ook aan de <em>Costa del Sol</em>": ("This service on the <em>Costa del Sol</em> too","Este servicio también en la <em>Costa del Sol</em>"),
 # sectoren (los & in koppen)
 "Kantoren": ("Offices","Oficinas"),
 "Logistiek &amp; bedrijfsruimte": ("Logistics &amp; industrial","Logística e industrial"),
 "Retail &amp; winkels": ("Retail &amp; shops","Retail y comercios"),
 "Zorgvastgoed": ("Healthcare real estate","Inmuebles sanitarios"),
 "Residentieel": ("Residential","Residencial"),
 "Hospitality": ("Hospitality","Hostelería"),
 "Hospitality &amp; leisure": ("Hospitality &amp; leisure","Hostelería y ocio"),
 "Onderwijs &amp; publiek": ("Education &amp; public","Educación y sector público"),
 "Data centers &amp; industrie": ("Data centers &amp; industry","Centros de datos e industria"),
 "Onze diensten": ("Our services","Nuestros servicios"),
 "Sectoren": ("Sectors","Sectores"),
 "Onze aanpak": ("Our approach","Nuestro enfoque"),
 "Beschikbare werkplekken": ("Available workspaces","Espacios de trabajo disponibles"),
 "Beschikbare kantoorruimte": ("Available office space","Oficinas disponibles"),
 "Business unit": ("Business unit","Unidad de negocio"),
 "Diensten &amp; expertises": ("Services &amp; expertise","Servicios y especialidades"),
 "Sectoren &amp; branches": ("Sectors &amp; industries","Sectores e industrias"),
 "Zo werken wij": ("How we work","Cómo trabajamos"),
 "Business cases": ("Business cases","Casos de éxito"),
 "Het team": ("The team","El equipo"),
 "Reviews": ("Reviews","Reseñas"),
 "Gratis download": ("Free download","Descarga gratuita"),
 "Veelgestelde vragen": ("Frequently asked questions","Preguntas frecuentes"),
 "Kennis &amp; certificeringen": ("Knowledge &amp; certifications","Conocimiento y certificaciones"),
 "Gerelateerde diensten": ("Related services","Servicios relacionados"),
 "Werken bij Spring": ("Working at Spring","Trabajar en Spring"),
 "Arbeidsvoorwaarden": ("Benefits","Condiciones laborales"),
 "Sollicitatieproces": ("Application process","Proceso de selección"),
 "Open posities": ("Open positions","Vacantes abiertas"),
 "Ons team": ("Our team","Nuestro equipo"),
 "Specialisme": ("Specialism","Especialidad"),
 "Recent werk": ("Recent work","Trabajo reciente"),
 "Over deze locatie": ("About this location","Sobre esta ubicación"),
 "Kantoorimpressie": ("Office impression","Vista de la oficina"),
 "Aanbod": ("Listings","Inmuebles"),
 "Sectoren &amp; specialismen": ("Sectors &amp; specialisms","Sectores y especialidades"),
 "Onze sectoren": ("Our sectors","Nuestros sectores"),
 "Klantverhalen &amp; cases": ("Client stories &amp; cases","Casos de clientes"),
 # headings (incl. <em>)
 "Kies een <em>business unit</em>": ("Choose a <em>business unit</em>","Elige una <em>unidad de negocio</em>"),
 "Expertise in <em>elke sector</em>": ("Expertise in <em>every sector</em>","Experiencia en <em>cada sector</em>"),
 "Direct <em>beschikbaar</em>": ("Immediately <em>available</em>","<em>Disponible</em> de inmediato"),
 "Voor wie we <em>werken</em>": ("Who we <em>work for</em>","Para quién <em>trabajamos</em>"),
 "Onze <em>aanpak</em> in 4 stappen": ("Our <em>approach</em> in 4 steps","Nuestro <em>enfoque</em> en 4 pasos"),
 "Recente <em>resultaten</em>": ("Recent <em>results</em>","<em>Resultados</em> recientes"),
 "Uw <em>experts</em>": ("Your <em>experts</em>","Tus <em>expertos</em>"),
 "Wat klanten <em>zeggen</em>": ("What clients <em>say</em>","Lo que dicen los <em>clientes</em>"),
 "Onderbouwd &amp; <em>gecertificeerd</em>": ("Substantiated &amp; <em>certified</em>","Fundamentado y <em>certificado</em>"),
 "Ook <em>interessant</em>": ("Also <em>relevant</em>","También <em>relevante</em>"),
 "Wat je bij ons <em>krijgt</em>": ("What you <em>get</em> with us","Lo que <em>obtienes</em> con nosotros"),
 "Zo verloopt je <em>sollicitatie</em>": ("How your <em>application</em> works","Cómo es tu <em>candidatura</em>"),
 "Onze <em>vacatures</em>": ("Our <em>vacancies</em>","Nuestras <em>vacantes</em>"),
 "Vragen over <em>solliciteren</em>": ("Questions about <em>applying</em>","Preguntas sobre <em>candidaturas</em>"),
 "De mensen achter <em>Spring</em>": ("The people behind <em>Spring</em>","Las personas detrás de <em>Spring</em>"),
 "Waar we het <em>verschil</em> maken": ("Where we make the <em>difference</em>","Donde marcamos la <em>diferencia</em>"),
 "Gerelateerd <em>aanbod</em>": ("Related <em>listings</em>","Inmuebles <em>relacionados</em>"),
 "Uw <em>aanspreekpunt</em>": ("Your <em>point of contact</em>","Tu <em>punto de contacto</em>"),
 # leads / paragraphs
 "Klik op een dienst voor de volledige business-unit-pagina met experts, cases en antwoorden.":
   ("Click a service for the full business-unit page with experts, cases and answers.",
    "Haz clic en un servicio para ver la página completa de la unidad de negocio, con expertos, casos y respuestas."),
 "Van kantoren en logistiek tot retail, zorg en residentieel vastgoed.":
   ("From offices and logistics to retail, healthcare and residential real estate.",
    "Desde oficinas y logística hasta retail, salud e inmuebles residenciales."),
 "Een greep uit onze serviced offices en flexibele werkplekken.":
   ("A selection of our serviced offices and flexible workspaces.",
    "Una selección de nuestras oficinas serviced y espacios flexibles."),
 "Een greep uit de actuele kantoorruimte in ons aanbod.":
   ("A selection of the current office space in our portfolio.",
    "Una selección del espacio de oficinas actual de nuestra cartera."),
 "Onze adviseurs denken graag met u mee — vrijblijvend en vanuit uw vraag.":
   ("Our advisors are happy to think along with you — no obligation, starting from your question.",
    "Nuestros asesores estarán encantados de ayudarte — sin compromiso y partiendo de tu pregunta."),
 "Onze specialisten staan voor u klaar — bel, mail of plan een afspraak.":
   ("Our specialists are ready to help — call, email or book an appointment.",
    "Nuestros especialistas están a tu disposición — llama, escribe o reserva una cita."),
 "Laat uw e-mail achter en ontvang ons praktische rapport direct in uw inbox.":
   ("Leave your email and receive our practical report straight in your inbox.",
    "Déjanos tu correo y recibe nuestro informe práctico directamente en tu bandeja."),
 "Een mix van jong en ervaren talent — luister naar wat onze mensen drijft.":
   ("A mix of young and experienced talent — hear what drives our people.",
    "Una mezcla de talento joven y experimentado — escucha qué motiva a nuestra gente."),
 "We maken graag kennis. Stuur een open sollicitatie — wie weet groeien we samen.":
   ("We'd love to meet you. Send an open application — who knows, we might grow together.",
    "Nos encantaría conocerte. Envía una candidatura abierta — quién sabe, quizá crezcamos juntos."),
 # werkwijze-stappen (business unit)
 "Kennismaken": ("Introduction","Conocernos"),
 "We brengen uw vraag en situatie scherp in kaart.":
   ("We map your question and situation precisely.","Analizamos tu pregunta y situación con precisión."),
 "Analyse &amp; advies": ("Analysis &amp; advice","Análisis y asesoramiento"),
 "Datagedreven advies en een concreet plan van aanpak.":
   ("Data-driven advice and a concrete action plan.","Asesoramiento basado en datos y un plan de acción concreto."),
 "Uitvoering": ("Execution","Ejecución"),
 "Wij voeren uit en houden u continu op de hoogte.":
   ("We execute and keep you continuously informed.","Ejecutamos y te mantenemos informado en todo momento."),
 "Oplevering &amp; nazorg": ("Delivery &amp; aftercare","Entrega y seguimiento"),
 "Resultaat opgeleverd, met nazorg waar nodig.":
   ("Result delivered, with aftercare where needed.","Resultado entregado, con seguimiento cuando sea necesario."),
 # cases
 "Herpositionering kantoorobject": ("Office repositioning","Reposicionamiento de oficina"),
 "Snelle invulling leegstand": ("Vacancy filled fast","Vacante cubierta rápido"),
 "Aankoop beleggingsobject": ("Investment acquisition","Adquisición de inversión"),
 # blog/kennis kaarten
 "Kennisartikel": ("Knowledge article","Artículo"),
 "Marktinzicht": ("Market insight","Análisis de mercado"),
 "Zo bepaalt u de juiste strategie": ("How to set the right strategy","Cómo definir la estrategia correcta"),
 "Begrippen": ("Glossary","Conceptos"),
 "Belangrijke termen uitgelegd": ("Key terms explained","Términos clave explicados"),
 "Nog een vraag?": ("Another question?","¿Otra pregunta?"),
 # rollen / property-labels
 "Senior Adviseur": ("Senior Advisor","Asesor sénior"),
 "Adviseur": ("Advisor","Asesor"),
 "Specialist": ("Specialist","Especialista"),
 "Beschikbaar": ("Available","Disponible"),
 "Te huur": ("For rent","En alquiler"),
 "Te koop": ("For sale","En venta"),
 "Kantoorruimte": ("Office space","Oficina"),
 "Beleggingsobject": ("Investment property","Inmueble de inversión"),
 # vacatures
 "Bekijk vacature": ("View vacancy","Ver vacante"),
 "Bekijk vacatures": ("View vacancies","Ver vacantes"),
 "Open sollicitatie": ("Open application","Candidatura abierta"),
 "Marktconform salaris &amp; bonus": ("Competitive salary &amp; bonus","Salario competitivo y bonus"),
 "Een eerlijk salaris met een prestatieafhankelijke bonusregeling.":
   ("A fair salary with a performance-based bonus scheme.","Un salario justo con un bonus por desempeño."),
 "Opleiding &amp; groei": ("Training &amp; growth","Formación y crecimiento"),
 "Ruim opleidingsbudget en een persoonlijk ontwikkelplan.":
   ("A generous training budget and a personal development plan.","Amplio presupuesto de formación y un plan de desarrollo personal."),
 "Hybride werken": ("Hybrid working","Trabajo híbrido"),
 "Flexibel werken vanuit kantoor, thuis of een van onze vestigingen.":
   ("Work flexibly from the office, home or one of our branches.","Trabaja con flexibilidad desde la oficina, casa o una de nuestras sedes."),
 "Auto / mobiliteit": ("Car / mobility","Coche / movilidad"),
 "Mobiliteitsregeling die past bij jouw rol en situatie.":
   ("A mobility scheme that fits your role and situation.","Un plan de movilidad adaptado a tu puesto y situación."),
 "Internationale kansen": ("International opportunities","Oportunidades internacionales"),
 "Werk en groei mee over de grens — van Utrecht tot Valencia.":
   ("Work and grow across borders — from Utrecht to Valencia.","Trabaja y crece más allá de las fronteras — de Utrecht a Valencia."),
 "Teamspirit &amp; events": ("Team spirit &amp; events","Espíritu de equipo y eventos"),
 "Borrels, uitjes en een hecht team dat successen samen viert.":
   ("Drinks, outings and a close-knit team that celebrates success together.","Aperitivos, salidas y un equipo unido que celebra los éxitos juntos."),
 "Solliciteer": ("Apply","Postula"),
 "Stuur je cv en motivatie — binnen 5 werkdagen hoor je van ons.":
   ("Send your CV and motivation — you'll hear from us within 5 working days.","Envía tu CV y motivación — te responderemos en 5 días laborables."),
 "Kennismaking": ("Introduction","Conocernos"),
 "Een open gesprek over jou, je ambities en het team.":
   ("An open conversation about you, your ambitions and the team.","Una conversación abierta sobre ti, tus ambiciones y el equipo."),
 "Verdiepend gesprek": ("In-depth interview","Entrevista en profundidad"),
 "We gaan dieper in op de rol en je vakkennis.":
   ("We dive deeper into the role and your expertise.","Profundizamos en el puesto y tus conocimientos."),
 "Aanbod &amp; start": ("Offer &amp; start","Oferta e incorporación"),
 "Een passend aanbod en een warm welkom in het team.":
   ("A suitable offer and a warm welcome to the team.","Una oferta a tu medida y una cálida bienvenida al equipo."),
 "Vastgoed met hoofd &eacute;n hart. We groeien en zoeken mensen die het verschil maken — in Utrecht, Amsterdam, Valencia en Estepona.":
   ("Real estate with both head and heart. We're growing and looking for people who make the difference — in Utrecht, Amsterdam, Valencia and Estepona.",
    "Inmobiliaria con cabeza y corazón. Crecemos y buscamos personas que marquen la diferencia — en Utrecht, Ámsterdam, Valencia y Estepona."),
 "Bij Spring werk je in kleine, slagvaardige teams met korte lijnen en veel eigen verantwoordelijkheid. Je krijgt de ruimte om te ondernemen, ondersteund door de beste data en tools in de markt.":
   ("At Spring you work in small, decisive teams with short lines and plenty of personal responsibility. You get room to take initiative, backed by the best data and tools in the market.",
    "En Spring trabajas en equipos pequeños y resolutivos, con comunicación directa y mucha responsabilidad propia. Tienes margen para emprender, con los mejores datos y herramientas del mercado."),
 "Of je nu start of al jaren ervaring hebt: je groeit mee met een groep die commercieel &eacute;n residentieel vastgoed onder &eacute;&eacute;n dak brengt, in Nederland en Spanje.":
   ("Whether you're just starting out or have years of experience: you grow with a group that brings commercial and residential real estate under one roof, in the Netherlands and Spain.",
    "Tanto si empiezas como si tienes años de experiencia: creces con un grupo que reúne inmuebles comerciales y residenciales bajo un mismo techo, en los Países Bajos y España."),
 # sectoren / cases leads
 "Een brede vastgoedgroep — commercieel &eacute;n residentieel. We kennen de dynamiek van elke markt waarin u actief bent.":
   ("A broad real estate group — commercial and residential. We know the dynamics of every market you operate in.",
    "Un grupo inmobiliario amplio — comercial y residencial. Conocemos la dinámica de cada mercado en el que operas."),
 "Echte projecten, echte resultaten. Filter op sector of doelgroep en ontdek hoe we waarde cre&euml;ren.":
   ("Real projects, real results. Filter by sector or audience and discover how we create value.",
    "Proyectos reales, resultados reales. Filtra por sector o público y descubre cómo creamos valor."),
}

_LOC_TAGS = "h1|h2|h3|h4|h5|span|p|a|small|b|li"
def localize(html):
    """Injecteer EN/ES-vertalingen in elk element waarvan de inhoud exact een NL-sleutel is."""
    for nl, (en, es) in UI_TR.items():
        attrs = trh(en, es)
        if not attrs:
            continue
        pat = re.compile(r'(<(' + _LOC_TAGS + r')((?:\s[^>]*)?)>)' + re.escape(nl) + r'(</\2>)')
        def repl(m, nl=nl, attrs=attrs):
            tag, rest, close = m.group(2), m.group(3), m.group(4)
            if 'data-tr' in rest or 'data-i18n' in rest:
                return m.group(0)
            return f'<{tag}{rest}{attrs}>{nl}{close}'
        html = pat.sub(repl, html)
    return html

def tlabel(nl):
    """los tekstlabel met inline NL/EN/ES (voor tekst die localize niet vangt, bv. sector-chips)."""
    en, es = UI_TR.get(nl, ("", ""))
    return f'<span{trh(en, es)}>{nl}</span>'

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

# pitch-portretten (e-mail -> fotopad) + parse van betrokken personen
try:
    FACES = json.load(open(os.path.join(ROOT, "build", "faces.json"), encoding="utf-8"))
except Exception:
    FACES = {}
_EMAIL_RE = re.compile(r'[a-z]+\.[a-z]+@springrealestate\.com')
def parse_person(pp):
    """ 'Naam — Rol — email' -> (naam, rol, email, fotopad|None) """
    m = _EMAIL_RE.search(pp)
    email = m.group(0) if m else ""
    rest = pp.replace(email, "") if email else pp
    parts = [x.strip(" -–—·|") for x in re.split(r'[—–·|]', rest) if x.strip(" -–—·|")]
    name = parts[0] if parts else "Spring-adviseur"
    role = parts[1] if len(parts) > 1 else "Spring Real Estate"
    return name, role, email, FACES.get(email)
# unieke teamleden over alle units (voor de teampagina)
PEOPLE = []
_seen = set()
for _num in sorted(_raw):
    for _pp in (_raw[_num].get("people") or []):
        nm, role, email, photo = parse_person(_pp)
        key = email or nm
        if key in _seen:
            continue
        _seen.add(key)
        if email:
            pslug = email.split("@")[0].lower()
        else:
            pslug = re.sub(r'&[a-z]+;', '', nm).lower()
            pslug = re.sub(r'[^a-z0-9]+', '-', pslug).strip('-') or "medewerker"
        PEOPLE.append({"name": nm, "role": role, "email": email, "photo": photo, "slug": pslug})

# ----------------------------------------------------------------------
# DATA MODEL
# ----------------------------------------------------------------------
DOELGROEPEN = {
    "gebruiker":   {"num":"01","name":"Gebruiker","name_en":"User","name_es":"Usuario",
        "q":"Ik zoek een kantoor of werkplek","q_en":"I'm looking for an office or workspace","q_es":"Busco una oficina o espacio de trabajo",
        "intro":"Op zoek naar de juiste werkomgeving? Spring vindt, onderhandelt en richt in — van een eigen kantoor tot een flexibele werkplek.",
        "intro_en":"Looking for the right work environment? Spring finds, negotiates and fits out — from your own office to a flexible workspace.",
        "intro_es":"¿Buscas el entorno de trabajo adecuado? Spring busca, negocia y acondiciona — desde tu propia oficina hasta un espacio flexible."},
    "eigenaar":    {"num":"02","name":"Eigenaar","name_en":"Owner","name_es":"Propietario",
        "q":"Ik wil mijn vastgoed verkopen of verhuren","q_en":"I want to sell or lease my property","q_es":"Quiero vender o alquilar mi inmueble",
        "intro":"Haal maximaal rendement uit uw object met scherpe marketing, het juiste netwerk en betrouwbare taxaties.",
        "intro_en":"Get the maximum return from your property with sharp marketing, the right network and reliable valuations.",
        "intro_es":"Obtén el máximo rendimiento de tu inmueble con un marketing afinado, la red adecuada y tasaciones fiables."},
    "investeerder":{"num":"03","name":"Investeerder","name_en":"Investor","name_es":"Inversor",
        "q":"Ik wil investeren in vastgoed","q_en":"I want to invest in real estate","q_es":"Quiero invertir en inmuebles",
        "intro":"Van acquisitie tot beheer: datagedreven advies over de volledige levenscyclus van uw belegging.",
        "intro_en":"From acquisition to management: data-driven advice across the full lifecycle of your investment.",
        "intro_es":"De la adquisición a la gestión: asesoramiento basado en datos durante todo el ciclo de vida de tu inversión."},
    "ontwikkelaar":{"num":"04","name":"Ontwikkelaar","name_en":"Developer","name_es":"Promotor",
        "q":"Ik wil vastgoed ontwikkelen of optimaliseren","q_en":"I want to develop or optimise real estate","q_es":"Quiero desarrollar u optimizar inmuebles",
        "intro":"Van acquisitie en concept tot oplevering en verhuur — met data en taxaties als kompas.",
        "intro_en":"From acquisition and concept to delivery and leasing — with data and valuations as your compass.",
        "intro_es":"De la adquisición y el concepto a la entrega y el alquiler — con datos y tasaciones como brújula."},
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
<link rel="stylesheet" href="css/styles.css?v=10">
<link rel="icon" type="image/png" href="images/favicon.png?v=10">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png?v=10">
<meta name="theme-color" content="#7CA73F">
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
  <a href="index.html" class="logo" aria-label="Spring Real Estate"><img src="images/logo-ink.png" alt="Spring Real Estate" class="logo-img"></a>
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
      <div class="logo logo--light"><img src="images/logo-white.png" alt="Spring Real Estate" class="logo-img"></div>
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
      <li><a href="begrippen.html">Begrippen</a></li>
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
  <div class="mm-head"><div class="logo logo--light"><img src="images/logo-white.png" alt="Spring Real Estate" class="logo-img"></div><button class="mm-close" id="mmClose">&times;</button></div>
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

<script src="js/main.js?v=10"></script>
<script src="js/i18n.js?v=10"></script>
</body>
</html>
"""

def li_checks(items):
    return "".join(f'<li>{ic(I_CHECK,"2.4")} {x}</li>' for x in items)

# ----------------------------------------------------------------------
# DOELGROEP HUB PAGE
# ----------------------------------------------------------------------
# tuples: (nl_titel, nl_tekst, en_titel, en_tekst, es_titel, es_tekst)
DG_WHY = {
 "gebruiker":[("Snel de juiste ruimte","We kennen de markt op straatniveau en koppelen uw eisen aan het beste beschikbare aanbod.",
               "The right space, fast","We know the market at street level and match your requirements to the best available supply.",
               "El espacio adecuado, rápido","Conocemos el mercado a pie de calle y conectamos tus necesidades con la mejor oferta disponible."),
              ("Onderhandeld op uw voorwaarden","Scherpe huurprijs, incentives en flexibele voorwaarden — wij behartigen uw belang.",
               "Negotiated on your terms","Sharp rent, incentives and flexible terms — we represent your interest.",
               "Negociado en tus términos","Alquiler ajustado, incentivos y condiciones flexibles — defendemos tu interés."),
              ("Instapklaar opgeleverd","Van zoektocht tot inrichting: één partner regelt het hele traject.",
               "Move-in ready","From search to fit-out: one partner handles the entire process.",
               "Listo para entrar","De la búsqueda al acondicionamiento: un solo socio gestiona todo el proceso.")],
 "eigenaar":[("Maximaal rendement","Datagedreven waardebepaling en een scherpe positionering van uw object.",
              "Maximum return","Data-driven valuation and sharp positioning of your property.",
              "Máxima rentabilidad","Valoración basada en datos y un posicionamiento afinado de tu inmueble."),
             ("Actieve salesaanpak","Wij benaderen kopers en huurders direct en creëren beweging in de markt.",
              "Active sales approach","We approach buyers and tenants directly and create movement in the market.",
              "Enfoque de ventas activo","Contactamos directamente con compradores e inquilinos y generamos movimiento en el mercado."),
             ("Betrouwbare taxaties","Onafhankelijke, gevalideerde taxaties volgens de hoogste normen.",
              "Reliable valuations","Independent, validated valuations to the highest standards.",
              "Tasaciones fiables","Tasaciones independientes y validadas según los más altos estándares.")],
 "investeerder":[("De hele levenscyclus","Van acquisitie en beheer tot exit — strategisch advies in elke fase.",
                  "The full lifecycle","From acquisition and management to exit — strategic advice at every stage.",
                  "Todo el ciclo de vida","De la adquisición y la gestión a la salida — asesoramiento estratégico en cada fase."),
                 ("Onderbouwd met data","Actuele markt- en transactiedata als fundament onder elke beslissing.",
                  "Backed by data","Current market and transaction data as the foundation of every decision.",
                  "Respaldado por datos","Datos actuales de mercado y transacciones como base de cada decisión."),
                 ("Volledig ontzorgd","Asset management, beheer en administratie onder één dak.",
                  "Fully taken care of","Asset management, property management and administration under one roof.",
                  "Totalmente despreocupado","Asset management, gestión y administración bajo un mismo techo.")],
 "ontwikkelaar":[("Van acquisitie tot oplevering","Begeleiding over de volledige ontwikkeling, met data en taxaties als kompas.",
                  "From acquisition to delivery","Guidance across the entire development, with data and valuations as your compass.",
                  "De la adquisición a la entrega","Acompañamiento en todo el desarrollo, con datos y tasaciones como brújula."),
                 ("Haalbaarheid vooraf","We toetsen locatie, bestemming en markt voordat u zich vastlegt.",
                  "Feasibility upfront","We assess location, zoning and market before you commit.",
                  "Viabilidad por adelantado","Evaluamos ubicación, calificación y mercado antes de que te comprometas."),
                 ("Marktinzicht als kompas","Research en advies die uw plan onderbouwen en versterken.",
                  "Market insight as compass","Research and advice that substantiate and strengthen your plan.",
                  "El análisis de mercado como brújula","Investigación y asesoramiento que fundamentan y refuerzan tu plan.")],
}
# tuples: (nl, en, es)
DG_QUOTE = {
 "gebruiker":("De grootste fout bij het zoeken naar ruimte is alleen naar de huurprijs kijken. Wij kijken naar groei, flexibiliteit en uw totale huisvestingsstrategie.",
   "The biggest mistake when looking for space is to look only at the rent. We look at growth, flexibility and your total accommodation strategy.",
   "El mayor error al buscar espacio es fijarse solo en el alquiler. Nosotros miramos el crecimiento, la flexibilidad y tu estrategia de espacio en conjunto."),
 "eigenaar":("Een succesvol verhuur- of verkooptraject draait om de juiste prijs én een actieve benadering van de markt. Daar sturen we op.",
   "A successful lease or sale comes down to the right price and an active approach to the market. That's what we steer on.",
   "Un alquiler o una venta con éxito dependen del precio adecuado y de un enfoque activo del mercado. En eso nos centramos."),
 "investeerder":("Rendement begint bij de juiste data en een scherpe strategie — en wordt geborgd door goed beheer.",
   "Returns start with the right data and a sharp strategy — and are secured by good management.",
   "La rentabilidad empieza con los datos correctos y una estrategia afinada — y se asegura con una buena gestión."),
 "ontwikkelaar":("Een goede ontwikkeling begint bij de juiste acquisitie en een onderbouwd plan. Wij denken vanaf dag één mee.",
   "A good development starts with the right acquisition and a well-founded plan. We think along from day one.",
   "Un buen desarrollo empieza con la adquisición adecuada y un plan bien fundamentado. Pensamos contigo desde el primer día."),
}
def render_doelgroep(key):
    d = DOELGROEPEN[key]
    units = units_for(key)
    cards = ""
    for j,(slug,name,_dg,tag,exp,sec) in enumerate(units):
        img = PHOTOS[j % 3]
        cards += f'''<a class="kat-card" href="unit-{slug}.html"><img src="{img}" alt=""><span class="ktag">{d['name']}</span><span class="kbody"><h3>{name}</h3><p>{tag}</p></span><span class="karr"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">{I_ARR}</svg></span></a>'''
    why_cards = "".join(f'<div class="value"><div class="ic">{ic(I_CHECK,"2.4")}</div><h3{trh(ent, est)}>{t}</h3><p{trh(enx, esx)}>{x}</p></div>' for t,x,ent,enx,est,esx in DG_WHY[key])
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
    <div class="crumbs"><a href="index.html">Home</a> / <span{trh("Services","Servicios")}>Diensten</span> / <span{trh(d['name_en'], d['name_es'])}>{d['name']}</span></div>
    <span class="eyebrow"{trh(f"Audience {d['num']}", f"Público {d['num']}")}>Doelgroep {d['num']}</span>
    <h1{trh(f"{d['name_en']} — <em style=\"color:var(--green);font-style:italic;font-weight:500\">{d['q_en']}</em>", f"{d['name_es']} — <em style=\"color:var(--green);font-style:italic;font-weight:500\">{d['q_es']}</em>")}>{d['name']} — <em style="color:var(--green);font-style:italic;font-weight:500">{d['q'].lower()}</em></h1>
    <p class="lead"{trh(d['intro_en'], d['intro_es'])}>{d['intro']}</p>
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
    <span class="eyebrow"{trh(f"For the {d['name_en'].lower()}", f"Para el {d['name_es'].lower()}")}>Voor de {d['name'].lower()}</span>
    <h2 class="disp"{trh(f"{d['q_en']}? <em>We'll help you</em>", f"{d['q_es']}? <em>Te ayudamos</em>")}>{d['q']}? <em>Wij helpen u verder</em></h2>
    <p{trh(d['intro_en'], d['intro_es'])}>{d['intro']}</p>
    <p{trh("Whether it's a single question or a complex process: you get one point of contact with the whole Spring ecosystem behind it — commercial and residential, in the Netherlands and Spain.", "Ya sea una sola pregunta o un proceso complejo: tienes un único punto de contacto con todo el ecosistema de Spring detrás — comercial y residencial, en los Países Bajos y España.")}>Of het nu om één vraag gaat of om een complex traject: u krijgt één aanspreekpunt met het hele Spring-ecosysteem erachter — commercieel én residentieel, in Nederland en Spanje.</p>
    <a href="#diensten" class="btn btn--primary" style="margin-top:6px"{trh("View the services","Ver los servicios")}>Bekijk de diensten</a>
  </div>
  <div class="media-tall"><img src="images/photo-1.jpg" alt="{d['name']}"></div>
</div></div></section>

<section class="section--tight section--soft"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow"{trh("Why Spring","Por qué Spring")}>Waarom Spring</span><h2 class="disp"{trh(f"Why the {d['name_en'].lower()} chooses <em>Spring</em>", f"Por qué el {d['name_es'].lower()} elige <em>Spring</em>")}>Waarom de {d['name'].lower()} voor <em>Spring</em> kiest</h2></div></div>
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
    <p class="disp disp--light" style="font-size:clamp(1.5rem,3vw,2.3rem);line-height:1.3"{trh(f'<em>"{DG_QUOTE[key][1]}"</em>', f'<em>"{DG_QUOTE[key][2]}"</em>')}><em>"{DG_QUOTE[key][0]}"</em></p>
    <p class="muted" style="margin-top:16px">— Spring Real Estate</p>
  </div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Sectoren</span><h2 class="disp">Expertise in <em>elke sector</em></h2><p class="lead">Van kantoren en logistiek tot retail, zorg en residentieel vastgoed.</p></div><a href="sectoren.html" class="btn btn--ghost">Alle sectoren</a></div>
  <div class="units-grid">
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>{tlabel("Kantoren")}</a>
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>{tlabel("Logistiek &amp; bedrijfsruimte")}</a>
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>{tlabel("Retail &amp; winkels")}</a>
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>{tlabel("Zorgvastgoed")}</a>
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>{tlabel("Residentieel")}</a>
    <a class="unit" href="sectoren.html"><span class="u-dot"></span>{tlabel("Hospitality")}</a>
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
    sectors = "".join(f'<div class="sector">{ic(I_CHECK,"2.4")} {tlabel(s)}</div>' for s in sec)
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
            nm, role, mail, photo = parse_person(pp)
            mlink = f"mailto:{mail}" if mail else "#"
            tc.append(f'<div class="agent"><div class="ph">{phinner(nm,photo)}</div><div class="body"><div class="name">{he(nm)}</div><div class="role">{he(role)}</div><div class="socials"><a href="#" aria-label="LinkedIn">in</a><a href="{mlink}" aria-label="E-mail">@</a></div></div></div>')
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
    def _agent(nm, role, photo=None):
        return (f'<div class="agent"><div class="ph">{phinner(nm, photo)}</div><div class="body">'
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
          + _agent("Sofia Mart&iacute;n", "Investment Advisor · Valencia")
          + _agent("Carlos Ferrer", "Asset Manager · Estepona")
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
    <div class="sec-head"><div class="t"><span class="eyebrow">Diensten &amp; expertises</span><h2 class="disp"{trh(f"What we do in <em>{title_low}</em>", f"Qué hacemos en <em>{title_low}</em>")}>Wat wij doen binnen <em>{title_low}</em></h2></div></div>
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
  <div class="sec-head"><div class="t"><span class="eyebrow">Veelgestelde vragen</span><h2 class="disp"{trh(f"FAQ about <em>{title_low}</em>", f"Preguntas sobre <em>{title_low}</em>")}>FAQ over <em>{title_low}</em></h2></div></div>
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
    <a class="post" href="resources.html"><div class="ph"><img src="{ph}" alt=""></div><div class="body"><span class="cat">Kennisartikel</span><h3{trh(f"Trends in {name.lower()} for 2026", f"Tendencias en {name.lower()} para 2026")}>Trends in {name.lower()} voor 2026</h3><span class="date">12 juni 2026 · 5 min</span></div></a>
    <a class="post" href="resources.html"><div class="ph"><img src="{ph2}" alt=""></div><div class="body"><span class="cat">Marktinzicht</span><h3>Zo bepaalt u de juiste strategie</h3><span class="date">3 juni 2026 · 6 min</span></div></a>
    <a class="post" href="resources.html"><div class="ph"><img src="{PHOTOS[(idx+2)%3]}" alt=""></div><div class="body"><span class="cat">Begrippen</span><h3>Belangrijke termen uitgelegd</h3><span class="date">28 mei 2026 · 4 min</span></div></a>
  </div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="logos-cap"{trh("Trusted by clients &amp; partners","La confianza de clientes y socios")}>Vertrouwd door opdrachtgevers &amp; partners</div>
  <div class="logos-row">
    <span class="clogo">MERIN</span><span class="clogo">a.s.r.&nbsp;<small>real estate</small></span><span class="clogo">BPD</span><span class="clogo">Vesteda</span><span class="clogo">Heimstaden</span><span class="clogo">Bouwinvest</span>
  </div>
</div></section>

<section class="section--tight section--soft"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow"{trh("Glossary","Glosario")}>Begrippenlijst</span><h2 class="disp"{trh("Jargon <em>explained</em>","Jerga <em>explicada</em>")}>Vakjargon <em>uitgelegd</em></h2><p class="lead"{trh(f"The key terms around {title_low}, in plain language.", f"Los términos clave sobre {title_low}, en lenguaje claro.")}>De belangrijkste begrippen rondom {title_low}, in begrijpelijke taal.</p></div></div>
  <div class="glossary">
    <div class="gloss"><b>k.k. — kosten koper</b><p>De koper betaalt de kosten voor de overdracht, zoals overdrachtsbelasting en notaris.</p></div>
    <div class="gloss"><b>BVO / VVO</b><p>Bruto vloeroppervlak versus verhuurbaar vloeroppervlak — bepalend voor huurprijs en vergelijkbaarheid.</p></div>
    <div class="gloss"><b>Aanvangsrendement</b><p>De verhouding tussen de jaarlijkse huurinkomsten en de aankoopprijs van een beleggingsobject.</p></div>
    <div class="gloss"><b>BREEAM</b><p>Internationaal keurmerk dat de duurzaamheidsprestatie van een gebouw beoordeelt.</p></div>
    <div class="gloss"><b>Triple net (NNN)</b><p>Huurvorm waarbij de huurder naast de huur ook belastingen, verzekering en onderhoud betaalt.</p></div>
    <div class="gloss"><b>Due diligence</b><p>Het grondige onderzoek naar een object vóór aankoop: juridisch, technisch en financieel.</p></div>
  </div>
</div></section>

{office_html}
{spain_html}
<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Gerelateerde diensten</span><h2 class="disp">Ook <em>interessant</em></h2></div><a href="{dglink}" class="btn btn--ghost">Alle diensten</a></div>
  <div class="units-grid">{related_html}</div>
</div></section>

<section class="section--tight" id="contact"><div class="container"><div class="cta">
  <h2{trh(f"Questions about {name.lower()}?", f"¿Preguntas sobre {name.lower()}?")}>Vragen over {name.lower()}?</h2>
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
 ("Senior Real Estate Advisor","Amsterdam · Zuidas","Fulltime","Acquisitie & advies",
  "Als Senior Real Estate Advisor begeleid je gebruikers en eigenaren bij huur-, koop- en verkooptransacties van commercieel vastgoed in de regio Amsterdam. Je bouwt langdurige relaties op en bent het gezicht van Spring richting opdrachtgevers.",
  ["Begeleiden van huur- en verkooptransacties van A tot Z","Onderhandelen over voorwaarden namens opdrachtgevers","Opbouwen en onderhouden van een eigen netwerk","Adviseren over huisvestings- en vastgoedstrategie"],
  ["Minimaal 5 jaar ervaring in commercieel vastgoed","Sterk netwerk in de regio Amsterdam","Commercieel, ondernemend en resultaatgericht","Uitstekende beheersing van Nederlands en Engels"],
  ["Marktconform salaris met een aantrekkelijke bonusregeling","Auto van de zaak en mobiliteitsregeling","Veel autonomie en korte lijnen","Doorgroei binnen een snelgroeiende vastgoedgroep"]),
 ("Investment Analyst","Utrecht","Fulltime","Investments",
  "Als Investment Analyst onderbouw je beleggingsbeslissingen met data en analyses. Je werkt aan acquisities, taxatie-onderbouwing en portefeuilleoptimalisatie voor onze investeerders.",
  ["Uitvoeren van markt-, locatie- en rendementsanalyses","Opstellen van investeringsmemoranda en cashflowmodellen","Ondersteunen bij acquisitie- en verkooptrajecten","Bijhouden van markt- en transactiedata"],
  ["Afgeronde opleiding in finance, economie of vastgoedkunde","Sterk met Excel en data; affiniteit met vastgoed","Analytisch, nauwkeurig en cijfermatig","0–4 jaar ervaring; ook starters welkom"],
  ["Een steile leercurve binnen een ervaren team","Ruim opleidingsbudget en begeleiding","Hybride werken vanuit Utrecht","Marktconform salaris en bonus"]),
 ("Vastgoedmarketeer","Utrecht","32–40 uur","Marketing",
  "Als Vastgoedmarketeer zet je objecten en business units sterk in de markt. Je maakt campagnes, content en presentaties die opvallen en converteren — met data als kompas.",
  ["Ontwikkelen van object- en merkcampagnes","Beheren van website, social en nieuwsbrieven","Coördineren van fotografie, video en copy","Meten en optimaliseren op basis van data"],
  ["Ervaring met (vastgoed)marketing of een mediabureau","Sterk in content, beeld en tone-of-voice","Zelfstandig, creatief en datagedreven","Goede beheersing van Nederlands en Engels"],
  ["Veel vrijheid om je eigen plan te maken","Werken aan een sterk groeiend merk","Hybride werken, 32–40 uur","Marktconform salaris en goede secundaire voorwaarden"]),
 ("Taxateur RT","Amsterdam","Fulltime","Taxaties",
  "Als Taxateur RT stel je onafhankelijke, gevalideerde taxaties op van beleggings- en bedrijfsvastgoed. Je werkt voor eigenaren, investeerders en financiers en bewaakt de kwaliteit volgens de hoogste normen.",
  ["Taxeren van beleggings- en bedrijfsvastgoed","Opstellen van gevalideerde taxatierapporten","Onderbouwen van waardes met markt- en transactiedata","Contact met opdrachtgevers en validerende instanties"],
  ["RT-registratie (of vergevorderd in het traject)","Ervaring met commercieel vastgoed taxeren","Zorgvuldig, onafhankelijk en onderbouwd","Kennis van NRVT-richtlijnen"],
  ["Werken met een modern, datagedreven taxatieplatform","Ruimte voor permanente educatie","Marktconform salaris en bonus","Een hecht en ervaren taxatieteam"]),
 ("Asociado Comercial","Valencia (ES)","Fulltime","España",
  "Vanuit ons kantoor in Valencia begeleid je Nederlandse investeerders en gebruikers op de Spaanse vastgoedmarkt. Je bent de lokale schakel met een Nederlands aanspreekpunt.",
  ["Begeleiden van acquisities en huisvesting in Spanje","Onderhouden van lokale contacten en aanbod","Schakelen tussen NL-opdrachtgevers en de Spaanse markt","Ondersteunen bij due diligence en onderhandeling"],
  ["Vloeiend Spaans én Engels; Nederlands is een pré","Kennis van de Spaanse vastgoedmarkt","Commercieel en cultureel sensitief","Woonachtig in (de regio) Valencia"],
  ["Werken in een internationaal team","Een unieke NL–ES brugfunctie","Marktconform Spaans salaris met bonus","Doorgroei in een groeiende internationale tak"]),
 ("Property Manager","Utrecht","Fulltime","Vastgoedbeheer",
  "Als Property Manager beheer je een portefeuille commercieel vastgoed: technisch, commercieel en administratief. Je zorgt voor tevreden huurders en optimaal renderende objecten.",
  ["Beheren van een eigen vastgoedportefeuille","Aansturen van onderhoud en leveranciers","Contact met huurders en eigenaren","Bewaken van budgetten en rapportages"],
  ["Ervaring in commercieel vastgoedbeheer","Servicegericht, georganiseerd en proactief","Kennis van huurrecht en servicekosten","Goede beheersing van Nederlands en Engels"],
  ["Een afwisselende beheerportefeuille","Marktconform salaris en mobiliteitsregeling","Hybride werken vanuit Utrecht","Een professioneel beheerteam"]),
 ("Stage: Vastgoeddata & onderzoek","Utrecht","Stage","Data",
  "Tijdens je stage bij Spring werk je mee aan markt- en transactiedata die onze adviezen onderbouwen. Je leert het vak van datagedreven vastgoedadvies van binnenuit.",
  ["Verzamelen en verrijken van markt- en transactiedata","Maken van analyses, dashboards en marktrapporten","Meedraaien met het research- en investmentteam","Bijdragen aan kennisartikelen en marktinzichten"],
  ["HBO/WO-student vastgoed, economie of data","Handig met Excel; affiniteit met data","Leergierig, nauwkeurig en zelfstandig","Beschikbaar voor een meewerkstage"],
  ["Een leerzame stage met echte verantwoordelijkheid","Stagevergoeding en begeleiding","Kans op een vaste baan na je studie","Een jong en gedreven team"]),
]
def vac_slug(title):
    s = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    return s or "vacature"

def _vmeta(loc, typ, team):
    return (f'<div class="vmeta">'
            f'<span><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="10" r="3"/><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/></svg> {loc}</span>'
            f'<span><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg> {typ}</span>'
            f'<span><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{I_BLD}</svg> {team}</span></div>')

def render_vacature_detail(v):
    t,loc,typ,team,intro,taken,eisen,bieden = v
    slug = vac_slug(t)
    taken_li = "".join(f"<li>{ic(I_CHECK,'2.4')} {x}</li>" for x in taken)
    eisen_li = "".join(f"<li>{ic(I_CHECK,'2.4')} {x}</li>" for x in eisen)
    bieden_li = "".join(f"<li>{ic(I_CHECK,'2.4')} {x}</li>" for x in bieden)
    subj = t.replace(' ', '%20')
    html = HEAD.format(title=f"{he(t)} — Vacature — Spring Real Estate", desc=f"Vacature {he(t)} bij Spring Real Estate — {loc}, {typ}. Solliciteer direct.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero"><div class="container">
  <div class="crumbs"><a href="index.html">Home</a> / <a href="vacatures.html" data-i18n="nav.vacatures">Vacatures</a> / {he(t)}</div>
  <span class="eyebrow" data-i18n="nav.vacatures">Vacatures</span>
  <h1>{he(t)}</h1>
  {_vmeta(loc, typ, team)}
  <div class="ph-cta" style="margin-top:22px"><a href="contact.html" class="btn btn--primary">Solliciteer op deze functie</a><a href="mailto:jobs@springrealestate.com?subject=Sollicitatie%20{subj}" class="btn btn--ghost">Mail je cv</a></div>
</div></section>

<section class="section"><div class="container"><div class="split">
  <div>
    <p class="lead">{intro}</p>
    <h3 style="margin-top:26px">Wat ga je doen?</h3><ul class="checks">{taken_li}</ul>
    <h3 style="margin-top:22px">Wat vragen we?</h3><ul class="checks">{eisen_li}</ul>
    <h3 style="margin-top:22px">Wat bieden we?</h3><ul class="checks">{bieden_li}</ul>
  </div>
  <div class="aside-card aside-dark">
    <h3>Interesse in deze functie?</h3>
    <p style="color:#bcbeb2;font-size:.94rem">Solliciteer direct of stuur je cv — we reageren doorgaans binnen 5 werkdagen.</p>
    <a href="contact.html" class="btn btn--primary" style="width:100%;margin-top:8px">Solliciteer</a>
    <a href="mailto:jobs@springrealestate.com?subject=Sollicitatie%20{subj}" class="btn btn--ghost" style="width:100%;margin-top:10px;color:#fff;border-color:rgba(255,255,255,.3)">Mail je cv</a>
    <div class="dlist" style="margin-top:18px">
      <div class="di"><span class="di-k">Locatie</span><span class="di-v">{loc}</span></div>
      <div class="di"><span class="di-k">Dienstverband</span><span class="di-v">{typ}</span></div>
      <div class="di"><span class="di-k">Team</span><span class="di-v">{team}</span></div>
    </div>
  </div>
</div></div></section>

<section class="section--tight"><div class="container"><div class="cta">
  <h2>Niet helemaal jouw functie?</h2>
  <p>Bekijk alle vacatures of stuur ons een open sollicitatie — we maken graag kennis.</p>
  <div class="btns"><a href="vacatures.html" class="btn btn--light btn--lg">Alle vacatures</a><a href="contact.html" class="btn btn--lg" style="background:rgba(255,255,255,.16);color:#fff;border-color:rgba(255,255,255,.4)">Open sollicitatie</a></div>
</div></div></section>
'''
    html += FOOTER
    return html

def render_vacatures():
    rows = ""
    for v in VACS:
        t,loc,typ,team,intro,taken,eisen,bieden = v
        rows += f'''<a class="vac" href="vacature-{vac_slug(t)}.html">
          <div><h3>{t}</h3>{_vmeta(loc, typ, team)}</div>
          <span class="vac-cta"><span data-tr="1" data-en="View vacancy" data-es="Ver vacante">Bekijk vacature</span> <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
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
      <h2 class="disp"{trh(f"About <em>{name.split(' ')[0]}</em>", f"Sobre <em>{name.split(' ')[0]}</em>")}>Over <em>{name.split(' ')[0]}</em></h2>
      <p>{name} is {role.split('·')[0].strip().lower()} bij Spring Real Estate in {loc.split('·')[0].strip()}, met {years} ervaring. {name.split(' ')[0]} is gespecialiseerd in {spec.lower()} en werkt datagedreven samen met klanten aan de beste oplossing.</p>
      <ul class="pf-facts">
        <li><span{trh("Years of experience","Años de experiencia")}>Jaren ervaring</span><b>{years}</b></li>
        <li><span{trh("Specialism","Especialidad")}>Specialisme</span><b>{spec}</b></li>
        <li><span{trh("Office","Oficina")}>Kantoor</span><b>{loc.split('·')[0].strip()}</b></li>
        <li><span{trh("Education","Formación")}>Opleiding</span><b>MSc Real Estate</b></li>
        <li><span{trh("Accreditations","Acreditaciones")}>Lidmaatschappen / accreditaties</span><b>RICS · NRVT</b></li>
        <li><span{trh("Languages","Idiomas")}>Talen</span><b>NL · EN · ES</b></li>
      </ul>
      <a href="contact.html" class="btn btn--primary" style="margin-top:6px">Plan een afspraak</a>
    </div>
  </div>
</div></section>

<section class="section--tight section--soft"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow"{trh("Personal market vision","Visión de mercado")}>Persoonlijke marktvisie</span><h2 class="disp"{trh(f"The vision of <em>{name.split(' ')[0]}</em>", f"La visión de <em>{name.split(' ')[0]}</em>")}>De visie van <em>{name.split(' ')[0]}</em></h2></div></div>
  <p class="disp" style="font-size:clamp(1.3rem,2.4vw,1.9rem);line-height:1.4;max-width:60ch"><em>"De beste resultaten ontstaan waar marktkennis en persoonlijk contact samenkomen. Ik denk met u mee over de lange termijn — niet alleen over de transactie van vandaag."</em></p>
</div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Specialisme</span><h2 class="disp"{trh(f"Who {name.split(' ')[0]} <em>serves</em>", f"A quién atiende <em>{name.split(' ')[0]}</em>")}>Wie {name.split(' ')[0]} <em>bedient</em></h2></div></div>
  <div class="sector-grid">{sect}</div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow"{trh("Reviews","Reseñas")}>Reviews</span><h2 class="disp"{trh(f"What clients say about <em>{name.split(' ')[0]}</em>", f"Lo que dicen los clientes de <em>{name.split(' ')[0]}</em>")}>Wat klanten over <em>{name.split(' ')[0]}</em> zeggen</h2></div></div>
  <div class="cards-grid">
    <div class="rev-card"><div class="stars">★★★★★</div><p>"{name.split(' ')[0]} kent de markt door en door en regelde meer dan we vroegen. Snelle, transparante begeleiding van begin tot eind."</p><b>Klantnaam, Organisatie</b></div>
    <div class="rev-card"><div class="stars">★★★★★</div><p>"Datagedreven advies en een scherpe onderhandeling. We zaten binnen de afgesproken termijn in het juiste pand."</p><b>Klantnaam, Organisatie</b></div>
    <div class="rev-card"><div class="stars">★★★★★</div><p>"Een vertrouwde adviseur die met ons meedenkt over de lange termijn, niet alleen de transactie van vandaag."</p><b>Klantnaam, Organisatie</b></div>
  </div>
</div></section>

<section class="section--tight section--soft"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow"{trh("References","Referencias")}>Referenties</span><h2 class="disp"{trh("Recent <em>clients</em>","<em>Clientes</em> recientes")}>Recente <em>opdrachtgevers</em></h2></div></div>
  <div class="logos-row">
    <span class="clogo">MERIN</span><span class="clogo">a.s.r.&nbsp;<small>real estate</small></span><span class="clogo">BPD</span><span class="clogo">Vesteda</span><span class="clogo">Bouwinvest</span>
  </div>
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
# TEAMLID-PROFIEL (eigen pagina per medewerker uit PEOPLE)
# ----------------------------------------------------------------------
def render_person_profile(p):
    name, role, email, photo, slug = p["name"], p["role"], p["email"], p.get("photo"), p["slug"]
    first = name.split(" ")[0] if name.split(" ")[0][:1].isupper() else (name.split(" ")[1] if len(name.split(" "))>1 else name)
    mail = email or "info@springrealestate.com"
    media = f'<img src="{photo}" alt="{esc(name)}">' if photo else f'<div class="ph" style="aspect-ratio:4/5">{phinner(name, None)}</div>'
    sectors = ["Kantoren","Logistiek &amp; bedrijfsruimte","Retail","Zorgvastgoed"]
    sect = "".join(f'<div class="sector">{ic(I_CHECK,"2.4")} {tlabel(s)}</div>' for s in sectors)
    html = HEAD.format(title=f"{he(name)} — Spring Real Estate", desc=f"{he(name)}, {he(role)} bij Spring Real Estate.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero"><div class="container">
  <div class="crumbs"><a href="index.html">Home</a> / <a href="agents.html">Agents</a> / {he(name)}</div>
  <span class="eyebrow" data-tr="1" data-en="Our team" data-es="Nuestro equipo">Ons team</span>
  <h1>{he(name)}</h1>
  <p class="lead">{he(role)}</p>
  <div class="ph-cta">
    <a href="mailto:{mail}" class="btn btn--primary">E-mail {he(first)}</a>
    <a href="tel:+31302001020" class="btn btn--ghost">+31 30 200 10 20</a>
    <a href="#" class="btn btn--ghost">LinkedIn</a>
  </div>
</div></section>

<section class="section"><div class="container"><div class="two-col">
  <div class="media-tall">{media}</div>
  <div class="prose">
    <span class="eyebrow" data-tr="1" data-en="Professional experience" data-es="Experiencia profesional">Professional experience</span>
    <h2 class="disp"{trh(f"About <em>{he(first)}</em>", f"Sobre <em>{he(first)}</em>")}>Over <em>{he(first)}</em></h2>
    <p>{he(name)} is {he(role.lower())} bij Spring Real Estate en werkt datagedreven samen met klanten aan de beste vastgoedoplossing. [Bio in te vullen — 2&ndash;4 zinnen met jaartal, regio en specialisme.]</p>
    <ul class="pf-facts">
      <li><span{trh("Role","Función")}>Functie</span><b>{he(role)}</b></li>
      <li><span{trh("Years of experience","Años de experiencia")}>Jaren ervaring</span><b>10+ jaar</b></li>
      <li><span{trh("Office","Oficina")}>Kantoor</span><b>Amsterdam · Utrecht</b></li>
      <li><span{trh("Education","Formación")}>Opleiding</span><b>MSc Real Estate</b></li>
      <li><span{trh("Accreditations","Acreditaciones")}>Lidmaatschappen / accreditaties</span><b>RICS · NRVT</b></li>
      <li><span{trh("Languages","Idiomas")}>Talen</span><b>NL · EN · ES</b></li>
    </ul>
    <a href="mailto:{mail}" class="btn btn--primary" style="margin-top:6px">Plan een afspraak</a>
  </div>
</div></div></section>

<section class="section--tight section--soft"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow"{trh("Personal market vision","Visión de mercado")}>Persoonlijke marktvisie</span><h2 class="disp"{trh(f"The vision of <em>{he(first)}</em>", f"La visión de <em>{he(first)}</em>")}>De visie van <em>{he(first)}</em></h2></div></div>
  <p class="disp" style="font-size:clamp(1.3rem,2.4vw,1.9rem);line-height:1.4;max-width:60ch"><em>"[Persoonlijke marktvisie in te vullen — 2&ndash;3 zinnen die de expertise van {he(first)} tonen.]"</em></p>
</div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Specialisme</span><h2 class="disp"{trh(f"Who {he(first)} <em>serves</em>", f"A quién atiende <em>{he(first)}</em>")}>Wie {he(first)} <em>bedient</em></h2></div></div>
  <div class="sector-grid">{sect}</div>
</div></section>

<section class="section--tight section--soft"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow"{trh("Reviews","Reseñas")}>Reviews</span><h2 class="disp"{trh(f"What clients say about <em>{he(first)}</em>", f"Lo que dicen los clientes de <em>{he(first)}</em>")}>Wat klanten over <em>{he(first)}</em> zeggen</h2></div></div>
  <div class="cards-grid">
    <div class="rev-card"><div class="stars">★★★★★</div><p>"[Review in te vullen — benoem de dienst, regio en een concreet resultaat.]"</p><b>Klantnaam, Organisatie</b></div>
    <div class="rev-card"><div class="stars">★★★★★</div><p>"[Review in te vullen — met toestemming van de klant.]"</p><b>Klantnaam, Organisatie</b></div>
    <div class="rev-card"><div class="stars">★★★★★</div><p>"[Review in te vullen.]"</p><b>Klantnaam, Organisatie</b></div>
  </div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow"{trh("References","Referencias")}>Referenties</span><h2 class="disp"{trh("Recent <em>clients</em>","<em>Clientes</em> recientes")}>Recente <em>opdrachtgevers</em></h2></div></div>
  <div class="logos-row">
    <span class="clogo">MERIN</span><span class="clogo">a.s.r.&nbsp;<small>real estate</small></span><span class="clogo">BPD</span><span class="clogo">Vesteda</span><span class="clogo">Bouwinvest</span>
  </div>
</div></section>

<section class="section--tight section--soft"><div class="container">
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
# OBJECT-DETAILPAGINA (eigen pagina per object, Funda-stijl)
# ----------------------------------------------------------------------
LOC_LATLNG = {"amsterdam":"52.339,4.872","utrecht":"52.0894,5.110","valencia":"39.4667,-0.3667","estepona":"36.4275,-5.1459"}
DESC = {
 "kantoor":"Representatieve kantoorruimte op een uitstekend bereikbare locatie. De ruimte is efficiënt indeelbaar, beschikt over veel lichtinval en hoogwaardige voorzieningen, en is geschikt voor uiteenlopende kantoorconcepten.",
 "bedrijf":"Functionele bedrijfs- en logistieke ruimte met goede bereikbaarheid en moderne specificaties. Geschikt voor opslag, productie en last-mile distributie, met ruime vrije hoogte en laad-/losmogelijkheden.",
 "winkel":"Winkelruimte op een sterke, goed bezochte locatie met hoge passantenstromen. Representatieve pui en een indeling die zich leent voor diverse retail- en horecaformules.",
 "belegging":"Beleggingsobject met een stabiele kasstroom en een aantrekkelijk bruto aanvangsrendement. Een solide toevoeging aan een vastgoedportefeuille, op een courante locatie met goede verhuurbaarheid.",
}
def render_listing_detail(d):
    offer, typ = d["offer"], d["type"]
    pl, pe, pes = d["ptype"]; a_nl, a_en, a_es = d["area_label"]; s_nl, s_en, s_es = d["spec3"]
    pool = ["photo-1.jpg", "photo-2.jpg", "hero.jpg"]
    thumbs = [p for p in pool if p != d["img"]][:2] + [d["img"]]
    tagtxt = ("Te huur", "For rent", "En alquiler") if offer == "huur" else ("Te koop", "For sale", "En venta")
    eyebrow = f'{pl} {tagtxt[0].lower()}'
    spec_rows = [("Prijs", d["price"]), ("Type", pl), (a_nl.split()[0] if a_nl[0].isdigit() else "Oppervlakte", a_nl), ("Beschikbaarheid", s_nl if offer=="huur" else "In overleg")]
    if offer == "koop":
        spec_rows = [("Vraagprijs", d["price"]), ("Type", pl), ("Oppervlakte", a_nl), ("Bruto aanvangsrendement", s_nl), ("Beschikbaarheid", "In overleg")]
    else:
        spec_rows = [("Huurprijs", d["price"]), ("Type", pl), ("Oppervlakte", a_nl), ("Beschikbaarheid", s_nl), ("Opleveringsniveau", "Turn-key / in overleg")]
    rows = "".join(f'<div class="spec-row"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in spec_rows)
    adv = PEOPLE[0]
    similar = [x for x in LISTINGS if x["offer"] == offer and x["slug"] != d["slug"]][:3]
    simcards = "".join(
        f'<a class="prop-card" href="aanbod-{x["slug"]}.html"><div class="ph"><span class="tag tag--{x["offer"]}">{("Te huur" if x["offer"]=="huur" else "Te koop")}</span><img src="images/{x["img"]}" alt=""></div>'
        f'<div class="body"><span class="ptype">{x["ptype"][0]}</span><h3>{x["title"]}</h3><span class="addr">{x["addr"]}</span><div class="meta"><span class="price">{x["price"]}</span></div></div></a>'
        for x in similar)
    subj = d["title"].replace(" ", "%20")
    price_plain = re.sub(r'<[^>]+>', '', d["price"])
    html = HEAD.format(title=f'{he(d["title"])} — {pl} {tagtxt[0].lower()} — Spring Real Estate',
                       desc=f'{pl} {tagtxt[0].lower()} in {he(d["addr"])}. {a_nl}, {price_plain}. Bekijk dit object bij Spring Real Estate.')
    html += TOPBAR + HEADER
    html += f'''
<div class="detail-top"><div class="container">
  <a href="listings.html" class="back"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M11 18l-6-6 6-6"/></svg> <span data-tr="1" data-en="Back to listings" data-es="Volver a inmuebles">Terug naar aanbod</span></a>
</div></div>
<div class="container"><div class="detail-wrap">
  <div class="detail-main">
    <div class="gallery">
      <div class="g-main"><span class="g-badge tag--{offer}" data-tr="1" data-en="{tagtxt[1]}" data-es="{tagtxt[2]}">{tagtxt[0]}</span><img src="images/{thumbs[2]}" alt="{esc(d["title"])}"><span class="g-allfotos"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg> {d["photos"]} foto's</span></div>
      <div class="g-side"><div class="g-thumb"><img src="images/{thumbs[0]}" alt=""></div><div class="g-thumb"><img src="images/{thumbs[1]}" alt=""></div><div class="g-thumb"><img src="images/{thumbs[2]}" alt=""></div></div>
    </div>
    <div class="d-titlebar">
      <div>
        <span class="d-eyebrow">{eyebrow}</span>
        <h1>{he(d["title"])}</h1>
        <div class="d-addr">{he(d["addr"])}</div>
        <div class="d-meta"><span>{ic(I_CHECK,"2")} {pl}</span><span>{ic(I_CHECK,"2")} {a_nl}</span><span>{ic(I_CHECK,"2")} {s_nl}</span></div>
      </div>
      <div class="d-price"><div class="pp">{d["price"]}</div><div class="sub">{"Excl. BTW en servicekosten" if offer=="huur" else "Kosten koper"}</div><div class="area">{a_nl}</div></div>
    </div>
    <div class="d-actions">
      <a href="contact.html" class="btn btn--primary btn--lg">Plan bezichtiging</a>
      <a href="mailto:info@springrealestate.com?subject=Brochure%20{subj}" class="btn btn--ghost btn--lg">Download brochure</a>
    </div>
    <div class="d-section"><h2>Over dit object</h2><p class="muted">{DESC.get(typ, DESC["kantoor"])}</p></div>
    <div class="d-section"><h2>Specificaties</h2><div class="spec-grid"><div>{rows}</div><div class="spec-extra"><div id="detail-map" data-loc="{d["loc"]}" data-title="{esc(d["title"])}" data-price="{esc(d["price"])}" data-offer="{offer}"></div></div></div></div>
  </div>
  <aside class="detail-side">
    <div class="side-card" id="aanvraag">
      <h3>Interesse in dit object?</h3>
      <p class="sc-sub">Laat je gegevens achter — onze adviseur neemt snel contact met je op.</p>
      <form onsubmit="return false">
        <div class="form-field"><input type="text" placeholder="Naam *" data-i18n-ph="form.firstname"></div>
        <div class="form-field"><input type="email" placeholder="E-mailadres *" data-i18n-ph="form.email"></div>
        <div class="form-field"><input type="tel" placeholder="Telefoon" data-i18n-ph="form.phone"></div>
        <button class="btn btn--primary" style="width:100%">Verstuur aanvraag</button>
      </form>
    </div>
    <div class="side-card">
      <h3 style="margin-bottom:14px">Uw adviseur</h3>
      <div class="advisor">{phinner(adv["name"], adv.get("photo"))}<div><b>{he(adv["name"])}</b><span>{he(adv["role"])}</span></div></div>
      <div class="advisor-contact">
        <a href="tel:+31302001020"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg> +31 30 200 10 20</a>
        <a href="mailto:{adv["email"] or "info@springrealestate.com"}"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg> {adv["email"] or "info@springrealestate.com"}</a>
      </div>
      <a href="profile-{adv["slug"]}.html" class="btn btn--ghost" style="width:100%;margin-top:6px">Bekijk profiel</a>
    </div>
  </aside>
</div></div>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Vergelijkbaar aanbod</span><h2 class="disp">Ook <em>interessant</em></h2></div><a href="listings.html" class="btn btn--ghost">Heel het aanbod</a></div>
  <div class="cards-grid">{simcards}</div>
</div></section>
'''
    html += FOOTER
    return html

# ----------------------------------------------------------------------
# LOCATION PAGES (eigen pagina per kantoor)
# ----------------------------------------------------------------------
LOCATIES = {
 "utrecht":   {"name":"Utrecht","flag":"\U0001F1F3\U0001F1F1","tag":"Hoofdkantoor","tag_en":"Headquarters","tag_es":"Sede central","addr":"Stadhouderskade 12 · 3531 BJ Utrecht","count":"8",
   "intro":"Vanuit ons hoofdkantoor in Utrecht bedienen we heel Nederland. Centraal gelegen en uitstekend bereikbaar — de thuisbasis van onze taxatie-, asset management- en marketingteams.",
   "intro_en":"From our headquarters in Utrecht we serve the whole of the Netherlands. Centrally located and easily accessible — the home base of our valuation, asset management and marketing teams.",
   "intro_es":"Desde nuestra sede central en Utrecht damos servicio a todos los Países Bajos. Céntrica y muy accesible — la base de nuestros equipos de tasación, asset management y marketing."},
 "amsterdam": {"name":"Amsterdam","flag":"\U0001F1F3\U0001F1F1","tag":"Zuidas","tag_en":"Zuidas","tag_es":"Zuidas","addr":"Gustav Mahlerlaan 2999 · 1082 MK Amsterdam","count":"12",
   "intro":"Op de Zuidas, in het zakelijke hart van Nederland, zit ons team voor kantoorhuisvesting, serviced offices en investments — dicht bij onze opdrachtgevers.",
   "intro_en":"On the Zuidas, in the business heart of the Netherlands, sits our team for office space, serviced offices and investments — close to our clients.",
   "intro_es":"En la Zuidas, el corazón empresarial de los Países Bajos, está nuestro equipo de oficinas, serviced offices e inversiones — cerca de nuestros clientes."},
 "valencia":  {"name":"Valencia","flag":"\U0001F1EA\U0001F1F8","tag":"España","tag_en":"Spain","tag_es":"España","addr":"Paseo de la Alameda 7 · 46023 Valencia","count":"7",
   "intro":"Onze vaste basis in Spanje. Vanuit Valencia begeleiden we Nederlandse investeerders en gebruikers bij acquisities en huisvesting op de Spaanse markt.",
   "intro_en":"Our permanent base in Spain. From Valencia we guide Dutch investors and users with acquisitions and accommodation in the Spanish market.",
   "intro_es":"Nuestra base permanente en España. Desde Valencia acompañamos a inversores y usuarios neerlandeses en adquisiciones y alojamiento en el mercado español."},
 "estepona":  {"name":"Estepona","flag":"\U0001F1EA\U0001F1F8","tag":"España · Costa del Sol","tag_en":"Spain · Costa del Sol","tag_es":"España · Costa del Sol","addr":"Avenida Litoral 12 · 29680 Estepona","count":"6",
   "intro":"Aan de Costa del Sol begeleiden we vanuit Estepona investeringen en huisvesting in Zuid-Spanje — van residentieel tot commercieel vastgoed, met lokale kennis en een Nederlands aanspreekpunt.",
   "intro_en":"On the Costa del Sol, from Estepona, we guide investments and accommodation in southern Spain — from residential to commercial real estate, with local knowledge and a Dutch point of contact.",
   "intro_es":"En la Costa del Sol, desde Estepona, acompañamos inversiones y alojamiento en el sur de España — de lo residencial a lo comercial, con conocimiento local y un punto de contacto neerlandés."},
}
def render_locatie(key):
    L = LOCATIES[key]
    team3 = "".join(
        f'<div class="agent" data-profile="profile-{pp["slug"]}.html"><div class="ph">{phinner(pp["name"], pp["photo"])}</div><div class="body"><a class="name" href="profile-{pp["slug"]}.html">{he(pp["name"])}</a><div class="role">{he(pp["role"])}</div><div class="socials"><a href="profile-{pp["slug"]}.html">in</a><a href="mailto:{pp["email"] or "info@springrealestate.com"}">@</a></div></div></div>'
        for pp in PEOPLE[:3])
    html = HEAD.format(title=f"{L['name']} — Spring Real Estate", desc=f"Spring Real Estate {L['name']}: {L['addr']}. Aanbod, team en contact in {L['name']}.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / <a href="locaties.html">Locaties</a> / {L['name']}</div>
    <span class="eyebrow">{L['flag']} <span{trh(L['tag_en'], L['tag_es'])}>{L['tag']}</span></span>
    <h1>Spring in <em style="color:var(--green);font-style:italic;font-weight:500">{L['name']}</em></h1>
    <p class="lead">{L['addr']}</p>
    <div class="ph-cta"><a href="listings.html" class="btn btn--primary"{trh(f"Listings in {L['name']}", f"Inmuebles en {L['name']}")}>Aanbod in {L['name']}</a><a href="contact.html" class="btn btn--ghost">Route &amp; contact</a></div>
  </div>
</section>

<section class="section"><div class="container"><div class="two-col">
  <div class="prose"><span class="eyebrow">Over deze locatie</span><h2 class="disp"{trh(f"Locally strong in <em>{L['name']}</em>", f"Fuertes a nivel local en <em>{L['name']}</em>")}>Lokaal sterk in <em>{L['name']}</em></h2><p{trh(L['intro_en'], L['intro_es'])}>{L['intro']}</p>
    <div class="stat-pop" style="display:flex;gap:34px;margin-top:18px"><div><b style="font-size:1.9rem;font-weight:800;display:block;color:var(--green)">{L['count']}</b><span class="muted"{trh("properties available","inmuebles disponibles")}>objecten beschikbaar</span></div><div><b style="font-size:1.9rem;font-weight:800;display:block;color:var(--green)">15+</b><span class="muted"{trh("years in the region","años en la región")}>jaar in de regio</span></div></div>
  </div>
  <div class="loc-map" style="aspect-ratio:4/3;border-radius:var(--r-lg);overflow:hidden;position:relative;background:linear-gradient(135deg,#e9efe0,#dfe7d2);border:1px solid var(--line)">
    <svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" style="position:absolute;inset:0;width:100%;height:100%"><rect width="400" height="300" fill="#e6ecdb"/><path d="M0 170 Q120 150 240 175 T400 160" stroke="#c7d3ad" stroke-width="2" fill="none"/><path d="M90 0 L110 300" stroke="#d3ddbf" stroke-width="2"/></svg>
    <span class="pin2" style="position:absolute;left:50%;top:46%;transform:translate(-50%,-100%)"><span class="dot" style="display:block;width:30px;height:30px;border-radius:50% 50% 50% 0;background:var(--green);transform:rotate(-45deg);border:3px solid #fff;box-shadow:0 6px 14px -4px rgba(0,0,0,.4)"></span></span>
  </div>
</div></div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Kantoorimpressie</span><h2 class="disp"{trh(f"Our office in <em>{L['name']}</em>", f"Nuestra oficina en <em>{L['name']}</em>")}>Zo ziet ons kantoor in <em>{L['name']}</em> eruit</h2></div></div>
  <div class="cards-grid">
    <div style="border-radius:var(--r);overflow:hidden;aspect-ratio:4/3"><img src="images/photo-1.jpg" alt="Kantoor {L['name']}" style="width:100%;height:100%;object-fit:cover"></div>
    <div style="border-radius:var(--r);overflow:hidden;aspect-ratio:4/3"><img src="images/photo-2.jpg" alt="Kantoor {L['name']}" style="width:100%;height:100%;object-fit:cover"></div>
    <div style="border-radius:var(--r);overflow:hidden;aspect-ratio:4/3"><img src="images/hero.jpg" alt="Kantoor {L['name']}" style="width:100%;height:100%;object-fit:cover"></div>
  </div>
</div></section>

<section class="section dark-sec"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow" style="color:var(--green-soft)"{trh(f"The team in {L['name']}", f"El equipo en {L['name']}")}>Het team in {L['name']}</span><h2 class="disp" style="color:#fff">Uw <em>aanspreekpunt</em></h2></div><a href="agents.html" class="btn btn--secondary">Heel het team</a></div>
  <div class="team-grid">{team3}</div>
</div></section>

<section class="section--tight"><div class="container">
  <div class="sec-head"><div class="t"><span class="eyebrow">Aanbod</span><h2 class="disp"{trh(f"Available in <em>{L['name']}</em>", f"Disponible en <em>{L['name']}</em>")}>Beschikbaar in <em>{L['name']}</em></h2></div><a href="listings.html" class="btn btn--ghost">Bekijk alles</a></div>
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
# BEGRIPPEN / KENNISBANK (eigen begrippenpagina — doorzoekbaar)
# ----------------------------------------------------------------------
GLOSSARY = [
 ("k.k. — kosten koper","De koper betaalt de kosten voor de overdracht, zoals overdrachtsbelasting en notariskosten."),
 ("v.o.n. — vrij op naam","De verkoper betaalt de overdrachtskosten; de prijs is inclusief deze kosten."),
 ("BVO / VVO","Bruto vloeroppervlak versus verhuurbaar vloeroppervlak — bepalend voor huurprijs en vergelijkbaarheid van objecten."),
 ("Bruto aanvangsrendement (BAR)","De verhouding tussen de bruto jaarhuur en de totale aankoopprijs van een beleggingsobject, uitgedrukt in procenten."),
 ("Netto aanvangsrendement (NAR)","Het rendement na aftrek van de exploitatiekosten — een zuiverder beeld van het werkelijke rendement."),
 ("Triple net (NNN)","Huurvorm waarbij de huurder naast de huur ook de belastingen, verzekering en het onderhoud betaalt."),
 ("BREEAM","Internationaal keurmerk dat de duurzaamheidsprestatie van een gebouw beoordeelt — van Pass tot Outstanding."),
 ("Energielabel","Wettelijke score (A t/m G) voor de energiezuinigheid van een gebouw; kantoren vereisen minimaal label C."),
 ("Due diligence","Het grondige onderzoek naar een object vóór aankoop: juridisch, technisch, fiscaal en commercieel."),
 ("Leegstandsrisico","Het risico dat (een deel van) een object niet verhuurd is en dus geen huurinkomsten oplevert."),
 ("WALT","Weighted Average Lease Term — de gewogen gemiddelde resterende looptijd van de huurcontracten in een object."),
 ("Servicekosten","Vergoeding voor gemeenschappelijke voorzieningen en diensten, naast de kale huur."),
 ("Incentives","Tijdelijke voordelen om een huurder te bewegen, zoals huurvrije periodes of een inrichtingsbijdrage."),
 ("Erfpacht","Het recht om grond van een ander (vaak de gemeente) langdurig te gebruiken tegen een jaarlijkse canon."),
]
def render_begrippen():
    cards = "".join(f'<div class="gloss"><b>{he(t)}</b><p>{he(u)}</p></div>' for t, u in GLOSSARY)
    html = HEAD.format(title="Begrippenlijst — Spring Real Estate", desc="Begrippenlijst commercieel vastgoed: k.k., v.o.n., BAR, NAR, BREEAM, WALT, erfpacht en meer — helder uitgelegd door Spring Real Estate.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero"><div class="container">
  <div class="crumbs"><a href="index.html">Home</a> / Begrippen</div>
  <span class="eyebrow"{trh("Glossary","Glosario")}>Begrippenlijst</span>
  <h1{trh("Vastgoedjargon, <em style=\"color:var(--green);font-style:italic;font-weight:500\">helder uitgelegd</em>", "Jerga inmobiliaria, <em style=\"color:var(--green);font-style:italic;font-weight:500\">explicada con claridad</em>")}>Vastgoedjargon, <em style="color:var(--green);font-style:italic;font-weight:500">helder uitgelegd</em></h1>
  <p class="lead"{trh("The most important terms in commercial real estate, in plain language — searchable.", "Los términos más importantes del sector inmobiliario comercial, en lenguaje claro — con búsqueda.")}>De belangrijkste begrippen in commercieel vastgoed, in begrijpelijke taal — doorzoekbaar.</p>
</div></section>
<section class="section filterable"><div class="container">
  <div class="list-search"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg><input type="text" placeholder="Zoek een begrip…" data-i18n-ph="search.term" aria-label="Zoek een begrip"></div>
  <div class="glossary">{cards}</div>
  <p class="filter-empty" style="display:none;color:var(--ink-soft);padding:20px 0">Geen begrip gevonden.</p>
</div></section>
<section class="section--tight"><div class="container"><div class="cta">
  <h2{trh("A term you don't see?","¿Falta algún término?")}>Een begrip dat u mist?</h2>
  <p{trh("Ask our specialists — we're happy to explain.","Pregunta a nuestros especialistas — te lo explicamos con gusto.")}>Vraag het onze specialisten — we leggen het graag uit.</p>
  <div class="btns"><a href="contact.html" class="btn btn--light btn--lg">Neem contact op</a></div>
</div></div></section>
'''
    html += FOOTER
    return html

# ----------------------------------------------------------------------
# AGENTS / TEAM PAGE (echte mensen + foto's uit de pitch)
# ----------------------------------------------------------------------
def agent_cat(role):
    r = role.lower()
    if "valuation" in r or "taxat" in r: return "valuations"
    if "asset management" in r or "investor" in r or "investment" in r: return "investments"
    if "property management" in r or "property manager" in r or "beheer" in r: return "management"
    if "research" in r: return "research"
    if any(k in r for k in ("accounting","financial","operations","people advisor","controller")): return "support"
    return "agency"

def render_agents():
    cards = ""
    for i, p in enumerate(PEOPLE):
        first = p["name"].split(" ")[0]
        mlink = f'mailto:{p["email"]}' if p["email"] else "#"
        cards += (f'<div class="person" data-cat="{agent_cat(p["role"])}" data-profile="profile-{p["slug"]}.html"><div class="ph">{phinner(p["name"], p["photo"])}</div>'
                  f'<div class="body"><a class="name" href="profile-{p["slug"]}.html">{he(p["name"])}</a><div class="role">{he(p["role"])}</div>'
                  f'<p class="bio" data-tr="1" data-en="{he(first)} is a specialist at Spring Real Estate. Feel free to get in touch for an introduction and personal advice." data-es="{he(first)} es especialista en Spring Real Estate. No dudes en ponerte en contacto para una presentaci&oacute;n y asesoramiento personal.">{he(first)} is specialist bij Spring Real Estate. Neem gerust contact op voor een kennismaking en persoonlijk advies.</p>'
                  f'<div class="socials"><a href="#" aria-label="LinkedIn"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.8-2 3.7-2 4 0 4.75 2.6 4.75 6V21H21v-5.3c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9V21H13z"/></svg></a>'
                  f'<a href="{mlink}" aria-label="E-mail"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></a></div></div></div>')
    html = HEAD.format(title="Ons team — Spring Real Estate", desc="Maak kennis met het team van Spring Real Estate in Amsterdam, Utrecht, Valencia en Estepona.")
    html += TOPBAR + HEADER
    html += f'''
<section class="page-hero"><div class="container">
  <div class="crumbs"><a href="index.html">Home</a> / Agents</div>
  <span class="eyebrow" data-tr="1" data-en="Our team" data-es="Nuestro equipo">Ons team</span>
  <h1 data-tr="1" data-en="The people behind <em style=&quot;color:var(--green);font-style:italic;font-weight:500&quot;>Spring</em>" data-es="Las personas detr&aacute;s de <em style=&quot;color:var(--green);font-style:italic;font-weight:500&quot;>Spring</em>">De mensen achter <em style="color:var(--green);font-style:italic;font-weight:500">Spring</em></h1>
  <p class="lead" data-tr="1" data-en="{len(PEOPLE)} specialists who know your market &mdash; click a colleague for more on their expertise and contact details." data-es="{len(PEOPLE)} especialistas que conocen tu mercado &mdash; haz clic en un compa&ntilde;ero para ver su experiencia y contacto.">{len(PEOPLE)} specialisten die uw markt kennen &mdash; klik op een collega voor meer over diens expertise en contact.</p>
</div></section>

<section class="section filterable"><div class="container">
  <div class="list-search"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg><input type="text" placeholder="Zoek een medewerker op naam of functie…" data-i18n-ph="search.people" aria-label="Zoek een medewerker"></div>
  <div class="team-filter">
    <a href="#" class="active" data-key="alle" data-tr="1" data-en="All" data-es="Todos">Alle</a><a href="#" data-key="agency">Agency</a><a href="#" data-key="valuations">Valuations</a><a href="#" data-key="investments">Investments</a><a href="#" data-key="management">Management</a><a href="#" data-key="research">Research</a><a href="#" data-key="support">Support</a>
  </div>
  <div class="people-grid">{cards}</div>
  <p class="filter-empty" style="display:none;color:var(--ink-soft);padding:20px 0" data-tr="1" data-en="No colleagues found. <a href=&quot;#&quot; class=&quot;link-arrow&quot; data-key=&quot;alle&quot; style=&quot;display:inline&quot;>Show all</a>" data-es="No se encontraron compa&ntilde;eros. <a href=&quot;#&quot; class=&quot;link-arrow&quot; data-key=&quot;alle&quot; style=&quot;display:inline&quot;>Mostrar todos</a>">Geen medewerkers gevonden. <a href="#" class="link-arrow" data-key="alle" style="display:inline">Toon alle</a></p>
</div></section>

<section class="section--tight"><div class="container"><div class="cta">
  <h2 data-tr="1" data-en="Work at Spring?" data-es="&iquest;Trabajar en Spring?">Werken bij Spring?</h2>
  <p data-tr="1" data-en="We're growing &mdash; and looking for people who approach real estate with both head and heart." data-es="Estamos creciendo &mdash; y buscamos personas que aborden el sector inmobiliario con cabeza y coraz&oacute;n.">We groeien &mdash; en zoeken mensen die vastgoed met hoofd &eacute;n hart benaderen.</p>
  <div class="btns"><a href="vacatures.html" class="btn btn--light btn--lg" data-tr="1" data-en="View vacancies" data-es="Ver vacantes">Bekijk vacatures</a></div>
</div></div></section>
'''
    html += FOOTER
    return html

# ----------------------------------------------------------------------
# WRITE
# ----------------------------------------------------------------------
def write(name, html):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(localize(html))
    return name

def main():
    written = []
    for key in DOELGROEPEN:
        written.append(write(f"doelgroep-{key}.html", render_doelgroep(key)))
    for i,u in enumerate(UNITS):
        written.append(write(f"unit-{u[0]}.html", render_unit(i,u)))
    written.append(write("vacatures.html", render_vacatures()))
    written.append(write("agents.html", render_agents()))
    for p in PEOPLE:
        written.append(write(f"profile-{p['slug']}.html", render_person_profile(p)))
    for v in VACS:
        written.append(write(f"vacature-{vac_slug(v[0])}.html", render_vacature_detail(v)))
    for d in LISTINGS:
        written.append(write(f"aanbod-{d['slug']}.html", render_listing_detail(d)))
    for key in LOCATIES:
        written.append(write(f"locatie-{key}.html", render_locatie(key)))
    written.append(write("sectoren.html", render_sectoren()))
    written.append(write("cases.html", render_cases()))
    written.append(write("begrippen.html", render_begrippen()))
    print(f"Generated {len(written)} pages:")
    for w in written: print("  "+w)

if __name__ == "__main__":
    main()
