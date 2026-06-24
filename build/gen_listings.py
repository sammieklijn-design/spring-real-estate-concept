# -*- coding: utf-8 -*-
"""Funda-/sollf-stijl aanbod: rijke kaarten, verhuur + verkoop/belegging, kenmerken."""
import re, os, sys
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from listings_data import LISTINGS

# legacy tuple list kept for reference (no longer used for rendering)
_LEGACY = [
 # ---------- VERHUUR (sollf-stijl: kantoren, serviced, bedrijfs-/winkelruimte) ----------
 ("Gustav Mahlerlaan 2999","1082 MK Amsterdam · Zuidas","amsterdam","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€720 <small>/m²/jaar</small>",720,1250,("vanaf 1.250 m²","from 1,250 m²","desde 1.250 m²"),("Direct beschikbaar","Available now","Disponible ya"),18,"photo-1.jpg","direct"),
 ("Claude Debussylaan 24","1082 MD Amsterdam · Zuidas","amsterdam","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€395 <small>/m²/jaar</small>",395,480,("vanaf 480 m²","from 480 m²","desde 480 m²"),("Direct beschikbaar","Available now","Disponible ya"),12,"photo-2.jpg","direct"),
 ("Mahler Tower · 14e etage","1082 MA Amsterdam · Zuidas","amsterdam","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€510 <small>/m²/jaar</small>",510,720,("vanaf 720 m²","from 720 m²","desde 720 m²"),("Per Q3 2026","From Q3 2026","Desde Q3 2026"),20,"hero.jpg","overleg"),
 ("WTC Amsterdam · Tower C","1077 XX Amsterdam · Zuidas","amsterdam","kantoor",("Serviced office","Serviced office","Oficina serviced"),"huur","€1.250 <small>/werkplek/mnd</small>",1250,120,("8–40 werkplekken","8–40 workspaces","8–40 puestos"),("Flexibel contract","Flexible term","Contrato flexible"),24,"photo-2.jpg","direct"),
 ("Gustav Mahlerplein 109","1082 MS Amsterdam · Zuidas","amsterdam","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€465 <small>/m²/jaar</small>",465,350,("vanaf 350 m²","from 350 m²","desde 350 m²"),("Direct beschikbaar","Available now","Disponible ya"),10,"photo-1.jpg","direct"),
 ("Strawinskylaan 3051","1077 ZX Amsterdam · Zuidas","amsterdam","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€540 <small>/m²/jaar</small>",540,900,("vanaf 900 m²","from 900 m²","desde 900 m²"),("In overleg","By arrangement","A convenir"),14,"hero.jpg","overleg"),
 ("Stationsplein 8","3511 ED Utrecht · Centrum","utrecht","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€295 <small>/m²/jaar</small>",295,600,("vanaf 600 m²","from 600 m²","desde 600 m²"),("Direct beschikbaar","Available now","Disponible ya"),9,"photo-1.jpg","direct"),
 ("Industrieweg 40","3542 AD Utrecht · Lage Weide","utrecht","bedrijf",("Bedrijfsruimte","Industrial space","Espacio industrial"),"huur","€95 <small>/m²/jaar</small>",95,1800,("vanaf 1.800 m²","from 1,800 m²","desde 1.800 m²"),("Laaddock & 8 m vrije hoogte","Dock & 8 m clear height","Muelle y 8 m de altura"),11,"hero.jpg","overleg"),
 ("Oudegracht 187","3511 NE Utrecht · Centrum","utrecht","winkel",("Winkelruimte","Retail space","Local comercial"),"huur","€350 <small>/m²/jaar</small>",350,180,("180 m²","180 m²","180 m²"),("A1-winkellocatie","A1 retail location","Ubicación retail A1"),8,"photo-2.jpg","direct"),
 ("Paseo de la Alameda 7","46023 Valencia · España","valencia","kantoor",("Serviced office","Serviced office","Oficina serviced"),"huur","€1.450 <small>/werkplek/mnd</small>",1450,200,("12–30 werkplekken","12–30 workspaces","12–30 puestos"),("Flexibel contract","Flexible term","Contrato flexible"),16,"hero.jpg","direct"),
 ("Avenida del Puerto 102","46023 Valencia · España","valencia","bedrijf",("Bedrijfsruimte","Industrial space","Espacio industrial"),"huur","€78 <small>/m²/jaar</small>",78,2400,("vanaf 2.400 m²","from 2,400 m²","desde 2.400 m²"),("Last-mile locatie","Last-mile location","Ubicación last-mile"),10,"photo-2.jpg","overleg"),
 # ---------- VERKOOP / BELEGGING (funda in business-stijl: k.k. + BAR) ----------
 ("Stadhouderskade 12","3531 BJ Utrecht · Centrum","utrecht","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€4,9 mln <small>k.k.</small>",4900000,2100,("2.100 m² v.v.o.","2,100 m² LFA","2.100 m²"),("6,2% BAR","6.2% gross yield","6,2% rent. bruta"),22,"photo-2.jpg","direct"),
 ("Keizersgracht 210","1016 DX Amsterdam · Grachtengordel","amsterdam","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€6,4 mln <small>k.k.</small>",6400000,1850,("1.850 m² v.v.o.","1,850 m² LFA","1.850 m²"),("5,4% BAR","5.4% gross yield","5,4% rent. bruta"),26,"photo-1.jpg","direct"),
 ("Croeselaan 28","3521 CA Utrecht · Beurskwartier","utrecht","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€8,9 mln <small>k.k.</small>",8900000,3400,("3.400 m² v.v.o.","3,400 m² LFA","3.400 m²"),("6,0% BAR","6.0% gross yield","6,0% rent. bruta"),20,"hero.jpg","overleg"),
 ("Carrer de Colón 28","46004 Valencia · España","valencia","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€3,8 mln <small>k.k.</small>",3800000,1450,("1.450 m²","1,450 m²","1.450 m²"),("7,1% BAR","7.1% gross yield","7,1% rent. bruta"),18,"photo-1.jpg","overleg"),
 ("Estepona Marina Plaza","29680 Estepona · Costa del Sol","estepona","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€1,2 mln <small>k.k.</small>",1200000,220,("220 m²","220 m²","220 m²"),("6,8% BAR","6.8% gross yield","6,8% rent. bruta"),14,"hero.jpg","direct"),
]
HEART='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-4.5-9.5-9C1 9 2.5 5.5 6 5.5c2 0 3.2 1.2 4 2.3.8-1.1 2-2.3 4-2.3 3.5 0 5 3.5 3.5 6.5C19 16.5 12 21 12 21z"/></svg>'
IC_AREA='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h7v7H3zM14 14h7v7h-7z"/><path d="M14 3l7 7M10 14l-7 7"/></svg>'
IC_TYPE='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M5 21V8l7-5 7 5v13"/></svg>'
IC_INFO='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/></svg>'
IC_YIELD='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l6-6 4 4 8-8M21 7v6M21 7h-6"/></svg>'
IC_CAM='<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="6" width="18" height="14" rx="2"/><circle cx="12" cy="13" r="3.5"/><path d="M8 6l1.5-2h5L16 6"/></svg>'
def tag(offer):
    return ('<span class="tag tag--huur" data-tr="1" data-en="For rent" data-es="En alquiler">Te huur</span>' if offer=='huur'
            else '<span class="tag tag--koop" data-tr="1" data-en="For sale" data-es="En venta">Te koop</span>')
