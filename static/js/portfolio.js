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
  },
];

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

      let linksHtml = `<a href="${project.repo.html_url}" target="_blank" rel="noopener noreferrer">GitHub</a>`;
      for (const [label, url] of Object.entries(project.links)) {
        linksHtml += ` · <a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`;
      }

      html += `
        <div class="portfolio-card" style="animation-delay: ${i * 0.2}s">
          <div class="portfolio-card-header">
            <h3>${project.title}</h3>
            <span class="portfolio-stars">&#11088; ${project.repo.stargazers_count}</span>
          </div>
          <p class="portfolio-tagline">${project.tagline}</p>
          <div class="portfolio-tags">
            ${langEntries.map(([lang, bytes]) => {
              const pct = totalBytes ? Math.round((bytes / totalBytes) * 100) : 0;
              return `<span class="portfolio-tag">${lang} ${pct}%</span>`;
            }).join('')}
          </div>
          <ul class="portfolio-features">
            ${project.features.map(f => `<li>${f}</li>`).join('')}
          </ul>
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
