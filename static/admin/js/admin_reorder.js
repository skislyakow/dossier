(function () {
  const originalSortRecords = window.sortRecords;

  window.sortRecords = function (e) {
    if (originalSortRecords) {
      originalSortRecords(e);
    }

    const table = e.from;
    const orderingField = table.dataset.orderingField;
    if (!orderingField) return;

    const rows = table.querySelectorAll('tbody[data-pk]');
    const items = Array.from(rows).map(function (tbody) {
      return parseInt(tbody.getAttribute('data-pk'), 10);
    });

    if (!items.length) return;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfToken) return;

    fetch(window.location.pathname + 'reorder/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken.value,
      },
      body: JSON.stringify({ items: items }),
    })
      .then(function (res) {
        if (res.ok) return res.json();
        throw new Error(res.statusText);
      })
      .then(function (data) {
        if (data.ok) {
          const msg = document.createElement('div');
          msg.className =
            'fixed top-4 right-4 z-50 px-4 py-2 rounded shadow-lg text-sm text-white bg-green-600';
          msg.textContent = 'Порядок сохранён';
          document.body.appendChild(msg);
          setTimeout(function () {
            msg.remove();
          }, 2000);
        }
      })
      .catch(function () {
        const msg = document.createElement('div');
        msg.className =
          'fixed top-4 right-4 z-50 px-4 py-2 rounded shadow-lg text-sm text-white bg-red-600';
        msg.textContent = 'Ошибка сохранения порядка';
        document.body.appendChild(msg);
        setTimeout(function () {
          msg.remove();
        }, 3000);
      });
  };
})();
