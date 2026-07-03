const PORTFOLIO = [
  {
    repo: "skislyakow/opencode-py",
    title: "Opencode Python SDK",
    tagline: "Python SDK для open source AI coding агента",
    features: [
      "Published on PyPI — pip install opencode-py",
      "Sync + Async API со streaming и сессиями",
      "Встроенный Web UI (ноль зависимостей)",
    ],
    links: {
      pypi: "https://pypi.org/project/opencode-py/",
    },
    badges: [
      "https://img.shields.io/pypi/v/opencode-py.svg?style=flat-square&labelColor=e4e4e7&color=6366f1",
      "https://img.shields.io/pypi/pyversions/opencode-py.svg?style=flat-square&labelColor=e4e4e7&color=6366f1",
      "https://img.shields.io/pypi/l/opencode-py.svg?style=flat-square&labelColor=e4e4e7&color=6366f1",
      "https://img.shields.io/pypi/dm/opencode-py.svg?style=flat-square&labelColor=e4e4e7&color=6366f1",
    ],
  },
  {
    repo: "skislyakow/ferma",
    title: "Ferma",
    tagline: "Автоматизированная ферма Telegram-каналов",
    features: [
      "Парсинг постов с t.me/s/ доноров",
      "Фильтрация рекламы, тизеров, дубликатов",
      "Автоперевод через Yandex Translate",
      "Публикация в каналы с CPA-ссылками",
    ],
    links: {},
    badges: [],
  },
  {
    repo: "skislyakow/dossier",
    title: "Dossier",
    tagline: "Персональный сайт-визитка с production-стеком и CI/CD",
    features: [
      "Typing-анимация на чистом JavaScript",
      "Интеграция с GitHub API (статистика, языки, звёзды)",
      "Секция портфолио с карточками проектов",
      "Production: Django + Gunicorn + Nginx на Ubuntu VPS",
      "Автодеплой через GitHub Actions",
    ],
    links: {
      www: "http://132.243.121.192/",
    },
    badges: [
      "https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white&labelColor=e4e4e7",
      "https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white&labelColor=e4e4e7",
      "https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black&labelColor=e4e4e7",
      "https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white&labelColor=e4e4e7",
      "https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white&labelColor=e4e4e7",
    ],
  },
];

const ICONS = {
  github: '<svg height="18" width="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
  pypi: '<svg height="18" width="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 7v10l10 5 10-5V7l-10-5zM4 9.24l6 3v6.47l-6-3V9.24zm14 0v6.47l-6 3V12.24l6-3zM12 5.06L17.66 8 12 10.94 6.34 8 12 5.06z"/></svg>',
  www: '<svg height="18" width="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>',
};

const portfolioBtn = document.getElementById('portfolio-btn');
const portfolioSection = document.getElementById('portfolio');

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
    const cards = await Promise.all(PORTFOLIO.map(async (project) => {
      const [repoRes, langRes] = await Promise.all([
        fetch(`https://api.github.com/repos/${project.repo}`),
        fetch(`https://api.github.com/repos/${project.repo}/languages`),
      ]);
      const repo = await repoRes.json();
      const langs = await langRes.json();
      return { ...project, repo, langs };
    }));

    let html = '';
    cards.forEach((project, i) => {
      const langEntries = Object.entries(project.langs);
      const totalBytes = Object.values(project.langs).reduce((a, b) => a + b, 0);

      const badgesHtml = (project.badges || []).map(url =>
        `<img src="${url}" alt="" class="portfolio-badge-img">`
      ).join('');

      let linksHtml = `<a href="${project.repo.html_url}" target="_blank" rel="noopener noreferrer" class="portfolio-link-icon" title="GitHub">${ICONS.github}</a>`;
      for (const [label, url] of Object.entries(project.links)) {
        const icon = ICONS[label] || ICONS.github;
        linksHtml += `<a href="${url}" target="_blank" rel="noopener noreferrer" class="portfolio-link-icon" title="${label}">${icon}</a>`;
      }

      html += `
        <div class="portfolio-card" style="animation-delay: ${i * 0.2}s">
          <div class="portfolio-card-header">
            <h3>${project.title}</h3>
            <span class="portfolio-stars"><svg height="14" width="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> ${project.repo.stargazers_count}</span>
          </div>
          <p class="portfolio-tagline">${project.tagline}</p>
          <div class="portfolio-tags">
            ${langEntries.map(([lang, bytes]) => {
              const pct = totalBytes ? Math.round((bytes / totalBytes) * 100) : 0;
              return `<span class="portfolio-tag">${lang} ${pct}%</span>`;
            }).join('')}
          </div>
          ${badgesHtml ? `<div class="portfolio-badges">${badgesHtml}</div>` : ''}
          <hr class="portfolio-divider">
          <ul class="portfolio-features">
            ${project.features.map(f => `<li>${f}</li>`).join('')}
          </ul>
          <hr class="portfolio-divider">
          <div class="portfolio-links">${linksHtml}</div>
        </div>
      `;
    });

    portfolioSection.innerHTML = html;
  } catch (err) {
    console.error('Portfolio error:', err);
    portfolioSection.innerHTML = '<p class="error">Failed to load portfolio</p>';
    portfolioSection.classList.add('show');
  }
});
