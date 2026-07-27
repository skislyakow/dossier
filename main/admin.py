from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from adminsortable2.admin import SortableAdminMixin
from .models import Skill, Project, TimelineItem, ContactInfo
from .widgets import IconPickerWidget


@admin.register(Skill)
class SkillAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ['icon_display', 'name', 'size', 'sort_order']
    search_fields = ['name']
    list_filter = ['size']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'icon' in form.base_fields:
            form.base_fields['icon'].widget = IconPickerWidget()
        return form

    def icon_display(self, obj):
        if obj.icon:
            return format_html(
                '<span class="material-symbols-outlined" style="font-size:20px;vertical-align:middle">{}</span>',
                obj.icon
            )
        return ''
    icon_display.short_description = ''


@admin.register(Project)
class ProjectAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ['title', 'role', 'sort_order', 'is_published']
    list_editable = ['is_published']
    search_fields = ['title', 'tagline', 'role']
    list_filter = ['is_published', 'role']
    fieldsets = [
        (None, {
            'fields': ['title', 'tagline', 'role', 'repo', 'pypi'],
        }),
        ('Content', {
            'fields': ['features', 'badges_config'],
        }),
        ('Links', {
            'fields': ['links'],
            'classes': ['collapse'],
        }),
        ('Meta', {
            'fields': ['is_published'],
        }),
    ]


@admin.register(TimelineItem)
class TimelineItemAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ['title', 'item_type', 'date_label', 'sort_order']
    list_filter = ['item_type']
    search_fields = ['title', 'description']
    fieldsets = [
        (None, {
            'fields': ['item_type', 'date_label', 'title'],
        }),
        ('Details', {
            'fields': ['description', 'role', 'repo', 'url'],
        }),
        ('Meta', {
            'fields': ['date_range'],
        }),
    ]


@admin.register(ContactInfo)
class ContactInfoAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ['contact_type', 'label', 'sort_order']
    list_filter = ['contact_type']
