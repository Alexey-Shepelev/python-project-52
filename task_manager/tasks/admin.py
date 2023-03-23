from django.contrib import admin
from .models import Task, TaskLabelRelation


# admin.site.register(Task)
class LabelInLine(admin.TabularInline):
    model = TaskLabelRelation


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [LabelInLine]
    list_display = (
        'id',
        'name',
        'creator',
        'get_labels',
        'executor',
        'created_at',
    )
