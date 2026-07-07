(function () {
    var TYPE_SPEED = 60;
    var LINE_PAUSE = 300;

    var introLines = [
        { prompt: true, text: './services.sh' },
        { item: 1, text: 'Telegram-боты' },
        { item: 2, text: 'Django-сайты' },
        { item: 3, text: 'API-интеграции' },
        { item: 4, text: 'Python SDK' },
        { item: 5, text: 'Парсинг данных' },
        { item: 6, text: 'Автоматизация' },
    ];

    function buildLine(line) {
        if (line.prompt) {
            return '<span class="prompt">$ </span><span class="arg">' + line.text + '</span>';
        }
        return '<span class="prompt">&gt; </span><span class="num">[' + line.item + ']</span> <span class="item">' + line.text + '</span>';
    }

    function escapeHTML(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
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

    function showPrompt(contentEl, showHint) {
        if (showHint) {
            var hint = document.createElement('div');
            hint.className = 'terminal-hint';
            hint.textContent = '# Ask me anything about my experience, projects, or skills';
            contentEl.appendChild(hint);
        }

        var promptLine = document.createElement('div');
        promptLine.className = 'terminal-input-line';

        var prompt = document.createElement('span');
        prompt.className = 'prompt';
        prompt.textContent = '$ ';

        var cursor = document.createElement('span');
        cursor.className = 'terminal-cursor blink';
        cursor.textContent = '█';

        var input = document.createElement('input');
        input.className = 'terminal-input';
        input.type = 'text';
        input.placeholder = 'ask a question...';
        input.spellcheck = false;
        input.autocomplete = 'off';

        promptLine.appendChild(prompt);
        promptLine.appendChild(cursor);
        promptLine.appendChild(input);
        contentEl.appendChild(promptLine);

        input.focus();
        input.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && input.value.trim()) {
                var question = input.value.trim();
                input.disabled = true;
                input.classList.add('done');
                cursor.remove();
                handleQuestion(contentEl, question);
            }
        });

        contentEl.parentElement.addEventListener('click', function () {
            if (!input.disabled) input.focus();
        });
    }

    function handleQuestion(contentEl, question) {
        var qLine = document.createElement('div');
        qLine.innerHTML = '<span class="prompt">$ </span><span class="arg">' + escapeHTML(question) + '</span>';
        contentEl.appendChild(qLine);

        var thinkingLine = document.createElement('div');
        thinkingLine.className = 'terminal-thinking';
        thinkingLine.innerHTML = '<span class="prompt">... </span><span class="thinking-text">thinking</span>';
        contentEl.appendChild(thinkingLine);

        var answerPrefix = document.createElement('div');
        answerPrefix.className = 'terminal-answer-prefix';
        answerPrefix.innerHTML = '<span class="prompt">&gt; </span>';
        answerPrefix.style.display = 'none';
        contentEl.appendChild(answerPrefix);

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
                answerPrefix.style.display = '';
                return;
            }

            if (data.chunk) {
                var span = document.createElement('span');
                span.textContent = data.chunk;
                answerBlock.appendChild(span);
                contentEl.parentElement.scrollTop = contentEl.parentElement.scrollHeight;
            }

            if (data.error) {
                answerPrefix.style.display = '';
                answerBlock.classList.add('terminal-error');
                answerBlock.textContent = data.error;
            }

            if (data.done || data.error) {
                evtSource.close();
                clearInterval(thinkingInterval);
                thinkingLine.remove();
                showPrompt(contentEl, false);
            }
        };

        evtSource.onerror = function () {
            evtSource.close();
            clearInterval(thinkingInterval);
            thinkingLine.remove();
            answerPrefix.style.display = '';
            var errDiv = document.createElement('div');
            errDiv.className = 'terminal-error';
            errDiv.textContent = 'Connection error. Try again.';
            contentEl.appendChild(errDiv);
            showPrompt(contentEl, false);
        };
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
                    showPrompt(contentEl, true);
                });
            }, 400);
        }, 3500);
    });
})();
