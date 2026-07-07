(function () {
    var TYPE_SPEED = 60;
    var LINE_PAUSE = 300;
    var CHAR_SPEED = 25;

    var introLines = [
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

    function appendHTML(el, html) {
        var tmp = document.createElement('div');
        tmp.innerHTML = html;
        while (tmp.firstChild) {
            el.appendChild(tmp.firstChild);
        }
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

    function showPrompt(contentEl) {
        var hint = document.createElement('div');
        hint.className = 'terminal-hint';
        hint.textContent = '# Ask me anything about my experience, projects, or skills';
        contentEl.appendChild(hint);

        var promptLine = document.createElement('div');
        promptLine.className = 'terminal-input-line';

        var prompt = document.createElement('span');
        prompt.className = 'prompt';
        prompt.textContent = '$ ';

        var input = document.createElement('input');
        input.className = 'terminal-input';
        input.type = 'text';
        input.placeholder = 'ask a question...';
        input.spellcheck = false;
        input.autocomplete = 'off';

        promptLine.appendChild(prompt);
        promptLine.appendChild(input);
        contentEl.appendChild(promptLine);

        input.focus();
        input.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && input.value.trim()) {
                var question = input.value.trim();
                input.disabled = true;
                input.classList.add('done');
                handleQuestion(contentEl, question);
            }
        });

        contentEl.parentElement.addEventListener('click', function () {
            if (!input.disabled) input.focus();
        });
    }

    function handleQuestion(contentEl, question) {
        var hint = contentEl.querySelector('.terminal-hint');
        if (hint) hint.remove();

        var inputLine = contentEl.querySelector('.terminal-input-line');
        if (inputLine) inputLine.remove();

        var qLine = document.createElement('div');
        qLine.innerHTML = '<span class="prompt">$ </span><span class="arg">' + escapeHTML(question) + '</span>';
        contentEl.appendChild(qLine);

        var thinkingLine = document.createElement('div');
        thinkingLine.className = 'terminal-thinking';
        thinkingLine.innerHTML = '<span class="prompt">... </span><span class="thinking-text">thinking</span>';
        contentEl.appendChild(thinkingLine);

        var answerBlock = document.createElement('div');
        answerBlock.className = 'terminal-answer';
        contentEl.appendChild(answerBlock);

        var evtSource = new EventSource('/api/ask/?q=' + encodeURIComponent(question));
        var thinkingDots = 0;
        var thinkingInterval = setInterval(function () {
            thinkingDots = (thinkingDots + 1) % 4;
            var dots = '.'.repeat(thinkingDots);
            var thinkingEl = thinkingLine.querySelector('.thinking-text');
            if (thinkingEl) thinkingEl.textContent = 'thinking' + dots;
        }, 400);

        evtSource.onmessage = function (event) {
            var data = JSON.parse(event.data);

            if (data.status === 'thinking') {
                clearInterval(thinkingInterval);
                thinkingLine.remove();
                return;
            }

            if (data.chunk) {
                var span = document.createElement('span');
                span.textContent = data.chunk;
                answerBlock.appendChild(span);
                contentEl.parentElement.scrollTop = contentEl.parentElement.scrollHeight;
            }

            if (data.done || data.error) {
                evtSource.close();
                clearInterval(thinkingInterval);
                thinkingLine.remove();
                showPrompt(contentEl);
            }
        };

        evtSource.onerror = function () {
            evtSource.close();
            clearInterval(thinkingInterval);
            thinkingLine.remove();
            var errDiv = document.createElement('div');
            errDiv.className = 'terminal-error';
            errDiv.textContent = 'Connection error. Try again.';
            contentEl.appendChild(errDiv);
            showPrompt(contentEl);
        };
    }

    function escapeHTML(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
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
                    showPrompt(contentEl);
                });
            }, 400);
        }, 3500);
    });
})();
