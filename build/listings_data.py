# -*- coding: utf-8 -*-
"""Gedeelde aanbod-dataset voor de listings-grid, de kaart en de detailpagina's."""
import re

def lslug(title, addr):
    base = (title + "-" + addr.split("·")[0]).lower()
    base = re.sub(r'[^a-z0-9]+', '-', base).strip('-')
    return base[:60] or "object"

# Elk object: zie veldnamen hieronder. ptype/area/spec3 zijn (nl,en,es)-tuples.
_RAW = [
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
 ("Stadhouderskade 12","3531 BJ Utrecht · Centrum","utrecht","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€4,9 mln <small>k.k.</small>",4900000,2100,("2.100 m² v.v.o.","2,100 m² LFA","2.100 m²"),("6,2% BAR","6.2% gross yield","6,2% rent. bruta"),22,"photo-2.jpg","direct"),
 ("Keizersgracht 210","1016 DX Amsterdam · Grachtengordel","amsterdam","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€6,4 mln <small>k.k.</small>",6400000,1850,("1.850 m² v.v.o.","1,850 m² LFA","1.850 m²"),("5,4% BAR","5.4% gross yield","5,4% rent. bruta"),26,"photo-1.jpg","direct"),
 ("Croeselaan 28","3521 CA Utrecht · Beurskwartier","utrecht","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€8,9 mln <small>k.k.</small>",8900000,3400,("3.400 m² v.v.o.","3,400 m² LFA","3.400 m²"),("6,0% BAR","6.0% gross yield","6,0% rent. bruta"),20,"hero.jpg","overleg"),
 ("Carrer de Colón 28","46004 Valencia · España","valencia","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€3,8 mln <small>k.k.</small>",3800000,1450,("1.450 m²","1,450 m²","1.450 m²"),("7,1% BAR","7.1% gross yield","7,1% rent. bruta"),18,"photo-1.jpg","overleg"),
 ("Estepona Marina Plaza","29680 Estepona · Costa del Sol","estepona","belegging",("Beleggingsobject","Investment property","Inmueble de inversión"),"koop","€1,2 mln <small>k.k.</small>",1200000,220,("220 m²","220 m²","220 m²"),("6,8% BAR","6.8% gross yield","6,8% rent. bruta"),14,"hero.jpg","direct"),
]
KEYS = ["title","addr","loc","type","ptype","offer","price","price_num","area","area_label","spec3","photos","img","avail"]
LISTINGS = []
for r in _RAW:
    d = dict(zip(KEYS, r))
    d["slug"] = lslug(d["title"], d["addr"])
    LISTINGS.append(d)
