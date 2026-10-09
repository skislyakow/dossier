// Экранирование значений из API перед вставкой в HTML (закрыто в тикете 06)
function tlEsc(value) {
  return String(value == null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function prefersReducedMotion() {
  return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function initTimeline() {
  const dotsEl = document.getElementById("timeline-dots");
  const experienceEl = document.getElementById("experience");
  const progressEl = document.getElementById("timeline-progress");
  if (!dotsEl || !experienceEl) return;

  fetch('/api/timeline/').then(function (r) { return r.json(); }).then(function (data) {
    const PRIOR = data.prior;
    const JOB = data.job;
    const PRESENT = data.present;
    const TIMELINE = data.timeline || [];

    // Слоты рельса сверху вниз: prior → job → проекты → present
    const slots = [];
    if (PRIOR) slots.push({ id: "prior", kind: "prior", data: PRIOR });
    if (JOB) slots.push({ id: "job", kind: "job", data: JOB });
    TIMELINE.forEach(function (item, i) {
      slots.push({ id: "project-" + i, kind: "project", data: item });
    });
    if (PRESENT) slots.push({ id: "present", kind: "present", data: PRESENT });
    if (!slots.length) return;

    const total = slots.length;
    let active = null;

    function pctOf(index) {
      return total > 1 ? (index / (total - 1)) * 100 : 50;
    }

    function labelFor(slot) {
      if (slot.kind === "job") return (JOB.dateRange || "").split(" — ")[0] || JOB.title;
      if (slot.kind === "present") return "сейчас";
      return slot.data.date;
    }

    // Строка секции «Опыт»: дата (моно) + заголовок + роль/описание/ссылка
    function itemHtml(slot) {
      const d = slot.data;
      const date = slot.kind === "job" ? (d.dateRange || "")
        : slot.kind === "present" ? "сейчас"
        : (d.date || "");
      const role = slot.kind === "job" && d.role
        ? '<div class="exp-role">' + tlEsc(d.role) + '</div>'
        : "";
      const descText = slot.kind === "job" && !d.desc ? "Описание пока не добавлено" : (d.desc || "");
      const desc = descText ? '<p class="exp-desc">' + tlEsc(descText) + '</p>' : "";
      let link = "";
      if (slot.kind === "job" && d.url) {
        const host = String(d.url).replace(/^https?:\/\//, "").replace(/\/$/, "");
        link = '<a class="exp-link" href="' + tlEsc(d.url) + '" target="_blank" rel="noopener noreferrer">' + tlEsc(host) + '</a>';
      } else if (slot.kind === "project" && d.repo) {
        link = '<a class="exp-link" href="https://github.com/' + tlEsc(d.repo) + '" target="_blank" rel="noopener noreferrer">GitHub</a>';
      }
      return '<div class="exp-item exp-item--' + slot.kind + '" id="exp-' + tlEsc(slot.id) + '" data-slot="' + tlEsc(slot.id) + '">' +
        '<div class="exp-date">' + tlEsc(date) + '</div>' +
        '<h3 class="exp-title">' + tlEsc(d.title) + '</h3>' +
        role + desc + link +
        '</div>';
    }

    experienceEl.innerHTML =
      '<div class="exp-label">' +
      '<span class="exp-brace">{ </span><span class="exp-name">опыт</span>' +
      '<span class="exp-count">: ' + total + '</span><span class="exp-brace"> }</span>' +
      '</div>' +
      '<div class="exp-list">' + slots.map(itemHtml).join("") + '</div>';

    slots.forEach(function (slot) {
      slot.itemEl = document.getElementById("exp-" + slot.id);
    });

    function scrollToItem(id) {
      const target = document.getElementById("exp-" + id);
      if (target) target.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "center" });
    }

    slots.forEach(function (slot, i) {
      const pct = pctOf(i);
      const suffix = slot.kind === "prior" ? "-prior"
        : slot.kind === "job" ? "-job"
        : slot.kind === "present" ? "-present"
        : "";

      const dot = document.createElement("div");
      dot.className = "tl-dot" + (suffix ? " tl-dot" + suffix : "");
      dot.style.top = pct + "%";
      dot.title = slot.data.title;

      const label = document.createElement("div");
      label.className = "tl-label" + (suffix ? " tl-label" + suffix : "");
      label.style.top = pct + "%";
      label.textContent = labelFor(slot);

      dot.addEventListener("click", function () {
        select(slot.id);
        scrollToItem(slot.id);
      });
      dotsEl.appendChild(dot);
      dotsEl.appendChild(label);

      slot.dot = dot;
      slot.pct = pct;
    });

    function select(id) {
      if (id === active) return;
      active = id;

      let current = null;
      slots.forEach(function (slot) {
        const on = slot.id === id;
        if (on) current = slot;
        slot.dot.classList.toggle("active", on);
        if (slot.itemEl) slot.itemEl.classList.toggle("active", on);
      });
      if (!current) return;

      progressEl.style.height = current.pct + "%";
    }

    select(slots[slots.length - 1].id);
    document.getElementById("hero-timeline").classList.add("show");
  });
}

// Рельс fixed во вьюпорте: в hero — полный, вне hero (скролл > 12vh) — компакт
function initRailMode() {
  const rail = document.getElementById("hero-timeline");
  if (!rail) return;
  let compact = null;
  function update() {
    const next = window.scrollY > window.innerHeight * 0.12;
    if (next !== compact) {
      compact = next;
      rail.classList.toggle("compact", compact);
    }
  }
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  update();
}

document.addEventListener("DOMContentLoaded", function () {
  initTimeline();
  initRailMode();
});
