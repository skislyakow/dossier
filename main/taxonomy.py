from collections import Counter

from .models import Project


def tag_counts():
    """Частота тегов по опубликованным проектам: {тег: N}."""
    counts = Counter()
    for tags in Project.objects.filter(is_published=True).values_list('tags', flat=True):
        counts.update(tags or [])
    return counts


def skill_size(count):
    """Размер тега по частоте: 5+ → xl / 3–4 → lg / 1–2 → md / 0 → sm."""
    if count >= 5:
        return 'xl'
    if count >= 3:
        return 'lg'
    if count >= 1:
        return 'md'
    return 'sm'


def resolve_tag(skill):
    """Тег проекта, по которому фильтрует навык: filter_tag, иначе имя навыка."""
    return skill.filter_tag or skill.name


def tag_cloud():
    """Облако тегов проектов: [{name, count, size}], по убыванию частоты."""
    counts = tag_counts()
    return [
        {'name': name, 'count': count, 'size': skill_size(count)}
        for name, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ]
