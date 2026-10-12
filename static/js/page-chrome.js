// Page-chrome: тема, acid-градиенты, scroll-reveal, back-to-top.
// Грузится последним (после contact.js); util.js обязан быть загружен раньше
// (prefersReducedMotion). Модуль владеет только «поверхностью страницы»;
// панели и их контент — у владельцев секций (portfolio/github/contact).
(() => {
  function bindGradient(el) {
    if (!el || prefersReducedMotion()) return;
    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      el.style.setProperty('--mx', x + '%');
      el.style.setProperty('--my', y + '%');
    });
  }

  function revealNow(root) {
    if (!root) return;
    root.querySelectorAll('.reveal:not(.is-visible)').forEach((el) => el.classList.add('is-visible'));
  }

  function revealObserveAll() {
    const items = document.querySelectorAll('.reveal');
    if (!items.length) return;
    if (prefersReducedMotion()) {
      items.forEach((el) => el.classList.add('is-visible'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    items.forEach((el) => io.observe(el));
  }

  function initTheme() {
    const root = document.documentElement;
    const toggle = document.getElementById('theme-toggle');
    const stored = localStorage.getItem('theme');
    if (stored === 'light') {
      root.setAttribute('data-theme', 'light');
    } else {
      root.removeAttribute('data-theme');
    }
    if (!toggle) return;
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      const isLight = root.getAttribute('data-theme') === 'light';
      if (isLight) {
        root.removeAttribute('data-theme');
        localStorage.setItem('theme', 'dark');
      } else {
        root.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
      }
    });
  }

  function initBackToTop() {
    const btn = document.getElementById('back-to-top');
    if (!btn) return;
    window.addEventListener('scroll', () => {
      btn.classList.toggle('visible', window.scrollY > 300);
    });
    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  bindGradient(document.querySelector('.hero'));
  bindGradient(document.getElementById('portfolio'));
  revealObserveAll();
  initTheme();
  initBackToTop();

  window.pageChrome = { reveal: { now: revealNow, observeAll: revealObserveAll } };
})();
