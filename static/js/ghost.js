function initGhostSkills() {
  var container = document.querySelector('.hero-ghost');
  if (!container) return;

  fetch('/api/skills/').then(function (r) { return r.json(); }).then(function (skills) {
    skills.forEach(function (skill) {
      var el = document.createElement('span');
      el.className = 'ghost-skill';
      el.style.cssText = [
        'top: ' + (Math.random() * 80 + 5) + '%',
        'left: ' + (Math.random() * 80 + 5) + '%',
        'animation-duration: ' + (14 + Math.random() * 10) + 's',
        'animation-delay: ' + (Math.random() * 12) + 's',
      ].join(';');

      var icon = document.createElement('span');
      icon.className = 'material-symbols-outlined ghost-skill-icon';
      var size = 1.5 + Math.random() * 4;
      icon.style.cssText = 'font-size: ' + size.toFixed(1) + 'rem';
      icon.textContent = skill.icon || 'code';
      el.appendChild(icon);

      container.appendChild(el);
    });
  });
}

document.addEventListener('DOMContentLoaded', function () {
  setTimeout(initGhostSkills, 500);
});
