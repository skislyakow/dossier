// Состояние фильтра портфолио (GLOSSARY): единый владелец тега+роли.
// Все источники (скиллы, облако тегов, role-чипы) эмитят через set*,
// каждый модуль подсвечивает свою разметку через subscribe. Панели —
// не забота модуля: сценарий «открыть с фильтром/сбросом» решает portfolio.
(() => {
  let tag = '';
  let role = '';
  const listeners = new Set();

  function get() {
    return { tag, role };
  }

  function emit() {
    const state = get();
    listeners.forEach((fn) => fn(state));
  }

  function setTag(next) {
    const value = next || '';
    if (value === tag) return;
    tag = value;
    emit();
  }

  function setRole(next) {
    const value = next || '';
    if (value === role) return;
    role = value;
    emit();
  }

  function clear() {
    if (!tag && !role) return;
    tag = '';
    role = '';
    emit();
  }

  function subscribe(fn) {
    listeners.add(fn);
    return () => listeners.delete(fn);
  }

  window.filterState = { get, setTag, setRole, clear, subscribe };
})();
