function initTimeline() {
  const dotsEl = document.getElementById("timeline-dots");
  const detailsEl = document.getElementById("timeline-details");
  const progressEl = document.getElementById("timeline-progress");
  if (!dotsEl) return;

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

    function scrollToDetails() {
      setTimeout(function () {
        const target = document.getElementById("timeline-details");
        if (target) target.scrollIntoView({ behavior: "smooth", block: "center" });
      }, 100);
    }

    function labelFor(slot) {
      if (slot.kind === "job") return (JOB.dateRange || "").split(" — ")[0] || JOB.title;
      if (slot.kind === "present") return "сейчас";
      return slot.data.date;
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
        scrollToDetails();
      });
      dotsEl.appendChild(dot);
      dotsEl.appendChild(label);

      slot.dot = dot;
      slot.pct = pct;
    });

    function cardFor(slot) {
      const d = slot.data;
      if (slot.kind === "prior") {
        return [
          '<div class="tl-details-card tl-details-card--prior">',
          '  <div class="tl-details-date">' + d.date + "</div>",
          '  <h4 class="tl-details-title">' + d.title + "</h4>",
          '  <p class="tl-details-desc">' + d.desc + "</p>",
          "</div>",
        ].join("\n");
      }
      if (slot.kind === "job") {
        return [
          '<div class="tl-details-card tl-details-card--job">',
          '  <div class="tl-details-job-range">' + d.dateRange + "</div>",
          '  <h4 class="tl-details-title">' + d.title + "</h4>",
          '  <div class="tl-details-job-role">' + d.role + "</div>",
          '  <p class="tl-details-desc">' + (d.desc || "Описание пока не добавлено") + "</p>",
          '  <a href="' + d.url + '" target="_blank" rel="noopener noreferrer" class="tl-details-link">',
          '    efko.digital',
          "  </a>",
          "</div>",
        ].join("\n");
      }
      if (slot.kind === "present") {
        return [
          '<div class="tl-details-card tl-details-card--present">',
          '  <h4 class="tl-details-title">' + d.title + "</h4>",
          '  <p class="tl-details-desc">' + d.desc + "</p>",
          "</div>",
        ].join("\n");
      }
      return [
        '<div class="tl-details-card">',
        '  <div class="tl-details-date">' + d.date + "</div>",
        '  <h4 class="tl-details-title">' + d.title + "</h4>",
        '  <p class="tl-details-desc">' + d.desc + "</p>",
        '  <a href="https://github.com/' + d.repo + '" target="_blank" rel="noopener noreferrer" class="tl-details-link">',
        '    <svg height="14" width="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
        "    GitHub",
        "  </a>",
        "</div>",
      ].join("\n");
    }

    function select(id) {
      if (id === active) return;
      active = id;

      let current = null;
      slots.forEach(function (slot) {
        const on = slot.id === id;
        if (on) current = slot;
        slot.dot.classList.toggle("active", on);
      });
      if (!current) return;

      progressEl.style.height = current.pct + "%";
      detailsEl.innerHTML = cardFor(current);
      detailsEl.classList.add("show");
    }

    select(slots[slots.length - 1].id);
    document.getElementById("hero-timeline").classList.add("show");
  });
}

document.addEventListener("DOMContentLoaded", function () {
  initTimeline();
});
