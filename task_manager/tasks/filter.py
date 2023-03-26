import django_filters
from django import forms
from .models import Task
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
    )
    own_tasks = django_filters.BooleanFilter(
        method='show_own_tasks',
        widget=forms.CheckboxInput,
        label=_('Own tasks only')
    )

    def show_own_tasks(self, queryset, arg, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
