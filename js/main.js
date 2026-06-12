/* Spring Real Estate — concept interactions */

// Mobile menu
const burger = document.getElementById('burger');
const mobileMenu = document.getElementById('mobileMenu');
const mmClose = document.getElementById('mmClose');
if (burger) burger.addEventListener('click', () => mobileMenu.classList.add('open'));
if (mmClose) mmClose.addEventListener('click', () => mobileMenu.classList.remove('open'));

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
    const grid = scope.querySelector('.people-grid, .blog-grid');
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
