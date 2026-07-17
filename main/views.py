import json
import logging
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .models import Skill, Project, TimelineItem, ContactInfo

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


def api_skills(request):
    skills = Skill.objects.all()
    return JsonResponse([
        {'name': s.name, 'size': s.size, 'icon': s.icon}
        for s in skills
    ], safe=False)


def api_projects(request):
    projects = Project.objects.filter(is_published=True)
    return JsonResponse([
        {
            'repo': p.repo,
            'pypi': p.pypi or None,
            'title': p.title,
            'role': p.role or None,
            'tagline': p.tagline,
            'features': p.features,
            'links': p.links,
            'badges': p.badges_config,
        }
        for p in projects
    ], safe=False)


def api_timeline(request):
    items = TimelineItem.objects.all()
    job = None
    present = None
    timeline = []

    for item in items:
        obj = {
            'date': item.date_label,
            'title': item.title,
            'desc': item.description,
        }
        if item.item_type == 'job':
            job = {
                'title': item.title,
                'role': item.role,
                'dateRange': item.date_range,
                'url': item.url,
                'desc': item.description,
            }
        elif item.item_type == 'present':
            present = {
                'title': item.title,
                'desc': item.description,
            }
        else:
            obj['repo'] = item.repo
            timeline.append(obj)

    return JsonResponse({
        'job': job,
        'present': present,
        'timeline': timeline,
    })


def api_contact(request):
    contacts = ContactInfo.objects.all()
    return JsonResponse([
        {
            'type': c.contact_type,
            'label': c.label,
            'value': c.value,
        }
        for c in contacts
    ], safe=False)
