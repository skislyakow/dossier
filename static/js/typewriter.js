(function () {
    var TYPE_SPEED = 60;
    var LINE_PAUSE = 300;

    var introLines = [
        { prompt: true, text: './services.sh' },
        { item: 1, text: 'Telegram & VK-боты' },
        { item: 2, text: 'Django-сайты' },
        { item: 3, text: 'API-интеграции' },
        { item: 4, text: 'Python SDK' },
        { item: 5, text: 'Парсинг & NLP' },
        { item: 6, text: 'Автоматизация' },
    ];

    function buildLine(line) {
        if (line.prompt) {
            return '<span class="prompt">$ </span><span class="arg">' + line.text + '</span>';
        }
        return '<span class="prompt">&gt; </span><span class="num">[' + line.item + ']</span> <span class="item">' + line.text + '</span>';
    }

    function typeIntro(contentEl, onComplete) {
        var lineIdx = 0;

        function typeLine() {
            if (lineIdx >= introLines.length) {
                onComplete();
                return;
            }

            var html = '';
            for (var i = 0; i <= lineIdx; i++) {
                if (i > 0) html += '<br>';
                html += buildLine(introLines[i]);
            }
            contentEl.innerHTML = html;
            lineIdx++;

            if (lineIdx < introLines.length) {
                setTimeout(typeLine, LINE_PAUSE);
            } else {
                setTimeout(onComplete, LINE_PAUSE);
            }
        }

        typeLine();
    }

    function showStaticPrompt(contentEl) {
        var hint = document.createElement('div');
        hint.className = 'terminal-hint';
        hint.textContent = '# специализация и стек';
        contentEl.appendChild(hint);

        var promptLine = document.createElement('div');
        promptLine.className = 'terminal-input-line';
        promptLine.innerHTML = '<span class="prompt">$ </span>';
        contentEl.appendChild(promptLine);
    }

    document.addEventListener('DOMContentLoaded', function () {
        var terminal = document.querySelector('.terminal');
        var skillsCloud = document.querySelector('.skills-cloud');
        var contentEl = document.getElementById('terminal-content');

        setTimeout(function () {
            terminal.classList.add('show');
            skillsCloud.classList.add('show');
            setTimeout(function () {
                typeIntro(contentEl, function () {
                    showStaticPrompt(contentEl);
                });
            }, 400);
        }, 3500);
    });
})();
