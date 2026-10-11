function esc(value) {
  return String(value == null ? '' : value).replace(
    /[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]),
  );
}

function prefersReducedMotion() {
  return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function disclosurePanel(trigger, panel, onClose) {
  if (!trigger || !panel) return null;
  trigger.setAttribute('aria-expanded', 'false');
  if (panel.id) trigger.setAttribute('aria-controls', panel.id);
  var api = {
    isOpen: function () {
      return panel.classList.contains('show');
    },
    set: function (open) {
      panel.classList.toggle('hidden', !open);
      panel.classList.toggle('show', open);
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    },
    close: function () {
      if (!api.isOpen()) return false;
      api.set(false);
      if (typeof onClose === 'function') onClose();
      return true;
    },
  };
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' && e.key !== 'Esc') return;
    if (api.close()) trigger.focus({ preventScroll: true });
  });
  return api;
}
