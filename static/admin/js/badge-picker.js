document.addEventListener('alpine:init', () => {
  Alpine.data('badgePicker', (el) => ({
    active: [],
    catalog: { github: [], pypi: [] },

    init() {
      try {
        this.active = JSON.parse(el.dataset.bpValue || '[]');
      } catch (e) {
        this.active = [];
      }
      try {
        this.catalog = JSON.parse(el.dataset.bpCatalog || '{}');
      } catch (e) {
        this.catalog = { github: [], pypi: [] };
      }
    },

    isActive(source) {
      return this.active.some(b => b.source === source);
    },

    toggle(badge) {
      const idx = this.active.findIndex(b => b.source === badge.source);
      if (idx >= 0) {
        this.active.splice(idx, 1);
      } else {
        this.active.push({ label: badge.label, source: badge.source });
      }
    },

    remove(index) {
      this.active.splice(index, 1);
    },

    addLabel() {
      const label = prompt('Label:');
      if (label) this.active.push({ label: label });
    },

    addStatic() {
      const label = prompt('Label:');
      if (!label) return;
      const value = prompt('Value:');
      this.active.push(value ? { label: label, value: value } : { label: label });
    },
  }));
});
