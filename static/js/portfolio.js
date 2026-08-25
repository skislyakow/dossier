const ICONS = {
  github: '<svg height="18" width="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
  pypi: '<svg height="18" width="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 7v10l10 5 10-5V7l-10-5zM4 9.24l6 3v6.47l-6-3V9.24zm14 0v6.47l-6 3V12.24l6-3zM12 5.06L17.66 8 12 10.94 6.34 8 12 5.06z"/></svg>',
  www: '<svg height="18" width="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>',
  telegram: '<svg height="18" width="18" viewBox="0 0 24 24" fill="currentColor"><path d="M11.944 0A12 12 0 000 12a12 12 0 0012 12 12 12 0 0012-12A12 12 0 0012 0a12 12 0 00-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 01.171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>',
  vk: '<svg height="18" width="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.785 16.241s.288-.032.436-.194c.136-.148.132-.427.132-.427s-.02-1.304.576-1.496c.588-.19 1.341 1.26 2.14 1.818.605.422 1.064.33 1.064.33l2.137-.03s1.117-.071.587-.964c-.043-.073-.308-.661-1.588-1.87-1.34-1.264-1.16-1.059.453-3.246.983-1.332 1.376-2.145 1.253-2.493-.117-.332-.84-.244-.84-.244l-2.406.015s-.178-.025-.31.056c-.13.079-.213.262-.213.262s-.382 1.03-.892 1.906c-1.074 1.846-1.504 1.943-1.68 1.829-.408-.263-.306-1.057-.306-1.62 0-1.762.264-2.497-.516-2.687-.26-.063-.451-.104-1.115-.112-.854-.009-1.577.003-1.987.206-.273.135-.484.435-.356.452.158.021.515.098.704.36.245.34.236 1.106.236 1.106s.141 2.107-.33 2.368c-.324.179-.769-.186-1.722-1.853-.489-.854-.858-1.802-.858-1.802s-.141-.349-.327-.465c-.24-.15-.577-.098-.577-.098L5.8 11.54s-.758.024-.83.356c-.067.303.28.927.301 1.108.014.106.144.198.144.198.512.904 1.497 2.386 1.497 2.386.748 1.098 1.252 1.029 1.252 1.029.244.006.706-.07.863-.276.153-.2.375-.476.375-.476s1.121-.18 2.383-.49z"/></svg>',
};

function renderProjectMedia(project, skills) {
  if (project.screenshot) {
    return `<img src="${project.screenshot}" alt="${project.title}" class="portfolio-card-img" loading="lazy">`;
  }
  const ghost = (skills || []).map(skill => {
    const size = 1.1 + Math.random() * 2.8;
    return `<span class="material-symbols-outlined portfolio-ghost-skill" style="top: ${(5 + Math.random() * 80).toFixed(1)}%; left: ${(5 + Math.random() * 80).toFixed(1)}%; font-size: ${size.toFixed(1)}rem; animation-duration: ${(12 + Math.random() * 10).toFixed(1)}s; animation-delay: ${(Math.random() * 5).toFixed(1)}s;">${skill.icon || 'code'}</span>`;
  }).join('');
  return `<div class="portfolio-card-placeholder">${ghost}</div>`;
}

async function fetchProjectData(project) {
  const promises = [
    fetch(`https://api.github.com/repos/${project.repo}`).catch(() => null),
    fetch(`https://api.github.com/repos/${project.repo}/languages`).catch(() => null),
  ];

  if (project.pypi) {
    promises.push(
      fetch(`https://pypi.org/pypi/${project.pypi}/json`).catch(() => null)
    );
    promises.push(
      fetch(`https://pypistats.org/api/packages/${project.pypi}/recent`).catch(() => null)
    );
  }

  const results = await Promise.all(promises);

  let repo = {};
  let langs = {};
  try {
    if (results[0]?.ok) repo = await results[0].json();
  } catch (_) {}
  try {
    if (results[1]?.ok) langs = await results[1].json();
  } catch (_) {}

  let pypi = null;
  let stats = null;

  if (project.pypi) {
    try {
      if (results[2]?.ok) pypi = await results[2].json();
    } catch (_) {}
    try {
      if (results[3]?.ok) stats = await results[3].json();
    } catch (_) {}
  }

  return { ...project, repo, langs, pypi, stats };
}

