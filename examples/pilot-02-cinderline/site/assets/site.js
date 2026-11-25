'use strict';
(() => {
  const toggle = document.querySelector('.nav-toggle');
  const menu = document.querySelector('#site-nav');
  const notice = document.querySelector('[data-form-message]');
  if (notice) notice.focus();
  if (!toggle || !menu) return;
  const close = () => { menu.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-label','Open navigation'); };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { close(); toggle.focus(); } });
  menu.addEventListener('click', e => { if (e.target.closest('a')) close(); });
  window.addEventListener('resize', () => { if (innerWidth > 760) close(); });
})();
