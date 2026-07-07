(function () {
    var TYPE_SPEED = 60;
    var LINE_PAUSE = 300;
    var LOOP_PAUSE = 3000;

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

    function typeTerminal(el, onComplete) {
        var contentEl = document.getElementById('terminal-content');
        var lineIdx = 0;
        var charIdx = 0;
        var currentHTML = '';

        function typeLine() {
            if (lineIdx >= lines.length) {
                setTimeout(onComplete, LOOP_PAUSE);
                return;
            }

            var line = lines[lineIdx];
            var fullHTML = buildLine(line);
            var plainText = line.prompt ? '$ ' + line.text : '> [' + line.item + '] ' + line.text;

            if (charIdx === 0) {
                currentHTML += (lineIdx > 0 ? '<br>' : '') + fullHTML.substring(0, 0);
            }

            charIdx++;
            if (charIdx <= plainText.length) {
                currentHTML = '';
                for (var i = 0; i <= lineIdx; i++) {
                    if (i > 0) currentHTML += '<br>';
                    currentHTML += buildLine(lines[i]);
                }
                contentEl.innerHTML = currentHTML;
                setTimeout(typeLine, TYPE_SPEED);
            } else {
                lineIdx++;
                charIdx = 0;
                setTimeout(typeLine, LINE_PAUSE);
            }
        }

        typeLine();
    }

    function loop() {
        var el = document.getElementById('terminal-content');
        el.innerHTML = '';
        typeTerminal(el, function () {
            loop();
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        setTimeout(loop, 800);
    });
})();
