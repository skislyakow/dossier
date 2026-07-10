const JOB = {
  title: "ЭФКО Цифровые решения",
  role: "ИТ-Специалист",
  dateRange: "Январь 2026 — настоящее время",
  url: "https://efko.digital/",
  desc: "",
};

const TIMELINE = [
  {
    date: "Апрель 2026",
    title: "Dossier",
    desc: "Персональный сайт-визитка: Django + Gunicorn + Nginx на VPS, CI/CD через GitHub Actions",
    repo: "skislyakow/dossier",
  },
  {
    date: "Июнь 2026",
    title: "Онлайн библиотека",
    desc: "Генератор статического сайта на Jinja2 + Bootstrap 5. 92 книги с пагинацией, обложками и чтением онлайн.",
    repo: "skislyakow/online_library",
  },
  {
    date: "Июнь 2026",
    title: "Ferma",
    desc: "Автоматизированная ферма Telegram-каналов: парсинг доноров, фильтрация рекламы, автоперевод, CPA-ссылки.",
    repo: "skislyakow/ferma",
  },
  {
    date: "Июнь 2026",
    title: "Devman Bot",
    desc: "Telegram-бот для уведомлений о проверке работ на Devman через Long Polling API.",
    repo: "skislyakow/devman-bot",
  },
  {
    date: "Июль 2026",
    title: "opencode-py",
    desc: "Python SDK для opencode AI агента: sync + async API, SSE-стриминг, опубликован на PyPI.",
    repo: "skislyakow/opencode-py",
  },
];

function initTimeline() {
  const trackEl = document.querySelector(".timeline-track");
  const jobEl = document.getElementById("timeline-job");
  const dotsEl = document.getElementById("timeline-dots");
  const detailsEl = document.getElementById("timeline-details");
  const progressEl = document.getElementById("timeline-progress");
  let active = "project-4";

  if (!dotsEl) return;

  function scrollToDetails() {
    setTimeout(function () {
      detailsEl.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);
  }

  TIMELINE.forEach((item, i) => {
    // projects from 20% to 100%, leaving 0% for job dot
    var pct = TIMELINE.length > 1 ? ((i + 1) / TIMELINE.length) * 100 : 100;

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

  // job start dot at 0% (logically before April)
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

  // SVG arrow from job dot up-right to job bar
  var arrowSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  arrowSvg.setAttribute("class", "tl-job-arrow");
  arrowSvg.setAttribute("viewBox", "0 0 100 60");
  arrowSvg.setAttribute("preserveAspectRatio", "none");
  arrowSvg.innerHTML =
    '<defs><marker id="arrhead" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">' +
    '<path d="M 0 1 L 9 5 L 0 9 z" fill="#e4b592"/></marker></defs>' +
    '<path d="M 2 30 Q 5 20, 8 12" stroke="#e4b592" fill="none" stroke-width="1.5" marker-end="url(#arrhead)"/>';
  trackEl.appendChild(arrowSvg);

  jobEl.addEventListener("click", function () {
    select("job");
    scrollToDetails();
  });
  jobEl.innerHTML = [
    '<span class="tl-job-title">' + JOB.title + '<span class="tl-job-role">' + JOB.role + "</span></span>",
  ].join("\n");
  select("project-" + (TIMELINE.length - 1));

  document.getElementById("hero-timeline").classList.add("show");

  function select(id) {
    if (id === active) return;
    active = id;
    const isJob = id === "job";

    dotsEl.querySelectorAll(".tl-dot:not(.tl-dot-job)").forEach(function (d, i) {
      d.classList.toggle("active", !isJob && i === TIMELINE.length - 1);
    });
    var jobDotEl = dotsEl.querySelector(".tl-dot-job");
    if (jobDotEl) jobDotEl.classList.toggle("active", isJob);
    jobEl.classList.toggle("active", isJob);

    if (isJob) {
      progressEl.style.width = "100%";
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
    } else {
      const idx = parseInt(id.split("-")[1], 10);
      dotsEl.querySelectorAll(".tl-dot:not(.tl-dot-job)").forEach((d, i) => {
        d.classList.toggle("active", i === idx);
      });
      if (jobDotEl) jobDotEl.classList.remove("active");
      progressEl.style.width = ((idx + 1) / TIMELINE.length * 100) + "%";

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
}

document.addEventListener("DOMContentLoaded", () => {
  setTimeout(initTimeline, 3600);
});
