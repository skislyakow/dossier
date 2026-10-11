// Секция Skills: рендер сгруппированной сетки из /api/skills/.
// Названия и порядок категорий приходят с сервера (categories), клиент
// группирует по коду и рендерит серверную метку (esc()). Клик по навыку —
// фильтр портфолио через window.__applyPortfolioTag.
(() => {
  const container = document.getElementById('skills');
  if (!container) return;

  window.getSkills().then(function (data) {
    const skills = data.skills || [];
    const categories = data.categories || [];
    let html = '';
    categories.forEach(function (cat) {
      const items = skills.filter(function (s) { return s.category === cat.code; });
      if (!items.length) return;
      html += '<div class="skill-group"><h3 class="skill-group-title">' + esc(cat.label) + '</h3><div class="skill-group-items">';
      html += items.map(function (s) {
        const size = ['xl', 'lg', 'md', 'sm'].indexOf(s.size) !== -1 ? s.size : 'sm';
        return '<button type="button" class="tag tag-' + size + '" data-tag="' + esc(s.tag) + '">' + esc(s.name) + '</button>';
      }).join('');
      html += '</div></div>';
    });
    container.innerHTML = html;
  }).catch(function () {});

  container.addEventListener('click', function (e) {
    const btn = e.target.closest('.tag[data-tag]');
    if (!btn || typeof window.__applyPortfolioTag !== 'function') return;
    window.__applyPortfolioTag(btn.getAttribute('data-tag'));
  });
})();