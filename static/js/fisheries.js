async function loadFisheriesData() {
    const apiUrl = '/api/fisheries';  // ходим на свой бекенд

    const loadingEl = document.getElementById('fisheries-loading');
    const dataEl = document.getElementById('fisheries-data');
    const errorEl = document.getElementById('fisheries-error');

    if (!loadingEl || !dataEl || !errorEl) {
        return;
    }

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error('Backend response was not ok');
        }

        const json = await response.json();
        if (!Array.isArray(json) || json.length === 0) {
            throw new Error('Нет данных по вылову');
        }

        const last = json[json.length - 1];
        const year = last.year;
        const catchTons = last.catch;

        loadingEl.classList.add('d-none');
        dataEl.classList.remove('d-none');

        dataEl.textContent =
            `По данным OpenFisheries, общий вылов рыбы в ${year} году ` +
            `составил ${catchTons.toLocaleString('ru-RU')} тонн.`;
    } catch (err) {
        console.error('Ошибка при загрузке данных:', err);
        loadingEl.classList.add('d-none');
        errorEl.classList.remove('d-none');
        errorEl.textContent = 'Не удалось загрузить статистику вылова 🐟';
    }
}

document.addEventListener('DOMContentLoaded', loadFisheriesData);