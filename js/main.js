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
