# -*- coding: utf-8 -*-
import re, os
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = [
 ("Gustav Mahlerlaan 2999","1082 MK Amsterdam · Zuidas","amsterdam","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€720 <small>/m²/jaar</small>",("vanaf 1.250 m²","from 1,250 m²","desde 1.250 m²"),1250,"photo-1.jpg","direct"),
 ("Claude Debussylaan 24","1082 MD Amsterdam · Zuidas","amsterdam","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€395 <small>/m²/jaar</small>",("vanaf 480 m²","from 480 m²","desde 480 m²"),480,"photo-2.jpg","direct"),
 ("Mahler Tower, 14e etage","1082 MA Amsterdam · Zuidas","amsterdam","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€510 <small>/m²/jaar</small>",("vanaf 720 m²","from 720 m²","desde 720 m²"),720,"hero.jpg","overleg"),
 ("WTC Amsterdam · Tower C","1077 XX Amsterdam · Zuidas","amsterdam","kantoor",("Serviced office","Serviced office","Oficina serviced"),"huur","€1.250 <small>/maand</small>",("8 werkplekken","8 workspaces","8 puestos"),120,"photo-2.jpg","direct"),
 ("Gustav Mahlerplein 109","1082 MS Amsterdam · Zuidas","amsterdam","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€465 <small>/m²/jaar</small>",("vanaf 350 m²","from 350 m²","desde 350 m²"),350,"photo-1.jpg","direct"),
 ("Strawinskylaan 3051","1077 ZX Amsterdam · Zuidas","amsterdam","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€540 <small>/m²/jaar</small>",("vanaf 900 m²","from 900 m²","desde 900 m²"),900,"hero.jpg","overleg"),
 ("Stadhouderskade 12","3531 BJ Utrecht · Centrum","utrecht","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€4,9 mln <small>k.k.</small>",("2.100 m²","2,100 m²","2.100 m²"),2100,"photo-2.jpg","direct"),
 ("Stationsplein 8","3511 ED Utrecht · Centrum","utrecht","kantoor",("Kantoorruimte","Office space","Oficina"),"huur","€295 <small>/m²/jaar</small>",("vanaf 600 m²","from 600 m²","desde 600 m²"),600,"photo-1.jpg","direct"),
 ("Industrieweg 40","3542 AD Utrecht · Lage Weide","utrecht","bedrijf",("Bedrijfsruimte","Industrial space","Espacio industrial"),"huur","€95 <small>/m²/jaar</small>",("vanaf 1.800 m²","from 1,800 m²","desde 1.800 m²"),1800,"hero.jpg","overleg"),
 ("Oudegracht 187","3511 NE Utrecht · Centrum","utrecht","winkel",("Winkelruimte","Retail space","Local comercial"),"huur","€350 <small>/m²/jaar</small>",("180 m²","180 m²","180 m²"),180,"photo-2.jpg","direct"),
 ("Paseo de la Alameda 7","46023 Valencia · España","valencia","kantoor",("Serviced office","Serviced office","Oficina serviced"),"huur","€1.450 <small>/maand</small>",("12 werkplekken","12 workspaces","12 puestos"),200,"hero.jpg","direct"),
 ("Carrer de Colón 28","46004 Valencia · España","valencia","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€3,8 mln <small>k.k.</small>",("1.450 m²","1,450 m²","1.450 m²"),1450,"photo-1.jpg","overleg"),
 ("Avenida del Puerto 102","46023 Valencia · España","valencia","bedrijf",("Bedrijfsruimte","Industrial space","Espacio industrial"),"huur","€78 <small>/m²/jaar</small>",("vanaf 2.400 m²","from 2,400 m²","desde 2.400 m²"),2400,"photo-2.jpg","direct"),
 ("Estepona Marina Plaza","29680 Estepona · Costa del Sol","estepona","winkel",("Winkelruimte","Retail space","Local comercial"),"koop","€1,2 mln <small>k.k.</small>",("220 m²","220 m²","220 m²"),220,"hero.jpg","direct"),
]
HEART='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-4.5-9.5-9C1 9 2.5 5.5 6 5.5c2 0 3.2 1.2 4 2.3.8-1.1 2-2.3 4-2.3 3.5 0 5 3.5 3.5 6.5C19 16.5 12 21 12 21z"/></svg>'
def tag(offer):
    return ('<span class="tag" data-tr="1" data-en="For rent" data-es="En alquiler">Te huur</span>' if offer=='huur'
            else '<span class="tag" data-tr="1" data-en="For sale" data-es="En venta">Te koop</span>')
cards=[]
for (t,addr,lk,tk,(pl,pe,pes),offer,price,(s_nl,s_en,s_es),area,img,besch) in P:
    cards.append(
      '<a class="prop-card" href="listing-detail.html" data-offer="%s" data-type="%s" data-loc="%s" data-area="%d" data-avail="%s">'
      '<div class="ph">%s<span class="fav">%s</span><img src="images/%s" alt=""></div>'
      '<div class="body"><span class="ptype" data-tr="1" data-en="%s" data-es="%s">%s</span>'
      '<h3>%s</h3><span class="addr">%s</span>'
      '<div class="meta"><span class="price">%s</span>'
      '<span style="margin-left:auto" data-tr="1" data-en="%s" data-es="%s">%s</span></div></div></a>'
      % (offer,tk,lk,area,besch, tag(offer),HEART,img, pe,pes,pl, t,addr, price, s_en,s_es,s_nl))
grid='\n        '.join(cards)
co=Counter(p[5] for p in P); ct=Counter(p[3] for p in P); cl=Counter(p[2] for p in P)
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
fp=os.path.join(ROOT,'listings.html')
s=open(fp,encoding='utf-8').read()
s=re.sub(r'<aside class="filters" id="filters">.*?</aside>', lambda m: filters, s, count=1, flags=re.S)
s=re.sub(r'(<div class="results-grid">).*?(</div>\s*\n\s*<div class="pager">)',
         lambda m: m.group(1)+'\n        '+grid+'\n      '+m.group(2), s, count=1, flags=re.S)
n=len(P)
s=s.replace('Aanbod op de kaart · 27 objecten','Aanbod op de kaart · %d objecten'%n)
s=s.replace('data-en="Listings on the map · 27 properties"','data-en="Listings on the map · %d properties"'%n)
s=s.replace('data-es="Inmuebles en el mapa · 27 propiedades"','data-es="Inmuebles en el mapa · %d propiedades"'%n)
open(fp,'w',encoding='utf-8').write(s)
print('listings updated; cards:',n)
