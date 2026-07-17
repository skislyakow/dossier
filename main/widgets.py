from django import forms
from django.urls import reverse_lazy


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