function parsePythonVersions(requiresPython) {
  if (!requiresPython) return "";
  const match = requiresPython.match(/[\d.]+/g);
  if (!match) return requiresPython;
  return match.join(" | ");
}

function formatDownloads(count) {
  if (!count || count < 0) return null;
  if (count >= 1000000) return `${(count / 1000000).toFixed(1)}m`;
  if (count >= 1000) return `${(count / 1000).toFixed(1)}k`;
  return String(count);
}

function resolveBadge(badge, ctx) {
  if (!badge.source) {
    if (badge.value) {
      return { label: badge.label, value: badge.value };
    }
    return { label: badge.label };
  }

  const { source } = badge;
  let value = null;

  if (source === "github_stars") {
    value = ctx.repo.stargazers_count;
    if (value !== undefined) value = String(value);
  } else if (source === "github_forks") {
    value = ctx.repo.forks_count;
    if (value !== undefined) value = String(value);
  } else if (source === "github_license") {
    value = ctx.repo.license?.spdx_id || null;
  } else if (source === "github_lang") {
    value = ctx.repo.language || null;
  } else if (source === "github_issues") {
    value = ctx.repo.open_issues_count;
    if (value !== undefined) value = String(value);
  } else if (source === "github_size") {
    value = ctx.repo.size;
    if (value !== undefined) {
      if (value >= 1024) value = `${(value / 1024).toFixed(1)} MB`;
      else value = `${value} KB`;
    }
  } else if (source === "github_created") {
    value = ctx.repo.created_at
      ? new Date(ctx.repo.created_at).toLocaleDateString("ru-RU")
      : null;
  } else if (source === "github_updated") {
    value = ctx.repo.pushed_at
      ? new Date(ctx.repo.pushed_at).toLocaleDateString("ru-RU")
      : null;
  } else if (source === "pypi_version") {
    value = ctx.pypi?.info?.version ? `v${ctx.pypi.info.version}` : null;
  } else if (source === "pypi_python") {
    value = ctx.pypi?.info?.requires_python
      ? parsePythonVersions(ctx.pypi.info.requires_python)
      : null;
  } else if (source === "pypi_license") {
    value = ctx.pypi?.info?.license || null;
  } else if (source === "pypistats_month") {
    value = ctx.stats?.data?.last_month != null
      ? `${formatDownloads(ctx.stats.data.last_month)}/mo`
      : null;
  } else if (source === "pypistats_total") {
    value = ctx.stats?.data?.total != null
      ? formatDownloads(ctx.stats.data.total)
      : null;
  }

  if (value === null || value === undefined) return null;
  return { label: badge.label, value: String(value) };
}

const portfolioBtn = document.getElementById('portfolio-btn');
const portfolioSection = document.getElementById('portfolio');

function buildPreviewHtml(project, skills) {
  const langEntries = Object.entries(project.langs);
  const totalBytes = Object.values(project.langs).reduce((a, b) => a + b, 0);

  const badgesHtml = (project.badges || [])
    .map(b => resolveBadge(b, project))
    .filter(Boolean)
    .map(b => {
      if (b.value) {
        return `<span class="badge"><span class="badge-label">${b.label}</span><span class="badge-value">${b.value}</span></span>`;
      }
      return `<span class="badge badge--single">${b.label}</span>`;
    })
    .join('');

  let linksHtml = `<a href="${project.repo?.html_url || '#'}" target="_blank" rel="noopener noreferrer" class="portfolio-link-icon" title="GitHub">${ICONS.github}</a>`;
  for (const [label, url] of Object.entries(project.links || {})) {
    const icon = ICONS[label] || ICONS.github;
    linksHtml += `<a href="${url}" target="_blank" rel="noopener noreferrer" class="portfolio-link-icon" title="${label}">${icon}</a>`;
  }

  return `
    <div class="portfolio-preview-body">
      <div class="portfolio-preview-content">
        <div class="portfolio-preview-info">
          <div class="portfolio-card-header">
            <div class="portfolio-card-title-wrap"><h3>${project.title}</h3></div>
            <span class="portfolio-stars"><svg height="14" width="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> ${project.repo?.stargazers_count ?? ''}</span>
          </div>
          <p class="portfolio-tagline">${project.tagline}</p>
          ${project.role ? `<span class="badge badge-role">role: ${project.role}</span>` : ''}
          <div class="portfolio-tags">
            ${langEntries.map(([lang, bytes]) => {
              const pct = totalBytes ? Math.round((bytes / totalBytes) * 100) : 0;
              return `<span class="portfolio-tag">${lang} ${pct}%</span>`;
            }).join('')}
          </div>
          ${badgesHtml ? `<div class="portfolio-badges">${badgesHtml}</div>` : ''}
          <hr class="portfolio-divider">
          <ul class="portfolio-features">
            ${(project.features || []).map(f => `<li>${f}</li>`).join('')}
          </ul>
          <hr class="portfolio-divider">
          <div class="portfolio-links">${linksHtml}</div>
        </div>
        <div class="portfolio-preview-media">${renderProjectMedia(project, skills)}</div>
      </div>
    </div>
  `;
}

