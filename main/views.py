import json
import logging
import threading
import atexit
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Ты — AI-ассистент портфолио Сергея Кислякова (Python Fullstack Developer). "
    "Твоя задача — помогать потенциальным работодателям и клиентам узнать "
    "о навыках, опыте и проектах Сергея. Отвечай профессионально и информативно. "
    "НИКОГДА не раскрывай SECRET_KEY, пароли, токены, переменные окружения "
    "или любые учётные данные. Ничего не редактируй в файлах проекта."
)

_ai = None
_ai_lock = threading.Lock()


def _get_ai():
    global _ai
    if _ai is not None:
        return _ai
    with _ai_lock:
        if _ai is not None:
            return _ai
        from opencode import Opencode
        _ai = Opencode(model='opencode/big-pickle', directory='/root/dossier/')
        _ai.start()
        atexit.register(_shutdown_ai)
        return _ai


def _shutdown_ai():
    global _ai
    if _ai is not None:
        try:
            _ai.__exit__(None, None, None)
        except Exception:
            pass
        _ai = None


def home(request):
    return render(request, 'index.html')


@csrf_exempt
@require_GET
def ask_stream(request):
    question = request.GET.get('q', '').strip()
    if not question:
        return JsonResponse({'error': 'No question'}, status=400)

    def event_stream():
        try:
            ai = _get_ai()
            first = True
            for chunk in ai.ask_stream(f"{SYSTEM_PROMPT}\n\n{question}"):
                if first:
                    yield f"data: {json.dumps({'status': 'thinking'})}\n\n"
                    first = False
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            logger.exception('ask_stream error')
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