cards=[]
for d in LISTINGS:
    offer=d["offer"]; pl,pe,pes=d["ptype"]; a_nl,a_en,a_es=d["area_label"]; s_nl,s_en,s_es=d["spec3"]
    s3ic = IC_YIELD if offer=='koop' else IC_INFO
    cards.append(
      '<a class="prop-card flisting" href="aanbod-%s.html" data-offer="%s" data-type="%s" data-loc="%s" data-area="%d" data-price="%d" data-avail="%s">'
      '<div class="ph">%s<span class="fav" aria-label="Bewaar">%s</span><span class="ph-count">%s %d</span><img src="images/%s" alt=""></div>'
      '<div class="body"><div class="fl-price">%s</div>'
      '<h3>%s</h3><span class="addr">%s</span>'
      '<div class="fl-specs">'
      '<span class="fl-spec">%s <span data-tr="1" data-en="%s" data-es="%s">%s</span></span>'
      '<span class="fl-spec">%s <span data-tr="1" data-en="%s" data-es="%s">%s</span></span>'
      '<span class="fl-spec">%s <span data-tr="1" data-en="%s" data-es="%s">%s</span></span>'
      '</div></div></a>'
      % (d["slug"],offer,d["type"],d["loc"],d["area"],d["price_num"],d["avail"], tag(offer),HEART,IC_CAM,d["photos"],d["img"], d["price"], d["title"],d["addr"],
         IC_AREA,a_en,a_es,a_nl, IC_TYPE,pe,pes,pl, s3ic,s_en,s_es,s_nl))
grid='\n        '.join(cards)
co=Counter(d["offer"] for d in LISTINGS); ct=Counter(d["type"] for d in LISTINGS); cl=Counter(d["loc"] for d in LISTINGS)
def opt(group,val,label_nl,en,es,count):
    return ('<label class="fopt"><input type="checkbox" data-fgroup="%s" data-val="%s"> '
            '<span data-tr="1" data-en="%s" data-es="%s">%s</span> <span class="cnt">%d</span></label>'
            % (group,val,en,es,label_nl,count))
