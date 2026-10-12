// Состояние фильтра портфолио (GLOSSARY): единый владелец тега+роли.
// Все источники (скиллы, облако тегов, role-чипы) эмитят через set*,
// каждый модуль подсвечивает свою разметку через subscribe. Панели —
// не забота модуля: сценарий «открыть с фильтром/сбросом» решает portfolio.
(() => {
  const state = { tag: '', role: '' };
  const listeners = new Set();

  function get() {
    return { tag: state.tag, role: state.role };
  }

  function emit() {
    const snapshot = get();
    listeners.forEach((fn) => fn(snapshot));
  }

  function set(key, next) {
    const value = next || '';
    if (value === state[key]) return;
    state[key] = value;
    emit();
  }

  function setTag(next) {
    set('tag', next);
  }

  function setRole(next) {
    set('role', next);
  }

  function clear() {
    if (!state.tag && !state.role) return;
    state.tag = '';
    state.role = '';
    emit();
  }

  function subscribe(fn) {
    listeners.add(fn);
  }

  window.filterState = { get, setTag, setRole, clear, subscribe };
})();
