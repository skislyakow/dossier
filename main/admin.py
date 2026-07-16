from django.contrib import admin
from .models import Skill, Project, TimelineItem, ContactInfo


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'order']
    list_editable = ['size', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'role', 'order', 'is_published']
    list_editable = ['order', 'is_published']


@admin.register(TimelineItem)
class TimelineItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'item_type', 'date_label', 'order']
    list_editable = ['order']
    list_filter = ['item_type']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['contact_type', 'label', 'order']
    list_editable = ['order']
