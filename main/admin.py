from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django import forms
from unfold.admin import ModelAdmin
from .models import Skill, Project, TimelineItem, ContactInfo
from .widgets import IconPickerWidget, BadgePickerWidget
from .admin_views import admin_reorder


class SortableAdminMixin:
    def get_urls(self):
        opts = self.model._meta
        custom = [
            path(
                'reorder/',
                admin_reorder,
                {'model_name': opts.model_name},
                name=f'{opts.app_label}_{opts.model_name}_reorder',
            ),
        ]
        return custom + super().get_urls()

    @property
    def media(self):
        base = super().media
        extra = forms.Media(js=['admin/js/admin_reorder.js'])
        return base + extra


@admin.register(Skill)
class SkillAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ['icon_display', 'name', 'size']
    search_fields = ['name']
    list_filter = ['size']
    ordering_field = 'sort_order'
    hide_ordering_field = True

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
    list_display = ['title', 'role', 'is_published']
    list_editable = ['is_published']
    search_fields = ['title', 'tagline', 'role']
    list_filter = ['is_published', 'role']
    ordering_field = 'sort_order'
    hide_ordering_field = True
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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'badges_config' in form.base_fields:
            form.base_fields['badges_config'].widget = BadgePickerWidget()
        return form


@admin.register(TimelineItem)
class TimelineItemAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ['title', 'item_type', 'date_label']
    list_filter = ['item_type']
    search_fields = ['title', 'description']
    ordering_field = 'sort_order'
    hide_ordering_field = True
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
    list_display = ['contact_type', 'label']
    list_filter = ['contact_type']
    ordering_field = 'sort_order'
    hide_ordering_field = True
