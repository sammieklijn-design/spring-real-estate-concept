/* Spring Real Estate — lichte i18n laag (NL / EN / ES)
   Elementen met data-i18n="key" krijgen vertaalde tekst.
   NL is de basistaal (in de HTML geschreven); EN/ES uit de woordenlijst.
   Placeholders via data-i18n-ph. */
window.SPRING_I18N = {
  en: {
    "nav.diensten":"Services","nav.listings":"Listings","nav.about":"About Us","nav.agents":"Agents",
    "nav.resources":"Resources","nav.vacatures":"Careers","nav.contact":"Contact","cta.aanbod":"View listings",
    "dd.gebruiker":"User","dd.gebruiker.d":"I'm looking for office space","dd.eigenaar":"Owner",
    "dd.eigenaar.d":"I want to sell or lease","dd.investeerder":"Investor","dd.investeerder.d":"I want to invest in real estate",
    "dd.ontwikkelaar":"Developer","dd.ontwikkelaar.d":"I want to develop or optimise",
    "search.lblloc":"Location or keyword","search.phloc":"E.g. Amsterdam Zuidas, office…",
    "search.lbltype":"Type","search.lblarea":"Floor area","search.btn":"Search",
    "search.t.huur":"Rent","search.t.koop":"Buy","search.t.invest":"Invest",
    "foot.doelgroepen":"Audiences","foot.navigatie":"Navigation","foot.locaties":"Locations",
    "foot.nieuwsbrief":"Newsletter","foot.nieuwsbrief.p":"Market insights & new listings in your inbox.",
    "foot.inschrijven":"Subscribe","foot.email":"Your email address","foot.tagline":"Powered by People. Backed by Tech. Your partner in commercial real estate in the Netherlands & Spain.",
    "foot.rights":"© 2026 Spring Real Estate. All rights reserved."
  },
  es: {
    "nav.diensten":"Servicios","nav.listings":"Inmuebles","nav.about":"Sobre nosotros","nav.agents":"Equipo",
    "nav.resources":"Recursos","nav.vacatures":"Empleo","nav.contact":"Contacto","cta.aanbod":"Ver inmuebles",
    "dd.gebruiker":"Usuario","dd.gebruiker.d":"Busco espacio de oficina","dd.eigenaar":"Propietario",
    "dd.eigenaar.d":"Quiero vender o alquilar","dd.investeerder":"Inversor","dd.investeerder.d":"Quiero invertir en inmuebles",
    "dd.ontwikkelaar":"Promotor","dd.ontwikkelaar.d":"Quiero desarrollar u optimizar",
    "search.lblloc":"Ubicación o palabra clave","search.phloc":"Ej. Ámsterdam Zuidas, oficina…",
    "search.lbltype":"Tipo","search.lblarea":"Superficie","search.btn":"Buscar",
    "search.t.huur":"Alquilar","search.t.koop":"Comprar","search.t.invest":"Invertir",
    "foot.doelgroepen":"Públicos","foot.navigatie":"Navegación","foot.locaties":"Ubicaciones",
    "foot.nieuwsbrief":"Boletín","foot.nieuwsbrief.p":"Análisis de mercado y nuevos inmuebles en tu correo.",
    "foot.inschrijven":"Suscribirse","foot.email":"Tu correo electrónico","foot.tagline":"Powered by People. Backed by Tech. Tu socio en inmuebles comerciales en los Países Bajos y España.",
    "foot.rights":"© 2026 Spring Real Estate. Todos los derechos reservados."
  }
};

(function(){
  const dict = window.SPRING_I18N;
  function apply(lang){
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i18n]').forEach(el=>{
      if(el.dataset.nl === undefined) el.dataset.nl = el.textContent;
      el.textContent = (lang!=='nl' && dict[lang] && dict[lang][el.dataset.i18n]) || el.dataset.nl;
    });
    document.querySelectorAll('[data-i18n-ph]').forEach(el=>{
      if(el.dataset.nlPh === undefined) el.dataset.nlPh = el.getAttribute('placeholder')||'';
      el.setAttribute('placeholder',(lang!=='nl' && dict[lang] && dict[lang][el.dataset.i18nPh]) || el.dataset.nlPh);
    });
    document.querySelectorAll('.lang button, .mm-lang button').forEach(b=>{
      b.classList.toggle('active', b.dataset.lang===lang);
    });
    try{ localStorage.setItem('spring-lang', lang); }catch(_){}
  }
  window.SPRING_setLang = apply;
  document.addEventListener('click', e=>{
    const b = e.target.closest('.lang button, .mm-lang button');
    if(b && b.dataset.lang) apply(b.dataset.lang);
  });
  let saved='nl';
  try{ saved = localStorage.getItem('spring-lang') || 'nl'; }catch(_){}
  document.addEventListener('DOMContentLoaded', ()=>apply(saved));
})();
