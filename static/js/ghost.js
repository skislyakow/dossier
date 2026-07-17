function initGhostSkills() {
  var container = document.querySelector('.hero-ghost');
  if (!container) return;

  fetch('/api/skills/').then(function (r) { return r.json(); }).then(function (skills) {
    var shuffled = skills.slice().sort(function () { return Math.random() - 0.5; });
    var selected = shuffled.slice(0, Math.min(shuffled.length, 8));
    var sizes = { xl: '5rem', lg: '4rem', md: '3rem', sm: '2rem' };

    selected.forEach(function (skill) {
      var el = document.createElement('span');
      el.className = 'ghost-skill';
      el.textContent = skill.name;
      el.style.cssText = [
        'top: ' + (Math.random() * 80 + 5) + '%',
        'left: ' + (Math.random() * 80 + 5) + '%',
        'font-size: ' + (sizes[skill.size] || '3rem'),
        'animation-duration: ' + (14 + Math.random() * 10) + 's',
        'animation-delay: ' + (Math.random() * 12) + 's',
      ].join(';');
      container.appendChild(el);
    });
  });
}

document.addEventListener('DOMContentLoaded', function () {
  setTimeout(initGhostSkills, 500);
});
