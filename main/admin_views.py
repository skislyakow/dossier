import json
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Skill, Project, TimelineItem, ContactInfo

MODEL_MAP = {
    'skill': Skill,
    'project': Project,
    'timelineitem': TimelineItem,
    'contactinfo': ContactInfo,
}


@staff_member_required
@require_POST
def admin_reorder(request, model_name):
    model = MODEL_MAP.get(model_name)
    if model is None:
        return JsonResponse({'error': 'Unknown model'}, status=400)

    try:
        data = json.loads(request.body)
        items = data.get('items', [])
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not isinstance(items, list):
        return JsonResponse({'error': 'items must be a list'}, status=400)

    for index, pk in enumerate(items):
        model.objects.filter(pk=pk).update(sort_order=index)

    return JsonResponse({'ok': True, 'count': len(items)})