portfolioBtn.addEventListener('click', async (e) => {
  e.preventDefault();

  if (portfolioSection.classList.contains('show')) {
    portfolioSection.classList.remove('show');
    portfolioSection.classList.add('hidden');
    return;
  }

  portfolioSection.innerHTML = '<div class="loader"></div>';
  portfolioSection.classList.remove('hidden');
  portfolioSection.classList.add('show');

  try {
    const [projects, skills] = await Promise.all([
      fetch('/api/projects/').then(r => r.json()),
      window.getSkills(),
    ]);
    const cards = await Promise.all(projects.map(fetchProjectData));

    const previewCache = new Map();
    cards.forEach(project => {
      const key = project.repo.full_name || project.title;
      previewCache.set(key, buildPreviewHtml(project, skills));
    });

    const roles = [...new Set(cards.map(p => p.role).filter(Boolean))];
    const counts = new Map();
    cards.forEach(p => counts.set(p.role || '', (counts.get(p.role || '') || 0) + 1));
    const total = cards.length;

    const catBtn = (role, label, count, active) =>
      `<button class="portfolio-cat${active ? ' active' : ''}" data-role="${role}" type="button"><span class="cat-brace">{ </span><span class="cat-name">${label}</span><span class="cat-count">: ${count}</span><span class="cat-brace"> }</span></button>`;

    const catsHtml = catBtn('', 'All', total, true) +
      roles.map(role => catBtn(role, role, counts.get(role) || 0, false)).join('');

    const listHtml = cards.map((project, i) => {
      const key = project.repo.full_name || project.title;
      return `<button class="portfolio-list-item${i === 0 ? ' active' : ''}" data-repo="${key}" data-role="${project.role || ''}" type="button">${project.title}</button>`;
    }).join('');

    const firstKey = cards[0].repo.full_name || cards[0].title;
    portfolioSection.innerHTML = `
      <div class="portfolio-cats">${catsHtml}</div>
      <div class="portfolio-layout">
        <div class="portfolio-list">${listHtml}</div>
        <div class="portfolio-preview">${previewCache.get(firstKey)}</div>
      </div>
    `;

    const preview = portfolioSection.querySelector('.portfolio-preview');
    const listItems = () => portfolioSection.querySelectorAll('.portfolio-list-item');

    listItems().forEach((item) => {
      item.addEventListener('click', () => {
        if (item.classList.contains('active')) return;
        listItems().forEach(el => el.classList.remove('active'));
        item.classList.add('active');
        preview.classList.remove('fade-in');
        void preview.offsetWidth;
        preview.innerHTML = previewCache.get(item.dataset.repo);
        preview.classList.add('fade-in');
      });
    });

    portfolioSection.querySelector('.portfolio-cats').addEventListener('click', (e) => {
      const btn = e.target.closest('.portfolio-cat');
      if (!btn || btn.classList.contains('active')) return;
      portfolioSection.querySelectorAll('.portfolio-cat').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const role = btn.dataset.role;
      let firstVisible = null;
      listItems().forEach(item => {
        const show = !role || item.dataset.role === role;
        item.style.display = show ? '' : 'none';
        if (show && !firstVisible) firstVisible = item;
      });

      const active = portfolioSection.querySelector('.portfolio-list-item.active');
      if (active && active.style.display === 'none' && firstVisible) {
        firstVisible.click();
      }
    });

    setTimeout(() => portfolioSection.scrollIntoView({ behavior: 'smooth', block: 'start' }), 150);
  } catch (err) {
    console.error('Portfolio error:', err);
    portfolioSection.innerHTML = '<p class="error">Failed to load portfolio</p>';
    portfolioSection.classList.add('show');
  }
});