filters = ('<aside class="filters" id="filters">\n'
      '      <div style="display:flex;align-items:center;justify-content:space-between">\n'
      '        <h3 data-tr="1" data-en="Filters" data-es="Filtros">Filters</h3>\n'
      '        <a href="#" class="f-clear" id="fClear" data-tr="1" data-en="Clear" data-es="Borrar">Wissen</a>\n'
      '      </div>\n'
      '      <div class="fgroup">\n'
      '        <div class="fg-t" data-tr="1" data-en="Offer type" data-es="Tipo de oferta">Aanbodvorm</div>\n'
      '        %s\n        %s\n'
      '      </div>\n'
      '      <div class="fgroup">\n'
      '        <div class="fg-t" data-tr="1" data-en="Type" data-es="Tipo">Type</div>\n'
      '        %s\n        %s\n        %s\n        %s\n'
      '      </div>\n'
      '      <div class="fgroup">\n'
      '        <div class="fg-t" data-tr="1" data-en="Location" data-es="Ubicación">Locatie</div>\n'
      '        %s\n        %s\n        %s\n        %s\n'
      '      </div>\n'
      '      <div class="fgroup">\n'
      '        <div class="fg-t" data-tr="1" data-en="Floor area (m²)" data-es="Superficie (m²)">Oppervlakte (m²)</div>\n'
      '        <div class="frange"><input type="number" id="fAreaMin" placeholder="min"><input type="number" id="fAreaMax" placeholder="max"></div>\n'
      '      </div>\n'
      '    </aside>'
      % (opt('offer','huur','Te huur','For rent','En alquiler',co['huur']),
         opt('offer','koop','Te koop','For sale','En venta',co['koop']),
         opt('type','kantoor','Kantoorruimte','Office space','Oficina',ct['kantoor']),
         opt('type','bedrijf','Bedrijfsruimte','Industrial space','Espacio industrial',ct['bedrijf']),
         opt('type','winkel','Winkelruimte','Retail space','Local comercial',ct['winkel']),
         opt('type','belegging','Beleggingsobject','Investment property','Inmueble de inversión',ct['belegging']),
         opt('loc','amsterdam','Amsterdam','Amsterdam','Ámsterdam',cl['amsterdam']),
         opt('loc','utrecht','Utrecht','Utrecht','Utrecht',cl['utrecht']),
         opt('loc','valencia','Valencia (ES)','Valencia (ES)','Valencia (ES)',cl['valencia']),
         opt('loc','estepona','Estepona (ES)','Estepona (ES)','Estepona (ES)',cl['estepona'])))
seg = ('<div class="seg-toggle" id="segToggle">\n'
       '        <button class="active" data-seg="all" data-tr="1" data-en="All" data-es="Todo">Alle</button>\n'
       '        <button data-seg="huur" data-tr="1" data-en="For rent" data-es="Alquiler">Verhuur</button>\n'
       '        <button data-seg="koop" data-tr="1" data-en="Sale &amp; investment" data-es="Venta e inversión">Verkoop &amp; belegging</button>\n'
       '      </div>\n      ')
fp=os.path.join(ROOT,'listings.html')
s=open(fp,encoding='utf-8').read()
s=re.sub(r'<aside class="filters" id="filters">.*?</aside>', lambda m: filters, s, count=1, flags=re.S)
s=re.sub(r'(<div class="results-grid">).*?(</div>\s*\n\s*(?:<p class="filter-empty"|<div class="pager">))',
         lambda m: m.group(1)+'\n        '+grid+'\n      '+m.group(2), s, count=1, flags=re.S)
# insert segment toggle once, before the results-head
if 'id="segToggle"' not in s:
    s=s.replace('<div class="results-head">', seg+'<div class="results-head">', 1)
n=len(LISTINGS); nh=co['huur']; nk=co['koop']
s=re.sub(r'Aanbod op de kaart · \d+ objecten','Aanbod op de kaart · %d objecten'%n,s)
s=re.sub(r'data-en="Listings on the map · \d+ properties"','data-en="Listings on the map · %d properties"'%n,s)
s=re.sub(r'data-es="Inmuebles en el mapa · \d+ propiedades"','data-es="Inmuebles en el mapa · %d propiedades"'%n,s)
s=re.sub(r'<b id="rcCount">\d+</b>','<b id="rcCount">%d</b>'%n,s)
open(fp,'w',encoding='utf-8').write(s)
print('listings rebuilt: %d total (%d huur, %d koop)'%(n,nh,nk))
