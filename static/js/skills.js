// Секция Skills: рендер сгруппированной сетки из /api/skills/.
// Названия и порядок категорий приходят с сервера (categories), клиент
// группирует по коду и рендерит серверную метку (esc()). Клик по навыку —
// эмит в filterState; подсветка своих кнопок — по subscribe, своим DOM.
(() => {
  const container = document.getElementById('skills');
  if (!container) return;

  let skillsPromise;
  const getSkills = () => {
    skillsPromise = skillsPromise || fetch('/api/skills/')
      .then((r) => r.json())
      .catch(() => ({ skills: [], categories: [] }));
    return skillsPromise;
  };

  getSkills().then(function (data) {
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
    syncButtons(window.filterState.get());
  }).catch(function () {});

  function syncButtons(state) {
    container.querySelectorAll('.tag[data-tag]').forEach((btn) => {
      btn.classList.toggle('active', Boolean(state.tag) && btn.dataset.tag === state.tag);
    });
  }

  window.filterState.subscribe(syncButtons);

  container.addEventListener('click', function (e) {
    const btn = e.target.closest('.tag[data-tag]');
    if (!btn) return;
    window.filterState.setTag(btn.getAttribute('data-tag'));
  });
})();