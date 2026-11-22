from django import template

register = template.Library()


@register.filter
def resume_lines(value: str | None) -> list[str]:
    """Описание записи CMS построчно — для маркированного списка в резюме."""
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]
