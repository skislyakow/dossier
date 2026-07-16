function initTimeline() {
  const dotsEl = document.getElementById("timeline-dots");
  const detailsEl = document.getElementById("timeline-details");
  const progressEl = document.getElementById("timeline-progress");
  if (!dotsEl) return;

  fetch('/api/timeline/').then(function (r) { return r.json(); }).then(function (data) {
    const JOB = data.job;
    const PRESENT = data.present;
    const TIMELINE = data.timeline;
    let active = "present";

    function scrollToDetails() {
      setTimeout(function () {
        detailsEl.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    }

    TIMELINE.forEach(function (item, i) {
      var pct = TIMELINE.length > 1 ? ((i + 1) / (TIMELINE.length + 1)) * 100 : 50;

      var dot = document.createElement("div");
      dot.className = "tl-dot";
      dot.style.left = pct + "%";
      dot.title = item.title;

      var label = document.createElement("div");
      label.className = "tl-label";
      label.style.left = pct + "%";
      label.textContent = item.date;

      dot.addEventListener("click", function () {
        select("project-" + i);
        scrollToDetails();
      });
      dotsEl.appendChild(dot);
      dotsEl.appendChild(label);
    });

    // job start dot at 0%
    var jobDot = document.createElement("div");
    jobDot.className = "tl-dot tl-dot-job";
    jobDot.style.left = "0%";
    jobDot.title = JOB.title;
    var jobLabel = document.createElement("div");
    jobLabel.className = "tl-label tl-label-job";
    jobLabel.style.left = "0%";
    jobLabel.textContent = JOB.dateRange.split(" — ")[0];
    jobDot.addEventListener("click", function () {
      select("job");
      scrollToDetails();
    });
    dotsEl.appendChild(jobDot);
    dotsEl.appendChild(jobLabel);

    // present dot at 100%
    var presentDot = document.createElement("div");
    presentDot.className = "tl-dot tl-dot-present";
    presentDot.style.left = "100%";
    presentDot.title = PRESENT.title;
    var presentLabel = document.createElement("div");
    presentLabel.className = "tl-label tl-label-present";
    presentLabel.style.left = "100%";
    presentLabel.textContent = "сейчас";
    presentDot.addEventListener("click", function () {
      select("present");
      scrollToDetails();
    });
    dotsEl.appendChild(presentDot);
    dotsEl.appendChild(presentLabel);

    select("present");
    document.getElementById("hero-timeline").classList.add("show");

  function select(id) {
    if (id === active) return;
    active = id;
    const isJob = id === "job";
    const isPresent = id === "present";

    dotsEl.querySelectorAll(".tl-dot:not(.tl-dot-job):not(.tl-dot-present)").forEach(function (d, i) {
      d.classList.toggle("active", !isJob && !isPresent && i === TIMELINE.length - 1);
    });
    var jobDotEl = dotsEl.querySelector(".tl-dot-job");
    if (jobDotEl) jobDotEl.classList.toggle("active", isJob);
    var presentDotEl = dotsEl.querySelector(".tl-dot-present");
    if (presentDotEl) presentDotEl.classList.toggle("active", isPresent);

    if (isJob) {
      progressEl.style.width = "0%";
      detailsEl.innerHTML = [
        '<div class="tl-details-card tl-details-card--job">',
        '  <div class="tl-details-job-range">' + JOB.dateRange + "</div>",
        '  <h4 class="tl-details-title">' + JOB.title + "</h4>",
        '  <div class="tl-details-job-role">' + JOB.role + "</div>",
        '  <p class="tl-details-desc">' + (JOB.desc || "Описание пока не добавлено") + "</p>",
        '  <a href="' + JOB.url + '" target="_blank" rel="noopener noreferrer" class="tl-details-link">',
        '    efko.digital',
        "  </a>",
        "</div>",
      ].join("\n");
    } else if (isPresent) {
      progressEl.style.width = "100%";
      detailsEl.innerHTML = [
        '<div class="tl-details-card tl-details-card--present">',
        '  <h4 class="tl-details-title">' + PRESENT.title + "</h4>",
        '  <p class="tl-details-desc">' + PRESENT.desc + "</p>",
        "</div>",
      ].join("\n");
    } else {
      const idx = parseInt(id.split("-")[1], 10);
      dotsEl.querySelectorAll(".tl-dot:not(.tl-dot-job):not(.tl-dot-present)").forEach((d, i) => {
        d.classList.toggle("active", i === idx);
      });
      if (jobDotEl) jobDotEl.classList.remove("active");
      if (presentDotEl) presentDotEl.classList.remove("active");
      progressEl.style.width = ((idx + 1) / (TIMELINE.length + 1) * 100) + "%";

      const item = TIMELINE[idx];
      detailsEl.innerHTML = [
        '<div class="tl-details-card">',
        '  <div class="tl-details-date">' + item.date + "</div>",
        '  <h4 class="tl-details-title">' + item.title + "</h4>",
        '  <p class="tl-details-desc">' + item.desc + "</p>",
        '  <a href="https://github.com/' + item.repo + '" target="_blank" rel="noopener noreferrer" class="tl-details-link">',
        '    <svg height="14" width="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
        "    GitHub",
        "  </a>",
        "</div>",
      ].join("\n");
    }
    detailsEl.classList.add("show");
  }
  });
}

document.addEventListener("DOMContentLoaded", function () {
  setTimeout(initTimeline, 3600);
});
