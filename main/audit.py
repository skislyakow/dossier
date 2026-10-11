def audit_content():
    """Консистентность тегов проектов и навыков для кликабельной секции Skills.

    Возвращает (errors, warnings):
    - errors: тег опубликованного проекта не достижим ни одним навыком
      (по имени или filter_tag) — по технологии нет кнопки-навыка;
    - warnings: навык (по filter_tag или имени) не находит ни одного тега
      опубликованных проектов — клик даст пустую выдачу.
    """
    from .models import Project, Skill
    from .taxonomy import resolve_tag

    skills = list(Skill.objects.all())
    resolvable = {s.name for s in skills} | {s.filter_tag for s in skills if s.filter_tag}

    used_tags = set()
    for (tags,) in Project.objects.filter(is_published=True).values_list('tags'):
        used_tags.update(tags or [])

    errors = []
    missing_skills = used_tags - resolvable
    if missing_skills:
        errors.append(
            'Теги проектов без навыка: %s. Добавьте Skill с именем или filter_tag, '
            'равным тегу, иначе по технологии нет кликабельной кнопки.'
            % ', '.join(sorted(missing_skills)),
        )

    warnings = []
    no_match = {resolve_tag(s) for s in skills} - used_tags
    if no_match:
        warnings.append(
            'Навыки, чей фильтр не находит ни одного тега проектов: %s. '
            'Клик даст пустую выдачу — добавьте проект с таким тегом или поправьте filter_tag.'
            % ', '.join(sorted(no_match)),
        )

    return errors, warnings