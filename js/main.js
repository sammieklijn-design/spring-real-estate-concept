/* Spring Real Estate — concept interactions */

// Mobile menu
const burger = document.getElementById('burger');
const mobileMenu = document.getElementById('mobileMenu');
const mmClose = document.getElementById('mmClose');
if (burger) burger.addEventListener('click', () => mobileMenu.classList.add('open'));
if (mmClose) mmClose.addEventListener('click', () => mobileMenu.classList.remove('open'));

// Desktop dropdown nav — click to open/close
document.querySelectorAll('.has-drop > button').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation();
    const parent = btn.closest('.has-drop');
    const isOpen = parent.classList.contains('click-open');
    document.querySelectorAll('.has-drop').forEach(d => d.classList.remove('click-open'));
    if (!isOpen) parent.classList.add('click-open');
  });
});
document.addEventListener('click', () => {
  document.querySelectorAll('.has-drop').forEach(d => d.classList.remove('click-open'));
});

// Search tabs
const tabs = document.getElementById('searchTabs');
if (tabs) {
  tabs.addEventListener('click', e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    tabs.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
}

// Moving hero banner (auto crossfade, with pause/play) — Colliers best practice
(function () {
  const bg = document.getElementById('heroBg');
  const toggle = document.getElementById('heroToggle');
  const dotsWrap = document.getElementById('heroDots');
  if (!bg) return;
  const slides = [...bg.querySelectorAll('img')];
  if (slides.length < 2) return;
  let i = 0, timer = null;
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let playing = !reduce;
  // dots
  const dots = slides.map((_, idx) => {
    const b = document.createElement('button');
    b.setAttribute('aria-label', 'Toon beeld ' + (idx + 1));
    if (idx === 0) b.classList.add('is-active');
    b.addEventListener('click', () => { show(idx); restart(); });
    dotsWrap && dotsWrap.appendChild(b);
    return b;
  });
  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach((s, idx) => s.classList.toggle('is-active', idx === i));
    dots.forEach((d, idx) => d.classList.toggle('is-active', idx === i));
  }
  function next() { show(i + 1); }
  function start() { stop(); timer = setInterval(next, 6000); }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  function restart() { if (playing) start(); }
  function setPlaying(p) {
    playing = p;
    if (toggle) {
      toggle.querySelector('.ht-pause').style.display = p ? '' : 'none';
      toggle.querySelector('.ht-play').style.display = p ? 'none' : '';
      toggle.querySelector('.ht-label').textContent = p ? 'Pauze' : 'Afspelen';
    }
    p ? start() : stop();
  }
  if (toggle) toggle.addEventListener('click', () => setPlaying(!playing));
  setPlaying(playing);
})();

// Working filters + search (team page, resources) on .filterable sections
(function () {
  document.querySelectorAll('.filterable').forEach(scope => {
    const grid = scope.querySelector('.people-grid, .blog-grid, .glossary, .case-grid');
    if (!grid) return;
    const items = [...grid.children];
    const chips = [...scope.querySelectorAll('.team-filter a')];
    const search = scope.querySelector('.list-search input');
    const empty = scope.querySelector('.filter-empty');
    let key = 'alle';
    function apply() {
      const q = (search ? search.value : '').toLowerCase().trim();
      let shown = 0;
      items.forEach(it => {
        const txt = it.textContent.toLowerCase();
        const cat = (it.getAttribute('data-cat') || '').toLowerCase();
        const okKey = key === 'alle' || (cat ? cat === key : txt.indexOf(key) >= 0);
        const okQ = !q || txt.indexOf(q) >= 0;
        const show = okKey && okQ;
        it.style.display = show ? '' : 'none';
        if (show) shown++;
      });
      if (empty) empty.style.display = shown ? 'none' : '';
    }
    chips.forEach(c => c.addEventListener('click', e => {
      e.preventDefault();
      key = (c.getAttribute('data-key') || c.textContent.trim().toLowerCase());
      if (key === 'alle' || c.textContent.trim().toLowerCase() === 'alle') key = 'alle';
      chips.forEach(x => x.classList.remove('active'));
      const tab = chips.find(x => (x.getAttribute('data-key') || x.textContent.trim().toLowerCase()) === key);
      (tab || chips[0]).classList.add('active');
      apply();
    }));
    // "toon alle" reset link inside empty-state
    scope.querySelectorAll('.filter-empty [data-key]').forEach(a => a.addEventListener('click', e => {
      e.preventDefault(); key = 'alle'; if (search) search.value = '';
      chips.forEach(x => x.classList.remove('active')); if (chips[0]) chips[0].classList.add('active'); apply();
    }));
    if (search) search.addEventListener('input', apply);
  });
})();

