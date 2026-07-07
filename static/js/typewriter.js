(function () {
    var TYPE_SPEED = 60;
    var LINE_PAUSE = 300;

    var lines = [
        { prompt: true, text: './services.sh' },
        { item: 1, text: 'Telegram-боты' },
        { item: 2, text: 'Django-сайты' },
        { item: 3, text: 'API-интеграции' },
        { item: 4, text: 'Python SDK' },
        { item: 5, text: 'Парсинг данных' },
        { item: 6, text: 'Автоматизация' },
        { prompt: true, text: '' }
    ];

    function buildLine(line) {
        if (line.prompt) {
            return '<span class="prompt">$ </span><span class="arg">' + line.text + '</span>';
        }
        return '<span class="prompt">&gt; </span><span class="num">[' + line.item + ']</span> <span class="item">' + line.text + '</span>';
    }

    function typeTerminal() {
        var contentEl = document.getElementById('terminal-content');
        var lineIdx = 0;

        function typeLine() {
            if (lineIdx >= lines.length) return;

            var fullHTML = '';
            for (var i = 0; i <= lineIdx; i++) {
                if (i > 0) fullHTML += '<br>';
                fullHTML += buildLine(lines[i]);
            }
            contentEl.innerHTML = fullHTML;
            lineIdx++;

            if (lineIdx < lines.length) {
                setTimeout(typeLine, LINE_PAUSE);
            }
        }

        typeLine();
    }

    document.addEventListener('DOMContentLoaded', function () {
        var terminal = document.querySelector('.terminal');
        var skillsCloud = document.querySelector('.skills-cloud');

        setTimeout(function () {
            terminal.classList.add('show');
            skillsCloud.classList.add('show');
            setTimeout(typeTerminal, 400);
        }, 3500);
    });
})();
