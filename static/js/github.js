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
        const res = await fetch('/api/github/');
        if (!res.ok) throw new Error('bad status');
        const data = await res.json();
        const user = data.user || {};

        let html = `
            <a href="${user.html_url || '#'}" target="_blank" rel="noopener noreferrer" class="gh-card">
                <div class="gh-card-avatar">
                    <img src="${user.avatar_url || ''}" alt="${user.login || ''}" />
                </div>
                <div class="gh-card-info">
                    <span class="gh-card-name">${user.name || user.login || ''}</span>
                    <span class="gh-card-login">@${user.login || ''}</span>
                    ${user.bio ? `<span class="gh-card-bio">${user.bio}</span>` : ''}
                </div>
            </a>
        `;

        html += `<div class="langs-container">`;
        (data.langs || []).forEach(({ lang, percent }) => {
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
            statsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    } catch (error) {
        console.error('GitHub stats error:', error);
        statsContainer.innerHTML = '<p class="error">GitHub stats unavailable</p>';
        statsContainer.classList.add('show');
    }
});
