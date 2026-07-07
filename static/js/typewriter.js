(function () {
    var TYPE_SPEED = 70;
    var ERASE_SPEED = 30;
    var PAUSE = 2000;

    var directionsText = "Telegram-боты · Django-сайты · API-интеграции · Python SDK · Парсинг данных · Автоматизация";
    var skillsText = "Python · Django · DRF · PostgreSQL · SQLite · Docker · Nginx · Gunicorn · GitHub Actions · Ubuntu · Git · REST API · asyncio · requests · httpx · Pydantic · PyPI · HTML · CSS · JavaScript";

    function typewriteLoop(elementId, text) {
        var el = document.getElementById(elementId);
        if (!el) return;

        function type() {
            var i = 0;
            var interval = setInterval(function () {
                el.textContent = text.substring(0, i + 1);
                i++;
                if (i >= text.length) {
                    clearInterval(interval);
                    setTimeout(erase, PAUSE);
                }
            }, TYPE_SPEED);
        }

        function erase() {
            var j = text.length;
            var interval = setInterval(function () {
                el.textContent = text.substring(0, j - 1);
                j--;
                if (j <= 0) {
                    clearInterval(interval);
                    setTimeout(type, PAUSE);
                }
            }, ERASE_SPEED);
        }

        type();
    }

    document.addEventListener("DOMContentLoaded", function () {
        setTimeout(function () {
            typewriteLoop("directions-text", directionsText);
            typewriteLoop("skills-text", skillsText);
        }, 500);
    });
})();
