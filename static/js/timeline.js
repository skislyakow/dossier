function initTimeline() {
  const dotsEl = document.getElementById("timeline-dots");
  const experienceEl = document.getElementById("experience");
  const progressEl = document.getElementById("timeline-progress");
  if (!dotsEl || !experienceEl) return;

  fetch('/api/timeline/').then(function (r) { return r.json(); }).then(function (data) {
    const PRIOR = data.prior;
    const JOBS = data.jobs || [];
    const PRESENT = data.present;
    const TIMELINE = data.timeline || [];

    // Рельс компактный: prior (проф. деятельность) → проекты → present.
    // Все места работы живут только в секции «Опыт».
    const slots = [];
    if (PRIOR) slots.push({ id: "career", kind: "prior", data: PRIOR });
    TIMELINE.forEach(function (item, i) {
      slots.push({ id: "project-" + i, kind: "project", data: item });
    });
    if (PRESENT) slots.push({ id: "present", kind: "present", data: PRESENT });
    if (!slots.length && !JOBS.length) return;

    const total = slots.length;
    let active = null;

    function pctOf(index) {
      return total > 1 ? (index / (total - 1)) * 100 : 50;
    }

    function labelFor(slot) {
      if (slot.kind === "present") return "сейчас";
      if (slot.kind === "prior") return String(slot.data.date || "").slice(0, 4) || "вехи";
      return slot.data.date;
    }

    function bullets(text) {
      const lines = String(text || "").split("\n").map(function (line) {
        return line.trim();
      }).filter(Boolean);
      if (lines.length > 1) {
        return '<ul class="exp-bullets">' + lines.map(function (line) {
          return '<li>' + esc(line) + '</li>';
        }).join('') + '</ul>';
      }
      return lines.length ? '<p class="exp-desc">' + esc(lines[0]) + '</p>' : '';
    }

    // Строка секции «Опыт»: дата (моно) + заголовок + роль/описание/ссылка
    function itemHtml(slot) {
      const d = slot.data;
      const date = slot.kind === "job" ? (d.dateRange || d.date || "")
        : slot.kind === "present" ? "сейчас"
        : (d.date || "");
      const role = slot.kind === "job" && d.role
        ? '<div class="exp-role">' + esc(d.role) + '</div>'
        : "";
      const descText = slot.kind === "job" && !d.desc ? "Описание пока не добавлено" : (d.desc || "");
      const desc = bullets(descText);
      let link = "";
      if (slot.kind === "job" && d.url) {
        const host = String(d.url).replace(/^https?:\/\//, "").replace(/\/$/, "");
        link = '<a class="exp-link" href="' + esc(d.url) + '" target="_blank" rel="noopener noreferrer">' + esc(host) + '</a>';
      } else if (slot.kind === "project" && d.repo) {
        link = '<a class="exp-link" href="https://github.com/' + esc(d.repo) + '" target="_blank" rel="noopener noreferrer">GitHub</a>';
      }
      return '<div class="exp-item exp-item--' + slot.kind + '" id="exp-' + esc(slot.id) + '">' +
        '<div class="exp-date">' + esc(date) + '</div>' +
        '<h3 class="exp-title">' + esc(d.title) + '</h3>' +
        role + desc + link +
        '</div>';
    }

    const jobsHtml = JOBS.map(function (job, i) {
      return itemHtml({ id: "job-" + i, kind: "job", data: job });
    }).join('');
    const slotsHtml = slots.map(itemHtml).join('');

    experienceEl.innerHTML =
      '<div class="sec-label">' +
      '<span class="sec-brace">{ </span><span class="sec-name">опыт</span>' +
      '<span class="sec-count">: ' + (JOBS.length + slots.length) + '</span><span class="sec-brace"> }</span>' +
      '</div>' +
      (jobsHtml ? '<div class="exp-group-title">Работа</div><div class="exp-list">' + jobsHtml + '</div>' : '') +
      (slotsHtml ? '<div class="exp-group-title">Проекты и вехи</div><div class="exp-list">' + slotsHtml + '</div>' : '');

    slots.forEach(function (slot) {
      slot.itemEl = document.getElementById("exp-" + slot.id);
    });

    function scrollToItem(slot) {
      if (slot.itemEl) slot.itemEl.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "center" });
    }

    slots.forEach(function (slot, i) {
      const pct = pctOf(i);
      const suffix = slot.kind === "prior" ? "-prior"
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
        scrollToItem(slot);
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

    if (slots.length) {
      select(slots[slots.length - 1].id);
      document.getElementById("hero-timeline").classList.add("show");
    }
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
