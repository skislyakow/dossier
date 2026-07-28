import json
from django import forms
from django.utils.safestring import mark_safe


ICONS_CATEGORIES = {
    'Programming': [
        'code', 'code_off', 'data_object', 'data_array', 'functions',
        'terminal', 'javascript', 'css', 'html', 'python',
        'database', 'storage', 'cloud', 'dns', 'api',
        'menu_book', 'school', 'auto_awesome', 'smart_toy',
    ],
    'DevOps': [
        'settings', 'build', 'construction', 'deployed_code',
        'deployed_code_update', 'deployed_code_history', 'network_node',
        'dns', 'cloud_sync', 'cloud_done', 'cloud_queue',
        'docker', 'kubernetes',
    ],
    'Tools': [
        'terminal', 'bug_report', 'integration_instructions',
        'account_tree', 'account_balance', 'schema',
        'science', 'biotech', 'psychology', 'neurology',
        'troubleshoot', 'frame_source', 'manage_search',
        'search', 'tune', 'filter_alt', 'sort',
    ],
    'Git': [
        'commit', 'branch', 'merge', 'merge_type',
        'fork_left', 'fork_right', 'call_split',
        'call_merge', 'call_made', 'call_received',
        'compare_arrows', 'update', 'downloading',
    ],
    'Data': [
        'dataset', 'dataset_linked', 'table', 'table_rows',
        'database', 'bar_chart', 'pie_chart', 'trending_up',
        'trending_down', 'monitoring', 'analytics', 'insights',
        'data_exploration', 'data_thresholding', 'data_alert',
        'cognition', 'neurology', 'psychology',
    ],
    'Communication': [
        'mail', 'send', 'chat', 'sms', 'call',
        'telegram', 'whatsapp', 'link', 'hub',
        'notifications', 'campaign', 'rss_feed',
    ],
    'Web': [
        'public', 'language', 'web', 'webhook', 'http',
        'globe', 'travel_explore', 'explore', 'new_window',
        'iframe', 'frames_wireless', 'publish',
    ],
    'Design': [
        'palette', 'colorize', 'design_services', 'draw',
        'brush', 'style', 'text_fields', 'format_bold',
        'format_italic', 'auto_fix', 'magic',
    ],
}

COMMON_ICONS = [icon for icons in ICONS_CATEGORIES.values() for icon in icons]


class IconPickerWidget(forms.TextInput):
    template_name = 'admin/widgets/icon_picker.html'

    class Media:
        css = {
            'all': ['admin/css/icon-picker.css'],
        }
        js = ['admin/js/icon-picker.js']

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['categories'] = ICONS_CATEGORIES
        return context


GITHUB_BADGES = [
    {"label": "stars", "source": "github_stars", "icon": "star"},
    {"label": "forks", "source": "github_forks", "icon": "call_split"},
    {"label": "issues", "source": "github_issues", "icon": "track_changes"},
    {"label": "license", "source": "github_license", "icon": "balance"},
    {"label": "language", "source": "github_lang", "icon": "code"},
    {"label": "size", "source": "github_size", "icon": "hard_drive"},
    {"label": "created", "source": "github_created", "icon": "calendar_today"},
    {"label": "updated", "source": "github_updated", "icon": "update"},
]

PYPI_BADGES = [
    {"label": "pypi", "source": "pypi_version", "icon": "package_2"},
    {"label": "python", "source": "pypi_python", "icon": "terminal"},
    {"label": "license", "source": "pypi_license", "icon": "balance"},
    {"label": "downloads/m", "source": "pypistats_month", "icon": "download"},
    {"label": "downloads total", "source": "pypistats_total", "icon": "download_done"},
]


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
        catalog_json = json.dumps({'github': GITHUB_BADGES, 'pypi': PYPI_BADGES})

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
