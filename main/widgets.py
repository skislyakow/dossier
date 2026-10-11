import json
from django import forms
from django.utils.safestring import mark_safe
from .badge_utils import catalog as badge_catalog


class BadgePickerWidget(forms.Widget):
    class Media:
        css = {'all': ['admin/css/badge-picker.css']}
        js = ['admin/js/badge-picker.js']

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                value = []

        widget_id = attrs.get('id', f'id-{name}')
        catalog_json = json.dumps(badge_catalog())

        return mark_safe(
            '<div class="badge-picker" '
            f'data-bp-catalog=\'{catalog_json}\' '
            f'data-bp-value=\'{json.dumps(value)}\' '
            f'data-bp-name="{name}" '
            f'data-bp-id="{widget_id}" '
            'x-data="badgePicker($el)">'

            '<div class="bp-catalog">'
            # GitHub
            '<div class="bp-group">'
            '<div class="bp-group__title">GitHub</div>'
            '<div class="bp-group__items">'
            '<template x-for="badge in catalog.github" :key="badge.source">'
            '<button type="button" class="bp-catalog__item"'
            ' :class="{\'bp-catalog__item--active\': isActive(badge.source)}"'
            ' x-on:click="toggle(badge)">'
            '<span class="material-symbols-outlined bp-catalog__icon" x-text="badge.icon"></span>'
            '<span class="bp-catalog__label" x-text="badge.label"></span>'
            '</button>'
            '</template>'
            '</div>'
            '</div>'
            # PyPI
            '<div class="bp-group">'
            '<div class="bp-group__title">PyPI</div>'
            '<div class="bp-group__items">'
            '<template x-for="badge in catalog.pypi" :key="badge.source">'
            '<button type="button" class="bp-catalog__item"'
            ' :class="{\'bp-catalog__item--active\': isActive(badge.source)}"'
            ' x-on:click="toggle(badge)">'
            '<span class="material-symbols-outlined bp-catalog__icon" x-text="badge.icon"></span>'
            '<span class="bp-catalog__label" x-text="badge.label"></span>'
            '</button>'
            '</template>'
            '</div>'
            '</div>'
            # Custom
            '<div class="bp-group">'
            '<div class="bp-group__title">Custom</div>'
            '<div class="bp-group__items">'
            '<button type="button" class="bp-catalog__item bp-catalog__item--add" x-on:click="addLabel()">'
            '<span class="material-symbols-outlined bp-catalog__icon">add</span>'
            '<span class="bp-catalog__label">Label</span>'
            '</button>'
            '<button type="button" class="bp-catalog__item bp-catalog__item--add" x-on:click="addStatic()">'
            '<span class="material-symbols-outlined bp-catalog__icon">add</span>'
            '<span class="bp-catalog__label">Custom</span>'
            '</button>'
            '</div>'
            '</div>'
            '</div>'

            # Active badges
            '<div class="bp-active">'
            '<div class="bp-active__list">'
            '<template x-for="(badge, index) in active" :key="index">'
            '<div class="bp-active__item">'
            '<span class="bp-badge" :class="{\'bp-badge--single\': !badge.source && !badge.value}">'
            '<span class="bp-badge__label" x-text="badge.label"></span>'
            '<template x-if="badge.source">'
            '<span class="bp-badge__source" x-text="badge.source"></span>'
            '</template>'
            '<template x-if="badge.value && !badge.source">'
            '<span class="bp-badge__value" x-text="badge.value"></span>'
            '</template>'
            '</span>'
            '<button type="button" class="bp-active__remove" x-on:click="remove(index)">'
            '<span class="material-symbols-outlined">close</span>'
            '</button>'
            '</div>'
            '</template>'
            '<div class="bp-active__empty" x-show="active.length === 0">Нет активных бейджей</div>'
            '</div>'
            '</div>'

            # Hidden input
            f'<input type="hidden" name="{name}" :value="JSON.stringify(active)" id="{widget_id}">'
            '</div>'
        )

    def value_from_datadict(self, data, files, name):
        raw = data.get(name, '[]')
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return []
