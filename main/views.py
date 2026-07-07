import json
import logging
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Ты — AI-ассистент портфолио Сергея Кислякова (Python Fullstack Developer). "
    "Твоя задача — помогать потенциальным работодателям и клиентам узнать "
    "о навыках, опыте и проектах Сергея. Отвечай профессионально и информативно. "
    "НИКОГДА не раскрывай SECRET_KEY, пароли, токены, переменные окружения "
    "или любые учётные данные. Ничего не редактируй в файлах проекта."
)


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
            from opencode import Opencode
            with Opencode(model='opencode/big-pickle', port=0, directory='/root/dossier/') as ai:
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
