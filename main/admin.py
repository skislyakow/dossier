from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Skill, Project, TimelineItem, ContactInfo
from .widgets import IconPickerWidget


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ['icon_display', 'name', 'size', 'order']
    list_editable = ['size', 'order']
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
class ProjectAdmin(ModelAdmin):
    list_display = ['title', 'role', 'order', 'is_published']
    list_editable = ['order', 'is_published']
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
            'fields': ['order', 'is_published'],
        }),
    ]


@admin.register(TimelineItem)
class TimelineItemAdmin(ModelAdmin):
    list_display = ['title', 'item_type', 'date_label', 'order']
    list_editable = ['order']
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
            'fields': ['date_range', 'order'],
        }),
    ]


@admin.register(ContactInfo)
class ContactInfoAdmin(ModelAdmin):
    list_display = ['contact_type', 'label', 'order']
    list_editable = ['order']
    list_filter = ['contact_type']
