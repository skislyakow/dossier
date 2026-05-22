const link = document.querySelector('.github-link');
const statsContainer = document.getElementById('stats');

link.addEventListener('click', async (e) => {
    e.preventDefault();
    
    if (statsContainer.classList.contains('show')) {
        statsContainer.classList.remove('show');
        statsContainer.classList.add('hidden');
        return;
    }

    statsContainer.innerHTML = '<div class="loader"></div>';
    statsContainer.classList.remove('hidden');
    statsContainer.classList.add('show');

    try {
        const [userRes, reposRes] = await Promise.all([
            fetch('https://api.github.com/users/skislyakow'),
            fetch('https://api.github.com/users/skislyakow/repos?sort=stars&per_page=6')
        ]);

        const userData = await userRes.json();
        const repos = await reposRes.json();

        const reposRes2 = await Promise.all(repos.map(r => 
            fetch(`https://api.github.com/repos/skislyakow/${r.name}/languages`).then(res => res.json())
        ));

        const langCount = {};
        repos.forEach((repo, i) => {
            const langs = reposRes2[i];
            for (const [lang, bytes] of Object.entries(langs)) {
                langCount[lang] = (langCount[lang] || 0) + bytes;
            }
        });

        const total = Object.values(langCount).reduce((a, b) => a + b, 0);
        const sorted = Object.entries(langCount).sort((a, b) => b[1] - a[1]).slice(0, 5);

        let html = `
            <a href="${userData.html_url}" target="_blank" rel="noopener noreferrer" class="gh-card">
                <div class="gh-card-avatar">
                    <img src="${userData.avatar_url}" alt="${userData.login}" />
                </div>
                <div class="gh-card-info">
                    <span class="gh-card-name">${userData.name || userData.login}</span>
                    <span class="gh-card-login">@${userData.login}</span>
                    ${userData.bio ? `<span class="gh-card-bio">${userData.bio}</span>` : ''}
                </div>
            </a>
        `;

        html += `<div class="langs-container">`;
        sorted.forEach(([lang, bytes]) => {
            const percent = Math.round((bytes / total) * 100);
            html += `
                <div class="lang-row">
                    <span class="lang-name">${lang}</span>
                    <div class="lang-bar"><div class="lang-fill" style="width: 0%"></div></div>
                    <span class="lang-percent">${percent}%</span>
                </div>
            `;
        });
        html += `</div>`;

        statsContainer.innerHTML = html;

        setTimeout(() => {
            statsContainer.querySelector('.gh-card')?.classList.add('visible');
            statsContainer.querySelector('.langs-container')?.classList.add('visible');
            document.querySelectorAll('.lang-fill').forEach(bar => {
                bar.style.width = bar.parentElement.nextElementSibling.textContent;
            });
            document.querySelectorAll('.lang-row').forEach(row => row.classList.add('visible'));
        }, 100);
    } catch (error) {
        console.error('GitHub stats error:', error);
        statsContainer.innerHTML = '<p class="error">GitHub stats unavailable</p>';
        statsContainer.classList.add('show');
    }
});