// Count-up animation for stat numbers ("resultaten laten oplopen")
(function () {
  const sel = '.hero-stats b, .stats-band b, .sf-stat b, .stat-pop b';
  const nodes = [...document.querySelectorAll(sel)].filter(el => /^\d[\d.]*(\+|%)?$/.test(el.textContent.trim()));
  if (!nodes.length || !('IntersectionObserver' in window)) return;
  function run(el) {
    const txt = el.textContent.trim();
    const m = txt.match(/^(\d[\d.]*)(\+|%)?$/);
    const hadDot = m[1].includes('.');
    const target = parseInt(m[1].replace(/\./g, ''), 10);
    const suffix = m[2] || '';
    const dur = 1100, t0 = performance.now();
    function fmt(n) { return hadDot && n >= 1000 ? n.toLocaleString('nl-NL') : String(n); }
    function step(now) {
      const p = Math.min(1, (now - t0) / dur);
      const e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(target * e)) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  const obs = new IntersectionObserver((entries, o) => {
    entries.forEach(en => { if (en.isIntersecting) { run(en.target); o.unobserve(en.target); } });
  }, { threshold: 0.5 });
  nodes.forEach(n => obs.observe(n));
})();

// Clickable team members -> modal with their info
(function () {
  function buildModal() {
    const m = document.createElement('div');
    m.className = 'pmodal';
    m.innerHTML = '<div class="pmodal-ov" data-close></div>' +
      '<div class="pmodal-card"><button class="pmodal-close" data-close aria-label="Sluiten">&times;</button>' +
      '<div class="pm-photo"><img alt=""></div>' +
      '<div class="pm-body"><div class="pm-role"></div><h3></h3><p class="pm-bio"></p><div class="pm-contact"></div></div></div>';
    document.body.appendChild(m);
    m.addEventListener('click', e => { if (e.target.hasAttribute('data-close')) m.classList.remove('open'); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') m.classList.remove('open'); });
    return m;
  }
  let modal;
  const ICON = {
    mail: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    phone: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    linkedin: '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.8-2 3.7-2 4 0 4.75 2.6 4.75 6V21H21v-5.3c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9V21H13z"/></svg>'
  };
  document.addEventListener('click', e => {
    const card = e.target.closest('.person, .agent');
    if (!card) return;
    if (e.target.closest('a[href]')) return; // let real links work
    e.preventDefault();
    // each team member has their own page — navigate there when available
    const directProfile = card.getAttribute('data-profile');
    if (directProfile) { window.location.href = directProfile; return; }
    if (!modal) modal = buildModal();
    const img = card.querySelector('img');
    const name = (card.querySelector('.name') || {}).textContent || '';
    const role = (card.querySelector('.role') || {}).textContent || '';
    const bio = (card.querySelector('.bio') || {}).textContent ||
      (name + ' is specialist bij Spring Real Estate. Neem gerust contact op voor een kennismaking en persoonlijk advies.');
    modal.querySelector('.pm-photo img').src = img ? img.src : '';
    modal.querySelector('.pm-role').textContent = role;
    modal.querySelector('h3').textContent = name;
    modal.querySelector('.pm-bio').textContent = bio;
    const mail = (name.toLowerCase().replace(/[^a-z]+/g, '.').replace(/^\.|\.$/g, '') || 'info') + '@springrealestate.com';
    modal.querySelector('.pm-contact').innerHTML =
      '<a href="mailto:' + mail + '">' + ICON.mail + ' ' + mail + '</a>' +
      '<a href="tel:+31302001020">' + ICON.phone + ' +31 30 200 10 20</a>' +
      '<a href="#">' + ICON.linkedin + ' LinkedIn-profiel</a>';
    // link to a full profile page when one exists for this person
    const ROSTER = ['daan-van-der-meer', 'sofia-martin', 'lars-bakker', 'emma-de-vries', 'thomas-jansen', 'nina-aydin'];
    const slug = name.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    const prof = card.getAttribute('data-profile') || (ROSTER.indexOf(slug) >= 0 ? 'profile-' + slug + '.html' : '');
    let pl = modal.querySelector('.pm-profile-link');
    if (!pl) { pl = document.createElement('a'); pl.className = 'btn btn--primary pm-profile-link'; pl.style.marginTop = '18px'; pl.textContent = 'Bekijk volledig profiel'; modal.querySelector('.pm-body').appendChild(pl); }
    if (prof) { pl.href = prof; pl.style.display = 'inline-flex'; } else { pl.style.display = 'none'; }
    modal.classList.add('open');
  });
})();

// Listings page — working filters (checkboxes + area + search), dynamic count & chips
(function () {
  const grid = document.querySelector('.results-grid');
  const filters = document.getElementById('filters');
  if (!grid || !filters) return;
  const cards = [...grid.querySelectorAll('.prop-card')];
  const checks = [...filters.querySelectorAll('input[type=checkbox][data-fgroup]')];
  const amin = document.getElementById('fAreaMin');
  const amax = document.getElementById('fAreaMax');
  const search = document.querySelector('.page-hero .search input');
  const rcCount = document.getElementById('rcCount');
  const chipbar = document.getElementById('chipbar');
  const empty = document.getElementById('listEmpty');
  const wpmin = document.getElementById('fWpMin');
  const wpmax = document.getElementById('fWpMax');
  const LABELS = { huur: 'Te huur', koop: 'Te koop', kantoor: 'Kantoorruimte', bedrijf: 'Bedrijfsruimte', winkel: 'Winkelruimte', belegging: 'Beleggingsobject', amsterdam: 'Amsterdam', utrecht: 'Utrecht', valencia: 'Valencia', estepona: 'Estepona', parkeren: 'Parkeren', vergaderen: 'Vergaderruimte', receptie: 'Receptieservice', ov: 'Dichtbij OV', breeam: 'BREEAM / Duurzaam', lift: 'Lift aanwezig' };
  function apply() {
    const groups = {};
    checks.filter(c => c.checked).forEach(c => { (groups[c.dataset.fgroup] = groups[c.dataset.fgroup] || new Set()).add(c.dataset.val); });
    const mn = parseFloat(amin && amin.value) || 0;
    const mx = parseFloat(amax && amax.value) || Infinity;
    const wpMn = parseFloat(wpmin && wpmin.value) || 0;
    const wpMx = parseFloat(wpmax && wpmax.value) || Infinity;
    const q = (search ? search.value : '').toLowerCase().trim();
    let shown = 0;
    cards.forEach(card => {
      let ok = true;
      for (const g in groups) {
        if (g === 'wensen') continue;
        if (!groups[g].has(card.dataset[g])) { ok = false; break; }
      }
      if (ok) { const a = parseFloat(card.dataset.area) || 0; if (a < mn || a > mx) ok = false; }
      if (ok && (wpMn > 0 || wpMx < Infinity)) {
        const wp = parseFloat(card.dataset.wp);
        if (!wp || wp < wpMn || wp > wpMx) ok = false;
      }
      if (ok && groups['wensen']) {
        const cardW = (card.dataset.wensen || '').split(' ');
        for (const w of groups['wensen']) { if (!cardW.includes(w)) { ok = false; break; } }
      }
      if (ok && q) ok = card.textContent.toLowerCase().indexOf(q) >= 0;
      card.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });
    if (rcCount) rcCount.textContent = shown;
    if (empty) empty.style.display = shown ? 'none' : '';
    document.dispatchEvent(new CustomEvent('listings:filtered'));
    if (chipbar) {
      chipbar.innerHTML = '';
      checks.filter(c => c.checked).forEach(c => {
        const chip = document.createElement('span'); chip.className = 'fchip';
        chip.innerHTML = (LABELS[c.dataset.val] || c.dataset.val) + ' <button aria-label="Verwijder">&times;</button>';
        chip.querySelector('button').addEventListener('click', e => { e.preventDefault(); c.checked = false; apply(); });
        chipbar.appendChild(chip);
      });
    }
  }
  checks.forEach(c => c.addEventListener('change', apply));
  [amin, amax, wpmin, wpmax].forEach(el => el && el.addEventListener('input', apply));
  if (search) search.addEventListener('input', apply);
  function clearAll(e) { if (e) e.preventDefault(); checks.forEach(c => c.checked = false); if (amin) amin.value = ''; if (amax) amax.value = ''; if (wpmin) wpmin.value = ''; if (wpmax) wpmax.value = ''; if (search) search.value = ''; apply(); }
  const fc = document.getElementById('fClear'); if (fc) fc.addEventListener('click', clearAll);
  const fc2 = document.getElementById('listClear2'); if (fc2) fc2.addEventListener('click', clearAll);
  const ft = document.getElementById('filterToggle'); if (ft) ft.addEventListener('click', () => filters.classList.toggle('open'));
  // Prefill from URL (finder wizard / deep links): ?offer=&type=&loc=&area=&q=
  (function () {
    const p = new URLSearchParams(location.search);
    ['offer', 'type', 'loc'].forEach(g => {
      const v = p.get(g); if (!v) return;
      const c = checks.find(x => x.dataset.fgroup === g && x.dataset.val === v);
      if (c) c.checked = true;
    });
    const area = p.get('area'); if (area && amin) amin.value = area;
    const q = p.get('q'); if (q && search) search.value = q;
  })();
  apply();
})();

// Language switcher (concept — stores choice; real site swaps content / routes /nl /en /es)
const lang = document.getElementById('lang');
if (lang) {
  lang.addEventListener('click', e => {
    const btn = e.target.closest('button');
    if (!btn) return;
    lang.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.documentElement.lang = btn.dataset.lang;
    try { localStorage.setItem('spring-lang', btn.dataset.lang); } catch (_) {}
  });
}

/* ============================================================
   NEXT-LEVEL ENHANCEMENTS (additive — appended)
   ============================================================ */

// 1. Scroll-reveal animations
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const sel = '.sec-head,.cards-grid,.kat-grid,.values-grid,.units-grid,.units-acc,.two-col,.statfeature,.txn-list,.news-wrap,.glossary,.vac-list,.people-grid,.dark-cards,.logos-row,.results-grid,.team-grid,.svc-grid,.sector-grid,.timeline,.pf-facts,.split,.panel';
  const els = [...document.querySelectorAll(sel)];
  els.forEach(e => e.classList.add('reveal'));
  const io = new IntersectionObserver((ents) => {
    ents.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  els.forEach(e => io.observe(e));
  // failsafe: never leave content hidden
  setTimeout(() => els.forEach(e => e.classList.add('in')), 1800);
})();

// 2. Sticky shrinking header
(function () {
  const h = document.querySelector('.header'); if (!h) return;
  const on = () => h.classList.toggle('scrolled', window.scrollY > 24);
  on(); addEventListener('scroll', on, { passive: true });
})();

// 3. Active nav highlight
(function () {
  const page = (location.pathname.split('/').pop() || 'index.html');
  document.querySelectorAll('.nav a[href]').forEach(a => {
    const href = a.getAttribute('href');
    if (href === page) a.classList.add('active-nav');
  });
})();

// 4. Back-to-top button
(function () {
  const b = document.createElement('button');
  b.className = 'to-top'; b.setAttribute('aria-label', 'Terug naar boven');
  b.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
  document.body.appendChild(b);
  const on = () => b.classList.toggle('show', window.scrollY > 600);
  on(); addEventListener('scroll', on, { passive: true });
  b.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
})();

// 5. Cookie consent banner
(function () {
  try { if (localStorage.getItem('spring-cookie')) return; } catch (_) {}
  const lang = (document.documentElement.lang || 'nl');
  const txt = lang === 'en' ? 'We use cookies to improve your experience and analyse traffic.'
    : lang === 'es' ? 'Usamos cookies para mejorar tu experiencia y analizar el tráfico.'
      : 'We gebruiken cookies om je ervaring te verbeteren en het gebruik te analyseren.';
  const ok = lang === 'en' ? 'Accept' : lang === 'es' ? 'Aceptar' : 'Akkoord';
  const c = document.createElement('div');
  c.className = 'cookie';
  c.innerHTML = '<p>' + txt + ' <a href="#">Privacy</a></p><button class="btn btn--primary">' + ok + '</button>';
  document.body.appendChild(c);
  document.body.classList.add('has-cookie'); // lifts the leadbot above the banner
  c.querySelector('button').addEventListener('click', () => { try { localStorage.setItem('spring-cookie', '1'); } catch (_) {} c.remove(); document.body.classList.remove('has-cookie'); });
})();

// 6. Favorites (hearts persist in localStorage)
(function () {
  const KEY = 'spring-favs';
  let favs; try { favs = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (_) { favs = []; }
  document.querySelectorAll('.prop-card .fav').forEach(fav => {
    const card = fav.closest('.prop-card');
    const id = ((card.querySelector('h3') || {}).textContent || card.getAttribute('href') || '').trim();
    if (favs.indexOf(id) >= 0) fav.classList.add('is-fav');
    fav.addEventListener('click', e => {
      e.preventDefault(); e.stopPropagation();
      const i = favs.indexOf(id);
      if (i >= 0) { favs.splice(i, 1); fav.classList.remove('is-fav'); }
      else { favs.push(id); fav.classList.add('is-fav'); }
      try { localStorage.setItem(KEY, JSON.stringify(favs)); } catch (_) {}
    });
  });
})();

// 7. Listings ?q= prefill (the AI-search module #19 handles routing/submit)
(function () {
  if (!document.querySelector('.results-grid')) return;
  const q = new URLSearchParams(location.search).get('q');
  if (q) { const inp = document.querySelector('.page-hero .search input'); if (inp) { inp.value = q; inp.dispatchEvent(new Event('input')); } }
})();

// 8. Listing-detail gallery: thumbnail swap + lightbox
(function () {
  const main = document.querySelector('.g-main img');
  const thumbs = [...document.querySelectorAll('.g-side .g-thumb img')];
  if (!main && !thumbs.length) return;
  thumbs.forEach(th => th.addEventListener('click', () => { if (main) { const s = main.getAttribute('src'); main.setAttribute('src', th.getAttribute('src')); th.setAttribute('src', s); } }));
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.innerHTML = '<button class="lb-close" aria-label="Sluiten">&times;</button><img alt="">';
  document.body.appendChild(lb);
  const lbImg = lb.querySelector('img');
  if (main) main.addEventListener('click', () => { lbImg.src = main.src; lb.classList.add('open'); });
  lb.addEventListener('click', e => { if (e.target !== lbImg) lb.classList.remove('open'); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') lb.classList.remove('open'); });
})();

// 11. Skip-to-content link + main landmark
(function () {
  const target = document.querySelector('.hero, .page-hero, .detail-top, main, section');
  if (target && !target.id) target.id = 'main';
  const a = document.createElement('a');
  a.className = 'skip-link'; a.href = '#' + (target ? target.id : 'main');
  a.textContent = 'Naar inhoud';
  document.body.insertBefore(a, document.body.firstChild);
})();

// 12. Lazy-load images (skip above-the-fold hero/gallery)
(function () {
  document.querySelectorAll('img:not([loading])').forEach(img => {
    if (img.closest('.hero, .page-hero, .g-main, .logo')) return;
    img.loading = 'lazy'; img.decoding = 'async';
  });
})();

// 13. Form submit feedback (non-search forms)
(function () {
  function toast(msg) {
    let t = document.querySelector('.toast');
    if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 3400);
  }
  document.querySelectorAll('form').forEach(f => {
    if (f.classList.contains('search')) return;
    f.addEventListener('submit', e => {
      e.preventDefault();
      const lang = document.documentElement.lang || 'nl';
      toast(lang === 'en' ? 'Thank you! We will be in touch shortly.' : lang === 'es' ? '¡Gracias! Te contactaremos en breve.' : 'Bedankt! We nemen snel contact met u op.');
      try { f.reset(); } catch (_) {}
    });
  });
})();

// 9 + 10. Structured data (JSON-LD) + Open Graph / Twitter meta
(function () {
  const head = document.head, origin = location.origin;
  function ld(obj) { const s = document.createElement('script'); s.type = 'application/ld+json'; s.textContent = JSON.stringify(obj); head.appendChild(s); }
  function meta(key, val, attr) { if (!val) return; const m = document.createElement('meta'); m.setAttribute(attr || 'property', key); m.setAttribute('content', val); head.appendChild(m); }
  // Organization / RealEstateAgent — every page
  ld({ "@context": "https://schema.org", "@type": "RealEstateAgent", "name": "Spring Real Estate", "url": origin + "/", "logo": origin + "/images/logo-ink.png", "image": origin + "/images/hero.jpg", "email": "info@springrealestate.com", "telephone": "+31302001020", "priceRange": "€€", "areaServed": ["Nederland", "España"], "address": { "@type": "PostalAddress", "streetAddress": "Stadhouderskade 12", "addressLocality": "Utrecht", "postalCode": "3531 BJ", "addressCountry": "NL" } });
  // WebSite + search action
  ld({ "@context": "https://schema.org", "@type": "WebSite", "name": "Spring Real Estate", "url": origin + "/", "potentialAction": { "@type": "SearchAction", "target": origin + "/listings.html?q={query}", "query-input": "required name=query" } });
  // Breadcrumbs from .crumbs
  const cr = document.querySelector('.crumbs');
  if (cr) {
    const parts = [...cr.childNodes].map(n => n.textContent).join('/').split('/').map(s => s.trim()).filter(s => s && s !== '·');
    const links = [...cr.querySelectorAll('a')];
    const items = parts.map((name, i) => { const o = { "@type": "ListItem", "position": i + 1, "name": name }; if (links[i]) o.item = new URL(links[i].getAttribute('href'), location.href).href; return o; });
    if (items.length) ld({ "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items });
  }
  // FAQPage from FAQ items
  const faqEls = [...document.querySelectorAll('.faq-list details, details.faq-item')];
  const faqs = faqEls.map(d => { const sum = d.querySelector('summary'); const ans = d.querySelector('.ans, .faq-a, p, div:not(:first-child)'); if (!sum) return null; const q = sum.textContent.replace(/\s*\+\s*$/, '').trim(); const a = (ans ? ans.textContent : '').trim(); return q && a ? { "@type": "Question", "name": q, "acceptedAnswer": { "@type": "Answer", "text": a } } : null; }).filter(Boolean);
  if (faqs.length) ld({ "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faqs });
  // Open Graph / Twitter
  const desc = (document.querySelector('meta[name=description]') || {}).content || '';
  const img = document.querySelector('.hero img, .page-hero img, .media-tall img, .g-main img, .darkcard img');
  meta('og:title', document.title); meta('og:description', desc); meta('og:type', 'website');
  meta('og:site_name', 'Spring Real Estate'); meta('og:url', location.href);
  meta('og:image', img ? img.src : origin + '/images/hero.jpg');
  meta('twitter:card', 'summary_large_image', 'name'); meta('twitter:title', document.title, 'name'); meta('twitter:description', desc, 'name');
})();

// 15. Leadbot — chat / lead-capture widget (bottom-right)
(function () {
  const lang = (function () { try { return localStorage.getItem('spring-lang') || document.documentElement.lang || 'nl'; } catch (_) { return 'nl'; } })();
  const T = {
    nl: { label: 'Hulp nodig?', title: 'Spring Real Estate', status: 'Online · reactie < 1 werkdag', greet: '👋 Welkom bij Spring! Waarmee kunnen we je helpen?', quick: ['Ik zoek ruimte', 'Verkopen of verhuren', 'Investeren in vastgoed', 'Plan een gesprek'], ask: 'Top! Laat je gegevens achter, dan neemt de juiste specialist snel contact met je op.', name: 'Naam', email: 'E-mailadres', phone: 'Telefoon (optioneel)', msg: 'Je bericht', send: 'Versturen', thanks: n => `Bedankt ${n}! We nemen binnen één werkdag contact met je op. 🌱`, err: 'Vul je naam en een geldig e-mailadres in.', call: 'Bellen', mail: 'E-mail', wa: 'WhatsApp' },
    en: { label: 'Need help?', title: 'Spring Real Estate', status: 'Online · reply < 1 business day', greet: '👋 Welcome to Spring! How can we help you?', quick: ['I\'m looking for space', 'Sell or lease', 'Invest in real estate', 'Book a consultation'], ask: 'Great! Leave your details and the right specialist will get back to you soon.', name: 'Name', email: 'Email address', phone: 'Phone (optional)', msg: 'Your message', send: 'Send', thanks: n => `Thanks ${n}! We\'ll be in touch within one business day. 🌱`, err: 'Please enter your name and a valid email.', call: 'Call', mail: 'Email', wa: 'WhatsApp' },
    es: { label: '¿Ayuda?', title: 'Spring Real Estate', status: 'En línea · respuesta < 1 día', greet: '👋 ¡Bienvenido a Spring! ¿Cómo podemos ayudarte?', quick: ['Busco espacio', 'Vender o alquilar', 'Invertir en inmuebles', 'Reservar una cita'], ask: '¡Genial! Déjanos tus datos y el especialista adecuado te contactará pronto.', name: 'Nombre', email: 'Correo electrónico', phone: 'Teléfono (opcional)', msg: 'Tu mensaje', send: 'Enviar', thanks: n => `¡Gracias ${n}! Te contactaremos en un día laborable. 🌱`, err: 'Introduce tu nombre y un correo válido.', call: 'Llamar', mail: 'Correo', wa: 'WhatsApp' }
  }[lang] || null;
  const t = T || { label: 'Hulp nodig?', title: 'Spring Real Estate', status: 'Online', greet: 'Welkom!', quick: ['Ik zoek ruimte', 'Verkopen of verhuren', 'Investeren', 'Plan een gesprek'], ask: 'Laat je gegevens achter:', name: 'Naam', email: 'E-mail', phone: 'Telefoon', msg: 'Bericht', send: 'Versturen', thanks: n => `Bedankt ${n}!`, err: 'Vul naam en e-mail in.', call: 'Bellen', mail: 'E-mail', wa: 'WhatsApp' };

  const launch = document.createElement('button');
  launch.className = 'lead-launch'; launch.setAttribute('aria-label', t.label);
  launch.innerHTML = '<span class="ll-dot"></span><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg><span class="ll-label">' + t.label + '</span>';
  document.body.appendChild(launch);

  const panel = document.createElement('div');
  panel.className = 'lead-panel'; panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', t.title);
  panel.innerHTML =
    '<div class="lp-head"><div class="lp-ava">S</div><div><h4>' + t.title + '</h4><div class="lp-status">' + t.status + '</div></div><button class="lp-close" aria-label="Sluiten">&times;</button></div>' +
    '<div class="lp-body" id="lpBody"></div>' +
    '<div class="lp-actions"><a href="tel:+31302001020"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>' + t.call + '</a>' +
    '<a href="https://wa.me/31302001020" target="_blank" rel="noopener"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15l-1.3 4.8 4.9-1.3A10 10 0 1 0 12 2zm0 2a8 8 0 1 1-4.2 14.8l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 0 1 12 4z"/></svg>' + t.wa + '</a>' +
    '<a href="mailto:info@springrealestate.com"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>' + t.mail + '</a></div>';
  document.body.appendChild(panel);

  const body = panel.querySelector('#lpBody');
  function add(cls, html) { const m = document.createElement('div'); m.className = 'lp-msg ' + cls; m.innerHTML = html; body.appendChild(m); body.scrollTop = body.scrollHeight; return m; }
  function esc(s) { return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  let started = false;
  function start() {
    if (started) return; started = true;
    add('bot', t.greet);
    const q = document.createElement('div'); q.className = 'lp-quick';
    t.quick.forEach(opt => { const b = document.createElement('button'); b.textContent = opt; b.addEventListener('click', () => choose(opt)); q.appendChild(b); });
    body.appendChild(q); body.scrollTop = body.scrollHeight;
  }
  function choose(topic) {
    const q = body.querySelector('.lp-quick'); if (q) q.remove();
    add('user', esc(topic));
    setTimeout(() => { add('bot', t.ask); showForm(topic); }, 350);
  }
  function showForm(topic) {
    if (panel.querySelector('.lp-form')) return;
    const f = document.createElement('form'); f.className = 'lp-form';
    f.innerHTML = '<input name="name" placeholder="' + t.name + ' *" autocomplete="name"><input name="email" type="email" placeholder="' + t.email + ' *" autocomplete="email"><input name="phone" placeholder="' + t.phone + '" autocomplete="tel"><textarea name="msg" placeholder="' + t.msg + '">' + esc(topic) + '</textarea><button class="btn btn--primary" type="submit">' + t.send + '</button>';
    panel.querySelector('.lp-actions').before(f);
    f.addEventListener('submit', e => {
      e.preventDefault();
      const d = { name: f.name.value.trim(), email: f.email.value.trim(), phone: f.phone.value.trim(), topic: topic, msg: f.msg.value.trim() };
      if (!d.name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) { add('bot', t.err); return; }
      try { const a = JSON.parse(localStorage.getItem('spring-leads') || '[]'); a.push(Object.assign(d, { ts: Date.now() })); localStorage.setItem('spring-leads', JSON.stringify(a)); } catch (_) {}
      add('user', esc(d.name + ' · ' + d.email));
      f.remove();
      setTimeout(() => add('bot', t.thanks(esc(d.name.split(' ')[0]))), 350);
    });
    body.scrollTop = body.scrollHeight;
  }
  function open() { panel.classList.add('open'); launch.classList.add('hide'); start(); }
  function close() { panel.classList.remove('open'); launch.classList.remove('hide'); }
  launch.addEventListener('click', open);
  panel.querySelector('.lp-close').addEventListener('click', close);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
})();

// 16. Listings — segment toggle (Verhuur / Verkoop) + working sort
(function () {
  const grid = document.querySelector('.results-grid'); if (!grid) return;
  const offerChecks = [...document.querySelectorAll('input[data-fgroup="offer"]')];
  const seg = document.getElementById('segToggle');
  if (seg) {
    seg.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      seg.querySelectorAll('button').forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      const v = b.dataset.seg;
      offerChecks.forEach(c => { c.checked = (v !== 'all' && c.dataset.val === v); });
      (offerChecks[0] || {}).dispatchEvent && offerChecks[0].dispatchEvent(new Event('change'));
    });
  }
  const sortSel = document.querySelector('.results-tools .fselect');
  if (sortSel) {
    sortSel.addEventListener('change', () => {
      const v = sortSel.selectedIndex;
      const num = c => parseFloat(c.dataset.price) || 0;
      const area = c => parseFloat(c.dataset.area) || 0;
      let cmp = null;
      if (v === 1) cmp = (a, b) => num(a) - num(b);
      else if (v === 2) cmp = (a, b) => num(b) - num(a);
      else if (v === 3) cmp = (a, b) => area(b) - area(a);
      if (!cmp) return;
      [...grid.children].sort(cmp).forEach(c => grid.appendChild(c));
    });
  }
})();

// 17. Interactive maps (Leaflet) — listings overview (clustered price pins, follow filters) + detail mini-map
(function () {
  const listEl = document.getElementById('listings-map');
  const detEl = document.getElementById('detail-map');
  if (!listEl && !detEl) return;
  const COORD = { amsterdam: [52.339, 4.872], utrecht: [52.0894, 5.110], valencia: [39.4667, -0.3667], estepona: [36.4275, -5.1459] };
  function addCSS(href) { const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = href; document.head.appendChild(l); }
  function addJS(src) { return new Promise((res, rej) => { const s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.body.appendChild(s); }); }
  addCSS('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css');
  let chain = addJS('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js');
  if (listEl) { addCSS('https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css'); addCSS('https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css'); chain = chain.then(() => addJS('https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js')); }
  chain.then(init).catch(() => { if (listEl) listEl.style.display = 'none'; if (detEl) detEl.style.display = 'none'; });

  function tile(map) {
    window.L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', { attribution: '&copy; OpenStreetMap &copy; CARTO', subdomains: 'abcd', maxZoom: 19 }).addTo(map);
  }
  function pinIcon(L, offer, price) { return L.divIcon({ className: '', html: '<div class="map-pin ' + offer + '">' + price + '</div>', iconSize: [1, 1] }); }

  function init() {
    const L = window.L; if (!L) return;
    if (listEl) initOverview(L);
    if (detEl) initDetail(L);
  }

  function initOverview(L) {
    const cards = [...document.querySelectorAll('.results-grid .prop-card')]; if (!cards.length) { listEl.style.display = 'none'; return; }
    const map = L.map(listEl, { scrollWheelZoom: false }).setView([50, 3], 5);
    tile(map);
    const cluster = (L.markerClusterGroup ? L.markerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 46, spiderfyDistanceMultiplier: 1.6 }) : L.featureGroup());
    const pairs = [];
    cards.forEach((card, i) => {
      const base = COORD[card.dataset.loc]; if (!base) return;
      const ang = (i % 6) * 1.05;
      const lat = base[0] + Math.sin(ang) * 0.012 * (1 + (i % 3)), lng = base[1] + Math.cos(ang) * 0.018 * (1 + (i % 3));
      const offer = card.dataset.offer;
      const pn = card.querySelector('.fl-price'); const price = pn ? (pn.firstChild.textContent || '').trim() : '';
      const title = (card.querySelector('h3') || {}).textContent || '';
      const addr = (card.querySelector('.addr') || {}).textContent || '';
      const href = card.getAttribute('href') || '#';
      const m = L.marker([lat, lng], { icon: pinIcon(L, offer, price) });
      m.bindPopup('<div class="map-pop"><h4>' + title + '</h4><div class="mp-addr">' + addr + '</div><div class="mp-price">' + price + '</div><a href="' + href + '">Bekijk object &rarr;</a></div>');
      pairs.push({ card: card, marker: m, ll: [lat, lng] });
    });
    map.addLayer(cluster);
    function refresh() {
      cluster.clearLayers();
      const vis = pairs.filter(p => p.card.style.display !== 'none');
      vis.forEach(p => cluster.addLayer(p.marker));
      if (vis.length) map.fitBounds(vis.map(p => p.ll), { padding: [40, 40], maxZoom: 13 });
    }
    refresh();
    document.addEventListener('listings:filtered', refresh);
    setTimeout(() => map.invalidateSize(), 250);
  }

  function initDetail(L) {
    const base = COORD[detEl.dataset.loc] || [52.1, 5.1];
    const map = L.map(detEl, { scrollWheelZoom: false, zoomControl: true }).setView(base, 14);
    tile(map);
    const offer = detEl.dataset.offer || 'huur';
    const price = detEl.dataset.price ? detEl.dataset.price.replace(/<[^>]+>/g, '').trim() : '';
    L.marker(base, { icon: pinIcon(L, offer, price) }).addTo(map)
      .bindPopup('<div class="map-pop"><h4>' + (detEl.dataset.title || '') + '</h4><div class="mp-price">' + price + '</div></div>');
    setTimeout(() => map.invalidateSize(), 250);
  }
})();

// 18. Herbouwwaarde-check (HBW) — indicatieve herbouwwaarde + onderverzekeringsrisico
(function () {
  const go = document.getElementById('hbw-go'); if (!go) return;
  const RATE = { residentieel: 2100, kantoor: 1700, bedrijf: 1050, winkel: 1550 }; // €/m² indicatieve herbouwkosten
  const euro = n => '€ ' + Math.round(n).toLocaleString('nl-NL');
  const $ = id => document.getElementById(id);
  function calc() {
    const ins = parseFloat($('hbw-waarde').value) || 0;
    const cat = $('hbw-cat').value;
    const m2 = parseFloat($('hbw-m2').value) || 0;
    const lagen = Math.max(1, parseFloat($('hbw-lagen').value) || 1);
    const regio = $('hbw-regio').value;
    const btw = $('hbw-btw').value;
    if (!m2) { return; }
    let v = m2 * (RATE[cat] || 2000);
    v *= (1 + Math.min(lagen - 1, 10) * 0.015);
    if (regio === 'randstad') v *= 1.10;
    if (btw === 'incl') v *= 1.21;
    $('hbw-placeholder').style.display = 'none';
    $('hbw-out').style.display = '';
    $('hbw-value').textContent = euro(v);
    const risk = $('hbw-risk'), rt = $('hbw-risk-text'), det = $('hbw-detail');
    risk.classList.remove('mid', 'high');
    if (!ins) { rt.textContent = 'Vul de verzekerde waarde in voor uw risico'; det.textContent = 'Indicatieve herbouwwaarde o.b.v. ' + m2.toLocaleString('nl-NL') + ' m² ' + cat + '.'; return; }
    const ratio = v / ins;
    if (ratio <= 1.05) { rt.textContent = 'Lage kans op onderverzekering'; }
    else if (ratio <= 1.25) { risk.classList.add('mid'); rt.textContent = 'Middelgrote kans op onderverzekering'; }
    else { risk.classList.add('high'); rt.textContent = 'Hoge kans op onderverzekering'; }
    const pct = Math.round((ratio - 1) * 100);
    det.textContent = ratio > 1.05
      ? 'De indicatieve herbouwwaarde ligt circa ' + pct + '% boven uw verzekerde waarde van ' + euro(ins) + '. Een actuele taxatie voorkomt onderverzekering.'
      : 'Uw verzekerde waarde sluit goed aan op de indicatieve herbouwwaarde. Een periodieke taxatie houdt dit actueel.';
  }
  go.addEventListener('click', calc);
  ['hbw-waarde', 'hbw-cat', 'hbw-m2', 'hbw-lagen', 'hbw-regio', 'hbw-btw'].forEach(id => { const el = $(id); if (el) { el.addEventListener('input', calc); el.addEventListener('change', calc); } });
})();

// 20. Homepage finder wizard ("In een paar clicks") -> routes to listings with params
(function () {
  const f = document.getElementById('finder'); if (!f) return;
  const sel = { loc: null, type: null, area: null };
  const tabs = [...f.querySelectorAll('.finder-tabs .ft')];
  const panels = [...f.querySelectorAll('.finder-panel')];
  function go(step) { tabs.forEach((t, i) => t.classList.toggle('active', i === step)); panels.forEach((p, i) => p.hidden = i !== step); }
  tabs.forEach((t, i) => t.addEventListener('click', () => go(i)));
  panels.forEach((p, pi) => {
    p.querySelectorAll('.fp-opt').forEach(b => b.addEventListener('click', () => {
      p.querySelectorAll('.fp-opt').forEach(x => x.classList.remove('sel'));
      b.classList.add('sel');
      const v = b.dataset.val;
      if (pi === 0) { sel.loc = v; go(1); }
      else if (pi === 1) { sel.type = v; go(2); }
      else { sel.area = v; }
      const p2 = new URLSearchParams();
      if (sel.loc) p2.set('loc', sel.loc);
      if (sel.type) p2.set('type', sel.type);
      if (sel.area) p2.set('area', sel.area);
      p2.set('offer', 'huur');
      const btn = document.getElementById('finderGo');
      if (btn) btn.href = 'listings.html?' + p2.toString();
    }));
  });
})();

// 21. Recently viewed listings (localStorage) — capture on detail, render strip on listings
(function () {
  const KEY = 'spring-recent';
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (_) { return []; } }
  function save(a) { try { localStorage.setItem(KEY, JSON.stringify(a.slice(0, 6))); } catch (_) {} }
  // Capture on listing detail page
  const det = document.getElementById('detail-map');
  if (det) {
    const slug = location.pathname.split('/').pop().replace(/^aanbod-/, '').replace(/\.html$/, '');
    const item = {
      slug: slug,
      title: det.dataset.title || '',
      addr: (document.querySelector('.d-addr') || {}).textContent || '',
      price: det.dataset.price || '',
      offer: det.dataset.offer || 'huur',
      img: (document.querySelector('.g-main img') || {}).getAttribute('src') || ''
    };
    if (slug && item.title) {
      const list = load().filter(x => x.slug !== slug);
      list.unshift(item);
      save(list);
    }
    return;
  }
  // Render strip on listings page
  const anchor = document.querySelector('.results-grid');
  if (!anchor) return;
  const cur = location.pathname.split('/').pop();
  const items = load().filter(x => 'aanbod-' + x.slug + '.html' !== cur);
  if (items.length < 2) return;
  const sec = document.createElement('section');
  sec.className = 'section--tight recent-sec';
  sec.innerHTML = '<div class="container"><div class="sec-head"><div class="t"><span class="eyebrow" data-tr="1" data-en="Recently viewed" data-es="Visto recientemente">Recent bekeken</span><h2 class="disp">Verder waar je <em>was</em></h2></div></div><div class="recent-strip"></div></div>';
  const strip = sec.querySelector('.recent-strip');
  items.forEach(x => {
    const a = document.createElement('a');
    a.className = 'prop-card'; a.href = 'aanbod-' + x.slug + '.html';
    const tag = x.offer === 'koop' ? 'Te koop' : 'Te huur';
    a.innerHTML = '<div class="ph"><span class="tag tag--' + x.offer + '">' + tag + '</span>' + (x.img ? '<img src="' + x.img + '" alt="">' : '') + '</div>'
      + '<div class="body"><h3>' + x.title + '</h3><span class="addr">' + x.addr + '</span><div class="meta"><span class="price">' + x.price + '</span></div></div>';
    strip.appendChild(a);
  });
  const host = anchor.closest('section') || anchor.parentElement;
  if (host && host.parentElement) host.parentElement.insertBefore(sec, host);
})();

// 22. Quick-contact dock — persoonlijk contact in één klik, op elke pagina
(function () {
  if (document.querySelector('.qcontact')) return;
  const PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>';
  const WA = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M.06 24l1.7-6.2A11.9 11.9 0 1 1 12 24a11.9 11.9 0 0 1-5.7-1.45L.06 24zM6.6 20.1l.37.22a9.9 9.9 0 0 0 5.05 1.38h.004a9.9 9.9 0 1 0-8.4-4.6l.24.38-1 3.67 3.74-.98zM17.5 14.3c-.15-.25-.55-.4-1.15-.7s-1.77-.87-2.04-.97-.47-.15-.67.15-.77.97-.94 1.17-.35.22-.65.07a8.13 8.13 0 0 1-2.4-1.48 9 9 0 0 1-1.66-2.06c-.17-.3 0-.46.13-.6s.3-.35.45-.52a2 2 0 0 0 .3-.5.55.55 0 0 0 0-.52c-.07-.15-.67-1.62-.92-2.22s-.5-.5-.67-.5h-.57a1.1 1.1 0 0 0-.8.37 3.35 3.35 0 0 0-1.04 2.5 5.8 5.8 0 0 0 1.22 3.08 13.3 13.3 0 0 0 5.1 4.5c.7.3 1.27.49 1.7.63a4.1 4.1 0 0 0 1.88.12c.57-.09 1.77-.72 2.02-1.42s.25-1.3.17-1.42z"/></svg>';
  const MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>';
  const wrap = document.createElement('div');
  wrap.className = 'qcontact';
  wrap.innerHTML =
    '<a href="tel:+31302001020" aria-label="Bel direct">' + PHONE + '<span data-tr="1" data-en="Call now" data-es="Llamar">Bel direct</span></a>'
    + '<a class="qc-wa" href="https://wa.me/31302001020?text=Hoi%20Spring,%20ik%20heb%20een%20vraag" target="_blank" rel="noopener" aria-label="WhatsApp">' + WA + '<span>WhatsApp</span></a>'
    + '<a class="qc-mail" href="mailto:info@springrealestate.com" aria-label="E-mail">' + MAIL + '<span data-tr="1" data-en="Email" data-es="Correo">E-mail</span></a>';
  document.body.appendChild(wrap);
})();
