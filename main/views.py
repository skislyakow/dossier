import json
import logging
import time
import threading
import atexit
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

logger = logging.getLogger(__name__)

_server = None
_server_lock = threading.Lock()


def _get_server():
    global _server
    if _server is not None:
        return _server
    with _server_lock:
        if _server is not None:
            return _server
        from opencode import Opendcode
        _server = Opendcode.__new__(Opendcode)
        _server._started = True
        atexit.register(_shutdown_server)
        return _server


def _shutdown_server():
    global _server
    if _server is not None:
        try:
            _server.__exit__(None, None, None)
        except Exception:
            pass
        _server = None


def home(request):
    return render(request, 'index.html')


@csrf_exempt
@require_POST
def ask_api(request):
    try:
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        if not question:
            return JsonResponse({'error': 'No question provided'}, status=400)

        from opencode import opencode
        answer = opencode(question, keep=True)
        return JsonResponse({'answer': answer})
    except Exception as e:
        logger.exception('ask_api error')
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
def ask_stream(request):
    question = request.GET.get('q', '').strip()
    if not question:
        return JsonResponse({'error': 'No question'}, status=400)

    def event_stream():
        try:
            from opencode import Opencode
            with Opencode(model='opencode/big-pickle') as ai:
                first = True
                for chunk in ai.ask_stream(question):
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
